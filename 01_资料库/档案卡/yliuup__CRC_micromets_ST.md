# `yliuup/CRC_micromets_ST`（档案卡）

> 由 agent 依据本地克隆实测撰写；不确定处一律【待补充】；禁止编造星标/日期/功能。

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-074：《结直肠癌宏微转移空间多组学》"Spatial Multi-Omics Landscape of Colorectal Cancer Macro- and Micrometastases"（Liu Y. et al.，MD Anderson；期刊/DOI【待补充】，README 未给） |
| 精选级 | A |
| 主分类 | P8（疾病应用，复核维持） |
| 次要用途 | P3（基质屏障/免疫抑制 niche）；P6（CNV 系统发育 + 空间联合解读）；bulk 验证支线（CLiMi 六基因 signature） |
| 一句话功能 | CRC 原发灶-肝/肺转移 49 例（19 患者）空间多组学复现：Figure1–7 每图 R 脚本 + 随仓 Visium 病理注释元数据，软件版本清单完整 |
| License | 无LICENSE(仅可学习不可转载) |
| 语言与规模 | Python x3 / Shell x1（主表口径；R 脚本为主）；8.6MB |
| 运行入口 | Figure1/Figure1D_E.R 等按图组织；Meta_data/ 提供 visium_meta_raw/after_qc.rds；README 给完整版本清单（R+Python 双侧） |
| 复现难度 | 中 — 版本清单与病理注释元数据齐备；原始数据 accession【待补充】，上游产物需自跑 |
| 与范式的关系 | 候选池（P8 转移场景最完整论证链之一）：克隆演化 × 空间生态位 × signature 生存验证三层结构；Meta_data 随仓是少见好做法 |
| 坑提示 | ① 无 LICENSE；② Readme/ 目录与 README.md 并存（注意大小写）；③ 每图仅 1–2 个脚本、上游处理散落各图 |
| 锁定 SHA | 主表未登记（空）；本地克隆 HEAD `b6c40903eeda67d812712f2bb77064041db38e6c` |

## 结构速览

- `Figure1`–`Figure7`：每目录 1–2 个脚本（实测 Figure2/：Figure2A.R、Figure2C_S4A.R、
  Figure2D_E_F_G_H.R、Figure2I.sh、infercnv.R）。
  - Figure2A.R（实测头部）：ape + phangorn + ggtree + ggsci；
    输入 `avg.cnv.df`（样本×特征 CNV 矩阵），先算距离（euclidean/manhattan 可选）再建 NJ 树
    ——CNV 系统发育进入空间分析的标准写法。
- `Meta_data/`（实测）：visium_meta_raw.rds、visium_meta_after_qc.rds——
  Visium 样本病理注释（区域标签、病理分类、配套元数据），README 明示供下游空间分析用。
- `Readme/`：图形摘要 graphical_abstract.jpg。
- README.md 摘要要点：
  - 49 tumors / 19 patients；spot 级 + 高分辨 ST + 多区域 LCM-WGS + 高plex 蛋白成像。
  - 肝微转移（CLiMi）源自早期克隆分歧，保留干性静息态（metastatic dormancy）。
  - 巨转移被肌成纤维包裹；微转移被 T 细胞耗竭型免疫抑制 niche 包裹。
  - CLiMi 特异六基因 signature 关联 MRD 状态、DFS 与化疗耐药（跨多个独立队列）。
- README 软件版本（原文）：R 侧 Seurat v5.2.1、BayesSpace v1.10.1、CytoTRACE v0.3.3、
  ggraph v2.2.1、survminer v0.5.0、survival v3.7.0、survcomp v1.54.0、GSVA v1.52.3、NMF v0.27、
  SpatialInferCNV v1.0.1、CNVkit v0.9.12；Python 侧 cell2location v0.1.4、Stardist v0.8.3、
  Cellpose v4.0.4、SMURF v1.0.2。

## 复核与实读补充

- 主分类维持 P8：仓的内容主体是转移场景的多模态疾病分析，方法件（BayesSpace、
  cell2location、SMURF）均为调用而非交付，不另设 P3/P7 主类。
- 复核依据：README 自带逐项软件版本与病理注释元数据，是 18 仓中"元数据随仓"做得
  最规范的两个之一（另一个为 Prostate_TRM 的图版映射表）。
- 后续提炼建议：优先抽 Figure2A 的"CNV→NJ 树"写法与六基因 signature 的
  多队列生存验证链路。
