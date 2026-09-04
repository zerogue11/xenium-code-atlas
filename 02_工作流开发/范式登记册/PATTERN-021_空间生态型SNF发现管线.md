# PATTERN-021 · 空间生态型 SNF 发现管线（网格SN→分类型metacell→多视图融合→Louvain）
- 来源: digitalcytometry/spatialecotyper（LIT-047）相对/路径:行号 — R/SpatialEcoTyper.R:106-187；R/GetSpatialMetacells.R:99-119；R/SNF2.R:96-114
- 场景: 单细胞分辨率空间数据（Xenium/MERSCOPE/CosMx）上发现多细胞生态型（niche），且要求"每个细胞类型在 niche 内的组成状态"可解释；也可用于 Visium 去卷积后的生态型恢复。
- 做法: 把组织按 grid.size≈1.4×radius 网格化为空间邻域（SN）；对每个细胞类型，用 KNN 半径加权把邻近同类细胞聚合成"空间 metacell"（分类型聚合保住细胞类型维度）；对每类 metacell 分别 PCA→构造细胞类型特异相似网络；SNF 融合所有视图成统一图；在融合图上 Louvain 得 SE 标签，再回写单细胞 metadata。
```r
ncmeta$SpotID <- paste0("X", round(ncmeta$X/grid.size), "_Y", round(ncmeta$Y/grid.size))   # 网格化 SN
metacell <- tmpgcm %*% weights   # 每细胞类型: 表达矩阵 × KNN 权重 = 空间metacell
obj = SNF2(snlist, t=iterations, minibatch=minibatch, ncores=ncores)  # 多视图融合
obj %>% RunPCA %>% RunUMAP %>% FindNeighbors %>% FindClusters(resolution=resolution)
obj$SE = paste0("NewSE", as.numeric(as.character(obj$seurat_clusters)) + 1)
metadata = AnnotateCells(metadata, obj)   # SE 回写单细胞
```
- 搬运条件: R/Seurat>=4.2/Matrix/RANN/NMF；入参契约=归一化矩阵+metadata 必含 X/Y/CellType（SpatialEcoTyper.R:102-104 强校验）；Stanford 非商业许可，学术用途需保留声明；Windows 下 mclapply 串行需换并行方案。
- 工程评价: 11/14 分，契约校验与超参编码进产物名（SpatialEcoTyper.R:181-185）是亮点；SNF2 支持 minibatch 内存友好；核心改造（稀疏+缺失容忍的 SNF）有真实算法贡献。
- 迭代记录: 2026-09-04 收录(一期精读批次C)
