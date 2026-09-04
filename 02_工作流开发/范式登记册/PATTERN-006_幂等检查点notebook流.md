# PATTERN-006 · 幂等检查点 notebook 流（步骤编号 + 中间层落盘 + html 归档）

- 来源: broadinstitute/ist_benchmarking（LIT-086）14 个编号 notebook 的统一组织模式；代表块 02_specificity_sensitivity_reproducibility.ipynb 单元6（`if not os.path.exists(f'{wd}/data/specificity')`）与 st_utils.py:631-650（save_html）
- 场景: 分析以 notebook 步骤流交付（每步一图一结论）但要求可安全重跑：任何一步中断后重进，已算完的中间层不重算，直接续跑；最终每步留一份 html 快照作为审查依据。
- 做法: 三条纪律叠加——①notebook 按两位数字编号即执行序（00 数据→01 中间层→02 指标→03+ 各分析），文件名即 pipeline 文档；②每个重计算块前挂 `if not os.path.exists(产物路径)` 守卫，产物按语义层落 `data/<层名>/`，图落 `figures/<图号>/`；③工具函数 save_html 用 nbconvert 把当前 notebook 转成带后缀的 html 归档。
  ```python
  wd = os.getcwd()                                   # 每步统一，无硬编码盘符
  if not os.path.exists(f'{wd}/data/specificity'):
      os.makedirs(f'{wd}/data/specificity')
      for sample in run_samples: ...                 # 重计算块，仅首次执行
  df_m = pd.concat([pd.read_csv(f'{wd}/data/specificity/{s}_specificity.csv') ...])
  # st_utils.py
  def save_html(ipynb, suffix=''):
      cmd = 'jupyter nbconvert --to html ' + ipynb.split('/')[-1]
      p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE); p.communicate()
  ```
- 搬运条件: 依赖 jupyter/nbconvert；需改造点——①一次性步骤用文件名后缀（`_no_need_to_run`）区分，搬运时应改为配置开关或独立目录；②shell=True 调 nbconvert 换 `jupyter nbconvert --to html notebook.ipynb` 列表式 subprocess；③守卫只看路径存在性，不校验数据版本——上游换数据需手工清产物，可加 mtime/hash 校验。
- 工程评价: 五仓中唯一把"重跑成本"当设计约束的仓，守卫+分层落盘+归档三件套成本低、收益大，是整合 pipeline 步骤手册的直接蓝本；弱点是业务逻辑仍内联在 notebook，只能靠纪律维持一致性。
- 迭代记录: 2026-09-04 收录(一期精读批次A)
