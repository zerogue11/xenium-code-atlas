# 精读笔记 · Teichlab__crohns-fibroblast-atlas

- repo: Teichlab/crohns-fibroblast-atlas（LIT-066）
- 来源文献: Kinchen et al., Cell — 克罗恩病成纤维细胞图谱（2026）
- 锁定SHA: 96e481451695a7380c2b84f26ac60149210dcc7b
- 复核分类: 注释/图谱/生态位组 · S 级 · notebook 群仓（28 个研究模块目录，本仓 858MB，不读数据目录）
- 精读日期: 2026-09-04（一期精读批次C）

## 代码结构走读

- 顶层 28 个平级目录按研究主题切块（scRNA/scATAC/cNMF/trajectory/scenic+/bulk 等），**本组重点精读 `xenium/`（Xenium 5K 链，23 个编号 notebook，38628 行）**。
- `xenium/` 链条（编号即顺序）：
  - **1a–1d**（各 ~3070 行，每样本一篇）：`sc.read_10x_h5(cell_feature_matrix.h5)` + cells.csv + 官方 graphclust → QC（calculate_qc_metrics/filter_cells）→ normalize/log1p → neighbors/leiden → **celltypist.annotate(megagutSmallIntestine_lvl1/lvl3.pkl)** 单样本预注释。
  - **2_joint**(1713行)：四样本 concat → **`scvi.model.SCVI(adata, n_layers=2, n_latent=30, gene_likelihood="nb")`，setup_anndata(layer="counts", batch_key="sample")**（2_joint cell34）→ 联合 celltypist。
  - **3a–3c**：间质子集（megagut_lvl1=='Mesenchymal' 过滤+lvl3 反证排除 10 类污染，3a cell6-9）→ **多分辨率 leiden 1/2/4/5/10 并存**（3a：leiden1/2/4/5/10 五个 key）→ **cluster→标签人工映射字典**（3a cell36，3891 字符的 leiden5=='0'→Myofibroblast_1 式硬编码）→ 每亚型概率列（S1_prob...）。
  - **4a**(1431行)：`sq.gr.spatial_neighbors(delaunay=True, library_key='sample')` → **`cc.gr.aggregate_neighbors(n_layers=3, use_rep='X_scVI')`** → **`cc.tl.ClusterAutoK(n_clusters=(4,25), GaussianMixture, random_state=42, max_runs=5)`** → autok_stability 曲线选 k（4a cell17-19）。
  - **5**：免疫室 `celltypist.annotate(adata, model="Immune_All_Low.pkl", majority_voting=True)`（cell14）；**6–8**：图/表/cytokine 签名/niche 图。
- scVI→celltypist 落地方式确认：scVI 只做整合给 latent，注释直接在 **counts 重建后的表达**上跑 celltypist（megagut 模型自带预处理），未把 latent 喂给注释器。

## 关键脚本清单

| 文件 | 一句话 | 行数 |
|---|---|---|
| xenium/1a_xenium5k_1.ipynb | 单样本 Xenium 读取+QC+celltypist 预注释模板 | 3075 |
| xenium/2_xenium5k_joint.ipynb | 四样本 concat + scVI(batch=sample, n_latent=30) | 1713 |
| xenium/3a_xenium5k_annotation.ipynb | 间质子集多分辨率 leiden + 人工映射注释 | 2377 |
| xenium/4a_xenium5k_niche.ipynb | CellCharter ClusterAutoK niche 发现全流程 | 1431 |
| xenium/5_xenium5k_immune_annotation.ipynb | Immune_All_Low 免疫注释 | 1278 |
| xenium/7a_xenium5k_cytokine_signature.ipynb | niche×cytokine 签名 | 1092 |

## 技术路线还原（勾选实际步骤，按序）

[数据读取(10x_h5+cells.csv+graphclust), 质控QC(calculate_qc_metrics+filter_cells), 归一化(normalize_total+log1p), 降维(scVI latent 30), 聚类(leiden 多分辨率), 注释(celltypist 两级+人工 cluster 映射), 空间邻域/域(CellCharter n_layers=3+AutoK 4-25), 多样本整合(scVI batch_key=sample), 绘图(sq.pl.spatial_scatter+UMAP), 导出(h5ad/figures_niches PDF/tables)] — 共 10 步
未做：HVG（scVI 直接用 counts 全基因）、去卷积、细胞通讯、亚细胞、空间统计、配准/3D。

## 工程审计表（0-2 分/维，共 14）

| 维度 | 分 | 证据 |
|---|---|---|
| ①职责单一 | 1 | 每篇 notebook 单一样本/环节职责尚清，但 28 目录平级无索引层 |
| ②命名规范 | 2 | xenium/ 编号系统 1→8 严格有序；megagut_lvl1/3 列名语义清楚 |
| ③安全性 | 1 | 相对路径 data//h5ad/ 克制，无凭据；但样本 ID 硬编码散布（4a cell13 "0043587_affected"） |
| ④最简化 | 1 | .ipynb_checkpoints 已提交（7a1 与 checkpoint 双份同 783 行）；3a1/4d 等碎篇多 |
| ⑤健壮性 | 0 | notebook 无断言/参数校验；3a cell36 硬编码 leiden 簇号→标签映射，重跑即失效 |
| ⑥可复现性 | 1 | random_state=42（4a cell17 model_params）；4a cell1 import print_versions 但 xenium/ 内 grep 0 次调用【待补充：其余 notebook 是否调用】 |
| ⑦验证纪律 | 0 | 无 env 锁文件/CI/测试；LICENSE 有 |

**总分 7/14**

## 可搬运模式

- PATTERN-025 Xenium 5K 三段式注释迁移链（单样本 celltypist→联合 scVI→子集多分辨率+人工映射）
- PATTERN-026 CellCharter niche 发现契约（delaunay 图→n_layers=3 聚合→ClusterAutoK 稳定性选 k）

## 坑与限制（实读发现）

1. **leiden 簇号→标签是硬编码字典**（3a cell36），leiden 重跑簇号漂移后整段映射作废——搬运时必须改为"簇号→marker 证据→标签"的可追溯映射。
2. celltypist 的 megagut 模型是在 scRNA 上训练的，Xenium 5K panel 只有 ~5000 基因，模型基因集与 panel 的交集大小未见检查——迁移质量依赖基因覆盖。
3. notebook 间靠 h5ad 文件接力（h5ad/xenium5k_scVI.h5ad），无 schema 校验，上游改列名下游静默断。
4. ClusterAutoK (4,25) + max_runs=5 是重计算，GPU trainer_params 写死 accelerator='cpu'（4a cell17）——吞吐瓶颈。
5. 858MB 大仓：克隆后勿在 28 个主题目录里找数据文件，代码集中在各目录 notebook，数据走外部下载。

## 一句总评

"注释列契约"最贴近本组需求的实仓：单样本 celltypist→联合 scVI→子集精修三段式可直接搬，但硬编码簇号映射与无锁环境决定了它只能当"路线参考"而非"可复现工程"。
