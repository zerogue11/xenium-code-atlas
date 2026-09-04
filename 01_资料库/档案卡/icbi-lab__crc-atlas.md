# `icbi-lab/crc-atlas`（档案卡）

> 由 agent 依据本地克隆实测撰写；不确定处一律【待补充】；禁止编造星标/日期/功能。

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-072：《结直肠癌中性粒细胞表型与空间组织》（Single-cell integration and multi-modal profiling reveals phenotypes and spatial organization of neutrophils in colorectal cancer, bioRxiv 2024.08.26.609563） |
| 精选级 | S |
| 主分类 | P2（复核维持：分类体系 P2 定义明列 crc-atlas——427 万细胞/650 患者 CRC 图谱） |
| 次要用途 | P0（Nextflow DSL2 + Singularity 全容器化图谱构建管线，工程范式标杆）；Xenium/IMC 空间验证分析 |
| 一句话功能 | CRC 单细胞图谱构建与下游分析复现：build_atlas 工作流（scVI/scANVI/scAR/solo 整合注释）+ 9 组下游分析（髓系 cNMF、TCGA 生存、RNA velocity、Xenium 空间、IMC 空间等） |
| License | BSD |
| 语言与规模 | Python×107 / R×13 / Shell×2，46.7 MB（容器与数据不入 git，由下载命令生成） |
| 运行入口 | `run_build_atlas.sh` + `main.nf`（Nextflow，参数 `params_build_atlas.yaml`）；容器 Singularity、依赖 `envs/` conda yaml + `pyproject.toml`；README 自述 build_atlas 需特定 CPU+GPU（Xeon Gold 6342×2 + A100 80GB）才能精确复现 |
| 复现难度 | 高：A100 GPU + Nextflow + Singularity 全栈；scVI/scANVI/UMAP 跨硬件结果会漂移并影响细胞类型标签（README 明示）；zenodo 预计算结果标注"coming soon"（当前状态【待补充】） |
| 与范式的关系 | 管线工程范式首选参考（conf/modules/subworkflows/envs 分层 + 可复现性声明写法）；`60_Xenium_spatial` 分析组可单独借鉴；候选池重点对象 |
| 坑提示 | `params_build_atlas.yaml` 硬编码作者集群绝对路径（/data/scratch/marteau/、/data/projects/2022/CRCA/）；仓内残留 `.nextflow.log`；data/results/containers 目录需下载/运行时生成 |
| 锁定 SHA | 82c15ecc2ea36baa0c4cffe8818bf58e21dcfc48 |

## 结构速览

- `main.nf` + `workflows/build_atlas.nf` + `modules/`、`subworkflows/`、`conf/`：Nextflow DSL2 图谱构建主链。
- `bin/`：scVI.py、scANVI.py、scAR.py、solo.py、gtf_to_table.sh 可执行脚本。
- `analyses/`：01_dataloader → 02_harmonize → 03_qc_and_seed_annotations → 04_tidy_atlas；20_myeloid_cNMF、41_TCGA_survival、42_RNA_velocity、50_Mouse_neutrophils、60_Xenium_spatial、70_IMC_spatial。
- `envs/`、`src/`、`tables/`（HGNC/细胞周期基因/reference_meta 等静态表）。

## 实读要点

- main.nf 实读：仅 include build_atlas 一个 workflow——README 宣称的 downstream_analyses 工作流实际以 `analyses/` 独立分析组形式组织（可直接读预计算结果运行）。
- params_build_atlas.yaml 实读：outdir/tmpDir/external_datasets/own_datasets/annotation 全部指向作者集群绝对路径（/data/scratch/marteau/results/crc-atlas/ 等），移植必须整体改参；hgnc 与细胞周期基因表在 tables/ 内有版本化文件名（hgnc_complete_set_2023-03-02.txt）。
- README 可复现性声明实读：硬件影响 scVI/scANVI 嵌入→连锁影响细胞类型标签，并给出 scanpy issue #2014 讨论；bin/scVI.py 等是工作流调用的独立可执行入口。
- 图谱规模自述：427 万细胞、650 患者、49 研究（77 数据集）、70 亿表达值，交互浏览在 crc.icbi.at（cell-x-gene）。

## 复现路径（怎么跑）

1. 整体复跑：Nextflow+Singularity 环境装好后改 params_build_atlas.yaml 的 5 处绝对路径 → run_build_atlas.sh（需 A100 级 GPU 才能期望标签级一致）。
2. 轻量路线：从 zenodo 取预计算 build_atlas 结果 → 直接跑 analyses/ 各分析组（60_Xenium_spatial、70_IMC_spatial 优先）。
3. 工程参考：不必跑，读 conf/modules/subworkflows/envs 的分层与 src 自定义库写法即可。

## 借鉴与风险

- 可移植点：Nextflow DSL2 + conda yaml + Singularity + "可复现性/硬件声明"四件套是本项目整合 pipeline 的工程对标；analyses 编号目录法（01→70 主题分组）可直接借用。
- 风险：zenodo 预计算"coming soon"若未上线则轻量路线断粮；GPU 漂移导致注释不可比是方法论固有坑。S 级合理；不建议再升格。

