# -*- coding: utf-8 -*-
r"""Xenium 决策剧场 · 参数化预计算脚本（T1/T2 资产生产）

种子数据（本机）:
  HCC  F:\xenium数据\资源\resource-full_Xenium_V1_肝癌\           (V1 官方输出, 156,555 细胞 x 474 基因)
  CTRL F:\xenium数据\资源\resource-肝脏健康V1\                    (健康肝对照, 仅 zarr.zip)
  BRCA F:\xenium数据\ov工作流测试\simulator_precompute\raw\BRCA\  (10x Xenium FFPE Human Breast Cancer Rep1, cf.10xgenomics.com 单文件直链)
  CRC  F:\xenium数据\ov工作流测试\simulator_precompute\raw\CRC\   (执行期核实后下载)
  ZXM  F:\xenium数据\ZXM\RAW_DATA\output-XETG00099__0066171__Region_1__20260204__104132\output-XETG00099__0066171__Region_1__20260204__104132\
       (新版式完整输出, onboard analysis 复用 + <=3 万细胞抽样)

产出:
  docs\simulator\assets\<场景>\*.png          T1 图 (半分辨率 PNG)
  docs\simulator\assets\<场景>\coords\*.json.gz  T2 交互坐标 (<=3 万细胞, <=2MB/文件)
  docs\simulator\assets\<场景>\manifest.json  资产清单 + 每图三行式标注(来源/性质/参考文献)
  中间缓存 F:\xenium数据\ov工作流测试\simulator_precompute\cache\<场景>\  (不入 git)

用法:
  C:\xenium_envs\xenium-cn-py311\Scripts\python.exe scripts\precompute_simulator.py --dataset hcc --step all
  可选: --step qc|cluster|annotate|downstream|coords|control ; --seed 0

教学设计（已拍板）:
  QC 三档: loose(统一核心减半) / standard(PATTERN-047 统一核心 50/10/1/10) / strict(统一核心加倍)
  聚类: leiden resolution 0.4/0.6/1.0 三候选并行, seed 全链冻结
  归一化+HVG+PCA 固定默认(非决策点): normalize_total(1e4)+log1p, 小 panel 全基因进 PCA(参照 ist_benchmarking)
"""
import argparse
import gzip
import json
import os
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

# 第三方库析构期反复抛出的非致命异常走 sys.unraisablehook（numpy randint 越界刷屏 300MB+）:
# 只计数不打印, 结果不受影响
_UNRAISED = [0]
def _quiet_unraisable(hook):
    _UNRAISED[0] += 1
sys.unraisablehook = _quiet_unraisable

ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS = ROOT / "docs" / "simulator" / "assets"
CACHE = Path(r"F:\xenium数据\ov工作流测试\simulator_precompute\cache")
SEED = 0

# ---------------- 教学参数（冻结） ----------------
QC_TIERS = {  # standard 档 = PATTERN-047 跨平台统一 QC 核心 (源 LIT-053 UCSF)
    "loose":    dict(min_counts=25,  min_genes=5,  gene_min_counts=1, gene_min_cells=5),
    "standard": dict(min_counts=50,  min_genes=10, gene_min_counts=1, gene_min_cells=10),
    "strict":   dict(min_counts=100, min_genes=20, gene_min_counts=1, gene_min_cells=20),
}
RESOLUTIONS = [0.4, 0.6, 1.0]
PCA_COMPS = 20
N_NEIGHBORS = 15
COORD_SUBSAMPLE = 30000
GENE_BUCKETS = 64  # 表达值分桶 (uint 级, 省 gzip 体积)

# 全局一致 cluster 色板（场景内所有图共用, 决策剧场设计系统）
CLUSTER_PALETTE = [
    "#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3", "#937860",
    "#DA8BC3", "#8C8C8C", "#CCB974", "#64B5CD", "#2F4B7C", "#FFA600",
    "#6A51A3", "#31A354", "#E6550D", "#3182BD", "#756BB1", "#636363",
    "#D6616B", "#9E9AC8", "#31A354", "#FDB462", "#80B1D3", "#B3DE69",
]

