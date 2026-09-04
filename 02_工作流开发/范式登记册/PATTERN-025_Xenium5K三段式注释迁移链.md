# PATTERN-025 · Xenium 5K 三段式注释迁移链（单样本 celltypist → 联合 scVI → 子集多分辨率精修）
- 来源: Teichlab/crohns-fibroblast-atlas（LIT-066）相对/路径:行号 — xenium/1a_xenium5k_1.ipynb(cell4-17)；xenium/2_xenium5k_joint.ipynb(cell34)；xenium/3a_xenium5k_annotation.ipynb(cell6-9,36)
- 场景: Xenium 5K panel 少样本（2-4 张）注释：既要粗粒度全覆盖，又要在目标区室（如间质）里细分到亚型——两级分辨率注释的实际落地参考。
- 做法: ①单样本：读 10x_h5+cells.csv+官方 graphclust → QC → normalize/log1p → celltypist.annotate(megagutSmallIntestine_lvl1/lvl3.pkl) 预注释打底；②联合：四样本 concat 后 `scvi.model.SCVI(adata, n_layers=2, n_latent=30, gene_likelihood="nb")`，setup_anndata(layer="counts", batch_key="sample")（counts 层全基因，不做 HVG）；③精修：按 lvl1=='Mesenchymal' 取子集、用 lvl3 预测反向剔除 10 类不一致细胞，再在子集上并跑 leiden resolution=1/2/4/5/10 五个 key，人工把 leiden5 簇号映射到亚型标签，每亚型附概率列。
```python
scvi.model.SCVI.setup_anndata(adata, layer="counts", batch_key="sample")
model = scvi.model.SCVI(adata, n_layers=2, n_latent=30, gene_likelihood="nb")
# 精修: 用另一级 celltypist 预测反证剔除污染
exclude_cells = ["Enterocyte","Trm_CD8",...]  # lvl3 与间质矛盾的细胞
adata_mesen = adata_mesen[~adata_mesen.obs.megagut_lvl3_majority_voting.isin(exclude_cells)]
sc.tl.leiden(adata_mesen, resolution=5.0, key_added='leiden5')  # 1/2/4/5/10 并存
```
- 搬运条件: celltypist 模型须与 panel 基因交集足够（源仓未检查交集，需自加）；注释列契约=megagut_lvl1/lvl3_majority_voting 两级+自定义 annot 列；簇号映射是硬编码（3a cell36），重跑前必须重建映射——搬运时应改为"簇号→marker 证据→标签"三列表。
- 工程评价: 路线本身（三段式+反证剔除+多分辨率并存）是本批"注释列契约"最直接模板；但 notebook 硬编码簇号、.ipynb_checkpoints 入库、无 env 锁（7/14 分）——搬路线不搬实现。
- 迭代记录: 2026-09-04 收录(一期精读批次C)
