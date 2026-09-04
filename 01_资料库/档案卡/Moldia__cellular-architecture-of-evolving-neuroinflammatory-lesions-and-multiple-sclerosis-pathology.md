# `Moldia/cellular-architecture-of-evolving-neuroinflammatory-lesions-and-multiple-sclerosis-pathology`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\Moldia__cellular-architecture-of-evolving-neuroinflammatory-lesions-and-multiple-sclerosis-pathology`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-017：MS 病理。英文原题（README 原文）"Cellular architecture of evolving neuroinflammatory lesions and multiple sclerosis pathology"（bioRxiv 2023.06.29.547074；配图标注 Cell 2024；Zenodo 10.5281/zenodo.8037425） |
| 精选级 | A |
| 主分类 | 复核维持 P8（神经炎症/MS 疾病应用；ISS+Xenium 双平台） |
| 次要用途 | P0 边缘：ISS（原位测序）上游处理链在作者另 4 个仓库（ISS_CARE/preprocessing/decoding/postprocessing），本仓为下游 |
| 一句话功能 | EAE 小鼠 + 人 MS 尸检脊髓的单细胞空间病理图谱复现：processing/ 15 个 notebook（CARE 图像恢复、ISS 解码格式化、主聚类、病理 compartments、边界距离、多边形生成/绘制）、visualization/ 6 个逐图 notebook（FIGURE1~7）；数据（52 小鼠 + 6 人样本 adata/转录本/DAPI）在 Zenodo，另有 TissUUmaps 在线浏览 |
| License | 无LICENSE(仅可学习不可转载) |
| 语言与规模 | Pythonx25（全部 ipynb）；14.8 MB |
| 运行入口 | Jupyter notebook 逐个运行；环境【待补充】（无 yaml/requirements）；ISS 上游需另部署作者系列仓 |
| 复现难度 | 高 — 原始测序数据数 TB 不提供（作者明说），Zenodo 只给 adata+转录本+mask；作者原话"notebooks 供透明性，不保证对你能跑通"；上游 ISS 管线散在 5 个兄弟仓 |
| 与范式的关系 | "疾病邻域/病理 compartments（active/inactive lesion 解卷积）+ 距软膜边界距离分析"范式对 TME 分区分析可类比借鉴；Xenium_benchmarking 兄弟仓是方法学参考；候选池（疾病分区叙事） |
| 坑提示 | ① 依赖链长：本仓只覆盖下游，CARE/解码/分割在 Moldia/Lee_2023 等仓（含 PDF 手册）；② 无 env 文件；③ 人样本仅 6 切片，属描述性分析，注意单生物学重复语境下的统计话术 |
| 锁定 SHA | a9869c66c0d1965e00d4938d6fd79554fce78703（主表） |

## 结构速览

- processing/：CARE、DECODING、SPACETX_FORMAT、MAIN_CLUSTERING、HM_MS_CLUSTERING、COMPARTMENTS、DISTANCE_FROM_BOUNDARY、GEN_POLYGONS、PLOT_POLYGONS、INGEST/DENOVO_EAE_INGEST、CALCULATE_COMPARTMENT_AREA、Resize_*_DAPI
- visualization/：FIGURE1/2/4/5/6/6_7.ipynb 逐图复现
- images/：图形摘要与图版 PNG；数据本体在 Zenodo + TissUUmaps 门户

## README/代码实读要点

- README 明确数据处理上游归属（4 个 ISS 仓 + Lee_2023 手册 PDF）并建议参考其 Xenium_benchmarking 预印本
- 数据格式为 anndata（兼容 scanpy/squidpy）；小鼠含每样本 transcript 文件+DAPI+mask，人仅转录本+cell-by-gene
- 免责声明原文："These notebooks are supplied for transparency, and we cannot guarantee that they will work flawlessly for you."

## 抽读实录

- 读 README 全文；ls processing/（15 项）与 visualization/（6 项）；未深读 notebook 内部（作者已声明透明性优先）。

## 复用建议

- 取其 compartments/边界距离两个分析概念映射到肿瘤 niche；复现优先用 Zenodo adata + visualization notebook，不碰 ISS 上游。关联仓 Moldia__Xenium_benchmarking 本库已有档案卡，可配套阅读。
