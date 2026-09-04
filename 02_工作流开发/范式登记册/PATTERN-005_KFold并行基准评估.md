# PATTERN-005 · KFold 交叉验证 + 进程池并行的基准评估驱动

- 来源: QuKunLab/SpatialBenchmarking（Nat Methods 2022）BLAST_GenePrediction.ipynb 代码单元 9-13（KFOLD + multiprocessing.Pool(10)）
- 场景: 插补/预测类方法的公平比较：把已知基因切成 train/test 折，逐折训练-预测-评分；数据集多、方法多、折多时用进程池把"折"维并行掉，单机即可跑完整基准。
- 做法: 先用 KFold 生成 train_list/test_list 的折索引列表；每个方法定义一个只吃折号 K 的顶层函数（数据经 global 注入 worker）；`Pool.map` 按折并行，结果按列拼接落盘。四指标评分（SSIM/PCC/RMSE/JS）由独立 count 类对 raw vs impute 逐基因计算。
  ```python
  KFOLD = list(range(len(train_gene)))            # train_gene: KFold 切好的折列表
  with multiprocessing.Pool(10) as pool:
      result = pd.concat(pool.map(SpaGE_impute, KFOLD), axis=1)  # 每折返回 test 基因×spot 矩阵
  result.to_csv(outdir + "/SpaGE_impute.csv", header=1, index=1)
  # GenesMetrics.count 类随后逐基因算 SSIM/PCC/RMSE/JS
  self.impute_count = self.impute_count.fillna(1e-20)   # NaN 消毒后再评分
  ```
- 搬运条件: 依赖 multiprocessing/pandas/scikit-learn；需改造点——①global 变量注入 worker 是 fork-only hack，跨平台或改 spawn 模式需改传参或用共享内存；②**KFold 必须加 random_state**（原实现无 seed，折划分不可复现，这是其基准结论的硬伤）；③Pool 大小应按 CPU 数配置而非硬编码 10。
- 工程评价: "折即任务"的并行粒度选取聪明（方法内部无法并行，折间天然独立），与 PATTERN-003/004 组成完整基准驱动三件套；实现是 notebook 级的（global 注入、无 seed、无进度反馈），搬运时需重写为带 seed 与日志的脚本。
- 迭代记录: 2026-09-04 收录(一期精读批次A)
