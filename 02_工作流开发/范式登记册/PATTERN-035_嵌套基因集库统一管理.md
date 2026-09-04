# PATTERN-035 · 嵌套基因集库统一管理（prepare_targets 前置件）
- 来源: Teichlab/drug2cell（LIT-018）相对路径:行号 `drug2cell/util.py:19-51(prepare_targets)、8-17(reconstruct_targets)`；同构实现 `Teichlab/snp2cell/snp2cell_class.py:35-38(SUFFIX)`
- 场景: 方法包的每个公开函数都要接受"基因组字典"，但来源有三种：用户手传扁平 dict、手传嵌套分类 dict（如 ATC 一级/二级）、不传（用随包默认库）；还要支持按分类子集化、以及从上次打分结果反解基因组。不统一就到处重复 if/else。
- 做法: 单一 `prepare_targets(adata, targets, nested, categories, sep, reconstruct)` 收口所有形态：targets=None 时按需从 `.uns` 反解或载默认库；categories 先子集化（键筛选）；nested=True 时用 `collections.ChainMap` 把 dict-of-dicts 展平成 `{group:[genes]}`；全程 copy 防止改用户原字典。三个主函数开头各调一次，函数体只面对一种形态。
  ```python
  def prepare_targets(adata, targets=None, nested=False, categories=None, sep=",", reconstruct=False):
      if targets is None:
          if reconstruct and ('drug2cell' in adata.uns):
              targets = reconstruct_targets(adata, sep=sep)   # 从 .uns 反解
          else:
              targets = data.chembl(); nested = True
      else:
          targets = targets.copy()
      if categories is not None:
          targets = {k: targets[k] for k in categories}
      if nested:
          targets = dict(ChainMap(*[targets[cat] for cat in targets]))
      return targets   # 永远是 {group:[genes]}
  ```
- 搬运条件: 纯 stdlib+pandas，无许可风险（BSD-3 / GRL——自写等价物即可）；需改造点：可加 categories 不存在时的 KeyError 提示与去重告警。
- 工程评价: 24 行解决四态输入，是"参数归一化收口到单一函数"的教科书小例； drug2cell 无测试使其缺乏回归保护，搬运时应配单测（10/14）。
- 迭代记录: 2026-09-04 收录(一期精读批次D)
