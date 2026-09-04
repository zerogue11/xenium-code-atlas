# PATTERN-018 · coo npz 稀疏掩码交换格式 + map_coordinates spot→cell 分配
- 来源: Moldia/ISS_postprocessing（LIT-017）ISS_postprocessing/segmentation.py:61-64,109,169（save_npz(coo_matrix(...))）、annotated_objects.py:63-72（assign_spots_to_cells）、117-127（create_anndata_obj 主链）
- 场景: 分割结果（大图 label mask）与下游分析（spot 归细胞、细胞×基因矩阵）通常不在同一进程/同一环境——需要一种轻量、可并行分块、无需整图加载的交换格式与分配算法。
- 做法: 分割端把 label mask 转成 scipy coo_matrix 压缩存 npz（每 tile 一份 + 拼接后全图一份）；分析端 load_npz 后，把 spot 的 (y,x) 像素坐标用 `ndi.map_coordinates(mask, coords.T, order=0)` 查表得细胞 label，再 `groupby(['Gene','cell']).size().unstack()` 得细胞×基因计数矩阵，细胞质心/面积用 regionprops 取出作 obs。骨架：
```python
# 分割端: 存
save_npz(outpath+'/tile1.npz', coo_matrix(expanded_labels), compressed=True)
# 分析端: 分配
coo = load_npz(segmentation_mask)
cell_labels = ndi.map_coordinates(coo.toarray(), spots[['y','x']].T, order=0)
spots['cell'] = cell_labels
hm = spots.groupby(['Gene','cell']).size().unstack(fill_value=0)
an_sp = sc.AnnData(X=hm.T)          # 细胞×基因
```
- 搬运条件: 仅依赖 scipy/pandas/scanpy；改造点：coo.toarray() 整图稠密化在 Xenium 大视场会爆内存，应换 ndi.map_coordinates 直接收 coo 稀疏坐标或分块；`order=0` 最近邻查表对掩码边缘 spot 会分给扩张伪影区（expand_labels 的产物），建议记录 cell 面积并过滤过小对象。
- 工程评价: 协议设计（npz coo + tilepos.csv + decoded.csv）简单可靠，是三件套里真正跑通全链的粘合层；实现函数有 NameError bug（pciseq.py:8）与重复定义，搬运时以本卡骨架为准、逐行核对源码。
- 迭代记录: 2026-09-04 收录(一期精读批次B)
