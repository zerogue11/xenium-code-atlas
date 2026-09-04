# 精读笔记 · ding-lab__mushroom

- repo: ding-lab/mushroom
- 来源文献: LIT-019; LIT-071（3D Imaging and Multimodal Spatial Characterization of the Precancer-to-Cancer Transition in Breast and Prostate）
- 锁定SHA: dc3598950fd233f2255a8e53006c915cc425a4a7（2025-07-31，README 更新）
- 复核分类: 分割/ISS 工具链（S 级）——3D 连续切片配准 + 多模态整合；953MB 克隆中 notebooks/old、examples_old、manuscript/submission* 为历史版本，本次只读主包 `mushroom/`（约 5200 行）与 tutorials 目录清单

## 代码结构走读

目录 → 模块职责（实读）：
- `mushroom/mushroom.py`（867 行）：两个核心类。`Mushroom` = 顶层编排（按 dtype 拆分 sections → 每种数据模态一个 `Spore` → 统一网格分辨率 → z 插值成体积 → 跨模态整合）；`Spore` = 单模态模型封装（SAE + lightning Trainer + 聚类/概率/重缩放）。
- `mushroom/data/`：多平台统一接入口。`datasets.py`（579 行）按 dtype 分发 `get_*_section_to_img`（xenium/cosmx/visium/he/multiplex/points 六种），把各家数据统一为"网格化表达图像"喂给 SAE；`xenium.py`（113 行）演示 Xenium 接入：cell_feature_matrix.h5 + cells.csv.gz + morphology_focus.ome.tif → adata → `to_multiplex()`。
- `mushroom/model/sae.py`（336 行）：SAE 网络——ViT encoder + slide/dtype embedding + 分级 codebook（num_clusters=(8,4,2) 层级）+ 每 dtype 独立 decoder，gumbel_softmax 量化出层级 cluster，loss = 重构 MSE + 跨切片邻域一致性 CE（VariableScaler 逐 ramp 邻域权重）。
- `mushroom/model/model.py`（238 行）：`LitSpore`（LightningModule 包装 SAE、输出展平重建整图）、`WandbImageCallback`、`VariableTrainingCallback`（空壳）。
- `mushroom/model/integration.py`（155 行）：跨模态 3D 整合核心——各 dtype 概率体积平滑 → 分块 einsum 取联合 argmax 合并 → 以 dtype 间 cluster 强度距离建 igraph → leiden 合并 → `merge_labels_by_contact` 清理小标签。
- `mushroom/registration/bigwarp.py`（342 行）：读 BigWarp 导出的位移场（ddf），torch 重采样 `warp_image`/`warp_pts`，把 HE/multiplex 对齐到统一坐标。
- `mushroom/visualization/`（517+317+215+135+103 行）：napari viewer、聚类/概率/体积展示辅助。
- 入口链（notebooks/tutorials 三个 ipynb）：data_preperation_and_registration（bigwarp 手动配准）→ mushroom_tutorial（Mushroom.from_config → train → embed_sections → generate_interpolated_volumes）→ output_analysis。

## 关键脚本清单

| 文件 | 行数 | 一句话 |
|---|---|---|
| mushroom/mushroom.py | 867 | Mushroom/Spore 双层编排：dtype 分治训练、统一网格、z 插值、持久化 |
| mushroom/data/datasets.py | 579 | 六平台→统一网格图像的分发层，含训练/推理 Dataset 与 collate |
| mushroom/model/integration.py | 155 | 平滑→分块联合 argmax→igraph+leiden 的跨模态体积合并 |
| mushroom/model/sae.py | 336 | ViT+分级 codebook SAE，gumbel 量化产生层级空间域 |
| mushroom/model/model.py | 238 | LitSpore：lightning 训练/预测步与输出重拼装 |
| mushroom/registration/bigwarp.py | 342 | BigWarp 位移场读取与 torch 图像/点云形变 |
| mushroom/data/xenium.py | 113 | Xenium 标准输出→adata→网格表达图像的接入口 |

## 技术路线还原（勾选固定清单，按实际顺序）

