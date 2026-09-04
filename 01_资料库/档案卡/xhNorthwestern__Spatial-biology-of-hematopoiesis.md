# `xhNorthwestern/Spatial-biology-of-hematopoiesis`（档案卡）

> 由 agent 依据本地克隆实测撰写；不确定处一律【待补充】；禁止编造星标/日期/功能。

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-060：《红细胞生态位》空间造血研究（论文题录【待补充】，README 未给） |
| 精选级 | B |
| 主分类 | P8（疾病应用，复核维持） |
| 次要用途 | P3（Giotto 邻域/生态位）；PHZ 应激脾是独特场景 |
| 一句话功能 | 造血组织（小鼠/人骨髓、胎肝、脾、PHZ 处理脾）Visium + Xenium + scRNA 的 47 个按样本命名独立 R 脚本（Giotto Suite 4.0.x 为主，scRNA 用 Seurat 5.0.3） |
| License | 无LICENSE(仅可学习不可转载) |
| 语言与规模 | R x47；0.6MB |
| 运行入口 | 每样本一个 R 脚本；Xenium 系基于 Giotto（checkGiottoEnvironment + createGiottoInstructions，直读 Xenium 原生文件）；无 env 文件 |
| 复现难度 | 中 — README 明确软硬件与版本，数据需自行从 GEO 下载（accession【待补充】） |
| 与范式的关系 | 场景参考：发育（E13.5/E14.5 胎肝）-成体骨髓-应激脾（PHZ）三态对比；Giotto 直读 Xenium 亚细胞文件脚本可作模板。候选池：否 |
| 坑提示 | ① 每样本一文件的复制粘贴式脚本，路径/参数散在各文件（硬编码 ~/Desktop/...）；② Giotto 版本混用（4.0.2/4.0.5）；③ 无 LICENSE |
| 锁定 SHA | 主表未登记（空）；本地克隆 HEAD `ce5ab17641211505c12c97da6f0b779006d73f5b` |

## 结构速览

- Visium 系约 30 个脚本：人/小鼠骨髓各样本（1022D1、124C1、172C1、279C1、308D1、865D1、
  89 weeks BM、P8 BM、955D1、1067D1、1074D1、1279D1、1603D1 等）+ EDTA 处理骨髓 +
  Combined normal BM + 成体脾（WT1/WT2/C1qa KO1/KO2）+ E14.5 胎肝（KO2/KO4/Repeated/WT2/WT4）
  + 人 12/16 周胎肝。
- Xenium 系约 10 个：E14.5 胎肝、人正常胎肝、人正常 BM、141C1 重复、p8 BM、89 周 BM（5K panel）、
  NC/PHZ 脾、E13.5 FL（5K）。
- scRNA 系 5 个：E14.5 胎肝、小鼠骨髓/脾、人骨髓 MDSEB2、人骨髓 scRNA。
- Xenium 脚本模式（实测 Human normal bone marrow Xenium analysis.R 头部）：
  - `checkGiottoEnvironment()` 检查 Giotto 环境。
  - `createGiottoInstructions(save_dir, save_plot=TRUE, show_plot=FALSE, return_plot=FALSE)`——
    图直接落盘不进编辑器（README 自述"省时间"）。
  - 输入为 Xenium 原生文件：experiment.xenium、morphology_focus.ome.tif、morphology_mip.ome.tif、
    cell_boundaries.csv.gz、nucleus_boundaries.csv.gz（亚细胞文件）。
  - 结果目录硬编码 `~/Desktop/Xenium/Giotto analysis/...`。
- README：R 4.3.3/4.3.2、RStudio 版本、Giotto 4.0.5/4.0.2、Seurat 5.0.3、
  机器规格（Apple M2 Ultra 192GB / M1 8GB）+ GEO 取数提示 + 逐脚本导入 RStudio 分步运行。