# ---------------- 场景注册表 ----------------
DATASETS = {
    "hcc": dict(
        key="HCC",
        matrix=r"F:\xenium数据\资源\resource-full_Xenium_V1_肝癌\cell_feature_matrix.h5",
        cells=r"F:\xenium数据\资源\resource-full_Xenium_V1_肝癌\cells.parquet",
        metrics=r"F:\xenium数据\资源\resource-full_Xenium_V1_肝癌\metrics_summary.csv",
        control_matrix=r"F:\xenium数据\资源\resource-肝脏健康V1\cell_feature_matrix.zarr.zip",
        control_cells=r"F:\xenium数据\资源\resource-肝脏健康V1\cells.zarr.zip",
        source="本地官方 Xenium V1 人肝细胞癌 FFPE 输出（resource-full_Xenium_V1_肝癌，run 信息见 experiment.xenium）",
        ref="数据：10x Genomics 官方 Xenium V1 输出；方法参照本库 LIT-088 Moldia/Xenium_benchmarking（Nat Methods 基准仓）与 PATTERN-047 统一 QC 核心（LIT-053）",
        genes_focus=["GPC3", "CYP3A4", "KRT7", "CD68", "MS4A1", "LYVE1"],
        # marker 集已按本 panel 474 基因实际清单核对(2026-09-05, 见 tier 缓存 var_names)
        markers=dict(
            Hepatocyte=["CYP2A7", "CYP2B6", "CYP3A4", "HAMP", "HPX", "TAT", "APOA5", "GLYATL1"],
            Cholangiocyte=["KRT7", "CFTR"],
            Tumor_GPC3=["GPC3"],
            Macrophage_Kupffer=["CD68", "CD163", "MRC1", "MPEG1", "AIF1"],
            DC=["CD1C", "CD1E", "FCER1A", "CLEC10A"],
            LSEC_Endothelial=["LYVE1", "MMRN1", "PECAM1", "VWF"],
            T_NK_cell=["CD3D", "CD3E", "CD8A", "CD4", "TRAC", "NKG7"],
            B_cell=["CD79A", "MS4A1", "CD19", "BANK1"],
            Plasma=["MZB1", "DERL3", "TNFRSF13B"],
            Mast=["CPA3", "KIT", "MS4A2"],
            Fibroblast_Stellate=["PDGFRB", "PDGFRA", "MFAP5", "COCH", "OGN"],
            Erythroid=["ALAS2", "AHSP", "GYPA"],
        ),
        anno_colors=dict(
            Hepatocyte="#E8B44C", Cholangiocyte="#64B5CD", Tumor_GPC3="#C44E52",
            Macrophage_Kupffer="#DD8452", DC="#7F7F7F", LSEC_Endothelial="#55A868",
            T_NK_cell="#4C72B0", B_cell="#DA8BC3", Plasma="#CCB974", Mast="#8172B3",
            Fibroblast_Stellate="#937860", Erythroid="#5BC0BE", Unassigned="#D0D0D0",
        ),
    ),
    "brca": dict(
        key="BRCA",
        matrix=r"F:\xenium数据\ov工作流测试\simulator_precompute\raw\BRCA\Xenium_FFPE_Human_Breast_Cancer_Rep1_cell_feature_matrix.h5",
        cells=r"F:\xenium数据\ov工作流测试\simulator_precompute\raw\BRCA\Xenium_FFPE_Human_Breast_Cancer_Rep1_cells.parquet",
        metrics=r"F:\xenium数据\ov工作流测试\simulator_precompute\raw\BRCA\Xenium_FFPE_Human_Breast_Cancer_Rep1_metrics_summary.csv",
        source="10x Genomics 公开数据集 Xenium FFPE Human Breast Cancer Rep1（cf.10xgenomics.com 单文件直链下载）",
        ref="数据：https://cf.10xgenomics.com/samples/xenium/1.0.1/Xenium_FFPE_Human_Breast_Cancer_Rep1/（Janesick et al. 2023 配套, bioRxiv doi:10.1101/2022.10.06.510405, GEO GSE243275）；方法参照本库 LIT-002/LIT-088",
        genes_focus=["ERBB2", "EPCAM", "ESR1", "KRT5", "ACTA2", "FOXA1"],
        # marker 集已按本 panel 313 基因实际清单核对(2026-09-05; KRT18/COL1A1/DCN/TAGLN 不在 panel)
        markers=dict(
            Invasive_Tumor=["EPCAM", "KRT8"],
            DCIS=["ERBB2", "ESR1", "PGR"],
            Myoepi_ACTA2=["ACTA2", "MYH11", "KRT14"],
            Fibroblast=["LUM", "PDGFRA"],
            Macrophage=["CD68", "CD163", "LYZ"],
            Endothelial=["PECAM1", "VWF"],
            T_cell=["CD3D", "CD3E", "CD8A"],
            B_cell=["CD79A", "MS4A1"],
            Plasma=["MZB1"],
            Mast=["KIT", "CPA3"],
        ),
        anno_colors=dict(
            Invasive_Tumor="#C44E52", DCIS="#E58BB4", Myoepi_ACTA2="#8172B3",
            Fibroblast="#937860", Macrophage="#DD8452", Endothelial="#55A868",
            T_cell="#4C72B0", B_cell="#64B5CD", Plasma="#CCB974", Mast="#6A51A3",
            Unassigned="#D0D0D0",
        ),
    ),
    "crc": dict(
        key="CRC",
        matrix=r"F:\xenium数据\ov工作流测试\simulator_precompute\raw\CRC\cell_feature_matrix.h5",
        cells=r"F:\xenium数据\ov工作流测试\simulator_precompute\raw\CRC\cells.parquet",
        metrics=r"F:\xenium数据\ov工作流测试\simulator_precompute\raw\CRC\metrics_summary.csv",
        source="10x Genomics 公开数据集 Xenium_V1_Human_Colorectal_Cancer_Addon_FFPE（V1 panel + Immuno-Oncology add-on，共 480 基因，cf.10xgenomics.com/samples/xenium/2.0.0/）",
        ref="数据：https://cf.10xgenomics.com/samples/xenium/2.0.0/Xenium_V1_Human_Colorectal_Cancer_Addon_FFPE/（10x 官方数据集页）；结论参照本库 LIT-072 icbi-lab/crc-atlas 与 LIT-074 yliuup/CRC_micromets_ST",
        genes_focus=["CDX2", "EPCAM", "CD3D", "MS4A1", "ACTA2", "PECAM1"],
        # marker 集已按本 panel 480 基因实际清单核对(2026-09-05; KRT20/LYZ/VWF/MYH11 不在 panel)
        markers=dict(
            Tumor_Epithelial=["EPCAM", "CDX2"],
            T_cell=["CD3D", "CD8A", "CD4"],
            B_cell=["CD79A", "MS4A1"],
            Plasma=["MZB1", "XBP1"],
            Myeloid=["CD68", "CD163"],
            Fibroblast=["ACTA2", "PDGFRA", "RGS5"],
            Endothelial=["PECAM1", "CD34"],
        ),
        anno_colors=dict(
            Tumor_Epithelial="#C44E52", T_cell="#4C72B0", B_cell="#64B5CD",
            Plasma="#CCB974", Myeloid="#DD8452", Fibroblast="#937860",
            Endothelial="#55A868", Unassigned="#D0D0D0",
        ),
    ),
}

