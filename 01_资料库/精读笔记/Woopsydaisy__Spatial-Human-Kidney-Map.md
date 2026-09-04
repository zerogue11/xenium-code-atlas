# 精读笔记 · Woopsydaisy__Spatial-Human-Kidney-Map

- repo: Woopsydaisy/Spatial-Human-Kidney-Map（LIT-048）
- 来源文献: 人类糖尿病肾病（DKD）空间图谱 — CosMx + Xenium 双平台，scVI/scANVI 整合 + niche 全家桶 + 4 专题（伤小管/免疫/B 细胞/NicheCompass）
- 锁定SHA: 8ddde5d6ed285c5c742a733d3cd9f251e554b758（2026-04-10）
- 复核分类: 应用范式组 · S 级 · 图谱型脚本链仓（A-K 主题目录，docker 容器级运行说明）
- 精读日期: 2026-09-04（一期精读批次E）

## 代码结构走读

- 实际读取: README 全文（A-K 每脚本一行职责+容器）、Exporting_Xenium.py 全文、Final_Combined_Integration_Script2 全文、Niche_Analysis Script1/2/3 头部与关键段、Tubular_ME_Script3、Nichecompass_Script2 关键行。
- 顶层 A-K 十一个字母主题目录 = 管线章节：A 导出（AtoMx/Xenium raw→h5ad+QC）→ B 整合（CosMx/Xenium 分别 scVI-scANVI 过滤→最终三方合并整合→注释→imputation）→ C SCIB 多方法基准 → D niche 全家桶（9 脚本）→ E NicheCompass → F COVET/Hotspot → G/H/I/J 四专题 → K 杂项。
- 入口链是"脚本编号即 DAG"：README 是唯一索引，无 make/nextflow 编排，靠脚本间 h5ad 文件接力（export→prescvi→scvi→scanvi→imputed→neighbored→niche）。
- README 每脚本标注容器（docker://10jll/spatial:version2 / scvi_cuda12:version4 / cellphonedb:version1 / nichecompass:version1），Colab/本地运行处也注明——"容器即环境文档"。
- 跨平台邻域（本仓核心价值）：Script1 按平台分支设半径——CosMx `radius=20/0.12`（µm→像素换算，0.12 µm/px）vs Xenium `radius=20`（原生 µm），五个尺度（20/40/60/80/200 µm）成对展开。

## 关键脚本清单

| 文件 | 一句话 | 行数 |
|---|---|---|
| A/Exporting_Xenium.py | spatialdata_io.xenium 读 bundle→四联 QC 直方图→写 h5ad | 62 |
| B/Final_Combined_Integration/Final_Combined_Integration_Script2_SCVI_SCANI.py | scVI(n_layers=4,n_latent=30,batch=tech,连续协变量 nCount/percent_mt)→SCANVI 迁移→预测+latent | 103 |
| B/Final_Combined_Integration/Final_Combined_Integration_Script4_Imputation.py | 用 SCANVI latent+归一化表达把 SN 参考表达"搬运"到空间细胞 | 195 |
| D/Niche_Analysis_Script1_call_neighbors.py | 五尺度半径分平台换算调 sq.gr.spatial_neighbors，直方图自检 | 370 |
| D/Niche_Analysis_Script2_Neighbor_Dataframe.py | 每细胞×每注释类型的 20/40µm 邻居计数矩阵（邻域即特征） | 183 |
| D/Niche_Analysis_Script3_Kmeans.py | 邻居计数→StandardScaler→PCA→MiniBatchKMeans(k=17)→niche | 137 |
| D/Niche_Analysis_Script5_cellphoneDB.py + G/I 系列 | imputed 表达+微环境分组喂 CellPhoneDB→相关疾病严重度 | ~108 |
| E/Nichecompass_Script2_model.py | NicheCompass 图模型：cat_covariates=样本、48 embed、训练/重载 | 187 |

## 技术路线还原（按脚本编号序）

[数据读取(平台 raw→h5ad), 质控QC(导出期直方图+过滤), 多样本整合(scVI/scANVI，batch_key=tech、协变量 proj/orig_ident), 降维(scVI latent), 聚类(leiden), 注释(scANVI 标签迁移+level1 注释), 空间邻域/域(五尺度 spatial_neighbors→邻居计数→KMeans niche→20µm 环境), 细胞通讯(CellPhoneDB on imputed 表达), 空间统计(COVET/Hotspot 基因-基因相关、GFR 相关), 导出(imputed/neighbored h5ad), 绘图] —— 共 11 步。HVG 与显式归一化未在所读脚本中出现（counts layer 直接进 scVI）【待补充：Integration Script1 中可能有，未读全】。SCIB 环节（harmony/scanorama/pyliger/scvi 四法基准）是图谱级验证支线。

## 工程审计表（7 维 0-2 分，总分 7/14）

| 维度 | 分 | 证据 |
|---|---|---|
| ①职责单一/模块化 | 2 | 一脚本一步骤、helper 函数集中（ecotype 式 helper 无，但 KMeans/邻域各管各）；G/H/I 专题复用 D 的脚本模式而非复制粘贴目录结构 |
| ②命名规范 | 1 | ScriptN 编号清晰，但有实名笔误：`Final_Combined_Integration_Script2_SCVI_SCANI.py`（SCANVI 少 V）、`Integration_Xenium_Scrip1.py`（少 t），README 表述与文件名不一致 |
| ③安全性(硬编码) | 0 | 全仓硬编码 `/home/bcd/revision_nature/...` 个人路径（Script2:18,20,39 等，几乎每脚本 3-5 处） |
| ④最简化 | 0 | Script1 把 20/40/60/80/200µm 五尺度×两平台写成 10 段展开代码（29-340 行）未函数化；COVET_Script4 4363 行线性 clustermap 重复块（266 处 def/import） |
| ⑤逻辑健壮性 | 1 | Script3_Kmeans.py:38 `assert all(adata_subset.obs_names == new_adata.obs_names)` 细胞对齐断言是亮点；其余脚本无校验 |
| ⑥可复现性 | 1 | 容器版本标注（version2/version4）可追但 tag 不透明；KMeans random_state=42（Script3:94）；`seed=10` 定义后从未使用（Script2:16，唯一 seed 引用） |
| ⑦验证纪律 | 1 | C/SCIB 四脚本显式多方法基准+silhouette 选 k；无 CI/测试；邻域直方图自检图是好习惯 |

## 可搬运模式

- PATTERN-048 · 微米半径跨平台换算的多尺度邻域层（Script1:29-340）
- PATTERN-049 · 邻居计数矩阵→KMeans 生态位发现链（Script2+Script3）

## 坑与限制

- 无编排器：脚本 DAG 靠文件接力，断点重跑要人工从中间脚本启动，且输入路径硬编码无法换机。
- "niche 全家桶"里 KMeans k=17 无选择依据注释（silhouette 已 import 但未见选择记录）【待补充】。
- imputed 表达喂 CellPhoneDB 是双刃剑：解决空间平台 panel 限制，但配体-受体结论部分由参考图谱"脑补"，读其结论时要打折。
- 容器 tag（version2/version4）内容不可考，严格复现需重建环境定义。

## 一句总评

"README 即手册、脚本编号即管线"的图谱仓样板，niche 全家桶的步骤分解（邻域→计数→聚类→注释→通讯→相关→差异）是最值得整段借走的分析骨架，但代码层硬编码路径与展开式重复让它只能"抄思路"，不能"搬文件"。
