# `VividKai/SpatialBC`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\VividKai__SpatialBC`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-038：肌层浸润性膀胱癌。英文原题（README 原文）"A Spatial Atlas of Muscle-Invasive Bladder Cancer Reveals Lineage-Specific Vulnerabilities and Immune Architecture"（Yu et al., Cancer Discovery in revision 2026；MD Anderson 王凌华组，与 LungPCA/LungIMC 同团队） |
| 精选级 | B |
| 主分类 | 复核维持 P8（膀胱癌空间图谱应用） |
| 次要用途 | （空） |
| 一句话功能 | 膀胱癌空间图谱逐图 R 脚本（Fig1~6.R + RCTD.R 去卷积）：Seurat + scigenex（聚类 program）+ GSVA/scalop（打分）+ limma/ broom（统计）+ circlize（弦图）组合，覆盖谱系特异脆弱性与免疫架构分析 |
| License | 无LICENSE(仅可学习不可转载) |
| 语言与规模 | Rx7；0.2 MB |
| 运行入口 | 逐脚本运行；README 仅论文题名与联系方式，数据来源/环境【待补充】 |
| 复现难度 | 高 — 无数据、无 env、无图版输入说明；脚本假定本地 Seurat 对象与中间文件存在 |
| 与范式的关系 | RCTD 去卷积 + scigenex program + GSVA 打分的 R 侧组合可作参考；膀胱癌谱系（luminal/basal）脆弱性叙事与 LungPCA 同团队同风格；参考池低位 |
| 坑提示 | ① 单 commit 式论文伴随仓，脚本自用属性强；② 依赖小众包（scigenex、scalop）安装可能困难；③ 与 LIT-032/031 同为 MD Anderson 系，README 模板一致（"code necessary for the analysis"），均无数据/env |
| 锁定 SHA | f854197edb9730a9fc215ce1022a44474446f99c（主表） |

## 结构速览

- Fig1.R ~ Fig6.R：按图版编号的 R 出图/分析脚本
- RCTD.R：spaceXR 去卷积
- README：4 行（题名+联系邮箱）

## README/代码实读要点

- head Fig2.R：tidyverse/Seurat/scigenex/scCustomize/limma/GSVA/scalop/circlize 等 20+ 包一次载入，脚本体量大、混合分析与出图
- README 无任何运行/数据指引

## 抽读实录

- 读 README 全文；head Fig2.R（20 行）；ls 顶层。

## 复用建议

- 只作膀胱癌空间图谱的叙事对照与 RCTD 用法旁证；不建议投入复现。若做膀胱相关课题优先看其图版设计与 lineage 程序定义。
