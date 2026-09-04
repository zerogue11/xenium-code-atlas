# `10XGenomics/janesick_nature_comms_2023_companion`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\10XGenomics__janesick_nature_comms_2023_companion`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-002：肿瘤微环境高分辨率图谱（10x 官方伴随）。英文原题 "High resolution mapping of the breast cancer tumor microenvironment using integrated single cell, spatial and in situ analysis of FFPE tissue"（Janesick et al., Nat Commun 2023；biorxiv 2022.10.06.510405；数据 GSE243275） |
| 精选级 | S |
| 主分类 | 复核维持 P8（疾病应用类；伴随代码为单 notebook 教学/复现件） |
| 次要用途 | P2 边缘：Xenium↔Visium 配准与 spot 插值方法学演示（配准/坐标变换支线参考件） |
| 一句话功能 | 单 notebook（+companion_functions.py）演示同一 FFPE 乳腺癌连续切片上 Xenium 与 Visium 的配准：用 Xenium Explorer 导出的变换矩阵把 Xenium 细胞/转录本 bin 到 Visium spot 网格（spot interpolation），并与实测 Visium 计数做相关性对比、做 Visium spot 的细胞型比例推断，复现论文配准相关图版 |
| License | MIT |
| 语言与规模 | Pythonx2（companion_notebook.ipynb + companion_functions.py）；8.2 MB（figures 目录截图占大头） |
| 运行入口 | Jupyter notebook；environment.yml（conda env：xenium-publication-env）；依赖 scanpy/skimage/tifffile/pandas |
| 复现难度 | 中 — README 内嵌完整 Quick Start（conda env、数据 curl 下载到 $HOME/xenium-publication 固定布局、cell_groups.csv 从 xlsx 手工导出），但配准矩阵来自 Xenium Explorer 交互式手工操作并硬编码在 notebook 中 |
| 与范式的关系 | Xenium→Visium 坐标配准 + 转录本/细胞 bin 到 spot 的官方参考实现，qv>=20 过滤、capture area 求交等细节可直接抄；与用户"配准/HE→表达预测"支线直接相关，候选池 |
| 坑提示 | ① 变换矩阵硬编码于 notebook，换数据必须重做 Xenium Explorer 配准；② 数据路径假定 $HOME/xenium-publication/{xenium,visium}/；③ README 即 notebook 渲染（含输出），真正的 .ipynb 是执行入口；④ 作者自注多边形 groupby 绘图很慢需缓存 |
| 锁定 SHA | 60828a5a112254336f138bc759caa547b9e80654（主表） |

## 结构速览

- companion_notebook.ipynb：主分析入口（坐标系讲解→配准→spot 插值→相关性→细胞型推断）
- companion_functions.py：配准/变换/binning/多边形绘制的函数库
- environment.yml：conda 环境定义
- figures/：README 与论文图（nuclei_figure.png 等）；数据本体不在仓内（10x 官网/GEO）

## README/代码实读要点

- Synopsis 明确四步：坐标系统图示→keypoint 配准（Xenium DAPI vs Visium H&E）→Xenium 数据 spot 插值→Visium spot MLE 细胞型推断
- bin_xenium_data_to_visium_spots / generate_anndata_matrix_from_transcript_assignments 是核心函数；__OUTSIDE_VISIUM_CAPTURE_AREA_BARCODE__ 处理 capture area 不重叠
- 细胞型标签来自匹配 FLEX 数据的 label transfer（Cell_Barcode_Type_Matrices.xlsx 手工另存 CSV）

## 抽读实录

- 读 README 全文（含 notebook 渲染内容与全部关键代码 cell）；未深读 companion_functions.py（README 已列全函数清单）。

## 复用建议

- 学"Xenium Explorer 手工配准导出矩阵 → 矩阵链乘（xenium→morphology→visium）→ spot binning"这条最小可行路径；10x 官方数据可完整复跑，适合做配准支线的练手与基准件。
