# `WuLabMDA/LungIMC`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\WuLabMDA__LungIMC`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-031：肺腺癌前体空间多组学（README 原文仅 "Lung Imaging Mass Cytometry Study"；论文题名/期刊【待补充】；MD Anderson 王凌华组） |
| 精选级 | A |
| 主分类 | 复核维持 P8。注意：平台为 IMC（成像质谱流式，蛋白组），与 Xenium 转录组平台差异大 |
| 次要用途 | P0 边缘：DeepCell/Steinbock 分割 + 特征多样性/分解分析 + 病灶聚合（ITH、系统发育树）的 IMC 流程参考 |
| 一句话功能 | 肺腺癌 IMC 全流程：预处理（Matlab 去噪/串扰校正）→ 分割（DeepCellSeg、Steinbock）→ 特征分析（FeatureAnalysis：分解/多样性/DEG/优势/趋势）→ 表型可视化 → 病灶级聚合分析（Aggregation：CoreDistProgression、ITH、LesionPhylogeneticTree、MarginCoreCmp）→ TMB 状态关联与 bootstrap → Docker 封装（Dockerfile+Docker.md） |
| License | BSD |
| 语言与规模 | Rx189/Pythonx125/MATLABx26；1.3 MB（纯代码，图像数据不在仓内） |
| 运行入口 | 按模块目录的 R/py/Matlab 脚本 + Dockerfile；Steinbock 模块自带独立 Docker.md；数据获取【待补充】 |
| 复现难度 | 高 — IMC 原始图像→分割→特征→分析链条长且三语言混合；平台数据（标注 IMC 图像）需自备 |
| 与范式的关系 | 与 LIT-032（LungPCA）、LIT-038（SpatialBC）同团队：IMC 蛋白组与空转转录组的"多组学互证"组织方式可参考；病灶级聚合/ITH/进展距离分析是肿瘤演化叙事模板；参考池（平台差异背景下取方法叙事） |
| 坑提示 | ① 平台差异：IMC 为抗体蛋白组，panel 设计与分析逻辑与 Xenium 不同，勿直接搬注释流程；② 26 个 Matlab 脚本（PreprocessIMC-Matlab）增加环境负担；③ README 只有一句话，模块功能靠目录名推断 |
| 锁定 SHA | be35039a579cb658b8a247450f61c5626d8dd886（主表） |

## 结构速览

- PreprocessIMC-Matlab/ + DenoiseStains/（含 SpilloverCorrection）：图像预处理
- DeepCellSeg/ + Steinbock/（含 Docker.md）：分割两条路线
- FeatureAnalysis/（Decomposition/Diversity/FeatureDEG/FeatureDominant/FeatureTrends）+ PhenotypeVis/：细胞表型与特征
- Aggregation/（LesionAgg、CoreDistProgression、ITH、LesionPhylogeneticTree、MarginCoreCmp、FeatureVolcano）+ TMB/（slide 级状态与 bootstrap）+ AnalysisR/（Fig01/Fig02/Macrophage/TIM3）

## README/代码实读要点

- README 全文一句话；ls 实测 11 个模块目录与上述子结构
- TMB/ 脚本命名（obtain_slide_tmb_status、bootstrap_slide_tmb_feas、volcano_slide_tmb）显示 slide 级 TMB 状态与特征关联分析【TMB 具体定义以论文为准，待补充】
- Dockerfile + Docker.md 说明作者有意封装运行环境

## 抽读实录

- 读 README 全文；find 两级目录结构与 TMB/Steinbock 模块文件清单。

## 复用建议

- 仅作 IMC 流程与"病灶聚合/ITH"叙事参考；若用户未来接入 IMC/CyTOF 蛋白组数据再回来细读 Steinbock 与 Aggregation 模块。A 级建议维持（平台差异限制了直接复用）。
