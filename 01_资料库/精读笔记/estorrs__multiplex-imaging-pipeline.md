# 精读笔记 · estorrs/multiplex-imaging-pipeline

- repo: https://github.com/estorrs/multiplex-imaging-pipeline
- 来源文献: LIT-019 / 多重免疫荧光成像处理管线（README 未绑特定期刊，作者 Erik Storrs，WUSTL ding-lab 生态，与 3d-analysis/mushroom 同源）【待补充期刊卷期】
- 锁定SHA: `c351da1d41e284eef2f732b3553e5602438ed978`（2025-09-08，v0.3.0）
- 复核分类: 图像/管线组 · mip CLI 四模式（+show-channels 共 5 子命令）多重成像处理管线 · CWL + docker · MIT（setup.py classifiers）

## 代码结构走读（实际读了什么）

包体 1903 行 + CWL 层 + docker 层 + 集群层：
- `multiplex_imaging_pipeline/multiplex_imaging_pipeline.py`（208 行）：argparse 单入口，`mode` choices 锁定五种任务（:20-24）：`make-ome`（平台分支装载 qptiff/codex/raw tif→HTAN ome.tiff 金字塔）、`segment-ome`（deepcell Mesmer 切块分割，split-size 控内存）、`generate-spatial-features`（逐细胞强度+门控分型→AnnData）、`generate-region-features`（区域掩码+形态学特征）、`show-channels`。segmentation 为可选依赖：`importlib.util.find_spec("deepcell")` 探测后再导入（:16-17）。
- `ome.py`（313 行）：三个平台装载器 `generate_ome_from_tifs/:71`、`generate_ome_from_qptiff/:152`、`generate_ome_from_codex_imagej_tif/:223`，统一走 `write_HTAN_ome`（:48，多分辨率金字塔）。
- `spatial_features.py`（276 行）：`generate_feature_table`（:134，regionprops 逐细胞 + 每通道均值强度）、`auto_calculate_threshold`（:122，自动阈值）、`gate_cells`（:210，声明式门控→细胞类型标注）、`get_spatial_features`（:256，总装配→AnnData）。文件头 `DEFAULT_GATING_STRATEGY`（:20-120）内置上皮/T/B/巨噬/内皮等 10+ 门控 JSON。
- `region_features.py`（267 行）：`fast_expand_labels/fast_shrink_labels`（:24/:35，距离扩张收缩）、`get_morphology_masks`（:66，肌上皮/边界带二环掩码）、`generate_region_mask`（:175，多 marker 阈值布尔组合）、`get_region_features`（:190）。
- `region_classification.py`（184 行）：区域分类器，**CLI 未挂接**（choices 里没有），属半成品。
- `utils.py`（383 行）：`extract_ome_tiff`（:139，flexibility 参数控制严格度）、伪彩/合并通道/标注保存等可视化工具。
- CWL 层（cwl/）：8 个子工作流 + 每个配 `template.*.yaml` 输入模板；主链 `full_imaging_workflow.cwl`：image_preprocessing → image_processing_to_thresholds，输出 ome_tiff/labeled_*/spatial_features_*/region_features 等固定契约。
- 运行层：`docker/Dockerfile`（ubuntu18.04+miniconda+deepcell+wombat）；`multiplex_imaging_pipeline/compute1/generate_run_commands.py`（142 行，生成 WashU compute1 LSF 集群批量命令）；`submodules/omero-wrapper`（OMERO 桥接）。

## 关键脚本清单

| 文件 | 行数 | 一句话 |
|---|---|---|
| multiplex_imaging_pipeline.py | 208 | argparse 五模式分派主入口 |
| spatial_features.py | 276 | 逐细胞特征表 + 声明式门控分型 + AnnData 装配 |
| region_features.py | 267 | 区域掩码生成（阈值组合/距离扩张）与区域级特征 |
| ome.py | 313 | 三平台图像格式→HTAN ome.tiff 金字塔 |
| utils.py | 383 | ome.tiff 抽取与可视化工具箱 |
| cwl/full_imaging_workflow.cwl | - | 端到端 CWL 编排（预处理→分割→双特征） |
| compute1/generate_run_commands.py | 142 | HPC 集群命令批量生成器 |

