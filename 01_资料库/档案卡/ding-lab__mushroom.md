# `ding-lab/mushroom`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\ding-lab__mushroom`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-019：《肿瘤在二维和三维空间中的进化与微环境相互作用》（Nature 2024）；LIT-071：《乳腺癌和前列腺癌前期到癌症转变的空间映射》（Cancer Discovery 2026） |
| 精选级 | S |
| 主分类 | P1 分割与重分割（复核确认，与初判一致；分类体系 P1 明确列 mushroom；实质为 3D 连续切片配准+区域/ROI 分割分析工作流） |
| 次要用途 | P6 空间统计·配准·3D（BigWarp/napari 配准链）；P7 图像组学（H&E 通道蛋白预测 U-Net） |
| 一句话功能 | 3D 逐切片配准与分析工作流：多模态（ST+H&E 等）连续切片 BigWarp/napari 配准、H&E 蛋白表达预测模型训练、3D ROI 生成与定量、上皮区域自动检测、DEG 分析；先后支撑 LIT-019（subclone 线）与 LIT-071（癌前转变线）两篇论文 |
| License | MIT（主表值，与仓库 LICENSE 一致） |
| 语言与规模 | Python；py/ipynb 252 个 + R 1 个；体积 953.7 MB（含大 notebook/历史版本目录，本次未进入大数据子目录） |
| 运行入口 | conda 新环境（python 3.11 + jupyter）→ pip install git+... → notebooks/tutorials 三部曲：data_preperation_and_registration → mushroom_tutorial → output_analysis |
| 复现难度 | 高 — 3D 多模态配准含 BigWarp(Fiji) 与 napari 人工交互标定点环节，数据体量大；README 自述 under active development、API subject to change |
| 与范式的关系 | "连续切片 ST→3D 重构→区域分割→DEG"是本项目 HE→表达预测支线之外的 3D 高阶范式参考；H&E 蛋白预测（he_channel_prediction.ipynb）与 zoro-spatial 的形态-表达对齐直接相关；候选池 |
| 坑提示 | ① 953MB：notebooks/ 下混有 examples_old、old、manuscript（submission_v1/v2）多套历史版本，引用前先认版本（LIT-071 材料在 submission_v2，LIT-019 分析在 subclone-resubmission 分支）；② API 不稳定，教程即文档；③ 无 environment.yml，靠 conda+pip 命令行建环境 |
| 锁定 SHA | 【待补充：主表"锁定SHA"列空】；本地克隆 HEAD 实测 `dc3598950f` |

## 结构速览

- `mushroom/`：主包——mushroom.py（主流程）、registration/（bigwarp.py、napari 接口等）、data/、model/、visualization/、utils.py
- `notebooks/tutorials/`：三份官方教程（配准→运行→输出分析）
- `notebooks/manuscript/`：submission_v1（he_channel_prediction、analyses_brca_v3）与 submission_v2（step1 注册→step2 ROI→step5 区域→step6 DEG）
- `notebooks/examples|examples_old|old|projects|napari/`：历史版本与项目脚本
- `setup.py`、`LICENSE`、`README.md`

## README/代码实读要点

- 官方推荐隔离安装：conda create -n mushroom -c conda-forge python=3.11 jupyter → pip install git+…
- 两篇论文材料索引齐全：LIT-071 线 = H&E 蛋白预测模型训练（submission_v1）+ 注册/ROI/区域/DEG 四步（submission_v2）；LIT-019 线 = subclone-resubmission 分支的邻域模型训练与图 6 分析
- README 双声明："Under active development" 与 "API subject to change..."
- registration/ 内含 bigwarp.py 与 napari 接口，说明配准有人工标定环节（Fiji BigWarp 工作流）

## 抽读实录

- 读 README 全文（安装、教程链接、两篇论文材料索引）；ls mushroom/、registration/、notebooks/（未进入大数据子目录）。

## 复用建议

- 作 3D 范式阅读源（不急跑通）：先读 tutorials 三部曲理解数据组织；HE 蛋白预测 notebook 与 zoro-spatial HE→表达支线直接对标；真要跑先 fork 冻结 commit。
