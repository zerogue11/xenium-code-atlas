# `ktakehara/Prostate_TRM`（档案卡）

> 由 agent 依据本地克隆实测撰写；不确定处一律【待补充】；禁止编造星标/日期/功能。

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-061：《前列腺组织驻留记忆T细胞》——README 自述手稿进行中："Distinct tissue niches contribute to prostate TRM cell differentiation and heterogeneity"（期刊/DOI【待补充】） |
| 精选级 | A |
| 主分类 | P8（疾病应用，复核维持） |
| 次要用途 | P1（Baysor 分割后处理与评估）；P3（Squidpy 邻域、空间区域标记）；P4（GLM 细胞因子-邻域关联） |
| 一句话功能 | 小鼠前列腺 TRM 空转研究全流程：外部 nextflow 分割（Baysor）→ 11 步预处理 notebook（评估/过滤/整合/细胞分型）→ 图版级复现 notebook（Squidpy 邻域、细胞因子、T 细胞动态）+ 2 个 Quarto GLM 分析 |
| License | 无LICENSE(仅可学习不可转载) |
| 语言与规模 | Python x27 / R x2（另含 2 个 .qmd）；25.6MB |
| 运行入口 | preprocessing/01–11 ipynb 顺序执行；figures/01–09 ipynb + 10/11 GLM qmd（需 Quarto）；分割走外部 maximilian-heeg/xenium-segmentation v0.1.2 |
| 复现难度 | 中 — README 推荐直接从 GEO（GSE296275）下载处理对象起步；图版→脚本映射表完整、Python/R 依赖清单已列 |
| 与范式的关系 | 候选池（本批组织最好的仓之一）：逐图版映射表 + 外部管线版本/参数登记 + "处理对象起步"策略，三件事都可复制 |
| 坑提示 | ① models/prostate_nuclei/ 为空目录【待补充】；② GLM 用 .qmd 需 Quarto；③ 手稿进行中结构可能变动；④ 无 LICENSE |
| 锁定 SHA | 主表未登记（空）；本地克隆 HEAD `2b5c7221d887c3233a1f6a3c24956c81af9c97b6` |

## 结构速览

- `preprocessing/`：11 步 notebook 顺序管线。
  - 01_Postprocessing_Baysor_Segmentation → 02_Evaluating_Baysor_Segmentation。
  - 03_Processing_and_Filtering → 04_Calculating_Initial_Neighborhoods → 05_Remove_Bad_Tissue。
  - 06_Integration → 07_Marking_spatial_regions → 08_celltype_refinement。
  - 09_Cross_correlation_vs_differential_expression → 10_Re-integrate_after_filtering
    → 11_Celltyping_and_metadata。
- `core_functions/`（Python 模块，与 notebook 配套）：
  baysor_postprocessing.py、segmentation_evaluation.py、processing_and_filtering.py、
  initial_neighborhoods.py、neighborhood_decomposition.py、unrolling.py、iexplorer.py。
- `figures/`：01_T_cell_gene_removal、02_T_cell_D7、03_T_cell_D30、04_Frequencies_celltypes、
  05_Cytokines_D30、06_Spatial_Neighborhood_Squidpy、07_TGBF_proximity_scores、
  08_Spatial_intro_figure、09_Spatial_transcripts（ipynb）+ 10_GLM_Tcells.qmd、11_GLM_Cytokines.qmd。
- `models/prostate_nuclei/`：空目录。
- README：摘要（LCMV Armstrong 感染模型 + 人前列腺样本；TGFβ/IL-7/IL-15 niche 依赖；
  IL-15、TGFβ 在上皮富集）+ 外部分割参数 + 逐图版映射表（6B→09、6G→11 等 11 行）+ 联系人
  （Allen Institute/Goldrath 实验室）。

## 实读补充

- 外部分割参数（README 原文）：tile.minimal_transcripts = 300000；
  baysor.prior_segmentation_confidence = 0.95；管线版本 xenium-segmentation v0.1.2。
- 复现策略：README 明示"We recommend using our processed object on GEO as a starting point
  for the figure scripts"——先对象后图脚本，注释一致性有保障。
