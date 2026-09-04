# 精读笔记 · estorrs/3d-analysis

- repo: https://github.com/estorrs/3d-analysis
- 来源文献: LIT-071 / "3D Imaging and Multimodal Spatial Characterization of the Precancer-to-Cancer Transition in Breast and Prostate"（README:3）
- 锁定SHA: `14f04c1b787991898380305702c31d52c19fa694`（2026-05-06）
- 复核分类: 3D 组 · 手稿配套 notebook 仓库（非包）· 核心配准明确外链 ding-lab/mushroom（README:9-19）· MIT（LICENSE）

## 代码结构走读（实际读了什么）

无 Python 包，全靠编号 notebook 流水线 + 少量脚本：
- 预处理三胞胎：`1_cosmx_preprocessing.ipynb`（70 cell，CosMx AtoMx 输出→h5ad，内嵌样本元数据表直接写在 cell 里）、`1_visium_preprocessing.ipynb`（17 cell）、`1_visiumhd_preprocessing.ipynb`（7 cell，读 spaceranger `square_002um` binned 输出+tissue_positions.parquet）。三者产出统一写入 `../data/spatial/inputs/<平台>/` 的 h5ad 数据湖。
- `2_sc_analysis.ipynb`（49 cell）：单细胞参考（mmread mtx→AnnData）→ QC（mt/ribo/hb 指标）→ filter → normalize/log1p → HVG(2000, batch_key) → PCA → **harmony 整合** → leiden → DEG。
- `3_2d_degs.ipynb`（157 cell，README:23 指认的"自动 2D 上皮区域检测"主方法）：Xenium adata 装载 → EPCAM 转录本空间分布 → gaussian filter + 二值形态学（fill_holes/erosion/label/remove_small_objects）生成上皮掩码 → `count_genes_in_regions`（掩码内基因计数，带列名校验 raise ValueError）→ `correlate_to_target_per_sample`（区域级基因与目标基因 Pearson 相关）→ case/sample 两级指标聚合与阈值判定。
- `4_deg_ranking.ipynb`（157 cell）：把 2D 区域相关谱与单细胞 DEG 排名对齐打分（PyComplexHeatmap 出热图）。
- `5_func_validation_canidates.ipynb`（文件名拼写 canidates）、`6_supp_table_reformatting.ipynb`、`7_figure8_panels.ipynb`（图 8 组面板）。
- `notebooks/summarize_counts_h5ad.py`（5.7k）：全仓唯一独立 CLI 脚本——argparse、类型注解、分块统计 counts.h5ad 的 QC 指标，坐标列名候选自动匹配（`COORDINATE_COLUMN_CANDIDATES`，:30-47），质量显著高于 notebook。
- `scripts/config.json` + `config.example.json`：jobs 数组按 modality（xenium/visium/...）列样本清单、参考 CSV、include_specimens、path_overrides——配置驱动采集。`compute1/launch_jupyter.sh`、`docker/Dockerfile`（ubuntu20.04+miniconda+scanpy+Seurat 双语环境）。

## 关键脚本清单

| 文件 | 一句话 |
|---|---|
| 3_2d_degs.ipynb (157 cell) | 主方法：EPCAM 掩码→区域基因计数→相关谱→阈值判定（手稿图 8 核心链） |
| 2_sc_analysis.ipynb (47 code cell) | 单细胞参考：QC→HVG→PCA→harmony→leiden→DEG |
| 1_*_preprocessing.ipynb ×3 | CosMx/Visium/VisiumHD 异构输出→统一 h5ad 数据湖 |
| 4_deg_ranking.ipynb | 空间相关谱 × 单细胞 DEG 排名比对 |
| summarize_counts_h5ad.py | 唯一 CLI：h5ad QC 指标汇总，带列名 fallback 与分块 |
| scripts/config.json | 多平台样本采集配置（jobs 数组驱动） |

## 技术路线还原（固定清单勾选）

