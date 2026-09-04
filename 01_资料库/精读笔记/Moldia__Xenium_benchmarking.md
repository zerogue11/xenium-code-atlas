# 精读笔记 · Moldia__Xenium_benchmarking

- repo: Moldia/Xenium_benchmarking
- 来源文献: LIT-088（Marco Salas et al., "Optimizing Xenium In Situ data utility by quality assessment and best practice analysis workflows", Nat Methods 2024 线）
- 锁定SHA: 50249f7d03d9cfc1453c4b81ef3b1053c4d23052（2026-04-10 "Add files via upload"）
- 复核分类: S 级 / 基准-质控组 / Python 包 xb + notebook 群（克隆 1023MB，data/ 未进入）
- 语言与体量: Python 3.7；xb/ 12 模块 3175 行；notebooks/ 11 个任务目录；end-to-end notebook 65 单元（95MB 含输出）

## 代码结构走读

```
xb/_quality_metrics.py  (204行) 12 个 QC 指标函数（cell_density/assigned_reads比例/中位reads每细胞/基因数…）
xb/formatting.py        (804行) Xenium 原始输出→AnnData（4 个版本变体）+ Baysor 输入准备 + 核重叠过滤
xb/preprocessing.py     (166行) main_preprocessing（模拟用参数扫描版）+ preprocess_adata（主流程版）
xb/calculating.py       (366行) 亚细胞分布（dist_nuc 核距离）、分散度、VI/NMI/FMI、负marker纯度、Moran I
xb/domain_identification.py (306行) Banksy/NBD/RBD 三种域识别 + 域间比较
xb/neighborhood.py      (49行)  Squidpy 邻域富集封装
xb/simulating.py        (429行) 模拟数据生成；Spage_main.py (431行) SpaGE 插补+留一验证
xb/comparing.py (102) plotting.py (127) util.py (149) _combined.py (42)
Banksy_py/              git submodule（prabhakarlab/Banksy_py，本克隆未初始化，空目录）
notebooks/0-10_*        按任务编号：formatting/exploration/segmentation_free/techniques_comparison/
                        optimal_expansion/segmentation_benchmark/simulating/domain/SVF/annotation/imputation
end-to-end_pipeline_optimized.ipynb   官方推荐入口：format→Baysor→preprocess→域→插补→SVF→邻域
```

入口链（端到端 notebook，实际逐单元抽取通读）：`files=[样本目录]` → `format_to_adata()`（formatting.py:634，合并多切片、min_quality/max_nucleus_distance 过滤）→ 可选 `prep_xenium_data_for_baysor()`+docker 跑 Baysor → `preprocess_adata()`（preprocessing.py:98）→ 三选一域识别 `domains_by_banksy/nbd/rbd` → `compare_domains` → SpaGE 插补 + `leave_one_out_validation` → `svf_moranI` → `nhood_squidpy`。全部函数来自 xb 包 import，notebook 只做参数与编排。

## 关键脚本清单

| 文件 | 行数 | 一句话 |
|---|---|---|
| xb/formatting.py:634 format_to_adata | ~40 | 多 Xenium 样本目录→AnnData 的统一入口（use_parquet 可选） |
| xb/preprocessing.py:17 main_preprocessing | ~80 | 参数化预处理+自适应分辨率聚类（迭代调 resolution 至目标簇数±3） |
| xb/preprocessing.py:98 preprocess_adata | ~68 | 主流程：过滤→归一→HVG→PCA→neighbors→多分辨率聚类→UMAP→DE→批量出图→写 h5ad |
| xb/_quality_metrics.py | 204 | 12 个单指标函数（PATTERN-001 原型） |
| xb/domain_identification.py:68/257/153 | ~180 | Banksy/NBD/RBD 三域算法统一签名 domains_by_*(adata, hyperparameters) |
| xb/calculating.py:341 svf_moranI | ~25 | Squidpy Moran's I 批量 SVF |
| notebooks/5_segmentation_benchmark/{gen_counts,methods,metrics,run_*}.py | 1071 | 分割基准自包含工具箱：模拟计数→Cellpose/核/分箱/Baysor/ClusterMap→指标 |

## 技术路线还原（勾选自固定清单，按实际顺序）

