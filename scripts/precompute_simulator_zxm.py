# -*- coding: utf-8 -*-
r"""Xenium 决策剧场 · ZXM 本地专属关预计算（onboard 复用 + 抽样 coords）

教学定位: 百万级样本不复算——复用 onboard analysis/ 结果（官方线 large_sample_reuse 先例）。
产物(全部写 docs/simulator/assets/ZXM_local/, 已 .gitignore 排除, 不入公开仓):
  manifest.json / scenario.json
  coords/coords_onboard.json.gz  (<=3 万细胞抽样: 空间质心 + onboard UMAP + graphclust + 焦点基因表达)
  qc_tiers_subsample.png         (QC 三档在 3 万细胞抽样上的重演, 图与标注均显式声明"抽样")

数据源(本机):
  F:\xenium数据\ZXM\RAW_DATA\output-XETG00099__0066171__Region_1__20260204__104132\
    output-XETG00099__0066171__Region_1__20260204__104132\
用法:
  C:\xenium_envs\xenium-cn-py311\Scripts\python.exe scripts\precompute_simulator_zxm.py
"""
import gzip
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = ROOT / "docs" / "simulator" / "assets" / "ZXM_local"
SEED = 0
SUBSAMPLE = 30000
GENE_BUCKETS = 64

ZXM = Path(r"F:\xenium数据\ZXM\RAW_DATA\output-XETG00099__0066171__Region_1__20260204__104132\output-XETG00099__0066171__Region_1__20260204__104132")
FOCUS_GENES = ["EPCAM", "KRT8", "PTPRC", "CD3D", "ACTA2", "PECAM1"]  # 命中即用

SOURCE = "本机课题数据 ZXM 完整 outs（新版式 Xenium 输出，onboard analysis 结果复用 + 3 万细胞抽样）"
REF = "数据：本地课题 run（output-XETG00099__0066171__Region_1，2026-02 onboard 分析）；策略参照本库候选流程池·官方线 large_sample_reuse 模式"


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def read_zarr_zip(path, max_bytes=200_000_000):
    """读取 zarr.zip 但只物化小数组(守卫 polygon_vertices 级别的 19GB 巨物)。"""
    import zarr
    store = zarr.ZipStore(str(path), mode="r")
    root = zarr.group(store=store)
    found = {}

    def walk(g, prefix=""):
        for k, v in g.arrays():
            try:
                if v.nbytes > max_bytes:
                    found[prefix + k] = None  # 巨物占位, 不物化
                    continue
            except Exception:
                pass
            found[prefix + k] = np.asarray(v)
        for k, v in g.groups():
            walk(v, prefix + k + "/")

    walk(root)
    store.close()
    return found


