# PATTERN-051 · ROI 细胞组成 niche-assay（邻域当 Seurat 对象跑）
- 来源: navinlabcode/tnbc-chemo（LIT-046）相对/路径:行号 `analysis/scripts/spatial_niche/xenium.spatialEcotype.step2a.initiate_niche_assay.R:35-46,100,158-163,180,202`（commandArgs 默认值、NormalizeData、ScaleData(regress nCount_niche)、RunPCA(npcs=30)、FindNeighbors(dims=1:30)）
- 场景: Xenium/影像式空间数据的空间生态型（spatial ecotype）：以 ROI（如 30µm 半径圆窗）内细胞类型组成为特征，把"每个 ROI"当一个细胞、把"各类型组成"当基因，直接复用 Seurat 标准流程发现 niche。想借力成熟 Seurat 工具链（归一化/回归/PCA/聚类/可视化全家桶）时首选。
- 做法: step1 先按半径造 ROI 并统计各细胞类型组成矩阵（freq 与 ncell 双份）→ step2a 把组成矩阵装进 Seurat 对象建 `niche` assay，标准化后回归 ROI 总细胞数（nCount_niche）去测序深度效应，再走 RunPCA→FindNeighbors→聚类得 niche，step2b/2c 跨样本共识成 MetaNiche。
  ```r
  niche_assay <- NormalizeData(niche_assay, assay = "niche")          # :100
  niche_assay <- ScaleData(niche_assay,
      vars.to.regress = c("nCount_niche"))                            # :158
  niche_assay <- RunPCA(niche_assay, npcs = 30)                       # :161-163
  niche_assay <- FindNeighbors(niche_assay, reduction = "pca",
                               dims = 1:30)                           # :202
  ```
- 搬运条件: 依赖 Seurat/R≥4；无许可障碍（Navin 组脚本未见 LICENSE 文件【待补充】，搬运时只借模式重写）。需改造点：①ROI 半径 30µm 是该数据经验值，须扫描（他们 step1 支持多半径）；②freq 矩阵归一化+ncell 回归的组合保留；③输入 df 行名=细胞条码、列=类型名，先做 PATTERN-049 的邻域计数或自己的 ROI 窗口。
- 工程评价: "组成矩阵伪装成表达矩阵进 Seurat"是巧妙的工具复用而非造轮子（对齐用户规则 13 复用优先级）；实现里 `if (!identical(rownames(...)))` 行名对齐兜底（:71-77）值得照抄，作者 HPC 硬编码路径需全换。
- 迭代记录: 2026-09-04 收录(一期精读批次E)
