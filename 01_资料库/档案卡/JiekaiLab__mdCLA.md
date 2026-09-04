# `JiekaiLab/mdCLA`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\JiekaiLab__mdCLA`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-041：小鼠胚胎发育年表。README 原文 "reproduction code for key figures from 'Developmental Chronology of Mouse Embryo'"（正式期刊与 DOI【待补充】，README 未给出） |
| 精选级 | A |
| 主分类 | 复核维持 P8（发育生物学疾病应用向；胚胎发育非空间方法学） |
| 次要用途 | P1 边缘：Code/ 自绘 sc 绘图工具链（sc_plotkits/sc_toolkits）可单独取用 |
| 一句话功能 | 小鼠胚胎发育单细胞年表的逐图复现 notebook 集：Figure1~5 目录约 40 个 ipynb（含 Extended Data），覆盖 AUC/TF 共表达 program 打分、RNA velocity（Figure3_bc_velocity）、monocle3/slingshot 拟时序（Figure5 Extended）、性别分类器（sex_classifier）等；Code/ 提供公共 imports/绘图工具与 treesing 工具 |
| License | 无LICENSE(仅可学习不可转载) |
| 语言与规模 | Pythonx109（notebook 为主）；276.9 MB（本批最大仓，含 .git 历史） |
| 运行入口 | 逐 notebook 运行；Code/global_script + sc_imports.py 为公共依赖；环境/数据说明【待补充】（README 仅 1 句话，无 env/requirements） |
| 复现难度 | 高 — README 无数据来源、无环境、无运行顺序说明；notebook 依赖自写 toolkit 与外部数据，复现路径需逐 notebook 反推 |
| 与范式的关系 | 大体量逐图 notebook + 公共绘图 toolkit 的组织方式（sc_plotkits）值得借鉴；拟时序/velocity 多方法并跑（monocle3+slingshot+scVelo）的图版组织可参考；非空间仓，与 zoro-spatial 主线关系弱 |
| 坑提示 | ① README 信息量极低（1 句话），期刊/数据号全缺；② 277 MB 体积大但无数据文件说明；③ treesing 为仓内自带工具，出处与用法【待补充】；④ Figure1 目录内文件名有拼写错误（Fgiure1_abc.ipynb），引用时注意 |
| 锁定 SHA | bfa8eb72a163b98abc32e641a657764fa33a394b（主表） |

## 结构速览

- Code/：global_script、sc_imports.py、sc_plotkits.py、sc_toolkits.py、treesing/
- Figure1/：7 个 notebook（含 sex_classifier、Figure1_d 两步流程）
- Figure2/：program 打分（AUC/TF coexp，Qiu2024 对照）+ predict_scripts/
- Figure3/：velocity 与轨迹；Figure4/：5 notebook；Figure5/：monocle3/slingshot/ot 拟时序对照

## README/代码实读要点

- README 全文仅："This GitHub repo provides reproduction code for key figures from 'Developmental Chronology of Mouse Embryo'"
- ls 实测 Figure2~5 共约 30 个 notebook + predict_scripts；notebook 命名含 step1/step2 与方法名，可推断执行顺序

## 抽读实录

- 读 README 全文；ls Code 与 Figure1~5；未深读 notebook 内容（B 类信息密度，避免过度展开）。

## 复用建议

- 只取 Code/sc_toolkits.py 类绘图工具与"方法对照式"图版组织思路；要复现科学结果前需先向作者/期刊补充数据与环境信息，当前状态下不作复现候选。
