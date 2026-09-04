# 精读笔记 · broadinstitute__ist_benchmarking

- repo: broadinstitute/ist_benchmarking
- 来源文献: LIT-086（"Systematic benchmarking of imaging spatial transcriptomics platforms in FFPE tissues"，Broad Huan Wang 等）
- 锁定SHA: abb4acc39c68b16fdaf6909f1639947a55173182（2025-08-13 "protein validation"）
- 复核分类: S 级 / 基准-质控组 / notebook 流 + 工具模块（15MB，纯代码，数据走 GCS bucket）
- 语言与体量: Python；14 个 notebook + constants.py(271) + st_utils.py(852) + seg_eval.py(499) + depreciated_st_utils.py(121)

## 代码结构走读

```
constants.py (271行)   全局常量中心：平台×面板命名映射(CORRECT_PLATFORM_PANEL)、TMA 名映射、
                       Okabe-Ito 配色字典、SAMPLES 清单、matching_cores 匹配核列表
st_utils.py  (852行)   26 个函数：data_loader 三平台装载、calculate_qc_metric、name_parser、
                       standardize_data、GIS/几何辅助(df_2_gdf)、save_html 归档、可视化
seg_eval.py  (499行)   分割评估：ground truth 多边形 vs 各平台 mask 的 TP/FN/FP→precision/recall/F1/IoU
depreciated_st_utils.py(121行) 显式归档的弃用函数
00_copy_data / 00_setup_and_data_example        数据自 GCS bucket 拉取 + 数据样例走读
01_data_generator (no need to run)              一次性构建 cell_level/transcript_level/gene_level 中间层
02_FDR / 02_panel_to_panel / 02_specificity     FDR（blank/负控）、面板-面板可重复性、特异度/灵敏度
03_gene_by_gene / 04_tissue_marker              逐基因相关、组织 marker 富集 sanity check
06_single_cell_metrics / 07_coexpression        转录本每细胞/基因每细胞热图、disjoint marker 共表达
08_segmentation_evaluation / 09_cell_area / 10_cell_count   分割精度、细胞面积、细胞数
11_protein_validation / 12_gene_length          CD274 vs PD-L1 蛋白验证、基因长度偏倚
```

入口链：没有单一入口，14 步即目录名序列。每步开头 `wd=os.getcwd()` + `from st_utils import …` + `from constants import …`，中间产物按 `data/<层名>/` 与 `figures/<图号>/` 落盘，各块用 `if not os.path.exists(...)` 幂等守卫。实际通读：readme、constants.py 头 60 行、st_utils.py 函数清单+calculate_qc_metric/data_loader/name_parser/standardize_data/save_html 全文、seg_eval.py:61-122 全文、14 个 notebook 逐单元首行抽取、02_specificity notebook 核心单元全文。

## 关键脚本清单

| 文件 | 行数 | 一句话 |
|---|---|---|
| st_utils.py:201 data_loader | ~107 | xenium/merscope/cosmx 三模态→统一 AnnData+坐标 DataFrame（PATTERN-007 原型） |
| st_utils.py:62 calculate_qc_metric | ~11 | Squidpy QC 指标 + min_counts/min_cells 过滤（含一行 bug，见坑1） |
| st_utils.py:725 standardize_data | ~30 | 标准化对照链：counts 层→归一→log→PCA→UMAP→leiden→双图落盘 |
| seg_eval.py:61-122 | ~60 | TP/FN/FP 几何判定（gpd.sjoin 质点在 mask 内）→precision/recall/F1/IoU |
| st_utils.py:619 name_parser | ~11 | 从样本名解析 platform/panel/tma 三元组（下标脆弱） |
| st_utils.py:631 save_html | ~20 | jupyter nbconvert 把每步 notebook 归档为 html |
| constants.py | 271 | 平台命名/配色/TMA 映射/匹配核清单集中管理 |

## 技术路线还原（勾选自固定清单，按实际顺序）