LIT_DOCS = {  # 三行式标注：精读笔记正本相对路径（用于跳转）
    "hcc": "01_资料库/精读笔记/Moldia__Xenium_benchmarking.md",
    "brca": "01_资料库/精读笔记/10XGenomics__janesick_nature_comms_2023_companion.md",
    "crc": "01_资料库/精读笔记/icbi-lab__crc-atlas.md",
}


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def setup_mpl():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False
    return plt


def save_fig(fig, out: Path, target_kb=160):
    """半分辨率 PNG 落盘, 过大则降 dpi 重存一次。"""
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=110, facecolor="white")
    if out.stat().st_size > target_kb * 1024 * 2:
        fig.savefig(out, dpi=85, facecolor="white")
    log(f"  -> {out.name} ({out.stat().st_size // 1024} KB)")


def cluster_color(i):
    return CLUSTER_PALETTE[i % len(CLUSTER_PALETTE)]


# ---------------- 数据读取 ----------------

def load_xenium_h5(cfg):
    import scanpy as sc
    import pandas as pd
    log(f"读取 {cfg['matrix']}")
    adata = sc.read_10x_h5(cfg["matrix"])
    adata.var_names_make_unique()
    cells_path = cfg.get("cells")
    if cells_path and Path(cells_path).exists():
        cells = pd.read_parquet(cells_path)
        cells.index = cells["cell_id"].astype(str) if "cell_id" in cells.columns else cells.index.astype(str)
        common = adata.obs_names.intersection(cells.index)
        if len(common) >= 0.5 * adata.n_obs:
            adata = adata[common].copy()
            for col in ("x_centroid", "y_centroid"):
                if col in cells.columns:
                    adata.obs[col] = cells.loc[common, col].values
        elif len(cells) == adata.n_obs:
            # h5 barcodes 为位置序号时 cell_id 无法交集 → 按位置对齐
            log("  cell_id 与 h5 barcodes 不一致 → 按位置对齐质心")
            for col in ("x_centroid", "y_centroid"):
                if col in cells.columns:
                    adata.obs[col] = cells.reset_index(drop=True)[col].values[: adata.n_obs]
        else:
            log("  cells.parquet 对齐失败(交集与行数均不符) → 无质心")
    metrics_note = {}
    mpath = cfg.get("metrics")
    if mpath and Path(mpath).exists():
        import pandas as pd
        try:
            m = pd.read_csv(mpath)
            for c in ("Metrics", "Value"):
                pass
            metrics_note = {str(r.iloc[0]): str(r.iloc[1]) for _, r in m.iterrows()}
        except Exception as e:  # metrics 仅作记录, 失败不致命
            log(f"  metrics_summary 读取失败(忽略): {e}")
    log(f"装载完成: {adata.n_obs} 细胞 x {adata.n_vars} 基因")
    return adata, metrics_note


def read_zarr_zip_group(path):
    """通用读取 Xenium zarr.zip（运行时自省结构）。数组在校验存储关闭前物化为 numpy。"""
    import zarr
    import numpy as np
    store = zarr.ZipStore(str(path), mode="r")
    root = zarr.group(store=store)
    found = {}

    def walk(g, prefix=""):
        for k, v in g.arrays():
            found[prefix + k] = np.asarray(v)  # 必须在 store.close() 前物化
        for k, v in g.groups():
            walk(v, prefix + k + "/")

    walk(root)
    store.close()
    return found


