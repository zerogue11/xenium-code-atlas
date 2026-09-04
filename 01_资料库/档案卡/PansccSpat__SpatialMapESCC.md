# `PansccSpat/SpatialMapESCC`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\PansccSpat__SpatialMapESCC`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-033：食管癌多阶段癌变（仓名 SpatialMapESCC；README 不存在，论文题名/期刊【待补充】） |
| 精选级 | B |
| 主分类 | 复核维持 P8（食管鳞癌多阶段空间图谱应用） |
| 次要用途 | （空） |
| 一句话功能 | 食管鳞癌空间图谱的 R 脚本流水（无 README）：stp1 网格/样本汇总 → stp2 上皮区域与空间（epiArea/epiSpatial/表达空间分布/program 分析与空间映射/FOV 出图/线距离）→ stp3 细胞 niche kmeans、成纤维-上皮距离、免疫/髓系/T 细胞空间分析；Seurat + ComplexHeatmap + data.table 体系，另含 laminar-fish 平台数据对照 |
| License | 无LICENSE(仅可学习不可转载) |
| 语言与规模 | Rx15；0.3 MB（纯脚本平铺，无函数包结构） |
| 运行入口 | 逐脚本运行，执行顺序按 stp1/stp2/stp3 前缀推断；脚本间以 data/*/ 中间 rds/csv 串联 |
| 复现难度 | 高 — 无 README、无 env、无数据；脚本内硬编码作者机器路径（source('~/xenium/header.R')、read_rds('stp2_epi/data/…rds')、fread('~/metaprogram_data/…')），data 目录不在仓内 |
| 与范式的关系 | "上皮程序（QP/CY/MD/TD/HY/RO/DO/AP）× 空间阶段 × niche kmeans"的多阶段癌变叙事可参考；代码本身自用性质强，不建议复跑 |
| 坑提示 | ① 全部输入 rds/csv 缺失且目录树未公开，需按脚本反推自建；② metaprogram 系列来自 ~/metaprogram_data 外部目录（疑似作者其他项目产物）；③ 平台混用：主体似 Xenium/Seurat，另读 lamfish（laminar-fish?）数据，平台对照关系【待补充】 |
| 锁定 SHA | 1f34e3eaa95e60465622705a4225231f3e3aed05（主表） |

## 结构速览

- stp1_gridid.R / stp1_sampleid.R / stp1_summary.R：网格与样本级汇总
- stp2_*（8 个）：上皮区域、空间分布、program 分析、FOV 图、线距离
- stp3_*（5 个）：CN_kmeans niche、成纤维-上皮距离、免疫/髓系/T 空间
- 无 README、无 LICENSE、无 env、无数据

## README/代码实读要点

- head stp2_programAnalysis.R（80 行）：source 硬编码 ~/xenium/header.R；读 ct_epi_SCT_2.rds 等；上皮 8 类 marker（QP:KRT15/MYC、CY:TOP2A/MKI67…）与 program 配色 hardcode
- 分析框架：SCTransform→PCA→UMAP→FindClusters(resolution seq(0.1,1,0.1))，多 resolution 并行（对应 zoro 多候选纪律）

## 抽读实录

- ls 顶层（15 个 R 脚本，确认无 README）；head stp2_programAnalysis.R（80 行）。

## 复用建议

- 只读不跑：借鉴其多阶段上皮 program 命名与"stage × program × niche"交叉叙事；若需复现需联系作者补数据与环境。
