# `Teichlab/skeletal_dev_atlas`（档案卡）

> 由 agent 依据本地克隆实测撰写；不确定处一律【待补充】；禁止编造星标/日期/功能。

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-018：《骨骼发育多组学图谱》（Nature 2024, doi:10.1038/s41586-024-08189-z） |
| 精选级 | A |
| 主分类 | P2（复核维持：胚胎骨骼发育多组学图谱） |
| 次要用途 | 调控推断（CellOracle GRN+perturbation、SCENIC+/cisTopic）；配套方法外链 snp2cell(P5)、iss_patcher(P1)、nf-fgwas |
| 一句话功能 | 人类胚胎骨骼发育多组学图谱论文的两个核心分析模块：CellOracle 基因调控网络/拟时序/扰动打分 notebook 序列 + SCENIC+/cisTopic 主题建模与 motif 富集 notebook 序列 |
| License | BSD |
| 语言与规模 | Python×21（均为 .py.ipynb 笔记本 + scanpy_helpers.py），0.2 MB |
| 运行入口 | Jupyter notebook（按字母序 A→J 串成流水线）；无 env/lock 文件，依赖 CellOracle、SCENIC+、cisTopic 重型栈【待补充版本号】 |
| 复现难度 | 中偏高：notebook 顺序清晰但输入数据（metacell h5ad、cisTopic 对象）需从论文数据源另取，且 GRN/主题建模栈安装重 |
| 与范式的关系 | 图谱 → GRN → 拟时 → 虚拟扰动打分的"发育图谱调控解读"路线参考；是否候选池待精读 |
| 坑提示 | README 明说"其余脚本 upon request"（仓库不完整）；核心重型依赖（snp2cell 等）是独立仓库，本仓只有调用侧 |
| 锁定 SHA | 91630a160f2fb62bf7a1cec3df4643fb7e5ede46 |

## 结构速览

- `celloracle/`：A 获取 metacell h5ad → B 运行 CellOracle → C 打分绘图 → D GRN+velocity → E pseudotime → F/G/H 背景梯度与扰动打分汇总。
- `scenicplus/`：A 准备 anndata → B/C cisTopic 对象构建与 barcode 映射 → D metacells 子集 → E cisTopic 绘图 → F/G 主题建模与评估 → H motif 富集 → I 运行 SCENIC+ → J 后处理。
- 两目录各带 `scanpy_helpers.py`；scenicplus 另有 `utils.py`。

## 实读要点

- README 全文极短：论文 DOI + 三个配套仓库外链（snp2cell、ISS-patcher、nf-fgwas）+ "additional scripts upon request"，即本仓只收录 GRN 调控两模块，ISS 修补等在别仓。
- celloracle 链以 metacell 为起点（`A_get_metacell_h5ad.py.ipynb`），后续含 GRN+velocity 融合（D）、背景梯度计算（F）与虚拟扰动打分汇总（G/H），是 CellOracle 官方流程之外的论文定制扩展。
- scenicplus 链覆盖 cisTopic 主题建模的建-评-选（F/G）与 motif 富集（H）→ SCENIC+ 主运行（I）→ 后处理（J），与主表另收的 Teichlab/snp2cell（S 级）形成上下游。

## 复现路径（怎么跑）

1. 数据与依赖先置：metacell 输入、cisTopic 输入的构建数据来源 README 未给（需回论文数据可得性声明），CellOracle/SCENIC+/cisTopic 安装为最大前置成本。
2. 调控线：celloracle A→H 顺序执行（metacell → GRN → velocity 融合 → pseudotime → 扰动打分）。
3. 顺式调控线：scenicplus A→J 顺序执行（cisTopic 对象 → metacell 子集 → 主题建模 → motif → SCENIC+ → 后处理）。

## 借鉴与风险

- 可移植点：两条 notebook 流水线的"字母序=执行序"命名纪律；CellOracle 虚拟扰动打分（perturbation scores）作为图谱→功能解释层。
- 风险：仓库自认不完整（upon request）；数据入口缺失使端到端复现断链，宜按模块借鉴而非整体复跑；A 级定级合理，暂不建议升 S。

