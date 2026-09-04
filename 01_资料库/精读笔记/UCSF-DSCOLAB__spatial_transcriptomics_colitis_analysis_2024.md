# 精读笔记 · UCSF-DSCOLAB__spatial_transcriptomics_colitis_analysis_2024

- repo: UCSF-DSCOLAB/spatial_transcriptomics_colitis_analysis_2024（LIT-053）
- 来源文献: Mennillo/Lotstein et al. 2024 bioRxiv — 结肠炎（UC）FFPE 活检空间转录组，9 数据集（7 Xenium + 1 CosMx + 1 MERSCOPE）跨平台细胞网络
- 锁定SHA: ef610b37ed40f37a6549465e33cb95ac706b34d1（2026-04-19，"Update mapping function"）
- 复核分类: 应用范式组 · S 级 · 跨平台泛化管线（UC 课题第一参照仓）
- 精读日期: 2026-09-04（一期精读批次E）

## 代码结构走读

- 实际读取: README 全文、Preprocessing 4 个 notebook 关键 cell、Additional_QC/QCComparisons_CrossPlatforms.ipynb、CellCharter notebook、DownstreamComparisons notebook、3 个环境 yaml。
- 顶层 5 目录按"阶段"划分：Preprocessing（4 个平台版预处理）/ Additional_QC（跨平台 QC 对比+转录本级 QC）/ DESeq2 + GSEA（R 侧）/ More_Downstream（CellCharter+跨平台下游）/ Python_Yaml_Files（3 环境）。
- 体量：全仓 10 个 notebook + 4 个 Rmd + 3 个 yaml，无独立 .py 模块，逻辑全部内嵌 notebook cell。
- 入口链：GEO 原始 bundle → Preprocessing_XeniumRep1and2.ipynb（sc.read_10x_h5 + cells.csv 拼 obs → QC → filter → 归一化 → harmony → leiden）→ 标注 h5ad → CellCharter/DownstreamComparisons 消费。
- 关键跨平台设计：所有 notebook 路径统一用 `/path/` 占位（脱敏），notebook 首个 markdown 声明"所需输入文件+用哪个 conda 环境"，可当模板直接抄。
- QC 泛化做法（本仓核心价值）：统一过滤核心（min_counts=50/min_genes=10/基因 min_counts=1/min_cells=10）在三平台 notebook 中逐字一致（Merscope 版 cell18 注释自证 "matches CosMx and Xenium"），平台差异以"补丁层"追加——CosMx 追加 NanoString qcFlags 五连 Pass 过滤（cell20），MERSCOPE 追加 FOV/体积指标与 lite 方案（min_counts=10，小样本数据集）。控制探针/解码负对照比例按平台 obs 列名分别计算（Xenium control_probe_counts vs CosMx nCount_negprobes）。

## 关键脚本清单

