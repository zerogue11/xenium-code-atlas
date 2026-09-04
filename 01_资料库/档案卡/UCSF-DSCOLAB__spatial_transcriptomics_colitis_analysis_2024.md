# `UCSF-DSCOLAB/spatial_transcriptomics_colitis_analysis_2024`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\UCSF-DSCOLAB__spatial_transcriptomics_colitis_analysis_2024`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-053：FFPE 活检结肠炎相关细胞网络。英文原题 "Single-cell spatial transcriptomics of fixed, paraffin-embedded biopsies reveals colitis-associated cell networks"（bioRxiv 2024.11.11.623014，Combes/Kattah 组） |
| 精选级 | S |
| 主分类 | 复核维持 P8（结肠炎=用户 UC 课题近亲，重点参照仓） |
| 次要用途 | P0 边缘：跨平台（Xenium/CosMx/MERSCOPE）统一预处理与 QC 比较方法学 |
| 一句话功能 | 9 个空间数据集（7 Xenium+1 CosMx+1 MERSCOPE，FFPE 活检）的结肠炎分析：为每个主要分析步骤提供"泛化管线" notebook——四套平台预处理、跨平台 CellCharter 联合聚类、邻域富集、空间散点、跨平台 QC 对比（MECR、block age、过滤转录本生成），R 侧 DESeq2+GSEA，外加 HCV→HC/UC pre/post 队列设计【待补充：队列命名以 notebook 实读为准】 |
| License | 无LICENSE(仅可学习不可转载) |
| 语言与规模 | Pythonx14/Rx3/Shellx1；18.2 MB；notebook 为主，3 个 conda yaml |
| 运行入口 | Jupyter/Rmd notebook 分目录组织；conda env：Python_Yaml_Files/{default_env,cellcharter_env,harmony_integration_env}.yaml；数据从 GEO/FigShare 获取（README 称发表后放出） |
| 复现难度 | 中 — 预处理 notebook 从 GEO 原始文件起步（read_10x_h5 + cells.csv）、三个 conda 环境齐备、路径多用 /path 占位可替换；难在数据依赖发表后才完整放出，部分 notebook 依赖上游产出 |
| 与范式的关系 | 用户 UC 课题第一参照仓：① 一次分析跑三个平台并做跨平台一致性 QC/比较；② Xenium 纵向队列（治疗前后）设计；③ CellCharter 跨数据集邻域；候选池 |
| 坑提示 | ① README 声明"所有分析 Python，DESeq2/GSEA 为 R"，R 侧仅 3 件（h5ad→Seurat 转换、DESeq2、GSEA）；② 数据可用性以论文发表状态为准，克隆内不含数据；③ notebook 无预存输出，逐个自跑 |
| 锁定 SHA | ef610b37ed40f37a6549465e33cb95ac706b34d1（主表） |

## 结构速览

- Preprocessing/：Preprocessing_XeniumRep1(.ipynb)、XeniumRep1and2、CosMx、Merscope 四套从原始输出起步的预处理
- Additional_QC/：BlockAge_QCComparison、QCComparisons_CrossPlatforms、MECR_Plots、原始转录本 parquet→csv 的 shell、过滤转录本生成
- More_Downstream_Analyses_And_Visualizations/：CellCharter 联合（275 shared genes）、跨平台对比、邻域富集、空间散点
- DESeq2/ + GSEA/：Rmd+csv（HC/UC pre/post 元数据、基因集）；Python_Yaml_Files/：3 个 conda 环境

## README/代码实读要点

- 抽读 Preprocessing_XeniumRep1.ipynb 头部：markdown 声明"从 GEO 原始文件开始，先建 default_env 环境"；imports 为 numpy/pandas/scanpy/squidpy/anndata
- README 逐点强调"泛化管线可直接用于你自己的数据"，即管线以函数化/参数化方式组织而非一次性脚本
- DESeq2 目录含 first_steps_to_convert_h5ad_to_seurat.ipynb，是 Python→R 交接示范

## 抽读实录

- 读 README 全文；head Preprocessing_XeniumRep1.ipynb（前 80 行 JSON）；ls 全部 6 个子目录。

## 复用建议

- 优先抽三条线进 zoro-spatial 参考池：① Xenium 原始输出的标准预处理 notebook（read_10x_h5→QC）；② 跨平台 QC（MECR 等）指标；③ CellCharter 跨样本联合聚类参数。UC 课题立项后按其目录结构组织本项目分析。
