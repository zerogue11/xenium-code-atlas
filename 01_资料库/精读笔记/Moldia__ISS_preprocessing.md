# 精读笔记 · Moldia__ISS_preprocessing

- repo: Moldia/ISS_preprocessing
- 来源文献: LIT-017（ISS 空转三件套的前端：显微镜原始图像 → 跨循环配准拼接 → 重切片）
- 锁定SHA: b44f242a8425a78eb48f98642b8cc216ee716bf4（2022-11-08，"updated leica stacking function"）
- 复核分类: 分割/ISS 工具链（S 级）——ISS 前端 ASHLAR 拼接链；仓库混有 dist/、build 产物与 .pyc，实读仅源码

## 代码结构走读

目录 → 模块职责（实读）：
- `ISS_processing/preprocessing.py`（807 行，唯一实质模块）：三显微镜三条通路 + ASHLAR 封装 + 重切片：
  - Zeiss czi 通路：`czi_to_tiff`（L634-786，aicspylibczi 读 czi、MIP 或 Z 栈、写 tile 坐标）+ `stack_cycle_images_zeiss`（L789-799）。
  - Leica tiff 通路：`leica_mipping`（L106-213，Z 栈逐像素最大投影）→ `leica_OME_tiff`（L214-307，从 xlif metadata 解析 tile 坐标、组装 OME-TIFF）→ `preprocessing_main_leica`（L485-540，主入口串 mip→OME→ashlar→retile）。
  - `ashlar_wrapper`（L310-403）：把 ashlar CLI 脚本 `process_single/process_plates` 函数化调用（align_channel/maximum_shift/filter_sigma 等参数对齐 CLI）。
  - `tile_stitched_images`（L418-484）：拼接大图重切为 tile_dim 网格 + 写 tilepos.csv（x,y 供下游 SpaceTx 坐标）。
- `ISS_processing/__init__.py`（10 行）：from preprocessing import 9 个函数。
- `ISS_preprocessing.ipynb`：实际入口，`from ISS_processing.preprocessing import preprocessing_main_leica` → `preprocessing_main_leica(input_dirs, output_location, ...)`。
- `installation.sh`：一键装三件套（preprocessing/decoding/postprocessing 三个 conda env，命名 1_/2_/3_ 前缀）。
- `preprocessing.yml`：conda 全版本锁（ashlar==1.13.1, tifffile==2022.2.9, aicspylibczi==3.0.5 等）。

## 关键脚本清单

| 文件 | 行数 | 一句话 |
|---|---|---|
| ISS_processing/preprocessing.py | 807 | MIP→OME-TIFF→ASHLAR 配准拼接→重切片 全链函数集 |
| ISS_preprocessing.ipynb | notebook | 主入口：调 preprocessing_main_leica 跑通单 region/多 region |
| installation.sh | 40 | 三 conda 环境一键安装（含 ipykernel 注册） |
| preprocessing.yml | ~90 | 版本锁环境（ashlar 1.13.1） |

## 技术路线还原（勾选固定清单，按实际顺序）

1. 数据读取（czi_to_tiff L634 / leica_mipping L106：读 czi/tiff + XML metadata）
2. 配准/3D（ashlar_wrapper L314：跨 sequencing cycle 通道配准 + tile 拼接；z 由 MIP 折叠）
3. 导出（OME-TIFF L278-307、ReslicedTiles/tilepos.csv L479-483，衔接 decoding 仓的 SpaceTx 格式）

未做：质控QC、归一化、HVG、降维、聚类、注释、去卷积、空间邻域/域、细胞通讯、亚细胞、空间统计、多样本整合、绘图。

## 工程审计表（7 维，0-2 分）

| 维度 | 分 | 证据 |
|---|---|---|
| 职责单一/模块化 | 1 | 函数按显微镜/步骤划分尚清楚，但 807 行单文件混三厂商通路+配准+切片 |
| 命名规范 | 1 | 循环变量用瑞典字母 `ö`/`å`/`ååå`（preprocessing.py:135,172,195）；bases/w/q 语义不明 |
| 安全性 | 1 | pixel_size=0.1625 双处硬编码（L88,293）；坐标换算魔数 `/.000000321`（L273-274）；yml 末尾 prefix 写死 `/home/christoffer/anaconda3` |
| 最简化 | 1 | 死代码 `tile_size = tile_size`（L347-349）；`np.sum(np.sum(...))` 类无效语句；注释掉的旧写法成片 |
| 逻辑健壮性 | 0 | `zen_OME_tiff` L86 调 `join()` 但函数内未 import（全文件仅 L118/219 函数内导入 join）——该函数一跑必 NameError；裸 except 吞损坏图像（L203-205）；positions 在 meta 循环中被覆盖只留最后一个（L58-74） |
| 可复现性 | 2 | conda yml 全 == 锁（含 ashlar==1.13.1、scikit-image==0.16.2），installation.sh 固化三环境 |
| 验证纪律 | 0 | 无测试/CI；NameError 级 bug 未被发现说明无冒烟验证；dist/egg/pyc 混入版本库 |

总分：6/14

## 可搬运模式

- PATTERN-016 ASHLAR CLI 函数化封装 + 分段 conda 环境流水线（与 PATTERN-018 同源，卡在 016）

## 坑与限制

- `zen_OME_tiff` 实际不可运行（join 未定义），证明 Zeiss OME 通路从未被回归验证；只有 leica 通路被 notebook 主用。
- 强耦合 Nilsson SOP 文件命名规范（L22 自述 "predicated on ... nilsson SOP"），换命名约定全链重写正则。
- 图像尺寸 2048×2048、通道数 5 双处硬编码（L84,286），非标准采集直接数组越界。
- `stack_cycle_images_leica` L617 的 ImageDescription 写死字符串 `'[zsize, image_dimensions[0], image_dimensions[1]]'` 未做 f-string 插值——写出的 metadata 是假的。
- ashlar 1.13.1 为 2022 年版本，API 与当前 labsyspharm ashlar 已不兼容，搬运须锁环境。

## 一句总评

真实的"显微镜出图→配准拼接→重切片"参考链，ashlar 函数化封装与 tilepos 协议可搬；但 Zeiss 通路是跑不通的死代码，健壮性几乎为零，只能当流程文档读。
