# `Banovich-Lab/Spatial_PF`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\Banovich-Lab__Spatial_PF`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-025：肺纤维化远端肺重塑分子微环境（README 英文原题 "Spatial transcriptomics identifies molecular niche dysregulation associated with distal lung remodeling in pulmonary fibrosis"，Nature Genetics 2025，GEO: GSE250346） |
| 精选级 | A |
| 主分类 | 复核建议 P3 空间域·生态位（初判 P6 不当：主脚本为细胞生态位识别与细胞邻近/互作计算，无空间统计/配准/3D 内容；终审定夺） |
| 次要用途 | P1 边缘：lumen_preprocessing.R + lumen_segmentation.py 腔隙分割；预处理与细胞注释脚本 |
| 一句话功能 | IPF Xenium 生态位分析手稿代码：Seurat v5 细胞生态位（cell niche）识别、基于 sf+自定义圆域的细胞邻近（proximity）计算与 logistic 回归、聚类/亚聚类、Xenium 细胞分区（partition）与腔隙分割、论文出图 |
| License | 无LICENSE(仅可学习不可转载) |
| 语言与规模 | R 为主（主表 Rx7/Pythonx3/Shellx1）；1.1 MB；13 个脚本平铺顶层，无包结构 |
| 运行入口 | 逐脚本独立运行的 R 脚本/py/ipynb；无 env/renv 文件；数据需自备（GEO GSE250346，README 提示 2024-08-20 曾更新、以 GEO 内 README 为准） |
| 复现难度 | 高 — 脚本内硬编码作者 HPC 绝对路径（如 /scratch/avannan/late_IPF_spatial/...），无环境声明，需自行重组数据路径与依赖版本 |
| 与范式的关系 | "细胞生态位+邻近互作"疾病应用范式：Seurat 系生态位识别 + 手写圆域邻近计算，可与成熟工具（ neighborhoods/Banksy 系）对照；参考池 |
| 坑提示 | ① README 指向 tniche 分支的 transcript_niche 分析（转录本生态位）未随克隆带下（git branch -a 仅 main），该分支是否仍存在【待补充】；② /scratch/... 绝对路径遍布脚本，跑前须批量改路径；③ 生态位脚本 set.seed(0309) 内嵌，结果可复但不宜乱改；④ proximity 计算是自写函数（circleFun+欧氏距离），非成熟库，语义按源码理解 |
| 锁定 SHA | 99da8d1954e0c2680f0b87a672ac5eda9f438178（主表） |

## 结构速览

- 生态位主线：cell_niche_identification.R（Seurat v5 生态位识别）、cellproximity_calculation_share.R/.sh（sf 圆域邻近）、cellproximity_logreg_share.R
- 预处理支线：preprocessing_and_celltype_annotation.R、clustering_subclustering.ipynb、partition_cells_xenium.py、lumen_preprocessing.R + lumen_segmentation.py
- 出图：figures.R、figures_lineage_UMAPs.R；README 含论文链接与 GEO 号
- 关联：无同作者其他仓在库；主题相近仓见肺纤维化/COPD 组（SaulerLab/COPD_snRNA-seq 等）

## README/代码实读要点

- README 主体为作者列表与论文/GEO 链接；唯一的分析指引是"Transcript niche analysis 见 tniche 分支"
- cell_niche_identification.R：Seurat v5 读 Xenium RDS，把 xy 质心注册为 "sp" 降维对象，配全局色表
- cellproximity_calculation_share.R：sf + 自写 circleFun/distance 函数做邻近域计算

## 抽读实录

- 读 README 全文；head cell_niche_identification.R（40 行）、cellproximity_calculation_share.R（20 行）；git branch -a 与 git log -1。

## 复用建议

- 学其"细胞生态位→邻近互作→logreg 关联表型"的叙事结构而非照搬代码；跑通需先在 GEO 重建数据并全局替换路径；transcript niche（转录本级生态位）部分需另去 GitHub 网页确认分支。
