# `FilbinLab/Multidimensional_STEPN`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\FilbinLab__Multidimensional_STEPN`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-045：幕上室管膜瘤异质性。英文原题（README 原文）"Code repository for single-cell multidimensional profiling of supratentorial ependymomas"（bioRxiv 2024.08.07.607066；sc GSE300150 / spatial GSE300146 / 原始数据 EGAS50000001513） |
| 精选级 | A |
| 主分类 | 复核维持 P8（儿童脑肿瘤多维度应用） |
| 次要用途 | P2 边缘：Xenium 空间模块（coherence、niche、CellCharter）+ epnApp ShinyApp 数据浏览范式 |
| 一句话功能 | 幕上室管膜瘤 sc/snRNA-seq + Xenium + 共培养 + 临床前模型的多维度分析仓：编号目录 1~6 覆盖 QC→inferCNV（冻/鲜样本双分支）→NMF→pseudobulk 发育投影→Xenium 预处理/program 注释/niche/coherence/CellCharter→共培养与 PDX；另附 epnApp ShinyApp 承载全部 sc/sn 数据探索 |
| License | MIT |
| 语言与规模 | Rx108/Pythonx6/Shellx3；87.3 MB；含 .Rproj、resources/、epnApp/ |
| 运行入口 | R 脚本按编号顺序执行（1.filtering.R→…→10_classification）；Xenium 模块 0~4 编号 R 脚本 + cellcharter/ 子目录；README 给出 R 4.3.1/Seurat v5.0.2/scanpy 1.11.2/squidpy 1.6.5/cellcharter 0.3.4 等全套版本号 |
| 复现难度 | 高 — 版本清单详尽但无 renv/conda 锁文件；GEO 已放 processed 数据、原始在 EGA 需申请；模块多、依赖中间 qs/rds 传递 |
| 与范式的关系 | "sc 定义 program → label transfer 到 Xenium → niche/coherence/CellCharter 邻域"链路完整可借鉴；coherence 分析在同类仓中少见；ShinyApp 是数据交付形态参考。候选池 |
| 坑提示 | ① R 侧极重（108 个 R 脚本），Seurat v5 + inferCNV 双管线，机器负担大；② 共培养/临床前模块与空间主线独立，勿混跑；③ Python 仅 6 文件（cellcharter/scvi 系），R-Python 间需经数据文件交接 |
| 锁定 SHA | 72650ca32d106fcbba0bf303a7b0720925a27dee（主表） |

## 结构速览

- 1.sc_snRNAseq_preprocessing/：filtering→inferCNV（3a/4a/5a 冻、3b/4b/5b 鲜）→NMF 准备与运行→cleanup/classification→Oncoprint
- 2.Plots/ + 3.Pseudobulk_analysis/：患者样本出图；发育参考数据集另置 Developmental_dataset_processing
- 4.Xenium/：0_preparation_scRNAseq_data.R、1_preprocessing.R、2_assign_programs.R、3_NicheAnalysis.R、4_coherence.R + cellcharter/ + resources/
- 5.Co-culture/、6.Preclinical_models/、epnApp/（ShinyApp）

## README/代码实读要点

- README 逐目录列出脚本编号与功能（含 inferCNV 冻/鲜分支这一细节），是复现顺序的唯一权威来源
- Xenium 模块五步结构（准备 sc 参考→预处理→program 注释→niche→coherence）与本库 zoro-spatial 的分析分层高度可映射
- 联系方式给出 3 位作者邮箱

## 抽读实录

- 读 README 全文；ls 顶层与 4.Xenium/（已确认 5 个编号脚本 + cellcharter/resources 子目录）。

## 复用建议

- 重点抄 4.Xenium 的 0→2（sc 参考准备+label transfer 注释）与 4_coherence（空间一致性打分）；epnApp 若用户想给合作方做数据浏览可作模板。全量复现不现实，按模块取用。
