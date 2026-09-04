# 精读笔记 · 10XGenomics__janesick_nature_comms_2023_companion

- repo: 10XGenomics/janesick_nature_comms_2023_companion（LIT-002）
- 来源文献: Janesick et al. 2023 Nat Commun — FFPE 乳腺癌 Xenium↔Visium↔scRNA 整合（Xenium 旗舰数据集配套代码）
- 锁定SHA: 60828a5a112254336f138bc759caa547b9e80654（2023-11-30，"fix data download and conda environment"）
- 复核分类: 应用范式组 · S 级 · 单 notebook 配准支线（官方件，配准链路首选参考）
- 精读日期: 2026-09-04（一期精读批次E）

## 代码结构走读

- 实际读取: README 全文、companion_notebook.ipynb 42 cells（重点 cell 9-40）、companion_functions.py 全文、environment.yml。
- 极简三件套：`companion_notebook.ipynb`（42 cells 单一叙事入口）+ `companion_functions.py`（361 行 17 个函数的全部可复用逻辑）+ `environment.yml`（86 行全 pin）。figures/ 存论文图。
- 叙事结构：环境与数据下载（bash cell 可直接执行）→ 双平台坐标系讲解图（Visium 六边形网格、scalefactors、Xenium 金字塔层级）→ 配准 → 配准应用四连（分割/分型叠加、spot 插值、转录本相关、spot 级细胞类型推断）。
- 配准链路（本仓核心价值，官方手工环节全景）：
  1. **人工环节**：把 Visium 全分辨率 H&E 载入 Xenium Explorer 图像配准工作流，人工选关键点，导出 3×3 仿射/单应矩阵（cell14 markdown 明说该流程）；
  2. **矩阵硬编码**：`xenium_morphology_to_visium_full_res_transformation` 数值直接抄进 cell15（注释自证 "directly copied into the cell below for convenience"）；
  3. **级联**：Xenium 坐标≠图像坐标——从 OME-TIFF 元数据读 physical_size 换算（companion_functions.py:198-220，含 `/2**pyramid_level` 金字塔层级），两级矩阵相乘得 `xenium_to_visium_full_res_transformation`（cell15）；
  4. **应用**：`transform_coordinates`（:246-254，cv2.perspectiveTransform 齐次变换）作用于细胞质心/核多边形/捕获区多边形/Visium spot 全部对象。

## 关键脚本清单

| 文件 | 一句话 | 行数 |
|---|---|---|
| companion_functions.py | 全部几何与插值逻辑 17 函数：变换矩阵构建、齐次变换、凸包捕获区、KDTree 最近邻 spot 分配、Counter 法重建 CSC 矩阵 | 361 |
| companion_notebook.ipynb cell15 | 硬编码 Explorer 导出矩阵 × OME 元数据矩阵 = 级联变换 | ~20 |
| companion_functions.py:313 bin_xenium_data_to_visium_spots | spot 插值核心：变换后 KDTree 最近邻 spot 条码分配 + 凸包缓冲区外打 `Outside_Visium_Capture_Area` 标签 | 27 |
| companion_functions.py:342 generate_anndata_matrix_from_transcript_assignments | (barcode,gene) Counter→csc_matrix→AnnData，零循环重建计数矩阵 | 19 |
| companion_functions.py:257-288 | KDTree 中位 spot 间距→space-filling 六边形（自注"仅展示勿用于分析"） | 31 |
| environment.yml | python 3.10.13 + anndata==0.10.2 等全 pin | 86 |
| README.md + notebook cell2-4 | conda 环境 + curl 下载官方数据 bundle 的可执行复现脚本 | — |

## 技术路线还原（按 notebook 叙事序）

[数据读取(Visium h5+tissue_positions+scalefactors、Xenium parquet+cells+核多边形), 注释(直接读 Cell_Barcode_Type_Matrices.xlsx 导出的 cell_groups.csv 监督标签), 配准/3D(Explorer 人工配准矩阵+OME 元数据矩阵级联+齐次变换), 空间统计(Xenium-Visium 同基因表达相关), 绘图(坐标系讲解+叠加+六边形), 导出(spot-binned 细胞类型 AnnData)] —— 共 6 步。质控QC/归一化/聚类/整合均不做（消费现成标注），是"配准专项"而非全管线。

## 工程审计表（7 维 0-2 分，总分 10/14）

| 维度 | 分 | 证据 |
|---|---|---|
| ①职责单一/模块化 | 2 | notebook 只做叙事与调用，全部几何逻辑下沉 companion_functions.py 独立函数，函数间零耦合 |
| ②命名规范 | 1 | 函数名长而达意；但拼写错误成串：`nucleous`（notebook cell34/38）、`hexegon`（functions:272,285）、`Usefull`（functions:261） |
| ③安全性(硬编码) | 1 | 数据路径走 $HOME 相对约定（README 下载脚本）；cell15 变换矩阵属"数据集专属数值必须写死"，但未加"换数据须重配"警示注释（有说明来源，算半合格） |
| ④最简化 | 2 | 42 cells 无冗余；仅 cell9 import 列表重复 `celltypes` 一次，可忽略 |
| ⑤逻辑健壮性 | 1 | 无 assert；unique_encode 自述绕过 np.unique 换性能（:184-189）；float32 截断（:253）未讨论；捕获区外标签机制是隐性契约 |
| ⑥可复现性 | 2 | environment.yml 全 pin；官方 curl 数据源+GEO 双通道；变换矩阵数值公开正是可复现关键；pyramid_level 显式参数化 |
| ⑦验证纪律 | 1 | 无测试/CI；但 cell17-30 系列构成"每步变换都有可视化校验图"的验证叙事（质心落 DAPI、落 H&E、捕获区叠加三重目检） |

## 可搬运模式

- PATTERN-052 · GUI 配准矩阵+OME 元数据级联变换链（cell15 + functions:198-254）
- PATTERN-053 · 凸包缓冲区过滤+KDTree 最近邻 spot 插值（functions:291-361）

## 坑与限制

- 配准矩阵是**本数据集专属硬编码**：换成任何新 Xenium/Visium 切片都要重走 Xenium Explorer 人工配准并更新矩阵——这条手工环节无代码可替代，是我们移植时最大的隐性工作量。
- "MLE celltype inference" 只出现在概要 markdown；cell40 实际实现是 spot 内细胞类型计数除以细胞数（经验比例），无显式似然计算——引用该结论时勿照抄 "MLE" 说法。
- 六边形 spot 多边形函数自注明"仅展示勿用于分析"（functions:279），二次利用时要守约。
- serial sections（连续切片）而非同张组织：配准解决的是"近似对齐"，跨切片生物学差异仍在。

## 一句总评

官方配准参考件名副其实：变换矩阵从哪来（Explorer 人工配准）、怎么级联（OME 元数据×导出矩阵）、怎么用（齐次变换+最近邻插值）三个关键问题全部有可抄的代码答案，唯一无法搬走的是 Explorer 里那一下人工点击。