1. 数据读取（data/datasets.py 六平台分发；xenium.py:18-111 读 h5+cells+形态图）
2. 归一化（datasets.py:37 generate_norm_transform；xenium.py:109-110 sc.pp.log1p）
3. 降维（sae.py ViT encoder + codebook 量化，表达/多通道 → 64 维 codebook）
4. 聚类（sae.py:218-234 gumbel 量化出 (8,4,2) 层级 cluster；integration.py:149 leiden 跨模态合并）
5. 空间邻域/域（Spore 输出即 50 μm 网格空间域图；sae.py:296-314 邻域一致性 loss）
6. 配准/3D（registration/bigwarp.py 位移场形变 + mushroom.py:300-363 z 轴线性/label_gaussian 插值成体积）
7. 多样本整合（integration.py:88-156 多 dtype 体积 leiden 整合为 integrated volume）
8. 绘图（mushroom.py:365-835 display_* 系列；visualization/）
9. 导出（mushroom.py:210-278 config.yaml + outputs.pkl）

未做：质控QC、HVG、注释、去卷积、细胞通讯、亚细胞、空间统计（均不在本仓范围）。

## 工程审计表（7 维，0-2 分）

| 维度 | 分 | 证据 |
|---|---|---|
| 职责单一/模块化 | 2 | data/model/registration/visualization 四子包各司其职；Mushroom/Spore 分层（mushroom.py:75,481） |
| 命名规范 | 1 | dtype/sid/agg 缩写密集；拼写错误 `'intergrated'`（mushroom.py:392）；`Mushroom.assign_pts` L448 与 `Spore.assign_pts` L854-856 同名方法缩放方向相反（乘 scaler vs 除 scaler），易误用 |
| 安全性 | 1 | 无凭据泄漏；但 wandb project 'portobello' 个人项目名写进默认配置（mushroom.py:68），路径基本参数化 |
| 最简化 | 1 | 大量注释掉的旧代码（sae.py:121-142、mushroom.py:444-447）；`VariableTrainingCallback.on_train_epoch_end` 全注释空壳（model.py:74-87） |
| 逻辑健壮性 | 2 | assert 校验（mushroom.py:282,399,851）；找不到 morphology 图 raise RuntimeError（data/xenium.py:63-68）；单切片自动补 dup 再回退（mushroom.py:491-499） |
| 可复现性 | 1 | config.yaml+outputs.pkl 快照协议 + checkpoint 保存（mushroom.py:210-278,578-584）是亮点；但全仓无任何 seed 控制（grep manual_seed/random.seed 为空），训练不可精确复现 |
| 验证纪律 | 1 | 无测试/CI；靠 tutorials + manuscript submission_v1/v2 notebook 链接做人工复现（README.md:31-40） |

总分：9/14

## 可搬运模式

- PATTERN-011 dtype 分治 Spore + 统一网格 3D 整合
- PATTERN-012 config.yaml + outputs.pkl 快照/恢复协议

## 坑与限制

- 训练无 seed，复现只能靠 checkpoint；README 自述 "Under active development / API subject to change"。
- `Mushroom.assign_pts`（L448 乘）与 `Spore.assign_pts`（L854-856 除）缩放语义相反，外部调用极易弄反。
- `display_clusters` L392 `'intergrated'` 拼写错误使该条件永不成立（好在前 L377 已拦截 integrated 分支，属死代码级 bug）。
- integrate_volumes 的 `cluster_dists` 是 O(dtype²×cluster²) 全距离矩阵 + 全对 node 图（integration.py:124-140），ROI 大时 leiden 边数爆炸（n_labels² 条边先全建再过滤）。
- Xenium 接入假设 `spot_diameter_fullres: 10.`（xenium.py:101）为占位值，直接搬用会引入尺度误差。
- lightning 版本混用：model.py:5 import `pytorch_lightning.utilities.types` 但其余用 `lightning.pytorch`（新版命名），装旧版 pytorch_lightning 才不炸。

## 一句总评

科研 codebase 里少见的"多模态统一网格 + 层级量化 + 图整合"完整闭环，架构分层和持久化协议值得抄，但无 seed、拼错名、死代码说明它仍是活跃开发的实验室代码而非库。