1. **数据读取**（spaceranger/AtoMx/HTAN 元数据 CSV）
2. **质控QC**（mt/ribo/hb + filter_cells/genes，2_sc_analysis；区域掩码清理 binary_fill_holes/remove_small_objects）
3. **归一化**（normalize_total+log1p）
4. **HVG**（n_top_genes=2000, batch_key）
5. **降维**（PCA）
6. **多样本整合**（sce.pp.harmony_integrate(orig.ident)）
7. **聚类**（leiden）
8. **注释**（上皮/基底等区域类型 + EPCAM 相关判定）
9. **空间统计**（区域级基因-基因 Pearson 相关、case/sample 聚合阈值）
10. **绘图**（seaborn/PyComplexHeatmap/图 8 面板）
11. **导出**（h5ad 数据湖 + 支撑表 CSV）

**骨架步骤数：11**。未做：细胞通讯、亚细胞、去卷积、空间邻域图（squidpy 只 import 未实质使用）、配准/3D（外链 mushroom）。

## 工程审计表（7 维 × 0-2，共 6/14）

| 维度 | 分 | 证据 |
|---|---|---|
| ①职责单一/模块化 | 1 | 编号 notebook 序列职责清楚，但逻辑全埋在 cell 里不可 import；仅 summarize_counts_h5ad.py 独立成模块 |
| ②命名规范 | 1 | 编号规则清楚；`evan_crc_stuff.ipynb`（11MB）、`test.ipynb` 草稿混入正式目录；`5_func_validation_canidates` 拼写错误 |
| ③安全性 | 0 | 个人/集群路径入库：`/Users/erikstorrs/Downloads/...`（scripts/config.example.json path_overrides）、`/diskmnt/primary/...`、`/storage1/fs1/dinglab/...`（1_cosmx cell5）；config.json 带真实样本清单 |
| ④最简化 | 1 | notebook 内嵌输出未清（2/3/4 号共 14MB），草稿 notebook 未归档 |
| ⑤逻辑健壮性 | 1 | 好的一面：count_genes_in_regions 列缺失 raise ValueError（3_2d_degs）、summarize 脚本分块+列名 fallback；坏的一面：样本循环靠 try/except 包裹、多数 cell 无校验 |
| ⑥可复现性 | 1 | docker/Dockerfile 双语环境可重建；config.example.json 提供；但 notebook 无 seed、依赖 compute1 集群路径、无版本锁（pip 直装） |
| ⑦验证纪律 | 1 | 5 号 notebook 是功能验证痕迹、6/7 号有定版表格与图；无 CI/测试/断言矩阵 |

## 可搬运模式

- PATTERN-036：元数据跟踪表驱动的多平台统一数据湖装载（config jobs + 跟踪 CSV → 逐样本标准化 h5ad）。

## 坑与限制（实读发现）

- **无包无函数**：所有可复用逻辑都在 notebook cell，直接引用只能复制 cell；想工程化必须先抽函数。
- 元数据表以 `pd.read_csv(StringIO("""Case\t..."""))` 硬写在 cell 里（1_cosmx cell3），改样本要改代码。
- 3_2d_degs 的掩码参数（gaussian sigma、min_size、erosion 半径）为魔法数散落各 cell，无集中配置。
- `../data/` 相对路径约定跨 notebook 隐式耦合，目录一挪全断。
- 配准与 3D ROI 全在 mushroom 仓（本仓 README 明确外链），读本仓得不到 3D 配准细节。
- docker 镜像 amd64 锁死且 pip 不锁版本，与 2026 年复现环境有距离。

## 一句总评

典型的手稿配套仓：编号 notebook 串起"多平台预处理→单细胞参考→2D 区域相关→排名→成图"的完整证据链，方法本身（掩码+相关）简单可信，但工程形态是"可复现的实验记录"而非可搬运的软件，个人路径与巨型输出都需要清洗。
