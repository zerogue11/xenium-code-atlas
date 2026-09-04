# PATTERN-048 · 微米半径跨平台换算的多尺度邻域层
- 来源: Woopsydaisy/Spatial-Human-Kidney-Map（LIT-048）相对/路径:行号 `D Niche_Analysis/Niche_Analysis_Script1_call_neighbors.py:29,55,100,126,172,198,243,269,314,340`
- 场景: CosMx（像素坐标）与 Xenium（微米坐标）混装图谱：想让"邻域"在物理尺度上可比（20/40/60/80/200 µm 多尺度），必须做单位换算。
- 做法: 对每个平台×每个物理半径调用 squidpy.spatial_neighbors，坐标单位差异在 radius 上折算——CosMx 除以像素物理尺寸 0.12 µm/px，Xenium 直接用 µm；每尺度算完立即出邻居数直方图自检分布是否合理：
  ```python
  if tech == 'CosMx':
      sq.gr.spatial_neighbors(ad, radius=20/0.12, coord_type="generic",
                              key_added="20_micron", spatial_key="spatial_fov")
  if tech == 'Xenium':
      sq.gr.spatial_neighbors(ad, radius=20, coord_type="generic",
                              key_added="20_micron", spatial_key="spatial")
  n_nb = ad.obsp["20_micron_connectivities"].sum(1)  # 直方图自检
  ```
- 搬运条件: 依赖 squidpy≥1.2（obsp connectivities 契约）；无许可障碍。需改造点：①0.12 µm/px 是 AtoMx 导出坐标的换算系数，换平台/换导出版本必须先核实像素物理尺寸，建议从 metadata 读而非写死；②原实现 5 尺度×2 平台写成 10 段复制代码，搬运时抽成 `for r_um in [20,40,60,80,200]` + 平台查表；③逐样本切分算邻域再 concat 回填 obsp 的做法（Script1:21-70）要保留，否则跨样本会串邻居。
- 工程评价: 换算系数一行代码承载了整仓跨平台可比性的关键；实现是展开式重复（该仓 0 分维度），但"多尺度+直方图自检+key_added 命名隔离"的组合值得整段照搬。
- 迭代记录: 2026-09-04 收录(一期精读批次E)
