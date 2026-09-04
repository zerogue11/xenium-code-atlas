# 精读笔记 · QuKunLab__SpatialBenchmarking

- repo: QuKunLab/SpatialBenchmarking
- 来源文献: Li, Zhang, Guo et al., "Benchmarking spatial and single-cell transcriptomics integration methods for transcript distribution prediction and cell type deconvolution", Nat Methods 2022（LIT-088 映射存疑已备注：此为独立 NM 2022 基准文，非 Moldia 仓同文）
- 锁定SHA: 3586b9d81c479f939aa40adedfe1c95c5b496bcb（2022-06-10 "update codes"）
- 复核分类: S 级 / 基准-质控组 / Python 包 Benchmarking + 每方法一包装脚本 + 驱动 notebook（克隆 113MB，FigureData 结果未深读）
- 语言与体量: Python+R 混合；Benchmarking/ 包 777 行；Codes/Deconvolution 10 个方法包装 522 行；两个 BLAST 驱动 notebook

## 代码结构走读

```
Benchmarking/SpatialGenes.py      (327行) GenePrediction 类：8 种插补方法分派 + 结果落盘
Benchmarking/DeconvolutionSpot.py (139行) Deconvolutions 类：10 种去卷积方法分派（含跨语言 subprocess）
Benchmarking/GenesMetrics.py      (311行) count 类：SSIM/PCC/RMSE/JS 四指标逐基因计算 + 3 种尺度变换
Benchmarking/data_downsample.py   (70行)  按细胞/按总量两种降采样（稀疏矩阵鲁棒性实验用）
Codes/Deconvolution/*_pipeline.{py,r,sh}  10 个方法各一文件，统一 CLI：sc输入 空间输入 celltype_key 输出目录
Codes/Impute/{LIGER,Seurat}.r     R 侧插补包装（被 Python 经 Rscript 调）
BLAST_GenePrediction.ipynb        驱动1：45 数据集 × 8 插补方法 × KFold(5) 并行基准
BLAST_CelltypeDeconvolution.ipynb 驱动2：去卷积基准
Extenrnal/SpaGE, SpaOTsc          vendor 进仓的上游库（含 doc/_build 全套）
FigureData/                       论文各图的指标 txt/csv 结果快照（45 数据集 × 8 方法）
```

入口链：BLAST notebook 逐数据集读三件套（RNA tsv / spatial tsv / 坐标 tsv）→ KFold 切 train/test 基因 → `multiprocessing.Pool(10)` 按 fold 并行调各方法函数 → 结果 csv 落盘 → `GenesMetrics.count` 类算 SSIM/PCC/RMSE/JS → FigureData 快照。去卷积线：`Deconvolutions.Dencon(Methods)` 分派，Python 方法进程内跑、R 方法经 subprocess 调 *_pipeline.r，统一产出 *_result.txt。实际通读：SpatialGenes.py 类+Imputing 全文、GenesMetrics.py 头 90 行+count 类、Tangram_pipeline.py 全文、DeconvolutionSpot.py docstring 段、BLAST notebook 代码单元。

## 关键脚本清单

| 文件 | 行数 | 一句话 |
|---|---|---|
| Benchmarking/SpatialGenes.py:34 GenePrediction | ~250 | 插补基准调度类：构造时读三件套，每方法一个 *_impute() |
| Benchmarking/SpatialGenes.py:282 Imputing | ~45 | if "tool" in need_tools 分派器（PATTERN-004 原型） |
| Benchmarking/GenesMetrics.py:124 count | ~140 | 逐基因四指标评估器，per-gene 输出 tidy 表 |
| Benchmarking/GenesMetrics.py:18 cal_ssim | ~35 | 手写 SSIM（带形状断言） |
| Codes/Deconvolution/Tangram_pipeline.py | 46 | 统一 CLI 契约的 Tangram 包装：rank_genes_groups 取 top200 marker→map_cells_to_space |
| Benchmarking/data_downsample.py | 70 | 稀疏性压力测试的两种降采样 |
| BLAST_GenePrediction.ipynb | — | KFold(5)+Pool(10) 的跨数据集驱动（PATTERN-005 原型） |

