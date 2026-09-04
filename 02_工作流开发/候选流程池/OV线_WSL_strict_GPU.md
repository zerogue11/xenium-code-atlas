# 候选流程登记卡 · OV + WSL strict GPU 线

| 项 | 内容 |
|---|---|
| 名称 | OV + WSL strict GPU V1（omicverse GPU 规模化工作流） |
| 位置（指针，不复制） | `F:\xenium数据\ov工作流测试`（含全盘最完整的 `AGENT.md` 项目规范） |
| 技术栈 | omicverse 2.2.1rc1（本地源码 + 2 处补丁）+ scanpy 1.12.1 + PyTorch cu128 + RAPIDS singlecell 0.15.1（cuml/cugraph/rmm 26.4.0），Python 3.12 |
| 运行环境 | WSL2 发行版 `Ubuntu-22.04-OV-GPU`，micromamba 环境 `ov-gpu-xenium`，RTX 5070 Ti 16GB；Windows 原生仅 CPU 基线（win-64 无稳定 rapids-singlecell） |

## 已验证的跑通记录

1. 递进扩样纪律验证：readiness → smoke_5k → 200k → 500k → all。
2. ZXM 全量 1,131,184 细胞（QC 后）标准表达分析：QC→HVG→PCA→neighbors→UMAP→Leiden 33 / Louvain 40，全程 27.5 分钟。
3. zeng-lab GPU 两级注释（major+subtype）：239,180 细胞 207 秒，7 major 类。

## 强项（进整合 pipeline 时可取的部分）

- **百万级规模能力**：唯一已验证的全量 GPU 路线；strict GPU 校验（metadata 未证明 GPU 启用不算数）。
- 审计体系最完善：`run_metadata.json`（全参数+环境+device_policy）、`run_failed.json`（失败现场）、bundle/summary 三件套。
- readiness 探测脚本 + 环境重建脚本（WSL/micromamba 一键化）。

## 弱项 / 已知坑（补丁与固化参数）

- OV 本地补丁 2 处（`03_开源项目/omicverse/omicverse/pp/_preprocess.py`）：GPU neighbors 不得接收 scanpy 的 `method='umap'`（改 `algorithm="brute"`）；GPU umap 需 pop `gamma`（PUMAP fallback 还需 dill）。
- RMM 固化：`OV_GPU_MANAGED_MEMORY=false`、`POOL_ALLOCATOR=true`、devices=0（16GB 卡上 managed_memory=True 会分配失败）。
- `LD_LIBRARY_PATH` 必须优先指向 conda env 的 lib；假 GPU 测试（torch.cuda 不可用）两次发生过，readiness 必跑。
- OV 与官方的 cluster 编号不可直接互换。

## 关键文档

`OV_WSL_strict_GPU_V1.md`、`GPU环境策略.md`、`Xenium工作流固定方案评估.md`（4 路线对比与定版依据）、`run_ov_5k_colorectal_module2.py`（端到端主脚本模板）、`gpu_scale_readiness.py`。

## 二期定位建议

作为"基础范式主线"的**规模化引擎候选**；其 readiness→smoke→递进纪律与 metadata 审计应整体继承进整合 pipeline 的执行框架。
