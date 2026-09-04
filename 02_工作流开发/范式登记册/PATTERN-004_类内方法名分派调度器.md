# PATTERN-004 · 类内方法名分派调度器（方法注册表驱动）

- 来源: QuKunLab/SpatialBenchmarking（Nat Methods 2022）Benchmarking/SpatialGenes.py:282-327（Imputing）；同构 Benchmarking/DeconvolutionSpot.py:4-60（Dencon）
- 场景: 与 PATTERN-003 配对的上层调度：用户给一个方法名列表（如 `['SpaGE','gimVI','Tangram']`），调度器逐个调用对应实现并统一落盘，方法可任意增减而不改驱动代码结构。
- 做法: 一个类封装全部输入路径（构造器读三件套），每个方法一个 `*_impute()` 成员函数，分派器按 `if "tool" in need_tools` 线性展开，每支"调用→建目录→to_csv"。
  ```python
  def Imputing(self, need_tools):
      if "SpaGE" in need_tools:
          result_SpaGE = self.SpaGE_impute()
          os.makedirs(self.outdir, exist_ok=True)
          result_SpaGE.to_csv(self.outdir + "/SpaGE_impute.csv", header=1, index=1)
      if "gimVI" in need_tools:      # 原码此处 outdir 拼接漏 "/"，搬运时修正
          ...
      if 'LIGER' in need_tools:      # R 方法经 subprocess 进同一定义域
          os.system('Rscript Codes/Impute/LIGER.r ' + self.RNA_file + ' ' + self.outdir + '/LIGER_impute.txt')
  ```
- 搬运条件: 依赖 subprocess（跨语言分支）；需改造点——①if 链改为注册表 dict：`self._registry = {'SpaGE': self.SpaGE_impute, ...}` + 未知名直接报错（原实现对拼错的方法名静默忽略）；②R 分支换 `subprocess.run([...], check=True)` 列表传参；③统一 `os.makedirs(exist_ok=True)` 并修 outdir 拼接。
- 工程评价: 分派思想清晰、类构造器集中输入路径是好设计；实现层面三处硬伤（漏"/"的路径 bug、os.system 拼接、拼错名静默跳过）都集中在调度器——恰恰说明搬运时要重写的是调度器而非方法实现。
- 迭代记录: 2026-09-04 收录(一期精读批次A)