def load_control_zarr(cfg):
    """健康肝对照（仅 zarr.zip 打包, 10x cell_features CSR: 行=features 无 shape attrs）。
    质心列归属用多边形顶点均值校验挑选。失败返回 None。"""
    import numpy as np
    from scipy.sparse import csr_matrix
    import anndata as ad
    import zarr
    try:
        arrays = read_zarr_zip_group(cfg["control_matrix"])
        pre = "cell_features/"
        for need in ("data", "indices", "indptr"):
            if pre + need not in arrays:
                raise RuntimeError(f"zarr 缺 {pre}{need}")
        indptr = np.asarray(arrays[pre + "indptr"])
        n_feat = len(indptr) - 1
        n_cells = int(np.asarray(arrays[pre + "indices"]).max()) + 1
        X = csr_matrix((arrays[pre + "data"], arrays[pre + "indices"], indptr),
                       shape=(n_feat, n_cells)).T.tocsr().astype(np.float32)
        # feature_keys/feature_types 是 cell_features 组的 attrs(非子数组)
        store = zarr.ZipStore(str(cfg["control_matrix"]), mode="r")
        g = zarr.group(store=store)["cell_features"]
        var_keys = [str(x) for x in g.attrs["feature_keys"]]
        ftypes = [str(x) for x in g.attrs.get("feature_types", [])]
        store.close()
        keep = [i for i in range(min(len(var_keys), n_feat)) if not ftypes or ftypes[i] == "gene"]
        X = X[:, keep]
        adata = ad.AnnData(X)
        adata.var_names = [var_keys[i] for i in keep]
        adata.var_names_make_unique()
        carr = read_zarr_zip_group(cfg["control_cells"])
        summ = np.asarray(carr["cell_summary"], dtype=float)
        # 10x cell_summary 约定: col0=x_centroid, col1=y_centroid (col2/5=面积, col3/4=核质心, col6=顶点数)
        jx, jy = 0, 1
        if summ[:, jx].std() < 500 or summ[:, jy].std() < 500:
            raise RuntimeError("cell_summary col0/1 std 异常, 质心列归属失败")
        adata.obs["x_centroid"] = summ[: adata.n_obs, jx]
        adata.obs["y_centroid"] = summ[: adata.n_obs, jy]
        verts = np.asarray(carr["polygon_vertices"])  # (2, n_cells, 26) 软校验
        try:
            cx = np.where(verts[0] != 0, verts[0], np.nan).mean(axis=1)
            r = float(np.corrcoef(adata.obs["x_centroid"].values[: len(cx)], cx)[0, 1])
            if r < 0.3:
                log(f"  软警告: 多边形均值与 col0 相关性 {r:.3f} 偏低, 列归属请人工复核")
        except Exception:
            pass
        log(f"健康对照装载: {adata.n_obs} 细胞 x {adata.n_vars} 基因 (x=col{jx}, y=col{jy})")
        return adata
    except Exception as e:
        log(f"健康对照 zarr 读取失败(对照节点将降级为文案): {type(e).__name__}: {e}")
        return None


# ---------------- 主链（每 QC 档独立运行） ----------------

def run_tier(cfg, adata_full, tier):
    import scanpy as sc
    params = QC_TIERS[tier]
    cache_dir = CACHE / cfg["key"] / f"tier_{tier}"
    h5ad = cache_dir / "adata.h5ad"
    if h5ad.exists():
        log(f"[{tier}] 命中缓存 {h5ad}")
        return sc.read_h5ad(h5ad)
    adata = adata_full.copy()
    n0, g0 = adata.n_obs, adata.n_vars
    # scanpy 限制: 每次 filter 调用只允许一个阈值参数, 逐项拆开
    sc.pp.filter_cells(adata, min_counts=params["min_counts"])
    sc.pp.filter_cells(adata, min_genes=params["min_genes"])
    # 注意参数语义: min_cells=表达该基因的细胞数下限; min_counts=该基因计数下限 (P-001 教学点: 阈值不可错位)
    sc.pp.filter_genes(adata, min_cells=params["gene_min_cells"])
    sc.pp.filter_genes(adata, min_counts=params["gene_min_counts"])
    log(f"[{tier}] 过滤: {n0}->{adata.n_obs} 细胞, {g0}->{adata.n_vars} 基因")
    sc.pp.normalize_total(adata, target_sum=1e4)
    sc.pp.log1p(adata)
    log(f"[{tier}] 归一化完成")
    sc.tl.pca(adata, n_comps=min(PCA_COMPS, min(adata.n_obs, adata.n_vars) - 1), random_state=SEED)
    log(f"[{tier}] PCA 完成")
    sc.pp.neighbors(adata, n_neighbors=N_NEIGHBORS, n_pcs=PCA_COMPS, random_state=SEED)
    log(f"[{tier}] neighbors 完成")
    for r in RESOLUTIONS:
        sc.tl.leiden(adata, resolution=r, key_added=f"leiden_{r}", random_state=SEED,
                     flavor="igraph", n_iterations=2, directed=False)
    log(f"[{tier}] leiden x3 完成")
    sc.tl.umap(adata, random_state=SEED)
    log(f"[{tier}] UMAP 完成")
    adata.uns["qc"] = dict(tier=tier, n_cells_in=n0, n_genes_in=g0, n_cells_out=int(adata.n_obs),
                           n_genes_out=int(adata.n_vars), **params)
    cache_dir.mkdir(parents=True, exist_ok=True)
    adata.write_h5ad(h5ad)
    log(f"[{tier}] {n0}->{adata.n_obs} 细胞, {g0}->{adata.n_vars} 基因 (已缓存)")
    return adata


# ---------------- 绘图 ----------------

