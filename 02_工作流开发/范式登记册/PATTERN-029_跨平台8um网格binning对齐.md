# PATTERN-029 · 跨平台 8µm 网格 binning 对齐（转录本坐标 → 固定分辨率重分箱）
- 来源: zenglab-pku/SPATCH（LIT-084;LIT-090）相对/路径:行号 — analysis/2_8um_bin.py:23-31,48-56；analysis/1_load_data.py:9-54（cell-bin 对照组）
- 场景: 亚细胞分辨率平台（Xenium/CosMx）与 bin/spot 级平台（Visium HD/Stereo）做横向基准对比，需要把前者下采样到同一物理分辨率，消除"粒度优势"。
- 做法: 取转录本级坐标表，按平台分辨率换算后整除分箱：`binx = x_location*resolution // 8`；箱内转录本计数聚合为表达矩阵，箱中心坐标 ×8 还原为物理坐标存 obsm['spatial']；组织外信号剔除；对照组用平台自带 cell bin（Visium HD 配 geopandas sjoin 到 nuclei 多边形并剔除重叠）。
```python
def xenium_8um_bin(tr, tissue, resolution, platform):
    tr['binx'] = tr['x_location']*resolution//8      # 换算到 8µm 格
    tr['biny'] = tr['y_location']*resolution//8
    # groupby binx,biny 聚合计数 → AnnData
    adata.obsm['spatial'] = spatial * 8              # 还原物理坐标
```
- 搬运条件: 依赖转录本级原始输出（Xenium 的 transcripts.parquet / CosMx 的 tx 文件）；非 1µm 坐标系（CosMx px）需先确认 resolution 换算（源码未注释换算依据）；与 CODEX 蛋白组对比还需先过 3_registeration.py 的 SimpleITK 配准。
- 工程评价: 思路（同分辨率对照）是基准设计的关键一招，实现极简；但文件头 VSCode 残留、硬编码 /home/renpf 路径、无 LICENSE——代码不可搬，方法照抄 20 行即可自实现。
- 迭代记录: 2026-09-04 收录(一期精读批次C)
