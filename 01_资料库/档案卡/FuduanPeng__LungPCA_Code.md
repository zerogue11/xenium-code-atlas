# `FuduanPeng/LungPCA_Code`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\FuduanPeng__LungPCA_Code`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-032：肺前体病变进展。英文原题（README 原文）"Multimodal Spatial-Omics Reveal Co-Evolution of Alveolar Progenitors and Proinflammatory Niches in Progression of Lung Precursor Lesions"（Peng et al., Cancer Cell in revision 2025；processed data Zenode 10.5281/zenodo.17148540） |
| 精选级 | A |
| 主分类 | 复核维持 P8（肺腺癌前体 AAH→AIS→MIA→LUAD 进展，与用户肺课题近亲） |
| 次要用途 | （空） |
| 一句话功能 | 论文逐图脚本集：14 个文件按 "Figure N.R"（Seurat/ggplot2/ggsankey/pheatmap）与 "Figure Nx.py"（Python 侧）对应图版，从 ./Data/*.rda 加载处理后对象出图（如 Figure1B 的 AAH/AIS/MIA/LUAD sankey、细胞型配色 hardcode） |
| License | 无LICENSE(仅可学习不可转载) |
| 语言与规模 | Rx7/Pythonx6；0.1 MB（纯脚本，无数据无 env） |
| 运行入口 | 逐脚本独立运行；R 脚本开头 `rm(list=ls()); setwd(getwd())`，假定 ./Data 与 ./Results 目录；无 renv/conda/requirements |
| 复现难度 | 高 — 无环境声明、无数据（需从 Zenodo 自取并自建 ./Data 结构与 rda 对象名）、脚本间数据流不透明；仅适合对照论文图版阅读学习 |
| 与范式的关系 | 肺前体病变进展的分段（normal/AAH/AIS/MIA/LUAD）叙事与配色/图型参考；真正可迁移的是图版组织方式而非代码（无函数封装） |
| 坑提示 | ① `setwd(getwd())` + 相对路径，必须在仓根目录跑；② 每脚本 rm(list=ls()) 独占会话；③ Data/*.rda 对象名不可见于仓内，需按脚本变量名倒推 Zenodo 文件对应关系；④ 无 LICENSE 不可转载 |
| 锁定 SHA | fba87dbee8dbae497b15b81a4b0fa79edccd17b2（主表） |

## 结构速览

- Figure 1.R / 2.R / 3.R / 4.R / 5.R / 6.R / 7.R：R 出图主脚本（Seurat 对象 → ggplot 系）
- Figure 1E 4F.py、2C.py、3K 3N.py、6E 6F 7D.py、6G.py：Python 侧补充图
- README：仅论文题名、作者联系方式、Zenode DOI，无运行说明

## README/代码实读要点

- head "Figure 1.R"：load('./Data/Figure 1B.rda') 后直接 ggplot sankey；AAH→AIS→MIA→LUAD 配色 hardcode 在 scale_fill_manual
- 无任何函数抽象，全部顶层语句，适合读、不适合依赖

## 抽读实录

- 读 README 全文；head Figure 1.R（25 行）；ls 顶层。

## 复用建议

- 仅作"肺前体病变进展空间分析"叙事与图版参照；代码级复用价值低。若需其分析逻辑，应先从 Zenodo 拉 processed data 再对照脚本理解每图输入。
