# 精读笔记 · KChen-lab__ST_Comparison

- repo: KChen-lab/ST_Comparison
- 来源文献: LIT-089（Nat Commun s41467-025-63414-1，FFPE 肿瘤 TMA 上 CosMx/MERFISH/Xenium 三平台对照）
- 锁定SHA: e3a3256875cbf210b2090051de73d3bcbc730723（2026-08-31 "Update README.md"）
- 复核分类: S 级 / 基准-质控组 / R 脚本（28 个，851 行）
- 语言与体量: R；6 个 Seurat 处理脚本 + 20 个图脚本 + Annotations/ 8 个注释 RDS；共 4.7MB

## 代码结构走读

```
Seurat/{Xenium,CosMx,MERFISH}_{ICON,MESO}.R   6 个脚本 = 3 平台 × 2 数据集（肺腺癌 ICON / 间皮瘤 MESO），
                                               每个脚本独立完成该平台该数据集的全部处理
Figures/Figure_*.R + Supp*.R                  20 个与论文图号一一对应的 ggplot 片段脚本
Annotations/*.rds + READ.me                   各平台各样本的细胞类型注释结果（论文交付物，非代码）
```

入口链：没有统一入口。6 个 Seurat 脚本各自从 LoadXenium/LoadNanostring/ReadVizgen 起步，走完全同的 Seurat 标准链（QC→Normalize→HVG→PCA→Harmony→UMAP→聚类→marker→saveRDS）；图脚本假定全局环境里已有 `ST`、`mycols` 等对象，不能独立运行。实际通读：Xenium_MESO.R、CosMx_ICON.R、MERFISH_ICON.R 全文；Figure_2b.R、Figure_4a.R、Supp_Fig_1a.R 全文；README 全文。

## 关键脚本清单

| 文件 | 行数 | 一句话 |
|---|---|---|
| Seurat/Xenium_MESO.R | 65 | 双切片 Xenium 读入→合并→Harmony 整合→0.8 聚类→FindAllMarkers |
| Seurat/CosMx_ICON.R | 77 | CosMx 读入+背景矩阵、nCount>30 与面积<5×几何均值两道 QC→Harmony 链 |
| Seurat/MERFISH_ICON.R | 46 | ReadVizgen 读入+Blank 探剔除→无 Harmony 的单样本 PCA/UMAP/聚类 |
| Figures/Figure_2b.R | 17 | 13 样本 counts 箱线图（因子 levels 硬编码样本名） |
| Figures/Figure_4a.R | 42 | 各平台 vs bulk RNA-seq 的逐平台 Pearson 散点（ggscatter） |
| Figures/Supp_Fig_1a.R | 26 | disjoint marker 共表达箱线图 + wilcox 显著性条 |

## 技术路线还原（勾选自固定清单，按实际顺序）

1. 数据读取（LoadXenium / LoadNanostring / ReadVizgen 三平台分装）
2. 质控QC（Xenium nCount>10；CosMx nCount>30 + 面积<5×几何均值；MERFISH nCount>10 + Blank-* 探剔除）
3. 归一化（LogNormalize, scale.factor=10000）
4. HVG（vst, nfeatures=1000）
5. 降维（PCA npcs=30）
6. 聚类（FindNeighbors + FindClusters resolution=0.8）
7. 多样本整合（Harmony 按 Slide_ID；MERFISH 单样本线无此步）
8. 绘图（20 个图脚本）
9. 导出（saveRDS 主对象；注释以 RDS 交付）

未做：注释（脚本内不执行注释，Annotations/ 是外部产物直接发布）、去卷积、空间邻域/域、细胞通讯、亚细胞、空间统计、配准3D。（FindAllMarkers 属 marker 检出，清单无对应项，不计。）

## 工程审计表（7 维，0-2 分）

| 维度 | 分 | 证据 |
|---|---|---|
| ①职责单一/模块化 | 1 | 平台×数据集脚本化分工清楚、无共享代码文件（零函数抽象，全线性脚本）；Annotations 与代码分离是亮点 |
| ②命名规范 | 1 | 图脚本与图号对应（Figure_2b.R）；但 "Figures/Figure 2a.R" 文件名带空格、slide_ID/Slide_ID 大小写混用（CosMx_ICON.R:21 vs 44） |
| ③安全性 | 2 | 仅占位路径 "/path to data/"（Xenium_MESO.R:10），无凭据、无机器路径 |
| ④最简化 | 1 | 851 行 28 文件已很精瘦；但 11a-11d 四个补充图脚本 16 行同构复制、Figure_2b.R:6-8 levels 里 Xenium_UM_Meso1 写了两遍 |
| ⑤逻辑健壮性 | 0 | **语法错误两处**：Xenium_MESO.R:13 多余右括号、:17 缺右括号（脚本不可运行）；**复制粘贴错误两处**：Xenium_MESO.R:36 `AddMetaData(MESO1,...)` 应为 MESO2、CosMx_ICON.R:33 `subset(Icon1,...)` 赋给 Icon2；零断言零校验 |
| ⑥可复现性 | 1 | 图脚本有 set.seed(2023)（Figure_2b.R:1）但 Figure_4a.R:2 写成 20203；README 给出三个 GEO 登录号；无 renv/版本锁、无环境文件 |
| ⑦验证纪律 | 0 | 无 CI 无测试；语法错误证明脚本提交前从未执行过 |

**总分 6/14**

## 可搬运模式

- 无独立 PATTERN 卡（本仓方法学是 Seurat 官方标准链的逐平台实例化，无新范式）；其"每个处理脚本硬编码样本名后逐段复制"恰是 PATTERN-002（样本表驱动）要反例规避的做法。

## 坑与限制（实读发现）

1. 四处语法/逻辑错误意味着这些脚本只是**论文方法的文字化记录**，不是可执行代码；复现必须自行修错。
2. 图脚本依赖未定义的全局对象（ST、mycols、ICON2_D_M），且无 ggsave——只展示不落盘。
3. CosMx 的 ICON2 实际被用 Icon1 过滤两次的结果（CosMx_ICON.R:33），按此脚本得到的 ICON2 分析结论与论文可能不一致【待补充：论文端如何处理未查证】。
4. 无 config：样本名、阈值（10/30 counts、5×geomean）、分辨率 0.8 全部散落硬编码在各脚本。

## 一句总评

三平台 QC 阈值差异（counts 阈、面积过滤、Blank 剔除）与"注释结果单独成目录交付"是本仓仅有的可提炼资产，代码本身是未经运行的论文附件。
