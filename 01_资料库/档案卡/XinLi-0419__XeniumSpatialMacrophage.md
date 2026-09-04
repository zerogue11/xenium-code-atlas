# `XinLi-0419/XeniumSpatialMacrophage`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\XinLi-0419__XeniumSpatialMacrophage`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-077：肺间质巨噬细胞亚群（论文题名/期刊【待补充】；仓内无任何文献信息） |
| 精选级 | B |
| 主分类 | 复核维持 P8（肺部巨噬细胞 Xenium 应用，但仓内容仅 1 个工具函数） |
| 次要用途 | P2 边缘：Xenium subset 后转录本坐标同步过滤的实用工具 |
| 一句话功能 | 单文件工具仓：Xenium_image.susbet.R 定义 image.subset() 函数——用 sf 读 cell_boundaries 多边形，把 Seurat Xenium 对象 subset 后 @images[["fov"]]@molecules 里仍属全量切片的转录本坐标按"点在多边形内"过滤，解决 ImageFeaturePlot 在子集对象上仍画全片转录本的问题 |
| License | 无LICENSE(仅可学习不可转载) |
| 语言与规模 | Rx1；0.0 MB（约 56 行 R） |
| 运行入口 | source() 引入后对 Seurat Xenium 对象调用 image.subset()；依赖 sf/dplyr/purrr |
| 复现难度 | 低 — 纯函数、逻辑自包含；但需自备 Xenium Seurat 对象与 cell_boundaries.csv.gz |
| 与范式的关系 | 直接补 zoro-spatial 工具箱的已知坑（Seurat subset 不同步转录本坐标）；函数注释把问题机理讲清楚了 |
| 坑提示 | ① 函数硬编码 @images[["fov"]]（多 FOV 对象需循环改写）；② 假定 cell_boundaries 为 csv.gz 且列名 vertex_x/vertex_y（标准 Xenium 输出格式）；③ 文件名拼写 susbet（subset 之误）；④ 仓内无 README/License/论文信息，作者意图需从文献侧补 |
| 锁定 SHA | b67288e5441ffb479ff32ee32de88693e455f9a2（主表） |

## 结构速览

- Xenium_image.susbet.R：唯一文件，image.subset() 函数（56 行）
- 无 README、无 LICENSE、无数据

## README/代码实读要点

- 文件头注释（原文翻译）：Seurat 默认 subset 不修改转录本空间坐标，画转录本级图（ImageFeaturePlot）时仍显示全量转录本；需自定义空间过滤
- 实现：cell_boundaries → group_by(cell_id) 闭合多边形 → st_polygon → st_join 点-多边形内连接 → 按 subset 后 colnames 过滤 → 回写 @coords

## 抽读实录

- 读 Xenium_image.susbet.R 全文（56 行，全读）。

## 复用建议

- 可直接把 image.subset() 抄入 zoro-spatial 工具库（改名为 xenium_subset_transcripts，补多 FOV 支持与容错）；B 级合理（单函数仓）。
