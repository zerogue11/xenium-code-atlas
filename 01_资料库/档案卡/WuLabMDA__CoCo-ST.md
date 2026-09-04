# `WuLabMDA/CoCo-ST`（档案卡）

> 由 agent 依据本地克隆实测撰写；不确定处一律【待补充】；禁止编造星标/日期/功能。

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-087：《CoCo-ST检测全局与局部生物学结构》（Aminu et al., Nat Cell Biol 2025, doi:10.1038/s41556-025-01781-z） |
| 精选级 | B |
| 主分类 | P3（复核 P8→P3：核心是对比学习识别空间域/空间结构，命中 P3"空间域·生态位"定义；非基准非 QC 故不归 P0） |
| 次要用途 | P8 自带多平台应用宣称（Visium/Visium HD/Xenium） |
| 一句话功能 | CoCo-ST 方法 R 包：以前景/背景两数据集的归一化图拉普拉斯做对比成分分析（contrastive component analysis），分离肿瘤 vs 正常间的高方差与低方差空间结构、识别空间域 |
| License | MIT |
| 语言与规模 | R×7（R/CoCoST.R 包函数 + Codes/ 6 脚本），4.7 MB |
| 运行入口 | R 包：`devtools::install_github("WuLabMDA/CoCo-ST")`；教程 `Tutorials/visium_spot.html`（在线版 wulabmda.github.io/CoCo-ST）；入口示例 `Codes/main.R`；无 env/lock 文件【待补充依赖版本】 |
| 复现难度 | 低偏中：包安装 + 单教程可跑通；但需自备前景/背景亲和矩阵（W1/W2，示例用 kernlab laplacedot 核矩阵），核矩阵全量构建的超大规模内存开销实测【待补充】 |
| 与范式的关系 | "对比学习找共享 vs 独有空间结构"与常规 niche 方法（CellCharter/Banksy 系）互补，思路可借鉴；仅 1 个 Visium spot 教程、Xenium 教程缺位，进入候选池前需自测 |
| 坑提示 | README 宣称支持 Xenium 与百万 spot 级可扩展，但仓内无 Xenium 教程与基准数据佐证；亲和矩阵构建责任在用户侧；包处于持续开发期（README 自述） |
| 锁定 SHA | 7c65930fb2558573a89267c6db968df72ac53bfd |

## 结构速览

- `R/CoCoST.R`：核心函数（roxygen 文档完整：输入 data1/W1/data2/W2 + 对比参数 para，输出前/背景对比成分与投影矩阵）。
- `Codes/`：main.R、mainAnterior.R、mainPosterior.R（应用入口）、CoCoST_multisample_integration.R / _harmony.R（跨样本整合）、helperFunctions.R。
- `Tutorials/visium_spot.html`：唯一官方教程（Visium spot 空间域识别）。
- 标准 R 包结构：DESCRIPTION、NAMESPACE、man/CoCoST.Rd、CoCoST.Rproj。

## 实读要点

- R/CoCoST.R roxygen 文档实读：CoCoST 通过比较两个数据集（foreground/background）的归一化图拉普拉斯做对比成分分析；参数 para=对比减法权重（默认 0.2）、Dim=提取成分数（默认 2）；返回 projMatrix、fgComponents、bgComponents；示例代码用 kernlab `laplacedot(sigma=0.5)` + `kernelMatrix` 构造 W1/W2，即亲和矩阵需用户自行定义核函数。
- 语言复核结论：确认为 R 包（初判担心是 Python 方法的疑虑排除）；README 亦给 devtools/remotes 两种安装。
- README 实读：宣称多尺度（亚细胞/细胞/spot）、跨样本跨平台（Visium、Visium HD、Xenium）、百万 spot 级可扩展；仓内佐证仅 visium_spot 教程一个，Xenium 场景无教程无示例数据。

## 复现路径（怎么跑）

1. R 内 devtools::install_github("WuLabMDA/CoCo-ST")（示例依赖 kernlab，需一并安装）。
2. 跑 Tutorials/visium_spot.html 教程或 Codes/main.R：准备前景（如肿瘤）与背景（如正常）两数据矩阵 → 各自构建亲和矩阵 W1/W2 → CoCoST() 提取对比成分 → 空间映射识别域。
3. 跨样本整合参考 Codes/CoCoST_multisample_integration.R（含 harmony 变体）。

## 借鉴与风险

- 可移植点：前景/背景对比思路适合"肿瘤 vs 癌旁""病变 vs 正常"成对切片设计；para 减法权重提供一个可调的对比强度旋钮。
- 风险：全量核矩阵亲和构建在大样本（Xenium 60 万+细胞）下的可行性未验证；无 Xenium 教程；论文方法与仓实现的对应深度未精读。B 级维持，候选池观察。

