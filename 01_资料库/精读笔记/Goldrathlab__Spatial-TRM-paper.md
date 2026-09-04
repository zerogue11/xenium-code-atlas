# 精读笔记 · Goldrathlab__Spatial-TRM-paper

- repo: Goldrathlab/Spatial-TRM-paper（LIT-035）
- 来源文献: Heeg/Popescu et al. 2025 — "Tissue-resident memory CD8 T cell diversity is spatiotemporally imprinted"（Nature，TRM 时空印记）
- 锁定SHA: ccd50e1cafb8ac86d3daa2a9b1194b81d04c0b56（2025-02-05）
- 复核分类: 应用范式组 · S 级 · 论文级全复现仓（7 条 Xenium/MERSCOPE/VisiumHD 管线 + 逐图 notebook，devcontainer+pixi 工程标杆）
- 精读日期: 2026-09-04（一期精读批次E）

## 代码结构走读

- 实际读取: README 全文、pixi.toml、.devcontainer/devcontainer.json、.pre-commit-config.yaml、两条管线的 core_functions 全文、多个 notebook 首部 cell、图 notebook 抽样。
- 顶层=「processing_pipelines（7 条产数据管线）+ Figure_1~5/Extended_Data_Figure_7（逐图复现层）+ data（download.ipynb+签名文件）」双区结构。
- 每条管线 = 编号 notebook 链（00→14，Baysor 后处理→分割评估→QC→邻域→去坏组织→轴展开→整合→分型→空间分解→终对象）+ 私有 `core_functions/` python 包（6-7 个模块）。
- 入口链：data/download.ipynb 下载数据 → 管线 notebook 顺序执行产出 `data/adata/*.h5ad` 冻结对象 → 图 notebook `sc.read_h5ad("../data/adata/timecourse.h5ad")` 只做浅归一化+绘图（Figure_2/2e.ipynb cell 2-3）。
- README 即导览：预处理参数（xenium-segmentation v0.1.2、baysor.prior_segmentation_confidence=0.95）、7 管线链接、逐图 notebook 链接表、人工注释 xlsx/csv/json 留痕说明（README Preprocessing 节）。

## 关键脚本清单

| 文件 | 一句话 | 行数 |
|---|---|---|
| processing_pipelines/Xenium_human_processing/core_functions/processing_and_filtering.py | QC 契约：plot_qc_feature 小提琴图 + qc_before_clustering 双阈值过滤（20-800 总转录本/8-600 核内） | 106 |
| processing_pipelines/Xenium_human_processing/core_functions/initial_neighborhoods.py | 网格 bin 化→bin 均值表达→NMF 邻域分解→top-words 条形图 | 127 |
| processing_pipelines/Xenium_human_processing/core_functions/unrolling.py | 绒毛"展开"：kNN 距离去离群点→底膜点图→人工标注→轴建模 | 398 |
| processing_pipelines/Xenium_human_processing/07_Integration.ipynb | scVI 整合（n_layers=2, n_latent=30）→neighbors→leiden→MDE | ~200 |
| processing_pipelines/Xenium_human_processing/06_training_crypt_villi_axis_model.ipynb | 人工标注隐窝-绒毛轴参考点→训练轴回归模型 | ~150 |
| Figure_4/figure_object_creation/{01_guide_assignment,02_cluster_filtering,03_celltyping}.ipynb | perturb 对象构建：向导分配→过滤→分型 | 3 篇 |
| pixi.toml + pixi.lock | conda-forge/bioconda 双 channel 精确锁版（scanpy==1.9.5）+ 完整 lockfile | 66+ |
| .pre-commit-config.yaml | black-jupyter + nbstripout（notebook 输出清洗后入库） | 22 |

## 技术路线还原（管线主线，按 notebook 编号序）

[数据读取, 质控QC(分割评估+双阈值过滤), 降维(scVI latent), 聚类(leiden), 注释(人工+tokenize/classify 分型链), 空间邻域/域(网格bin+NMF 邻域), 空间统计(隐窝-绒毛轴模型+卷积热图+轴相关性), 细胞通讯(CellChat, R 侧 3g_part2/5h_part3), 多样本整合(scVI 合并 replicate), 绘图, 导出(冻结 h5ad)] —— 共 11 步。归一化（normalize_total/log1p）只在图级 notebook 做，管线内全程 raw counts；HVG 在管线中未做（grep 无 highly_variable）。MERSCOPE/VisiumHD/perturb 分支：VisiumHD 用 cellpose 核分割（00_train_cellpose.ipynb），perturb 用 PCA 代替邻域。

## 工程审计表（7 维 0-2 分，总分 10/14）

| 维度 | 分 | 证据 |
|---|---|---|
| ①职责单一/模块化 | 2 | core_functions 每模块单一职责（initial_neighborhoods.py 仅邻域三函数）；notebook 单步一文件 |
| ②命名规范 | 2 | notebook 数字前缀严格递增（01_Postprocessing→14_Creating_Final_Object）；图号命名（2abc.ipynb）与 README 表一一对应 |
| ③安全性(硬编码) | 0 | 03_Processing_and_Filtering.ipynb cell2 `data_dir="/mnt/sata1/Analysis_Alex/human_r1"`；各 notebook 内嵌主机路径 |
| ④最简化 | 1 | core_functions 在 4 条管线近重复复制（processing_and_filtering.py 106/107/107 行三份）；unrolling.py:126 注释掉的 D:\Alex 路径残留 |
| ⑤逻辑健壮性 | 1 | initial_neighborhoods.py:45-48 网格越界 `except: None` 静默吞错；processing_and_filtering.py:53-56 裸 except；QC 阈值集中参数化是加分项 |
| ⑥可复现性 | 2 | pixi.toml:12 `scanpy=="1.9.5"` 精确 pin + pixi.lock 全锁 + devcontainer GPU runArgs + postCreateCommand pixi install；notebook 层无 seed【待补充：scVI 训练未设 seed 语句】 |
| ⑦验证纪律 | 2 | 每管线内嵌 02_Evaluating_Baysor_Segmentation.ipynb 专评分割；人工标注 labels/ json + 注释 xlsx/csv 全留痕；pre-commit 强制格式 |

## 可搬运模式

- PATTERN-045 · 管线冻结对象+逐图 notebook 复现契约（本仓灵魂：产数层与出图层分离）
- PATTERN-046 · 网格 bin 化 NMF 空间邻域分解（initial_neighborhoods.py 三函数）

## 坑与限制

- core_functions 按管线复制而非抽公共包，改一处 QC 阈值需同步 4 处（正是我们 zoro 项目纪律要防的）。
- notebook 硬编码 /mnt/sata1 路径，非容器内相对路径，换机即断。
- 裸 except 大量存在，网格 bin 空桶被静默置零（NaN 行事后过滤，逻辑成立但不可见）。
- scVI/leiden 未设 seed，整合聚类严格复现有随机性。
- 人工环节（隐窝-绒毛轴标注、细胞分型）依赖 labels json + xlsx 补档，纯代码无法端到端重跑。

## 一句总评

应用范式组里工程外壳最完整的"全复现仓"：pixi+devcontainer+pre-commit 三件套与"管线产数、逐图复现"的双层组织是可直接照抄的模板，但代码内核（裸 except、复制式共享层、主机路径）说明外壳与内核的成熟度是两回事。
