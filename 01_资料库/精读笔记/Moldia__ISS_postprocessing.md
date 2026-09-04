# 精读笔记 · Moldia__ISS_postprocessing

- repo: Moldia/ISS_postprocessing
- 来源文献: LIT-017（ISS 空转三件套的后端：分割掩码 + 解码 spot → 细胞×基因 AnnData → 分型 → 空间分析）
- 锁定SHA: 3c779c6bc1673c73a21a3dfd30212e80945c084a（2022-06-15，"Adding scanpy and squidpy tutorials"）
- 复核分类: 分割/ISS 工具链（S 级）——cellpose→pciSeq→scanpy/squidpy 对象链

## 代码结构走读

目录 → 模块职责（实读）：
- `ISS_postprocessing/segmentation.py`（284 行）：**已核实 import 副作用问题属实**——L10 与 L124 两处模块顶层 `model = models.Cellpose(gpu=False, model_type='nuclei')`，`import ISS_postprocessing.segmentation`（包 __init__ 即执行）就会下载并实例化 cellpose 模型；且同一模型重复定义两次。`stardist_segmentation`（L27-68，函数内 from_pretrained 延迟加载，做法正确）→ expand_labels 扩张 → 存 coo npz；`cell_pose_segemenation_to_coo`（L73-111，函数名拼写错误）cellpose 分割 + 距离变换 watershed 再分裂 + expand_labels → coo；`segment_tile`（L141-223，逐 tile 分割→按 tilepos 行/列 vercat→全图 relabel）；`plot_segmentation_mask_colored`（L232-283，L278 使用未导入的 `mpl` —— 运行必 NameError）。
- `ISS_postprocessing/annotated_objects.py`（548 行）：`create_anndata_obj`（L78-141，spot 按 ndi.map_coordinates 分配到掩码 label → groupby(Gene,cell) 矩阵 → AnnData）；`recluster_specific_cluster`（L143-165，子聚类多 resolution）；`spatial_neighborhood`（L235-254，O(n²) 欧氏距离矩阵→邻域计数→leiden）；`create_ann_tiles`（L256-318，按 fov 逐 tile 建 AnnData 后 sc.concat 加 spatial 坐标）；`pciseq_anndata`（L358-381，pciSeq 结果转 AnnData）；大量绘图函数（color_cells_gene_expression 在 L383 与 L434 完全重复定义两次）。
- `ISS_postprocessing/pciseq.py`（44 行）：`run_pciseq`（L37-45，pciSeq.fit(spots, coo_mask, sc_expression_matrix) 做 spot→cell 分配 + 细胞类型）；`preprocess_spots`（L6-13，**L8 `spots = iss_spots.dropna()` 引用未定义变量 iss_spots，一调用即 NameError**）；`get_most_probable_call_pciseq`（L15-35）。
- `Scanpy_tutorial.ipynb` / `Squidpy_tutorial.ipynb`：normalize_total→log1p→HVG→scale→PCA→neighbors→leiden→UMAP→rank_genes_groups；squidpy 侧 spatial_neighbors→nhood_enrichment→co_occurrence→ripley→centrality_scores→spatial_autocorr。
- `postprocessing.yml`：cellpose==0.6.1、scanpy==1.9.0、squidpy==1.2.0 全锁。

## 关键脚本清单

| 文件 | 行数 | 一句话 |
|---|---|---|
| ISS_postprocessing/segmentation.py | 284 | cellpose/stardist 分割→watershed 分裂→expand→coo npz（import 即加载模型） |
| ISS_postprocessing/annotated_objects.py | 548 | spot→cell 分配、AnnData 构建、子聚类、邻域分析与绘图 |
| ISS_postprocessing/pciseq.py | 44 | pciSeq 细胞分型封装（preprocess_spots 含未定义变量 bug） |
| Scanpy_tutorial.ipynb | notebook | 标准单细胞流程在 ISS 对象上的演示 |
| Squidpy_tutorial.ipynb | notebook | 邻域富集/共现/Ripley/中心度等空间统计演示 |

## 技术路线还原（勾选固定清单，按实际顺序）

