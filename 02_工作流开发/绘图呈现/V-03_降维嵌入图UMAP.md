# V-03 · 降维嵌入图（UMAP/t-SNE）（组别：构成与身份）
> 频次: 5/269 条（书目 2026-09-27 口径）｜代表文献: LIT-012、LIT-047、LIT-048

## 这张图回答什么问题（论证链定位）
回答"细胞/邻域在转录组空间里分成几群、谁挨着谁、群间过渡长什么样"：它是细胞身份的总地图，几乎总在结果开篇出现，后续所有空间图的配色都从它定下。科学价值在于用一张图固定"身份坐标系"，让读者带着同一套颜色读完全文；空间组学里的进阶用法是把物理量（距边界距离、密度、时间点）编码进嵌入，让嵌入图与空间图互为印证。

## 数据前提
- adata.obsm['X_umap']（或 X_tsne/X_pca）嵌入坐标：复现须锁 random_state 与 neighbors 参数，否则形状漂移。

- obs 细胞类型/cluster 注释列：图上着色依据，也是全局 palette 表的主键。

- 可选数值列：密度（2D 核密度叠加）、梯度值（距肿瘤边界距离）、平台/批次标签（跨平台整合图）。

- 图级 notebook 输入应为管线冻结的 h5ad（本库契约：产数/出图双层，PATTERN-045）。

## 工具选型
- py 首选: scanpy sc.pl.umap——与 neighbors/leiden 同生态，palette 直接传 dict，点层可 rasterize。

- py 备选 / R: Seurat DimPlot；密度叠加用 seaborn.kdeplot 双层绘制（apoe 仓路线）；梯度着色自绘 scatter+colorbar 更可控。

- 本库参考实现: 01_资料库/精读笔记/Goldrathlab__Spatial-TRM-paper.md（产数/出图双层结构实测）。

## 最佳参考仓（实证）
- Goldrathlab/Spatial-TRM-paper：Figure_2/2abc.ipynb 纯绘图型 notebook——管线 notebook 冻结 h5ad 到 data/adata/，图级 notebook 只 sc.read_h5ad+浅归一化+绘图，自绘 Zissou 色表做空间图。
  本库价值："产数/出图双层"契约的直接模板，即 PATTERN-045 的原型。

- digitalcytometry/spatialecotyper：R/SpatialView.R 画空间邻域嵌入 UMAP，按"距肿瘤边界距离"着色呈现肿瘤核心→邻近间质连续梯度（LIT-047 Fig.2b 即出自此包）。
  本库价值：物理量编码进嵌入的现成 R 实现。

- Moldia/Xenium_benchmarking：xb/preprocessing.py 内 preprocess_adata 的 UMAP 出图段，与聚类同一函数链。
  本库价值：快速批量出图，但注意其出图与写盘耦合（见 V-01 卡坑 3）。

## 文献借鉴要点（书目摘录）
- LIT-012 Fig.1：在微胶质细胞 UMAP 上叠加 10/20/96 周龄三组细胞的 2D 核密度等高线，直观展示 TIM 状态随年龄的分布迁移。
  点评：跨时间点细胞状态动态的嵌入图标准写法。

- LIT-047 Fig.2b：空间邻域嵌入 UMAP 按"距肿瘤边界距离"着色，把物理空间位置编码进嵌入空间。
  点评：嵌入图与空间图互证的桥。

- LIT-048 Fig.1f：CosMx 1k+Xenium 5k+snRNA-seq 三平台经 scANVI 整合的 >500 万细胞统一 UMAP，跨平台图谱整合样板。
  点评：500 万细胞的点层 rasterize 是必做项。

## FigureYa 候选模板
- FigureYa93UMAP（Seurat RunUMAP 嵌入出图）

- FigureYa27t-SNE（t-SNE 嵌入出图）

（Source Pack 未配置，落地需先配置后 materialize；目录 319 模板可检索）

## zoro-figure 铁律适用条目
- 铁律 4：cluster 颜色全局一致唯一——嵌入图的配色就是全项目 palette 的源，先建表再出图。

- 铁律 7：统一色族，离散分类用定性色板、连续梯度用 sequential 色板，不混用。

- 铁律 8：Arial、mm 尺寸、6-7pt；点大与图幅匹配。

- 铁律 10：两位序号_英文短名，嵌入图多为 01_ 前缀的开篇图，图落 figures/<图号>/（PATTERN-006）。

## 常见坑
- UMAP 形状随 seed 漂移：随机性是固有属性，论文复现必须把 random_state、n_neighbors、min_dist 写进"怎么跑的"；跨版本对比先确认参数一致再比形状。

- 点太密糊成实心：先 rasterize 点层再叠矢量标注（matplotlib set_rasterized(True)），否则 PDF 巨大且印刷发糊。

- 跨平台/跨样本拼图时各 notebook 各自定义 palette 导致同群异色：本库纪律是建一张全局 palette 表，所有图从表取色（铁律 4）；Zissou 这类自绘色表也登记进表。
