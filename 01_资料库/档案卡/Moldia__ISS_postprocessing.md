# `Moldia/ISS_postprocessing`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\Moldia__ISS_postprocessing`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-017：《演变中神经炎症病变和多发性硬化症病理的细胞结构》（Cell 2024） |
| 精选级 | S |
| 主分类 | P0 流程基准与质控（复核确认，与初判一致） |
| 次要用途 | P1 分割后处理（cellpose 核分割→表达矩阵→scanpy/squidpy 衔接范例） |
| 一句话功能 | ISS 数据后处理 Python 包：cellpose 核分割与分割后处理（segmentation.py）、pciSeq 对接导出（pciseq.py）、带注释对象构建（annotated_objects.py），附 Scanpy/Squidpy 两个教程 notebook 及其 html 快照 |
| License | MIT（主表值，与仓库 LICENSE.txt 一致；Moldia 三包中唯一有宽松许可的） |
| 语言与规模 | Python；py/ipynb 8 个；体积 40.7 MB |
| 运行入口 | notebook（Scanpy_tutorial.ipynb、Squidpy_tutorial.ipynb、ISS_postprocessing_tutorial_scanpy.ipynb/.html）+ postprocessing.yml + setup.py |
| 复现难度 | 中 — 有 yml 与成套教程，但 cellpose 模型在模块导入时即实例化（需联网下权重），新机 cellpose 版本兼容【待补充】 |
| 与范式的关系 | "分割→表达矩阵→scanpy/squidpy 空间对象"的衔接范式与 zoro-spatial 下游完全同构，annotated_objects 的注释回写思路可借鉴；候选池 |
| 坑提示 | ① segmentation.py 顶层执行 `models.Cellpose(gpu=False, model_type='nuclei')`——import 即加载模型，无网/CI 环境直接卡死，且默认走 CPU；② 体积 40MB 主要为教程 html 与打包杂物；③ 教程基于 ISS 数据，平台参数不适用于 Xenium |
| 锁定 SHA | `3c779c6bc1673c73a21a3dfd30212e80945c084a`（主表锁定值；建卡时实测前缀 `3c779c6bc1` 一致） |

## 结构速览

- `ISS_postprocessing/`：3 个模块——segmentation.py（cellpose 核分割 + skimage/scipy 形态学后处理）、pciseq.py（pciSeq 对接）、annotated_objects.py（带注释空间对象）
- 3 组教程 notebook：Scanpy_tutorial、Squidpy_tutorial、ISS_postprocessing_tutorial_scanpy（附同名 .html）
- `postprocessing.yml`、`setup.py`、`dist/`、`ISS_postprocessing.egg-info`

## README/代码实读要点

- README 仅 1 行："used to postprocess In situ sequencinig data"，全靠代码与教程判断
- segmentation.py 顶部即定义 cellpose nuclei 模型并 import cellpose/skimage 全套（measure/morphology/segmentation），后处理链在模块层
- 三包中唯一含 LICENSE.txt（MIT），与 preprocessing/decoding 的无 LICENSE 形成对比
- html 教程快照可直接浏览器打开核对输出效果，不必先跑代码

## 抽读实录

- 读 README 全文；ls 包目录；读 segmentation.py 开头 15 行（确认顶层 cellpose 模型实例化与 skimage 依赖面）。

## 复用建议

- 取"分割后对象→scanpy/squidpy 衔接"的代码模式而非数据；引用前把 cellpose 初始化移入函数体以避免 import 副作用； pciSeq 对接段仅在做 ISS 空间推断时有用【待补充】。
