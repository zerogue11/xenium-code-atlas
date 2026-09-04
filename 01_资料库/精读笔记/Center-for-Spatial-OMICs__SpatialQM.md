# 精读笔记 · Center-for-Spatial-OMICs__SpatialQM

- repo: Center-for-Spatial-OMICs/SpatialQM
- 来源文献: LIT-028（成像 ST 标准化 QC 指标库；St. Jude Center for Spatial OMICs）
- 锁定SHA: 36e1a59d4ca3f8f360a1d826f5e999d9f40c6760（2026-05-06 "Fix duplicate README.MD/README.md on case-insensitive FS"）
- 复核分类: S 级 / 基准-质控组 / R 包（MIT）
- 语言与体量: R；R/ 共 7053 行（utils.R 3432 + utils_update_final.R 3431 + 辅助 190），tests 33 行，vignettes 3 篇

## 代码结构走读

```
R/coercion-input.R          (93行)  SCE/SPE→Seurat 强制转换 + 平台默认 tx 文件路径解析
R/DependencyPackages.R      (97行)  依赖自动安装脚本（devtools/BiocManager，含 GitHub 包）
R/utils.R                   (3432行) 主实现：读数据→15个get*指标→plot*绘图→报告
R/utils_update_final.R      (3431行) 同上文件的旧版近重复副本（多 get_tx_file/annotateData 两个函数）
tests/testthat/             (33行)  仅 5 个 test_that
vignettes/                  SpatialTouchstone(Rmd) + spatialqm-qc-workflow(Rmd, eval=FALSE)
docs/ + .github/workflows/  pkgdown 站点；CI: R-CMD-check(matrix) + coverage + pkgdown + pr-commands
```

入口链：用户构造 `df_samples`（sample_id/platform/expMat/tx_file/cell_meta 五列样本表）→ `getAllMetrics()` 逐指标 mapply 批算，把结果作为新列写回样本表 → `plotMetrics()`/`generateQCreport_table()` 出图出表。单样本路线：`readSpatial()`（R/utils.R:343，按 Xenium/CosMx/Merscope 分派读 h5/csv → Seurat）→ 各 `get*` 函数。实际通读：getAllMetrics 全文（utils.R:22-240 与 update_final 对应段）、readSpatial docstring、coercion-input.R 全文、generateQCreport_table 全文、tests 全部、两个 utils 的函数清单 diff。

## 关键脚本清单

| 文件 | 行数 | 一句话 |
|---|---|---|
| R/utils.R:22 getAllMetrics | ~280 | 样本表驱动的批量 QC 编排：每指标一个 tryCatch+mapply 块 |
| R/utils.R:343 readSpatial | ~200 | 三平台（Xenium/CosMx/Merscope）统一读入为 Seurat 并补 meta |
| R/utils.R:672-2568 get* 家族 18 个 | 各~90-160 | nCells/GlobalFDR/TxPerArea/TxPerNuc/信号噪比/MECR/Sparsity/Entropy/Complexity/Morans/ARI/NMI/RCTD… |
| R/utils.R:2569-3346 plot* 家族 24 个 | 各~35 | 每指标一个箱线图函数，接受聚合后的 tidy df |
| R/utils.R:3347 generateQCreport_table | ~85 | 单样本指标表+PDF 报告（依赖 ControlProbe/cell_area） |
| R/coercion-input.R | 93 | SCE/SPE→Seurat 强制转换 + 平台默认 tx 路径推断（.default_tx_file_for_platform） |
| R/DependencyPackages.R | 97 | 运行时自动 install.packages（工程反模式，见审计） |

## 技术路线还原（勾选自固定清单，按实际顺序）

