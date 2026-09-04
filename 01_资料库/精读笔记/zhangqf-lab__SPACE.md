# 精读笔记 · zhangqf-lab__SPACE

- repo: zhangqf-lab/SPACE（LIT-016，已改判 P3）
- 来源文献: SPACE — SPatial transcriptomics Analysis via Cell Embedding（PyPI space-srt 0.7.0）
- 锁定SHA: 6fc15f9eb84267e8eaa2f2a2c34f1508a0d5db09
- 复核分类: 注释/图谱/生态位组 · S 级 · PyG 图自编码器包（MIT，pyproject.toml classifiers）
- 精读日期: 2026-09-04（一期精读批次C）

## 代码结构走读

- `space/`（5 文件共 838 行）：
  - `layer.py`(61行)：`GAT_Encoder` = 2 层 GATv2Conv(hidden 128×128, heads=6) + 第 3 层 GATv2Conv 降维到 **latent_dim=10（硬编码，layer.py:21）**，forward 返回 z 与三层 attention weights。
  - `model.py`(68行)：`SPACE_Graph(GAE)` 用 InnerProductDecoder 图损失 + `decoder_x` MLP 特征重建（MSE/BCE 二选一，model.py:23-36）；`graph_loss` 内联负采样（model.py:46-58）。
  - `train.py`(165行)：训练循环 + EarlyStopping + 学习率衰减 + loss 曲线 PDF 导出。
  - `function.py`(169行)：唯一用户入口 `SPACE(adata,...)`——建图→Data 打包→RandomLinkSplit→训练→回载 checkpoint→写 `adata.obsm['latent']`→neighbors/UMAP→存 h5ad（function.py:28-168）。
  - `utils.py`(381行)：`graph_construction` KNN 建图、`celltype_connectivity`（niche-细胞类型连通性 bootstrap）、`mad_gap`、`load_SPACE_model` 推理复用、`extract_attention`。
- `scripts/`：3 篇 NSCLC/mouse 应用 notebook + `CCI/`（CellChat 对接 2 篇）。
- 入口链：`SPACE()` 一函数封全流程；`__init__.py` 只导出 `SPACE`。

## 关键脚本清单

| 文件 | 一句话 | 行数 |
|---|---|---|
| space/function.py | 全流程入口：建图→训练→latent→UMAP→h5ad | 169 |
| space/train.py | 训练循环+早停+损失分解（图损失 a=0.5，特征损失×10） | 165 |
| space/layer.py | GATv2 编码器，latent=10 硬编码 | 61 |
| space/model.py | GAE 封装：内积解码图损失+MLP 特征损失 | 68 |
| space/utils.py | KNN 建图/mad_gap/celltype_connectivity/模型复用 | 381 |

## 技术路线还原（勾选实际步骤，按序）

[数据读取(adata.obsm['spatial']+adata.X 由用户备好), 归一化(BCE 时 MaxAbsScaler，function.py:104-106), 降维(GAE latent 10), 聚类(notebooks 内 leiden on latent), 空间邻域/域(KNN 图 k=20 + SES 组织模块), 细胞通讯(scripts/CCI 对接 CellChat), 绘图(loss 曲线+UMAP), 导出(adata.h5ad+model.pt+attention 权重)] — 共 8 步
未做：质控QC、HVG、注释、去卷积、亚细胞、空间统计、配准/3D、多样本整合（单切片设计）。

## 工程审计表（0-2 分/维，共 14）

| 维度 | 分 | 证据 |
|---|---|---|
| ①职责单一 | 2 | model/layer/train/function/utils 五层分明；入口唯一 |
| ②命名规范 | 1 | 类名清楚；但 layer.py:54-62 `InnerProduct` 死类（model 实际用 PyG InnerProductDecoder） |
| ③安全性 | 2 | 无硬编码路径，outdir 参数化（function.py:84） |
| ④最简化 | 1 | train.py:107 **每个 epoch 重建 Adam**（动量清零、adjust_learning_rate 失效）；train.py:132-140 注释死代码；EarlyStopping.loss_min 存而不判（train.py:41,72） |
| ⑤健壮性 | 1 | NaN 即停（train.py:46-47）；但 latent_dim=10（layer.py:21）、特征损失×10（train.py:119-121）、heads 默认 6 全硬编码 |
| ⑥可复现性 | 2 | 全套 seed：function.py:72-82（np/torch/random/cudnn.deterministic）、train.py:78-86、model.py:15,20 |
| ⑦验证纪律 | 0 | 无测试无 CI；scripts/ notebook 即手工验证 |

**总分 9/14**

## 可搬运模式

- PATTERN-031 GATv2 图自编码器组织域发现（KNN 图+双损失 GAE+attention 可导出）

## 坑与限制（实读发现）

1. **train.py:107 每 epoch `torch.optim.Adam(...)` 重建**：Adam 状态每轮清零，`adjust_learning_rate` 设的 lr 随即被新 optimizer 的 init_lr 覆盖——训练动态与论文描述可能不符；搬运时必须提到循环外。
2. latent 10 维、hidden 128、×10 损失权重均不可调，需要改包才能扫参（与多候选并行纪律冲突）。
3. `space-srt` 0.7.0 依赖 squidpy/scanpy 但 requirements.txt 无版本上界，2026 年环境安装大概率版本漂移。
4. 建图 `graph_construction(adata.obsm['spatial'],...)` 默认欧氏 KNN，不支持样本内分块（多样本会跨切片连边），多样本需手工按 sample 切开分别跑。
5. 已改判 P3：方法上被 CellCharter/Nichecompass 类覆盖，主要价值是"极简 GAE 包结构"参考。

## 一句总评

500 行内讲清"GAE 怎么做组织域"的最小可用包，seed 纪律是亮点；但优化器循环 bug、硬编码超参与无测试使其只宜当教学/骨架参考，不宜直接进生产链。
