# `digitalcytometry/spatialecotyper`（档案卡）

> 由 agent 依据本地克隆实测撰写；不确定处一律【待补充】；禁止编造星标/日期/功能。

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-047：《空间生态型无创分析TME》（Non-invasive profiling of the tumour microenvironment with spatial ecotypes, Nature 2026, doi:10.1038/s41586-026-10452-4） |
| 精选级 | S |
| 主分类 | P2（复核维持：分类体系 P2 定义明列 SpatialEcotyper——生态位型注释/图谱映射） |
| 次要用途 | P3（空间生态型=多细胞社区识别）；P0（bulk 去卷积训练/恢复管线） |
| 一句话功能 | Spatial EcoTyper 正式 R 包（v1.0.4）：NMF 无监督框架从单细胞空间数据发现空间生态型（spatial ecotypes），并支持从 scRNA-seq、空间转录组、bulk 数据跨模态恢复/去卷积，含 8 个官方教程 |
| License | 自定义LICENSE(需人工核)：DESCRIPTION 注明 STANFORD NON-COMMERCIAL SOFTWARE LICENSE AGREEMENT（非商业许可） |
| 语言与规模 | R×42（R/ 目录 34 个函数文件），114.6 MB（含 docs/pkgdown 与数据） |
| 运行入口 | R 包：`BiocManager::install("digitalcytometry/spatialecotyper")` 或源码安装；依赖 R≥4.2、Seurat≥4.2、NMF≥0.25、spdep、ComplexHeatmap、presto；README 给 conda 方案与文档站 digitalcytometry.github.io/spatialecotyper |
| 复现难度 | 低：包级安装 + 8 个分步教程（单样本发现→多样本整合→NMF 训练→scRNA/ST 恢复→bulk 去卷积），文档完备 |
| 与范式的关系 | 高价值方法池候选：EcoTyper 团队（Newman lab, Stanford）官方升级版；"NMF 生态型发现 + 跨模态恢复 + bulk 去卷积"可直接嫁接进本项目空间邻域分析层 |
| 坑提示 | 非商业许可限制再分发/商用；Seurat v4/v5 结果有轻微差异（README 自述已双版验证）；presto 经 GitHub 安装可能需 GITHUB_PAT（README troubleshooting 给了解法）；依赖 Seurat 较深 |
| 锁定 SHA | 57d37cd2c31c2b0743a7d50e036c4d4a50b61eee |

## 结构速览

- `R/`：核心函数 34 个——NMF 系（NMFGenerateW/NMFpredict/nmfClustering/SelectBestRank）、空间 metacell（GetSpatialMetacells）、发现与恢复（SpatialEcoTyper/MultiSpatialEcoTyper/RecoverSE/DeconvoluteSE/IntegrateSpatialEcoTyper）、统计与可视化（Coassociation/Colocalization/MoranI/SpatialView）。
- `vignettes/` + `docs/` + `pkgdown/`：8 教程与文档站源。
- `DESCRIPTION`/`NAMESPACE`/`NEWS.md`：标准 R 包结构；另有 Stanford web app（spatialecotyper.stanford.edu）。

## 实读要点

- DESCRIPTION 实读：Version 1.0.4，maintainer Wubing Zhang（Stanford）；Depends 明确 R(≥4.2.0)、Seurat(≥4.2.0)、Matrix(≥1.5)、RANN(≥2.6)、NMF(≥0.25)、ggplot2、pals；Imports tidyr/dplyr/circlize/ComplexHeatmap(≥2.12)/spdep(≥1.4.2)/data.table(≥1.14)；自述"unsupervised machine learning framework for discovering spatial ecotypes (multi-cellular communities) from single-cell spatial data"。
- 语言复核结论：确认为标准 R 包（Rproj + DESCRIPTION + NAMESPACE + man/ + vignettes），不是脚本集合。
- 8 个官方教程覆盖完整使用闭环：单样本发现 / 多样本整合 / NMF 训练（sc+ST）/ 留一样本交叉验证 SE 特异细胞态 / scST 恢复 / scRNA 恢复 / bulk 去卷积模型训练 / bulk 丰度推断。
- README 引用同一团队 Liquid EcoTyper 与 web 平台（支持 Visium、bulk RNA-seq、肿瘤/血浆甲基化谱的生态型丰度推断）。

## 复现路径（怎么跑）

1. 安装：conda 建环境（r-base/r-seurat/r-spdep/r-nmf + bioconductor-complexheatmap）→ BiocManager 装 presto（失败按 README 设 GITHUB_PAT）→ BiocManager::install("digitalcytometry/spatialecotyper")。
2. 学习闭环按 8 教程顺序：单样本发现 → 多样本整合 → NMF 训练 → 恢复（scST/scRNA）→ bulk 去卷积训练与推断。
3. 用本项目 Xenium 注释后的对象（含细胞类型列）可直接进 GetSpatialMetacells → SpatialEcoTyper 主流程试跑。

## 借鉴与风险

- 可移植点：空间 metacell→NMF 生态型→跨模态恢复的三段式可整体作为本项目空间生态型层的方法候选；去卷积模型可对接 bulk/面板数据。
- 风险：Stanford 非商业许可影响代码再分发（本项目内部使用需留意）；NMF rank 选择（SelectBestRank）与 Seurat 版本都会影响结果稳定性。S 级+文档完备，无需升格动作。

