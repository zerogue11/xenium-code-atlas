# PATTERN-049 · 邻居计数矩阵 KMeans 生态位发现链
- 来源: Woopsydaisy/Spatial-Human-Kidney-Map（LIT-048）相对/路径:行号 `D Niche_Analysis/Niche_Analysis_Script2_Neighbor_Dataframe.py:27-39`（按注释类型切片 connectivity 求和）+ `Niche_Analysis_Script3_Kmeans.py:36-38,94,108`（StandardScaler→PCA→MiniBatchKMeans(random_state=42, k=17)）
- 场景: 已有细胞类型注释后，用"每个细胞周围 r µm 内各类型邻居数"作为特征发现生态位（niche）。比图神经网络/CellCharter 轻量、完全可解释，是 niche 分析的入门标配；与 PATTERN-026（CellCharter 契约）、PATTERN-046（NMF 程序视角）互为三选一候选。
- 做法: 对每样本切片 connectivity 矩阵按目标细胞类型列求和 → 拼"细胞×类型"邻居计数 df → 标准化 → PCA 看累计方差 → MiniBatchKMeans 聚出 niche → 沉回 AnnData（obs 顺序断言后回填元数据）。
  ```python
  # 每细胞的"邻居组成"特征
  idx = np.where(ad_s.obs['annotation_updated'] == pop)[0]
  temp_df[pop] = ad_s.obsp["20_micron_connectivities"][:, idx].sum(axis=1)
  # niche 发现
  X = StandardScaler().fit_transform(df_concat)
  kmeans = MiniBatchKMeans(n_clusters=17, random_state=42)
  assert all(adata_subset.obs_names == new_adata.obs_names)  # 回填前断言
  ```
- 搬运条件: 依赖 squidpy obsp+sklearn；无许可障碍。需改造点：①k=17 无选择依据留痕（silhouette 已 import 未用），我们须补 k 扫描曲线并按多候选纪律冻结；②半径与 PATTERN-048 的尺度层对齐（20µm 为主、40µm 复核）；③计数特征对稀疏类型偏斜，标准化后可再加 log1p 对比。
- 工程评价: 特征构造五行核心代码极干净（Script2 主循环），Script3 的 assert 回填是好习惯；全链无函数化、路径硬编码，搬运=重写为两个函数的事。
- 迭代记录: 2026-09-04 收录(一期精读批次E)
