# `spencerfar/fetal_lung_analysis`（档案卡）

> 由 agent 依据本地克隆实测撰写；不确定处一律【待补充】；禁止编造星标/日期/功能。

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-008：《胎儿肺图谱》"Early human fetal lung atlas reveals the temporal dynamics of epithelial cell plasticity"（配套主仓 The-HQQ/Human_fetal_lung_atlas，README 直链） |
| 精选级 | A |
| 主分类 | P8（疾病应用/发育场景，复核维持） |
| 次要用途 | 拟时/速度（latentvelo、scFates、cellrank、slingshot、tradeSeq）；P4（CellChat signaling） |
| 一句话功能 | 胎肺图谱论文的轨迹、信号、空间（Visium/Xenium）与 hPSC 分析配套仓：按细胞系与方法主题分 9 个目录的 notebook/脚本集合 |
| License | MIT |
| 语言与规模 | Python x28（另含 R/CellChat 脚本与多 ipynb）；29.9MB；根目录含数据集清单 xlsx |
| 运行入口 | 各主题目录内 ipynb/py；无 requirements.txt/yml，README 给完整版本清单（见实读补充） |
| 复现难度 | 中 — 版本清单明确、按主题分目录易导航；数据依赖主 atlas 仓与 GEO，accession【待补充】 |
| 与范式的关系 | 候选池（发育场景三线并行范本）：latentvelo 按 lineage 速度分析、CellChat 三件套、GW15 vs GW18 同平台跨时点对比 |
| 坑提示 | ① Citation "Coming..."；② 无 env 文件只靠 README 手列版本；③ 脚本命名含空格/大小写混用 |
| 锁定 SHA | 主表未登记（空）；本地克隆 HEAD `babeafce3daf1e1c199eadb71d28fb0a4d60a5fb` |

## 结构速览

- 细胞系四目录：endothelial、epithelial、immune、stromal（各自分析脚本）。
- 方法五目录：
  - hpsc/：多能干细胞分化方案对比分析。
  - latentvelo/（实测）：endothelial.py、epithelial.py、immune.py——按 lineage 各一的速度分析脚本。
  - signaling/（实测）："Cellchat all pathways.ipynb"、"Ligand Receptor analysis.ipynb"、
    "Signalling expression analysis.ipynb"——CellChat 三件套（R/CellChat 1.6.1）。
  - visium/：Visium 空间分析。
  - xenium/（实测）："Xenium week 15 enrichment.ipynb"、"Xenium week 18 enrichment.ipynb"、
    "TP proximity.ipynb"、xenium_GW15.py、xenium_GW18.py——GW15/GW18 两时点富集对比 +
    TP（terminal/proximal? 区域邻近）分析。
- 根目录 `Wong_Fetal_Lung_Dataset_August_2023.xlsx`：数据集对照清单。

## 实读补充（README 版本清单原文）

- Python：python 3.8.10、numpy 1.22.4、pandas 1.4.2、scanpy 1.9.1、scvelo 0.2.5、
  cellrank 2.0.0、anndata 0.8.0、matplotlib 3.5.2、sklearn 0.24.0、seaborn 0.13.0、squidpy 1.2.3、
  scFates 1.0.6。
- R：4.1.3、CellChat 1.6.1、Matrix 1.6.5、ggplot2 3.5.0、slingshot 2.7.0、
  SingleCellExperiment 1.16.0、tradeSeq 1.8.0。
- 版本组合较老（scanpy 1.9 / scvelo 0.2.5 时代），新建环境建议按此 pin，勿混用新版 API。