## 技术路线还原（勾选自固定清单，按实际顺序）

1. 数据读取（三件套 tsv/h5ad/h5Seurat 统一进类构造器）
2. 去卷积（10 方法：Cell2location/DestVI/RCTD/SPOTlight/STRIDE/Seurat/SpatialDWLS/Stereoscope/Tangram/DSTG）
3. 绘图（GenesMetrics.py:263 plot_boxplot 汇总箱线）
4. 导出（每方法每数据集 *_impute.csv / *_result.txt / *_Metrics.txt）

未做：质控QC（仅基因级 sum/var≠0 过滤，不足称 QC）、归一化（仅方法内部各自处理）、HVG/降维/聚类/注释（celltype 为外部输入）、空间邻域/细胞通讯/亚细胞/空间统计/配准/多样本整合（跨数据集批跑≠整合）。清单外核心步骤：基因插补基准（8 方法）、KFold CV、降采样模拟——此仓本质是"整合方法基准"而非 ST 分析 pipeline，清单命中少属正常。

## 工程审计表（7 维，0-2 分）

| 维度 | 分 | 证据 |
|---|---|---|
| ①职责单一/模块化 | 2 | 三层分工干净：方法包装（每方法一文件/一函数）→ 调度类 → 指标类；数据/代码/结果三分离（FigureData 快照独立） |
| ②命名规范 | 1 | DeconvolutionSpot/Dencon/Extenrnal 三处拼写错误；*_pipeline 后缀统一是加分项 |
| ③安全性 | 1 | os.system('Rscript ...' + 字符串拼接传参)（SpatialGenes.py:318-326），路径含空格即碎；无凭据 |
| ④最简化 | 0 | SpaOTsc doc/_build 全套 HTML/LaTeX 入库、__pycache__ ×3 代入库、113MB 大半是 vendor+结果；notebook 内联重复实现包函数（BLAST notebook 单元4 重写 SpaGE_impute） |
| ⑤逻辑健壮性 | 1 | outdir 拼接漏 "/"（SpatialGenes.py:293,317，gimVI/stPlus 结果写到 outdir 同级目录外）；加分项：impute_count.fillna(1e-20)（GenesMetrics.py:151）、cal_ssim 断言（:21-22）、指标除零由 scipy 兜底 |
| ⑥可复现性 | 1 | README 逐方法给精确版本号（Cell2location 0.6a0、scvi-tools 0.11.0 等）+ Benchmarkingenvironment.yml ✓；但 KFold 无 seed、novoSpaRc/Tangram 随机初始化无 seed，fold 划分不可复现 ✗ |
| ⑦验证纪律 | 1 | 无 CI 无测试；FigureData/ 保留 45 数据集全量指标 txt 作为可对照的验证快照，间接可校验重跑结果 |

**总分 7/14**

## 可搬运模式

- PATTERN-003（统一 CLI 契约的多方法包装器）
- PATTERN-004（类内方法名分派调度器）
- PATTERN-005（KFold+进程池并行基准评估）

## 坑与限制（实读发现）

1. outdir 路径 bug 意味着 gimVI/stPlus 的结果文件历史上落在 `outdir` 字符串拼接后的兄弟路径，迁移复跑时注意找文件位置。
2. 跨语言方法经 os.system 走全局 R 环境，与 conda 声明的隔离环境互相矛盾（R 包版本全靠 README 口头锁定）。
3. 指标对齐假设 raw 与 impute 列序完全一致（count 类不做列名对齐），换数据需自查。
4. 四种 scale（scale_max/z_score/plus/无）的选择散在各 metric 方法默认参数里，比较前必须弄清每个指标用了哪种尺度变换。
5. 该仓回答"哪个插补/去卷积方法好"，但其结论建立在无 seed 的 KFold 上，单次复跑分值会有波动。

## 一句总评

"每方法一包装 + 类调度 + 指标类 + 结果快照"的四层基准骨架是本计划整合 pipeline 基准模块最直接的模板，工程粗糙点集中在路径拼接与拼写，均可在搬运时一次性修掉。
