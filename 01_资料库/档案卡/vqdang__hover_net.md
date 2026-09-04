# `vqdang/hover_net`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\vqdang__hover_net`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-081：《一种基于空间可解释人工智能的框架，用于为HER2阳性乳腺癌患者量身定制新辅助双重HER2阻断治疗》（STTT 2026）；本仓为 HoVer-Net 官方实现（Med Image Anal 2019），被 LIT-081 用作核分割器 |
| 精选级 | S |
| 主分类 | P1 分割与重分割（复核确认，与初判一致；分类体系 P1 明确列 hover-net） |
| 次要用途 | P7 图像组学（HE/IF 图像的核级形态输入源，服务 HE→表达预测支线） |
| 一句话功能 | HoVer-Net 官方 PyTorch 实现：多分支网络用核像素到质心的水平/垂直距离图分离黏连核，同时完成核实例分割与类型分类；支持 tile 与 WSI（OpenSlide）推理，官方提供 CoNSeP/PanNuke/MoNuSAC/Kumar/CPM17 五套预训练权重，输出 json（bbox/centroid/contour/type）与 QuPath 兼容格式 |
| License | MIT（主表值，与 LICENSE 一致；注意 PanNuke 衍生权重为 CC BY-NC-SA 4.0 非商业） |
| 语言与规模 | Python；py/ipynb 42 个；体积 51.9 MB |
| 运行入口 | conda env（environment.yml）+ pip 装 torch==1.6.0/torchvision==0.7.0；run_train.py / run_infer.py（--model_mode original|fast）+ run_tile.sh、run_wsi.sh；权重经 convert_chkpt_tf2pytorch.py 由 TF 版转换 |
| 复现难度 | 中-高 — 锁 torch==1.6.0 + CUDA 10.2；WSI 推理要求 ≥100GB SSD 缓存目录；checkpoint 与 model_mode 必须严格匹配（Kumar/CPM17/CoNSeP=original，PanNuke/MoNuSAC=fast） |
| 与范式的关系 | 核分割标杆基线：LIT-081 的分割即由它承担；预训练权重可直接用于 HE/IF 预处理，为形态学特征与空间映射供核级输入；候选池（P1 骨干工具） |
| 坑提示 | ① torch 1.6/CUDA 10.2 老栈在新显卡上装不上风险高【待验证】；② 全部预训练权重托管在 Google Drive，国内下载需代理；③ PanNuke 权重的 NC 许可对商业/发表用途有约束；④ type_info.json 需按数据集改 overlay 颜色映射 |
| 锁定 SHA | 【待补充：主表"锁定SHA"列空】；本地克隆 HEAD 实测 `67e2ce5e3f` |

## 结构速览

- 主线脚本：run_train.py、run_infer.py、run_tile.sh、run_wsi.sh、config.py、dataset.py、extract_patches.py、compute_stats.py
- `models/`（hovernet 定义 + opt.py 超参/预训练权重路径）、`dataloader/`（增强管线）、`infer/`（base/tile/wsi 三级推理）
- `metrics/`（指标计算）、`run_utils/`（训练/验证循环与回调）、`misc/`
- `docs/`（图示）、`examples/usage.ipynb`（输出用法）、`type_info.json`、`convert_chkpt_tf2pytorch.py`+`variables_tf2pytorch.csv`

## README/代码实读要点

- 双模式推理：original（270×270 输入/80×80 输出，对应原论文）与 fast（256×256/164×164，PanNuke/MoNuSAC），checkpoint 文件名内标模式
- 输出规格：tile 出 json+mat+png overlay；WSI 出 json；可选 save_qupath（QuPath v0.2.3 兼容）、save_raw_map、draw_dot
- WSI 关键参数：proc_mag 默认 40×、cache_path 需 ≥100GB SSD、tile_shape 2048、ambiguous_size 128
- README 给出 TF vs PyTorch 复现对照表（Kumar/CoNSeP 上 DICE/PQ/AJI 差异 <0.01 量级）
- 训练前置：config.py 改数据与 checkpoint 路径，models/hovernet/opt.py 挂 Preact-ResNet50 预训练权重

## 抽读实录

- 读 README 全文（环境、训练/推理选项、权重许可、TF/PyTorch 结果对照表）；ls infer/（base.py/tile.py/wsi.py）。

## 复用建议

- 只用推理不用训练：PanNuke 分割+分类权重适配 HE/IF 常规核型；环境建议用 conda 独立环境锁 torch 1.6（或走 papermill/WSL）；输出 json 的 centroid/type 可直接喂下游形态-表达映射模块。
