# `mneyazi/cardiac_sarcoidosis`（档案卡）

> 由 agent 依据本地克隆实测撰写；不确定处一律【待补充】；禁止编造星标/日期/功能。

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-043：《心脏结节病》"Integrative Molecular Analyses of Inflammatory and Autoimmune Signals in Cardiac Sarcoidosis"（Neyazi, Venturini et al.；README 出版链接为占位符 XYZ，期刊/DOI【待补充】） |
| 精选级 | B |
| 主分类 | P8（疾病应用，复核维持） |
| 次要用途 | — |
| 一句话功能 | 心脏结节病研究的两段定制 R 分析：TRUST4 AIRR 跨样本合并与 V(D)J 克隆分配 + Xenium 固定半径空间邻域，合计 3 个脚本 |
| License | 无LICENSE(仅可学习不可转载) |
| 语言与规模 | R x3（每个约 100–200 行级，头部注释规范）；0.0MB |
| 运行入口 | 3 个 `#!/usr/bin/env Rscript` 脚本按编号顺序；无 env 文件；脚本内 Configuration 段改路径 |
| 复现难度 | 高 — 无数据来源、无环境/包版本说明，出版链接缺失；脚本自身文档好但输入对象需自备 |
| 与范式的关系 | 方法片段参考（与疾病无关可移植）：TRUST4 AIRR 合并、跨链克隆桥接、frNN 固定半径邻域三段。候选池：否 |
| 坑提示 | ① README 出版链接是占位符 XYZ（作者未填）；② clonality_vdj/empty.txt 占位文件；③ 输入需自备已 QC+已注释对象 |
| 锁定 SHA | 主表未登记（空）；本地克隆 HEAD `173fd608ecc1074990e8cb4104345005e7b90e66` |

## 结构速览

- `clonality_vdj/01_merge_trust4_airr.R`（实测头部注释）：
  - 扫描 `<trust4_dir>/<sample>/TRUST_possorted_genome_bam_barcode_airr.tsv`。
  - 跳过空文件，逐样本加 `orig.ident` 列，合并为 master data frame。
  - 输出 master_TRUST_file.rds 与 master_TRUST_file.tsv.gz。
- `clonality_vdj/02_assign_vdj_clones.R`（实测头部注释）：
  1. 由 locus 定义 receptor_type（BCR vs TCR）与 chain_type。
  2. 在 grouping unit × receptor_type × chain_type 内聚类 junction 序列。
  3. 跨链桥接链级克隆标签，得到 overall_clone。
  4. 计算 clone size / clone rank。
  5. clone_size==1 的单克隆对 overall_clone 与 chain_clone 置 NA。
  - 输入：含 master_TRUST_file 的 RDS。
- `spatial_neighborhood/01_spatial_neighborhood.R`（实测头部注释）：
  - 读已 QC、已注释的 Xenium Seurat 对象（需含细胞类型注释列）。
  - 提取组织坐标 → `dbscan::frNN` 固定半径邻域 → 逐细胞邻域细胞类型计数。
  - 输出带邻域计数矩阵的新 Seurat 对象（.rds）。
- 三个脚本头部均有 Description/Input/Output/Usage 注释块——这批小仓里文档写法最规范的一个。