def plot_qc_tiers(cfg, tier_stats, manifest):
    plt = setup_mpl()
    tiers = ["loose", "standard", "strict"]
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.6))
    cells = [tier_stats[t]["n_cells_out"] for t in tiers]
    genes = [tier_stats[t]["n_genes_out"] for t in tiers]
    ratios = [tier_stats[t]["n_cells_out"] / tier_stats[t]["n_cells_in"] for t in tiers]
    axes[0].bar(tiers, cells, color=["#DD8452", "#4C72B0", "#C44E52"])
    for i, v in enumerate(cells):
        axes[0].text(i, v, f"{v:,}", ha="center", va="bottom", fontsize=8)
    axes[0].set_title("Surviving cells")
    axes[1].bar(tiers, genes, color=["#DD8452", "#4C72B0", "#C44E52"])
    for i, v in enumerate(genes):
        axes[1].text(i, v, f"{v:,}", ha="center", va="bottom", fontsize=8)
    axes[1].set_title("Surviving genes")
    axes[2].bar(tiers, [r * 100 for r in ratios], color=["#DD8452", "#4C72B0", "#C44E52"])
    axes[2].set_title("Cell retention (%)")
    axes[2].set_ylabel("%")
    fig.suptitle(f"QC tiers  (loose/standard/strict; standard = PATTERN-047 core)", fontsize=10)
    fig.tight_layout()
    out = ASSETS / cfg["key"] / "qc_tiers.png"
    save_fig(fig, out)
    manifest["assets"].append(dict(file="qc_tiers.png", kind="T1", node="2-qc",
                                   title="QC 三档后果对比（细胞/基因存活数）",
                                   source=cfg["source"], nature="真实重算（预计算管线, seed=0）", ref=cfg["ref"]))
    plt.close(fig)


def plot_umap_trio(cfg, tier_data, manifest):
    plt = setup_mpl()
    tier = "standard"
    adata = tier_data[tier]
    for r in RESOLUTIONS:
        fig, ax = plt.subplots(figsize=(4.6, 4.2))
        labs = adata.obs[f"leiden_{r}"].astype(int)
        k = labs.max() + 1
        colors = [cluster_color(i) for i in range(k)]
        ax.scatter(adata.obsm["X_umap"][:, 0], adata.obsm["X_umap"][:, 1], s=0.4,
                   c=[colors[i] for i in labs], linewidths=0)
        ax.set_title(f"leiden resolution={r}  ({k} clusters)", fontsize=10)
        ax.set_xticks([]); ax.set_yticks([])
        fig.tight_layout()
        out = ASSETS / cfg["key"] / f"umap_res{str(r).replace('.', '')}.png"
        save_fig(fig, out)
        manifest["assets"].append(dict(file=out.name, kind="T1", node="4-cluster",
                                       title=f"UMAP leiden res={r}（standard QC 档）",
                                       source=cfg["source"], nature="真实重算（leiden/UMAP, seed=0）", ref=cfg["ref"]))
        plt.close(fig)


def annotate_markers(adata, markers):
    """marker 人工注释路线: 逐细胞类型 score_genes(逐列 z-score), argmax + 边际判据。
    返回 (labels, 有效集名, 单基因集名)。"""
    import numpy as np
    import scanpy as sc
    valid, single = {}, []
    for name, genes in markers.items():
        g = [x for x in genes if x in adata.var_names]
        if len(g) >= 1:
            valid[name] = g
            if len(g) == 1:
                single.append(name)
    labels = np.array(["Unassigned"] * adata.n_obs, dtype=object)
    score_mat = {}
    for name, g in valid.items():
        try:
            sc.tl.score_genes(adata, gene_list=g, score_name=f"score_{name}", random_state=SEED)
            score_mat[name] = np.asarray(adata.obs[f"score_{name}"].values, dtype=float)
        except Exception as e:
            log(f"  score_genes 失败({name}): {e}")
    if score_mat:
        names = list(score_mat)
        M = np.vstack([score_mat[n] for n in names]).T
        mu, sd = M.mean(0), M.std(0)
        sd[sd == 0] = 1.0
        Z = (M - mu) / sd
        best = Z.argmax(axis=1)
        part = np.partition(Z, -2, axis=1)
        top, second = part[:, -1], part[:, -2]
        assign = (top - second) >= 0.15  # z 单位边际, 近平票不强判
        labels[assign] = np.array(names, dtype=object)[best[assign]]
    return labels, list(valid), single


def plot_annotation(cfg, adata, labels, anno_colors, route, manifest, note=""):
    plt = setup_mpl()
    order = [c for c in anno_colors if c in set(labels)]
    cmap = {c: anno_colors[c] for c in order}
    # 空间图
    fig, ax = plt.subplots(figsize=(5.6, 5.2))
    for c in order:
        m = labels == c
        ax.scatter(adata.obs["x_centroid"].values[m], adata.obs["y_centroid"].values[m],
                   s=0.5, c=cmap[c], label=f"{c} ({m.sum():,})", linewidths=0)
    ax.invert_yaxis()
    ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    ax.legend(markerscale=12, fontsize=6.5, loc="best", framealpha=0.85)
    ax.set_title(f"Annotation route: {route}{note}", fontsize=10)
    fig.tight_layout()
    out = ASSETS / cfg["key"] / f"anno_{route}_spatial.png"
    save_fig(fig, out)
    manifest["assets"].append(dict(file=out.name, kind="T1", node="5-annotate",
                                   title=f"注释路线（{route}）· 空间分布",
                                   source=cfg["source"], nature="真实重算（score_genes argmax, seed=0）", ref=cfg["ref"]))
    plt.close(fig)
    # UMAP
    fig, ax = plt.subplots(figsize=(4.8, 4.4))
    um = adata.obsm["X_umap"]
    for c in order:
        m = labels == c
        ax.scatter(um[m, 0], um[m, 1], s=0.5, c=cmap[c], label=c, linewidths=0)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(f"Annotation route: {route}", fontsize=10)
    fig.tight_layout()
    out = ASSETS / cfg["key"] / f"anno_{route}_umap.png"
    save_fig(fig, out)
    manifest["assets"].append(dict(file=out.name, kind="T1", node="5-annotate",
                                   title=f"注释路线（{route}）· UMAP",
                                   source=cfg["source"], nature="真实重算（seed=0）", ref=cfg["ref"]))
    plt.close(fig)
    return out.parent


