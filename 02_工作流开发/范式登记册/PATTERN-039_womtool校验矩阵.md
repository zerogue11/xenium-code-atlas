# PATTERN-039 · womtool 校验矩阵（工作流 × 输入组合静态校验）
- 来源: hisplan/sharp（LIT-078）相对路径:行号 `validate.sh:1-49`
- 场景: 有多个主工作流、每个工作流多套合法输入组合（不同试剂盒/化学/参数形态）时，改了 WDL 或 inputs 后需要一种零成本的"改动即验"，把类型错误挡在提交集群之前。
- 做法: 一个 shell 脚本穷举 `工作流 × inputs.json` 的全部合法组合，逐个调 `womtool validate <wf.wdl> --inputs <json>`；脚本开头先断言引擎环境变量存在，任一组合失败即非零退出。矩阵列在脚本里即文档——读者一眼看清支持哪些组合（如 Hashtag×TSA/TSB/TSC/InDrop、CiteSeq、AsapSeq、CellPlex）。
  ```bash
  if [ -z $SCING_HOME ]; then echo "'SCING_HOME' not defined."; exit 1; fi
  java -jar ${SCING_HOME}/devtools/womtool.jar validate \
      Hashtag.wdl --inputs ./configs/hashtag-10x-v3-tsa.inputs.json
  # …继续穷举其余 6 个组合，任一失败即失败
  ```
- 搬运条件: 需 Java+womtool（Cromwell 发行版自带）；MIT 可自由搬；需改造点：改成 CI 步骤（GitHub Actions 每 PR 跑一遍）即从"手动纪律"升级为"自动门禁"；CWL 侧对应 `cwltool --validate`，snakemake 侧对应 dry-run，思想同构。
- 工程评价: 49 行换来"改坏必报"的静态门禁，是 sharp 全仓性价比最高的文件；缺 CI 接线是其未得满分之处（13/14 总评中的 ⑦=1 由此而来）。
- 迭代记录: 2026-09-04 收录(一期精读批次D)
