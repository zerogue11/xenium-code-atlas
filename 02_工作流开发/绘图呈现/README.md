# 绘图呈现层（Figure Grammar Layer）

> **定位：横向呈现层**——绘图不是排在 A9 之后的串行步骤，而是消费所有模块产出的输出层。与范式登记册同构：范式卡管"代码怎么写"，图型卡管"图回答什么问题、跟谁学、怎么画合规"。
> 数据基础：[图形类型书目.csv](../../01_资料库/图形类型书目.csv)（91 篇文献 269 条"绘图借鉴"派生，`scripts/build_figure_catalog.py` 可复跑）。

## 图语法总表（22 类 × 论证链）

| 卡 | 图型 | 频次 | 回答什么问题 | 主工具 | 最佳参考仓 | FigureYa |
|---|---|---|---|---|---|---|
| [V-01](V-01_QC技术评估图.md) | QC 技术评估 | 4 | 这份数据可信吗 | SpatialQM plot 家族 | SpatialQM | 待检索 |
| [V-02](V-02_基准性能对比图.md) | 基准性能对比 | 6 | 方法 A 比 B 好多少 | notebook 流+快照 | ist_benchmarking | 待检索 |
| [V-03](V-03_降维嵌入图UMAP.md) | UMAP/降维嵌入 | 5 | 分几群、谁挨着谁 | scanpy/Seurat | Spatial-TRM | Ya93UMAP |
| [V-04](V-04_细胞比例构成图.md) | 细胞比例构成 | 16 | 各组构成差多少 | bar+检验 | cardiac_sarcoidosis | Ya290BarGraph |
| [V-05](V-05_点图气泡图.md) | dotplot 气泡 | 5 | marker 检出与表达如何 | sc.pl.dotplot | NKTCL | Ya11bubbles |
| [V-06](V-06_热图矩阵图.md) | 热图矩阵 | 9 | 两两关系全景 | PyComplexHeatmap | 3d-analysis | Ya91cluster |
| [V-07](V-07_小提琴箱线图.md) | 小提琴/箱线 | 3 | 分布差异显著吗 | ggplot2 | ST_Comparison | Ya162boxViolin |
| [V-08](V-08_桑基冲积图.md) | 桑基/冲积 | 3 | 单元怎么流动对应 | ggsankey/ggalluvial | LungPCA | Ya25Sankey |
| [V-09](V-09_火山差异统计图.md) | 火山差异 | 4 | 谁显著多了少了 | Milo/DE+空间联 | p53-niche | Ya59volcanoV2 |
| [V-10](V-10_空间基因表达图.md) | 空间基因表达 | 24 | 基因在组织哪儿表达 | sq.pl.spatial_scatter | crohns | Ya239ST_PDAC |
| [V-11](V-11_空间细胞定位图.md) | 空间细胞定位 | 33 | 细胞在哪儿、什么关系 | sq.pl.spatial_scatter | tnbc-chemo | Ya239ST_PDAC |
| [V-12](V-12_空间域生态位分区图.md) | 空间域/生态位 | 27 | 微环境由什么组成 | CellCharter | crohns/p53 | 待检索 |
| [V-13](V-13_细胞邻域共定位图.md) | 邻域/共定位 | 16 | 挨着是随机还是显著 | sq.gr.nhood_enrichment | UCSF colitis | 待检索 |
| [V-14](V-14_距离分箱空间梯度图.md) | 距离分箱/梯度 | 20 | 离结构 X 越近怎么变 | cKDTree+LOESS | crohns/p53/CODEX | 待检索 |
| [V-15](V-15_组织学多模态对齐图.md) | 多模态对齐 | 17 | 分子与形态一致吗 | Explorer 矩阵/VALIS | SPATCH/SpatialQM | 待检索 |
| [V-16](V-16_3D跨切片连续图.md) | 3D/跨切片 | 3 | 2D 盲区 Z 轴真相 | mushroom 体系 | mushroom | 待检索 |
| [V-17](V-17_细胞通讯图.md) | 细胞通讯 | 20 | 谁给谁发信号 | CellChat/circlize | XeniumSpatialMacrophage | Ya14circos |
| [V-18](V-18_轨迹拟时序图.md) | 轨迹/拟时序 | 9 | 状态沿什么路径演化 | scvelo/PAGA | crc-atlas | Ya306slingshot |
| [V-19](V-19_克隆谱系追踪图.md) | 克隆/谱系 | 8 | 克隆空间怎么铺布 | scirpy/inferCNV | CRC_micromets | Ya320Clontype |
| [V-20](V-20_机制流程示意图.md) | 机制/流程示意 | 21 | 数据支持什么模型 | BioRender/Inkscape | （手绘，无仓） | 待检索 |
| [V-21](V-21_多面板组合图.md) | 多面板组合 | 4 | 一页讲完论证链 | gridspec/patchwork | crc-atlas/TRM | 待检索 |
| [V-22](V-22_富集通路图.md) | 富集/通路 | 5 | 这组基因在干什么 | gseapy/decoupler | spatial-brain-vasc | 待检索 |

## 使用方式

1. **出图前**：找到对应图型卡 → 读"回答什么问题"确认这张图在你的论证链里的位置 → 按数据前提核对输入 → 按工具选型+参考仓动手。
2. **画完自检**：对照卡内"zoro-figure 铁律适用条目"编号逐条过（完整规则见 zoro-figure 技能，卡内只列适用条目，单一来源）。
3. **组织纪律**：逐图产出走 PATTERN-045（产数/出图双层）+ PATTERN-050（图号反查手册）+ PATTERN-028（locked 命名）+ PATTERN-006（figures/<图号>/ 落盘）+ 铁律 #9（PNG+PDF+同名 CSV 三件套）。

## FigureYa 模板说明

- 已检索 11 个图族有候选模板 ID（表内"Ya"前缀）；其余图族标注"待检索"并附建议 query。
- **Source Pack 未配置**（目录 319 模板可检索、0 可落地）：materialize 前需先配置 Source Pack；落地时按铁律 13——复制到 scripts/ 微调并注明来源，不自动跑 install_dependencies。
- 检索纪律：figure_library_search 只是排序信号，用前必须 preview 实看打分（8/10 门槛）。

## 迭代

- 新图形类型入库：[迭代入库SOP](../../01_资料库/迭代入库SOP.md) §新图形类型。
- 卡内【待补充】项与参考仓路径以实测为准；修订记 ITERATION_LOG。
