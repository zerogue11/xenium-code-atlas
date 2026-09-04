# 精读笔记 · Teichlab/drug2cell

- repo: https://github.com/Teichlab/drug2cell
- 来源文献: LIT-018 / Kanemaru et al., "Spatially resolved multiomics of human cardiac niches", Nature 619:801-810 (2023)
- 锁定SHA: `a786c632fc521b94f597e452e2f09c45fd451640`（2024-12-21，v0.1.2）
- 复核分类: 亚细胞组 · scanpy 生态基因群活性打分/富集方法包 · 许可 **GRL 非商业**（LICENSE:1-9，商用需联系 legal@sanger.ac.uk）

## 代码结构走读（实际读了什么）

目录极小，共 845 行 Python：
- `drug2cell/__init__.py`（417 行）：三个公开函数全部在此——`score()`（:57，逐细胞基因群打分，结果写入 `.uns['drug2cell']`）、`gsea()`（:219，基于 blitzgsea 对 `sc.tl.rank_genes_groups()` 输出做富集）、`hypergeometric()`（:301，超几何过表达检验，statsmodels FDR）。
- `drug2cell/util.py`（164 行）：`reconstruct_targets`（:8，从 `.uns` 反解基因组字典）、`prepare_targets`（:19，统一入口——处理 None/嵌套 dict/categories 子集三种形态，ChainMap 展平）、`prepare_plot_args`（:53，产出 scanpy matrixplot 兼容的 var_names/positions/labels）、`plot_gsea`（:119）。
- `drug2cell/data.py`（24 行）：`pkg_resources.resource_stream` 加载随包分发的 `drug-target_dicts.pkl`（ChEMBL 药靶，ATC 分类嵌套）与 `cpdb_dict.pkl`（ConsensusPathDB 通路）。
- `drug2cell/chembl.py`（180 行）：ChEMBL 数据框的顺序过滤流水线（max_phase/机制/assay 类型/pChEMBL 阈值），带 bool/int 参数类型校验（:60-65）。
- 入口链：用户 adata（推荐 log-normalized）→ `d2c.score()` 矩阵乘法打分 → `.uns['drug2cell']` 新 AnnData（复制 `.obs`/`.obsm`）→ 对原对象跑 `sc.tl.rank_genes_groups()` → `d2c.gsea()`/`d2c.hypergeometric()` 按簇返回 DataFrame 字典。demo 全流程见 `notebooks/demo.ipynb`，ChEMBL 再构建见 `notebooks/chembl/` 两个 notebook。

## 关键脚本清单

| 文件 | 行数 | 一句话 |
|---|---|---|
| drug2cell/__init__.py | 417 | 打分/GSEA/超几何三件套；score 用稀疏矩阵乘 X·W 一次算全部基因组 |
| drug2cell/util.py | 164 | 基因组字典形态统一（ChainMap 展平）+ scanpy 绘图参数拼装 |
| drug2cell/chembl.py | 180 | ChEMBL 药靶库过滤（临床期/pChEMBL/assay 类型），产出随包 pickle |
| drug2cell/data.py | 24 | 打包数据加载（pkg_resources） |
| setup.py | 23 | v0.1.2，依赖 anndata/pandas/numpy/statsmodels/scipy/blitzgsea，全不锁版本 |
| notebooks/demo.ipynb | - | 官方演示：score→UMAP→rank_genes_groups→gsea/hypergeometric |

## 技术路线还原（固定清单勾选）

按实际执行顺序（该仓是打分/富集工具，不是全流程）：
1. **数据读取**（用户 adata + 随包 ChEMBL/CPDB pickle，data.py:8-24）
2. **绘图**（prepare_plot_args 产出 scanpy 绘图三参数、plot_gsea 调 blitzgsea.top_table，util.py:53-165）

未做：QC、归一化、HVG、降维、聚类、注释、去卷积、空间邻域/域、细胞通讯、亚细胞分割、空间统计、配准/3D、多样本整合、导出（结果只存 `.uns`，不落盘）。**骨架步骤数：2**。

## 工程审计表（7 维 × 0-2，共 10/14）

| 维度 | 分 | 证据 |
|---|---|---|
| ①职责单一/模块化 | 2 | 三主函数+util/data/chembl 分层清晰；__init__.py:57/219/301 与 util.py:19 职责互不重叠 |
| ②命名规范 | 2 | snake_case 一致；`_sparse_nanmean`/`_mean` 私有前缀（__init__.py:15,40）；参数名与文档一致 |
| ③安全性 | 2 | 全库无硬编码绝对路径/凭据；数据随包分发而非外链 |
| ④最简化 | 2 | 845 行无死代码；借 scanpy 的函数注明出处（__init__.py:16） |
| ⑤逻辑健壮性 | 1 | 有 `layer`+`use_raw` 互斥 ValueError（__init__.py:117）、chembl.py:60-65 类型校验；但 `score(method=...)` 无枚举校验，传错值静默按 mean 走（__init__.py:158-205 仅判断 =="seurat"） |
| ⑥可复现性 | 1 | seurat 分支 `np.random.shuffle` 无 seed 控制（__init__.py:176）；setup.py:12-18 依赖全不锁版本 |
| ⑦验证纪律 | 0 | 无 tests/、无 CI、无回归记录（CHANGELOG.md 仅版本流水账） |

## 可搬运模式

- PATTERN-033（稀疏矩阵乘法批量基因群打分 + 结果以子 AnnData 存 `.uns`）
- PATTERN-034 是同批 snp2cell 的网络传播，此处仅列其与 d2c 的共性：`prepare_targets` 的"嵌套字典 + categories 子集 + ChainMap 展平"是基因集库管理的通用前置件（PATTERN-035 单列）。

## 坑与限制（实读发现）

- **许可证是最大坑**：GRL 非商业许可（LICENSE:1-9），禁止任何"最终目标为商用产品/收费服务"的研究用途，与我们代码库的融合使用需注意边界——思路可搬，代码不宜直接并入商用产物。
- `score()` 存回 `.uns['drug2cell']` 时直接覆写同名槽位，重复调用不告警（__init__.py:209）。
- `hypergeometric()` 假定 `adata.uns['rank_genes_groups']` 已存在，直接索引（__init__.py:346,368），前置缺失时报 KeyError 而非友好提示。
- `data.py` 用 `pkg_resources`（setuptools 已弃用 API），新 setuptools 下会有 DeprecationWarning。
- ChEMBL 字典为 HGNC 符号，跨物种/非标准 var_names 需自行映射（README 已声明）。
- `hypergeometric()` 的 results 表按 `pvals_adj` 排序返回，但 `direction` 过滤发生在 marker 侧而非基因组侧（__init__.py:381-385），down 模式语义需读码确认。

## 一句总评

小而准的 scanpy 挂件：把"逐细胞打分→marker→富集"三步用矩阵乘法一次算完并优雅存回 AnnData，方法包 API 设计范本级，唯无测试、无 seed、非商业许可三处减分。
