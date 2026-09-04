# 精读笔记 · Moldia__ISS_decoding

- repo: Moldia/ISS_decoding
- 来源文献: LIT-017（ISS 空转三件套的中段：tile 图 → starfish/SpaceTx 格式 → 像素/spot 解码为基因）
- 锁定SHA: 10b318e1d84c2f8210860aa313c9d675167ccf7c（2022-06-15，"Add files via upload"）
- 复核分类: 分割/ISS 工具链（S 级）——starfish 0.2.2 像素解码链；build/lib 与源码不同步，实读以 ISS_decoding/ 包内为准

## 代码结构走读

目录 → 模块职责（实读）：
- `ISS_decoding/SpaceTx_format.py`（169 行）：把 preprocessing 仓输出的 ReslicedTiles 组装成 starfish 可读的 SpaceTx experiment.json：`make_codebook_json`（L41-55，CSV 码本→json codebook）、`get_tilepos`（L57-63，读 tilepos.csv）、`make_spacetx_format`（L65-168，定义 ISSTile2D(FetchedTile)/TileFetcher 闭包类 + write_experiment_json + 末尾把 json 里的绝对路径前缀剥掉）。
- `ISS_decoding/decoding.py`（258 行）：`ISS_pipeline`（L41-137，单 FOV 主流程：DAPI/最大投影配准 LearnTransform.Translation→Warp→WhiteTophat 滤波→MatchHistograms 通道归一化→BlobDetector LoG 找 spot→PerRoundMaxChannel 或 MetricDistance 解码）；`QC_score_calc`（L139-159，逐 read 逐碱基 max/sum 质量）；`process_experiment`（L161-196，多 FOV 断点续跑：扫输出目录跳过已完成 FOV）；`concatenate_starfish_output`/`plot_starfish_output`。
- `ISS_decoding/qc_metrics.py`（146 行）：解码后 QC 与可视化——quality_per_gene/per_cycle 小提琴、compare_scores、plot_expression 空间散点、`filter_reads`（L130-146，按 quality/distance/radius/intensity 阈值过滤）。
- `ISS_decoding.ipynb`：入口，`make_spacetx_format` → `Experiment.from_json` → `process_experiment(exp_path='.../SpaceTX_format_5_cycles/experiment.json')` → `concatenate_starfish_output`。
- `decoding.yml`：starfish==0.2.2、python 3.7 全锁。

## 关键脚本清单

| 文件 | 行数 | 一句话 |
|---|---|---|
| ISS_decoding/decoding.py | 258 | 配准→滤波→归一化→LoG spot→PRMC/MD 解码的单 FOV pipeline |
| ISS_decoding/SpaceTx_format.py | 169 | ReslicedTiles+码本→SpaceTx experiment.json 组装器 |
| ISS_decoding/qc_metrics.py | 146 | 解码质量 QC 指标与过滤函数集 |
| ISS_decoding.ipynb | notebook | 串联三模块的运行入口 |
| decoding.yml | ~140 | starfish==0.2.2 版本锁环境 |

## 技术路线还原（勾选固定清单，按实际顺序）

1. 数据读取（SpaceTx_format.py:135 write_experiment_json；decoding.py:178 Experiment.from_json）
2. 配准（decoding.py:56-75 跨 round 平移配准+warp——注意这在固定清单里属于"配准/3D"的前置图像配准）
3. 归一化（decoding.py:85-90 MatchHistograms 通道/循环直方图匹配，或 ClipPercentileToZero）
4. 质控QC（decoding.py:139-159 QC_score_calc 逐碱基质量；qc_metrics.py filter_reads 阈值过滤）
5. 注释（严格说是 spot→target 解码，非细胞注释：decoding.py:106-124 PerRoundMaxChannel/MetricDistance）
6. 绘图（plot_starfish_output L217-257 全基因空间散点；qc_metrics 各 plot）
7. 导出（decoded.csv / spots_PRMC.csv，decoding.py:198-215）

补充：固定清单的"配准/3D"项本仓为 2D 图像配准（无 3D）。未做：HVG、降维、聚类、去卷积、空间邻域/域、细胞通讯、亚细胞、空间统计、多样本整合。

## 工程审计表（7 维，0-2 分）

| 维度 | 分 | 证据 |
|---|---|---|
| 职责单一/模块化 | 2 | format/decoding/qc 三模块分工清晰，notebook 只做串联 |
| 命名规范 | 1 | 函数名达意，但 plot_frequencies 里 `on='targets'` 与 groupby('fov') 计数错位（qc_metrics.py:76-83）；死代码无操作列表推导（decoding.py:149） |
| 安全性 | 1 | conversion=0.1625 硬编码默认（decoding.py:220）；比例尺魔数 615.3846（decoding.py:247）；无凭据泄漏 |
| 最简化 | 0 | decoding.py:1-39 头部 import 三次重复（ApplyTransform/Filter/FindSpots 等），`test = os.getenv("TESTING")` 定义两次且未用（L24,38）；直接 import starfish.core 私有 API（L22-25） |
| 逻辑健壮性 | 1 | 空结果防护（decoding.py:129-131）；FOV 断点续跑（decoding.py:181-190）；但 QC min() 对全 NaN 行无防护、KeyError 之外无异常设计 |
| 可复现性 | 2 | decoding.yml 锁 starfish==0.2.2/python==3.7.11 全链版本 |
| 验证纪律 | 0 | 无测试/CI；build/lib 内代码与 ISS_decoding/ 不同步（diff 确认 differ），包构建产物混入仓库 |

总分：7/14

## 可搬运模式

- PATTERN-017 FOV 幂等断点续跑（process_experiment 扫输出跳已完成）
- （coo 掩码交换模式登记在 postprocessing 仓笔记）

## 坑与限制

- starfish 0.2.2 是 2022 年已停更版本，且 `from starfish.core...` 三处私有 API import（decoding.py:22-25）在后续版本必炸——搬运需整体 pin 或改造。
- `ISS_pipeline` 配准默认 `register_dapi=True` 用 nuclei stain 对齐，但 `process_experiment` 默认 register=False/register_dapi=False（decoding.py:163-164），两处默认不一致，调用方易混淆。
- QC_score_calc 逐 read Python 双层循环（decoding.py:143-154），百万 read 级数据极慢，应向量化。
- plot_starfish_output 硬编码暗背景、白字、固定比例尺，出图不符合出版规范需重写。
- make_spacetx_format 末尾逐行文本替换剥路径前缀（SpaceTx_format.py:160-168）是脆弱 hack，依赖 write_experiment_json 的输出格式。

## 一句总评

starfish ISS 解码的最小可行参考实现，模块切分和断点续跑值得借鉴；但建立在私有 API + 停更依赖上，import 头部与构建产物混乱，属于"能跑一次"的一次性科研代码。
