# `jason-spence-lab/Johnson_et_al_2025`（档案卡）

> 由 agent 依据本地克隆实测撰写；不确定处一律【待补充】；禁止编造星标/日期/功能。

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-040：《小肠与类器官间充质多样性》"Mapping the emergence of mesenchymal diversity in the developing human intestine and organoids"（Johnson K. et al. 2025，期刊/DOI【待补充】） |
| 精选级 | B |
| 主分类 | P8（疾病应用/发育场景，复核维持） |
| 次要用途 | P2（"scRNA 图谱 → 自定义 Xenium panel"设计）；P4（CytoSPACE 解卷积映射） |
| 一句话功能 | 发育人小肠 scRNA-seq + 自定义 Xenium panel + 类器官基准的单文件巨型 Rmd（3711 行）：间充质五大群体（SEC/LPF/SMF/SMC/CXCL13+）鉴定、时空重塑与类器官比较 |
| License | 无LICENSE(仅可学习不可转载) |
| 语言与规模 | R（1 个 Rmd，3711 行）+ README；0.1MB |
| 运行入口 | 单个 `Intestinal mesenchyme_scRNAseq and Xenium.Rmd`；无 env 文件、无包版本说明 |
| 复现难度 | 高 — 单文件巨 notebook，数据链接 README 未给【待补充】，依赖包版本未声明 |
| 与范式的关系 | 参考价值两点：① 用发育 scRNA 图谱定制 Xenium panel 的思路；② CytoSPACE 把 scRNA 图谱映射到 Xenium 切片。整仓作流程范本价值低。候选池：否（片段参考） |
| 坑提示 | ① 无 LICENSE；② Rmd 内以 Figure 为章节、QC1→QC3 多轮迭代痕迹明显，需按标题检索；③ 三类分析混在同一文件 |
| 锁定 SHA | 主表未登记（空）；本地克隆 HEAD `1ec9966c0514f1b9b2076b3ec28c668fd2ea70d2` |

## 结构速览

- README：论文 summary、作者/单位、关键词（development、mesenchyme、fibroblast、
  single-cell sequencing、spatial transcriptomics、Xenium）——无 Data/Code 运行说明。
- Rmd 章节（实测标题层级）：
  - `# scRNAseq data`：Figure 1A（Create the object——建含全样本的 Seurat 对象；
    Add age info）。
  - `## Figure 2A & 2C`：Mesenchyme extracted from full object → QC1 → QC2 → QC3 (final version)。
  - `# Fetal Xenium data`：Figure 1C（Functions → Apply functions → Merge objects →
    Randomly sampling for plots）。
  - `## Figure 2B & 2D`：Extract mesenchyme from whole objects → Clean mesn → Further QC →
    Merge objects → Down sampling for plots → Further clean up。
  - `# CytoSPACE -- D142 -- All cell types`：Sequencing data、Xenium data、
    Prepare for cytospace（Function + 两侧数据准备）。
- 论文结论要点（README）：5 类间充质占据固有层/黏膜下层的离散解剖 niche；
  发育中纤维母细胞 niche 动态重塑；以此基准比较多种分化方案 hiPSC 肠类器官。
