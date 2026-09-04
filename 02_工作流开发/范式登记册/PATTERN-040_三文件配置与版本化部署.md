# PATTERN-040 · 三文件配置（inputs/labels/options）+ 版本化部署
- 来源: hisplan/sharp（LIT-078）相对路径:行号 `configs/hashtag-10x-v3-tsa.inputs.json、configs/hashtag-10x-v3-tsa.labels.json、Sharp.options.gcp.json、make-deployable.sh:4-68`
- 场景: 管线要被多人/多样本/多环境复用时，"数据参数、运行元数据、引擎选项"三类东西混在代码或单一 config 里，迟早变成谁都不敢动的 YAML。
- 做法: 按变更频率拆三份 JSON，随每个 Assay×chemistry 组合成对存放：(1) `*.inputs.json`——每次运行都变的数据参数（fastq 路径、read 结构、资源规格）；(2) `*.labels.json`——谁在跑/什么项目/输出去哪（Cromwell 元数据，用于账单与检索）；(3) `options.json`——几乎不变的平台级引擎选项（缓存开关、失败模式 ContinueWhilePossible、maxRetries=3）。提交脚本用统一 getopts（-k 凭据 / -i inputs / -l labels / -o options）穿针引线。发布走 `make-deployable.sh`：读 `wf_name+version` 变量 → rsync 白名单文件 → tar.gz 到 $SCING_HOME/bin → 可选推 S3 并生成一行安装命令，版本号即回滚单元。
  ```bash
  wf_name="sharp"; version="0.1.1"
  files="submit-hashtag.sh ... Hashtag.wdl configs/*.json"
  rsync -Rv ${files} ${workdir}/${wf_name}-${version}/
  tar cvzf ${dest}/${wf_name}-${version}.tar.gz ${wf_name}-${version}/*
  # cromwell-tools submit --inputs-files X.inputs.json --label-file X.labels.json --options-file options.json
  ```
- 搬运条件: 纯 bash+JSON，MIT 可自由搬；对接 omicOS 时三文件思想可映射为 run_yaml(数据)/HANDOFF(元数据)/engine_profile(引擎)；需改造点：version 从硬编码改为 git tag 读取。
- 工程评价: "按变更频率分离配置"这一刀切得极准，inputs/labels 成对出现防漏填；部署脚本白名单制（不打包杂物）也值得学（13/14）。
- 迭代记录: 2026-09-04 收录(一期精读批次D)
