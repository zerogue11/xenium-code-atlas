# `cnio-bu/varca`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\cnio-bu__varca`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-054：膀胱癌新辅助免疫选择失败（论文题名/期刊【待补充】；README 未提及论文，只描述管线本身） |
| 精选级 | A |
| 主分类 | 复核维持 P8（膀胱癌研究伴生体细胞变异检测管线；非空间转录组仓） |
| 次要用途 | P0 边缘：可作为通用 WGS/WES GATK 变异检测 Snakemake 模板复用 |
| 一句话功能 | Snakemake 封装的 GATK best-practices 小变异检测管线：mapping→QC→calling（HaplotypeCaller 按 group 分组运行并合并；MuTect2 经 samples.tsv 的 control 列支持不跑/tumor-only/tumor-normal 三种模式）→filtering→annotation→stats 出报告；基于 snakemake-workflows/dna-seq-gatk-variant-calling 模板定制（作者 Elena Piñeiro、Tomás Di Domenico，CNIO） |
| License | MIT |
| 语言与规模 | Pythonx2（scripts/common.py、plot-depths.py，规则主体为 snakemake smk）；4.3 MB；rules/ 7 个 .smk + schemas/envs/report/res 全套 |
| 运行入口 | `snakemake --use-conda -n`（dry-run）→ `snakemake --use-conda --cores N`；config-example.yaml + samples/units/contigs-example.tsv 模板 + schema 校验；支持 qsub/DRMAA 集群与 singularity；.test 目录 + GitLab CI；snakemake min 8.6.0 |
| 复现难度 | 中 — 管线工程规范（模板级：配置校验、dry-run、CI、报告）；难在需自备 WGS/WES fastq、参考基因组与 GATK 资源包；与论文样本的对应关系未在 README 说明【待补充】 |
| 与范式的关系 | 与空间主线关系弱；仅当需要给空间队列配体细胞突变背景（TMB、克隆演化、新抗原）时作为变异检测层引入；作为 Snakemake 管线工程模板质量高 |
| 坑提示 | ① README 是模板原文（GATK workflow 通用说明），论文专属配置与样本表不在仓内；② git 仅 1 个 commit（Update config-example.yaml），无演进历史；③ MuTect2 模式由 control 列约定（"-" / 同名 / 配对名），配置错会静默改变分析模式 |
| 锁定 SHA | 0e6577f98655d10b9032aee33ee90adf5129172a（主表） |

## 结构速览

- Snakefile：min_version 8.6.0、config/samples/units 校验、report/workflow.rst
- rules/：mapping、qc、calling、filtering、annotation、stats、common（7 个 .smk）
- scripts/：common.py、plot-depths.py；config/schemas/envs/res/report/：配置与资源
- .test/ + .gitlab-ci.yml：自带测试样例与 CI

## README/代码实读要点

- README 主体为 snakemake-workflows 模板文档：安装→配置四张表→执行（本地/集群/singularity）→snakemake --report
- samples.tsv 的 group/control 语义是本管线定制核心（README 有三个模式示例表）
- head Snakefile：validate() schema 校验 + miniconda singularity 镜像声明

## 抽读实录

- 读 README 全文；head Snakefile（35 行）；ls rules/scripts；git log --oneline（仅 1 commit）。

## 复用建议

- 留作"需要体细胞突变层"时的即用管线（改 config 即可跑通测试样例）；膀胱癌课题若要做 TMB/突变特征与空间 niches 关联，此仓负责突变检测层。空间组工作流不依赖它。
