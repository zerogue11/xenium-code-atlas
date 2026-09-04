# PATTERN-031 · GATv2 图自编码器组织域发现（KNN 图 + 双损失 GAE + attention 可导出）
- 来源: zhangqf-lab/SPACE（LIT-016，P3）相对/路径:行号 — space/function.py:86-150；space/layer.py:15-51；space/train.py:76-165
- 场景: 组织模块/域发现需要"可解释的细胞间注意力"作为副产品（哪些邻居边主导了域的划分），且单切片数据量中等（万级细胞）可接受 GAT 训练。
- 做法: 空间坐标 KNN(k=20) 建图（或 squidpy spatial_neighbors 备选）→ 表达做 MaxAbs(BCE)/原值(MSE) 缩放 → GAE 训练：内积解码图损失 ×alpha(0.5 域发现/0.05 分型) + MLP 特征重建损失 ×10 → latent 10 维写 obsm['latent'] → leiden/UMAP；三层 GATv2 attention 权重可存 .pt 供边级解释。
```python
graph_dict = graph_construction(adata.obsm['spatial'], adata.shape[0], k=k)
train_data, _, _ = T.RandomLinkSplit(num_val=0.0, num_test=0.0, is_undirected=True)
z, attn_w = model.encode(x, edge_index)          # 三层 GATv2 attention
adata.obsm['latent'] = node_embeddings           # latent 10 维
sc.pp.neighbors(adata, use_rep='latent', key_added='SPACE')
```
- 搬运条件: torch+PyG；latent_dim=10（layer.py:21）、特征损失×10（train.py:119-121）硬编码需解参；**搬运前必修 train.py:107 每 epoch 重建 Adam 的 bug**（动量清零+lr 调度失效）；MIT 许可可自由改。
- 工程评价: seed 纪律满分（function.py:72-82 含 cudnn.deterministic）；包结构五层清晰是好的骨架模板；但优化器 bug、死类（layer.py InnerProduct）、无测试（9/14）——当结构参考，勿当数值基线。
- 迭代记录: 2026-09-04 收录(一期精读批次C)
