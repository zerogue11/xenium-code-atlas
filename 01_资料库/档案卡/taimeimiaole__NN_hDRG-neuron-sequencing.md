# `taimeimiaole/NN_hDRG-neuron-sequencing`（档案卡）

> 由 agent 依据本地克隆实测撰写；不确定处一律【待补充】；禁止编造星标/日期/功能。

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-010：《躯体感觉神经》人类 DRG 神经元测序（README 路径含 "Nature neuroscience ... Revision/Resubmission/20240716_Final"，为 Nat Neurosci 投稿修订稿；正式题录【待补充】） |
| 精选级 | A |
| 主分类 | P8（疾病应用/神经场景，复核维持） |
| 次要用途 | P2（跨物种/跨研究整合：Conos 比较人 vs Sharma 等 vs 恒河猴） |
| 一句话功能 | 人类 DRG 神经元测序论文的 25 组 Source_code 目录（Rmd/R/ipynb 与 .RData 数据混放），README 按图版逐条索引到"脚本+数据" |
| License | 无LICENSE(仅可学习不可转载) |
| 语言与规模 | 实测：Rmd x17、.R x3、ipynb x5、RData x13（散在各 Source_code 内）；664MB（主表）/实测约 744M |
| 运行入口 | 各 Source_code_N/ 内 Rmd/R/ipynb（如 Source_code_1 的 LCM 分析、22/23 的 Conos 整合）；无 env 文件、无包版本说明 |
| 复现难度 | 高 — README 索引路径全是作者本机 Windows 绝对路径，数据与代码耦合，需逐脚本改路径；包版本未声明 |
| 与范式的关系 | DRG/躯体感觉 marker 与跨物种 Conos 整合可作神经场景片段参考；整仓工程质量差。候选池：否 |
| 坑提示 | ① 硬编码 Windows 绝对路径遍布 README（含空格，可能渗入脚本）；② RData 散在 25 个目录、无集中数据目录；③ 编号缺 18/19 且 26/27 小写；④ 无 LICENSE |
| 锁定 SHA | 主表未登记（空）；本地克隆 HEAD `3759bed52e0551a818b67a598ab95a1a1acfcfe0` |

## 结构速览

- 25 个 Source_code 目录（实测：1–17、20–25 大写，26–27 小写），
  每组 = 分析脚本（.Rmd/.R/.ipynb）+ 运行所需 .RData。
  - Source_code_1/：Hs_LCM_final.Rmd + Hs_LCM_final.RData（LCM 数据的 Seurat 对象级 RData）。
  - Source_code_22/：Conos_Hs_vs_Sharma_INPUT_fig2A.RData（Conos 整合输入）。
  - Source_code_23/：conos_Hs_vs_Sharma_Fig2A.R（README 另注 conos_Hs_vs_Rhesus_Fig2B.R）。
- README 逐图版索引（实测样例）：
  - Figure1B/C/D/G → source code 1.Rmd；Figure1E → source code 3.ipynb。
  - Figure2A → source code 22；Figure2B → source code 23。
  - 每条附 "done" 标记与完整 Windows 路径（`C:\E\Posdoc work at Upenn\Lab_work\...`）。
- 无任何环境/版本说明；论文对应 Nat Neurosci 投稿修订版（README 路径含 20240716_Final）。
