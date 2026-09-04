# `estorrs/multiplex-imaging-pipeline`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\estorrs__multiplex-imaging-pipeline`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-019（肿瘤 2D/3D 进化）与 LIT-071（乳腺/前列腺癌 3D 多模态）共用图像管线（README 未直接挂论文，按主表溯源） |
| 精选级 | S |
| 主分类 | P7 图像组学·多模态（复核确认：多重成像 ome.tiff 生成→deepcell 分割→空间/区域特征→CWL 全流程；与初判一致） |
| 次要用途 | P0 边缘：CWL 工作流 + HTAN 兼容 ome.tiff 规范化，带流程工程参考价值 |
| 一句话功能 | estorrs 的多重成像通用管线：mip CLI 四模式（make-ome / segment-ome / generate-spatial-features / generate-region-features），支持 phenocycler(.qptiff)/CODEX/raw tif 目录三种输入转 HTAN ome.tiff，deepcell(Mesmer) 分割，门控细胞注释与区域特征表，附 CWL 全流程与 docker 镜像 |
| License | MIT |
| 语言与规模 | Python（主表 Pythonx61/Shellx4）；199.6 MB（含 submodules/omero-wrapper 子模块与大量 notebook） |
| 运行入口 | `pip install git+...` → `mip` 命令（README 逐模式给参数文档）；env.yaml（conda：omero-py + pip deepcell/torch）；docker estorrs/multiplex-imaging-pipeline；cwl/*.cwl 全流程 |
| 复现难度 | 中 — CLI 参数文档化好、docker 兜底；但 deepcell 分割需注册 users.deepcell.org 访问令牌，且 README 自述 deepcell 安装"在大量机器上会报错"，官方推荐 docker 路线 |
| 与范式的关系 | 多重成像"标准化→分割→特征→注释"骨架参考（LIT-071 数据侧底座，与 3d-analysis/mushroom 同作者体系）；CWL 化流程组织可借鉴；候选池 |
| 坑提示 | ① README 自述 under active development：generate-region-features "slightly buggy"、generate-spatial-features "may not work as intended"，两个功能按半成品对待；② deepcell 需 DEEPCELL_ACCESS_TOKEN（docker 也要 -e 传入）；③ submodules/omero-wrapper 需 --recursive 克隆，缺子模块则 omero 相关流程不完整；④ notebooks/ 内大量 Untitled*.ipynb 开发稿，勿当文档读，有效参考是 cell_annotation*、batch_neighborhood_analysis_v1/v2、brca_subtyping_paper |
| 锁定 SHA | c351da1d41e284eef2f732b3553e5602438ed978（主表） |

## 结构速览

- `multiplex_imaging_pipeline/`：ome.py、segmentation.py、spatial_features.py、region_features.py、region_classification.py、multiplex_imaging_pipeline.py（CLI）+ utils.py（CHANNEL_MAPPING）
- `cwl/`：full_imaging_workflow 等 8 个 .cwl + template/defaults yaml（含 omero 与 no_thresholds 变体）
- `notebooks/`（约 20 个，手稿+开发稿混存）、`env.yaml`、`docker/`、`submodules/omero-wrapper`、`examples/test`
- 关联仓：estorrs/3d-analysis（LIT-071 手稿分析侧，S 级）、ding-lab/mushroom（同体系 3D 配准主线，S 级）

## README/代码实读要点

- make-ome 按 platform 区分输入（phenocycler .qptiff / codex imagej tif / raw 目录），--bbox 可裁多组织切片
- segment-ome 大图自动切块（--split-size 默认 25000，内存不足调小），输出 cell/nuclei 两张 labeled tif
- generate-spatial-features 产出 h5ad + txt 特征表 + 细胞类型上色 png；门控策略默认 yaml 可替换，支持手工阈值文件消除批次效应
- docker 为官方推荐的重依赖（deepcell）规避方案

## 抽读实录

- 读 README 全文（四模式参数）；ls multiplex_imaging_pipeline/、cwl/、notebooks/、submodules/；cat env.yaml。

## 复用建议

- 作 Xenium 蛋白 panel/PhenoCycler 数据的工程骨架：借"ome.tiff 规范化→分割→特征表"三段式与 CWL 模板；生产环境走 docker + token，region-features 结果需人工抽验。
