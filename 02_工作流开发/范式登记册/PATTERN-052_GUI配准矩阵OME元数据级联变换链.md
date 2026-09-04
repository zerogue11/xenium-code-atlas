# PATTERN-052 · GUI 配准矩阵+OME 元数据级联变换链
- 来源: 10XGenomics/janesick_nature_comms_2023_companion（LIT-002）相对/路径:行号 `companion_notebook.ipynb` cell14-15（矩阵来源声明+硬编码+级联）+ `companion_functions.py:198-220`（get_xenium_to_morphology_transform_from_xenium_morphology_image）、`:246-254`（transform_coordinates，cv2.perspectiveTransform）
- 场景: Xenium 与另一平台（Visium/H&E/IF）serial section 对齐：官方链路是"Xenium Explorer 人工关键点配准导出矩阵 + 代码级联"，任何 Xenium↔Visium/H&E 共定位分析的地基，也是本库配准支线的首选参考件。
- 做法: 三段级联齐次变换：①Xenium 坐标(µm)→Xenium DAPI 图像像素：从 OME-TIFF 元数据读 physical_size 构造缩放矩阵（含金字塔层级 /2**level）；②图像像素→目标平台全分辨率像素：Xenium Explorer 人工配准导出的 3×3 矩阵（数值硬编码进 notebook）；③两矩阵相乘得端到端变换，任意点集/多边形经 perspectiveTransform 映射：
  ```python
  xenium_to_morph = np.array([[1/px_size_x/2**lvl, 0, 0],
                              [0, 1/px_size_y/2**lvl, 0], [0, 0, 1]])  # OME 元数据
  xenium_to_visium = explorer_matrix @ xenium_to_morph                # 级联
  coords_v = perspectiveTransform(coords.reshape(-1,1,2).astype(np.float32),
                                  xenium_to_visium)[:, 0, :]
  ```
- 搬运条件: 依赖 tifffile(OMEXML)、opencv perspectiveTransform；仓为 BSD-2 类（LICENSE 在仓）。需改造点：①Explorer 人工配准是不可替代的手工环节，换样本必须重配并更新矩阵——矩阵旁应注明"样本 ID+配准日期+操作人"；②金字塔层级与目标平台 scalefactors（tissue_hires_scalef）链路别算两遍；③float32 精度对亚像素级配准足够，但对跨 1e4 像素的平移建议复核残差（可视化校验图照抄 cell17-30 系列）。
- 工程评价: 变换来源、级联次序、金字塔换算三个易错点全有显式注释，是官方件的示范价值所在；硬编码矩阵属"数据集专属数值"合理硬编码，但缺"换数据须重配"的醒目警示。
- 迭代记录: 2026-09-04 收录(一期精读批次E)
