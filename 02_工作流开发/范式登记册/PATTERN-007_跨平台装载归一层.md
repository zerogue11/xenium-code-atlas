# PATTERN-007 · 跨平台数据装载归一层 + 常量中心

- 来源: broadinstitute/ist_benchmarking（LIT-086）st_utils.py:201-307（data_loader）、:619-628（name_parser）、constants.py:33-70（CORRECT_PLATFORM_PANEL/sample_color）
- 场景: 多平台（Xenium/MERSCOPE/CosMx…）数据进同一基准或 pipeline 时：装载环节吸收全部平台差异（目录结构、文件格式、坐标轴方向、区域拆分、字符解码），让下游所有分析只见统一的 AnnData + 坐标 DataFrame；平台命名/配色等展示属性集中在常量模块全局一致。
- 做法: data_loader 按 modality 三分支：Xenium 读 h5+parquet、MERSCOPE 逐 region 合并 cell_by_gene（cell id 加 region 后缀防重号）、CosMx 走自身格式；每支出口都归一到 `adata`（counts）+ `df`（x/y 坐标、transcript_counts 等 meta）的统一二元组。常量中心用 dict 把机器名（xenium_breast）映射为展示名（Xenium,Breast）并绑定配色。
  ```python
  # st_utils.py:201 data_loader(SAMPLE, modality)
  if modality == 'xenium':
      adata = sc.read_10x_h5(f'{SAMPLE}/cell_feature_matrix.h5')
      df = pd.read_parquet(f'{SAMPLE}/cells.parquet', engine='pyarrow')
      df['x'] = df['y_centroid']; df['y'] = df['x_centroid']   # 坐标轴差异在装载层吸收
      df.set_index(adata.obs_names, inplace=True)
  elif modality == 'merscope':
      ...  # region_* 合并 + f"{x}_{region}" 重编号
  # constants.py 常量中心
  CORRECT_PLATFORM_PANEL = {'cosmx_multitissue': 'CosMx,1k', 'xenium_breast': 'Xenium,Breast', ...}
  sample_color = {'Xenium,Breast': '#0072B2', 'MERSCOPE,Lung': '#F0E442', ...}
  ```
- 搬运条件: 依赖 scanpy/pandas/pyarrow；需改造点——①modality 分支改注册表（dict[modality]→loader 函数），加平台即加一行；②坐标翻转规则（x/y 互换）是平台+版本相关的隐式知识，必须显式注释并参数化；③name_parser 靠 split 下标解析样本名，应改为正则或查表；④2023/2024 格式差异分支（parquet 字符串解码）需保留为显式版本参数。
- 工程评价: "平台差异止步于装载层"的边界划得非常干净，下游 notebook 全程零平台 if——这是五仓中唯一做到的；实现瑕疵集中在 name_parser 脆弱解析与年度硬编码，属局部修补。常量中心（命名+配色+样本清单三合一）与项目 conventions 纪律天然契合。
- 迭代记录: 2026-09-04 收录(一期精读批次A)
