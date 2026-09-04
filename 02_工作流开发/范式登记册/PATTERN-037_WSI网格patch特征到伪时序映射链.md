# PATTERN-037 · WSI 网格 patch 特征 → AnnData 空间伪时序映射链
- 来源: kateyliu/ImagePseudo（LIT-023）相对路径:行号 `GradePrediction.py:69-146(extract_feature_from_WSI)、Pseudotime.py:11-40(paga)`
- 场景: 把病理大图变成"空间化的单细胞-like"对象：每个网格 patch 相当于一个细胞，ViT 特征当表达谱，从而套用 scanpy 的降维/聚类/拟时序全套武器，得到肿瘤演化的空间轨迹图。
- 做法: 关键是**网格坐标与特征并表**的交换格式——每行 `n_col, n_row, pred_class, x0..x767` 的 CSV（块内代码 84-88 行），n_col/n_row 就是 WSI 上的空间坐标。下游把特征列作 X、坐标列作 obs 建 AnnData，PCA→neighbors→leiden→PAGA→定根→DPT，伪时序和聚类标签再按网格坐标铺回 2D 热图。组织掩码在装载侧过滤非组织网格。
  ```python
  col_names = ['n_col','n_row','pred_class'] + [f"x{i}" for i in range(768)]
  x, obs = pd.DataFrame(wsi_df.iloc[:,3:]), pd.DataFrame(wsi_df.iloc[:,0:3])
  adata = ad.AnnData(x, obs)
  sc.tl.pca(adata); sc.pp.neighbors(adata, n_neighbors=4, n_pcs=20)
  sc.tl.leiden(adata, resolution=1); sc.tl.paga(adata, groups='leiden')
  adata.uns['iroot'] = np.flatnonzero(adata.obs['pred_class'] == start_class)[0]
  sc.tl.dpt(adata)
  ```
- 搬运条件: 依赖 openslide/transformers(phikon 或任意 ViT)/scanpy/anndata；MIT 可自由搬；需改造点：根节点改参数化（原实现硬编码 start_class=4）、逐行 loc 追加改批量、接 Xenium 时把"网格 patch"换成细胞/spot 即得空间伪时序，特征抽取器可换 HE 预测表达模型。
- 工程评价: 交换格式设计好（一张 CSV 贯通图像侧与 scanpy 侧），实现质量差（scipy.misc 必炸、裸 except 吞错、O(n²) 追加、死分支多，5/14）——搬运时保留格式协议、重写实现。
- 迭代记录: 2026-09-04 收录(一期精读批次D)
