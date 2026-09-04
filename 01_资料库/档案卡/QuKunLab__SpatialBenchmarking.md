# `QuKunLab/SpatialBenchmarking`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\QuKunLab__SpatialBenchmarking`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-088：《通过质量评估和最佳实践分析工作流优化Xenium原位数据效用》（主表映射；注意：README 自引为 Li, B. et al. "Benchmarking spatial and single-cell transcriptomics integration methods...", Nat Methods 2022——映射关系待项目主审复核【待补充】） |
| 精选级 | S |
| 主分类 | P0 流程基准与质控（复核确认，与初判一致；整合方法基准测试） |
| 次要用途 | 基因插补/去卷积方法选型证据源（服务 LIT-088 gene imputation 段的同类方法族） |
| 一句话功能 | 空间-单细胞整合方法系统基准：45 个配对数据集+32 个模拟数据集，评测 8 种 RNA 空间分布预测方法（gimVI、SpaGE、Tangram、Seurat、SpaOTsc、LIGER、novoSpaRc、stPlus）与 10 种细胞类型去卷积方法（cell2location、RCTD、SpatialDWLS、Stereoscope、SPOTlight、STRIDE、DestVI、DSTG 等），含稀疏矩阵下采样测试 |
| License | BSD（主表值，与仓库 LICENSE 一致） |
| 语言与规模 | Python 为主 + R；py/ipynb 29 个 + R 8 个；体积 111.2 MB |
| 运行入口 | conda env（Benchmarkingenvironment.yml）→ sh Config.env.sh → BLAST_GenePrediction.ipynb / BLAST_CelltypeDeconvolution.ipynb；doc/Tutorial.pdf 与 Tutorial.ipynb |
| 复现难度 | 高 — 需 R 3.6.1 与 8+10 个方法包的精确版本组合（cell2location 0.6a0、Seurat 4.0.5、scvi-tools 0.11.0 等），README 自述仅在 CentOS Linux 测试 |
| 与范式的关系 | P0 方法基准范式：哪些插补/去卷积方法在什么数据条件下更优，可直接引用其结论选型（不必重跑）；候选池（结论引用优先） |
| 坑提示 | ① 版本组合严苛，新版 Python/R 环境下老包（scvi-tools 0.11.0 时代）大概率装不上；② 全部数据从 Google Drive 目录下载，国内网络不可达风险高；③ 顶层目录名拼写 "Extenrnal"（External 拼错），引用路径时注意 |
| 锁定 SHA | 【待补充：主表"锁定SHA"列空】；本地克隆 HEAD 实测 `3586b9d81c` |

## 结构速览

- `Benchmarking/`：核心包——SpatialGenes.py（基因分布预测评测）、DeconvolutionSpot.py、GenesMetrics.py、data_downsample.py
- `Codes/`：Impute、Deconvolution 两子目录（各方法运行代码）
- 顶层 3 个 notebook（BLAST_GenePrediction、BLAST_CelltypeDeconvolution、SimulatedData）+ Config.env.sh + Benchmarkingenvironment.yml
- `doc/`（Tutorial.pdf/ipynb）、`FigureData/`、`Extenrnal/`

## README/代码实读要点

- 评测设计四步：8 方法精度评测→4 种输入表达矩阵方案对比→5 数据集下采样稀疏测试→10 方法去卷积评测
- 安装链明确：Miniconda→yml 建 env→sh Config.env.sh→R 内补装 vctrs/rlang/htmlwidgets；耗时 7-15 分钟
- 复现入口：两个 BLAST notebook 对应论文图 2 与图 4
- Benchmarking/SpatialGenes.py 顶部 import 面即评测栈：scipy.stats.wasserstein_distance、sklearn KFold、scanpy、multiprocessing

## 抽读实录

- 读 README 全文（方法清单、版本要求、安装步骤、数据来源）；ls Benchmarking/、Codes/；读 Benchmarking/SpatialGenes.py 开头 20 行（评测组件）。

## 复用建议

- 以"结论引用"为主：按自身数据形态（面板大小、稀疏度）查其图表选插补/去卷积方法；重跑仅在 CentOS+老版本 R 可行；Tutorial.ipynb 是把新数据跑通任一方法的最短路径。
