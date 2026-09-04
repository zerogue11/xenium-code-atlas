# 精读笔记 · hisplan/sharp

- repo: https://github.com/hisplan/sharp
- 来源文献: LIT-078 / SCING（Single-Cell pIpeliNe Garden）生态样本解混管线（README:23-24 明确归属 SCING；MSKCC dp-lab）【待补充正式发表条目】
- 锁定SHA: `68e7268744f886b1df4cd4ce5c76355d913fb581`（2022-05-18）
- 复核分类: 管线工程组 · WDL/Cromwell 样本解混（Hashtag/CiteSeq/AsapSeq/CellPlex 四模式）· **全库工程对照重点** · MIT（LICENSE）

## 代码结构走读（实际读了什么）

三层结构：主工作流 WDL（815 行 shell/wdl）+ 16 个模块 WDL + 每模块 docker + shell 运维层：
- 主工作流（4 个 Assay 模式）：`Hashtag.wdl`（185 行）imports 6 个模块（Preprocess/HtoDemuxSeurat/HtoDemuxKMeans/Combine/AnnData/BasicQC，:3-8），input 块集中声明全部参数（含 `Map[String,Int] resourceSpec` 内存自动估算约定 `memory:-1`，:58-60；`String dockerRegistry`，:63），`parameter_meta` 给参数写 help（:65-67），条件分支 `if (runSeuratDemux == true)` / `if (defined(denseCountMatrix))`（:114,125），output 块固定契约枚举全部产物（:143-168）。`CiteSeq.wdl`（105 行）、`AsapSeq.wdl`（168 行）、`Hashtag.wdl` 同构。
- `modules/Preprocess.wdl`：子工作流复用 8 个任务模块（MergeFastq→FastQC→Cutadapt→CutInDropSpacer→PrepCBWhitelist→CountReads/Count→AnnData），R1/R2 用同一 MergeFastq 模块别名两次调用（`as MergeFastqR1`）。
- `modules/HtoDemuxKMeans.wdl`（75 行）：task 模板范本——input 块、parameter_meta、`String dockerImage = dockerRegistry + "/hto-demux-kmeans:0.5.0"`（:17，版本钉死）、`command <<< set -euo pipefail ... >>>`（:20-33）、output 三件（classification/stats/log，:36-40）、runtime（docker/cpu/memory，:42-47）。
- 配置层 `configs/`：**三文件配置**——`*.inputs.json`（数据参数：s3 fastq、read 结构 cbStartPos/cbEndPos/umiStartPos/umiEndPos、whitelist、resourceSpec、dockerRegistry）+ `*.labels.json`（Cromwell 元数据：pipelineType/project/sample/owner/destination）+ `Sharp.options.aws.json`/`gcp.json`（引擎选项：cache 开关、`workflow_failure_mode: ContinueWhilePossible`、`maxRetries: 3`）。7 组 Assay× chemistry 组合各一对。
- 运维层 shell：`validate.sh`（49 行）——**womtool 校验矩阵**：4 个工作流 × 7 组 inputs.json 逐一 `java -jar ${SCING_HOME}/devtools/womtool.jar validate`（开头检查 SCING_HOME 缺失即退，:4-7）；`run-tests.sh`（36 行）用 configs/devtest/ 真云冒烟提交；`submit-hashtag.sh` 等 4 个（38 行）统一 getopts 接口（-k key/-i inputs/-l labels/-o options）→ `cromwell-tools submit`；`make-deployable.sh`（68 行）版本化打包 `sharp-0.1.1.tar.gz` + 可选 S3 发布 + 生成 install.sh。
- 模块 docker：`dockers/<module>/` 各含 Dockerfile + build.sh + push.sh + config.sh + 源码（如 hto-demux-kmeans 的 `demux_kmeans.py`/`dna3bit.py`）。
- 测试层：`tests/test.<Module>.wdl` ×13——每模块一个薄包装 workflow（只 import 单模块并透传 IO），配 `test.<Module>.inputs.json`，实现模块级隔离回归；`pytest.ini` 仅覆盖 `dockers/hto-adt-postprocess`（容器内 python 函数测试）。`manual-inspection/` 11 个 QC/重跑 notebook 是"计划-验证"痕迹；`docs/understanding-outputs-*.pdf` 输出契约文档。

## 关键脚本清单