1. 数据读取（format_to_adata：Xenium outputs→AnnData，raw 层保留）
2. 质控QC（keep_nuclei_and_quality 的 min_quality/max_nucleus_distance 过滤 + _quality_metrics 12 指标）
3. 归一化（normalize_total target_sum=100 + log1p）
4. HVG（preprocess_adata 内 highly_variable_genes；main_preprocessing 里可开关）
5. 降维（PCA arpack + UMAP）
6. 聚类（leiden/louvain 多分辨率 + 自适应分辨率循环逼近目标簇数）
7. 注释（notebooks/1_2、1_5 细胞类型识别线；end-to-end 主链不含）
8. 亚细胞（Baysor 转录本重分割备选 + calculating.py:22 dist_nuc 转录本-核距离分散度）
9. 空间邻域/域（Banksy/NBD/RBD 域识别 + nhood_squidpy 邻域富集）
10. 空间统计（svf_moranI 空间变异基因）
11. 多样本整合（files 列表合多切片、obs['sample'] 分层、adapt_banksy_for_multisample）
12. 绘图（plot_cell_counts/UMAP/空间图全在 preprocess_adata 与各 domains_by_* 内）
13. 导出（combined_processed.h5ad + figures/*.pdf）

未做：去卷积、细胞通讯、配准/3D。清单外步骤：SpaGE 基因插补（端到端第 5 步）与分割方法基准（notebooks/5）。

## 工程审计表（7 维，0-2 分）

| 维度 | 分 | 证据 |
|---|---|---|
| ①职责单一/模块化 | 2 | xb 12 模块按职责切分、函数签名统一（adata 进、adata/float 出）；notebook 按任务编号 0-10 组织；end-to-end 纯编排不含算法 |
| ②命名规范 | 1 | domains_by_banksy/nbd/rbd 命名对仗清晰；但 __init__.py 全部为非法语法 `from xb.plotting import .`（__init__.py:1-12），domain_identificaion 拼错，Spage_main 名不符实 |
| ③安全性 | 1 | notebook 端到端 cell23 内嵌作者个人路径 /media/sergio/…（示例性质）；yml:201 prefix=/home/sergio/anaconda3 入库；无凭据 |
| ④最简化 | 0 | dist/、3 个 egg-info、.ipynb_checkpoints、__pycache__、95MB notebook 带输出全部入库；formatting.py 存 4 个代际读入变体共存；QC 指标在 xb/_quality_metrics.py 与 notebooks/5/metrics.py 两处重复 |
| ⑤逻辑健壮性 | 0 | main_preprocessing 的 louvain 自适应循环里误调 sc.tl.leiden（xb/preprocessing.py:88，louvain 块写 leiden 的复制粘贴 bug）；无 seed；错误处理靠 print 无断言 |
| ⑥可复现性 | 1 | xenium_benchmarking.yml 完整 conda+pip 版本锁（python 3.7.13，pip 段逐包==）✓；Zenodo DOI 数据三件 ✓；但 xb/*.py 全文无 random_state/seed（grep 证实），leiden/UMAP 不可复现 ✗ |
| ⑦验证纪律 | 1 | readthedocs 文档站 + 端到端示例数据 DOI 是验证友好设计；无测试无 CI；notebook 即"计划-验证痕迹" |

**总分 6/14**

## 可搬运模式

- PATTERN-001（QC 指标库单指标单函数：_quality_metrics.py 是主原型，SpatialQM 为对照）
- PATTERN-009 候选未收录：自适应分辨率循环（preprocessing.py:72-88）思路可用但实现带 bug，且需 seed，暂不登记（宁缺毋滥）

## 坑与限制（实读发现）

1. `xb/__init__.py` 语法非法（`import .`），pip install -e . 后 `import xb` 即报 SyntaxError——所有 notebook 依赖的包入口实际是坏的，只能靠 `from xb.preprocessing import *` 这类绕过 __init__ 的子模块导入存活【待补充：CI 上是否曾验证过完整安装】。
2. preprocess_adata 把分析、绘图、写盘耦合在一函数（preprocessing.py:98-166），画几十张 pdf，重跑代价大；save 路径默认字符串 'output_path'（preprocessing.py:98 参数默认值即路径占位）。
3. main_preprocessing 面向模拟实验，与主流程 preprocess_adata 并行存在两套预处理逻辑，参数含义不同（target_sum=100 vs clustering_params 字典）。
4. Banksy_py 子模块未初始化，克隆后域识别 Banksy 线不可直接运行。
5. 无任何测试/CI，靠 notebook 执行记录背书。

## 一句总评

科学组织（任务编号 notebook + 端到端编排 + 统一 AnnData 契约）是五仓里最值得学的 pipeline 雏形，但包级工程卫生（坏 __init__、代际文件堆积、无 seed）拖到及格线下。
