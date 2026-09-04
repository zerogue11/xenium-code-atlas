# PATTERN-033 · 矩阵乘法批量基因群打分 + 结果以子 AnnData 存 `.uns`
- 来源: Teichlab/drug2cell（LIT-018）相对路径:行号 `drug2cell/__init__.py:143-217`；辅助 `drug2cell/util.py:19-51`
- 场景: 需要对 AnnData 一次性计算大量基因群（药靶/通路/GO）的逐细胞活性分，且希望结果继续用 scanpy 生态（UMAP、marker、绘图）而不是散装 DataFrame。
- 做法: 把"每个基因组一个循环"改为一次矩阵乘法：基因组成员表转成 基因×群 的 0/1 权重矩阵 W（按列归一到 1，即群内均值权重），`X @ W` 一步得到 细胞×群 分数矩阵；seurat 式背景校正同样用权重矩阵（按表达分箱构造对照基因权重，control_profiles @ drug_weights 再相减）。结果包成新 AnnData 存回 `.uns['drug2cell']`，复制 `.obs`/`.obsm`，把群成员基因写进新 `.var['genes']`，下游 scanpy 函数无缝可用。
  ```python
  weights = pd.DataFrame(targets_bool, index=var_names)   # 基因×群 0/1
  weights = weights.loc[:, weights.sum()>0]
  weights = weights / weights.sum()                        # 群内均值权重
  scores = X.dot(weights)                                  # 细胞×群 一次算完
  adata.uns['drug2cell'] = anndata.AnnData(scores, obs=adata.obs)
  adata.uns['drug2cell'].obsm = adata.obsm                 # 嵌入坐标直通
  ```
- 搬运条件: 依赖 anndata/pandas/numpy/scipy（稀疏 X.dot 通用）；许可证 GRL 非商业——**只搬思路不搬代码**，自写等价实现无法律风险；需改造点：method 参数枚举校验、shuffle 加 seed、结果槽位防覆写。
- 工程评价: 845 行小包零死代码，权重矩阵构造与 `.uns` 存回的接口设计是范本级；无测试无 CI，工程闭环不全（10/14）。
- 迭代记录: 2026-09-04 收录(一期精读批次D)
