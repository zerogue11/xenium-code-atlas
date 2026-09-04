# `natsuhiko/PHM`（档案卡）

> 由 agent 依据本地克隆实测撰写；不确定处一律【待补充】；禁止编造星标/日期/功能。

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-018：《骨骼发育图谱（PHM 配套）》——论文题录【待补充】，README 未给 |
| 精选级 | A |
| 主分类 | P8（复核维持但强标注：本仓是统计遗传方法工具，P0–P7 无对应类目，P8 为残类兜底；建议终审复核去留/改挂） |
| 次要用途 | 统计遗传方法：孟德尔随机化式 QTL→调控元件因果映射（非空间转录组） |
| 一句话功能 | Pairwise Hierarchical Model：C/C++ 两阶段贝叶斯层级模型，从 QTL 关联 Bayes 因子推断调控元件对之间的因果方向与 master regulator（hm 估计先验，phm 估计峰对先验） |
| License | 无LICENSE(仅可学习不可转载) |
| 语言与规模 | Shell x8 / C 与 C++ 头 x7（另有 R 转换脚本）；47.2MB（含 data/ 测试数据） |
| 运行入口 | src/ 下 make && make install（需自设 GSL、HTSlib、CLAPACK 的 CFLAGS/LDFLAGS），装到 $PHMDIR/bin；script/test.sh（chr22 端到端 <1h）；两阶段批量脚本 bayeslm1.sh、bayeslm2.sh |
| 复现难度 | 高 — 需自行编译三个 C 库；输入为自定义二进制 double 数组 + tabix 索引 VCF/bed |
| 与范式的关系 | 与空间组流程无直接交集；仅当 LIT-018 场景需要"图谱→调控因果"深挖时参考。候选池：否 |
| 坑提示 | ① README 红字警告列规范仅适用当前实现；② hm 要求 peak ID 从 1 连续编号；③ PHMDIR 必须 export；④ N*m* 数值列必须 scale 到 [0,1] |
| 锁定 SHA | 主表未登记（空）；本地克隆 HEAD `09f70244f02c56e457b16d930c9006fcd4e03629` |

## 结构速览

- `src/`：hm 与 phm 两个二进制的 C 源码/头文件；make 安装到 `$PHMDIR/bin`。
- `script/`：
  - test.sh：chr22 端到端验证，产出 Stage1/Stage2 输出目录。
  - bayeslm1.sh：变异级 Bayes 因子计算（前 2 参数=分箱号与每箱峰数，可并行）。
  - bayeslm2.sh：峰对级 RBF 计算（第 6/7 参数吃第一阶段 hm 输出）。
- `data/`：chr22 ATAC-seq 测试数据。
- README（方法仓少见的完整文档）：
  - 两阶段 workflow 图 + 输入列类型表：I（Peak ID）、C*n*（n 水平分类变量）、
    N*m*（m 个样条基的数值变量，须 scale 到 [0,1]，m=0 为线性）、B（Bayes 因子）、S（跳过）。
  - hm 的 -c 示例 `I,S,S,S,S,S,S,S,C2,C3,S,S,B`；phm 的 -c 示例 `J,K,N4,B10`。
  - 输出 pp.gz 逐列说明：null / 5' single / 3' single / linkage（独立 QTL）/ pleiotropy /
    5'→3' causality / 3'→5' causality 等 10 种交互子假设后验。
  - 输出 pmr.gz：master regulator 对数概率、上下游峰期望数、MAP 父峰 ID 及其对数后验。
  - CLAPACK 编译教程（netlib 源码 + `ln -s` 出 liblapack/libblas/tmglib）与 GSL 编译教程。

## 复核说明

- 主表初判 P8；实读确认这是独立的统计遗传方法仓（孟德尔随机化式调控映射），
  与骨骼发育图谱论文的配套关系体现在应用而非内容。
- P0–P7 无对应类目，暂按残类 P8 保留；建议终审时决定是否改挂方法类或降权。
