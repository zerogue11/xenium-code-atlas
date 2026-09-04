# 精读笔记 · Teichlab/snp2cell

- repo: https://github.com/Teichlab/snp2cell
- 来源文献: LIT-018 同批 / Pett et al., "snp2cell: leveraging GWAS and single-cell data for disease insights"（Bioinformatics 2024 伴生工具，README 未列正式引文【待补充】）
- 锁定SHA: `e25a6a7fc747a3d3efd759417def1828e4b80e2f`（2026-08-05，v0.3.0，"allow passing through pagerank parameters (#3)"）
- 复核分类: 亚细胞组 · GWAS+GRN 网络传播方法包 · BSD-3（LICENSE.txt:1-3）· 带测试与 CI

## 代码结构走读（实际读了什么）

3767 行 Python，四层：
- `snp2cell/snp2cell_class.py`（1647 行）：核心类 `SNP2CELL`（:41）+ `SUFFIX` 枚举（:35，`__zscore`/`__zscore_mad` 后缀体系）。数据结构三张表：`self.scores`（原始）、`self.scores_prop`（PageRank 传播后）、`self.scores_rand`（置换背景，dict）+ `self.grn`（networkx 图）+ `self.adata`。私有工具：`_prop_scr`（:286，`nx.pagerank(personalization=scr)`，`PROPAGATE_UNDIRECTED=True`）、`_check_init`（:333）、`_defrag_pandas`（:314）。公开主链：`add_score`（:486，打分→传播→置换→统计一条龙）、`propagate_scores`（:576，多 score 并行传播）、`rand_sim`（:620，n 次随机置换 + `loop_parallel` 并行）、`add_score_statistics`（:694，从置换分布算 pval）、`adata_add_de_scores`（:861，链回 scanpy `rank_genes_groups`）、`adata_combine_de_scores`（:984，DE 分数与 SNP 分数逐节点取 min/z-score 合并）、三个 plot 方法（:1267/:1356/:1479）。
- `snp2cell/util.py`（818 行）：GWAS 侧 `get_snp_scores`（:639，对每个 GRN 区域用 pyranges 重叠汇总统计，log Bayes factor≈`exp(logBF − L2/4)`）、`get_snp_scores_parallel`（:721，joblib 分块）、`export_for_fgwas`/`load_fgwas_scores`（:237/:312，fGWAS 外部工具桥接）、`get_gene2pos_mapping`（:175，pybiomart）、`loop_parallel`（:121）、`add_logger` 装饰器（:43）。
- `snp2cell/cli.py`（552 行）：typer 应用，8 个命令（create_object / create_gene2pos_mapping / filter_summ_stats / export_locations / score_snp / add_score / contrast_scores / score_de / combine_scores）把类方法暴露成 `snp2cell` 控制台命令（setup.py entry_points）。
- `snp2cell/recipes.py`（79 行）：GWAS 汇总统计文件预过滤。
- `tests/`（463 行）：`conftest.py` 假 GRN（barbell_graph）+ 假 adata + 绘图非空断言夹具；`test_toy_example.py` 全链路并断言数值序（C>B>A，:63-67）；CI：`.github/workflows/tests.yml`（flake8 + pytest，py3.10）。

## 关键脚本清单

| 文件 | 行数 | 一句话 |
|---|---|---|
| snp2cell/snp2cell_class.py | 1647 | SNP2CELL 类：分数三表 + PageRank 传播 + 置换检验 + scanpy DE 桥接 + 三种图 |
| snp2cell/util.py | 818 | GWAS→区域分数（logBF）、fGWAS 桥接、并行/日志工具 |
| snp2cell/cli.py | 552 | typer CLI 8 命令，类方法的命令行化 |
| tests/test_toy_example.py | 95 | 全链路玩具数据回归，含数值序断言 |
| tests/conftest.py | 65 | barbell 假 GRN/假 adata/绘图非空断言夹具 |
| snp2cell/recipes.py | 79 | 汇总统计过滤配方 |

## 技术路线还原（固定清单勾选）