1. 数据读取（data_loader 三平台归一 + 01 步建 cell/transcript/gene 三级中间层）
2. 质控QC（calculate_qc_metric 过滤；02_FDR blank/负控假阳性率；specificity/sensitivity 相对策划基因清单与匹配核）
3. 归一化（standardize_data: normalize_total→log1p）
4. 降维（PCA→UMAP）
5. 聚类（leiden resolution=1.0）
6. 绘图（每 notebook 大量 matplotlib/plotly/seaborn，图号即目录）
7. 导出（data/* 中间层 csv/parquet、figures/Fig_*、save_html 的 html 归档）

未做：HVG（standardize_data 无 highly_variable_genes，全 panel 进 PCA——面板基因数少故可行）、注释、去卷积、空间邻域/域、细胞通讯、亚细胞、空间统计（Moran 类）、配准/3D。分割评估（08）与蛋白验证（11）为清单外的基准特有步骤。

## 工程审计表（7 维，0-2 分）

| 维度 | 分 | 证据 |
|---|---|---|
| ①职责单一/模块化 | 1 | notebook=步骤、utils=函数、constants=配置三层分离清晰；但各 notebook 仍内嵌大量一次性业务逻辑（02_specificity 内联 load/匹配核逻辑），模块化是"半成品" |
| ②命名规范 | 1 | 常量大写集中（constants.py:33 CORRECT_PLATFORM_PANEL）、函数动词开头；depreciated（应为 deprecated）拼写错、vecterize/vectorize 不一致（st_utils.py:32 vs 832） |
| ③安全性 | 2 | wd=os.getcwd() 全 14 notebook 相对路径（无硬编码盘符）；GCS bucket 为公开数据地址无凭据 |
| ④最简化 | 1 | 弃用代码显式隔离进 depreciated_st_utils.py 而非删除（可辩护的取舍）；.DS_Store 入库多处；部分图保留 "plot with plotly (depreciated)" 双实现痕迹 |
| ⑤逻辑健壮性 | 1 | seg_eval 指标全带除零守卫（seg_eval.py:69-79）；但 calculate_qc_metric 把 min_counts 误传给 filter_genes 的 min_cells（st_utils.py:69-70）；name_parser 靠 split 下标（st_utils.py:619-628）样本名一变即错位 |
| ⑥可复现性 | 2 | requirements.txt 精确锁版（geopandas==0.13.0/scanpy==1.9.3/squidpy==1.3.1）；leiden resolution 显式 1.0；幂等检查点保证中间层可重建；无随机重步骤，seed 缺失影响小 |
| ⑦验证纪律 | 1 | 无 CI/测试；但 if-not-exists 幂等块 + data/ 中间产物留痕 + save_html 每步归档构成"执行即验证"痕迹链 |

**总分 9/14**

## 可搬运模式

- PATTERN-006（幂等检查点 notebook 流）
- PATTERN-007（跨平台数据装载归一层 + constants 常量中心）
- PATTERN-008（几何 ground truth 分割评估）

## 坑与限制（实读发现）

1. st_utils.py:70 `sc.pp.filter_genes(adata, min_cells=min_counts)`——基因过滤阈值错用了细胞 counts 阈值（10 而非 5），且函数 docstring 未声明此行为；搬运时需改为独立参数。
2. "no_need_to_run" 命名（01/02）靠注释文字区分一次性步骤与常规步骤，易被误跳/误跑。
3. 01 步硬编码年度分支（`if '2024' not in SAMPLE`，st_utils.py:217），跨年度数据混合装载需人工核对 parquet 字符串解码差异。
4. specificity 定义依赖每平台每面板的策划基因清单（data/gene_lists/<platform>_<panel>.csv），外部复用需自备等价清单。
5. notebook 体量与内联逻辑使其难以被程序化调用——它本质是"分析报告流水线"，不是可 import 的库。

## 一句总评

五仓中工程最规范的一仓：步骤化 notebook + 幂等落盘 + 常量中心 + 精确版本锁可直接映射为整合 pipeline 的"基准步骤手册"，两处小 bug（filter_genes 传参、name_parser 脆弱）搬运时修即可。
