# `Teichlab/snp2cell`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\Teichlab__snp2cell`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-018：《人类胚胎骨骼发育多组学图谱》（Nature 2024；README 自引 To, Fei, Pett et al. 2024 Nature，snp2cell 为该论文配套方法包） |
| 精选级 | S |
| 主分类 | P5 亚细胞·转录本定位（复核确认：分类体系 P5 明确列"drug2cell/snp2cell 类"；与初判一致） |
| 次要用途 | 通用 GWAS×单细胞调控网络解读工具（方法本身不依赖空间数据） |
| 一句话功能 | 网络传播方法包：把 GWAS 汇总统计、单细胞数据、base 基因调控网络（GRN）三类分数经网络传播整合到 GRN 图上，随机置换检验评估显著性，输出按细胞类型链接性状的调控程序（networkx 图） |
| License | BSD-3-Clause（setup.py 自述 BSD 3-clause，LICENSE.txt 为 BSD 条款文本；主表填"MIT"与仓库不符，建议更正） |
| 语言与规模 | Python；主表 Pythonx14；127 MB（docs 86 MB + .git 41 MB，代码本体很小） |
| 运行入口 | `pip install .` → Python 模块 + `snp2cell` CLI（typer）；docs/source/toy_example.ipynb 最小示例（README 称约 12 秒）+ snp2cell_fgwas_scores.ipynb；tests/test_toy_example.py 有对应单元测试 |
| 复现难度 | 中 — 包安装容易（pip，约 2 分钟）、toy 示例秒级；但完整流程需自备 GWAS 汇总统计、scRNA 数据与 base GRN 三类外部输入，数据准备是大头 |
| 与范式的关系 | "性状→细胞类型→调控程序"的 GRN 解读范式；与 drug2cell 构成 LIT-018 方法双件套；候选池（若做 GWAS/Xenium 联动分析） |
| 坑提示 | ① python_requires 声明 >=3.5,<3.12（README 同），新版 Python 装不上；② 依赖 pyranges/pybiomart（基因坐标/注释可能触发网络访问）；③ 127 MB 几乎全在 docs 示例数据，克隆前有预期；④ 主表 License 列 MIT 需人工更正为 BSD-3 |
| 锁定 SHA | e25a6a7fc747a3d3efd759417def1828e4b80e2f（主表） |

## 结构速览

- `snp2cell/`：5 个模块——snp2cell_class.py（核心类）、cli.py（typer 命令行入口）、recipes.py（流程配方）、util.py
- `docs/source/`：toy_example.ipynb、snp2cell_fgwas_scores.ipynb、fgwas/ 示例数据、API 文档
- `tests/`：pytest 单测（含 test_toy_example.py）；`requirements.txt` + `setup.py` + `LICENSE.txt`
- 关联仓：Teichlab/drug2cell（同文献方法件）、Teichlab/skeletal_dev_atlas（LIT-018 图谱数据仓）

## README/代码实读要点

- 三要素整合：GWAS summary statistics + single cell data + base GRN；网络传播叠加分数 + 随机置换算显著性
- 硬件：普通计算机即可（内存需装下数据），多核可加速；测试环境 macOS 12.6.7 与 Ubuntu 22.04
- 输出为 networkx 图，供按细胞类型检视性状相关调控程序

## 抽读实录

- 读 README 全文 + setup.py（依赖、python_requires、入口点）；ls snp2cell/、docs/source/；head LICENSE.txt。

## 复用建议

- 做 GWAS 性状→Xenium 细胞类型归因时可试用其 toy example 起步（成本极低）；base GRN 来源（如 CellPhoneDB/CellChat 衍生或公共 GRN）需先定，注意 pybiomart 需联网取注释。
