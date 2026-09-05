# `Lion-shine/Segment-Membranes-and-Nuclei-from-Histopathological-Images-via-Nuclei-Point-level-Supervision`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\Lion-shine__Segment-Membranes-...-Supervision`（全名过长，目录为原名）

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-081：《一种基于空间可解释人工智能的框架，用于为HER2阳性乳腺癌患者量身定制新辅助双重HER2阻断治疗》（STTT 2026）；注意：本仓 README 自述代码对应 MICCAI 2023 论文"Segment Membranes and Nuclei from Histopathological Images via Nuclei Point-level Supervision" |
| 精选级 | A |
| 主分类 | P1 分割与重分割（复核确认，与初判一致；核/膜分割，属分类体系 P1"nuclei 系"） |
| 次要用途 | P7 图像组学（IHC 膜染色图像的形态学量化前端） |
| 一句话功能 | PyTorch 弱监督分割代码：仅需细胞核点级标注（完整膜/不完整膜/无膜三色点），以 Seg-Net（分割膜与核）+ Tran-Net（分割结果转语义点）双网络在 IHC 膜染色图像上做膜与核分割，达到全监督约 81% IoU / 86% F1 的性能 |
| License | 无LICENSE(仅可学习不可转载)（主表值） |
| 语言与规模 | Python；py/ipynb 28 个；体积 7.4 MB |
| 运行入口 | python train.py / test.py（全部参数集中在 options.py）；scripts/run_GlaS.sh、run_MO.sh；数据先经 prepare_data.py 转成 .h5 |
| 复现难度 | 高 — 锁 torch==1.5.0（2020 年代栈，新 GPU/CUDA 兼容差【待验证】），且需自备点级标注 .h5 数据 |
| 与范式的关系 | 弱监督（点级监督）省标注思想对 IHC/HE 预分割有参考价值；与 hover_net 同属 LIT-081 工具栈，但本仓偏方法学、非 ST 流程核心；观察池 |
| 坑提示 | ① 无 LICENSE；② torch==1.5.0 环境在现代硬件上难以复现；③ README 引用的 PDF 链接为空（"(https://doi.org/)"未填）；④ 代码基于 huiqu18/FullNet-varCE 改造（README 已声明并要求引其原文） |
| 锁定 SHA | `0c507a4701207037c9d76bad6a262eff6d8add96`（主表锁定值；建卡时实测前缀 `0c507a4701` 一致） |

## 结构速览

- 训练/评测主线：train.py、test.py、options.py（dataset 默认 'her2'、model='Unet'、out_c=4、n_layers=4）、FullNet.py、attention_unet.py、nested_unet.py
- 损失/评测：loss.py、dice_loss.py、eval_utils.py、elu_vis.py
- 推理变体：infer.py、infer_membrane_nuclei.py、infer_membrane_nuclei_PDL1.py、multi_cls_cell_seg.py
- 数据管线：prepare_data.py、generate_samples.py、dataselect.py、split.py、my_transforms.py、draw_label.py
- 资源杂物：scripts/（run_GlaS.sh、run_MO.sh）、images/（示意图）、mean_std.npy、color_card.jpg

## README/代码实读要点

- 监督信号定义：每个标注点携带位置（细胞质心）+ 膜染色状态（红=完整膜、蓝=不完整膜、绿=无膜）
- 数据准备：点标注+图像转字典格式存 .h5（prepare_data.py），训练/测试参数全走 options.py
- 性能声明：两个 IHC 膜染色数据集上达到全监督方法 81.36% IoU / 85.51% F1
- 默认 dataset='her2'，与 LIT-081 的 HER2 乳腺癌语境对应；另有 PDL1 推理变体

## 抽读实录

- 读 README 全文（方法、依赖、用法、双引用）；ls 顶层；读 options.py 开头 20 行（默认数据集与网络超参）。

## 复用建议

- 仅在需要"少量点标注启动 IHC 分割"时考虑；新项目优先 hover_net/cellpose，本仓留作弱监督思想参照；若启用需先解决 torch 1.5 环境隔离（uv/conda 独立环境）。
