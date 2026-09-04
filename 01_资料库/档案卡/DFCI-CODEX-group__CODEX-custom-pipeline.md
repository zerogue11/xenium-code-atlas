# `DFCI-CODEX-group/CODEX-custom-pipeline`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\DFCI-CODEX-group__CODEX-custom-pipeline`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-079：溶瘤病毒治疗 GBM（配套 CODEX 分析管线；论文题名未在 README 出现【待补充】） |
| 精选级 | A |
| 主分类 | P7 图像组学·多模态（复核确认：CODEX 多重离子成像→分割→定量→counts 的标准化管线；与初判一致） |
| 次要用途 | P3 边缘：REDSEA 邻域感知定量与 structuring element 实验 notebook（空间校正定量思想） |
| 一句话功能 | DFCI 分子影像核心的 CODEX 自定义管线：基于 PathML 对 Akoya CODEX 多循环图像做细胞分割（SegmentMIF）+ 膜标记 watershed + REDSEA 邻域感知定量 + 边缘细胞过滤，输出 .h5path（内含 AnnData counts）与仅供 MAV 查看的 csv |
| License | 无LICENSE(仅可学习不可转载) |
| 语言与规模 | Python；主表 Pythonx5；0.7 MB |
| 运行入口 | conda env create -f environment.yml（环境名 codex）→ pip install pathml → `python codex-pathml.py --input-image ... --nucleus_marker_cycle_index ... --cytoplasm_marker_cycle_index ... --metadata experiment.json --tile-size 2048`；两个 ipynb 为 REDSEA 结构元素实验与合成图 |
| 复现难度 | 中 — 单命令行入口、参数少、README 步骤完整；但 pathml+javabridge+tensorflow 环境沉重，且上游必须先用 Akoya CODEX Processor v1.8.1.9 完成背景扣除/去卷积/阴影校正 |
| 与范式的关系 | PathML 官方 toolkit 的机构定制范例：多重蛋白成像"标准化→分割→定量"骨架可整体借鉴；REDSEA（邻域感知扣分）是亮点方法；观察池 |
| 坑提示 | ① codex-pathml.py 顶部 import javabridge（README 安装节未提），javabridge 在 Windows 几乎装不上，建议 WSL/Linux；② bfconvert 堆图前须把文件名 cycle 改成 t<###>（README 强调否则 BioFormats 识别失败），通道索引全 0-based；③ counts 的 .csv 仅供 MAV 查看器，正式下游用 .h5path 里的 AnnData；④ 自定义变换（FilterEdgeCells/MembraneMarkerWatershed/REDSEAQuantifyMIF）全部在本地 transforms.py，版本漂移时优先核对它 |
| 锁定 SHA | 65a8b3e4a7f93b01b776c1acd8980c9584f3e6b2（主表） |

## 结构速览

- `codex-pathml.py`：唯一主入口（argparse CLI，读入堆叠 ome.tif → PathML Pipeline → 输出）
- `transforms.py`：4 个自定义 PathML 变换（FilterEdgeCells、MembraneMarkerWatershed、REDSEAQuantifyMIF、CheckNACounts）
- `environment.yml`（conda codex 环境）+ `REDSEA_structuring_element_experiment.ipynb` + `composite_images.ipynb`/`composite_visualization.py`
- 关联仓：estorrs/multiplex-imaging-pipeline（同为多重成像分割→定量管线，功能部分重叠、技术栈不同）

## README/代码实读要点

- 分工明确：Akoya CODEX Processor 负责上游光学校正（明确排除在本仓外），本仓只做分割→定量→counts
- 支持 150+ 输入格式（PathML/bioformats），示例流程含 bfconvert 堆图 + pattern 文件写法
- 输出 .h5path 的 AnnData 与 ScanPy/Seurat 生态互通

## 抽读实录

- 读 README 全文；head codex-pathml.py（30 行，确认 javabridge/tf/pathml 依赖与 REDSEA import）；ls 顶层。

## 复用建议

- Xenium 蛋白 panel/CODEX 类数据需要"分割+邻域校正定量"时，其 transforms.py 四个变换可单独搬用（PathML 生态内）；环境部署直接按 WSL + conda 走，勿在原生 Windows 尝试。