def plot_downstream(cfg, adata, labels, anno_colors, niche_labels, manifest, healthy_labels=None):
    plt = setup_mpl()
    key = cfg["key"]
    order = [c for c in anno_colors if c in set(labels)]
    cmap = {c: anno_colors[c] for c in order}
    # A 细胞比例
    import numpy as np
    counts = np.array([(labels == c).sum() for c in order], dtype=float)
    props = counts / counts.sum()
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    ax.barh(order[::-1], props[::-1] * 100, color=[cmap[c] for c in order][::-1])
    for i, v in enumerate(props[::-1] * 100):
        ax.text(v + 0.3, i, f"{v:.1f}%", va="center", fontsize=7.5)
    ax.set_xlabel("% of cells")
    ax.set_title("Cell-type proportions (standard QC, res=0.6 annotation)", fontsize=9.5)
    fig.tight_layout()
    out = ASSETS / key / "ds_a_proportions.png"
    save_fig(fig, out)
    manifest["assets"].append(dict(file=out.name, kind="T1", node="6-downstream-a",
                                   title="下游 A · 细胞类型比例",
                                   source=cfg["source"], nature="真实重算（注释列汇总）", ref=cfg["ref"]))
    plt.close(fig)
    # B niche 空间图
    niche_ids = sorted(set(niche_labels))
    fig, ax = plt.subplots(figsize=(5.6, 5.2))
    niche_cmap = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3", "#937860"]
    for i, nid in enumerate(niche_ids):
        m = niche_labels == nid
        ax.scatter(adata.obs["x_centroid"].values[m], adata.obs["y_centroid"].values[m],
                   s=0.5, c=niche_cmap[i % len(niche_cmap)], label=f"niche {nid} ({m.sum():,})", linewidths=0)
    ax.invert_yaxis(); ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    ax.legend(markerscale=12, fontsize=7, loc="best")
    ax.set_title("Neighborhood niches (kNN k=15 composition + KMeans)", fontsize=9.5)
    fig.tight_layout()
    out = ASSETS / key / "ds_b_niche_spatial.png"
    save_fig(fig, out)
    manifest["assets"].append(dict(file=out.name, kind="T1", node="6-downstream-b",
                                   title="下游 B · 空间域 niche（PATTERN-049 教学实现）",
                                   source=cfg["source"], nature="真实重算（KMeans seed=0）", ref=cfg["ref"]))
    plt.close(fig)
    # C 单基因空间图 (前两个 focus 基因)
    focus = [g for g in cfg["genes_focus"] if g in adata.var_names][:2]
    for g in focus:
        vals = adata[:, g].X.toarray().ravel() if hasattr(adata[:, g].X, "toarray") else np.asarray(adata[:, g].X).ravel()
        vmax = np.quantile(vals, 0.98)
        fig, ax = plt.subplots(figsize=(5.4, 5.0))
        idx = vals > 0
        ax.scatter(adata.obs["x_centroid"].values[~idx], adata.obs["y_centroid"].values[~idx],
                   s=0.4, c="#EEEEEE", linewidths=0)
        sc_ax = ax.scatter(adata.obs["x_centroid"].values[idx], adata.obs["y_centroid"].values[idx],
                           s=0.6, c=vals[idx], cmap="magma", vmin=0, vmax=vmax, linewidths=0)
        ax.invert_yaxis(); ax.set_aspect("equal")
        ax.set_xticks([]); ax.set_yticks([])
        cb = fig.colorbar(sc_ax, ax=ax, shrink=0.55)
        cb.ax.tick_params(labelsize=6)
        ax.set_title(f"{g} spatial expression (log-norm)", fontsize=9.5)
        fig.tight_layout()
        out = ASSETS / key / f"ds_c_gene_{g}.png"
        save_fig(fig, out)
        manifest["assets"].append(dict(file=out.name, kind="T1", node="6-downstream-c",
                                       title=f"下游 C · 单基因空间图（{g}）",
                                       source=cfg["source"], nature="真实重算", ref=cfg["ref"]))
        plt.close(fig)
    # A2 健康对照对比（仅 hcc, 对照可用时）
    if healthy_labels is not None:
        horder = [c for c in anno_colors if c in set(healthy_labels)]
        hcounts = np.array([(healthy_labels == c).sum() for c in horder], dtype=float)
        hprops = dict(zip(horder, hcounts / hcounts.sum()))
        tprops = dict(zip(order, props))
        allc = [c for c in anno_colors if c in tprops or c in hprops]
        x = np.arange(len(allc))
        fig, ax = plt.subplots(figsize=(6.8, 3.6))
        tv = [tprops.get(c, 0) * 100 for c in allc]
        hv = [hprops.get(c, 0) * 100 for c in allc]
        ax.bar(x - 0.2, tv, width=0.4, label="HCC tumor", color="#C44E52")
        ax.bar(x + 0.2, hv, width=0.4, label="Healthy liver", color="#4C72B0")
        ax.set_xticks(x); ax.set_xticklabels(allc, rotation=45, ha="right", fontsize=7)
        ax.set_ylabel("% of cells")
        ax.legend(fontsize=8)
        ax.set_title("Tumor vs healthy liver composition (same pipeline)", fontsize=9.5)
        fig.tight_layout()
        out = ASSETS / key / "ds_a_tumor_vs_healthy.png"
        save_fig(fig, out)
        manifest["assets"].append(dict(file=out.name, kind="T1", node="6-downstream-a",
                                       title="下游 A · 肿瘤 vs 健康肝组成对比",
                                       source=cfg["source"] + "；健康对照 resource-肝脏健康V1（zarr 读入）",
                                       nature="真实重算（同管线同 seed）", ref=cfg["ref"]))
        plt.close(fig)


