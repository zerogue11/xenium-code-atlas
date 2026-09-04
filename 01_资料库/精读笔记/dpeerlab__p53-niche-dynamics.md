# 精读笔记 · dpeerlab__p53-niche-dynamics

- repo: dpeerlab/p53-niche-dynamics（LIT-078）
- 来源文献: Reyes et al., Cell 2026 — "Oncogenic and tumor suppressive forces converge on a progenitor niche at the benign-to-malignant transition"
- 锁定SHA: a97d1a42cede4c12416875a4aa50d3d63ee1fffd（MIT，LICENSE:1）
- 复核分类: 注释/图谱/生态位组 · S 级 · 论文复现 notebook 群 + RAPIDS GPU 工具库（349MB，不读数据）
- 精读日期: 2026-09-04（一期精读批次C）

## 代码结构走读

- `utils/`（11 模块 2850 行）= 仓库真正的可复用核心：
  - `preprocessing_utils.py`(211行)：size-factor 归一化+log1p（:23-38）、**HVG 三模式选择**（lowess/scanpy seurat_v3/自定义列表，:40-66）、**PCA 数自动选择四模式**（explainedvar50/inflection/kneepoint/fixed + min_pcs 兜底，:134-150）。
  - `neighborhood_utils.py`(170行)：**纯 RAPIDS GPU 邻域库**——cupy/cuml/cudf/cugraph import（:4-7）、`neighbors_gpu`（:86-91）、`get_spatial_knn`（:113-120）、`compute_sample_neighborhoods` 按 slide 切块算 KNN 后汇成 n_obs×n_obs 二值 csr 邻接矩阵（:122-147）、邻域均值/占比聚合（:32-60）。
  - 其余：plotting_functions(543)、copy_number_inference(245)、diffusion_maps(164)、DNA3Bit(FLEX 平台解码)、imaging_utils 等。
- 论文复现层：`transcriptomics/notebooks/`（Xenium/FLEX/KPLOH 等编号 notebook，**全部带 `locked20260305` 式冻结后缀**）+ `imaging_*/notebooks/`（spatialdata 分割-定量-分型-niche 00-09 编号）+ `SBATCH_quantify_data.sh`（HPC 投递）。
- Xenium 主链：step00_raw_tenx_to_adata → step01_embed_tiered_samples（cellbender/scvi/diffusion，grep 证实 cellbender×19、scvi×14、diffusion×114、milo×142）→ step02_annotate_cell_types → **step03_compute_neighborhoods_simplified（GPU KNN + spatialdata 圆环几何邻域：60µm 目标半径先按 70µm 过采样再精修，cell11 自述理由）** → step04_embed_tiered_cell_types；Milo 做邻域差异丰度。

## 关键脚本清单

| 文件 | 一句话 | 行数 |
|---|---|---|
| utils/neighborhood_utils.py | RAPIDS GPU 空间邻域：KNN→csr 邻接→聚合 | 170 |
| utils/preprocessing_utils.py | 归一化/HVG 三模式/PC 数自动选择四模式 | 211 |
| utils/copy_number_inference.py | Xenium CNV 推断 | 245 |
| transcriptomics/.../step03_...locked20260410.ipynb | 邻域计算主 notebook（GPU+rings） | 大 |
| imaging_progenitor_niche/.../03_quantify_channels_batch.py | 成像通道定量批处理（.py 非 ipynb） | 329 |

## 技术路线还原（勾选实际步骤，按序）

[数据读取(10x→adata step00), 质控QC(cellbender 去噪+QC), 归一化(size-factor+log1p), HVG(lowess/scanpy 三模式), 降维(PCA 自动选 PC+scVI+diffusion), 聚类(leiden), 注释(step02 细胞分型), 空间邻域/域(step03 GPU KNN+rings 邻域), 空间统计(Milo 邻域差异丰度), 多样本整合(scVI tiered), 绘图(plotting_functions+GenerateFigure notebooks), 导出(h5ad/csv.gz 中间产物目录化)] — 共 12 步
未做：去卷积、细胞通讯、亚细胞（转录组侧）、配准/3D（成像侧另有分割）。

## 工程审计表（0-2 分/维，共 14）

| 维度 | 分 | 证据 |
|---|---|---|
| ①职责单一 | 2 | utils 共享库与 per-figure notebook 分层；step00-04 单步一 notebook |
| ②命名规范 | 2 | `locked20260310` 冻结后缀+stepNN 前缀+FigN 对应关系（transcriptomics/ 目录清单可验证） |
| ③安全性 | 1 | 相对路径 `../xenium_rawdata/`（step03 cell5）；S3 公开数据链接写死 README |
| ④最简化 | 1 | step03 cell4 原样复制 utils/neighborhood_utils.py:27-53 的 create_diagonal_matrix/get_average_neighborhood_expression（notebook 本地重定义） |
| ⑤健壮性 | 1 | process_pca_var_explained/inflection 有 try/except 回退 50 PC（preprocessing_utils.py:98-103,110-115）；add_obs_names 校验失败 return None 隐患（preprocessing_utils.py:178-180） |
| ⑥可复现性 | 1 | locked 日期冻结纪律是亮点；但 step01 grep 不到 random_state/seed（0 hits）【待补充：seed 可能经 scvi.settings 隐式固定】 |
| ⑦验证纪律 | 1 | locked 后缀即"改版冻结"痕迹+SBATCH 脚本+figure 级 notebook 对应；无 CI/测试 |

**总分 9/14**

## 可搬运模式

- PATTERN-027 RAPIDS GPU 空间邻域库（cupy/cuml KNN→csr 邻接契约）
- PATTERN-028 locked 冻结命名纪律（lockedYYYYMMDD 后缀+figure 级 notebook 对应）
- PATTERN-032 自动 PC 数选择器（explainedvar/inflection/kneepoint/fixed 四模式+min_pcs 兜底）

## 坑与限制（实读发现）

1. `neighborhood_utils.py` 顶层 import cupy/cuml/cudf/cugraph（:4-7）——**无 GPU 环境连 import 都失败**，CPU 回退不存在（与 zoro"strict GPU"标准同款取舍）。
2. step03 notebook 本地重定义工具函数（cell4）导致 utils 与 notebook 双源，改 utils 不影响旧 notebook——搬运时以 utils 版为准。
3. 邻域是"锚-邻居"非对称 csr 矩阵（compute_sample_neighborhoods 返回 [1]*len(sources) 的单值矩阵），列归一在聚合函数里另做——复用时注意方向。
4. 数据靠 S3 tar.gz（README），代码仓不含数据；复现需先下 4 个 tar 包再按 locked notebook 顺序跑。
5. notebook 密度极高（单篇 step03 同时含几何、GPU、聚合、输出目录管理），拆解成本大，建议只抽 utils 层。

## 一句总评

本组最有"工程自觉"的论文仓：locked 冻结后缀+utils 抽库+GPU 邻域层三件事都做到了——直接对标 zoro-spatial 的 run_metadata 与 strict GPU 纪律，notebook 冗余是唯一硬伤。
