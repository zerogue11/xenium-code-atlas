# PATTERN-034 · PageRank 网络传播 + 置换检验显著性
- 来源: Teichlab/snp2cell（LIT-018）相对路径:行号 `snp2cell/snp2cell_class.py:486-548(add_score)、620-692(rand_sim)、694+(add_score_statistics)、286-313(_prop_scr)`
- 场景: 任何"节点上有分数（GWAS 区域分、DE 分、药靶分），想知道分数在网络上的富集位置是否超出随机"的问题——GRN、蛋白互作网、通路图、细胞邻接图都适用。
- 做法: 三段式。(1) 传播：把节点分数作为 personalization 向量喂给 `nx.pagerank(undirected(G), personalization=scores)`，得到平滑后的全局分数；(2) 置换：保留分数值、随机打乱节点标签 n 次（默认 1000），同样传播，得到零分布矩阵；(3) 统计：逐节点算观测值在零分布中的经验 p 值，多核并行。seed 显式传入保证可复现。
  ```python
  def _prop_scr(self, scr_dct, pagerank_kwargs=None):
      return nx.pagerank(self.grn.to_undirected(),
                         personalization=scr_dct, **(pagerank_kwargs or {}))
  # rand_sim: 打乱节点标签
  for key in random.choices(score_keys, k=n):
      node_list = self.scores[key].index.tolist()
      vals_list = self.scores[key].tolist()
      random.shuffle(node_list)
      pers_rand.append(dict(zip(node_list, vals_list)))
  prop_scores = loop_parallel(pers_rand, self._prop_scr, num_cores=num_cores)
  ```
- 搬运条件: 依赖 networkx+numpy+pandas+joblib（可换 omicverse/rapids 加速）；BSD-3 可自由搬运；需改造点：大图下 PageRank 是瓶颈，可换 GPU personalization-PR 或预分解；z-score 后缀命名协议（`__zscore`）建议改用列属性而非键名后缀。
- 工程评价: 类内 `_check_init` 断言、raw counts 校验、全零分数跳过、seed 全链路显式控制，配 CI+玩具数值回归，本批最佳（13/14）；唯 setup.py python_requires 声明与 PEP585 语法矛盾。
- 迭代记录: 2026-09-04 收录(一期精读批次D)
