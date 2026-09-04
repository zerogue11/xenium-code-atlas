# `imsb-uke/xenium-cgn`（档案卡）

> 由 agent 依据本地克隆实测撰写；不确定处一律【待补充】；禁止编造星标/日期/功能。

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-022：《肾小球新月体免疫-肾细胞时空互作》Sultana, S. et al. Spatiotemporal interaction of immune and renal cells controls glomerular crescent formation in autoimmune kidney disease. *Nat Immunol* 2025, DOI 10.1038/s41590-025-02291-8 |
| 精选级 | A |
| 主分类 | P8（疾病应用，复核维持） |
| 次要用途 | P3（NichePCA domain 识别、肾小球旁区注释）；P6（Xenium↔Phenocycler 图像配准） |
| 一句话功能 | 肾自身免疫 Xenium 全流程 11 步编号 notebook 管线：细胞分割→样本注释→图像配准→活检标签清洗→细胞类型注释→domain 识别→肾小球旁区标注→PCA 拟时→验证→空间互作→核内 RNA（NucSeq）分析 |
| License | 无LICENSE(仅可学习不可转载) |
| 语言与规模 | Python x56 / Shell x1；45.4MB；notebooks 按 01–10 编号目录组织，每目录自带 README.md（部分含 src/） |
| 运行入口 | notebooks/01–10 各目录内 ipynb 与 main.py；环境 `conda env create -f environment.yml`（全量导出，py311 基座） |
| 复现难度 | 中-高 — 步骤文档与环境 pin 齐全，但 paths.json 硬编码作者服务器路径，图像配准需原始 OME-TIF，中间产物需自建 |
| 与范式的关系 | 候选池（Xenium 疾病全流程范本）：编号步骤目录法、NichePCA 域识别、肾小球编号计数、NucSeq 验证支线均可借鉴 |
| 坑提示 | ① paths.json 需整体重写；② environment.yml 是 conda list 式导出（含 build 串、env 名 base），跨机重建易翻车；③ 原始数据 accession 未给【待补充】；④ readme.md 步骤名与目录名个别不一致 |
| 锁定 SHA | 主表未登记（空）；本地克隆 HEAD `3e2bce3faf9397970f74267854f2485ad442817e` |

## 结构速览

- `notebooks/01_cell_segmentation` … `10_NucSeqAnalysis`：11 个编号目录（含 09a_cell_interactions_spatial），
  覆盖 分割→注释→配准→清洗→celltype→domain→periglom→pseudotime→验证→互作→NucSeq。
- `notebooks/readme.md`：阶段索引（个别步骤名与目录名不一致，如 04 目录为
  cleaning_and_label_biopsies，readme 写 preprocessing；对照时以目录为准）。
- `03_image_registration/`：main.py + seperate_samples.ipynb +
  seperate_samples_phenocycler.ipynb（Xenium 与 Phenocycler 双模态配准）。
- `06_domain_identification/`（实测内容最密的一步）：
  - 01_nichepca_per_sample_step1 / step2（slide2 变体成对）——NichePCA 逐样本两步。
  - 02_merge_clusters_per_sample（+slide2）——跨样本合并 domain。
  - 03_mark_domains_via_gene_enrichment（+slide2）——基因富集标注 domain。
  - 04_clean&number_gloms（+slide2）、count_gloms、Plot_Gloms、Plot_golms_with_number——
    肾小球清洁、编号、计数与可视化；附 src/ 与 README.md。
- 顶层 `paths.json`：样本号 → img/adata 绝对路径映射
  （如 0011284 指向 /data/projects/robin/xenium_cgn/...；combined 指向 merged_with_Disease 系列 h5ad）。
- 顶层 `disease_colors.json`：疾病分组全局配色（符合"cluster 颜色全局一致"范式）。
- `data/`：cleaning_annots、outputs、raw、transcripts_codes、xenium_outs 五个子目录（结构占位为主）。
- `environment.yml`：conda list 式全量导出（含 _libgcc_mutex 级 build 串）。

## 实读补充

- NucSeqAnalysis（10 号）为核内转录本分析支线，在常规 Xenium 管线外，
  适合作为"亚细胞验证"模块参考。
- 配准步骤要求 original_TIF/converted_OME 的 OME-TIF，纯表达矩阵复现者需绕开 03/04 步。
