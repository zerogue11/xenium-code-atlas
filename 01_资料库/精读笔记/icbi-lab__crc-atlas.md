# 精读笔记 · icbi-lab__crc-atlas

- repo: icbi-lab/crc-atlas（LIT-072）
- 来源文献: Marteau et al. 2025 bioRxiv — 427 万细胞/650 患者/49 研究 CRC 单细胞图谱
- 锁定SHA: 82c15ecc2ea36baa0c4cffe8818bf58e21dcfc48
- 复核分类: 注释/图谱/生态位组 · S 级 · Nextflow DSL2 工作流（nf-core 风格自建）
- 精读日期: 2026-09-04（一期精读批次C）

## 代码结构走读

- 入口链：`main.nf`(8行) → `workflows/build_atlas.nf`(23行) 顺序串 3 个子工作流：
  `Load_datasets`（装载各数据集 h5ad+GTF 表）→ `Integrate_datasets`（核心）→ `Tidy_atlas`。
- `subworkflows/Integrate_datasets.nf`：scAR 去环境 RNA → 合并 → 细胞周期打分 → 按样本类型（tumor/normal/blood/metastasis/lymph_node/BD）分头 HVG → 种子注释 → SCVI_SEED → SOLO 双细胞 → SCVI → SCANVI → neighbors/leiden/UMAP。过程编排全在 DSL2 channel 上完成。
- `modules/local/`：两种模块范式并存——(a) `.nf` 进程包脚本（scVI.nf/scANVI 同文件、solo.nf、scAR.nf、neighbors_leiden_paga_umap.nf）；(b) **`jupyternotebook/main.nf`(77行) 通用 JUPYTERNOTEBOOK 进程**，把 analyses/ 下的 py 脚本当"notebook"经 jupytext→papermill→nbconvert 执行并导出 HTML 报告。
- `analyses/`：按 01_dataloader→03_qc_and_seed_annotations→04_tidy_atlas 编号放脚本；下游 9 组（20_myeloid_cNMF、41_TCGA_survival、42_RNA_velocity、60_Xenium_spatial、70_IMC_spatial 等）。
- `bin/`：scVI.py/scANVI.py/solo.py/scAR.py（各约 100 行 argparse CLI）；`src/`：sc_atlas_helpers+spatial_helpers 两个自建库。
- `conf/`：base.config（资源/容器）+ build_atlas.config；`envs/`：conda yaml + .def 容器定义双轨。

## 关键脚本清单

| 文件 | 一句话 | 行数 |
|---|---|---|
| workflows/build_atlas.nf | 三子工作流顺序编排 | 23 |
| subworkflows/Integrate_datasets.nf | 12 步整合主链（scAR→HVG→seed→SCVI→SOLO→SCANVI） | ~230 |
| modules/local/jupyternotebook/main.nf | papermill notebook 通用执行器，产 HTML+versions.yml | 77 |
| modules/local/scVI.nf | SCVI/SCANVI 双进程，GPU label，环境变量注入 | 70 |
| bin/scVI.py | set_all_seeds 全链确定性（含 use_deterministic_algorithms） | 112 |
| analyses/60_Xenium_spatial/01-05*.ipynb | Xenium 下游：预处理/注释/nichecompass/niches/出图 | 5 篇 |
| conf/base.config | GPU label cpus=12 固定为 scVI 可复现 | 74 |

## 技术路线还原（勾选实际步骤，按序）

[数据读取(Load_datasets 77 数据集), 质控QC(scAR环境RNA、Filter_mito、SOLO双细胞), 归一化(脚本内), HVG(按6类样本分头选), 降维(PCA/scVI), 聚类(neighbors_leiden_paga_umap), 注释(Get_seeds→scANVI 标签迁移), 空间邻域/域(仅下游 Xenium：nichecompass/niches), 多样本整合(scVI batch 核心), 绘图(notebook HTML), 导出(h5ad publishDir)] — 共 11 步
未做：去卷积、细胞通讯、亚细胞、空间统计、配准/3D（下游 60/70 号分析内部分涉及，主链不做）。

## 工程审计表（0-2 分/维，共 14）

| 维度 | 分 | 证据 |
|---|---|---|
| ①职责单一 | 2 | main.nf 8 行纯编排；进程/子工作流/脚本三层解耦（workflows/build_atlas.nf:11-23） |
| ②命名规范 | 2 | analyses/NN_ 前缀编号；进程名全大写动词；README 结构说明书逐条对应 |
| ③安全性 | 0 | params_build_atlas.yaml:2-8 硬编码 /data/scratch/marteau 与 /data/projects/2022/CRCA；conf/base.config:5 容器绝对路径 |
| ④最简化 | 1 | base.config:21-29 注释掉的 RMARKDOWN 块；scVI.nf:21-24 `OMP_NUM_cpus` 等无效环境变量拼写（OMP_NUM_cpus≠OMP_NUM_THREADS） |
| ⑤健壮性 | 1 | checkIfExists（Integrate_datasets.nf:63）、errorStrategy finish、cache lenient；无断言式 channel 校验 |
| ⑥可复现性 | 2 | NXF_VER=23.04.0 锁定（run_build_atlas.sh:3）；容器 def+yaml 双轨（envs/）；base.config:35 "cpus=12 For scVI reproducibility"；README 专节讨论 GPU 硬件敏感性 |
| ⑦验证纪律 | 1 | 每 process 产 versions.yml（jupyternotebook/main.nf:70-75）；无 CI/测试 |

**总分 9/14**

## 可搬运模式

- PATTERN-023 Nextflow JUPYTERNOTEBOOK 包装器（jupytext+papermill+nbconvert+versions.yml）
- PATTERN-024 scVI→scANVI 种子注释迁移链（seed annotation 先行再标签迁移）

## 坑与限制（实读发现）

1. 路径全面绑定作者集群（scratch/marteau），复现必须改 params_build_atlas.yaml + base.config 容器路径两处。
2. JUPYTERNOTEBOOK 把 .py 当 notebook 跑依赖 jupytext 转换，报错栈经过 papermill 难读；HTML 报告是唯一"验证痕迹"。
3. 下游 analyses/ 的 notebook 未接入 nextflow（60_Xenium_spatial 手工跑），管线只管 build_atlas 主链。
4. scVI/scANVI 进程 label gpu 但 nextflow.config 里 singularity `--no-home`，自建容器内 torch 版本与 def 文件耦合。
5. README 明示：换硬件重跑 build_atlas 可能改变细胞标签——即注释结果非硬件无关，引用其标签时要注意。

## 一句总评

427 万细胞级图谱工程的优秀编排范本：DSL2 分层+notebook 报告化+容器双轨都值得抄，但个人集群硬编码使其"可复现性"停留在方法学层面，落地需换路径重配。
