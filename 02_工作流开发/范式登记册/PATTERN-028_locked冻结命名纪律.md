# PATTERN-028 · locked 冻结命名纪律（lockedYYYYMMDD 后缀 + figure 级 notebook 对应）
- 来源: dpeerlab/p53-niche-dynamics（LIT-078）相对/路径:行号 — transcriptomics/notebooks/ 目录（如 Xenium_Preprocessing_step03_compute_neighborhoods_simplified_locked20260410.ipynb、KPLOH_GenerateFigure_Fig1_FigS1_DataS1_1_locked20260128.ipynb）
- 场景: 论文复现仓里 notebook 反复修改导致"哪版出了图"无法追溯；需要与 zoro 的 freeze 纪律（"以 X 为准"→登记定版）等价的文件系统级实现。
- 做法: 文件名三段式：`{数据集}_{阶段}_{内容}_{lockedYYYYMMDD}.ipynb`——阶段（Preprocessing/Precompute/GenerateFigure）+ 图号（FigN_FigSN）+ 冻结日期；迭代出新版不覆盖旧文件而是新日期另存（同目录并存 step02/step03 多个 locked 日期）；配 per-figure 目录（imaging_progenitor_niche_Fig3_FigS2/）把 notebook 与论文图一一对应；批量步骤配 SBATCH 脚本。
```
Xenium_Preprocessing_step00_raw_tenx_to_adata_locked20260318.ipynb
Xenium_Preprocessing_step01_embed_tiered_samples_locked20260318.ipynb
Xenium_Preprocessing_step02_annotate_cell_types_locked20260318.ipynb
Xenium_Preprocessing_step03_compute_neighborhoods_simplified_locked20260410.ipynb
KPLOH_GenerateFigure_FigS1_TumorDP_locked20260205.ipynb
```
- 搬运条件: 零依赖、纯命名约定；适合 notebook 群仓；与 zoro"新结果包不可覆盖，旧版归档 _历史版本/"同构，但以文件名后缀替代目录分层——小仓库更轻。
- 工程评价: 仅靠命名就解决了"改版不覆盖+图号可追溯"两个痛点，成本最低的 freeze 实现；局限：无哈希/校验（真防篡改仍需 git tag 配合）、文件名变长。
- 迭代记录: 2026-09-04 收录(一期精读批次C)