def main():
    import pandas as pd
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "coords").mkdir(exist_ok=True)
    manifest = dict(dataset="ZXM", generated=time.strftime("%Y-%m-%d"), seed=SEED,
                    source=SOURCE, nature="T1 本地关：onboard 结果复用 + 抽样重演", ref=REF,
                    doc="02_工作流开发/候选流程池/官方线_官方教程中文优化.md", assets=[], flags={})

    # ---- 1) 空间质心 + 细胞数 (cells.zarr.zip; 巨物数组守卫跳过) ----
    log("读取 cells.zarr.zip (质心)…")
    carr = read_zarr_zip(ZXM / "cells.zarr.zip")
    summ = np.asarray(carr["cell_summary"], dtype=np.float32)
    n_all = summ.shape[0]
    log(f"全样本 {n_all:,} 细胞 (onboard 口径, 不重算)")

    # ---- 2) h5 条码序为基准, onboard 产物按 Barcode 对齐 ----
    log("读取 h5 barcodes (基准序)…")
    import h5py
    with h5py.File(ZXM / "cell_feature_matrix.h5", "r") as f:
        barcodes = np.array([x.decode() for x in f["matrix/barcodes"][:]])
    log(f"h5 条码 {len(barcodes):,}")
    clus = pd.read_csv(ZXM / "analysis" / "clustering" / "gene_expression_graphclust" / "clusters.csv")
    proj = pd.read_csv(ZXM / "analysis" / "umap" / "gene_expression_2_components" / "projection.csv")
    log(f"onboard graphclust {clus.shape[0]:,} 行, UMAP {proj.shape[0]:,} 行 (被 onboard 过滤的细胞无标签)")
    bc_pos = pd.Series(np.arange(len(barcodes)), index=barcodes)
    clusters = clus.set_index("Barcode")["Cluster"].reindex(barcodes).fillna(-1).astype(int).values
    ux = proj.set_index("Barcode")["UMAP-1"].reindex(barcodes).values
    uy = proj.set_index("Barcode")["UMAP-2"].reindex(barcodes).values
    if summ.shape[0] == len(barcodes):
        x, y = summ[:, 0], summ[:, 1]  # zarr 与 h5 同序 (同一 XOA 输出保证)
    else:
        raise RuntimeError(f"cells.zarr {summ.shape[0]} 与 h5 条码 {len(barcodes)} 数量不一致")
    n_unlabeled = int((clusters < 0).sum())
    log(f"无 graphclust 标签的细胞: {n_unlabeled:,}")

    # ---- 3) 抽样 (seed=0, 仅取有标签细胞参与标签列; 空间视图全体可看) ----
    labeled = np.nonzero(clusters >= 0)[0]
    rng = np.random.default_rng(SEED)
    take = np.sort(rng.choice(labeled, size=min(SUBSAMPLE, len(labeled)), replace=False))
    log(f"抽样 {len(take):,} 细胞 (有 graphclust 标签者, seed={SEED})")

    # ---- 4) QC 三档在抽样上重演 (显式声明抽样, 非全样本结论) + 焦点基因表达 ----
    log("h5 分块扫描 (counts 直方图 + 目标基因)…")
    import h5py
    h5 = ZXM / "cell_feature_matrix.h5"
    with h5py.File(h5, "r") as f:
        g = f["matrix"]
        indptr = np.asarray(g["indptr"]).astype(np.int64)   # CSC over cells: len = n_cells+1
        n_cells = len(barcodes)                              # matrix 组无 shape 属性 → 用条码/特征长度推导
        genes_all = [x.decode() if isinstance(x, bytes) else str(x) for x in f["matrix/features/name"][:]]
        n_genes = len(genes_all)
        nnz_total = int(indptr[-1])
        log(f"h5: {n_genes} x {n_cells} (nnz={nnz_total:,})")
        if n_cells != n_all:
            raise RuntimeError(f"h5 细胞数 {n_cells} 与 cells.zarr {n_all} 不一致")
        counts_per_cell = np.diff(indptr)                    # 每细胞 stored entries = 转录本数
        sub_counts = counts_per_cell[take]

        genes_avail = genes_all
        var_pos = {n: i for i, n in enumerate(genes_avail)}
        targets = {var_pos[g]: g for g in FOCUS_GENES if g in var_pos}
        col_of = np.full(n_cells, -1, dtype=np.int64)
        col_of[take] = np.arange(len(take))
        # CSC 下目标基因散布全表: 分块扫描 (data, indices), searchsorted 回定位细胞列
        gene_cells = {gi: [] for gi in targets}
        gene_vals_list = {gi: [] for gi in targets}
        CH = 40_000_000
        for s in range(0, nnz_total, CH):
            e = min(s + CH, nnz_total)
            d = g["data"][s:e]
            idx = g["indices"][s:e]
            for gi in targets:
                m = idx == gi
                if not m.any():
                    continue
                pos = np.nonzero(m)[0] + s
                cell = np.searchsorted(indptr, pos, side="right") - 1
                keep = col_of[cell] >= 0
                gene_cells[gi].append(cell[keep])
                gene_vals_list[gi].append(d[m][keep])
            log(f"  扫描 {e:,}/{nnz_total:,}")
        gene_vals = {}
        for gi, gname in targets.items():
            v = np.zeros(len(take), dtype=np.float32)
            if gene_cells[gi]:
                cell = np.concatenate(gene_cells[gi])
                val = np.concatenate(gene_vals_list[gi]).astype(np.float32)
                v[col_of[cell]] = val
            vmax = np.quantile(v, 0.99) or 1.0
            gene_vals[gname] = np.clip((v / vmax * (GENE_BUCKETS - 1)).round(), 0, GENE_BUCKETS - 1).astype(int).tolist()

    tiers = dict(
        loose=dict(min_counts=25, min_genes=5),
        standard=dict(min_counts=50, min_genes=10),
        strict=dict(min_counts=100, min_genes=20),
    )
    # min_genes 需每细胞非零基因数——h5 全量基因级扫描代价高, 抽样上重算:
    # 从 counts 直方图不可得 genes/cell, 故对抽样细胞逐列读 nnz 不现实; 改用 counts 单阈值近似并注明
    qc_stats = {}
    for t, p in tiers.items():
        keep = sub_counts >= p["min_counts"]
        qc_stats[t] = dict(min_counts=p["min_counts"], min_genes=p["min_genes"],
                           n_cells_in=int(len(sub_counts)), n_cells_out=int(keep.sum()),
                           note="3 万细胞抽样重演, 仅 min_counts 单阈值口径")
        log(f"[{t}] 抽样 {len(sub_counts):,} -> {int(keep.sum()):,}")

    # ---- 5) 画 QC 三档 (抽样) 图 ----
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.6))
    ts = ["loose", "standard", "strict"]
    vals = [qc_stats[t]["n_cells_out"] for t in ts]
    axes[0].bar(ts, vals, color=["#DD8452", "#4C72B0", "#C44E52"])
    for i, v in enumerate(vals):
        axes[0].text(i, v, f"{v:,}", ha="center", va="bottom", fontsize=8)
    axes[0].set_title("Surviving cells (subsample, min_counts only)", fontsize=9.5)
    axes[1].hist(np.log10(sub_counts + 1), bins=60, color="#4C72B0")
    axes[1].set_title("log10(transcripts/cell) subsample", fontsize=9.5)
    fig.tight_layout()
    qc_png = OUT / "qc_tiers_subsample.png"
    fig.savefig(qc_png, dpi=110, facecolor="white")
    plt.close(fig)
    manifest["assets"].append(dict(file="qc_tiers_subsample.png", kind="T1", node="2-qc",
                                   title="QC 三档（3 万细胞抽样重演）",
                                   source=SOURCE, nature="onboard 数据抽样重算（显式声明抽样, seed=0）", ref=REF))
    manifest["qc_stats"] = qc_stats
    manifest["flags"]["subsample_qc"] = "min_counts 单阈值口径; min_genes 需全矩阵扫描, 略"

    # ---- 6) coords JSON.gz ----
    payload = dict(
        dataset="ZXM", qc_tier="onboard-reuse", resolution="graphclust",
        n=int(len(take)),
        x=np.round(x[take], 1).tolist(),
        y=np.round(y[take], 1).tolist(),
        umap=[np.round(ux[take], 2).tolist(), np.round(uy[take], 2).tolist()],
        clusters={"leiden_graphclust": [int(c) for c in clusters[take]]},
        anno_labels=[],
        niche=[],
        genes=gene_vals, gene_order=list(gene_vals),
        note="onboard graphclust/UMAP 复用 + 空间质心; 全样本 1.19M 细胞不复算(大样本策略教学)",
    )
    gz = OUT / "coords" / "coords_onboard.json.gz"
    with gzip.open(gz, "wt", encoding="utf-8", compresslevel=9) as f:
        json.dump(payload, f, separators=(",", ":"))
    log(f"coords_onboard.json.gz ({gz.stat().st_size // 1024} KB)")
    manifest["assets"].append(dict(file="coords/coords_onboard.json.gz", kind="T2", node="6-downstream",
                                   title="T2 交互散点（onboard 复用 + 抽样）",
                                   source=SOURCE, nature="onboard 结果复用 + 3 万细胞抽样（seed=0）", ref=REF))

    manifest["metrics_note"] = dict(n_cells_all=int(n_all), n_clusters=int(len(set(clusters[clusters >= 0]))),
                                    n_unlabeled=n_unlabeled)
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    log(f"[ZXM] manifest.json 完成, 共 {len(manifest['assets'])} 资产 → {OUT}")
    log("提示: ZXM scenario.json 需由主脚本/仓库提供; 本地版刷新模拟器首页即出现入口")


if __name__ == "__main__":
    main()
