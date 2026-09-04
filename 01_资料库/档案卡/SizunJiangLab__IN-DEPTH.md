# `SizunJiangLab/IN-DEPTH`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\SizunJiangLab__IN-DEPTH`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-070：同片空间多组学整合（肿瘤病毒相关 TME）。英文原题（README 原文）"Same-Slide Spatial Multi-Omics Integration with IN-DEPTH Reveals Tumor Virus-Linked Spatial Reorganization of the Tumor Microenvironment"（Cancer Discovery 2026, DOI 10.1158/2159-8290.CD-25-0775；DLBCL EBV+/EBV-） |
| 精选级 | A |
| 主分类 | 复核维持 P8（淋巴瘤 TME 应用 + 方法学组件） |
| 次要用途 | P0/P2 边缘：SGCC（Spectral Graph Cross-Correlation）跨模态整合框架 + 同片 CODEX×GeoMx 图像配准教程 |
| 一句话功能 | IN-DEPTH 工作流 + SGCC 整合框架的官方代码：src/ 8 条预处理分析管线（CODEX 蛋白组、GeoMx 转录组、SGCC、scSGCC、邻域 DEG/GSEA/配体受体）、paper_figures/ 23 个逐图脚本、tutorial/（codex-geomx 图像配准整合 notebook + SGCC R 包函数文档）；数据在 Zenodo 两部分（CC BY 4.0） |
| License | MIT 文件存在，但 README 声明代码仅限非商业学术用途、商用需书面许可（论文为 CC BY-NC-ND） |
| 语言与规模 | Rx60/Pythonx43；114.8 MB；含 CITATION.cff、docs 站点、CI 配置 |
| 运行入口 | R/Rmd/ipynb 混合：src 管线产出 → paper_figures 出图；教程 notebook（indepth_codex_geomx.ipynb）+ sgcc_tutorial.md（R 包安装与函数总览）；数据 Zenodo 10.5281/zenodo.14530077 与 10.5281/zenodo.18379155 |
| 复现难度 | 高 — 同片 CODEX+GeoMx 实验数据专属、管线链条长（配准→binning→去卷积→SGCC）；但教程与函数文档齐全，方法学单点（SGCC/配准）可单独学 |
| 与范式的关系 | 用户"同片/跨模态空间多组学整合"方向的关键参照：图像配准对齐蛋白-转录、SGCC 图互相关框架、scSGCC 单细胞扩展；候选池（方法层） |
| 坑提示 | ① 本地为部分 checkout：src/02_figure_2_CODEX_GeoMx_Tonsil_run/ 下名为"4_GeoMX functional analysis for Tonsil "（尾随空格）的子目录在 Windows 未检出，git status 显示一批 D（deleted），补齐需改克隆方式或换机器；② R/py 双栈混杂，逐图脚本间依赖 src 产物；③ License 非商用条款 |
| 锁定 SHA | c989db566252b4692ed7523ed05c644ca5ab64ee（主表） |

## 结构速览

- src/：01 CODEX前后对比、02 CODEX-GeoMx Tonsil 管线（部分未检出）、04 GeoMx、05 GeoMx 分析+SGCC、06 scSGCC+相关性、07 CODEX 管线+邻域分析
- paper_figures/：01~07 编号的逐图 R/Rmd/ipynb/py 脚本（README 有完整映射表）
- tutorial/：indepth_codex_geomx.ipynb + sgcc_tutorial.md；docs/：文档站点；CITATION.cff + bibtex

## README/代码实读要点

- README 给出 src 与 paper_figures 的全部脚本级索引（含修订补充图脚本）
- 数据许可区分明确：代码非商业、Zenodo 数据 CC BY 4.0
- git status 实测确认尾随空格目录未检出（"4_GeoMX functional analysis for Tonsil /"内 10+ 文件 D）

## 抽读实录

- 读 README 全文；ls src/tutorial；git -C status --short 抽查 checkout 完整性。

## 复用建议

- 先读 tutorial/sgcc_tutorial.md 与配准 notebook 再决定是否引入 SGCC；若采用，建议用 WSL/Linux 重新完整克隆以避开尾随空格目录问题。建议维持 A 级（方法学组件价值高但平台组合与用户 Xenium 主线不完全重合）。
