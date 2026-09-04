# `Teichlab/crohns-fibroblast-atlas`（档案卡）

> 由 agent 依据本地克隆实测撰写；不确定处一律【待补充】；禁止编造星标/日期/功能。

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-066：《克罗恩病基质细胞表观遗传调控病理生态位》 |
| 精选级 | S |
| 主分类 | P2（复核维持：克罗恩病成纤维细胞图谱+重分析） |
| 次要用途 | P3（xenium/ 目录用 CellCharter 做 niche 识别）；P0（bulk_ATACseq_pipeline、cNMF、CellTypist 迁移注释等模块化流程） |
| 一句话功能 | 克罗恩病成纤维细胞图谱全量伴随代码：scRNA/scATAC/velocity/bulk 组学/体外细胞因子扰动等约 30 个分析模块，含 Xenium 5K 注释-niche-细胞因子签名完整链（对 Xenium 工作流直接可借鉴） |
| License | MIT |
| 语言与规模 | Python×87 / R×18 / Shell×8，858.0 MB（大数据目录只 ls 未进入） |
| 运行入口 | R 脚本 + Jupyter notebook 混合，按分析主题分目录；顶层 README 仅 1 行标题，无 env 文件【待补充依赖清单】 |
| 复现难度 | 高：模块极多、数据量大（858MB 仓库仍不含 h5ad 原数据）、README 零说明；但单模块（如 xenium 链）可独立借鉴 |
| 与范式的关系 | 高价值：xenium/ 子链 = scVI 整合 → celltypist(megagut+成纤维专用模型) 迁移注释 → CellCharter niche → 细胞因子签名打分的完整 Xenium 5K 参考实现；候选池重点对象 |
| 坑提示 | notebook 内路径为相对路径 `h5ad/xenium5k_scVI.h5ad`，数据不在仓库；xenium notebook 打印版本 scanpy 1.9.6 / squidpy 1.6.0 / cellcharter 0.3.2 / celltypist 1.6.3（照抄版本可省踩坑）；858MB 体积主要在数据/输出目录，勿整体检视 |
| 锁定 SHA | 96e481451695a7380c2b84f26ac60149210dcc7b |

## 结构速览

- `xenium/` + `xenium_cell_abundances_cmp/`：Xenium 5K 分析链（1 数据加载 → 3 注释 → 4 niche → 7 细胞因子签名 → 8 选定 niche 出图）。
- `fibroblast_reanalysis*` 系列：RNA/ATAC 的 cNMF、轨迹（PAGA/monocle 系 notebook）、CellTypist、bulk DE 签名、整合。
- `2020*_scRNA/scATAC_batch*`：原始批处理；`bulk_ATACseq_pipeline`、`bulkRNAseq_Analysis_*`、`LigandCytokine_Expression`、`Spatial_LR_Analysis` 等。
- 顶层共 30 个目录 + LICENSE + README（仅 1 行）。

## 实读要点

- 抽读 `xenium/4a_xenium5k_niche.ipynb`：首 cell 注释 "Test number of niche clusters with CellCharter"；依赖 scanpy/squidpy/celltypist/cellcharter/print_versions；版本打印输出 scanpy==1.9.6、pandas==2.1.4、celltypist==1.6.3、squidpy==1.6.0、cellcharter==0.3.2。
- 载入 `h5ad/xenium5k_scVI.h5ad` 后 AnnData 形状 646,121 细胞 × 5001 基因；obs 含 Xenium 原生 QC 列（transcript_counts、control_probe_counts、nucleus_area、segmentation_method 等）+ megagut lvl1/lvl3 迁移注释列 + fibro 模型列 + MF1/MF2/PC/S1–S5x 概率列 + annot_matthias 人工注释列——即"预训练模型迁移注释 + 亚群概率"的完整落地样例。
- 注释模型组合：celltypist megagut（Teichlab 肠道图谱模型）+ 自训 fibro 模型双层；niche 阶段用 CellCharter 聚类数扫描。
- 其余 30 目录仅 ls 未进（遵守大数据不进入约定），bulk/ATAC/体外实验模块功能按目录名与 README【待补充】。

## 复现路径（怎么跑）

1. Xenium 单链优先（对本项目最相关）：按 xenium/ 编号顺序 1a-1d（样本加载）→ 2（joint）→ 3a-3c（celltypist 注释）→ 4a-4e（cellcharter niche）→ 5-6（免疫/间质出图）→ 7a-7b（细胞因子签名）。
2. 环境按 notebook 打印版本对齐（scanpy 1.9.6 / squidpy 1.6.0 / cellcharter 0.3.2 / celltypist 1.6.3），scVI 对象需自行重建或向作者获取。
3. bulk/ATAC 模块逐目录独立评估，勿求全链复跑。

## 借鉴与风险

- 可移植点：megagut+成纤维双 celltypist 模型迁移注释列结构（predicted_labels/over_clustering/majority_voting/conf_score + S1–S5 概率列）可直接套进本项目 Xenium 注释契约；CellCharter niche 聚类数扫描写法可作 zoro-spatial 邻域层候选实现。
- 风险：数据不在仓、README 零说明；模块间通过中间文件衔接（路径自理）；858MB 仓库克隆与迁移注意磁盘。维持 S 级合理。

