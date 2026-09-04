# PATTERN-017 · FOV 级幂等断点续跑
- 来源: Moldia/ISS_decoding（LIT-017）ISS_decoding/decoding.py:161-196（process_experiment）
- 场景: 数十个 FOV/切片逐个跑重型解码（或分割），中途崩溃/手工中断后不想从头再来；也便于多机分片。
- 做法: 输出目录本身当任务账本——每完成一个 FOV 落一个 `fov_x.csv`；重跑时 listdir 输出目录解析出已完成的 fov 名集合，与全量 FOV 差集后只跑缺的。骨架：
```python
def process_experiment(exp_path, output, ...):
    experiment = Experiment.from_json(exp_path)
    all_fovs = list(experiment.keys())
    csv_files = sorted(os.listdir(output))
    try:
        fovs_done = list(pd.DataFrame(csv_files)[0].str.split('.', expand=True)[0])
    except KeyError:
        fovs_done = []
    not_done = sorted(set(all_fovs).difference(set(fovs_done)))
    for i in not_done:
        decoded = ISS_pipeline(experiment[i], experiment.codebook, ...)
        df = QC_score_calc(decoded); df.to_csv(output + i + '.csv')
```
- 搬运条件: 仅依赖文件系统；改造点：文件名解析应加正则校验（现实现任何同名杂文件都会被当已完成 FOV——源码 L184 直接 split('.') 取首段）；输出落盘应为原子写（先写临时文件再 rename），防半截 csv 被下次误判已完成。
- 工程评价: 思路简单可靠、代码 5 行搞定，本批 Moldia 三仓中最值得直接抄的小模式；实现粗（无原子性、无校验），照搬思想、重写实现。
- 迭代记录: 2026-09-04 收录(一期精读批次B)
