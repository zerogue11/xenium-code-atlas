# `ding-lab/ST_subclone_publication`（档案卡）

> 由 agent 依据本地克隆实测撰写；不确定处一律【待补充】；禁止编造星标/日期/功能。

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-019：《肿瘤2D/3D进化》Mo, CK., Liu, J., Chen, S. et al. Tumour evolution and microenvironment interactions in 2D and 3D space. *Nature* 634, 1178–1186 (2024), DOI 10.1038/s41586-024-08087-4 |
| 精选级 | A |
| 主分类 | P8（疾病应用，复核维持） |
| 次要用途 | P6（Figure5 用 PASTE2 做 3D 重建）；上游比对 shell（cellranger/spaceranger 版本登记） |
| 一句话功能 | 按论文 Figure1–6 组织的空间克隆进化全套复现脚本：Visium 上 inferCNV/CalicoST 克隆演化、WES 突变映射、RCTD 去卷积、边界 DEG、COMMOT/边界 CCI、PASTE2 3D |
| License | 无LICENSE(仅可学习不可转载) |
| 语言与规模 | Shell x11 / Python x2（主表口径；另有多个 .R 脚本未计）；1.5MB |
| 运行入口 | 各 Figure 目录内 R 脚本与 shell；CalicoST 步骤是 md 说明需手动执行；无 env 文件、无 renv |
| 复现难度 | 高 — 数据须经 GDC（CPTAC snRNA-seq，按 Case ID）与 HTAN DCC（WUSTL Atlas）门户下载，仓内提供样本→库对应表 |
| 与范式的关系 | P8 肿瘤进化场景候选池：图版→脚本 README 映射模式 + 完整克隆演化路线，可映射到整合 pipeline 的克隆演化支线 |
| 坑提示 | ① 无 LICENSE；② R 包版本未声明【待补充】；③ Figure6 只有 README（复用 Figure5 产物）；④ gencode 注释文件需按 README 命令自行生成 |
| 锁定 SHA | 主表未登记（空）；本地克隆 HEAD `7067cd16f06ec4aa2500aa1e5c9a6eb1e6e42cfa` |

## 结构速览

- `Figure1/`：0_Load_All_Sample、1_Calculate_metrics——空间微区域（microregion）划分与指标计算。
- `Figure2/`（Focal clonal evolution）：
  - 1_inferCNV_run.R：Visium 上跑 inferCNV（Fig 2a–g）。
  - 2_CalicoST_run.md：CalicoST 运行说明（非脚本，手动执行）。
  - 3_CNV_jaccard_similarity.R：两个 CNV 谱 Jaccard 相似度。
  - 4_WES_CNV.sh：WES 数据推 CNV；5_genomic_heatmap.R：空间 CNV 基因组热图（2c–g）。
  - 6_mutation_mapping.sh：WES 体细胞突变映射回 Visium（2f）。
  - README 逐脚本→图版映射，附 gencode_v32_gene_name.txt 生成命令
    （broadinstitute/infercnv 的 gtf_to_position_file.py，GRCh38-2020-A 注释）。
- `Figure3/`：0_Load_All_Sample、1_Heterogenity_score、2_Correlation、3_Pathway、4_Layer——
  遗传差异驱动的肿瘤异质性与 core/edge 通路分层。
- `Figure4/`（克隆特异性 TME 互作）：1_RCTD_devolution.R、2_differential_celltype_fraction.R、
  3_celltype_layer.R、4_border_DEG.R、5_CCI_COMMOT.py、6_CCI_border.R。
- `Figure5/`（3D 结构）：0_data、0_palette、1_run_PASTE2、2_PASTE2_analysis。
- `Figure6/`：仅 README（3D TME 互作，复用 Figure5 产物）。
- `Processing_script/`：cellranger-arc v2.0.0、cellranger v5.0.1/v6.0.2、spaceranger v1.3/v2.1.1。
- `Data_access/`：Sample_ID_Lookup_table_v1.xlsx + CPTAC（GDC portal）/HTAN（WUSTL Atlas）取数说明。

## 实读补充

- README 映射模式的范例：Figure2 README 每条"脚本 + 关联图版 + 关键参数来源"三要素齐全。
- 数据侧只给 ID 与门户链接，无一键下载脚本——复现的第一道门槛是批量取数。
