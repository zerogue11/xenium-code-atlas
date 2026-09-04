# `XL-Genomics/2024_Senescent_Niche_in_HLHS`（档案卡）

> 由 agent 依据本地克隆实测撰写；不确定处一律【待补充】；禁止编造星标/日期/功能。

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-052：《心室辅助装置减负荷逆转微血管衰老》（Li et al., Nat Cardiovasc Res 2026;5(3):262-280, doi:10.1038/s44161-026-00790-x） |
| 精选级 | A |
| 主分类 | P3（复核维持：微血管衰老生态位 senescent niche 主题） |
| 次要用途 | P4（CellChat 通讯）；P2（scANVI 注释）；P6（Visium/Xenium 整合作图） |
| 一句话功能 | HLHS 心肌微环境研究全套计算脚本：snRNA-seq QC→scVI/scANVI 整合→Milo 差异丰度→scVelo→CellChat→pseudobulk→衰老评分→Visium/Xenium 空转整合，共 22 个 PART 编号脚本 |
| License | 无LICENSE(仅可学习不可转载) |
| 语言与规模 | R×18 / Python×3（PART07/08/24 为 ipynb），32.5 MB |
| 运行入口 | R 脚本（PART01–PART93 编号串联）+ 3 个 Jupyter 笔记本；数据存 Zenodo #18407403 但 README 明示受 Texas Genomic Act 2025 限制，需签数据使用协议向通讯作者申请；无 env 文件【待补充依赖版本】 |
| 复现难度 | 高：数据访问受限需申请，脚本链长且 PART 编号跳号（无 06/10-18 等中间号），路径为作者本地相对结构 |
| 与范式的关系 | "senescent niche 空间定位"叙事与 Xenium 整合脚本（PART65/68）可参考；心脏方向与本项目场景距离较远，观察池 |
| 坑提示 | 数据非公开直下（法务限制）；PART 序列不连续，运行顺序需自行梳理；readRDS 路径（integrated/PART19...）依赖上游中间产物齐全 |
| 锁定 SHA | 353a7d60c20d84feab3647753e174a5993f9778c |

## 结构速览

- PART01–05：数据收集、合并、过滤、双胞、清理（R）。
- PART07/08/09：scVI/scANVI（Python notebook + R 收尾）。
- PART19–32：注释固化、Milo、scvelo、CellChat、pseudobulk PCA、DEG、age score、pan-disease mapping。
- PART40–93：ipsc_cm、Visium、Xenium 整合/分析（PART65/68）、最终绘图（PART93.plot_r_v3.R）。

## 实读要点

- PART65.xenium_integration.R 实读：文件头自述作者 Xiao LI（Texas Heart Institute）、2022-09-01、Ver 2、Step=PART65_Xenium_Integration、Project=2022_hlhs_dturaga；载入 `integrated/PART19.annotated.srt.rds`（全细胞类型 Seurat 对象）与 `analysis/PART28.cell_state_marker.srt_mk.rds`（细胞态 marker）——Xenium 整合建立在 snRNA 主对象与 marker 表之上。
- README 自述三类计算内容：snRNA 处理与 QC、snRNA+ST 整合与细胞注释可视化、论文图可视化；iPS-CM 数据佐证心肌细胞内在衰老。
- 数据可得性 README 原文明示：Zenodo #18407403 存数字表达矩阵，但 Texas Genomic Act of 2025 限制人类数据共享，需 DUA+机构审批后按通讯作者申请。

## 复现路径（怎么跑）

1. 数据关即第一关：向通讯作者申请 DUA（Zenodo 条目存在但访问受限），拿到表达矩阵与 Visium/Xenium 原始产物。
2. R 侧按 PART 编号顺序重建运行序（编号有缺口，以脚本内部 readRDS 依赖为准：如 PART65 依赖 PART19 对象与 PART28 marker 表）。
3. Python 侧 PART07/08（scVI/scANVI）与 PART24（scvelo）独立环境，结果回接 R。

## 借鉴与风险

- 可移植点：PART 编号串联+脚本头 Ver/Step/Project 元数据注释的做法轻量好用；pseudobulk/age score/pan-disease mapping 的疾病评分思路可平移到其他疾病场景。
- 风险：数据非公开使端到端复现基本不可行，A 级定级合理（脚本可读可借鉴但不可复跑）；P3 维持。

