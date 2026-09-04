# `KChen-lab/ST_Comparison`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\KChen-lab__ST_Comparison`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-089：《基于FFPE肿瘤样本的成像式单细胞分辨率空间转录组平台对比》（Nat Commun 2025） |
| 精选级 | S |
| 主分类 | P0 流程基准与质控（复核确认，与初判一致） |
| 次要用途 | CosMx/MERFISH/Xenium 三平台的 Seurat 读取与 QC 阈值参照 |
| 一句话功能 | 论文伴随 R 代码：对肺腺癌（ICON）与胸膜间皮瘤（MESO）FFPE TMA 连续切片，用 Seurat 分别处理 CosMx、MERFISH、Xenium（uni/multi-modal）数据，并与 bulk RNA/多重 IF/GeoMx/H&E 对照做平台性能与人工表型对比，附逐图复现脚本与细胞类型注释数据 |
| License | MIT（主表值） |
| 语言与规模 | R；.R 脚本 28 个；体积 4.6 MB（含注释 .rds）；【主表标"非代码"，实测为 R 代码——主表该字段待修正】 |
| 运行入口 | R 脚本：Seurat/ 下 6 个处理脚本（平台×样本），Figures/ 下逐图脚本；无环境文件 |
| 复现难度 | 高 — 原始数据在 GEO（GSE299786/GSE299886/GSE300007）需自行下载，脚本内数据路径为占位符需手改，且无 renv/yml 锁版本 |
| 与范式的关系 | P0 平台对比范式的实测样例：LoadNanostring 读 CosMx、nCount>30 过滤、"面积<全体几何均值×5"去大细胞等 QC 细节可直接借鉴；候选池 |
| 坑提示 | ① 脚本硬编码占位路径（如 `data.dir = "/path to Cosmx data/"`）需逐个替换；② 无环境/版本锁，依赖全靠脚本内 library() 推断（dplyr/ggplot2/patchwork/Seurat）；③ 图脚本间无统一 pipeline 入口，按图号手工顺序执行 |
| 锁定 SHA | 【待补充：主表"锁定SHA"列空】；本地克隆 HEAD 实测 `e3a3256875` |

## 结构速览

- `Seurat/`：6 个脚本——CosMx_ICON.R、CosMx_MESO.R、MERFISH_ICON.R、MERFISH_MESO.R、Xenium_ICON.R、Xenium_MESO.R（每平台×每样本独立建 Seurat 对象并 QC）
- `Figures/`：15+ 个逐图复现脚本（Figure_2a.R … Figure_7b.R、Supp.Fig_11a/b.R）
- `Annotations/`：8 个细胞类型注释 .rds（跨平台共享）+ READ.me
- README：含摘要、GEO 登录号与发表链接，无运行说明

## README/代码实读要点

- 研究设计：同一 TMA 连续 5µm 切片跑三平台，以 bulk RNA/多重 IF/GeoMx/H&E 为参照
- CosMx_ICON.R 开头即建对象流程：LoadNanostring(data.dir=…, fov="Icon1", assay="Nanostring")→nCount_Nanostring>30→Area < 5×几何均值
- 注释 .rds 按平台/样本配对命名（如 ICON2_Xenium_UM/MM_Annotations 区分 Xenium 单模/多模）
- 图脚本按期刊图版号组织，即"一图一脚本"的论文伴随码典型形态

## 抽读实录

- 读 README 全文（含摘要与 GEO 登录号）；抽读 Seurat/CosMx_ICON.R 开头 20 行（对象构建与两道 QC 过滤）。

## 复用建议

- 不复跑全流程（数据+路径成本高），只取三平台读取与过滤参数做自家 Xenium/CosMx QC 阈值参照；注释 .rds 可作lung TME 注释参考【待验证可行性】。
