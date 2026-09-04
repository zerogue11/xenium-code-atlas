# `Moldia/ISS_decoding`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\Moldia__ISS_decoding`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-017：《演变中神经炎症病变和多发性硬化症病理的细胞结构》（Cell 2024） |
| 精选级 | S |
| 主分类 | P0 流程基准与质控（复核确认，与初判一致） |
| 次要用途 | starfish 像素级解码流程的实例化参考 |
| 一句话功能 | ISS 数据解码 Python 包：按 SpaceTx 格式组织循环图像，用 starfish 做滤波→像素级解码（Codebook/DecodeSpots）→强度表→表达矩阵，并附 qc_metrics.py 质控函数，配 Example_decoding.ipynb |
| License | 无LICENSE(仅可学习不可转载)（主表值） |
| 语言与规模 | Python；py/ipynb 12 个；体积 5.7 MB |
| 运行入口 | notebook（ISS_decoding.ipynb、Example_decoding.ipynb）+ decoding.yml conda 环境 + setup.py |
| 复现难度 | 高 — 硬依赖 starfish/slicedimage 全家桶（starfish 近年基本停止维护【待核】，版本兼容极敏感），且需 ISS 循环图像原始数据 |
| 与范式的关系 | LIT-017 解码段：SpaceTx Codebook 像素解码 + 精确匹配 spot trace 的完整链路实例，对理解 ISS/CartaNA 类数据解码原理有价值；候选池（依赖风险高，借鉴思路优先于跑通） |
| 坑提示 | ① decoding.py 顶层直接 import starfish 内部模块（starfish.core.spots.DecodeSpots.trace_builders.build_spot_traces_exact_match、starfish.core.expression_matrix 等），starfish 版本一变即崩；② 与 starfish 的版本组合以 decoding.yml 为准【待补充细读】；③ 无 LICENSE |
| 锁定 SHA | 【待补充：主表"锁定SHA"列空】；本地克隆 HEAD 实测 `10b318e1d8` |

## 结构速览

- `ISS_decoding/`：3 个模块——decoding.py（starfish 解码主链）、SpaceTx_format.py（SpaceTx 实验格式组织：FetchedTile/TileFetcher/write_experiment_json）、qc_metrics.py
- 两个 notebook：ISS_decoding.ipynb（主流程）、Example_decoding.ipynb（示例）
- `decoding.yml`、`setup.py`、`build/`、`dist/`、`ISS_decoding.egg-info`（打包杂物）

## README/代码实读要点

- README 仅 1 行："used to decode In situ sequencing data"，功能判断全靠代码
- decoding.py 开头 25 行全量 import starfish 的 image.Filter/ApplyTransform/LearnTransform/Segment 与 spots.FindSpots/DecodeSpots/AssignTargets，即完整 starfish 解析链
- 顶层有 `test = os.getenv("TESTING") is not None` 开关，提示作者与 starfish 测试体系耦合
- SpaceTx_format.py 按 starfish.experiment.builder 组织 tile，说明数据须先转 SpaceTx 格式才能进解码

## 抽读实录

- 读 README 全文；ls 包目录；读 decoding.py 开头 25 行（确认 starfish 依赖链与顶层 import）。

## 复用建议

- 不建议整包跑通（starfish 老栈风险）；价值在读懂"Codebook→像素解码→强度表"的 ISS 解码原理，以及在 qc_metrics.py 中挑可用的质控指标定义。