def compute_niche(adata, labels, k=15, n_niches=4):
    """PATTERN-049 教学实现: kNN 邻居注释构成矩阵 + KMeans。"""
    import numpy as np
    from sklearn.neighbors import NearestNeighbors
    from sklearn.cluster import KMeans
    coords = adata.obs[["x_centroid", "y_centroid"]].values
    nn = NearestNeighbors(n_neighbors=k + 1, algorithm="kd_tree").fit(coords)
    _, idx = nn.kneighbors(coords)
    idx = idx[:, 1:]  # 去自身
    cats = sorted(set(labels))
    cat_idx = {c: i for i, c in enumerate(cats)}
    lab_idx = np.array([cat_idx[l] for l in labels])
    K = len(cats)
    comp = np.zeros((adata.n_obs, K), dtype=np.float32)
    onehot = np.eye(K, dtype=np.float32)
    nb_lab = lab_idx[idx]  # n x k
    for j in range(k):
        comp += onehot[nb_lab[:, j]]
    comp /= k
    km = KMeans(n_clusters=n_niches, random_state=SEED, n_init=10).fit(comp)
    return km.labels_, cats, comp


# ---------------- coords JSON.gz (T2 交互) ----------------

def write_coords(cfg, adata, labels, niche_labels, manifest):
    import numpy as np
    rng = np.random.default_rng(SEED)
    n = adata.n_obs
    take = rng.choice(n, size=min(COORD_SUBSAMPLE, n), replace=False)
    take.sort()
    sub = adata[take]
    sub_lab = labels[take]
    sub_niche = niche_labels[take]
    res_keys = [f"leiden_{r}" for r in RESOLUTIONS]
    clusters = {rk: sub.obs[rk].astype(int).tolist() for rk in res_keys}
    cats = sorted(set(labels))
    anno_idx = np.array([cats.index(l) for l in sub_lab], dtype=int)
    focus = [g for g in cfg["genes_focus"] if g in sub.var_names][:6]
    gene_vals = {}
    for g in focus:
        v = sub[:, g].X.toarray().ravel() if hasattr(sub[:, g].X, "toarray") else np.asarray(sub[:, g].X).ravel()
        vmax = np.quantile(v, 0.99) or 1.0
        b = np.clip((v / vmax * (GENE_BUCKETS - 1)).round(), 0, GENE_BUCKETS - 1).astype(int)
        gene_vals[g] = b.tolist()
    # niche 与注释 ID 合并到 int 列表
    cats_json = [str(c) for c in cats]
    payload = dict(
        dataset=cfg["key"], qc_tier="standard", resolution=RESOLUTIONS[1],
        n=int(sub.n_obs),
        x=np.round(sub.obs["x_centroid"].values, 1).tolist(),
        y=np.round(sub.obs["y_centroid"].values, 1).tolist(),
        clusters=clusters,
        anno=anno_idx.tolist(), anno_labels=cats_json,
        niche=sub_niche.astype(int).tolist(),
        genes=gene_vals,
        gene_order=list(gene_vals),
    )
    outdir = ASSETS / cfg["key"] / "coords"
    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / "coords_standard.json.gz"
    with gzip.open(out, "wt", encoding="utf-8", compresslevel=9) as f:
        json.dump(payload, f, separators=(",", ":"))
    size_kb = out.stat().st_size // 1024
    log(f"  -> coords_standard.json.gz ({size_kb} KB, {sub.n_obs} 细胞)")
    manifest["assets"].append(dict(file="coords/coords_standard.json.gz", kind="T2", node="6-downstream",
                                   title="T2 交互散点（空间/UMAP/表达切换）",
                                   source=cfg["source"], nature=f"真实重算抽样 {sub.n_obs} 细胞（seed=0）", ref=cfg["ref"]))
    return cats_json


# ---------------- celltypist 路线（可用则算, 失败降 T3 并登记） ----------------

