# `hisplan/sharp`（档案卡）

> 由 agent 依据本地克隆实测撰写；不确定处一律【待补充】；禁止编造星标/日期/功能。

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-078：《胰腺癌祖细胞生态位》——本仓为该研究使用的样本解混管线；与 dpeerlab/p53-niche-dynamics 同论文不同仓（后者为空间 niche 动力学），互为对照 |
| 精选级 | S |
| 主分类 | P0（复核改判，主表初判 P8）——通用单细胞样本解混流程（Hashtag/CITE-seq/ASAP-seq/CellPlex），非疾病应用分析代码，归"流程"更贴切 |
| 次要用途 | 工程化对照范本；P8 场景中作上游样本解混步骤 |
| 一句话功能 | SCING（Single-Cell pIpeliNe Garden）生态内的 WDL/Cromwell 解混管线：barcode/UMI 校正定量 + 样本归属解混 + 跨样本双联体识别（CITE-seq 除外） |
| License | MIT |
| 语言与规模 | Shell x36 / Python x27（主表口径；主体为 WDL：4 顶层 workflow + 16 任务模块）；83.9MB（含 deps.zip 与 tutorial 数据） |
| 运行入口 | `./submit-*.sh -k secrets -i inputs -l labels -o options`（cromwell-tools 提交）；QC 手动生成 `manual-inspection/run.sh -t type -w workflowID`；依赖 scing conda、SCING_HOME、Cromwell 服务与云 secrets |
| 复现难度 | 高 — 强依赖 SCING 基础设施（cromwell 服务器、AWS/GCP 服务账号、womtool.jar），README 明示"假设已配置 SCING" |
| 与范式的关系 | **本批唯一 S 级工程范本，供管线工程对照**。候选池：工程做法对照（非空间流程本身） |
| 坑提示 | ① 输出说明仅一份 2021 PDF；② run-tests.sh 引用的 configs/devtest/ 未见【待补充】；③ cromwell-tools 旧 API 兼容需自验；④ memory=-1 自动估算有时不够 |
| 锁定 SHA | 主表未登记（空）；本地克隆 HEAD `68e7268744f886b1df4cd4ce5c76355d913fb581` |

## 结构速览

- 顶层 `Hashtag.wdl / CiteSeq.wdl / AsapSeq.wdl`：三个主 workflow（CellPlex 走同套模块）。
  - WDL 1.0；`import "modules/..." as <别名>` 组合；输入含 uriFastqR1/R2、R1/R2 长度、
    细胞条码白名单、`translate10XBarcodes`（TotalSeq-A false / B、C true）等开关。
- `modules/`：16 个任务 WDL——Preprocess、Cutadapt、MergeFastq、ReformatFastq、CountReads、
  Count、PrepCBWhitelist、TranslateBarcodes、CutInDropSpacer、HtoDemuxKMeans、HtoDemuxSeurat、
  BasicQC、SanityCheck、Combine、FastQC、AnnData（覆盖 10x/InDrop 两种平台与 TotalSeq-A/B/C）。
- `configs/`：7 种试剂盒场景的 inputs/labels 成对 JSON。
  - hashtag-10x-v3-tsa/tsb/tsc、hashtag-indrop-methanol、citeseq、asapseq-tsa、cellplex。
  - inputs 内含资源声明（如 `"Hashtag.resourceSpec": {cpu:4, memory:-1}`）。
- `dockers/`：每工具一目录（basic-qc、cite-seq-count、cut-indrop-spacer、hto-adt-postprocess、
  hto-demux-kmeans、hto-demux-seurat、seqkit），各含 Dockerfile + build.sh + push.sh + config.sh。
- `tests/`：每模块一对 test.<Module>.wdl + inputs.json（PrepCBWhitelist 有 3 套 inputs），
  附 run-test.sh / run-all-tests.sh / validate.sh / zip-deps.sh。
- `manual-inspection/`：9+ 个 QC/排查 notebook（hashtag 分类 v1/v2、citeseq 检查、
  kmeans 重跑、dna3bit.py 条码工具）+ run.sh（papermill 生成）。
- `tutorial/`：process-sharp-output.ipynb/html + 示例 3168_example_HTO.h5ad.gz。
- 顶层脚本：submit-*.sh 四件套、validate.sh（womtool 校验）、make-deployable.sh、run-tests.sh、
  Sharp.options.aws.json / Sharp.options.gcp.json、Sharp.deps.zip、pytest.ini、requirements.txt。

## 工程对照要点（供 02_工作流开发参考）

- **配置三分离**：inputs（数据与资源）/ labels（工作流标签）/ options（Cromwell 策略）。
- **Cromwell 策略集中**：`maxRetries:3`、`workflow_failure_mode: ContinueWhilePossible`、
  `write_to_cache: true`、`read_from_cache: false`，AWS/GCP 各一份 options。
- **校验矩阵**：validate.sh 用 womtool 对 7 种试剂盒配置逐一校验同一 workflow。
- **测试分层**：模块级 WDL 测试（tests/）+ docker 内 Python 单测（pytest，仅 hto-adt-postprocess）。
- **部署脚本化**：make-deployable.sh 内写死版本号 0.1.1，
  打包 submit 脚本 + WDL + deps.zip 到 $HOME/scing/bin 或 S3。
- **QC 闭环**：v0.1.0 起管线自动生成 QC notebook；手动兜底走 manual-inspection/run.sh。