1. 数据读取（decoded.csv/spots_PRMC.csv + 分割 npz + tilepos.csv，annotated_objects.py:89,115）
2. 质控QC（create_anndata_obj L91-100 按 quality_minimum/quality_mean/distance 过滤 read）
3. 归一化（notebook sc.pp.normalize_total + log1p）
4. HVG（notebook sc.pp.highly_variable_genes）
5. 降维（notebook sc.tl.pca / umap；annotated_objects.py:168-186 plot_umap）
6. 聚类（recluster_specific_cluster L143 多 resolution leiden；notebook sc.tl.leiden）
7. 注释（plot_marker_genes L188 rank_genes_groups；pciSeq 分型结果 MostProbableCellType）
8. 去卷积（pciseq.py:38 pciSeq.fit 用 sc 参考谱把 spot 分配给细胞并定细胞类型）
9. 空间邻域/域（spatial_neighborhood L235 自写邻域计数+leiden；squidpy nhood_enrichment/co_occurrence）
10. 空间统计（notebook sq.gr.ripley/centrality_scores/spatial_autocorr）
11. 绘图（plot_all_clusters/color_cells_gene_expression/map_of_clusters 等）
12. 导出（h5ad 落盘 annotated_objects.py:317）

未做：细胞通讯、亚细胞、配准/3D、多样本整合（concat_anndata L320 仅 concat 多样本 AnnData，无批次整合方法，不计）。

## 工程审计表（7 维，0-2 分）

| 维度 | 分 | 证据 |
|---|---|---|
| 职责单一/模块化 | 2 | segmentation/annotated_objects/pciseq 三模块 + 两个教程 notebook 分工清楚 |
| 命名规范 | 0 | 函数名拼写错误 `cell_pose_segemenation_to_coo`（segmentation.py:73）、`assinged`（annotated_objects.py:117）；同名函数 color_cells_gene_expression 定义两次（L383,L434） |
| 安全性 | 1 | 无凭据；但 dapi_channel=5、Base_5_stitched-5 路径模式硬编码（segmentation.py:143,155） |
| 最简化 | 0 | annotated_objects.py:1-41 import 块 numpy/scanpy/pandas/matplotlib 各重复 3-6 次；重复函数定义；死代码 cells[0].astype(int)-1 结果弃置（L132）、np.sum 未用（L247） |
| 逻辑健壮性 | 0 | 三处一调用即炸的 NameError：pciseq.py:8（iss_spots）、annotated_objects.py:350（add_fov_number 中 x/y 未定义）、segmentation.py:278（mpl 未导入）；裸 except 大量 |
| 可复现性 | 1 | postprocessing.yml 锁 cellpose==0.6.1/scanpy==1.9.0/squidpy==1.2.0 是亮点；但 import 即实例化模型的环境副作用 + requires.txt 无锁抵消部分 |
| 验证纪律 | 0 | 无测试/CI；多个 NameError 级 bug 长期存在，证明导出函数从未被整体运行过 |

总分：4/14

## 可搬运模式

- PATTERN-018 coo npz 稀疏掩码交换格式 + map_coordinates spot→cell 分配

## 坑与限制

- **import 副作用（任务重点核实项）**：segmentation.py L10/L124 顶层实例化 `models.Cellpose(gpu=False, model_type='nuclei')`，且经 `__init__.py` 导出链，只要 `import ISS_postprocessing` 就会加载 cellpose（首次运行还会下载权重）；正确做法是函数内延迟实例化（同文件 stardist_segmentation L46 就是这么写的）。
- `preprocess_spots`、`add_fov_number`、`plot_segmentation_mask_colored` 三个导出函数当前版本无法运行。
- `spatial_neighborhood` 全量欧氏距离矩阵 O(n²) 内存，1 万细胞即 800MB float64，大样本不可用。
- `create_ann_tiles` 假设 `spots.fov` 排序与 tilepos.csv 行号一致（L272-275 `tiles.iloc[i]` + `tile{i+1}.npz`），fov 编号偏移会导致错位。
- pciSeq 依赖与 cellpose 0.6.1 等旧版深度耦合，2026 年环境重建预计困难【待补充：未实际装环境验证】。

## 一句总评

从解码 spot 到带空间坐标的注释 AnnData 的完整参考链，模块划分和 squidpy 统计组合有参考价值；但 import 副作用、三处 NameError 和重复定义表明这是从未做整体回归的教学演示级代码，搬运必须逐函数重写验证。