1. 数据读取（readSpatial 三平台归一，readTxMeta 解析转录本表）
2. 质控QC（15 项核心指标：nCells/specificityFDR/TxPerCell/TxPerArea/TxPerNuc/SigNoiseRatio/CellTxFraction/DynamicRange/MECR/Sparsity/Entropy/Complexity/GlobalFDR/MeanExpression/MaxExpression/PanelSize）
3. 注释（辅助性：annotateData 参考映射 + getPseudobulk，供相关性指标用）
4. 去卷积（可选指标：getRCTD/getMaxRCTD，spacexr）
5. 空间统计（getMorans，Moran's I，Voyager）
6. 绘图（plot* 家族 24 函数）
7. 导出（generateQCreport_table 指标表 + PDF）

未做：归一化/HVG/降维/聚类（getClusterMetrics 只对**已有**聚类算 ARI/NMI，不执行聚类）/空间邻域/细胞通讯/亚细胞/配准3D/多样本整合（多样本=批算而非整合）。

## 工程审计表（7 维，0-2 分）

| 维度 | 分 | 证据 |
|---|---|---|
| ①职责单一/模块化 | 1 | 一指标一函数结构好（R/utils.R:672-2568）；但 getAllMetrics ~280 行巨型编排，且 R/ 下两份 3400 行近重复文件互为影子版本（utils.R 与 utils_update_final.R diff 仅差 2 函数），同名函数按字母序被 update_final 覆盖 |
| ②命名规范 | 2 | get*/plot*/read* 前缀一致（R/utils.R:672, 2616）；utils.R 新版改用具名列访问 df_samples$expMat（R/utils.R:40） |
| ③安全性 | 2 | 无硬编码绝对路径、无凭据；路径全部来自 df_samples 参数 |
| ④最简化 | 0 | 双版本冗余 3400 行；update_final 内 Sparsity 算两遍（R/utils_update_final.R:202,228）、PanelSize 误调 getSparsity（:239） |
| ⑤逻辑健壮性 | 1 | utils.R 有 .validate_sample_metrics_df 列校验（tests/testthat/test-inputs.R:2-6 证明）+ getPanelSize stop 校验（R/utils.R:2412）；但 tryCatch 吞错误仅 cat（R/utils_update_final.R:57-59），失败留 NA 不上报 |
| ⑥可复现性 | 1 | DESCRIPTION 声明 Imports 但无版本锁；R/DependencyPackages.R:1-9 运行时自动 install.packages 破坏环境确定性；CI matrix 多版本（.github/workflows/R-CMD-check.yaml:24） |
| ⑦验证纪律 | 1 | 4 个 CI workflow 齐备，但测试仅 33 行 5 个 test_that（tests/testthat/），test-utils.R 是 2*2=4 占位测试 |

**总分 8/14**

## 可搬运模式

- PATTERN-001（QC 指标库单指标单函数，与 Moldia xb/_quality_metrics.py 对照登记）
- PATTERN-002（样本表驱动批量 QC 编排 + 单指标失败隔离）

## 坑与限制（实读发现）

1. **两版本并存且覆盖方向反直觉**：utils.R 是重构版（具名列、校验、message），utils_update_final.R 是旧版；R 包按文件名拼载，update_final 后载入覆盖 utils.R 的同名导出——即**带 PanelSize bug 的旧版实际生效**（R/utils_update_final.R:239 `df_samples$PanelSize <- mapply(getSparsity,...)`，应为 getPanelSize；utils.R:271-272 是对的）。tests 里的列校验断言也因此会失败。
2. 位置索引 df_samples[,3]/[,5]（update_final 版全篇）与文档承诺的五列强耦合，列序一变全错。
3. getGlobalFDR 在编排里被调了两次（specificityFDR 与 GlobalFDR 两次 mapply），同一指标重复计算。
4. vignette 全部 eval=FALSE（vignettes/spatialqm-qc-workflow.Rmd:13），文档示例未验证执行。
5. generateQCreport_table 硬依赖 `ControlProbe` assay 与 `cell_area` meta（R/utils_update_final.R:3366-3369），CosMx 之外平台直接报错。

## 一句总评

指标定义层（一指标一函数+平台归一读入）值得整卡搬运，但仓库自身处于"重构到一半、新旧两版打架"状态，搬运时必须只取 utils.R 版并补齐错误上报。
