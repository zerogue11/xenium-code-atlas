# `maximemeylan/GBM_CAN3110`（档案卡）

> 由 agent 依据本地克隆实测撰写；不确定处一律【待补充】；禁止编造星标/日期/功能。

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-079：《溶瘤病毒GBM》Meylan M. et al. Persistent T cell Activation and Cytotoxicity against Glioblastoma Following Single Oncolytic Virus Treatment in a Clinical Trial, *Cell*（README 标 DOI 10.1016/j.cell.2025.12.055，出版年 2026） |
| 精选级 | A |
| 主分类 | P8（疾病应用，复核维持） |
| 次要用途 | P3（CODEX/Xenium 邻域）；P7（CODEX 成像处理）；TCR/bulk 整合支线 |
| 一句话功能 | 溶瘤病毒 CAN-3110 治疗 GBM 临床试验的空间免疫复现代码：Xenium 聚类注释/邻域/HSV/T 亚群 + CODEX T 细胞-肿瘤空间/邻域/HSV + bulk RNA 与 TCR，每图一 Rmd |
| License | MIT |
| 语言与规模 | R 为主：11 个 figures Rmd + 7 个 preprocessing R/Rmd + utils；3.3MB |
| 运行入口 | scripts/figures/*.Rmd 与 scripts/preprocessing/*.Rmd；每个脚本头部 source("../../config/constants.r")；数据入口 GEO GSE296577（Xenium+Seurat 对象）、BioImages S-BIAD1921（CODEX 图像）、dbGaP phs003378.v2.p1（TCR beta） |
| 复现难度 | 中 — 公开数据度高（dbGaP 需申请）、路径工程化好（constants.r 自动定位 root）；R 包版本未集中声明【待补充】 |
| 与范式的关系 | 候选池（P8 多模态肿瘤免疫 + 工程组织双参考）：constants.r 的路径/常量集中管理可低成本抄；CODEX+Xenium+TCR 三线逐图组织 |
| 坑提示 | ① data/ 目录实际只有 README（数据走 GEO），首次运行靠 constants.r 自动建目录；② 临床数据 DOI 域名与期刊【待补充】核实；③ nthreads 默认 10 按机器调整 |
| 锁定 SHA | 主表未登记（空）；本地克隆 HEAD `0f092d65e13ae6e5be4236aa8e473699712d2607` |

## 结构速览

- `config/constants.r`（实测头部）：
  - 路径自动定位：`if (file.exists("README.md") && dir.exists("scripts"))` 判 repo root，
    否则回退 `file.path(".", "..", "..")`——从根目录或嵌套脚本目录运行均可。
  - data_path/results_path/figpath 统一拼装；`dir.create(figpath, recursive=TRUE)` 自动建输出。
  - 全局常量：nthreads <- 10；codex_pixel_to_um <- 0.325；xenium_pixel_to_um <- 0.2125；配色。
- `scripts/preprocessing/`：Pre_processing_00_GBM_postTx.R、00_Xenium_GBM.R、
  01_GBM_postTx.Rmd、01_Xenium_GBM.Rmd、02_CODEX_GBM_preTX.Rmd、02_Xenium_GBM_Tumor.Rmd、
  03_Xenium_GBM_Tcell.Rmd（Xenium 与 CODEX 两线分列）。
- `scripts/figures/`（每图一 Rmd）：Figure_1_CODEX、Figure_1_XENIUM_clustering_annotations、
  Figure_2_CODEX_spatial_Tcell_tumor、Figure_2_3_Xenium、Figure_4_CODEX_Neighborhoods、
  Figure_4_XENIUM_Neighborhoods、Figure_4_CODEX_HSV、Figure_5_XENIUM_HSV、
  Figure_6_BULK_RNA_TCR、Figure_6_XENIUM_TCR、Figure_7_XENIUM_Tumor_subtype。
- `scripts/utils/maxime_utils.r`：公共函数。
- `data/README.md`（数据说明）+ `docs/assets/graphical_abstract.png`。

## 实读补充

- 数据可得性（README 原文）：CODEX 原始+处理图像 → S-BIAD1921（EBI BioImages）；
  Xenium 输出 + Seurat 对象 → GSE296577；TCR beta → phs003378.v2.p1（dbGaP）；
  临床数据另引 DOI（10.1038/s41586-023-06623-2，README 原文如此）。
- 代码作者 Maxime Meylan（DFCI）/ 通讯 Kai Wucherpfennig；MIT License 明确可复用。
