# `Goldrathlab/Spatial-TRM-paper`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\Goldrathlab__Spatial-TRM-paper`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-035：组织驻留记忆 CD8 T 细胞。英文原题 "Tissue-resident memory CD8 T cell diversity is spatiotemporally imprinted"（Nature 2025, s41586-024-08466-x；bioRxiv 2024.03.20.585130） |
| 精选级 | S |
| 主分类 | 复核维持 P8（疾病应用/大应用仓代表；小肠黏膜免疫，非肿瘤） |
| 次要用途 | P0/P5 边缘价值：7 条 Xenium/MERSCOPE/VisiumHD 处理管线 + 多模态图像配准（H&E/IF↔Xenium）工程范式 |
| 一句话功能 | 论文全复现仓：7 条空间数据处理管线（小鼠 Xenium 时间-course 双重复、MERSCOPE WT/TGFBR2-KO、人回肠 Xenium、VisiumHD、未感染对照、spatial CRISPR perturb）产出带转录本的 h5ad，再配 Figure_1~5+ED7 逐图 notebook 复现全部主图（含解剖轴分析、cytokine 梯度、spatial CellChat） |
| License | MIT |
| 语言与规模 | Pythonx195/Rx1；117.4 MB（本批 20 仓中最大应用仓）；.pixi.toml+pixi.lock 固定依赖；.devcontainer |
| 运行入口 | 逐图 Jupyter notebook（如 Figure_2/2abc.ipynb）；数据经 data/download.ipynb 从自托管站点下载；环境用 pixi install 或 devcontainer；上游分割走作者另维护的 xenium-segmentation/vizgen-segmentation nextflow 管线 |
| 复现难度 | 中 — pixi.lock+devcontainer 固定环境、数据下载脚本齐备、notebook 相对路径引用 ../data/adata/*.h5；但 7 条管线全跑耗时大，且限定 x64 Linux（作者明示 ARM64 macOS 不可用） |
| 与范式的关系 | 工程标杆：devcontainer+pixi.lock+数据下载 notebook+逐图映射表+pre-commit；科学上"解剖轴（绒毛长轴）空间坐标化→沿轴表达/互作分析"范式对 TME 轴分析有直接借鉴价值；候选池（工程与叙事两层） |
| 坑提示 | ① 细胞注释环节是人工探索（提供 excel/csv/json 存档），代码不完整，中间产物需邮件联系作者；② 部分分析 notebook 无输出（execution_count: null），需自跑；③ 依赖外部 nextflow 分割仓，复现上游需另行部署 |
| 锁定 SHA | ccd50e1cafb8ac86d3daa2a9b1194b81d04c0b56（主表） |

## 结构速览

- processing_pipelines/：7 条并行管线目录（Xenium_mouse_replicate_1/2、MERSCOPE_mouse、Xenium_human、visiumHD、Uninfected、perturb_spatial）+ alignment/（mouse/human 组织学配准）
- Figure_1~5/ + Extended_Data_Figure_7/：逐图 ipynb，README 有"图版→notebook"完整映射表
- data/：download.ipynb + 必需文件清单（8 个 h5ad、IF 对齐 txt、alignment npy、signatures、xenium_output）
- .devcontainer/ + pixi.toml + pixi.lock：可复现环境；pre-commit 配置

## README/代码实读要点

- 抽读 Figure_2/2abc.ipynb：scanpy 读 timecourse.h5ad 后自绘 Zissou 色表做空间图，纯绘图型 notebook，输入即处理产物 h5ad
- README 明示分割参数（tile.minimal_transcripts=300000、baysor.prior_segmentation_confidence=0.95 等）
- 数据自托管于 2024-spatial-trm.data.heeg.io；VisiumHD 数据也纳入（visium_hd.h5ad）

## 抽读实录

- 读 README 全文；head Figure_2/2abc.ipynb（前 60 行 JSON）；ls 顶层与 processing_pipelines 结构。

## 复用建议

- 三层借鉴：① pixi/devcontainer+数据下载脚本的仓工程规范（可作用户 xeno 项目级 AGENT.md 参照）；② "解剖轴→空间分布→CellChat 沿轴"分析叙事；③ MERSCOPE KO+Xenium 人鼠双平台联动的组织方式。跑通主线只需 data 下载+Figure notebook，上游分割管线不必先部署。
