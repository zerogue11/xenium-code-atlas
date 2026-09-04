# `Woopsydaisy/Spatial-Human-Kidney-Map`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\Woopsydaisy__Spatial-Human-Kidney-Map`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-048：糖尿病肾病空间图谱（DKD；论文题名/期刊【待补充】，README 以方法模块为主未列论文信息） |
| 精选级 | A |
| 主分类 | 复核维持 P8（糖尿病肾病 CosMx+Xenium 双平台疾病图谱） |
| 次要用途 | P0 边缘：SCIB 整合方法基准（Harmony/Scanorama/scVI/pyliger 对比）；NicheCompass/COVET/Hotspot 三个 niche 方法的并列实操 |
| 一句话功能 | DKD 人体肾空间图谱全流程：A AtoMx/Xenium 导出与 QC → B CosMx/Xenium 分别对 SN 参考图谱 scVI/scANVI 整合、最终三数据联合+注释+补算 → C SCIB 多方法基准 → D niche 分析（邻居 DF→kmeans→注释→CellPhoneDB→严重度相关→pseudobulk DESeq2）→ E NicheCompass → F COVET+Hotspot → G/H/I/J 小管损伤/免疫/B 细胞四个专题微环境模块 |
| License | 无LICENSE(仅可学习不可转载) |
| 语言与规模 | Pythonx57/Rx1；0.5 MB；每脚本在 README 中标注运行容器（docker://10jll/spatial:version2、10jll/scvi_cuda12:version4、10jll/cellphonedb:version1、10jll/nichecompass:version1） |
| 运行入口 | 按字母分目录的编号 Python 脚本（部分 R/Colab）；docker 容器指定；数据获取方式【待补充】（README 未给 GEO/链接） |
| 复现难度 | 中-高 — 脚本编号顺序、容器镜像、模块划分都极清晰（同类仓中工程性最好之一）；难在依赖 4 个自建 docker 镜像是否可拉取【待补充】与数据自备 |
| 与范式的关系 | 本批应用仓中"图谱级整合+niche 方法全家桶"最全：scVI/scANVI 注释补算、20um 邻域、CellPhoneDB、NicheCompass、COVET/Hotspot 全部并列可对照选型；候选池（高优先） |
| 坑提示 | ① docker://10jll/* 镜像为作者自建，公开可拉性未验证【待补充】；② SCIB 与部分 Hotspot/DESeq2 脚本标注"Google Colab 运行"，本地化需改；③ AtoMx 导出是 CosMx 特有前置，无 AtoMx 账号需走公开数据 |
| 锁定 SHA | 8ddde5d6ed285c5c742a733d3cd9f251e554b758（主表） |

## 结构速览

- A Exporting Spatial Data/：CosMx 2 脚本 + Xenium 导出，生成 h5ad+QC
- B Integration/：CosMx/Xenium 各自 SCVI-SCANVI 过滤 → 最终合并注释+补算；C SCIB/：4 脚本方法基准
- D Niche_Analysis/：9 脚本（邻居→kmeans→CellPhoneDB→相关性→DEG→pseudobulk）
- E Nichecompass/（3 脚本）、F COVET/（4 脚本）、G~J 专题（小管/免疫/B 细胞）、K Miscellaneous

## README/代码实读要点

- README 即完整脚本目录手册：57 个脚本逐一给出"容器 + 一句话功能"
- 整合主线明确用 SN（单核）参考图谱做 SCANVI 注释并向空间补算（imputation），CellPhoneDB 全部基于补算表达
- 严重度关联（Script6_correlation）把 niche 互作打分与疾病程度挂钩，是疾病叙事的量化钩子

## 抽读实录

- 读 README 全文；ls 11 个顶层目录。

## 复用建议

- 建议作为"多平台疾病图谱+niche 方法选型"的对照手册使用：D 模块（邻居 kmeans niche + CellPhoneDB + 严重度相关）最贴近用户 Xenium 主线，可先移植；E/F 模块按 zoro-spatial 选型需要再评估。A 级中质量突出，建议考虑升 S。
