# PATTERN-030 · 多注释器投票合并（5 工具并列 + 多数票 + 最近方法回退）
- 来源: zenglab-pku/SPATCH（LIT-084;LIT-090）相对/路径:行号 — analysis/9_st_annotation.py:12-97（Selina:12, Spoint:31, Tangram:46, Tacco:62, celltypist:71, 合并:81-97）
- 场景: 对同一 ST 数据用多种注释迁移方法各跑一遍后，需要合成一列"共识注释"并量化方法间一致性（基准测试或结果稳健性检查）。
- 做法: 每工具输出一列标签 → 按列拼接成 细胞×方法 表 → 逐细胞取众数为 final_annotation → 统计各方法与众数的一致率 → 众数为 unknown 的细胞回退到"与共识最接近的方法"的标签；一致性评估脚本另算方法两两一致率/簇数。
```python
data = pd.concat([pd.read_csv(f, header=None) for f in files], axis=1)  # 细胞×5方法
data['final_annotation'] = data.apply(vote, axis=1)                     # 逐行众数
intersect = [np.sum(data['final_annotation']==data.iloc[:,i]) for i in range(5)]
method_index = intersect.index(max(intersect))                          # 最贴近共识的方法
data.loc[data['final_annotation']=='unknown','final_annotation'] = \
    data.iloc[:,method_index][data['final_annotation']=='unknown']      # 回退
```
- 搬运条件: 各工具需先统一标签空间（源仓全用 'major' 参考标签）；vote 函数源码未随仓发布【待补充】需自实现（pandas mode）；注意源仓各工具预处理不统一（celltypist 自带 norm+log1p:72-75，Tacco 用原值:65-68），公平对比要拉齐。
- 工程评价: "多数票+最近方法回退"两级设计简单有效；但同名 predict 函数冲突（:12 与 :31 后者遮蔽前者）说明该文件从未被整体 import 运行——投票逻辑要重写，框架思路可保留。
- 迭代记录: 2026-09-04 收录(一期精读批次C)
