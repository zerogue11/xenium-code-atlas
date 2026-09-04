# `christophhmayr/2023_Mayr`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\christophhmayr__2023_Mayr`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-004：特发性肺纤维化病理生态位。README 原文："Code for the spatial transcriptomic paper on IPF lungs"（Mayr et al. 2023；期刊【待补充】；Visium processed counts Zenodo 10.5281/zenodo.10012934，整合 PF-ILD atlas 10.5281/zenodo.10015169） |
| 精选级 | A |
| 主分类 | 复核维持 P8（IPF 肺纤维化疾病应用，与用户肺课题近亲） |
| 次要用途 | P2 边缘：cell2location 注释迁移、CytAssist Visium 整合、衰老打分、Rings 邻域等 notebook 级方法示范 |
| 一句话功能 | IPF Visium 空间病理生态位 notebook 集（10 个 final_*.ipynb）：cell2location 注释迁移的相关性验证、CytAssist Visium 与 atlas 整合（niche 频率、功能 niche 富集、细胞衰老签名打分、Rings 空间邻域、邻域互作）、CellChat IPF vs healthy 配对处理与分析、IPF atlas 子集出图 |
| License | 无LICENSE(仅可学习不可转载) |
| 语言与规模 | Pythonx10（全部 notebook）；32.4 MB；README 极简（4 行） |
| 运行入口 | Jupyter notebook 逐个运行；无 env 文件【待补充】；部分 notebook 因体积限制另存 Zenodo（10.5281/zenodo.10012934） |
| 复现难度 | 中 — Zenodo 有 processed count tables + PF-ILD atlas，输入可得；notebook 命名即功能；缺环境声明与 cell2location/scanpy 版本 |
| 与范式的关系 | IPF niche 分析的"细胞型比例→niche 富集→衰老签名→Rings 邻域→邻域互作→CellChat"链条与用户肺纤维化/COPD 组分析高度相关；notebook 侧 cell2location 用法参考；候选池 |
| 坑提示 | ① 无 LICENSE；② 文件名 final_ 前缀但无编号，执行顺序需按依赖推断；③ 部分 notebook 在 Zenodo 不在仓内，对照论文图版时需去 Zenodo 找全；④ 32 MB 体积可能含 notebook 输出 |
| 锁定 SHA | 6ea419ffd2ece3774a6cca8b2c860fb819658109（主表） |

## 结构速览

- final_cytassist_human_visium_integrate_*.ipynb（6 个）：ct_percentages_perNiche、frequencies、functional_Niche_enrichment、senescence_signaturescoring、spatial_neighbourhood_Rings、spatial_neighbourhood_interactions
- final_CellChat_IPFhealthy_processing.ipynb / _analysis.ipynb：CellChat 配对
- final_correlation_c2l_annotations_labeltransfer.ipynb：cell2location 注释迁移验证
- final_IPFatlas_subsetted_plots.ipynb：atlas 子集出图

## README/代码实读要点

- README 仅题名、一张论文图、Zenodo 两个 DOI（counts 与 atlas、部分 notebook 存档）
- notebook 命名自释功能，覆盖 niche 分析全套件，是"读 notebook 学方法"型仓

## 抽读实录

- 读 README 全文；ls 顶层（10 notebook，全部 final_ 前缀）。

## 复用建议

- 与本库 COPD/IPF 组（Spatial_PF、SaulerLab）并列阅读；senescence 打分 + Rings 邻域两个 notebook 可直接作 zoro-spatial IPF 支线方法候选；复现从 Zenodo counts 起步可行。
