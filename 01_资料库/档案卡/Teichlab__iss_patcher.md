# `Teichlab/iss_patcher`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\Teichlab__iss_patcher`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-018：《人类胚胎骨骼发育多组学图谱》（Nature 2024） |
| 精选级 | A |
| 主分类 | P1 分割与重分割（复核确认，与初判一致；分类体系 P1 明确列 iss_patcher"分割后修补"） |
| 次要用途 | 通用"低维数据借高维参考补特征"插补工具（README 自述不限 ISS 场景） |
| 一句话功能 | Teichlab 小工具包：对低维 ISS 数据中未实验捕获的特征，在低维与高维（scRNA/GEX）数据的共享特征空间内做对数归一+z-score，为低维观测找高维近邻（annoy），以近邻均值近似插补缺失基因表达 |
| License | MIT（主表值，与仓库 LICENSE 一致） |
| 语言与规模 | Python；py/ipynb 3 个（核心仅 iss_patcher/__init__.py 一个模块 + demo notebook）；体积 1.3 MB |
| 运行入口 | pip install git+https://github.com/Teichlab/iss_patcher.git → notebooks/demo.ipynb（约 10 分钟）；文档 iss-patcher.readthedocs.io |
| 复现难度 | 低 — 依赖轻（scanpy/scipy/annoy），pyproject 声明 python>=3.7,<3.12，demo 完整且短 |
| 与范式的关系 | 小面板 ISS/Xenium 数据借 scRNA 参考补基因的轻量方案，可与 zoro-spatial 注释段衔接（先插补再打分）；观察池（功能单一但即插即用） |
| 坑提示 | ① annoy 在 Windows 上编译安装易失败【待验证】（WSL/conda-forge 路线更稳）；② 插补值为近邻均值而非模型预测，只能用于展示/粗打分，不可作定量结论；③ 插补结果与参考图谱批次效应耦合 |
| 锁定 SHA | 【待补充：主表"锁定SHA"列空】；本地克隆 HEAD 实测 `686991c272` |

## 结构速览

- `iss_patcher/__init__.py`：全部功能（单模块包，本仓即"一个函数的项目"）
- `notebooks/demo.ipynb`：唯一使用示例（README 标注约 10 分钟跑完）
- `docs/` + `.readthedocs.yaml`：API 文档（docstring 级）
- `pyproject.toml`：依赖与版本区间；`LICENSE`（MIT）、`README.md`

## README/代码实读要点

- 插补三步：识别共享特征空间→逐对象 log-normalise + z-score→低维观测在高维空间找最近邻、取邻居均值补缺失特征
- 系统要求：足够内存即可，测试环境 macOS Monterey 12.6.7 与 Ubuntu 18.04.6
- 出处：README 声明为"To, Fei, Pett et al. 人类早期骨骼发育多组学图谱"手稿组成部分（即 LIT-018 数据论文）
- 安装时长参考：约 2 分钟

## 抽读实录

- 读 README 全文（原理、系统要求、安装、引用）；ls iss_patcher/、notebooks/。

## 复用建议

- 可作 Xenium 小面板→全转录组打分的轻量补齐器试用（demo 10 分钟成本极低）；注意它不做批次校正，参考图谱要预先同处理；Windows 部署建议走 WSL。
