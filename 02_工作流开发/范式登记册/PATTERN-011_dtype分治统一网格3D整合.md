# PATTERN-011 · dtype 分治 Spore + 统一网格 3D 整合
- 来源: ding-lab/mushroom（LIT-019;LIT-071）mushroom/mushroom.py:75-478（Mushroom）、mushroom/model/integration.py:88-156（integrate_volumes）
- 场景: 同一组织的连续切片用了不同空间平台（Xenium/CosMx/Visium/HE/多色免疫荧光），需要把它们对齐到统一 3D 网格并产出跨模态一致的空间域图。
- 做法: 每种 dtype（模态）单独训练一个 Spore（SAE：ViT encoder + 分级 codebook + 该模态专属 decoder），所有模态重采样到同一目标分辨率网格（如 0.02 px/μm 即 50 μm 格宽）；各模态输出逐网格聚类概率体积后，沿 z 线性插值成连续体积；再以"各模态 cluster 的平均通道强度向量之间的距离"为边权建 igraph 图，leiden 合并成 integrated 体积。骨架：
```python
# mushroom.py:96-121 每个 dtype 一个 Spore
for dtype in self.dtypes:
    spore = Spore(dtype_sections, chkpt_filepath=..., sae_kwargs=..., trainer_kwargs=...)
    self.dtype_to_spore[dtype] = spore
# mushroom.py:203-208 统一网格分辨率
size = max(spore.clusters[0].shape[-2:] ...)
spore.resize_clusters(self, size=size)
# integration.py:149 图整合
g = igraph.Graph(); g.add_vertices(n); g.add_edges(edges)
results = g.community_leiden(weights=weights, resolution=..., objective_function='modularity')
```
- 搬运条件: 依赖 torch/lightning/vit-pytorch/einops/igraph/torchio；代码无许可证字段外的额外限制（仓库含 LICENSE，MIT 系【待补充：LICENSE 具体类型未逐行核对】）；需改造点：去掉 wandb 默认项目名、补 seed、cluster_dists 构图对大 ROI 要换近似近邻。
- 工程评价: 架构分层（Mushroom/Spore/SAE）与统一网格思想是本批最佳；实现层有拼写错误与死代码，训练不可复现（无 seed）。
- 迭代记录: 2026-09-04 收录(一期精读批次B)
