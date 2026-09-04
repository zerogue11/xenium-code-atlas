# PATTERN-032 · 自动 PC 数选择器（四模式 + min_pcs 兜底 + 可视化留痕）
- 来源: dpeerlab/p53-niche-dynamics（LIT-078）相对/路径:行号 — utils/preprocessing_utils.py:68-159（kneepoint:68-95、var_explained:97-103、inflection:105-115、总调度:134-150、绘图:121-132）
- 场景: 多样本/多 panel 管线里 PCA 维数不能一刀切（panel 大小差异大），需要每样本自动定 PC 数并留下"为什么是这个数"的图证——替代固定 npcs=20/30 的拍脑袋。
- 做法: 由 adata.uns['pca']['variance_ratio'] 累积求和得曲线，四选一：explainedvarNN（累计解释 NN% 方差的 PC 数）/ fixedNN（固定数）/ inflection（二阶差分平滑后过零点，epsilon 判据）/ kneepoint（首末点向量投影最大距离法）；结果小于 min_pcs(默认50) 时兜底抬到 50；同时画"累计方差曲线+选中点十字标注"图留痕。
```python
selected_pcs, var_explained = process_pca_results_from_cumulative_variance(
    np.cumsum(adata.uns['pca']['variance_ratio']),
    pca_mode='explainedvar50', min_pcs=50, epsilon=1e-5)
# except 分支: "Not enough PCs ... Default to 50 pcs."  (preprocessing_utils.py:101)
```
- 搬运条件: 纯 numpy/pandas/matplotlib 零重依赖，可直接抄进 zoro-scrna/zoro-spatial 公共层；注意 min_pcs 兜底会掩盖小 panel 数据"无 50 个有效 PC"的事实，需要把 var_explained 一并记录进 run_metadata。
- 工程评价: try/except 回退链完整（:98-115 两处兜底）、选择结果自带可视化证据（:121-131）符合"metadata 证明"要求；唯一弱点是 kneepoint/inflection 对噪声曲线的稳定性未做断言。
- 迭代记录: 2026-09-04 收录(一期精读批次C)
