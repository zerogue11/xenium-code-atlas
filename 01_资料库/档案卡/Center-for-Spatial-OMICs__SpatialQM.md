# `Center-for-Spatial-OMICs/SpatialQM`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\Center-for-Spatial-OMICs__SpatialQM`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-028：《基于成像的空间转录组学数据集的评估和可重复性标准化度量》（Nat Biotechnol 2025） |
| 精选级 | S |
| 主分类 | P0 流程基准与质控（复核确认，与初判一致） |
| 次要用途 | 可作 Xenium/CosMx 指标计算与出图函数库逐个复用 |
| 一句话功能 | R 包，为成像式空间转录组（Xenium、CosMx、Vizgen MERSCOPE）提供标准化 QC 指标：transcripts/cell、单位面积/核内转录本、稀疏度、熵、信号/阴性对照比、全局 FDR、MECR（互斥共表达率）、Moran's I、轮廓宽度等，并配套 plot* 系列出图 |
| License | 自定义LICENSE(需人工核)（主表值；实读 LICENSE.md 为 MIT 文本，另有一份版权占位式 LICENSE 文件） |
| 语言与规模 | R；.R 脚本 10 个（核心仅 R/ 下 4 个文件）；体积 6.4 MB；带 renv.lock |
| 运行入口 | R 包（remotes::install_github）+ vignettes；可选 inst/scripts/setup_dependencies.R 装依赖 |
| 复现难度 | 中 — 安装链含 GitHub 专有包（Voyager/SpatialFeatureExperiment/RCTD/InSituType，后者需 gcc+gfortran 本地编译），README 已给 Mac Makevars 配置 |
| 与范式的关系 | LIT-028 的指标定义库：getGlobalFDR（阴性对照定特异度）、getMECR、getMorans 等可直接搬进自建 Xenium QC 段，是 P0 质控骨架的现成积木；候选池 |
| 坑提示 | ① Merscope 平台支持 README 自述"under development"；② 实测 DESCRIPTION 的 Imports/Suggests 为空，依赖清单与 README 不一致，以 README 为准；③ InSituType 编译失败是常见卡点 |
| 锁定 SHA | `36e1a59d4ca3f8f360a1d826f5e999d9f40c6760`（主表锁定值；建卡时实测前缀 `36e1a59d4c` 一致） |

## 结构速览

- `R/`：仅 4 个文件——DependencyPackages.R、coercion-input.R（SCE/SPE→Seurat 强转）、utils.R、utils_update_final.R（全部 get*/plot* 函数）
- `inst/`（setup_dependencies.R）、`tests/`、`vignettes/`
- `renv/`+`renv.lock`（锁版本环境）；`docs/`+`_pkgdown.yml`（文档站点）
- `man/`（.Rd 手册）、codecov.yml/.github（CI）

## README/代码实读要点

- 数据入口三种：readSpatial() 读 Xenium/CosMx 路径建 Seurat；SCE/SPE 经 coerce_to_seurat()；或样本表（sample_id/platform/expMat/tx_file/cell_meta）交 getAllMetrics()
- 指标函数逐个独立：getTxPerCell/getTxPerArea/getTxPerNuc、getMeanSignalRatio（基因/阴性对照 log 比）、getMaxRatio/getMaxDetection（动态范围）、getCellTxFraction（Xenium UNASSIGNED/CosMx None 口径）
- getMorans 依赖 SCE→SpatialFeatureExperiment→Voyager 链，基因探针与对照探针分开算
- 可选注释/去卷积：RCTD（spacexr）与 InSituType 均需 GitHub 安装，InSituType 另需 C++ 编译
- plot* 16 个：plotTxPerCell、plotFractionTxInCell、plotMECR、plotMorans、plotSparsity、plotEntropy 等

## 抽读实录

- 读 README 全文（安装、输入表、全部函数说明）；grep DESCRIPTION（Version 0.1.0.9000，Imports/Suggests 实为空）；读 LICENSE/LICENSE.md 头部；ls R/ 全目录。

## 复用建议

- 取函数不取流程：把 getGlobalFDR/getMECR/getMorans/plot* 拆进 zoro-spatial QC 段；整包安装作为 Merscope 兜底方案前先等其开发完成。
