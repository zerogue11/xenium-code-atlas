# PATTERN-038 · 声明式门控策略的细胞/区域分型
- 来源: estorrs/multiplex-imaging-pipeline（LIT-019）相对路径:行号 `multiplex_imaging_pipeline/spatial_features.py:20-120(DEFAULT_GATING_STRATEGY)、210-255(gate_cells)`
- 场景: 多重免疫图像/空间蛋白数据按 marker 阈值组合给细胞分型（PanCK+ 上皮、CD3+CD8+ CTL、CD68+CD163+ M2……），需要分型规则可读、可改、可存档，而不是散在 if-else 里。
- 做法: 门控写成纯数据 JSON 列表：每条 = `{name, strategy: [{channel, value, direction}]}`，direction 为 pos/neg 的分位数阈值；`gate_cells` 把逐细胞强度表按每条策略的通道阈值取布尔并集/交集判定，默认阈值 `value=0.05` 表示该通道 Top5% 为阳性。一条规则可多通道（AND 语义），多条同名规则（如两条 Epithelial 用不同 marker）构成 OR。策略文件可随 metadata 存档、跨样本复用。
  ```python
  DEFAULT_GATING_STRATEGY = [
    {'name': 'CD8 T cell', 'strategy': [
        {'channel': 'CD3e', 'value': .05, 'direction': 'pos'},
        {'channel': 'CD8',  'value': .05, 'direction': 'pos'}]},
    {'name': 'B cell', 'strategy': [
        {'channel': 'CD20',  'value': .05, 'direction': 'pos'},
        {'channel': 'Pan-Cytokeratin', 'value': .05, 'direction': 'neg'}]}]
  # gate_cells(df, gating_strategy=...) -> 每细胞标签列
  ```
- 搬运条件: 纯 pandas/numpy，MIT 可自由搬；需改造点：通道缺失时显式报错（原实现静默 NaN）、阈值来源加"自动分位/人工定值"开关并写入 metadata、与 Xenium panel 的 marker 名对齐后可直接用于 A7 模块细胞分型层。
- 工程评价: 数据-逻辑分离做得好，规则本身即文档；弱点是阈值经验化且无校验（10/14）。
- 迭代记录: 2026-09-04 收录(一期精读批次D)
