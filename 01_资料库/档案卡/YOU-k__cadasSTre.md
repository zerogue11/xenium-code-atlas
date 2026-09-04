# `YOU-k/cadasSTre`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\YOU-k__cadasSTre`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-085：基于测序的空间方法系统比较。README 原文："cadasSTre is a cross-platform data for sequencing-based ST benchmarking which allows for the evaluation of the performance of each technology in terms of spatial resolution, capture efficiency, and molecular diffusion"（论文题名/期刊【待补充】） |
| 精选级 | A |
| 主分类 | 复核建议改判 P0（方法基准/平台比较类，非疾病应用）——评测 7 种测序式 ST 平台（Dbit-seq、Visium、Stereo-seq、BMKMANU S1000、Slide-seq、Pixel-seq、HDST）的预处理与性能评估，建议终审定夺 |
| 次要用途 | （空） |
| 一句话功能 | 测序式 ST 平台基准测试的预处理+评估脚本集：BAM 清洗/珠条码匹配/白名单生成（dbit）、基因组比对后条码检测计数（dbit.R）、Space Ranger 流程封装（visium_eb1.sh）、Stereo-seq 等平台 BAM→gene-UMI 矩阵（stereoseq.py/select_reads_copy.py）、下游 7 平台降采样与总 counts 等指标比较（evaluation/） |
| License | 无LICENSE(仅可学习不可转载) |
| 语言与规模 | Pythonx8/Rx3/Shellx1；0.7 MB |
| 运行入口 | 按 README 给定顺序执行：bam_barcode_matching.py → dbit.R → visium_eb1.sh → stereoseq.py → select_reads_copy.py；preprocessing/ 下另有 bmk/、slideseq/ 子目录与 steroseq.ipynb |
| 复现难度 | 高 — 各平台原始数据处理需各自上游工具（Space Ranger、比对、参考基因组）与大量原始 BAM/FASTQ；仓内只是脚本层，无流程封装与 env |
| 与范式的关系 | 与本库已有 QuKunLab__SpatialBenchmarking、KChen-lab__ST_Comparison、Moldia__Xenium_benchmarking 同属 P0 基准组；其价值在"测序式平台（dbit/stereo/slideseq）"侧的 BAM 级处理脚本，与 Xenium 主线互补 |
| 坑提示 | ① 评估脚本 readRDS("/path/to/your/data/seu_eye1_list.rds") 为占位路径（样本是视网膜 eye1/eye2 双重复）；② dbit.R 输入参数多（sample ID、参考基因组、注释、索引目录），对接需读脚本；③ 平台缩写命名混乱（stomic/bmk/pixel），配色映射 hardcode |
| 锁定 SHA | 73cb180bf757385f502318c8bbc692e5082397cd（主表） |

## 结构速览

- preprocessing/：dbit.R、visium_eb1.sh、steroseq.ipynb、bmk/、slideseq/（含 zip）
- evaluation/：count_bar_edited.R、list1_edited.R（平台间指标比较与出图）
- README：脚本顺序、输入输出逐条说明（本仓信息最完整的部分）

## README/代码实读要点

- README 以"Script 1~5 + Input/Output 表"格式逐脚本说明，可直接照做
- head evaluation/count_bar_edited.R：定义 7 平台 NPG 配色，读 seu_eye1/eye2_list.rds 汇总 nCount_RNA 并做降采样比较——证实其基准评测属性
- 评测维度（README 原文）：spatial resolution、capture efficiency、molecular diffusion

## 抽读实录

- 读 README 全文；head evaluation/count_bar_edited.R（30 行）；ls preprocessing/evaluation。

## 复用建议

- 归入 P0 基准组档案序列（与 QuKunLab/KChen-lab 并列）；其 dbit/stereo 的 BAM 级脚本仅在用户接触测序式 ST 原始数据时启用；日常 Xenium 工作不依赖。建议主分类终审改 P0。