def try_celltypist(cfg, adata, manifest):
    flags = {}
    try:
        import celltypist  # noqa
        from celltypist import models
        log("celltypist 可用, 尝试模型下载与迁移注释…")
        try:
            model = models.Model.load(model="Immune_All_Low.pkl")
            from celltypist import annotate
            import scanpy as sc
            ad_sub = adata[:, :].copy()
            pred = annotate(ad_sub, model=model, majority_voting=False)
            labels = pred.predicted_labels["predicted_labels"].values.astype(object)
            # 只保留 top 频次类型做教学可视化, 其余归 Other
            import numpy as np
            vals, cnts = np.unique(labels, return_counts=True)
            keep = set(vals[np.argsort(-cnts)[:8]])
            labels = np.array([l if l in keep else "Other" for l in labels], dtype=object)
            palette = dict(zip(sorted(set(labels)),
                               [cluster_color(i) for i in range(len(set(labels)))]))
            plot_annotation(cfg, adata, labels, palette, "celltypist", manifest,
                            note=" (Immune_All_Low transfer)")
            manifest["assets"][-1]["title"] = "注释路线（celltypist 迁移）· 空间分布"
            flags["celltypist"] = "ok"
        except Exception as e:
            log(f"celltypist 模型/注释失败 → 该路线降级 T3: {type(e).__name__}: {e}")
            flags["celltypist"] = "T3"
    except ImportError:
        log("celltypist 未安装 → 该路线在场景中以 T2/T3 文献结论重绘呈现并标注")
        flags["celltypist"] = "T3"
    return flags


# ---------------- 健康对照对照线 ----------------

def run_control(cfg, manifest):
    ctrl = load_control_zarr(cfg)
    if ctrl is None:
        return None
    import scanpy as sc
    p = QC_TIERS["standard"]
    sc.pp.filter_cells(ctrl, min_counts=p["min_counts"])
    sc.pp.filter_cells(ctrl, min_genes=p["min_genes"])
    sc.pp.filter_genes(ctrl, min_cells=p["gene_min_cells"])
    sc.pp.filter_genes(ctrl, min_counts=p["gene_min_counts"])
    sc.pp.normalize_total(ctrl, target_sum=1e4)
    sc.pp.log1p(ctrl)
    labels, _, _ = annotate_markers(ctrl, cfg["markers"])
    return labels


# ---------------- 主流程 ----------------

def pipeline_dataset(ds):
    cfg = DATASETS[ds]
    key = cfg["key"]
    manifest = dict(dataset=key, generated=__import__("datetime").date.today().isoformat(), seed=SEED,
                    doc=LIT_DOCS.get(ds, ""), assets=[],
                    source=cfg["source"], nature="T1 真实数据预计算", ref=cfg["ref"],
                    flags={})
    for p in (ASSETS / key,):
        p.mkdir(parents=True, exist_ok=True)
    adata_full, metrics_note = load_xenium_h5(cfg)
    tier_data = {}
    tier_stats = {}
    for tier in QC_TIERS:
        ad = run_tier(cfg, adata_full, tier)
        tier_data[tier] = ad
        q = ad.uns["qc"]
        tier_stats[tier] = {k: (int(v) if isinstance(v, (int, float)) else v) for k, v in q.items()}
    del adata_full
    plot_qc_tiers(cfg, tier_stats, manifest)
    plot_umap_trio(cfg, tier_data, manifest)
    # 注释与下游 (standard 档)
    adata = tier_data["standard"]
    labels, used_sets, single_gene = annotate_markers(adata, cfg["markers"])
    log(f"marker 注释: {len(set(labels))} 类 ({', '.join(sorted(set(labels)))}); 单基因集: {single_gene}")
    manifest["flags"]["marker_sets"] = {k: v for k, v in cfg["markers"].items() if k in used_sets}
    plot_annotation(cfg, adata, labels, cfg["anno_colors"], "marker", manifest)
    flags = try_celltypist(cfg, adata, manifest)
    manifest["flags"].update(flags)
    niche_labels, cats, comp = compute_niche(adata, labels)
    healthy_labels = None
    if cfg.get("control_matrix"):
        healthy_labels = run_control(cfg, manifest)
        manifest["flags"]["healthy_control"] = "ok" if healthy_labels is not None else "degraded_text_only"
    plot_downstream(cfg, adata, labels, cfg["anno_colors"], niche_labels, manifest, healthy_labels)
    write_coords(cfg, adata, labels, niche_labels, manifest)
    manifest["qc_stats"] = tier_stats
    manifest["metrics_note"] = dict(list(metrics_note.items())[:12])
    out = ASSETS / key / "manifest.json"
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    log(f"[{key}] manifest.json 写入完成, 共 {len(manifest['assets'])} 资产")
    return manifest


def main():
    ap = argparse.ArgumentParser(description="Xenium 决策剧场预计算")
    ap.add_argument("--dataset", required=True, choices=["hcc", "brca", "crc", "zxm", "uc", "crohn"])
    ap.add_argument("--step", default="all",
                    choices=["all", "qc", "cluster", "annotate", "downstream", "coords", "control"])
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    global SEED
    SEED = args.seed
    if args.dataset in ("zxm", "uc", "crohn"):
        log(f"数据集 {args.dataset} 的专用管线在 precompute_{args.dataset}.py / lit_redraw 中实现（二期补齐入口）")
        sys.exit(2)
    pipeline_dataset(args.dataset)


if __name__ == "__main__":
    main()
