# PATTERN-026 · CellCharter niche 发现契约（delaunay 图 → n_layers 聚合 → ClusterAutoK 稳定性选 k）
- 来源: Teichlab/crohns-fibroblast-atlas（LIT-066）相对/路径:行号 — xenium/4a_xenium5k_niche.ipynb(cell10,16-19)；交叉印证 zenglab-pku/SPATCH（LIT-090）analysis/10_spatial_cluster.py:26-46
- 场景: 单细胞分辨率空间数据的组织域/niche 无监督发现，且希望"k 值"由稳定性自动定而非人工拍——niche 列的产出契约参考。
- 做法: 建图用 delaunay（按 library_key=样本分块）→ `cc.gr.aggregate_neighbors(n_layers=3, use_rep='X_scVI')` 把每个细胞及其 3 跳邻域表达聚合成 X_cellcharter 表征 → `cc.tl.ClusterAutoK(n_clusters=(4,25), GaussianMixture, random_state=42, max_runs=5)` 自动跑全 k 段 → `cc.pl.autok_stability` 曲线选最优 k → GaussianMixture 终模型给每个细胞 niche 标签。SPATCH 变体：n_layers=5、AutoK(5,10)、先 `cc.gr.remove_long_links` 剔长边、GPU trainer_params。
```python
sq.gr.spatial_neighbors(adata, library_key='sample', coord_type='generic', delaunay=True)
cc.gr.aggregate_neighbors(adata, n_layers=3, use_rep='X_scVI')
models = cc.tl.ClusterAutoK(n_clusters=(4,25), model_class=cc.tl.GaussianMixture,
                            model_params={'random_state':42,'trainer_params':{'accelerator':'cpu'}}, max_runs=5)
models.fit(adata, use_rep='X_cellcharter')
ax = cc.pl.autok_stability(models, return_ax=True)   # 稳定性曲线定 k
```
- 搬运条件: cellcharter 依赖 pytorch-lightning；输入需已有多样本整合表征（X_scVI/X_trVAE，聚合层按 sample_key 分块）；AutoK 全 k 段+max_runs 是重计算，建议 GPU；出参=adata.obs 的 niche 标签列（两仓均以 obs 列为契约）。
- 工程评价: 两仓独立实现同一契约（delaunay→aggregate→AutoK→GMM），参数差异小（n_layers 3/5、k 段 (4,25)/(5,10)），说明该契约已在领域内定型——照抄参数即可起步；random_state 均固定（42/12345）。
- 迭代记录: 2026-09-04 收录(一期精读批次C)
