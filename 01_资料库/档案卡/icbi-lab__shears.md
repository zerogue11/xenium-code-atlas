# `icbi-lab/shears`（档案卡）

> 由 agent 依据本地克隆实测撰写；不确定处一律【待补充】；禁止编造星标/日期/功能。

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-072：《结直肠癌中性粒细胞》（论文题录【待补充】，README 未给） |
| 精选级 | A |
| 主分类 | P8（疾病应用，复核维持） |
| 次要用途 | 方法工具包：单细胞→bulk 反卷积 + 加权生存/GLM 关联（服务任意 P8 场景的 bulk 验证支线） |
| 一句话功能 | scverse 风格 Python 包：把单细胞图谱映射为 bulk 样本的"细胞权重"（ridge 正则反卷积），再做加权 Cox 生存回归与加权 GLM 关联，内置 TCGA/NSCLC/LUCA-30K 队列加载器 |
| License | BSD |
| 语言与规模 | Python x11；6.2MB；src 布局 + tests + readthedocs + CI + pre-commit/flake8 + codecov + bumpversion |
| 运行入口 | pip 安装后 API 调用（pp → tl → pl 流水）；datasets 模块直接取 TCGA 等队列 |
| 复现难度 | 低 — 标准包结构、pyproject 声明依赖、有测试与文档站；比 notebook 仓可复用性高一档 |
| 与范式的关系 | 候选池：P8 场景"空间/单细胞发现 → TCGA bulk 生存验证"一步打通的方法件；omicverse 生态外少数现成"加权 Cox"实现 |
| 坑提示 | ① README 几乎零信息，功能要读 tl/pp 源码与 tutorial；② 只能 git+https 安装；③ Citation t.b.a、CHANGELOG 停在 Unreleased |
| 锁定 SHA | 主表未登记（空）；本地克隆 HEAD `a4fcfc9c7e9a71b5de7f1701c2c5a95b5361cea2` |

## 结构速览

- `src/shears/pp/`（预处理与反卷积）：
  - quantile_norm：sklearn quantile_transform 写入新 layer（key_added 默认 "quantile_norm"）。
  - recipe_shears：n_top_genes=2000 默认，串联 quantile_norm 与后续准备。
  - `_deconvolute`：单 bulk 样本 vs sc 矩阵，alpha 正则、random_state 可控。
  - cell_weights：joblib 并行主入口（Parallel/delayed + tqdm）。
- `src/shears/tl/`（关联分析）：
  - `_prepare_bulk_obs_and_weights`：构建回归 formula、按需子集 bulk.obs、取 per-cell 权重。
  - `_test_cell_glm`：statsmodels family + formulaic model_matrix。
  - `_test_cell_cox`：lifelines CoxPHFitter（ConvergenceWarning 抑制 + threadpool_limits）。
  - shears_cox / shears_glm：对外主函数。
  - get_scaling_factor（中位数回调定标，weight_col 默认 "n_genes"）。
  - cell_type_fractions（as_fraction、bias_correction 选项）。
  - shears_stats（groupby + batch_key、cell_cutoff=20 的统计汇总）。
  - fdr_correction 在 `_util`。
- `src/shears/datasets/`：tcga(cohort, layers=("TPM","counts"))、tcga_nsclc()、luca_30k()。
- `src/shears/pl/`：plot_shears_boxplots。
- `docs/`：scverse cookiecutter 模板底子（index/api/changelog/template_usage +
  notebooks/tutorial.ipynb、example.ipynb）；.github 有 test.yaml。

## 实读补充

- 与 LIT-072 的对应关系（源码实读推断）：CRC 中性粒细胞信号 → recipe_shears 求 bulk 权重
  → shears_cox 关联生存 / shears_glm 关联协变量；论文具体用法【待补充】。
- 环境：Python ≥3.10（README），依赖含 anndata、scanpy、lifelines、statsmodels、formulaic、
  sklearn、joblib（pp/tl import 实测）。
