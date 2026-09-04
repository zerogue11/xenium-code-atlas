# PATTERN-023 · Nextflow JUPYTERNOTEBOOK 包装器（jupytext+papermill+nbconvert+versions.yml）
- 来源: icbi-lab/crc-atlas（LIT-072）相对/路径:行号 — modules/local/jupyternotebook/main.nf:15-77；analyses/03_qc_and_seed_annotations/*.py 经 subworkflows/Integrate_datasets.nf:20-25 以别名复用
- 场景: 工作流引擎（Nextflow）需要执行分析脚本/笔记本并要求：参数免转义注入、产物归档、执行报告（HTML）、运行环境版本留痕——"分析即报告"的场景。
- 做法: 定义一个通用 JUPYTERNOTEBOOK 进程：输入=(meta, notebook, parameters, files)；隐式注入 cpus/artifact_dir/input_dir/meta 参数到 .params.yml（免 CLI 转义，支持嵌套 map）；jupytext 把 py/Rmd 转 ipynb → papermill 参数化执行 → nbconvert 导出 HTML → 写 versions.yml 记录工具版本；artifacts/* 作为输出发射给下游进程。
```groovy
nb_params["cpus"] = task.cpus; nb_params["artifact_dir"] = "artifacts"
params_cmd = dump_params_yml(nb_params)          # 参数落 yaml，免转义
jupytext --to notebook --output - --set-kernel ${kernel} ${notebook} > ${notebook}.ipynb
papermill -f .params.yml ${notebook}.ipynb ${notebook}.executed.ipynb
jupyter nbconvert --stdin --to html --output ${prefix}.html < ${notebook}.executed.ipynb
cat <<-END_VERSIONS > versions.yml   # 每 process 版本留痕
```
- 搬运条件: 依赖 jupytext/papermill/nbconvert 三个工具在同一容器内；Nextflow>=23.04；需为每个 notebook 步骤建 meta(id)；同一进程体以 `JUPYTERNOTEBOOK as XXX` 别名复用十几次（Integrate_datasets.nf:20-31），报错经 papermill 栈难读。
- 工程评价: 版本留痕（versions.yml）与"参数 dump 到 yaml"两处是可直接抄的细节；别名复用让 analyses/ 下 17 个脚本全部纳入工作流编排；缺点是死代码注释多、报告型验证无法断言。
- 迭代记录: 2026-09-04 收录(一期精读批次C)
