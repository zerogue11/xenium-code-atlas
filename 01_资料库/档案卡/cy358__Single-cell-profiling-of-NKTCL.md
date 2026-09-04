# `cy358/Single-cell-profiling-of-NKTCL`（档案卡）

> 由 agent 依据本地克隆实测撰写；不确定处一律【待补充】；禁止编造星标/日期/功能。

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-057：《NK-T细胞淋巴瘤》单细胞图谱（论文 DOI 与正式题录【待补充】，README 未给） |
| 精选级 | A |
| 主分类 | P8（疾病应用，复核维持） |
| 次要用途 | P4（LIANA 细胞通讯片段）；P6（squidpy 邻域富集片段） |
| 一句话功能 | NKTCL 单细胞/空间分析轻量脚本集：bulk MP 信号生存、inferCNV、monocle3 拟时、LIANA 通讯、NMF 热图、Xenium marker dotplot 与邻域富集 |
| License | MIT |
| 语言与规模 | R 为主（5 个**无扩展名**脚本，2–3KB/个）+ Python x1；全仓约 15KB，主表记录 0.0MB |
| 运行入口 | R 脚本需自行改名/补扩展名后 source；`Neighborhood_enrichment_analysis.py`（scanpy/squidpy/spatialdata）；无 env 文件 |
| 复现难度 | 高 — README 仅一行标题，无环境/版本/数据说明；R 脚本引用的本地数据文件均不在仓内（见坑提示） |
| 与范式的关系 | 仅作 NKTCL 场景片段级参考：LIANA 按 MP_group 循环、squidpy nhood_enrichment 两段可抄；整仓不成流程。候选池：否 |
| 坑提示 | ① 五个带空格名字的条目（Bulk RNA-seq 等）是**文件**不是目录；② py 脚本 zarr 路径为占位；③ A 级系任务预置，就仓论仓实际质量接近 B |
| 锁定 SHA | 主表未登记（空）；本地克隆 HEAD `359f85c5465acf75b0c650804e41caab12b3a5fe` |

## 结构速览

- 顶层 8 个条目里 5 个是无扩展名 R 脚本文件（2008–3173 字节），不是目录。
- `Bulk RNA-seq`（R）：tidyverse + GSVA/GSEABase + survival/survminer。
  - 读 `data/MP_signature_genes.csv` 构建 MP1–MP4 信号基因集（na.omit 后入 gene_sets）。
  - 读 `data/bulk_expression_matrix.csv` 转矩阵，逐样本算 MP 信号分并做生存分析。
- `inferCNV`（R）：monocle/Seurat/ComplexHeatmap/harmony/multtest/Rcpp 依赖头，inferCNV 运行脚本。
- `monocle3`（R）：`new_cell_data_set(as.matrix(CD8T@assays$RNA@counts), ...)` 起 CD8 T 子集拟时。
- `Cell–cell communication analysis`（R）：Seurat + LIANA；
  `Idents(sce) <- cell_type` 后取 `mp_groups` 唯一值，逐组跑 liana 存入 `liana_results_list`。
- `NMF and cell subsets abundance calculation`（R）：
  读 `Fig2_data/nmf_intersect_sorted.rds`，值截断到 2–25，melt 后画 NMF 交集热图。
- `Neighborhood_enrichment_analysis.py`：
  - `sd.read_zarr("/xenium.zarr")`（占位路径）取 `sdata.tables["table"]`。
  - 30 个 marker（KLRC1/NCAM1/KLRK1、CD14/CD68/CD163、SNHG15/SOST/KIT、MZB1/XBP1/FCRL5、
    CD3E/CD8A/CD2、COL5A1/ANXA2/MMP14、PECAM1/POSTN/MYH9、MS4A1/CD19/CD79A、
    COL4A1/COL4A2/COL18A1、TUBB/STMN1/GZMB）做 `sc.pl.dotplot`（standard_scale="var", dot_max=0.7）。
  - `sq.gr.spatial_neighbors` + `sq.gr.nhood_enrichment`（cluster_key="leiden"）出邻域富集热图。

## 复核与实读补充

- 主分类维持 P8：内容为 NKTCL 疾病研究的多方法散装脚本，无独立方法学交付。
- 无 README 实质内容、无数据、无环境；A 级系任务预置，二期提炼建议只取
  "LIANA 逐组循环"与"squidpy nhood_enrichment"两个代码模式。
- data/、Fig2_data/ 等被引用目录在克隆内不存在，直接运行会立即报错。