主流程（GWAS 侧 + 单细胞侧汇合于 GRN）：
1. **数据读取**（fastQTL/fGWAS 输出、BED 汇总统计、GRN adjacency、sc adata）
2. **注释**（单细胞侧 `sc.tl.rank_genes_groups` 产出 per-celltype DE 分数并映射到 GRN 节点，snp2cell_class.py:861-975）
3. **降维/聚类不在此仓做**——链入的 adata 需预先处理好（仅检查非 raw counts，:910-914）
4. 传播与合并（PageRank + z-score 后缀体系 + min(DE,SNP) 组合）
5. **绘图**（plot_group_summary/heatmap/network）
6. **导出**（save_data dill 存档、get_dfs 出表）

固定清单勾选：[数据读取, 注释, 绘图, 导出] = **4 步**（QC/归一化/HVG/降维/聚类/去卷积/空间各步均不在仓内实现）。

## 工程审计表（7 维 × 0-2，共 13/14）

| 维度 | 分 | 证据 |
|---|---|---|
| ①职责单一/模块化 | 2 | 类/工具/CLI/配方四层； GWAS 侧全在 util.py，类只管网络与分数 |
| ②命名规范 | 2 | 私有 `_` 前缀、SUFFIX 枚举统一后缀语义（:35-38）、`outClass/outStats/outLog` 式输出命名一致 |
| ③安全性 | 2 | 无凭据/绝对路径；路径全参数化 |
| ④最简化 | 2 | 未发现死代码；长 docstring 属刻意 API 文档化 |
| ⑤逻辑健壮性 | 2 | `_check_init` 前置断言（:333）、raw counts 检查抛 ValueError（:910-914）、全零 score 跳过告警（:608-610）、多 score 无 perturb_key 报错（:666） |
| ⑥可复现性 | 1 | seed 纪律好：`RANDOM_SEED=42`（:28）、`__init__` 播种（:60-63）、`rand_sim(reset_seed=)`（:653-656）；但 setup.py:36 声称 `python_requires=">=3.5"`，而 util.py 无 future import 且有 13 处 PEP585 泛型（如 :639 `dict[str, float]`），py<3.9 直接 import 失败——声明失真 |
| ⑦验证纪律 | 2 | tests/ 三件套 + CI tests.yml + 玩具链路数值断言（test_toy_example.py:63-67）+ 绘图非空断言（conftest.py:9-22） |

## 可搬运模式

- PATTERN-034：PageRank 网络传播 + 置换检验显著性（add_score→rand_sim→add_score_statistics 三段式）。
- PATTERN-035：基因集库"嵌套字典+categories 子集"统一管理（与 drug2cell 共性，以 drug2cell util.py:19-51 为主证）。

## 坑与限制（实读发现）

- setup.py `python_requires=">=3.5, <3.12"` 与代码语法（PEP585，py≥3.9）矛盾，`<3.12` 上限也无依据；照 README 的 mamba 装旧 python 会炸。
- PageRank 用 `nx.pagerank` 全图迭代，GRN 大（百万边级）时置换 1000 次的开销可观；并行在 `loop_parallel`（进程池），内存翻倍风险。
- `adata_add_de_scores` 默认 `rank_by="up"` 且 query `pvals_adj < 0.05 and scores > 0`（:958），down 调节需显式传参。
- 组合分数的键名是表达式字符串（如 `min(DE_C__score__zscore,snp_score__zscore)`，test_toy_example.py:61），下游取列时依赖这个字符串协议，脆弱。
- `rand_sim` 用 `random.choices(list(score_key), k=n)`（:668）抽样决定置换哪个 key，单 key 语义没问题，但多 key 共享 perturb_key 时次数分配是随机的。
- 本仓不含 GRN 本身（需自带 SCENIC/pySCENIC 或 CellOracle 输出），GWAS 汇总统计需预过滤为带 Beta/SE/L2 列的 BED。

## 一句总评

本批工程质量标杆：类型注解、seed 纪律、typer CLI、CI+玩具回归一应俱全，"分数三表+PageRank 传播+置换背景"的类设计可直接抄给任何"网络打分显著性"问题，唯打包元数据撒了谎（python_requires）。
