# `LabOnoM/GSE284271`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\LabOnoM__GSE284271`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-036：小鼠胚胎腭。英文原题（README 原文）"Single Cell Spatial Transcriptomics of the Murine Embryonic Palate Links Pax9 to Patterning and Organization of Extracellular Matrix Components"（GSE284271；期刊【待补充】） |
| 精选级 | A |
| 主分类 | 复核维持 P8（发育/颅面应用，Visium HD 平台） |
| 次要用途 | P1 边缘：scRNA-seq 与 Visium HD 对照分析的最小双文件范式；配套在线分析报告（sessionInfo 全公开） |
| 一句话功能 | GSE284271 原始分析的两件套：00.NIH_10xVisiumHD.rmd（R 侧 Visium HD 空转分析）+ 01.scRNAseq10xVisiumHD.ipynb（Python 侧 scRNA-seq 与 Visium HD 对照），配 GitHub Pages 分析报告网站供核对原始结果 |
| License | BSD-2 变体 + 第三条禁商用（Bioinformatics Study Group in Okayama University License，禁商用/需书面许可） |
| 语言与规模 | Rx1/Pythonx1；1.2 MB（就两个入口文件） |
| 运行入口 | RStudio 打开 .rmd；Jupyter 打开 .ipynb；数据需自跑 spaceranger 从 GSE284271 重建；sessionInfo 在报告网站 Supplementary 节 |
| 复现难度 | 中 — 入口极简、环境版本经 sessionInfo 完整公开、结果有在线报告逐 cell 对照；主要成本是 spaceranger 重建 GSE 数据 |
| 与范式的关系 | "小仓+双语言入口+在线报告+sessionInfo 溯源"的极简可复现范式值得借鉴；VisiumHD 与 scRNA 对照读法简单清晰；候选池（范式参考） |
| 坑提示 | ① spaceranger 输出不随仓提供，必须自行处理 GSE284271 原始数据；② License 禁商用（BSD 三条款变体），转载需注意；③ 仓内无 env 文件，依赖版本看报告网站 |
| 锁定 SHA | 0c3f52aefe09779fb20aa4cfba77b02bb9858440（主表） |

## 结构速览

- 00.NIH_10xVisiumHD.rmd：R/Visium HD 主分析
- 01.scRNAseq10xVisiumHD.ipynb：Python/scRNA-seq 对照分析
- README.md + LICENSE + .gitignore；无数据、无 env

## README/代码实读要点

- README 核心指引：先自跑 spaceranger → 用 RStudio/Jupyter 打开两文件 → 结果对照 labonom.github.io/GSE284271 报告网站
- 报告网站含两份 notebook 的 sessionInfo（OS/R/包/Python 模块全记录）

## 抽读实录

- 读 README 全文（含 License 三条款原文）；ls 顶层确认仅两入口文件。

## 复用建议

- 把"sessionInfo 上网 + 报告网站对照"纳入用户项目交付契约的备选项；分析本体不复杂，可作 Visium HD 入门对照件。商用禁令不影响学习复现。
