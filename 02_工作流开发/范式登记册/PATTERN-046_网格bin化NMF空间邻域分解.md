# PATTERN-046 · 网格 bin 化 NMF 空间邻域分解
- 来源: Goldrathlab/Spatial-TRM-paper（LIT-035）相对/路径:行号 `processing_pipelines/Xenium_human_processing/core_functions/initial_neighborhoods.py:12-127`（create_grid_bins / create_binned_data / plot_top_words）
- 场景: 单细胞分辨率空间数据的"邻域发现"：不想建细胞图做图聚类，而是想问"组织每个局部区域里哪些基因/细胞程序共现"。适合大组织片、需要可视化 NMF 主题的空间铺展。
- 做法: 把组织切成 n×n 网格 bin，每 bin 内对落点细胞表达取均值，得到"bin×基因"伪 bulk AnnData，再跑 NMF，每个 topic 即一个空间邻域程序，top-words 条形图直接当图版素材。
  ```python
  # 1) 网格分桶：np.searchsorted 把 (x,y) 点分配进 n×n 格
  xi = np.searchsorted(xbins, x, side="right") - 1
  yi = np.searchsorted(ybins, y, side="right") - 1
  # 2) bin 内均值表达 → AnnData（bin=obs, gene=var），obsm["spatial"]=bin 中心
  bin_expression = np.mean(arr[where_bin, :], axis=0)
  # 3) NMF 主题 + 每 topic top 基因条形图
  model = NMF(n_components=k); W = model.fit_transform(binned_ad.X)
  ```
- 搬运条件: 依赖 sklearn NMF/scanpy；无额外许可风险。需改造点：①原实现网格越界用 `except: None` 静默吞点（initial_neighborhoods.py:45-48），搬运时改成显式边界过滤；②bin 数 n 与 NMF k 都需按组织尺度扫描后冻结；③bin 是规则网格，不规则组织边缘会产生空 bin（原实现置零后滤 NaN 行），可换 alphashape 裁剪（该仓 pixi.toml:38 已装 alphashape 佐证作者有此意图）。
- 工程评价: 三函数 127 行、docstring 完整、易抽走；与 PATTERN-021（SNF 生态型）互补——一个是网格伪 bulk 的基因程序视角，一个是细胞组成视角。
- 迭代记录: 2026-09-04 收录(一期精读批次E)
