# `Teichlab/drug2cell`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\Teichlab__drug2cell`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-018：《人类胚胎骨骼发育多组学图谱》（Nature 2024）；注：README 引用的方法出处为 Kanemaru 2023 心脏 niche 论文（Nature 619:801-810），drug2cell 系公开发布方法包，LIT-018 中作为配套工具使用 |
| 精选级 | S |
| 主分类 | P5 亚细胞·转录本定位（复核确认：分类体系 P5 明确列"drug2cell"；与初判一致） |
| 次要用途 | 任意基因群（通路/基因模块/自定义集合）逐细胞打分与富集的 scanpy 通用工具 |
| 一句话功能 | scanpy 插件式基因群活性评估工具：d2c.score() 按基因群（默认 ChEMBL 药物-靶点集）逐细胞打分并写入 .uns['drug2cell']，d2c.gsea()/d2c.hypergeometric() 基于 rank_genes_groups 结果做富集/过表达分析 |
| License | 自定义 GRL（Genome Research Ltd/Sanger）非商业许可：LICENSE 首段明言 "solely for non-commercial use"；主表"自定义LICENSE(需人工核)"属实，非 OSI 开源 |
| 语言与规模 | Python；主表 Pythonx9；4.5 MB；包内预置 drug-target_dicts.pkl 与 cpdb_dict.pkl 两个数据字典 |
| 运行入口 | `pip install drug2cell` → `import drug2cell as d2c`；notebooks/demo.ipynb 主示例；文档 drug2cell.readthedocs.io |
| 复现难度 | 低 — pip 装包即用，demo notebook 完整；仅依赖 scanpy 生态，无需外部数据即可上手 |
| 与范式的关系 | "药物扰动视角读细胞状态"范式：在空间/单细胞图谱上做药靶集打分反推可干预节点；与 snp2cell 同为 LIT-018 方法件；候选池（即插即用） |
| 坑提示 | ① 许可限非商业用途，再分发/转载需留意；② ChEMBL 预解析数据源为 ftp.sanger.ac.uk 外链（chembl_30 pkl），可能失效【待验证】；③ gsea/hypergeometric 需先跑 sc.tl.rank_genes_groups()；④ 换自定义基因集需按 dict{组名:[基因]} 格式传入 targets 参数 |
| 锁定 SHA | a786c632fc521b94f597e452e2f09c45fd451640（主表） |

## 结构速览

- `drug2cell/`：util.py（score/gsea/hypergeometric 实现）、chembl.py（ChEMBL 解析助手）、data.py + 两个预解析 pkl
- `notebooks/demo.ipynb`：官方演示；`notebooks/chembl/`：filtering.ipynb、initial_database_parsing.ipynb（ChEMBL 数据库解析复现）
- `setup.py` + `docs/`（ReadTheDocs 源）+ `LICENSE` + `CHANGELOG.md`
- 关联仓：Teichlab/snp2cell（同文献方法件）、Teichlab/skeletal_dev_atlas（LIT-018 图谱数据仓）

## README/代码实读要点

- score() 产出的基因群特征空间对象会复制原对象 .obs/.obsm，便于直接接绘图与 marker 检测
- 支持完全自定义基因群字典；ChEMBL 药靶集为默认随包数据
- 引用格式指向心脏 niche 论文（Kanemaru et al. 2023）

## 抽读实录

- 读 README 全文 + LICENSE 首段；ls drug2cell/、notebooks/、notebooks/chembl/。

## 复用建议

- 可直接接入 zoro-scrna/zoro-spatial 流程：对 Xenium 注释后的 cluster 做 d2c.score + gsea，把"细胞状态"翻译成药物靶点语言；注意非商业许可在成果发布/工具集成时的边界。
