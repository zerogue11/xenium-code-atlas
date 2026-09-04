# `navinlabcode/tnbc-chemo`（档案卡）

> 由 agent 依据本地克隆实测撰写；不确定处一律【待补充】；禁止编造星标/日期/功能。

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-046：《三阴性乳腺癌化疗空间生态型》（期刊/DOI【待补充】，README 未给；Navin 实验室出品） |
| 精选级 | A |
| 主分类 | P8（疾病应用，复核维持） |
| 次要用途 | P3（xenium.spatial_niche、ecotype）；P7（visium_hd、visium_cna）；P2（ML_13g/scML 13 基因分类器、archetype_prediction） |
| 一句话功能 | TNBC 化疗队列多模态空间生态型研究代码：约 20 份"分析操作手册（.md）+ 对应脚本"双轨组织，覆盖非整倍体识别、cancer archetype、fastNMF 元程序、ecotype、CellChat、Xenium niche、VisiumHD 与临床生存关联 |
| License | 无LICENSE(仅可学习不可转载) |
| 语言与规模 | 主表记 Python x1；实为 R 为主（analysis/scripts 下数十个 .R）+ 1 个 Snakemake wrapper；379MB（other/ 约 343MB） |
| 运行入口 | analysis/README.md 汇总"分析→图版"映射表，逐条链到 analysis/<主题>.md 手册；脚本在 analysis/scripts/ 主题子目录；fastNMF 链有 metamodule.fnmf.wrapper.snk.py |
| 复现难度 | 中-高 — 外部验证队列对象已随仓内置，省去跨库下载；自身队列数据与包版本说明【待补充】 |
| 与范式的关系 | **候选池，建议升 S**：md 手册+图版映射+主题化脚本目录，与"参考图+路径两步出图"工作流高度契合；fastNMF→临床关联管线完整 |
| 坑提示 | ① 379MB 几乎全在 other/（外部队列对象），data/ 仅 4KB——勿误删；② 无 LICENSE；③ 需按 md 手册找对应脚本 |
| 锁定 SHA | 主表未登记（空）；本地克隆 HEAD `fbe1dd3b1db05dd5e9f02485a45fdd438d6af9fb` |

## 结构速览

- `analysis/`（手册层，实测 README 映射表）：
  - Identifying aneuploid cells → Fig.1 / ED Fig.1（identifying_aneuploid_cells.md）。
  - Cancer-intrinsic archetypes → Fig.2 / ED Fig.2：archetype.md（scRNA 定 archetype）、
    visium_cna.md（Visium 高纯度 spots）、visium_hd.md（Visium HD 细胞识别）、
    archetype_and_response.md、archetype_and_OS.md、archetype_prediction.md（外部队列预测）。
  - Gene expression metaprograms → Fig.3：cancer_cell_metaprogram.md（含锚点小节）、
    cell_cycle_scoring.md（Fig.3i）。
  - 另有：ML_13g.md、ML_cell.md、TME.md、TME_freq_test.md、cellchat_ligand_receptor.md、
    ecotype.md、xenium.celltype.md、xenium.cellstate.md、xenium.spatial_niche.md。
- `analysis/scripts/`（脚本层）：
  - fastNMF 元程序链：fastnmf.R、metamodule_fnmf.s1.R / s2a / s2c / s2e.alt / s3、
    metamodule.fnmf.wrapper.snk.py（Snakemake 串联）、metamodule_cell_frequency.R、
    psbulk.fastNMF.R、psbulk.prepare.R、util.nmf.viz.R。
  - 主题目录：ML13g/、archetype/、cellchat/、ecotype/、scML/、sc_pp/、spatial_niche/、
    visiumHD/、visium_st/、xenium/。
  - 散件：KM_METABRIC_ALT.R（生存）、copykat_mix.R、default_seurat_pipe.R、
    integrate_seurat.R、cell_cycle_phase_comparison.R、std.AddModuleScore.R、
    pkg_enricher.R、util.ruok.R。
- `other/`（343MB，实测）：BrighTNess/、DiffusionMap/、ISPY990/、METABRIC/、SCANB/、SCTD/、
  TNBC_Burstein2015/、TME_gene_signatures/、hbca_ref.sr3.rds、tnbc_primary_tumor.se.rds、
  tnbc_solid_normal.se.rds、normal_breast_epithelial_lineage.gmx.csv + other/README.md。
- `supp/`（含 README）与 `website_images/`。

## 实读补充

- `data/` 实测仅 4KB——论文自身队列数据不在仓内【待补充】（README 未给 accession）。
- "md 手册 + 脚本双轨"的写法：每份 md 含步骤说明与图版关联，适合直接改造成
  本项目"参考图+路径"式的出图任务书。
