# `The-HQQ/Human_fetal_lung_atlas`（档案卡）

> 由 agent 依据本地克隆实测撰写；不确定处一律【待补充】；禁止编造星标/日期/功能。

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-008：《胎儿肺图谱》（Quach & Farrell et al. 2023, Early human fetal lung atlas reveals the temporal dynamics of epithelial cell plasticity） |
| 精选级 | A |
| 主分类 | P2（复核维持：胎儿肺发育图谱） |
| 次要用途 | P6（Visium 数据处理）；P5（Xenium 数据处理入口） |
| 一句话功能 | 胎儿肺图谱论文图表复现代码：scRNAseq/Visium/Xenium 三路数据处理 + 正文与补充图生成，README 给出完整 R/Python 依赖版本清单 |
| License | 无LICENSE(仅可学习不可转载) |
| 语言与规模 | R×24 / Python×1，0.1 MB（纯脚本，无数据） |
| 运行入口 | R/Python 脚本按 Data_processing → Figures → Supplementary 分层；数据需从 Synapse syn53437291 下载；无 env 文件但 README 列包版本 |
| 复现难度 | 中：依赖清单齐全、脚本分层清晰，但数据在 Synapse（需账号/网络）且 Seurat v4 旧栈与现行 v5 有兼容成本 |
| 与范式的关系 | "三平台（scRNA/Visium/Xenium）同图谱产出"的组织结构可参考；Xenium_analysis.R 是小型 Xenium 分析入口样例 |
| 坑提示 | README 指明关联仓 `Spencerfar/fetal_lung_analysis`（本库已另收，A 级），部分分析在彼仓不在本仓；macOS/Linux 测试，Windows 未验证 |
| 锁定 SHA | d4bad09dcc4894b2efaefc5c3be1761fa4633eb4 |

## 结构速览

- `Data_processing/Visium|Xenium|scRNAseq/`：三平台数据处理脚本（Xenium 仅 `Xenium_analysis.R` 一个入口）。
- `Figures/` + `Supplementary_Figures/` + `Supplementary_Note_Figures/`：正文图、补充图、补充笔记图生成脚本。

## 实读要点

- README 给出经测试的软件环境：macOS Ventura 13.5 / CentOS 7；R 侧 19 个包带版本（Seurat v4.0、SeuratData 0.2.2、SCENIC 1.3.1、SCopeLoomR 0.13.0、slingshot 2.7.0、clusterExperiment 2.16.0、AUCell 1.18.1、gam 1.22.2 等），Python 侧 6 个（scanpy 1.10.1、loompy 3.0.6、MulticoreTSNE 0.1 等）。
- 处理数据与调色板统一在 Synapse syn53437291 下载；代码用途自述为"产出正文图、补充数据图与补充笔记图"。
- 与本库另一 A 级仓 `spencerfar/fetal_lung_analysis` 为姊妹仓（README 互指），分工为：本仓=图表复现，彼仓=分析（29.9MB，Python×28）。

## 复现路径（怎么跑）

1. Synapse syn53437291 注册下载全部处理数据与调色板。
2. R 侧按 README 版本表装 Seurat v4 系依赖（建议独立 R 库路径隔离，避免与 Seurat v5 冲突）；Python 侧 scanpy 1.10.1 + loompy（SCENIC loom 输入）。
3. Data_processing 三平台各自独立 → Figures → Supplementary 依图追脚本。

## 借鉴与风险

- 可移植点：README 的"OS+逐包版本表"写法；Xenium_analysis.R 作为单文件 Xenium 入口可对照本项目 xenium 标准流程做差异审读。
- 风险：Seurat v4/SCENIC 1.3.1 旧栈在 2026 年环境装回有摩擦；Synapse 下载需账号；Windows 未测试。质量标准（版本表+分层清晰）突出，A 级合理；若做整卷复现验证可议升 S。

