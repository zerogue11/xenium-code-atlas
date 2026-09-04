# PATTERN-001 · QC 指标库单指标单函数化

- 来源: Moldia/Xenium_benchmarking（LIT-088）xb/_quality_metrics.py:8-203；对照 Center-for-Spatial-OMICs/SpatialQM（LIT-028）R/utils.R:672-2568
- 场景: 为整合 pipeline 建"质控模块"时：需要一套可对任意样本独立计算、可增可减、可单测的标准化 QC 指标集合（细胞密度、assigned reads 比例、中位 reads/基因数每细胞及其分位数等），而不是把 QC 埋进预处理主流程。
- 做法: 每个指标一个纯函数，统一签名——AnnData 进、标量出，附带 `pipeline_output` 开关决定返回值形态（供 notebook 展示或供上层聚合）。指标函数之间零耦合，上游一个编排器按需调用。SpatialQM 是 R 侧对照实现（getNcells/getTxPerArea/getEntropy…），同构但粒度更粗（函数内部自带读文件）。
  ```python
  def median_reads_cells(adata_sp: AnnData, pipeline_output=True):
      """Median number of reads/cells"""
      median_cells = np.median(np.sum(adata_sp.layers['raw'], axis=1))
      return median_cells          # xb/_quality_metrics.py:42-56 同构
  def cell_density(adata_sp: AnnData, pipeline_output=True):
      hull = ConvexHull(np.array(adata_sp.uns['spots'].loc[:, ['x','y']]))
      density = (adata_sp.shape[0] / hull.area)
      return density               # xb/_quality_metrics.py:8-23
  ```
- 搬运条件: 依赖 anndata/numpy/scipy（R 版依赖 Seurat）；需改造点——①约定指标必须落 `adata.uns['qc_metrics']` 或统一 DataFrame，Moldia 原实现仅 return 不落盘；②`pipeline_output` 参数在原码中半数未真正分支，搬运时应做成真开关；③raw 层约定（counts 存 `adata.layers['raw']`）须与装载层对齐。
- 工程评价: Moldia 版签名统一、docstring 齐全是五仓里最接近"库"的 QC 实现，但无聚合器、无落盘；SpatialQM 版覆盖指标更多（FDR/MECR/熵/复杂度/Moran）却与编排层纠缠且双版本打架。搬运建议：Moldia 骨架 + SpatialQM 的指标清单。
- 迭代记录: 2026-09-04 收录(一期精读批次A)
