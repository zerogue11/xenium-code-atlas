# V-01 · QC/技术评估图（组别：数据可信）
> 频次: 4/269 条（书目 2026-09-27 口径）｜代表文献: LIT-088、LIT-089、LIT-090

## 这张图回答什么问题（论证链定位）
回答"这份空间数据本身可信吗"：背景噪声有多大、探针特异性够不够、跨平台可比性如何、注释是否稳健。它在论证链最前端，通常出现在结果第一节、方法节末尾或补充图，是后续所有生物学结论的免责前置。单样本场景对应 QC 报告（指标表+图一键产出），多平台场景对应跨平台指标对比与总览表。科学价值在于把"数据能不能用"从口头声明变成可查的定量证据。

## 数据前提
- 细胞级 obs：总 counts、独特探针/基因数、细胞面积（cell_area）、qv 或质量列。

- 阴性对照：NegProbe（Xenium）/NegCode（CosMx）/空白条码（MERSCOPE）计数列，与目标基因探针计数同表才可算 FDR。

- 转录本级坐标：评估转录本扩散/组织外信号时必需（如 SPATCH 的组织外 bin 距离-计数曲线）。

- 平台/样本标签列：供分平台分面对比与总览表并排。

## 工具选型
- py 首选: squidpy/scanpy 算指标 + seaborn 箱线/小提琴分面出图——指标算好后画图很轻，且指标定义透明可改。

- py 备选 / R: R 侧首选 SpatialQM 整包（Seurat 生态，一指标一函数+一键报告），开箱即用但需先读两版本打架的坑。

- 本库参考实现: 01_资料库/精读笔记/Center-for-Spatial-OMICs__SpatialQM.md（指标定义层+plot* 家族逐行实测）。

## 最佳参考仓（实证）
- Center-for-Spatial-OMICs/SpatialQM：R/utils.R:2569-3346 plot* 家族 24 个函数，一指标一箱线图，接受聚合后 tidy df；R/utils.R:3347 generateQCreport_table 出单样本指标表+PDF 报告；R/utils.R:22 getAllMetrics 是批量 QC 编排入口。
  本库价值：整卡搬运"指标定义层"，一指标一函数的结构最值得学（精读笔记总评原话）。

- Moldia/Xenium_benchmarking：xb/preprocessing.py:98 preprocess_adata 尾段批量出 QC 图（counts/UMAP/空间图）后写 h5ad，QC 指标在 xb/_quality_metrics.py。
  本库价值：分析到出图一条链的样板，但需把出图段拆出（见坑 3）。

- zenglab-pku/SPATCH：analysis/4_diffusion.py 量化转录本扩散（组织内外最小距离）；analysis/2_8um_bin.py 做 bin 化+组织外信号去除，直接对应背景定量两步。
  本库价值：扩散与组织外信号两步是其他仓没有的独有模块。

## 文献借鉴要点（书目摘录）
- LIT-088 Fig.1b：把 25 个数据集的来源/组织/panel/reads per cell/genes per cell/qv>20 比例/assign 率并排成 QC 总览表。
  点评：多数据集入场第一表，列选择可直接照抄。

- LIT-089 Fig.2c,d：以阴性对照/空白探针计数与目标基因探针同图对照，定量各平台背景噪声与 FDR。
  点评：背景与信号同图是 FDR 可信的呈现关键。

- LIT-090 Fig.2b,e,f：NegProbe/NegCode 计数加 Moran's I 聚合度量化背景，组织外 bin 距离-计数曲线量化转录本扩散。
  点评：Moran's I 用于背景量化是少见而漂亮的用法。

## 模板候选（FigureYa / Bizard）
- Bizard（R，openbiox，2026-09-27 实查）：[Visdat](https://openbiox.github.io/Bizard/Hiplot/182-visdat.html)（数据质量/类型/缺失概览）、[QQ Plot](https://openbiox.github.io/Bizard/Hiplot/148-qqplot.html)（分布检验）。**无空间 QC 指标专页**——空间 QC 出图仍以参考仓 SpatialQM plot 家族为主。
- FigureYa：待检索，建议 query="quality control metrics QC"（Source Pack 未配置，落地需先配置后 materialize）。

## zoro-figure 铁律适用条目
- 铁律 3：多样本 QC 箱线图 x 轴样本名易挤，零重叠+45° 硬要求。

- 铁律 7：多平台对比统一色族，平台→颜色映射全项目唯一。

- 铁律 8：Arial、mm 定尺寸、6-7pt，QC 图常进补充图也要守。

- 铁律 9：PNG≥300dpi+PDF 成对+同名 CSV 存图内值——QC 指标表本就该交付。

## 常见坑
- SpatialQM 仓"重构到一半"：R/ 下 utils.R 与 utils_update_final.R 两份 3400 行近重复文件互为影子，同名函数按字母序被 update_final 覆盖，实际生效的是带 PanelSize bug 的旧版——搬运必须只取 utils.R 版并补错误上报（精读笔记实读）。

- generateQCreport_table 硬依赖 ControlProbe assay 与 cell_area meta，CosMx 之外平台直接报错（精读笔记实测）：Xenium 复用前先补这两列。

- Moldia preprocess_adata 把分析、绘图、写盘耦合在一函数且 save 默认字符串 'output_path'，重跑代价大：搬图代码时把出图段拆出来单独调。

- 多平台 QC 指标量纲不同（counts vs 面积 vs 比例）不能同 y 轴：一律分面，各面独立坐标。
