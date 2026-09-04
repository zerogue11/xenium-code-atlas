# PATTERN-016 · ASHLAR CLI 函数化封装 + 分段 conda 环境流水线
- 来源: Moldia/ISS_preprocessing（LIT-017）ISS_processing/preprocessing.py:314-403（ashlar_wrapper）、installation.sh:1-31
- 场景: 上游工具（ashlar/bigwarp 等科研软件）只提供 CLI 入口，需要嵌进自己的 python pipeline 又不想 shell 外调；多环节依赖互相冲突时分环境串联。
- 做法: 把 CLI 脚本的 main 逻辑复刻成 wrapper 函数：参数逐一对齐 CLI 旗标（align_channel→--align-channel 等），内部直接 import 模块调 process_single/process_plates，错误也沿用其 ProcessingError 分支返回码；环境层面按"preprocessing→decoding→postprocessing"拆三个 conda env（1_/2_/3_ 前缀 + 各自 yml 全版本锁），installation.sh 一键克隆三仓+建三环境+注册 ipykernel。骨架：
```python
def ashlar_wrapper(files, output='', align_channel=1, maximum_shift=500,
                   filter_sigma=5.0, filename_format='Round{cycle}_{channel}.tif', ...):
    aligner_args = {'channel': align_channel, 'max_shift': maximum_shift,
                    'filter_sigma': filter_sigma, 'verbose': not quiet}
    mosaic_path_format = str(pathlib.Path(output) / filename_format)
    return ashlar.process_single(filepaths, mosaic_path_format, flip_x, flip_y,
                                 ffp_paths, dfp_paths, aligner_args, mosaic_args,
                                 pyramid, quiet)
```
- 搬运条件: 依赖 ashlar==1.13.1（API 与当前版不兼容，必须连 yml 一起搬）；改造点：wrapper 里 `tile_size = tile_size`（L347-349）等死代码应删；三环境切换可换成 uv 隔离环境（zoro 规则 15）。
- 工程评价: 封装思路正确（避免 subprocess 解析文本输出），版本锁完整是 Moldia 三仓最强项；但 wrapper 未被测试覆盖，错误处理仅透传。
- 迭代记录: 2026-09-04 收录(一期精读批次B)
