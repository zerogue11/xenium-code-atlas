# `dpeerlab/p53-niche-dynamics`（档案卡）

> 由 agent 依据本地克隆实测撰写；不确定处一律【待补充】；禁止编造星标/日期/功能。

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-078：《胰腺癌祖细胞生态位》（Reyes et al., Cell 2026;189:2875-2897, doi:10.1016/j.cell.2026.03.032） |
| 精选级 | S |
| 主分类 | P3（复核维持：progenitor niche/邻域动态主题） |
| 次要用途 | P7（Xenium 形态学 Precompute 笔记本）；P2（多组学注释）；P6（条件密度等空间统计） |
| 一句话功能 | 胰腺癌良性→恶性转变祖细胞生态位研究复现代码：转录组/成像/multiome 五大模块的 locked 笔记本 + RAPIDS GPU 工具库，Xenium 数据提供预处理全链（raw→embed→注释→邻域→milo→niche 稳健性） |
| License | MIT |
| 语言与规模 | Python×76 / R×14 / Shell×4，349.4 MB |
| 运行入口 | Jupyter notebook（文件名自带 locked+日期后缀，如 `Xenium_Preprocessing_step03_compute_neighborhoods_simplified_locked20260410.ipynb`）；数据从 dp-lab-data-public S3 直链下 tarball/8 个 h5ad；依赖 `utils/` 自建工具库；无 env 文件【待补充】 |
| 复现难度 | 高：utils 直接 `import cupy/cuml/cugraph`（RAPIDS GPU 栈硬依赖），数据 tarball/h5ad 需从 S3 另取（体积【待补充】），notebook 相对路径引用 ../../utils |
| 与范式的关系 | 高价值：Xenium 邻域/niche 全链（step00–04 + Milo + conditional density + niche robustness 检验）是本项目空间生态位层直接可借鉴的实现；候选池重点对象 |
| 坑提示 | RAPIDS/cuML 版本敏感且 Windows 原生不可用（需 WSL2/Linux+GPU）；README 更新 2026/05/14：早期下载的 Xenium 对象淋巴结注释不完整，须取新版；349MB 仓库勿盲目全检 |
| 锁定 SHA | a97d1a42cede4c12416875a4aa50d3d63ee1fffd |

## 结构速览

- `transcriptomics/notebooks/`：KPLOH/Injury/Kras 抑制剂/FLEX/GiftOfLife 系列预处理与出图笔记本 + Xenium 出图组。
- `imaging_progenitor_niche_Fig3_FigS2/`、`imaging_kras_inhibition_4h_FigS5/`、`imaging_human_TMA_Fig4/`：成像分析（各含 notebooks）。
- `multiome_Fig7_FigS6/`：多组学模块。
- `utils/`：DNA3Bit、copy_number_inference、diffusion_maps、neighborhood_utils、preprocessing/plotting 等自建库（GPU 依赖集中于此）。

## 实读要点

- transcriptomics/notebooks 实读：Xenium 链完整命名——Preprocessing step00_raw_tenx_to_adata → step01_embed_tiered_samples → step02_annotate_cell_types → step03_compute_neighborhoods_simplified → step04_embed_tiered_cell_types；出图侧含 Fig2/3、Fig3/5、Fig6/S5_milo、FigS7_conditionalDensity、FigureS2_niche_robustness、celltype_proportions、Fig2_morphology。所有笔记本带 locked2026MMDD 后缀（冻结版）。
- utils/neighborhood_utils.py 实读：文件顶部直接 `import cupy, cuml, cugraph`，并自定义 lazy_import 以相对路径 `../../utils` 加载同库函数——GPU 硬依赖 + 相对路径双重移植成本。
- README 实读：4 个 S3 tarball（transcriptomics、两组成像、multiome）+ 8 个预处理 h5ad 直链（含 Xenium 邻域对象）；联系方式 José Reyes。

## 复现路径（怎么跑）

1. 环境：Linux/WSL2 + CUDA + RAPIDS（cupy/cuml/cugraph 版本对齐是成败关键，仓库未给 lock【待补充】）。
2. 数据：按 README S3 直链下 Reyes2026_transcriptomics.tar.gz 等 tarball 与 8 个 h5ad（注意 2026/05/14 更新公告，取新版 Xenium 对象）。
3. Xenium 链按文件名序：step00 raw→adata → step01 embed → step02 annotate → step03 neighborhoods → step04 tiered embed → 出图组（milo/conditional density/niche robustness）。

## 借鉴与风险

- 可移植点：Xenium step00-04 预处理全链 + niche 稳健性（robustness）+ 条件密度统计，正是本项目空间生态位层缺的"检验方法学"素材；locked+日期的笔记本冻结命名可借鉴。
- 风险：GPU 栈移植成本高、相对路径 ../../utils 脆弱；笔记本 frozen 无参数 CLI。S 级合理，不建议升格（无环境锁定）。

