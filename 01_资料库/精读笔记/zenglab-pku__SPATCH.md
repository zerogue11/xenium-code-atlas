# 精读笔记 · zenglab-pku__SPATCH

- repo: zenglab-pku/SPATCH（LIT-084;LIT-090）
- 来源文献: SPATCH — 亚细胞分辨率 ST 平台基准测试（spatch.pku-genomics.org）
- 锁定SHA: c20108f60660b86bc2740607d84fd825beaaceca
- 复核分类: 注释/图谱/生态位组 · S 级 · 基准测试脚本集（analysis/ 12 文件 1625 行，无 LICENSE）
- 精读日期: 2026-09-04（一期精读批次C）

## 代码结构走读

- 仓库只有 `README.md` + `analysis/`（10 步基准 + 2 个一致性评估脚本），无包结构无环境锁：
  - **1_load_data.py**(342行)：按平台装载——Stereo cell-bin 聚合（:9-54）、Visium HD cell-bin 用 **geopandas 空间 join + 重叠多 nuclei 剔除**（:56-120 起）、各平台转 h5ad。
  - **2_8um_bin.py**(176行)：Xenium/CosMx **转录本级坐标 → 8µm 网格 bin**（`tr['binx'] = tr['x_location']*resolution//8`，:23-24,48-49），跨平台对齐到同分辨率。
  - **3_registeration.py**(305行)：SimpleITK 重采样+landmark 初配准+Mattes 互信息多分辨率精配准，把 CODEX 与 ST 坐标对齐。
  - **4_diffusion.py**(127行)：组织内外相对扩散效应量化（sST 平台 RNA 扩散基准）。
  - **5_correlation_with_codex.py**(104行)：ST×CODEX 空间网格表达相关性。
  - **6_scrna.r**(44行)：scRNA 参考预处理（Seurat）。
  - **7_cluster.py**(29行)：标准 scanpy 链 QC→norm→HVG(基因数/10)→PCA30→leiden+轮廓系数。
  - **9_st_annotation.py**(96行)：**五种注释迁移工具并列**——Selina(:12-28)、Spoint(:31-43)、Tangram(:46-59)、Tacco(:62-68)、celltypist(:71-78)，外加 `annotation()` 五工具投票合并+回退(:81-97)。
  - **9_st_annotation_consistency.r**(123行)：跨工具注释一致性（簇数/一致率）。
  - **10_spatial_cluster.py**(155行)：CODEX 侧 trVAE、ST 侧 scVI → **CellCharter spatial_cluster（delaunay+remove_long_links+aggregate n_layers=5+ClusterAutoK(5,10)）**，best_k 查表。
- 文件间无 import 关系，各自为战；执行顺序=文件名编号（analysis/README.md 有每步一句话说明书）。

## 关键脚本清单

| 文件 | 一句话 | 行数 |
|---|---|---|
| analysis/2_8um_bin.py | Xenium/CosMx 转录本坐标→8µm 网格 bin 对齐 | 176 |
| analysis/9_st_annotation.py | 五工具注释迁移并列+投票合并 | 96 |
| analysis/10_spatial_cluster.py | scVI/trVAE→CellCharter 空间聚类基准 | 155 |
| analysis/3_registeration.py | SimpleITK CODEX-ST 图像配准 | 305 |
| analysis/1_load_data.py | 多平台装载+HD cell-bin geopandas 聚合 | 342 |
| analysis/7_cluster.py | 基线 scanpy 聚类链 | 29 |

## 技术路线还原（勾选实际步骤，按序）

[数据读取(1 号多平台), 质控QC(7 号 filter_low_quality 分位数), 归一化(7/10 号 normalize_total), HVG(7 号 n_top_genes=基因数/10), 降维(PCA30/scVI/trVAE), 聚类(leiden+CellCharter), 注释(9 号五工具+投票), 空间邻域/域(10 号 CellCharter spatial cluster), 亚细胞(2 号 8µm bin 转录本重分箱), 空间统计(4 号扩散效应/8 号细胞形态), 配准/3D(3 号 SimpleITK), 多样本整合(10 号 trVAE 条件对齐), 导出(h5ad/txt)] — 共 13 步
未做：细胞通讯、绘图专项（散见）。

## 工程审计表（0-2 分/维，共 14）

| 维度 | 分 | 证据 |
|---|---|---|
| ①职责单一 | 1 | 一文件一步骤编号清晰，但无公共库，平台特化代码重复 |
| ②命名规范 | 1 | 文件编号好；但**同名函数冲突**：9_st_annotation.py:12 与 :31 两个 `predict`（后者遮蔽前者）、10_spatial_cluster.py:10 与 :50 两个 `spatial_cluster` |
| ③安全性 | 0 | 硬编码 /home/renpf/...：4_diffusion.py:26-34、9_st_annotation.py:47、9_st_annotation_consistency.r:5,9 |
| ④最简化 | 1 | 每文件头部 VSCode 插件残留 `FilePath: /undefined/Users/morsouron/Desktop/...`（1_load_data.py:6 等 8 处）；7_cluster.py:29 silhouette_score 引用不存在的 'cluster' 列 |
| ⑤健壮性 | 0 | 脚本不可独立运行：9_st_annotation.py 引用未定义的 tissues/ref/device/params_train/vote；无断言无 try/except |
| ⑥可复现性 | 1 | seed 12345 全局一致（10_spatial_cluster.py:33,41,56,77）；无 requirements/env 锁、无 LICENSE |
| ⑦验证纪律 | 1 | 9_st_annotation_consistency.r 跨工具一致性评估=基准设计自含验证；无 CI/测试 |

**总分 5/14**

## 可搬运模式

- PATTERN-029 跨平台 8µm 网格 binning 对齐（转录本坐标→固定分辨率 bin）
- PATTERN-030 多注释器投票合并（5 工具并列+多数票+回退最接近方法）

## 坑与限制（实读发现）

1. **脚本是从大工程里"抠"出来的函数级摘要，不能直接跑**——全靠读者自补上下文；与本组其他仓相比是"方法清单"而非"工作流"。
2. 注释基准里五工具的输入预处理不统一（celltypist 自带 norm+log1p:72-75，Tacco 直接 float32 原值:65-68），基准公平性存疑，引用结论时需核对。
3. 8µm bin 的 binx 计算按分辨率缩放后再整除（2_8um_bin.py:23 `x_location*resolution//8`），分辨率非 1µm 平台（如 CosMx px 坐标）需先换算，注释未说明换算来源。
4. Visium HD cell-bin 聚合用 geopandas sjoin 且剔除重叠 nuclei（1_load_data.py:105-117）， bin 级 Stereo 聚合用 mask 索引（:25-29），两条路线不同——跨平台对比时聚合偏差要单独评估。
5. 无 LICENSE：法律上默认保留所有权利，代码只能看不能搬。

## 一句总评

十步基准覆盖面（8µm bin、配准、扩散、五工具注释、跨模态一致性）是本组最全的方法地图，但工程质量垫底（无许可证、硬编码、同名函数、不可运行），价值在"测什么"不在"怎么写"。
