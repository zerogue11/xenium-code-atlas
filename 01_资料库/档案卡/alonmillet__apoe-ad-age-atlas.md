# `alonmillet/apoe-ad-age-atlas`（档案卡）

> 由 agent 依据本地克隆实测撰写；不确定处一律【待补充】；禁止编造星标/日期/功能。

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-012：《APOE4/老年AD小胶质细胞》（Millet, Ledo et al., An Exhausted-Like Microglial Population Accumulates in Aged and APOE4 Genotype Alzheimer's Brains） |
| 精选级 | A |
| 主分类 | P2（复核维持：衰老/APOE4 小胶质细胞图谱） |
| 次要用途 | P5（multiome 的 SCENIC+/MIRA 顺式调控）；P4（CellPhoneDB/Compass）；Xenium 空间分析 |
| 一句话功能 | 论文全图复现代码：按图号一文件组织（Fig_1–7 R 脚本）+ CellRank/SCENIC/SCENIC+/MIRA/Xenium 配套 Python 笔记本，覆盖 10w/20w/96w 图谱、multiome、Xenium 六样本与 aducanumab 实验 |
| License | MIT |
| 语言与规模 | R×9 / Python×7，3.2 MB |
| 运行入口 | R 脚本（Fig_xxx.R 一图一文件）+ Jupyter notebook（CellRank、SCENIC、SCENIC+、MIRA、Xenium/squidpy）；数据在 GEO（GSE225503/GSE239977/GSE239974/GSE239975）与 Zenodo 10.5281/zenodo.8206638；无 env 文件 |
| 复现难度 | 中：README 逐文件给输入-输出与 accession，结构极清晰；但跨 Seurat/Signac/scanpy/squidpy 多栈且无版本锁 |
| 与范式的关系 | Xenium.ipynb 是轻量 Xenium→squidpy→R 出图的简洁参考；"一图一脚+README 逐段对应"的交付组织值得借鉴 |
| 坑提示 | Xenium 笔记本用 `glob('output*')` 就地读 Xenium 输出目录，路径约定需自行重建；SCENIC 系安装本身重；无依赖版本锁定 |
| 锁定 SHA | 754663ba478a4c9b8a869d2bb90b401bce35a566 |

## 结构速览

- 顶层 10 个 `Fig_*.R` + `Fig_6.R`：一图一脚本（Seurat/Signac 构建、DGE、in silico 分解、SCENIC/CellPhoneDB/Compass 调用）。
- `CellRank/`：h5ad 生成（splice-aware 比对）→ scVelo → CellRank 自定义 kernel 三个 Python 笔记本。
- `SCENIC.ipynb`、`SCENIC+.ipynb`、`MIRA Notebook.ipynb`、`Xenium.ipynb`：R 产物的 Python 下游。
- `schematic.png`：论文示意图。

## 实读要点

- README 逐文件段落写明每图输入输出与数据 accession：GSE225503（atlas+multiome）、GSE239977（bulk 免疫分解）、GSE239974（Aβ 摄取分选）、GSE239975（aducanumab 实验）、Zenodo 10.5281/zenodo.8206638（Xenium 原始+anndata+甲氧基-X04 全片扫描）。
- 抽读 `Xenium.ipynb`：6 个样本（E3×3、E4×3），`sc.read_10x_h5(cell_feature_matrix.h5)` + `cells.csv.gz` 合并 obs，用 `x_centroid/y_centroid` 构造 `obsm['spatial']`，QC（min_counts=5/min_cells=5）→ normalize_total → log1p → PCA → anndata.concat，后续转 R 绘图——标准轻量 Xenium 入口写法。
- scUTRquant（3'UTR 定量）按 Mayrlab 官方 Snakemake 管线外跑，参数在 README 明列（bx_whitelist=3M-february-2018、tech=10xv3、--fr-stranded、min_umis=1000）。

## 复现路径（怎么跑）

1. 按 README 段落下载对应 GEO/Zenodo 数据（每段都给了 accession 与随附 rds/h5ad 说明）。
2. R 线：Fig_1A-G（Seurat 构建+亚群）→ Fig_1H（bulk 分解）→ Fig_2/3（SCENIC、Signac multiome）→ Fig_4（跨物种/人锚定整合）→ Fig_6/7（功能实验）。
3. Python 线：CellRank、SCENIC(.ipynb)、SCENIC+、MIRA、Xenium(squidpy) 各笔记本接 R 产物。

## 借鉴与风险

- 可移植点：Xenium.ipynb 的 h5+cells.csv.gz→squidpy 前处理段（约 10 个 cell）是可抄的最小 Xenium 入口；"一图一脚+README 逐段对应+数据 accession 前置"是论文复现仓的交付范本。
- 风险：无版本锁、SCENIC 系安装重；`glob('output*')` 就地读目录的约定需重建目录名。文档质量突出，A 级合理；不建议升 S（无环境锁定、无管线封装）。

