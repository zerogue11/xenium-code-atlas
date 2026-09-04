# PATTERN-053 · 凸包缓冲区过滤+KDTree 最近邻 spot 插值
- 来源: 10XGenomics/janesick_nature_comms_2023_companion（LIT-002）相对/路径:行号 `companion_functions.py:291-307`（get_visium_capture_polygon，ConvexHull+LinearRing.buffer(spot_diameter)）、`:313-339`（bin_xenium_data_to_visium_spots，KDTree k=1+外部标签过滤）、`:342-361`（generate_anndata_matrix_from_transcript_assignments，Counter→csc_matrix）
- 场景: 配准完成后，把单细胞/单转录本分辨率的 Xenium 数据"插值"到 Visium spot 网格：赋值最近 spot、剔除落在 Visium 捕获区外的点、零循环重建"spot×基因(或 spot×细胞类型)"计数矩阵。跨分辨率数据整合的最小可靠实现。
- 做法: 捕获区=所有 spot 质心的凸包再外扩一个 spot 直径；变换后的 Xenium 点用 KDTree 最近邻分给 spot 条码；凸包外点统一打哨兵标签；最后 (barcode,feature) 计数器直接拼稀疏矩阵：
  ```python
  kdtree = KDTree(visium_spot_centroids)
  _, nb = kdtree.query(transform_coordinates(xenium_coords, T), k=1)
  barcodes = visium_barcodes[nb]
  barcodes[~points_in_poly(coords, capture_polygon)] = "Outside_Visium_Capture_Area"
  # (barcode, gene) -> CSC
  pairs, data = np.array(list(Counter(zip(bc_codes, ft_codes)).keys())).T, ...
  adata = sc.AnnData(X=csc_matrix((data, pairs)), obs=..., var=...)
  ```
- 搬运条件: 依赖 scipy KDTree/ConvexHull、shapely buffer、opencv；无许可障碍。需改造点：①"最近邻=插值"是隐含假设——spot 半径 55µm 外的 Xenium 点也被强行归给某 spot，建议保留距离向量并设最大距离阈值；②哨兵标签是字符串常量（functions:310），改成显式 NA 更安全；③Counter 法在 1e5 点级无压力，更大规模换 np.unique+bincount。
- 工程评价: 三个函数合计 ~60 行、注释含维基/KB 链接、边界（捕获区外）处理显式——是官方件里最值得原样搬走的一段；六边形 space-filling 多边形函数（:272-288）自注"仅展示勿用于分析"，勿挪作分割用。
- 迭代记录: 2026-09-04 收录(一期精读批次E)
