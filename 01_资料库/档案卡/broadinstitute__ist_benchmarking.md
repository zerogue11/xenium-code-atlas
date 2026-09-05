# `broadinstitute/ist_benchmarking`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\broadinstitute__ist_benchmarking`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-086：《FFPE组织中成像式空间转录组平台的系统基准测试》（Nat Commun 2025） |
| 精选级 | S |
| 主分类 | P0 流程基准与质控（复核确认，与初判一致） |
| 次要用途 | P1 分割评估（08_segmentation_evaluation）、图像叠加/QC 工具函数库 |
| 一句话功能 | Broad 研究所 FFPE 成像空间平台基准论文伴随 notebook 集：00 数据灌入与示例→02 面板间重现性（panel-to-panel）/FDR/特异性敏感性→03 逐基因作图→04 组织 marker 分析→06 单细胞指标→07 不相容 marker 共表达→08 分割评估→09/10 细胞面积与计数→11 蛋白验证→12 基因长度效应，配 st_utils.py、seg_eval.py、constants.py 三个工具模块 |
| License | 无LICENSE(仅可学习不可转载)（主表值） |
| 语言与规模 | Python；py/ipynb 19 个（14 个编号 notebook + 3 个模块 + 杂项）；体积 14.7 MB |
| 运行入口 | 按编号顺序执行的 notebook 流（01/02 两个文件名自带 no_need_to_run 标记）+ requirements.txt |
| 复现难度 | 高 — 分析对象是作者自产的多平台原始数据（需按 00_copy_data.ipynb 灌入自有目录结构），notebook 间强顺序依赖 |
| 与范式的关系 | P0 平台基准范式：面板重现性、FDR、敏感性/特异性、分割评估的整套指标设计可移植为自建 FFPE 多平台对比的检查单；st_utils 的 geopandas/gis 多边形路线可拆用；候选池 |
| 坑提示 | ① 无 LICENSE；② st_utils.py 与 depreciated_st_utils.py 并存，引用认准 st_utils.py；③ notebook 内分析绑定作者的 constants.py 平台/面板定义，换数据需逐项改；④ 仓库混有 .DS_Store（macOS 开发痕迹） |
| 锁定 SHA | `abb4acc39c68b16fdaf6909f1639947a55173182`（主表锁定值；建卡时实测前缀 `abb4acc39c` 一致） |

## 结构速览

- 14 个编号 notebook：00_copy_data、00_setup_and_data_example、01_data_generator（no_need_to_run）、02_FDR_calculation（no_need_to_run）、02×2（panel_to_panel / specificity_sensitivity 重现性）、03_gene_by_gene_plot、04_tissue_marker_analysis、06_single_cell_metrics、07_coexpression_of_disjoint_markers、08_segmentation_evaluation、09_cell_area、10_cell_count、11_protein_validation_light、12_gene_length
- `st_utils.py`：约 25 个工具函数（calculate_qc_metric、get_cell_by_gene、seg_overlay、standardize_data、df_2_gdf、load_shape_file 等），作者 Huan Wang（Broad STP）
- `seg_eval.py`（分割评估）、`constants.py`（全局常量）、`depreciated_st_utils.py`（弃用版）、`requirements.txt`

## README/代码实读要点

- readme.md 仅 1 行："repo for the manuscript 'Systematic benchmarking of imaging spatial transcriptomics platforms in FFPE tissues'"，功能判断主要依据 notebook 命名
- st_utils.py 以 docstring 列函数清单：QC 计算、多边形 gdf 转换、seg_overlay 图像叠加、log2 fold change 等
- "no_need_to_run"命名直接标出哪些 notebook 是一次性数据生成，不必复跑
- 全流程纯 notebook 驱动，无 CLI、无 Snakemaker/nextflow 类编排

## 抽读实录

- 读 readme.md 全文；ls 顶层；读 st_utils.py 开头 30 行（函数清单 docstring 与作者信息）。

## 复用建议

- 把 02 重现性/06 单细胞指标/08 分割评估三步的指标定义抽成自家 FFPE 多平台对比检查单；st_utils.py 可整体拷作工具库；其余 notebook 作指标口径参照。
