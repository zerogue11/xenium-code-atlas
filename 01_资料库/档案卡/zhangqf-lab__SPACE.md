# `zhangqf-lab/SPACE`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\zhangqf-lab__SPACE`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-016：通过细胞间相互作用感知发现组织模块（README 英文原题 "Tissue module discovery in single-cell-resolution spatial transcriptomics data via cell-cell interaction-aware cell embedding"，Cell Systems 2024） |
| 精选级 | S |
| 主分类 | 复核改判 P3 空间域·生态位（初判 P8 不当：SPACE 是已发布方法包/PyPI 工具，主产出为"组织模块"发现=空间域/模块识别；互作感知是建模手段而非产出；终审定夺） |
| 次要用途 | P4 细胞通讯：scripts/CCI 用 CellChat 构建 NSCLC 配体-受体互作对象，作为嵌入的互作先验 |
| 一句话功能 | 单细胞分辨率空间转录组的组织模块发现方法包（PyPI: space-srt）：PyTorch Geometric 图自编码器（GAE + 内积解码器）学习"细胞-细胞互作感知"的细胞嵌入，在嵌入空间聚类得到组织模块；CPU 可跑、推荐 GPU |
| License | MIT |
| 语言与规模 | Python；主表 Pythonx12；5.0 MB |
| 运行入口 | `pip install space-srt` 或源码 `python setup.py install`；需自装 PyTorch 与 PyTorch Geometric（版本须与 CUDA 对应）；example_data/MERFISH_sim.h5ad 模拟数据可立即上手；scripts/ 三个 NSCLC 应用 notebook；教程 tutorial-space.readthedocs.io |
| 复现难度 | 中 — 安装两行、带模拟数据；但官方教程自述"仍在编写中"（Still in progress），实际上手需读 notebook 与源码，PyTorch Geometric 的 CUDA 版本匹配是常见卡点 |
| 与范式的关系 | "互作感知嵌入→空间域/组织模块"方法范式，可作 P3 域识别候选工具，与 GraphSAGE/GNN 系空间域方法对照；候选池（方法工具，优先级高于论文复现） |
| 坑提示 | ① 教程文档未完成（README 自述），以 notebook 为准；② space/model.py 内 seed 硬编码 42（seed_everything），复现他人结果时留意被覆写；③ scripts/ 的 Roe_NSCLC/SES_slice153/SUS_NSCLC_score.ipynb 为论文应用脚本，NSCLC 数据需另行获取；④ GPU 非必需但 CPU 训练大切片会慢 |
| 锁定 SHA | 6fc15f9eb84267e8eaa2f2a2c34f1508a0d5db09（主表） |

## 结构速览

- `space/`：model.py（SPACE_Graph=GAE+InnerProductDecoder）、layer.py、train.py、function.py、utils.py
- `scripts/`：CCI/（0_NSCLC_CCI_data.ipynb、1_cellchat_object_NSCLC.ipynb）+ Roe_NSCLC.ipynb、SES_slice153.ipynb、SUS_NSCLC_score.ipynb
- `example_data/MERFISH_sim.h5ad` + `requirements.txt` + `setup.py`/`pyproject.toml` + `LICENSE`
- 关联：无同作者其他仓在库；P3 域识别对照仓见分类体系 P3 系（niche/domain/community）

## README/代码实读要点

- SPACE = Spatial transcriptomics Analysis via Cell Embedding；PyTorch 框架，GPU 推荐
- PyPI 包名 space-srt；另有 GitHub 源码安装（最新开发版）
- 引用指向 Cell Systems 2024（Li, Zhang, Gao, Zhang Q.C.）

## 抽读实录

- 读 README 全文；head space/model.py（25 行，确认 GAE/内积解码器/seed=42）；ls space/、scripts/、scripts/CCI/、example_data/。

## 复用建议

- 在 zoro-spatial 的域识别/模块发现环节可作候选工具试跑（MERFISH_sim 半小时内有感）；正式使用前从 scripts/ 的 CellChat 对象构建 notebook 反推互作输入格式；留意其嵌入seed与 PyG 版本。
