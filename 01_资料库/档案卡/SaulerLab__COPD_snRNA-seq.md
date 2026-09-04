# `SaulerLab/COPD_snRNA-seq`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\SaulerLab__COPD_snRNA-seq`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-069：COPD（慢阻肺 snRNA-seq 研究；论文题名/期刊【待补充】，README 未给出） |
| 精选级 | A |
| 主分类 | 复核维持 P8（COPD 肺病应用，与用户肺课题近亲） |
| 次要用途 | P0 边缘：NB-GLMM 细胞比例建模 + NicheNet LR 推断 + Xenium 双变量局部 Moran's I 空间验证的组合方法学 |
| 一句话功能 | COPD snRNA-seq 四模块分析：① 1_clustering 按细胞型比例对患者聚类；② 2_mediation WGCNA + 四组中介分析（总/年龄/肺功能/合并）；③ 3_LR_CCC NB-GLMM sender-receiver 建模 + NicheNet 受者/发送者分析（shell 并行作业）；④ 4_spatial_LR_validation 用 Xenium 数据对 LR 互作做双变量局部 Moran's I 空间验证 |
| License | MIT |
| 语言与规模 | Rx11/Shellx1；0.1 MB；四目录各 1~5 个脚本 |
| 运行入口 | R 脚本/Rmd 逐模块运行；3_LR_CCC 有 nbglmm_job_parallel.sh 作业脚本；数据与 env 均未随仓【待补充】 |
| 复现难度 | 高 — 模块结构清晰但无数据、无 env、无 README 运行顺序说明；NicheNet 先验数据库与 NB-GLMM 依赖需自行配置 |
| 与范式的关系 | "snRNA 发现→比例聚类→中介分析→LR 推断→Xenium 空间验证"完整叙事链是该仓最大价值；其中 4_spatial_LR_validation/LocalMoran.R 体量小、可独立移植到 zoro-spatial 作 LR 空间验证工具；候选池 |
| 坑提示 | ① 论文与数据入口缺失，需从 LIT-069 文献侧补齐；② WGCNA+中介分析对样本量与生物学重复敏感，移植时注意单重复禁 q/p 话术的全局规则；③ shell 并行脚本假定 HPC 环境 |
| 锁定 SHA | b08ed795d162635425ca07f35169adc3766e9e96（主表） |

## 结构速览

- 1_clustering/：01_functions.R + 02_cluster_5.Rmd（按细胞比例聚类患者）
- 2_mediation/：01_wgcna.R + 02~05 四组 mediation（base/age/pro/age×pro）
- 3_LR_CCC/：01_nbglmm_functions.R、02 并行 shell、03 NicheNet RO（receiver-oriented）、04 NicheNet SO（sender-oriented）
- 4_spatial_LR_validation/：LocalMoran.R（Xenium 双变量局部 Moran's I）

## README/代码实读要点

- README 按四模块给出脚本清单与一句话功能，无版本/数据/环境信息
- 空间验证明确写出方法名"bivariate local Moran's I on Xenium"，是仓内唯一空间分析件

## 抽读实录

- 读 README 全文；ls 四个子目录。

## 复用建议

- 重点抽 4_spatial_LR_validation/LocalMoran.R（小而独立）作为 LR 空间验证候选工具；3_LR_CCC 的 NB-GLMM+NicheNet 组合可在有足够样本量时参考。复现全流程不推荐（缺数据缺环境）。
