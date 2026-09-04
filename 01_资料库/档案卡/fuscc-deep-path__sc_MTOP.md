# `fuscc-deep-path/sc_MTOP`（档案卡）

> 由 agent 依据本地克隆实测撰写；不确定处一律【待补充】；禁止编造星标/日期/功能。

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-034;LIT-081：《HER2乳腺癌ADC疗效空间决定因素》——sc-MTOP 官方 PyTorch 实现；与 LIT-081 的 Lion-shine 仓（Segment-Membranes-and-Nuclei...）同论文不同仓，可对照 |
| 精选级 | A |
| 主分类 | P7（复核改判，主表初判 P8）——核心交付是 H&E WSI 的核分割+单细胞形态/纹理/拓扑特征，正对 P7"图像组学·形态学特征"定义 |
| 次要用途 | P8（HER2 ADC 疗效场景分析框架）；P1（HoVer-Net 核分割分类） |
| 一句话功能 | 基于数字病理的单细胞形态与拓扑剖析框架：HoVer-Net（PanNuke 预训练）核分割分类 → 逐细胞形态/纹理/拓扑特征与细胞邻接边表提取 → ImageScope 注释层可视化 |
| License | MIT |
| 语言与规模 | Python x47 / Shell x2；0.4MB（不含预训练权重与数据） |
| 运行入口 | CLI 三子命令（segment/feature/visual，经 main.py）；requirements.txt；权重与 demo 数据从 GitHub release 下载 |
| 复现难度 | 中 — README 全流程可跑，但硬件门槛高：GPU 显存>8GB、RAM≥128GB、SSD≥100GB 缓存；openslide 跨平台安装需单独处理 |
| 与范式的关系 | P7 形态学特征候选池：输出设计（特征 csv + 边表 csv，带 cell ID 与质心坐标）可直接复用；与 Lion-shine 仓互为同论文两条技术线 |
| 坑提示 | ① 仅分割步支持批处理；② segment 单样本约 2h（2080Ti）；③ 过大 ROI 的注释文件 ImageScope 打不开；④ 实测环境为 Windows 与 Ubuntu 16.04.7 |
| 锁定 SHA | 主表未登记（空）；本地克隆 HEAD `33ff31fbd01f37705118244da0a8df96a4f19014` |

## 结构速览

- `main.py`：segment / feature / visual 三个子命令总入口（README 给 Ubuntu bash 演示）。
- `F1_CellSegment.py`：调 `Hover/`（vqdang/hover_net 官方实现的克隆）做核分割+分类。
  - 输入 .ndpi 等 WSI（理论支持 HoVer-Net 全部格式）。
  - 输出逐样本 json（全部核实例与分类信息）。
  - 预训练模型 hovernet_fast_pannuke_type_tf2pytorch.tar，README 给 release wget 直链。
- `F3_FeatureExtract.py` + `WSIGraph.py`：特征提取。
  - 输入 WSI + 分割 json；可选 ImageScope（Aperio）xml 注释定义 ROI。
  - 输出每样本 4 个 csv：肿瘤/炎症/基质三类细胞各一（逐细胞特征 + cell ID + 质心坐标）、边表一（相连 cell ID 对）。
- `F4_Visualization.py` + `utils_xml.py`：把分割与核图写回 ImageScope 注释文件，供人工复核。
- 依赖：PyTorch + openslide-python（Linux/Windows 安装路径不同，README 链官方文档）。

## 实读补充（demo 命令与耗时，README 自述）

- segment：`python main.py segment --input_dir='./wsi' --output_dir='./output'`，约 2h（2080Ti + SSD）。
- feature：约 40min（128GB RAM、8 进程）。
- visual：输出到 fun_fig 目录，回写注释层。
- 硬件要求原文：GPU>8GB 显存；HoVer-Net 需 SSD≥100GB 做缓存；RAM≥128GB。

## 复核说明

- 改判 P7 的依据：分类体系 P7 = "H&E/多重离子成像整合、形态学特征、图像-表达对齐"，
  本仓交付即"核分割 + 形态/纹理/拓扑特征"，是典型图像组学件；疾病应用（HER2 ADC）
  是使用场景而非仓的内容主体，写入次要用途。
