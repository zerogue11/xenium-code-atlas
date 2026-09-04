# 精读笔记 · navinlabcode__tnbc-chemo

- repo: navinlabcode/tnbc-chemo（LIT-046）
- 来源文献: "Ecotypes of Triple-Negative Breast Cancer in Response to Chemotherapy"（Navin 实验室，TNBC 化疗响应生态型；scRNA+Visium+VisiumHD+Xenium 多平台）
- 锁定SHA: fbe1dd3b1db05dd5e9f02485a45fdd438d6af9fb（2026-08-04）
- 复核分类: 应用范式组 · S 级 · "20 份 md 操作手册 + 主题脚本"双轨仓（R/Seurat 生态为主）
- 精读日期: 2026-09-04（一期精读批次E）

## 代码结构走读

- 实际读取: 根 README、analysis/README 全文、ecotype.md 与 visium_hd.md 手册全文、scripts/ 下 spatial_niche/ecotype/xenium 子目录抽样与 metamodule.fnmf.wrapper.snk.py 全文、xenium.init.R 关键行。
- 双轨结构：`analysis/*.md`（19 份手册）负责"讲清楚每一步做什么、对应论文哪张图"；`analysis/scripts/<主题>/` 负责"能跑的 R/py 脚本"。`data/`+`supp/`+`other/`（343MB 公共数据：METABRIC/SCANB/ISPY990/BrighTNess/SCTD 参考对象，仅 ls 未读）三层交付。
- analysis/README 是总索引表：每个分析项 → md 链接 → 相关图号（Fig.1/ED Fig.2…），论文图号反查分析一步到位。
- 手册内部固定四段式：**Related figures → Rscript file path（kbd+GitHub 链接）→ Synopsis（编号步骤）→ Output（预期图网格，直接链到 website_images）**。即"手册=计划+验收标准"。
- 入口链（Xenium 支线）：xenium.init.R（Seurat 读 bundle）→ xenium.clean_cells.R（≤10 nFeature 过滤）→ integrate_seurat.xenium.R → TransferLabel_EvalMode（细胞类型）→ MapQuery consensus（细胞状态）→ spatialEcotype step0→2c（ROI→niche→MetaNiche）。

## 关键脚本清单

| 文件 | 一句话 | 行数 |
|---|---|---|
| analysis/scripts/xenium/xenium.init.R | Xenium bundle→Seurat 对象初始化（含 parquet 兼容注释与 nCount 检查） | 579 |
| analysis/scripts/spatial_niche/xenium.spatialEcotype.step2a.initiate_niche_assay.R | ROI 细胞组成矩阵建"niche assay"Seurat 对象：NormalizeData→ScaleData(regress nCount_niche)→PCA30→FindNeighbors | 209 |
| analysis/scripts/spatial_niche/xenium.spatialEcotype.step2b/2c.*.R | 每样本 niche 提案→跨样本 MetaNiche 共识 | 571/681 |
| analysis/scripts/ecotype/ecotype_1_define.R | 癌细胞 metaprogram×TME 状态相关图→louvain 社区=生态型，分辨率 0.01-10 扫 1000 档择优 | 91 |
| analysis/scripts/metamodule.fnmf.wrapper.snk.py | Snakemake 包装 fastNMF：样本×K(2-31) 网格扫描 reconstruction_err | 48 |
| analysis/scripts/visiumHD/（5 脚本） | VisiumHD 细胞类型三重共识：RCTD(TNBC ref)×RCTD(HBCA ref)×CopyKat 非整倍体 | 5 篇 |
| analysis/scripts/xenium/xenium.clean_cells.R | 硬细胞过滤（≤10 nFeature 等阈值注释在头部） | ~60 |
| analysis/ecotype.md | 手册范式标杆：图号↔脚本↔步骤↔预期输出四段式 | ~60 |

## 技术路线还原（主线按数据流序）

[数据读取(Seurat 读 Xenium/VisiumHD/scRNA), 质控QC(clean_cells nFeature 阈值), 多样本整合(integrate_seurat), 降维/聚类(Seurat 默认链 default_seurat_pipe.R), 注释(TransferLabel_EvalMode+MapQuery 共识决策), 去卷积(RCTD+CopyKat, VisiumHD 癌细胞三重共识), 亚细胞(无), 空间邻域/域(ROI niche assay→MetaNiche), 细胞通讯(CellChat ligand-receptor), 空间统计(archetype/生态型 igraph 图与 OS/响应关联, ML_13g 机器学习预测), 绘图, 导出(rds/表格)] —— 共 12 步。核心分析层（fastNMF metaprogram、archetype、ecotype）在单细胞对象之上叠加，构成"生态型发现→空间验证→临床关联"闭环。

## 工程审计表（7 维 0-2 分，总分 9/14）

| 维度 | 分 | 证据 |
|---|---|---|
| ①职责单一/模块化 | 2 | scripts 按主题域 10 个子目录，step0/2a/2b/2c 粒度均匀；helper 函数独立文件（ecotype_helper_functions.R, 214 行） |
| ②命名规范 | 2 | `.winner` 后缀标定终版脚本、step 前缀带字母插位（2a/2b/2c）；`util.*`/`std.*` 前缀区分工具与标准件 |
| ③安全性(硬编码) | 0 | step2a:24 `source("/volumes/USR1/yyan/project/.../util.pal.R")`，:30-34 默认路径全为作者 HPC 绝对路径 |
| ④最简化 | 1 | 手册与脚本少量重复描述；脚本内注释掉的死代码块（xenium.init.R:61,132-137 的旧 parquet 分支） |
| ⑤逻辑健壮性 | 1 | step2a:35-46 commandArgs 带默认值双分支；:71-77 行名不一致时 intersect 对齐兜底；但 stopifnot 多被注释（xenium.init.R:61） |
| ⑥可复现性 | 1 | ecotype_1:31 `set.seed(42)`；snk.py K 扫描参数化；但 R 包无版本锁、环境声明缺失【待补充：未发现 renv/conda 文件】 |
| ⑦验证纪律 | 2 | 手册 Synopsis=执行计划、Output 预期图=验收标准，构成完整"计划-验证痕迹"；`.winner` 终版命名=选择留痕；README 分析-图号映射=审查清单 |

## 可搬运模式

- PATTERN-050 · 图号反查 md 操作手册双轨组织（analysis/README 表 + 四段式手册）
- PATTERN-051 · ROI 细胞组成 niche-assay（spatialEcotype step2a：把邻域组成当 Seurat 对象跑标准流程）

## 坑与限制

- 纯 R/Seurat 栈：路径、Future 并行、rds 格式全部绑定作者机器，脚本直接运行成功率低，必须配合手册改路径。
- niche/生态型链条人工决策多（`.winner` 只保留终版，落选方案无存档），二分决策不可追溯。
- other/ 343MB 公共数据直接入仓（含 rds 二进制），git 体积大；我们镜像时按任务约定只 ls 不动。
- 细胞类型"共识决策"（MapQuery.consensus_decision）规则散在脚本内，手册未完整展开【待补充】。

## 一句总评

五仓中"面向人类读者"组织得最好的仓：md 手册四段式+图号反查+`.winner` 终版命名是可直接移植到我们项目文档体系的管理范式，脚本本身则是典型的"高精度复述、低可移植执行"实验室代码。
