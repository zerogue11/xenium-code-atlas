# `10XGenomics/HumanColonCancer_VisiumHD`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\10XGenomics__HumanColonCancer_VisiumHD`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-026：结直肠癌免疫细胞 VisiumHD。英文原题 "High definition spatial transcriptomic profiling of immune cell populations in colorectal cancer"（Oliveira et al., Nat Genet 2025, s41588-025-02193-3；GSE280318；10x 官方作者团） |
| 精选级 | A |
| 主分类 | 复核维持 P8。注意：平台为 Visium HD（8um/2um bin 化 FFPE 数据），非 Xenium，作为平台差异参照仓使用 |
| 次要用途 | P2 边缘：StarDist 核分割→bin 条码映射；修改版 spacexr 大规模去卷积（PR#206） |
| 一句话功能 | Visium HD FFPE 结直肠癌 TME 图谱复现代码：Methods（Flex 单细胞 Seurat v5 sketch analysis 采样 15% 再外推、spaceXR 去卷积、StarDist H&E 核分割并输出 bin→nuclei 映射 CSV）+ Figures（逐图复现脚本）+ MetaData（现成的 8um bin 去卷积/注释 parquet 可直接加载） |
| License | MIT |
| 语言与规模 | Rx18/Pythonx1；202.1 MB（本批最大，ext/ 与 Figures 中间文件占量） |
| 运行入口 | R 脚本（Methods 先行产出 → Figures 引用）；NucleiSegmentation.py 用 conda env_nucleisegmentation.yml（NucleiSeg env）；数据从 10x 官网 dataset 页/GEO 下载 |
| 复现难度 | 高 — 全流程需 cellranger aggr + Space Ranger 输出 + 修改版 spacexr + StarDist GPU 分割；但MetaData parquet + 每图脚本开头的 SampleData 模板 data.frame 使"只复现出图"可行 |
| 与范式的关系 | Visium HD 平台参照主件：bin 级去卷积（singlet/doublet 分类）、肿瘤周缘 50um 定义、巨噬亚群（SELENOP+/SPP1+）空间 niche 分析；Flex 参考→HD 去卷积链路与 zoro-spatial 的注释列契约可对照；候选池 |
| 坑提示 | ① 平台差异：Visium HD 无 Xenium 式单细胞分割，分析对象是 bin，去卷积质量依赖参考；② spacexr 用的是改动源码的版本（dmcable/spacexr PR#206），原版可跑但慢；③ Figures 依赖 Methods 产物，不能直接跑；④ 路径为 ~/VisiumHD/... 模板 |
| 锁定 SHA | df5801cf5e681b33b5026626989a7635fdf26b99（主表） |

## 结构速览

- Methods/：AuxFunctions.R、FlexSingleCell.R（sketch analysis）、Deconvolution.R（spaceXR）、NucleiSegmentation.py + environment_nucleisegmentation.yml
- Figures/：按图编号的复现脚本（依赖 Methods 输出）
- MetaData/：SingleCell_MetaData.csv.gz + P1CRC_Metadata.parquet（8um bin 全注释，含 DeconvolutionClass/Label1/2、Periphery、MacrophageSubtype）
- ext/、Team/、Figures 资源：图片与团队页，202 MB 体积主要来源

## README/代码实读要点

- README 给出 parquet 12 列的完整 schema（arrow::read_parquet），是 bin 级注释列设计的现成模板
- Flex 处理明确用 Seurat v5 sketch-based analysis（采样 15%≈37k 细胞后外推全量），可迁移到大数据场景
- bioRxiv 版本有 git tag（releases/tag/bioRxiv）可对照新旧代码

## 抽读实录

- 读 README 全文（含 Methods 各脚本参数说明与包列表）；未深读 Figures 内脚本（README 已声明其依赖 Methods 产物）。

## 复用建议

- 若用户接触 Visium HD 样本：按"Flex 参考→spaceXR 去卷积→bin 注释 parquet→周缘/亚群空间分析"顺序抄 Methods；StarDist 分割脚本可独立用于 H&E 核分割需求。与 Xenium 主线并行时注意单位/粒度差异。