## 技术路线还原（固定清单勾选）

1. **数据读取**（qptiff/codex tif/raw tif 目录→ome.tiff，ome.py）
2. （分割：deepcell Mesmer 细胞/核标签图——固定清单无此项，作为亚细胞级分割介于数据读取与特征间）
3. **注释**（gate_cells 门控→细胞类型，spatial_features.py:210）
4. **空间邻域/域**（region 掩码 + myoepi_dist/boundary_dist 距离带，region_features.py:66）
5. **空间统计**（Polsby-Popper 形态学指数、marker 强度/阳性分数，region_features.py:51/:125/:140）
6. **绘图**（utils.py 伪彩/合并/标注图）
7. **导出**（AnnData h5ad + txt + 标注图）

**骨架步骤数：6**（数据读取/注释/空间邻域域/空间统计/绘图/导出）。

## 工程审计表（7 维 × 0-2，共 10/14）

| 维度 | 分 | 证据 |
|---|---|---|
| ①职责单一/模块化 | 2 | CLI 单入口 5 模式分派（multiplex_imaging_pipeline.py:20-24,181）；7 个业务模块 + CWL 8 子工作流，层界清楚 |
| ②命名规范 | 2 | 模式名 make-ome/segment-ome/generate-*-features 动宾一致；函数名全 snake_case 语义明确 |
| ③安全性 | 2 | 无凭据/硬编码路径；路径全走 CLI 参数 |
| ④最简化 | 1 | region_classification.py 已写但 CLI 未挂接（choices 缺失）；主入口注释掉的参数块（:60-63）；README 自述两个 feature 模式 "may not work as intended" |
| ⑤逻辑健壮性 | 1 | deepcell 缺失时优雅跳过导入（:16-17）；extract_ome_tiff 有 strict/flexible 模式（utils.py:139）；但 make-ome 无输入存在性校验，gate 阈值通道缺失静默 NaN |
| ⑥可复现性 | 1 | CWL+template yaml 输入契约是亮点；但 docker/Dockerfile:11-12 pip 裸装不锁版本、setup.py 依赖不锁，镜像重建漂移风险大 |
| ⑦验证纪律 | 1 | examples/ + template 提供样例输入；无测试无 CI；README 明示两模式不可靠 |

## 可搬运模式

- PATTERN-038：声明式门控策略的细胞/区域分型（spatial_features.py DEFAULT_GATING_STRATEGY + gate_cells）。

## 坑与限制（实读发现）

- `generate-region-features`/`generate-spatial-features` 官方自述不稳定（README:8-9），使用前需自行验证；region_classification 完全未接线。
- 门控默认阈值 `DEFAULT_PIXEL_FRACTION=.05` 是"每通道 Top5% 阳性"的经验值，跨 panel/跨染色的鲁棒性无保证；通道名硬编码（Pan-Cytokeratin 等），panel 不同必须整套重写门控 JSON。
- deepcell/Mesmer 依赖极重（TF1 系），docker 外安装极易失败（README 用大段文字警告）。
- CWL 层与 Python CLI 层是两套参数体系（CWL 包一层再调 CLI），改参数要动两处。
- ome.py 输出像素 uint8 归一，dynamic range 压缩信息无记录。
- 与 3d-analysis 同作者但无共享代码（重复实现了 listfiles 等工具函数），两仓代码无互相 import。

## 一句总评

"CLI 模式分派 + 平台分支装载 + 声明式门控 + CWL 契约"四件套是本仓的真金，门控 JSON 直接可搬进 A7 图像-表型模块；但 feature 层半成品状态与不锁版本的 docker 拉低了成色。
