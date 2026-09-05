# `Moldia/Xenium_benchmarking`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\Moldia__Xenium_benchmarking`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-088：《通过质量评估和最佳实践分析工作流优化Xenium原位数据效用》（Nature Methods 2025，Marco Salas et al.） |
| 精选级 | S |
| 主分类 | P0 流程基准与质控（复核确认，与初判一致；Xenium QC 与最佳实践工作流的核心仓） |
| 次要用途 | P3 空间域（7_domain_exploration）、P6 SVF（8_SVF_identification）、分割基准（5_segmentation_benchmark）、基因插补（10_gene_imputation） |
| 一句话功能 | Xenium 独立基准评估论文伴随包：xb Python 模块（预处理、质控、分割工具对比、SVF、空间域、邻域、模拟、基因插补）+ 11 组主题 notebook + 一条可跑任意新 Xenium 数据的 end-to-end pipeline notebook；对比 25 个 Xenium 数据集与 8 种其他空间平台 |
| License | 无LICENSE(仅可学习不可转载)（主表值） |
| 语言与规模 | Python 为主；py/ipynb 158 个 + R 7 个；体积 1021.4 MB（含 data/ 大目录，本次仅 ls 未进入） |
| 运行入口 | conda env（xenium_benchmarking.yml）→ pip install -e . → notebook；文档 readthedocs（xenium-benchmarking-test） |
| 复现难度 | 中-高 — 环境与函数封装完整，但数据须从 10x 官网/三个 Zenodo DOI 自行下载（repo 的 data/ 只是挂载位），notebook 按任务分组需按序执行 |
| 与范式的关系 | 本项目最高优先 P0 仓之一：预处理参数扫描、分割工具对比、SVF/空间域工具选型结论与 end-to-end pipeline 骨架可直接映射进 zoro-spatial V1/5k 工作流做对照；候选池（核心） |
| 坑提示 | ① Banksy_py 为 git submodule（.gitmodules），普通 clone 拿不到，需 --recursive；② 1GB 体积来自 data/（formatted_for_R、unprocessed_adata 等），拷贝/备份耗时；③ .ipynb_checkpoints、dist、多套 egg-info 入库，属"论文伴随码"原生杂乱 |
| 锁定 SHA | `50249f7d03d9cfc1453c4b81ef3b1053c4d23052`（主表锁定值；建卡时实测前缀 `50249f7d03` 一致） |

## 结构速览

- `xb/`：15 个模块——preprocessing、calculating、comparing、domain_identification、neighborhood、simulating、plotting、formatting、Spage_main、_quality_metrics、_combined、util 等 + run_baysor.sh、baysor_params.toml
- `notebooks/`：0_formatting 至 10_gene_imputation 共 11 个主题目录（含 1_datasets_exploration、3_techniques_comparison、4_optimal_expansion、5_segmentation_benchmark、8_SVF_identification、9_spatial_domain_annotation）
- `end-to-end_pipeline_optimized.ipynb`：端到端示例管线（README 声明可用任意新 Xenium 数据）
- `data/`（大数据目录，未进入；内含 formatted_for_R、unprocessed_adata 等）、`figures/`、`Banksy_py`（submodule）

## README/代码实读要点

- 数据来源三类：10x 官网公开集（截至 2024-05-03）、Kukanja/Langseth Cell 2024 脊髓数据、自产小鼠脑 4 切片（Zenodo 10566172）
- 预格式化 AnnData 在三个 Zenodo DOI（11124988/11121221/11120307），示例数据（人脊髓）单列 DOI 11120922
- 环境搭建：conda env create --name xb --file=xenium_benchmarking.yml → conda activate xb → pip install -e .
- xb/preprocessing.py 的 main_preprocessing 默认参数：target_sum=100、mincounts=10、mingenes=3、neigh=15、total_clusters=30（用于预处理策略模拟）
- 4 个小鼠脑切片以 "hm" 标签贯穿全研究

## 抽读实录

- 读 README 全文（数据来源、文件夹结构、环境搭建）；ls xb/、notebooks/、data/（仅一层）；读 xb/preprocessing.py 开头 20 行（main_preprocessing 函数签名与默认参数）。

## 复用建议

- 优先精读 end-to-end_pipeline_optimized.ipynb 与 xb/_quality_metrics.py，映射 zoro-spatial readiness/QC 段做参数对照；5_segmentation_benchmark 结论用于分割器选型；Banksy 克隆时补 --recursive。
