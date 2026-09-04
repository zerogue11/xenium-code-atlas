# `jwangbio/spatial-brain-vasc`（档案卡）

> 由 agent 依据本地克隆实测撰写；不确定处一律【待补充】；禁止编造星标/日期/功能。

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-075：《人体脑血管空间图谱》"Cell and Spatial Atlas of the Brain Vasculature"（Wang et al.；期刊/DOI【待补充】，README 未给） |
| 精选级 | B |
| 主分类 | P8（疾病应用，复核维持） |
| 次要用途 | P3/P6：BANKSY 空间聚类 + 皮层深度打分 + KNN 邻域，方法件可移植 |
| 一句话功能 | 脑血管空间图谱的三项定制分析 R 脚本：BANKSY 空间聚类基础上的皮层深度评分、最近邻（RANN）邻域分析、跨样本/平台 cluster 一致性比较 |
| License | 无LICENSE(仅可学习不可转载) |
| 语言与规模 | R x3（116–151 行/个）；0.0MB |
| 运行入口 | 3 个独立 R 脚本；README 注明 R 4.4.1（Race for Your Life）；无 env 文件（脚本头部 library 清单即事实依赖） |
| 复现难度 | 中 — 脚本自含但硬依赖仓外对象 spatial_atlas_path（readRDS 的图谱对象）需自备；数据在 UCSC CellBrowser 与 UCSF Box 外链 |
| 与范式的关系 | 方法件参考：BANKSY 用法（lambda=0.95、assay=SCT、group='Section_ID'、split.scale=TRUE、k_geom=50）+ 皮层深度打分 + RANN-KNN 邻域组合。候选池：否（覆盖面窄） |
| 坑提示 | ① 无 LICENSE；② 脚本开头 .rs.restartR() 依赖 RStudio，非交互运行会中断；③ 仅 3 个脚本，远非图谱全流程 |
| 锁定 SHA | 主表未登记（空）；本地克隆 HEAD `56002c0c3b86fd3567d416bffe3bc618008d4bec` |

## 结构速览

- `Cortical_depth_score.R`（149 行）：
  - 头部 `rm(list=ls()); gc(); .rs.restartR()` + `set.seed(67)`。
  - 依赖 Banksy、Seurat、SeuratData、SeuratWrappers、harmony、monocle3、slingshot、
    rstatix、RANN、R.cache、pals 等。
  - `readRDS(spatial_atlas_path)` 后 subset 掉 Admixture/Pan-AC/Pan-Ex/Non-specific 注释。
  - `RunBanksy(obj, lambda=0.95, assay='SCT', slot='data', dimx='x', dimy='y',
    features='all', group='Section_ID', split.scale=TRUE, k_geom=50)`。
- `Nearest_neighbors_analysis.R`（116 行）：BANKSY + RANN 最近邻邻域统计。
- `Cluster_concordance.R`（151 行）：cluster 一致性比较（依赖 purrr/tidyr）。
- README：UCSC CellBrowser 浏览器链接（brain-vasc-spatial.cells.ucsc.edu）+
  2026-08-24 更正说明（Table S1 基因名格式，Box 外链）——引用其补充表用新版。
