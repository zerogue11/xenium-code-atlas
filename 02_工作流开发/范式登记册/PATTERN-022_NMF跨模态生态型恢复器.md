# PATTERN-022 · NMF 跨模态生态型恢复器（W 矩阵库 + argmax + 阈值回退 NonSE）
- 来源: digitalcytometry/spatialecotyper（LIT-047）相对/路径:行号 — R/RecoverSE.R:39-122；R/NMFGenerateW.R:97-110；R/NMFpredict.R
- 场景: 已在参考数据（MERSCOPE 短读长）上定版生态型后，把同一套生态型标签恢复到新模态（scRNA、Visium、其他 ST panel）——即"生态型列"的跨模态迁移。
- 做法: 按细胞类型分别训练 NMF，把 W 矩阵（基因×SE特异状态）存成模型库随包分发；预测时取交集基因、必要时自动 log2(x+1)、对每类细胞算 H=WX，argmax 取生态型，PredScore 低于 min.score 或映射表外的状态一律回退 NonSE。
```r
Ws <- lapply(list.files(system.file("extdata",package="SpatialEcoTyper"), "MERSCOPE_W_v1.*.rds", full.names=TRUE), readRDS)
if(all(dat>=0) & max(dat)>80) dat <- log2(dat+1)          # 输入量纲自动探测
H <- NMFpredict(Ws[[ct]], tmpdat, scale=TRUE, sum2one=TRUE)
assignRes$SE     <- colnames(resDF)[apply(resDF,1,which.max)]
assignRes$PredScore <- apply(resDF,1,max)
assignRes$SE[assignRes$PredScore < min.score] <- "NonSE"  # 阈值回退
```
- 搬运条件: 分发的是"每细胞类型一个 W 矩阵"而非端到端模型；新组织需用 NMFGenerateW 自训（多 seed，:97-110）；默认模型限定 9 种免疫/基质类型；Stanford 非商业许可。
- 工程评价: 恢复契约清晰（出参 CID/CellType/InitSE/SE/PredScore 五列，RecoverSE.R:102-106），量纲自动探测（:76-79）与未预测细胞补零（:93-99）细节到位；但 SE01-SE11 semap 硬编码（:115-117）换模型时必须走 custom 分支绕开。
- 迭代记录: 2026-09-04 收录(一期精读批次C)