| 文件 | 一句话 | notebook cell 数 |
|---|---|---|
| Preprocessing/Preprocessing_XeniumRep1and2.ipynb | 主链：读 10x h5→QC→统一过滤→HVG→regress/scale→PCA→harmony→neighbors/UMAP/leiden | 124 |
| Preprocessing/Preprocessing_CosMx.ipynb | CosMx 版：同核心过滤 + NanoString qcFlags 补丁层 | 52 |
| Preprocessing/Preprocessing_Merscope.ipynb | MERSCOPE 版：同核心过滤 + FOV 指标 + lite 方案 | 55 |
| Additional_QC/QCComparisons_CrossPlatforms.ipynb | 转录本级跨平台 QC：重叠基因表、核重叠率、每细胞转录本数分布 | 70 |
| More_Downstream/CellCharter_CombinedXeniumDatasets1and3_275SharedGenes.ipynb | CellCharter niche：275 共享基因子集+aggregate_neighbors+AutoK 多 k 候选 | 41 |
| More_Downstream/DownstreamComparisons_CrossPlatforms.ipynb | 跨平台标注级下游对比（Xenium rep1 vs CosMx） | 55 |
| DESeq2/Xenium_DESeq_Dataset1_HC_UCPRE.Rmd + GSEA/*.Rmd | R 侧 UC vs HC 差异与 GSEA；配 h5ad→Seurat 转换 notebook | 2+1 |

## 技术路线还原（按执行序）

[数据读取(各平台 bundle 拼装), 质控QC(统一过滤核心+平台补丁层+控制探针比例), 归一化(normalize_total→log1p→存 layer), HVG(min_mean=0.0125,max_mean=3,min_disp=0.5), 降维(PCA arpack), 聚类(leiden), 注释(独立标注流程，本仓未见代码【待补充】), 空间邻域/域(CellCharter n_layers=3+AutoK), 空间统计(squidpy 邻域富集 NeighborhoodEnrichmentAnalysis), 多样本整合(harmony on batch), 绘图, 导出(分阶段 write_h5ad: pre-norm/post-norm/post-harmony)] —— 共 12 步。细胞通讯/去卷积/配准未做。

## 工程审计表（7 维 0-2 分，总分 8/14）

| 维度 | 分 | 证据 |
|---|---|---|
| ①职责单一/模块化 | 1 | 阶段目录划分清晰、notebook 单职责；但三平台预处理为复制式 notebook 而非共享函数，改过滤阈值需同步 3 处 |
| ②命名规范 | 1 | 数据对象带日期版本前缀（cell3 `25_11_22_Xenium_Dataset1_290_IntReps1and2_Annotated.h5ad`）是亮点；目录名冗长（More_Downstream_Analyses_And_Visualizations） |
| ③安全性(硬编码) | 1 | notebook 层全部 `/path/` 占位脱敏（好习惯）；但 default_env.yaml:280 泄漏个人 HPC prefix `/c4/home/mlotstein/.conda/envs` |
| ④最简化 | 1 | Sept/Nov 双对象代码块成对复制（cell50/54/55/57），教学性 markdown 重复多 |
| ⑤逻辑健壮性 | 1 | 无 assert；有 print 自检（cell61 保留细胞比例复算）；autok pickle 持久化容错好（cell17） |
| ⑥可复现性 | 2 | 3 个 conda yaml 全 pin（default_env.yaml:156 python=3.7.7, :263 scanpy==1.9.3, harmony yaml:238 harmonypy==0.0.9）；CellCharter notebook cell1 `seed_everything(12345)`+`scvi.settings.seed=12345`；autok 多 k(8,9,10) 并存支持终审 |
| ⑦验证纪律 | 1 | QCComparisons/BlockAge/MECR 三个专项 QC notebook 即验证件；无 CI/测试；无验证计划文档 |

## 可搬运模式

- PATTERN-047 · 跨平台统一 QC 核心+平台补丁层（本仓最值钱的一招）

## 坑与限制

- 三份平台 notebook 是复制关系而非参数化模板：统一阈值虽一致，但这是靠"人肉保持一致"，没有单一事实源。
- 环境 python=3.7.7 + scanpy 1.9.3 较旧，与 CellCharter env（另环境）之间的对象传递靠 h5ad 文件落盘中转。
- 环境 yaml 里残留 conda prefix 个人路径，直接 `conda env create` 会报/带脏信息。
- "275 共享基因"交集对齐只在文件名/notebook 标题体现，重叠基因列表 csv 未入仓【待补充：仅 QCComparisons cell5 读入 CosMx1000Xenium290 重叠表路径】。
- 注释（cell type annotation）环节代码缺失，标注对象直接作为输入出现——复现链在注释处断档。

## 一句总评

跨平台泛化的"最小可信模板"：统一 QC 核心+平台补丁层+`/path/` 脱敏+多环境 yaml 的做法可以直接抄进我们 UC 课题，但复制式 notebook 与断档的注释环节提醒——模板抄的是纪律，不是代码本身。
