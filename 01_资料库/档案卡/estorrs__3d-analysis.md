# `estorrs/3d-analysis`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\estorrs__3d-analysis`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-071：乳腺/前列腺癌空间映射（README 英文原题 "3D Imaging and Multimodal Spatial Characterization of the Precancer-to-Cancer Transition in Breast and Prostate"） |
| 精选级 | S |
| 主分类 | P6 空间统计·配准·3D（复核确认：本项目 3D/配准代表仓；与初判一致） |
| 次要用途 | P8 边缘：CRC/乳腺癌 2D DEG、invasiveness masks、TAM 3D 分析等手稿级应用 notebook |
| 一句话功能 | LIT-071 手稿材料仓：CosMx/Visium/VisiumHD/Xenium 多平台预处理、sc 整合、2D DEG 检测与排序、功能验证、图 8 面板生成等编号 notebook；README 明确核心的配准与 3D ROI 工作流托管在 ding-lab/mushroom 仓 |
| License | MIT |
| 语言与规模 | Python（主表 Pythonx17/Shellx1/Rx1）；24.5 MB |
| 运行入口 | notebooks/ 编号 notebook（1_预处理 → 2_sc → 3_2d_degs → 4_deg_ranking → 5_func_validation → 6_supp → 7_figure8）；scripts/ 各平台 reference + config.json；compute1/launch_jupyter.sh（WashU HPC 启动器） |
| 复现难度 | 高 — 依赖 mushroom 仓配准产物与 HTAN 多平台原始数据，config.json 绑定作者数据路径，notebook 间有顺序依赖 |
| 与范式的关系 | 与 mushroom（本项目 S 级）构成"3D 配准 + 多模态量化"组合的公开分析侧；多平台（Visium/VisiumHD/CosMx/Xenium/CODEX）统一预处理 notebook 可直接借鉴；候选池（配合 mushroom 看） |
| 坑提示 | ① README 极简，5 个关键 notebook 链接直接指向 mushroom 仓，本仓不自足，须两仓联动；② scripts/config.json 是作者真实配置（含实际路径），与 config.example.json 对照后需重写；③ compute1/ 为 WashU compute1 集群专用脚本，本地无用；④ notebooks 内混有 evan_crc_stuff.ipynb、test.ipynb 等开发稿，甄别后使用 |
| 锁定 SHA | 14f04c1b787991898380305702c31d52c19fa694（主表） |

## 结构速览

- `notebooks/`：1_convert_rds/1_cosmx/1_visium/1_visiumhd 预处理、2_sc_analysis、3_2d_degs、4_deg_ranking、5_func_validation_canidates、6_supp_table_reformatting、7_figure8_panels、invasiveness_masks、tam_3d_analysis 等
- `scripts/`：codex/cosmx/he/visium/xenium_reference 子目录 + config.json、config.example.json + HTAN 元数据抽取脚本
- `docker/`（容器定义）+ `compute1/launch_jupyter.sh`（HPC）
- 关联仓：ding-lab/mushroom（核心配准工作流所在，S 级）、estorrs/multiplex-imaging-pipeline（同作者图像管线，S 级）

## README/代码实读要点

- README 全部内容即"手稿材料位置"清单：H&E 蛋白预测模型训练、serial section 配准、3D ROI 生成与定量、2D 上皮区域检测、区域连通性——5 条中 4 条指向 mushroom 仓
- 本仓独有贡献以 3_2d_degs.ipynb（自动 2D 上皮区域检测与定量）为代表
- 数据侧说明材料在 HTAN 体系内流转（htan_submission_parsing.ipynb）

## 抽读实录

- 读 README 全文；ls notebooks/、scripts/、compute1/（未进大数据子目录）。

## 复用建议

- 做 3D/多切片整合时与 mushroom 档案卡配套阅读：本仓提供"配准产物→下游定量/DEG"的完整下游范式；platform reference 目录结构可作为多平台数据组织模板。
