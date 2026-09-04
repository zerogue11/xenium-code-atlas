# `dwilliamsLab/gingiva-2025`（档案卡）

> 由 agent 依据本地克隆实测撰写；不确定处一律【待补充】；禁止编造星标/日期/功能。

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-067：《口腔黏膜免疫空间组织》（论文题录【待补充】，README 及子 README 均未给） |
| 精选级 | A |
| 主分类 | P8（疾病应用，复核维持） |
| 次要用途 | P3/P4（Xenium 邻域与 niche 功能 notebook）；IBEX 多重荧光成像的 ImageJ 宏预处理 |
| 一句话功能 | 牙龈组织三模态（CITE-seq / IBEX 成像 / Xenium）联合分析集合：R 细胞系注释脚本 + Xenium Rmd 处理管线 + Python 复聚类/邻域/niche 功能 notebook + ImageJ 宏 |
| License | MIT |
| 语言与规模 | Python x13（主表口径；另有 8 个 .R、5 个 .Rmd、7 个 .ijm、多 ipynb）；23.1MB |
| 运行入口 | R 脚本/Rmd（Seurat 系）与 Jupyter notebook 并行；`ibex/imagej/*.ijm` 在 FIJI/ImageJ 中运行；无 env 文件 |
| 复现难度 | 中-高 — 无环境/版本说明，数据下载链接 README 未提供【待补充】；三模态各自独立、靠 notebook 串联 |
| 与范式的关系 | 候选池（黏膜屏障免疫场景）：Xenium Rmd 01–05 编号管线 + xenHelpers.R 可抄；ImageJ 宏是稀有素材 |
| 坑提示 | ① 主/子 README 均为一行空标题；② ImageJ 宏文件名含括号，shell 引用需转义；③ Rmd 与 notebook 两套注释体系并存 |
| 锁定 SHA | 主表未登记（空）；本地克隆 HEAD `860a0e8afd32874826a965e9fdc98afe5e4a9783` |

## 结构速览

- `cite-seq/`：8 个 R 脚本，按细胞系分文件注释。
  - B Plasma Final.R、Cycling.R、Epithelial.R、Myeloid Final.R、Stromal Final.R、TNK final.R。
  - Integration and General Cell Types.R（跨样本整合与通用细胞类型）。
  - Shortened gene lists.R（精选基因列表）。
- `xenium/`：Seurat 系 Rmd 编号管线 + Python 复聚类双轨。
  - 01_Crop-Setup_run1-and-2_0um.Rmd（裁切与两个 run 的 setup）、02_Integration.Rmd、
    03_Clustering.Rmd、04_Annotation.Rmd。
  - 05_01_Analysis-Viz-Seurat.Rmd、05_02_CZI-datasets-PathAnalysis.Rmd、05_03_gingiva_PathAnalysis.Rmd。
  - 1)Reclustering_Xenium_in_Python.ipynb（Python 侧重聚类）、
    2)Xenium_neighborhood_analysis.ipynb、
    3)Epithelial_Stromal_functionality_per_niche.ipynb、4)Xenium_Figures_Manuscript.ipynb。
  - xenHelpers.R：管线共享函数。
- `integration-cite-seq/`：citeseq-Xenium_integration.ipynb（CITE-seq↔Xenium 映射）。
- `integration-tabSap/`：1)Epithelial_cross_organ_integration.ipynb（上皮跨器官整合）、
  2)Epithelial-integration-Figure generation.ipynb；子 README 为空标题。
- `ibex/`：Jupyter-notebook（code/files）+ imagej/ 宏 7 个。
  - A)Remove_detached_areas.ijm（单样本/批处理/H5 三个变体）。
  - B)Create_segmentation_multichannel_file.ijm、C)Segmentation_multichannel_file_to_hdf5.ijm。
  - D)IBEX_automated_channel_processing.ijm、E)CalculateROIs_.ijm。

## 实读补充

- 文件名带 `A)` `B)` 前缀表达执行顺序，是 ImageJ 宏常见的排序技巧；命令行调用需加引号。
- Xenium 侧"Rmd 出注释 → Python notebook 复聚类与邻域 → 成图 notebook"的接力顺序
  需按文件名编号推断，无总 README 说明。
