# PATTERN-014 · 内存感知 tile 缓存 + 并行后处理推理流水线
- 来源: vqdang/hover_net（LIT-081）infer/tile.py:236-387（process_file_list 主循环）
- 场景: 大图/大批 tile 推理时，既要吃满 GPU 又不能把 RAM 撑爆；推理快而后处理（重拼装、分水岭、IO）慢，需要流水线并行。
- 做法: 主循环按 psutil 报告的可用内存 × mem_usage 比例决定本轮缓存几张图（估算系数按模型手调）；缓存图展开成 patch 索引统一过 DataLoader 批推理；推理结果按文件 uid 重新拆分，丢进 ProcessPoolExecutor 并行做 patch 重拼装+后处理+落盘，future 逐个轮询回调。骨架：
```python
while len(file_path_list) > 0:
    available_ram = int(psutil.virtual_memory().available * self.mem_usage)
    while len(file_path_list) > 0:            # 按内存限额缓存文件
        expected_usage = sys.getsizeof(img) * 5
        if available_ram - expected_usage < 0: break
        available_ram -= expected_usage; cache(...)
    for batch in DataLoader(SerializeFileList(cache...), ...):
        sample_output_list = self.run_step(sample_data_list)   # GPU 批推理
    for file in use_path_list:
        proc_pool.submit(_post_process_patches, *func_args)    # CPU 并行后处理
```
- 搬运条件: 依赖 torch/psutil；系数 5 是 HoVerNet 经验值，换模型需重标定（源码 L270 自注释）；Moldia ISS_postprocessing 的 segment_tile 用朴素逐 tile 循环（无内存预算、无流水线）是对照组。
- 工程评价: 工业级；内存预算、断点式缓存、异常轮询（silent crash 检测 L373-386）都考虑到了；import 头部有冗余但主逻辑干净。
- 迭代记录: 2026-09-04 收录(一期精读批次B)
