# PATTERN-008 · 几何 ground truth 的分割评估（质点-多边形空间连接 → TP/FN/FP → 四指标）

- 来源: broadinstitute/ist_benchmarking（LIT-086）seg_eval.py:61-122（calculate_seg_eval_metrics + calculate_tp_fn_fp_from_gdf）；对照 Moldia/Xenium_benchmarking（LIT-088）notebooks/5_segmentation_benchmark/metrics.py:329（rand_idx 等聚类一致性指标）
- 场景: 评估任何细胞分割输出（Xenium/CosMx/MERSCOPE mask、Baysor、Cellpose）相对人工标注 ground truth 的精度时：用"GT 质点是否落入 mask 多边形"这一轻量几何判定替代昂贵的 IoU 矩阵全比对，得到 precision/recall/F1/IoU 四指标。
- 做法: GT 读成点 GeoDataFrame、分割 mask 读成多边形 GeoDataFrame；一次 `gpd.sjoin`（within）同时给出 TP（落点数）、FN（未落点数）、FP（无点的 mask 数）；指标计算全部带除零守卫返回 0。配套函数负责翻转/平移几何对齐不同坐标系的 GT。
  ```python
  tp_gdf = gpd.sjoin(gdf_gt, gdf_mask, how='left', op='within')   # GT 点 → 命中的 mask
  tp = tp_gdf['index_right'].notna().sum()                        # 有 mask 的 GT 点
  fn = tp_gdf['index_right'].isna().sum()                         # 无人认领的 GT 点
  fp = len(gdf_mask) - tp_gdf['index_right'].dropna().unique().shape[0]  # 空 mask
  precision = tp/(tp+fp) if (tp+fp) > 0 else 0                    # recall/F1/IoU 同构带守卫
  iou = tp/(tp+fp+fn) if (tp+fp+fn) > 0 else 0
  ```
- 搬运条件: 依赖 geopandas/shapely（rasterio 仅出图需要）；需改造点——①`op=` 参数新版 geopandas 更名 `predicate=`；②该判定容忍一 mask 多点（仍计 1 TP），若需严格一一对应要加去重逻辑；③GT 与 mask 的坐标系对齐依赖翻转/平移辅助函数，换数据源先跑 dapi_mask_annotation 叠图目检。
- 工程评价: ist 版实现短小、守卫齐全、附可视化函数，是可直接移植的质量；Moldia 对照组用rand index/VI/NMI 等聚类一致性指标从"表达聚类稳定性"角度互补评估分割——两套指标合并才是完整分割基准。
- 迭代记录: 2026-09-04 收录(一期精读批次A)