| 文件 | 行数 | 一句话 |
|---|---|---|
| Hashtag.wdl | 185 | 主工作流范本：6 模块编排+条件分支+固定输出契约 |
| modules/Preprocess.wdl | ~300 | 子工作流：merge→QC→trim→whitelist→count→AnnData |
| modules/HtoDemuxKMeans.wdl | 75 | task 模板范本：版本钉死 docker+set -euo pipefail+三输出 |
| validate.sh | 49 | womtool 校验矩阵（7 组合静态校验） |
| run-tests.sh | 36 | devtest 输入真云冒烟（AWS Cromwell） |
| make-deployable.sh | 68 | 版本化 tarball + S3 发布 + install.sh 生成 |
| configs/*.inputs.json | - | 数据参数与引擎参数全外置（三文件配置） |

## 技术路线还原（固定清单勾选）

1. **数据读取**（S3 fastq/whitelist/taglist，inputs.json 声明）
2. **质控QC**（FastQC html + CountReads count report + BasicQC notebook/html 报告，Hashtag.wdl:135-141）
3. **注释**（HTO 解混赋予样本来源标签+双联体判定，HtoDemuxKMeans/CorrectFalsePositiveDoublets）
4. **导出**（AnnData h5ad、count matrix、classification tsv、stats yml，output 块固定契约）

**骨架步骤数：4**（处理链是 fastq 级的：merge→trim→count→demux→AnnData→QC 报告）。

## 工程审计表（7 维 × 0-2，共 13/14）

| 维度 | 分 | 证据 |
|---|---|---|
| ①职责单一/模块化 | 2 | 4 主工作流×16 模块全部可独立测试/复用（tests/test.*.wdl 逐模块包装）；docker 按模块拆 7 个 |
| ②命名规范 | 2 | workflow/task PascalCase、输出 outClass/outStats/outLog 三件套一致（HtoDemuxKMeans.wdl:36-40）；configs 命名 `<assay>-<chemistry>` 规整 |
| ③安全性 | 2 | 凭据外置 `~/keys/*.json` 走 submit 脚本 -k 参数（submit-hashtag.sh:24）；inputs.json 用 `s3://.../` 占位；dockerRegistry 参数化不写死 |
| ④最简化 | 2 | 815 行 shell 总量零死代码；4 个 submit-*.sh 是刻意并列的薄包装而非复制粘贴逻辑 |
| ⑤逻辑健壮性 | 2 | command 内 `set -euo pipefail`（HtoDemuxKMeans.wdl:20）；memory=-1 触发自动估算（Preprocess.wdl:54）；validate.sh 环境变量缺失即退出（:4-7）；options maxRetries=3 |
| ⑥可复现性 | 2 | docker 镜像版本钉死 `:0.5.0`（:17）；三文件配置全外置；make-deployable.sh 版本号化部署（:4）；options.json 缓存策略显式 |
| ⑦验证纪律 | 1 | 校验矩阵+真云 devtest+13 个模块包装测试+QC notebook 痕迹俱在；但全为手动脚本、无 CI 接线，pytest.ini 仅覆盖 1/7 容器 |

## 可搬运模式

- PATTERN-039：womtool 校验矩阵（validate.sh）。
- PATTERN-040：三文件配置（inputs/labels/options）+ 版本化部署（make-deployable.sh）。
- PATTERN-041：模块级容器工厂（dockers/<module>/ 五件套 + WDL 内版本钉死）。

## 坑与限制（实读发现）

- 强绑定 SCING 环境：`SCING_HOME`、cromwell-tools、AWS secrets 全是外部前提，脱离其集群要重写 submit 层。
- 静态校验只保证 WDL+inputs 类型吻合，语义正确性靠 run-tests.sh 烧真钱（AWS Cromwell），无本地 tiny-data 回归。
- `pytest.ini` 与 13 个 WDL 包装测试并存但互不接线，测试入口割裂。
- 2022 年停更（最后提交 2022-05），WDL 1.0 语法老练但依赖的 docker 镜像版本需自维护。
- 输出契约依赖 PDF 文档（docs/*.pdf）而非机器可读 schema，程序化校验产物契约要自己写。
- KMeans 与 Seurat 双解混并行是设计冗余（可选项），但两套结果的合并逻辑留给下游。

## 一句总评

全库工程对照标杆名副其实：配置-代码-容器-校验四分离 + 固定输出契约 + 校验矩阵，把"参数在哪、镜像哪个版本、怎么验、怎么发版"四问全部落到了文件；扣一分只因验证全靠手动脚本而非 CI。
