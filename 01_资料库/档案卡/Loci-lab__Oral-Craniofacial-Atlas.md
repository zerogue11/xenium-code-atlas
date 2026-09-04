# `Loci-lab/Oral-Craniofacial-Atlas`（档案卡）

> 由 agent 依据本地克隆实测撰写；不确定处一律【待补充】；禁止编造星标/日期/功能。

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-082：《口腔颅面成纤维细胞免疫调节图谱》 |
| 精选级 | A |
| 主分类 | P2（复核维持：图谱 + 自写空间注释方法） |
| 次要用途 | P4（Spatial analysis 目录含 LR 空间配体作图与同型/异型邻接分析） |
| 一句话功能 | 口腔颅面图谱（OCF Atlas）论文伴随代码：阈值法空间细胞类型注释（TACIT）、免疫调节模块（MCIM）与健康/疾病对比、以及一套 4 阶段图学习空间社区（TCN）识别算法 |
| License | 无LICENSE(仅可学习不可转载) |
| 语言与规模 | R×8 / Python×11（TCN 算法为 py），2.8 MB |
| 运行入口 | R 脚本（各子目录一题一脚本）+ TCN/Demo/running_the_algo.ipynb；源数据在论文 GDrive 网盘（README 给链接），无 env 文件 |
| 复现难度 | 中：脚本短小、一题一脚，但数据需从 GDrive 另取且 README 无环境/版本说明，路径需自行适配 |
| 与范式的关系 | TACIT 阈值注释与 TCN 图学习社区识别是可借鉴的自写小工具范式（对比重型依赖方法）；是否候选池待精读 |
| 坑提示 | README 仅 3 行近乎零文档；数据全在 GDrive（国内访问不稳）；"Healthy vs Disease" 目录名含空格，Windows/Git 操作易踩坑；TCN 全称 README 未说明【待补充】 |
| 锁定 SHA | e9e3866dfa3a5e0fa2ff9ff8508236c1b8c692ab |

## 结构速览

- `CellType/TACIT_ocf.R`：TACIT = Threshold-based Assignment for Cell Type Identifying in Spatial Omics，签名矩阵+QC+阈值注释（Seurat+segmented）。
- `MCIMs/MCIMs_Ocf.R` + `Healthy vs Disease/`：免疫调节模块与疾病对比脚本。
- `Spatial analysis/`：连接矩阵、LR 空间作图、drug2cell.ipynb、同型/异型关系、TCN_analysis。
- `TCN/Algo`：stage1 WSI 分块 → stage2 子图构建 → stage3 集体无监督训练 → stage4 TCN 分配（partition/consensus 两版）；`TCN/Demo` 带 demo notebook。

## 实读要点

- TACIT_ocf.R 头注释自述四步：加载数据 → 加载签名矩阵 → QC → Run TACIT；依赖 `ggplot2/Seurat/segmented`，脚本内含 "Colon datasets (Figure 2 top)" 字样，疑似附结肠数据集验证段（未深读确认）。
- TCN/Algo 五个 py 脚本文件名即算法文档：WSI 分块、子图构建、集体无监督训练、按块分配与共识分配两条路线；配套 `running_the_algo.ipynb` 可跑 demo。
- `Spatial analysis/` 共 6 个脚本：Connection matrix.R、LR_Spatial_Plot.R、MCIMs analysis.R、TCN_analysis.R、homotypic or heterotypic.R、drug2cell.ipynb。

## 复现路径（怎么跑）

1. 从 README 给的 GDrive 链接取源数据并按脚本内路径摆放（脚本内路径约定【待补充】——README 未写，需读脚本确定）。
2. 注释/模块对比走 R 线：TACIT_ocf.R → MCIMs_OCF.R → healthy vs disease.R。
3. 空间社区走 TCN 线：TCN/Algo stage1–4 依次运行，先跑 Demo notebook 验证环境。

## 借鉴与风险

- 可移植点：TACIT 的"签名矩阵+阈值"注释思路实现轻（仅 Seurat+segmented），适合做 Xenium 注释的快速旁证；TCN 的 WSI 分块+子图训练流程对 HE→邻域支线有参考价值。
- 风险：零文档零版本锁，R/py 两栈混用；GDrive 数据在境内拉取不稳定；TCN 无论文外独立说明，算法细节需读代码确认。

