# `ding-lab/morph`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\ding-lab__morph`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-019：《肿瘤在二维和三维空间中的进化与微环境相互作用》（Nature 2024） |
| 精选级 | A |
| 主分类 | P1 分割与重分割（复核确认，与初判一致；数学形态学划分肿瘤/外周区域，属空间重分割工具） |
| 次要用途 | P8 疾病应用（TME 分区与肿瘤边界距离特征，服务下游 spatial CNV/细胞分布/通讯分析） |
| 一句话功能 | 基于数学形态学的 ST 肿瘤区域提取工具集：由转录本坐标构建 backbone 图像（任意分辨率/非矩形网格），施加腐蚀/膨胀/开/闭等形态学操作与自定义结构元（如六边形），自动提取肿瘤 microregion、外周层与相关距离特征；在 6 癌种 117 张 ST 切片验证，秒级运行 |
| License | MIT（主表值，与仓库 LICENSE 一致） |
| 语言与规模 | Python；py 7 个；体积 0.4 MB |
| 运行入口 | pip install git+https://git@github.com/ding-lab/morph.git；README 给出 Xenium 示例：readers.transcripts → backbone(...) → Mapper().xenium(cells, d) → writers.xenium |
| 复现难度 | 低-中 — 纯 Python 小模块、无重依赖、输入为标准 transcripts.csv.gz/cells.csv.gz；但除 README 片段外无 notebook 教程【待补充】 |
| 与范式的关系 | 肿瘤/基质自动分区+距离层特征，可接在 zoro-spatial 注释之后做 TME 分区、肿瘤-基质界面分析；与 mushroom 同作者（LIT-019 栈）；观察池→低成本可试 |
| 坑提示 | ① pip 包名 Morph（import Morph）与仓库名 morph 大小写不一致；② 功能描述主要来自 README，模块内部（backbone/features/operators）未逐行核验；③ 无 conda 锁环境文件 |
| 锁定 SHA | `ba1db03976a72f0da0558e87207054ef9404309b`（主表锁定值；建卡时实测前缀 `ba1db03976` 一致） |

## 结构速览

- `Morph/`：6 个模块——backbone.py（转录本→图像骨架）、operators.py（形态学操作与结构元）、features.py（区域/距离特征）、modules.py（Mapper 等胶水）、readers.py、writers.py
- `pyproject.toml`、`LICENSE`（MIT）、`image.png`（示意图）
- README：一段完整的方法介绍 + 一个可复制的 Xenium 运行片段 + 作者联系方式（andretargino@wustl.edu）

## README/代码实读要点

- 示例参数组：d=10、G={'TFF2','KRT7'}（backbone 通道基因）、S=3×3 结构元、tau=3、lambda_=4
- 运行链：transcripts 读入→backbone（xenium, d, total+G, maximum, closing, binary, area_opening, blob）→cells 读入→Mapper().xenium(cells, d)→writers.xenium 写回 csv
- 方法特征：不限平台、支持六边形点阵（Visium），无近似、每样本秒级
- 接受多输入类型：肿瘤纯度、人工标注等均可作 backbone 通道

## 抽读实录

- 读 README 全文（含完整 Xenium 运行片段）；ls Morph/ 包目录。

## 复用建议

- 用自家 Xenium 数据以 README 片段为起点试跑（成本极低）；输出的肿瘤区/外周层标签可与注释列并轨做 TME 分区；试跑前先核 operators.py 的操作语义与 README 是否一致。
