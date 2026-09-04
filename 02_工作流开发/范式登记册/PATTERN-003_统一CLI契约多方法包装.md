# PATTERN-003 · 统一 CLI 契约的多方法包装器（每方法一文件）

- 来源: QuKunLab/SpatialBenchmarking（Nat Methods 2022）Codes/Deconvolution/Tangram_pipeline.py:1-46（10 个 *_pipeline.{py,r,sh} 同构）
- 场景: 基准测试要在同一批数据上跑 N 个第三方方法（跨 Python/R/shell），且后续还要加新方法、换数据集时：给每个方法写一个入口文件，参数顺序与输出格式完全一致，上层驱动器就能用同一循环横扫所有方法。
- 做法: 每方法一个独立脚本，固定四元 CLI 契约 `[sc_file, spatial_file, celltype_key, output_dir]`；内部自行做该方法所需的前置（如 Tangram 取 top200 marker、过滤稀有 celltype），末尾把结果写 `output_dir/<方法名>_result.txt` 的统一长表格式。方法依赖的环境差异（R 版本、conda env）由外层驱动决定。
  ```python
  # Codes/Deconvolution/Tangram_pipeline.py
  sc_file_path, spatial_file_path, celltype_key, output_file_path = sys.argv[1:5]
  ad_sc, ad_sp = sc.read_h5ad(sc_file_path), sc.read_h5ad(spatial_file_path)
  sc.tl.rank_genes_groups(ad_sc, groupby=celltype_key, use_raw=False)
  markers_df = pd.DataFrame(ad_sc.uns["rank_genes_groups"]["names"]).iloc[0:200, :]
  tg.pp_adatas(ad_sc, ad_sp, genes=list(set(...)))
  ad_map = tg.map_cells_to_space(ad_sc, ad_sp, mode='clusters', cluster_label=celltype_key)
  tg.project_cell_annotations(ad_map, ad_sp, annotation=celltype_key)
  ad_sp.obsm['tangram_ct_pred'].to_csv(output_file_path + '/Tangram_result.txt')
  ```
- 搬运条件: 无框架依赖；需改造点——①用 argparse + `--output` 显式参数替代位置 argv；②输出文件名统一由驱动器传入而不是方法名硬编码；③R 方法包装需配 subprocess + 独立 env 调用（原仓用 os.system 字符串拼接，路径含空格即碎）。
- 工程评价: 契约设计本身是本仓最有价值的资产——10 个方法（Python 4 + R 5 + sh 1）保持同一签名，使 BLAST 驱动 notebook 只写一遍循环；各包装内部质量参差（Tangram 版有稀有类过滤，Seurat 版仅 16 行近乎裸跑），搬运时按仓内最完整版本为准。
- 迭代记录: 2026-09-04 收录(一期精读批次A)
