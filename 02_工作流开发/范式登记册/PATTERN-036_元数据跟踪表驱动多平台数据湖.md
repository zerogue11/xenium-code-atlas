# PATTERN-036 · 元数据跟踪表驱动的多平台统一数据湖装载
- 来源: estorrs/3d-analysis（LIT-071）相对路径:行号 `scripts/config.json(jobs 数组)、scripts/config.example.json:2-16、notebooks/1_cosmx_preprocessing.ipynb cell3-5(元数据 StringIO 表)、1_visiumhd_preprocessing.ipynb cell3-5`
- 场景: 多平台（Xenium/CosMx/Visium/VisiumHD…）多样本要装进统一分析格式，原始数据散落在不同目录结构/命名里，需要一份"样本→原始路径→输出路径→是否纳入"的单一事实来源。
- 做法: 两层配置。(1) 仓库级 `config.json` 用 jobs 数组描述每平台：metadata_csv 参考表、panel 参考、include_specimens 白名单、path_overrides_by_specimen 逐样本路径覆盖；(2) 平台级跟踪 CSV（Section_ID_clean 为主键）逐行样本，notebook 里 `for i, row in meta.iterrows()` 逐行读取原始输出、平台专属解析后统一 `write_h5ad` 进 `data/spatial/inputs/<平台>/` 数据湖，下游 notebook 只认湖不认原始路径。
  ```python
  meta = pd.read_csv(config['metadata_csv'])          # 平台跟踪表
  for job in config['jobs']:                          # 每平台一个 job
      if job['modality'] == 'xenium':
          for sid in job['include_specimens']:
              path = job['path_overrides_by_specimen'][sid]
              adata = adata_from_xenium(path)          # 平台专属解析
              adata.write(f"data/spatial/inputs/xenium/{sid}.h5ad")
  ```
- 搬运条件: 依赖 anndata/scanpy/pandas（各平台 reader 按需）；MIT 可自由搬；需改造点：把 StringIO 内嵌元数据改成外部 CSV、path_overrides 移出 git、解析循环抽成函数并加存在性校验——本仓原实现 notebook 化，搬运时直接升级为 `03_开源项目` 风格的 load_xxx.py。
- 工程评价: 思路正确（跟踪表+白名单+路径覆盖+数据湖分层），落地形态弱（逻辑在 cell、个人路径入库、config.json 与 example 同架构但前者含真实清单）；对 A5 模块"多平台装载层"是直接可抄的骨架（6/14）。
- 迭代记录: 2026-09-04 收录(一期精读批次D)
