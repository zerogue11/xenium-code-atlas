# PATTERN-047 · 跨平台统一 QC 核心+平台补丁层
- 来源: UCSF-DSCOLAB/spatial_transcriptomics_colitis_analysis_2024（LIT-053）相对/路径:行号 `Preprocessing/Preprocessing_XeniumRep1and2.ipynb` cell57、`Preprocessing_CosMx.ipynb` cell19-20、`Preprocessing_Merscope.ipynb` cell18（注释自证 "matches CosMx and Xenium"）与 cell20 lite 方案
- 场景: 7 Xenium+CosMx+MERSCOPE 这类跨平台研究：QC 过滤既要"平台间可比"（同一把尺子），又要尊重平台特有质控字段（NanoString qcFlags、FOV、控制探针）。任何多平台 Xenium 课题第一课。
- 做法: 先定义所有平台逐字一致的"统一过滤核心"，平台特有 QC 以补丁层追加，控制指标按平台 obs 列名分别计算：
  ```python
  # ---- 统一核心（三平台逐字一致）----
  sc.pp.filter_cells(ad, min_counts=50); sc.pp.filter_cells(ad, min_genes=10)
  sc.pp.filter_genes(ad, min_counts=1);  sc.pp.filter_genes(ad, min_cells=10)
  # ---- 平台补丁层 ----
  if platform == "CosMx":   # NanoString 官方 flag 全 Pass
      ad = ad[ad.obs['qcFlagsRNACounts'] == 'Pass']  # (+CellCounts/CellPropNeg/CellComplex…)
  if platform == "MERSCOPE" and small_dataset:       # lite 方案
      sc.pp.filter_cells(ad, min_counts=10)
  # 控制指标按平台列名分算: Xenium control_probe_counts / CosMx nCount_negprobes
  ```
- 搬运条件: 依赖 scanpy；无许可障碍。需改造点：①原实现是三份复制 notebook 人肉保持一致，搬运时应抽成单一函数+平台参数字典（单一事实源）；②补丁层顺序固定在核心过滤之后；③阈值(50/10/1/10)要按我们 panel 重扫分布图后冻结。
- 工程评价: "统一核心+补丁层+分平台控制指标"三段式思想质量高，实现载体（复制 notebook）质量一般（总评 8/14）；另可顺带抄两个习惯：notebook 路径一律 `/path/` 占位脱敏、autok 类随机产物 pickle 落盘+多 k 候选并存（CellCharter notebook cell15-17）。
- 迭代记录: 2026-09-04 收录(一期精读批次E)
