# 精读笔记 · digitalcytometry__spatialecotyper

- repo: digitalcytometry/spatialecotyper（LIT-047）
- 来源文献: SpatialEcoTyper — 空间生态型（multi-cellular communities）发现与跨模态恢复
- 锁定SHA: 57d37cd2c31c2b0743a7d50e036c4d4a50b61eee（v1.0.4，DESCRIPTION:4）
- 复核分类: 注释/图谱/生态位组 · S 级 · R 包（Stanford 非商业许可，DESCRIPTION:24）
- 精读日期: 2026-09-04（一期精读批次C）

## 代码结构走读

- `R/`：34 个函数一函数一文件，共 4351 行。三条链清晰分层：
  - **发现链**：`PreprocessST.R`(65行,基因/细胞过滤) → `SpatialEcoTyper.R`(195行,单样本主编排) → `GetSpatialMetacells.R`(177行,KNN 加权空间 metacell) → `GetPCList.R`/`GetSNList.R`(分细胞类型 PCA→相似网络) → `SNF2.R`(164行,稀疏矩阵版 SNF 融合) → Seurat `RunPCA/RunUMAP/FindNeighbors/FindClusters` → `AnnotateCells.R`(47行,SE 标签回写单细胞 metadata)。
  - **恢复链**：`NMFGenerateW.R`(255行,分细胞类型训练 NMF W) → `NMFpredict.R`(143行,H=WX 预测) → `RecoverSE.R`(122行,argmax+阈值→SE/NonSE)。
  - **多样本/下游**：`MultiSpatialEcoTyper.R`(144行)、`IntegrateSpatialEcoTyper.R`(270行)、`Colocalization.R`(303行,spdep)、`ComputeNormalizedMoranI.R`(127行)、`SpatialView.R`/`HeatmapView.R`(绘图)。
- `vignettes/`：8 篇 Rmd（单样本发现/积分/bulk-scRNA-scST 恢复/去卷积模型训练），即用户手册。
- `inst/extdata/`：内置 MERSCOPE 训练的默认 W 模型（`MERSCOPE_W_v1.*.rds`）与 SE_CellStates 注释表——恢复链开箱即用（RecoverSE.R:49-52）。

## 关键脚本清单

| 文件 | 一句话 | 行数 |
|---|---|---|
| R/SpatialEcoTyper.R | 单样本主入口：网格化SN→分类型metacell→PCA→SNF→Louvain | 195 |
| R/GetSpatialMetacells.R | 按细胞类型 KNN 加权聚合表达，构造空间 metacell 矩阵 | 177 |
| R/SNF2.R | SNFtool 改造：支持稀疏矩阵/缺失值/minibatch/并行 | 164 |
| R/RecoverSE.R | NMF 模型把单细胞恢复为 SE/NonSE，含 SE01-SE11 映射表 | 122 |
| R/NMFGenerateW.R | 分细胞类型多 seed 训练 NMF，W 矩阵用于恢复 | 255 |
| R/IntegrateSpatialEcoTyper.R | 多样本 SE 整合 | 270 |
| R/Colocalization.R | SE 共定位分析（spdep） | 303 |

## 技术路线还原（勾选实际步骤，按序）

[数据读取(用户传矩阵+metadata必需X/Y/CellType), 质控QC(PreprocessST min.cells/min.features, R/SpatialEcoTyper.R:96-100), 归一化(log1p自动判断 R/SpatialEcoTyper.R:123; Znorm单位方差), HVG(分类型nfeatures=300), 降维(PCA npcs=20), 聚类(Louvain res=0.5 on SNF图), 注释(AnnotateCells SE标签), 空间邻域/域(网格SN+metacell+SNF生态型), 空间统计(Colocalization+Moran I), 多样本整合(MultiSpatialEcoTyper), 绘图(SpatialView/HeatmapView), 导出(saveRDS)] — 共 12 步
未做：去卷积、细胞通讯、亚细胞、配准/3D。

## 入参/出参契约（niche 组重点）

- `SpatialEcoTyper(normdata, metadata)`：入参=基因×细胞的归一化矩阵 + metadata（**必须含 X、Y、CellType 三列**，SpatialEcoTyper.R:102-104 强校验）。
- 出参=list(obj=融合网络的 Seurat 对象, metadata=加 SE 列的单细胞 metadata)；SE 标签为 `NewSE{n}`。
- 恢复链出参=data.frame(CID, CellType, InitSE, SE, PredScore)，低于 min.score 判 NonSE（RecoverSE.R:102-108）。

## 工程审计表（0-2 分/维，共 14）

| 维度 | 分 | 证据 |
|---|---|---|
| ①职责单一 | 2 | 一函数一文件；主入口只编排不实现（SpatialEcoTyper.R:96-187 全部调子函数） |
| ②命名规范 | 2 | roxygen 文档全覆盖（SpatialEcoTyper.R:1-73 含 @return @examples）；PascalCase 统一 |
| ③安全性 | 2 | grep 无硬编码路径/凭据；示例数据走 URL（SpatialEcoTyper.R:52-53） |
| ④最简化 | 1 | SNF2.R:88-94 注释掉的 sum_matrix 死代码；SNF2.R:26,118 冗余 require；RecoverSE.R:45 deprecated 参数残留 |
| ⑤健壮性 | 2 | stop() 校验遍布（SpatialEcoTyper.R:93-104、GetSpatialMetacells.R:62-73）；NaN/Inf 清洗（SNF2.R:110-111）；>1e8 稀疏矩阵降级循环防 NA（GetSpatialMetacells.R:139-155） |
| ⑥可复现性 | 2 | seed 参数化（NMFGenerateW.R:97,110；nmfClustering.R:61）；Seurat v4/v5 分支（SpatialEcoTyper.R:171-174）；project.name 编码全部超参（SpatialEcoTyper.R:181-185） |
| ⑦验证纪律 | 0 | 无 tests/、无 CI（ls 证实）；验证=8 篇 vignette 手工跑通 |

**总分 11/14**

## 可搬运模式

- PATTERN-021 空间生态型发现管线（网格SN→分类型metacell→SNF→Louvain）
- PATTERN-022 NMF 跨模态生态型恢复器（W矩阵+argmax+阈值+NonSE 回退）

## 坑与限制（实读发现）

1. R 包强依赖 Seurat(>=4.2)+NMF，Windows 下 mclapply 退化为串行（parallel 包限制），ncores 参数在 win 上无效。
2. `grid.size = round(radius*1.4)` 网格化会丢弃跨 bin 细胞（SpatialEcoTyper.R:23-25 文档自认），Xenium 单细胞级数据建议先用默认 radius=50 试。
3. RecoverSE 默认模型按 9 种免疫/基质细胞类型（B/CD4T/CD8T/NK/Plasma/Macrophage/DC/Fibroblast/Endothelial）训练，其他组织需自训 W（RecoverSE.R:9-11）。
4. SE01-SE11→SE1-SE9 的 semap 硬编码映射（RecoverSE.R:115-117），换默认模型时必须关闭（传 Ws 走 custom 分支）。
5. 无单元测试，升级 R/Seurat 大版本可能破坏（v5 分支只处理了 data slot 一处）。

## 一句总评

教科书级 R 包工程：入参契约有强校验、超参全部编码进产物名、算法核心（SNF2 稀疏化）有真实改造，是"生态位/生态型发现"模块的参考实现，但零测试、Windows 并行退化需要留意。
