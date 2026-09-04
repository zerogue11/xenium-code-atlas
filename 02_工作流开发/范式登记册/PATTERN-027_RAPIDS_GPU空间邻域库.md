# PATTERN-027 · RAPIDS GPU 空间邻域库（cupy/cuml KNN → 二值 csr 邻接契约）
- 来源: dpeerlab/p53-niche-dynamics（LIT-078）相对/路径:行号 — utils/neighborhood_utils.py:4-7,86-91,113-147
- 场景: 数十万至上百万细胞的单细胞空间数据上反复算空间 KNN 邻域（niche 分析、邻域表达聚合、Milo 前置图），CPU 内存/耗时撑不住时。
- 做法: 空间坐标上 cupy 数组 + cuml NearestNeighbors GPU 求解 KNN；按 slide_key 分块（防跨切片连边），把 (source,target) 对汇成 n_obs×n_obs 的**二值 uint8 csr 邻接矩阵**——这一个 csr 就是后续一切邻域聚合（均值/总数/布尔占比）的统一入参；聚合端用"对角归一化矩阵 @ 邻接 @ 表达"三连乘实现，全程稀疏。
```python
def neighbors_gpu(mat, k=30):
    X_mat = cupy.array(mat)
    model = cuml.neighbors.NearestNeighbors(n_neighbors=k); model.fit(X_mat)
    return model.kneighbors(X_mat)

spatial_neighborhood = scipy.sparse.csr_matrix(
    ([1]*len(sources), (sources, targets)), shape=[adata.n_obs]*2).astype(np.uint8)
average_expression = D_inv @ spatial_neighborhood @ X_neighbors   # 邻域均值
```
- 搬运条件: 需 RAPIDS 全家桶（cupy/cuml/cudf/cugraph 顶层 import，:4-7），**无 CPU 回退**——符合 strict GPU 纪律但要写进环境文档；KNN 是欧氏（不含半径截断，源仓的半径版在 step03 notebook 里用 spatialdata rings 另实现）；邻接矩阵是"锚行-邻居列"非对称，聚合时注意方向。
- 工程评价: 接口设计好（一个 csr 贯穿所有聚合函数，:32-73），分 slide 切块防串样本；缺点是 notebook 侧复制了同函数造成双源（step03 cell4 vs utils），搬运以 utils 为准。
- 迭代记录: 2026-09-04 收录(一期精读批次C)
