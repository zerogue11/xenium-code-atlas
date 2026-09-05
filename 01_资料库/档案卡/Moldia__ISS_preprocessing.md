# `Moldia/ISS_preprocessing`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\Moldia__ISS_preprocessing`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-017：《演变中神经炎症病变和多发性硬化症病理的细胞结构》（Cell 2024） |
| 精选级 | S |
| 主分类 | P0 流程基准与质控（复核确认，与初判一致；分类体系 P0 明确列 ISS 前后处理） |
| 次要用途 | ASHLAR 拼接封装与显微镜私有格式转换的调用范例 |
| 一句话功能 | ISS（原位测序）数据预处理 Python 包：Zeiss/Leica 原始图像转 OME-TIFF（zen_OME_tiff、czi_to_tiff、leica_OME_tiff）、循环图像堆叠、ASHLAR 对齐拼接（ashlar_wrapper）、重切 tile（reshape_split、tile_stitched_images），配 demo notebook |
| License | 无LICENSE(仅可学习不可转载)（主表值） |
| 语言与规模 | Python；py/ipynb 6 个；体积 0.2 MB |
| 运行入口 | installation.sh（一键连装 ISS_preprocessing/decoding/postprocessing 三包）+ preprocessing.yml conda 环境 + ISS_preprocessing.ipynb、Stacking_files_demo.ipynb |
| 复现难度 | 中 — 有安装脚本与 yml，但依赖版本停在 2021 年代（ipykernel 5.3.4、ipython 7.18.1、jupyterlab 3.2.9），新机重建环境可能踩旧包兼容坑 |
| 与范式的关系 | LIT-017 ISS 图像链前端：显微镜私有格式→OME-TIFF→ASHLAR 拼接→tile 的封装方式可借鉴到任何 cycle 图像配准场景；候选池 |
| 坑提示 | ① 面向 Leica/Zeiss 显微镜私有格式的硬件语境强，无对应机型时多数函数用不上；② 无 LICENSE；③ pip 源码包（setup.py+dist）与 egg-info/__pycache__ 杂物入库 |
| 锁定 SHA | `b44f242a8425a78eb48f98642b8cc216ee716bf4`（主表锁定值；建卡时实测前缀 `b44f242a84` 一致） |

## 结构速览

- `ISS_processing/preprocessing.py`：全部功能函数
- `__init__.py`：显式导出 10 个函数——zen_OME_tiff、ashlar_wrapper、reshape_split、leica_mipping、leica_OME_tiff、tile_stitched_images、preprocessing_main_leica、czi_to_tiff、stack_cycle_images_zeiss、stack_cycle_images_leica
- `installation.sh`（三包联装）、`preprocessing.yml`、`setup.py`
- 两个 notebook：主流程 + 堆叠文件 demo；`dist/`、`ISS_processing.egg-info`（打包杂物）

## README/代码实读要点

- README 仅 6 行：定位（alignment + stitching 用 ASHLAR + retiling）与安装方式
- ASHLAR 为外链依赖（labsyspharm/ashlar），本包只做 wrapper
- 三包（pre/dec/post）设计为一个 installation.sh 统一安装，配套 Cell 2024 论文的 ISS 全链
- 环境 yml 通道为 anaconda/defaults/conda-forge 混合，pip 段未细读【待补充】

## 抽读实录

- 读 README 全文；ls 包目录；读 ISS_processing/__init__.py（函数导出清单）与 preprocessing.yml 头部（依赖版本）。

## 复用建议

- 只在不涉及其工作流时参考 ashlar_wrapper 的调用方式；Leica/Zeiss 格式转换函数仅在拥有对应显微数据时有用；Windows 下中文路径处理【待验证】。
