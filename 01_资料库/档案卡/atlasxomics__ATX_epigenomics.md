# `atlasxomics/ATX_epigenomics`（档案卡）

> 由 agent 依据本地克隆实测撰写；不确定处一律【待补充】；禁止编造星标/日期/功能。

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-039：《非黑色素瘤皮肤癌巨噬状态》 |
| 精选级 | B |
| 主分类 | P2（复核建议改 P0：实读为 DBiT-seq ATAC/CUT&Tag 平台级 fastq→fragment 预处理管线 + ArchR/Seurat 通用分析教程，仓内未见皮肤癌疾病特异代码；是否随文献映射保留 P2 由终审定） |
| 次要用途 | P6（空间表观降维/聚类/peak calling 的空间整合分析教程） |
| 一句话功能 | DBiT-seq 空间 ATAC/CUT&Tag 分析脚本：fastq2frags snakemake 管线（连接子校验 → Chromap 比对 → fragment.tsv.gz）+ renv 管理的 R 分析教程（ArchR 降维聚类/差异可达性 + Seurat 空间整合） |
| License | MIT |
| 语言与规模 | R×3（analysis 教程+utils），fastq2frags 为 Snakefile+条码文件，14.0 MB（多为图片/文档） |
| 运行入口 | `fastq2frags/Snakefile`（snakemake，README 建议 Linux 64GB RAM / 8 核 / 1TB 磁盘，给 AWS EC2 指引）+ `analysis/epigenomics_tutorial.Rmd`（renv.lock 锁定环境，需 AtlasXbrowser 产出的 spatial 文件夹） |
| 复现难度 | 高：硬件门槛（1TB 磁盘/64GB RAM）+ 依赖 AtlasXbrowser 专有产物 + fastq 原始数据自备 |
| 与范式的关系 | 空间表观（ATAC/CUT&Tag）管线范式参考；与本研究 Xenium 转录组主线互补但非必需；观察池 |
| 坑提示 | analysis 依赖 AtlasXbrowser（另一 GUI 包）生成的 spatial 目录，脱离其生态跑不通；仓内容为平台通用代码，与 LIT-039 皮肤癌文献的具体映射关系待人工核【待补充】 |
| 锁定 SHA | 843b75443eafe7478efae22e0ff3d95f1757d8f9 |

## 结构速览

- `fastq2frags/`：Snakefile + 4 个条码 whitelist（bc50.txt.gz、bc96.txt.gz、bc220_25-APR.txt.gz、bc220-20-MAY.txt.gz）+ README。
- `analysis/`：`epigenomics_tutorial.Rmd/.md`（ArchR+Seurat 空间表观分析全教程）、`renv.lock`、`session_info.txt`、`utils.R`、figures。
- `static/`：logo 等静态图。

## 实读要点

- README 自述适用"barcodes on read2"的 Zhang et al. 2023 条码方案；管线三步：连接子序列正确性过滤 → Chromap 比对与预处理 → BED 转 fragment.tsv.gz。
- analysis 目录为完整 renv 项目（.Rprofile、renv.lock、session_info.txt），教程输出 md 版可直接阅读；上游需 AtlasXbrowser（github.com/atlasxomics/AtlasXbrowser）产出 spatial 文件夹。
- README 引用 Deng 2022 Spatial-CUT&Tag（Science）、Liu 2022/2023 DBiT-seq/spatial-CITE-seq 等 5 篇方法学引文，说明本仓定位是平台方法而非单篇疾病论文。

## 复现路径（怎么跑）

1. fastq 线：Linux/大磁盘机器（README 建议 64GB RAM/8 核/1TB）上以 snakemake 跑 fastq2frags/Snakefile，read2 条码按 whitelist（bc50/bc96/bc220）校验，输出 fragment.tsv.gz。
2. 分析线：R 内 renv::restore()（renv.lock 锁环境）→ 跑 epigenomics_tutorial.Rmd，输入需 AtlasXbrowser 产出的 spatial 文件夹。
3. 云端按 README 的 AWS EC2 指引可免除本地硬件门槛。

## 借鉴与风险

- 可移植点：fastq2frags 的"条码正确性过滤→Chromap→fragment"三步是空间表观预处理的干净骨架；renv.lock+session_info 的环境冻结做法值得本项目吸收。
- 风险：绑定 AtlasXbrowser 生态；B 级定级合理（文档好但与映射文献的疾病分析内容未见于仓，且平台与本主线距离远）。

