# ITERATION_LOG — 范式级决策与迭代记录

> 记录：结构性决策、分类修订、模式升级、pipeline 版本事件。新条目加在最上面。

## 名称变更对照表（2026-09-27 去黑话改写）

| 旧名（此前记录中的写法） | 现名 |
|---|---|
| 范式登记册 | 做法登记册 |
| 范式卡 / PATTERN 卡 | 做法卡（PATTERN-XXX 编号不变） |
| 候选流程池 | 候选流程对比 |
| 整合pipeline | 整合流程 |
| 基础范式主干（docs/01） | 基础流程 |
| PATTERN-028_locked冻结命名纪律 | PATTERN-028_定稿命名规则 |
| PATTERN-045_管线冻结对象逐图notebook复现契约 | PATTERN-045_结果存盘后逐图出图的流程 |
| PATTERN-050_图号反查md操作手册双轨组织 | PATTERN-050_图号反查md操作手册并行组织 |

以下历史条目中出现的旧名均指上表现名。

## 2026-09-27（晚）· Bizard 模板源接入 + 站点评论与周检

- **Bizard 登记**：生态与官方资源.md 新增"绘图模板库"小节（FigureYa/Bizard/R Graph Gallery 并列；Bizard=Openbiox 社区库，五段式教程，2026-09-27 Gallery 全量索引实查）。
- **10 卡补 R 候选**：V-01/02/12/13/14/15/16/20/21/22 的模板节改"模板候选（FigureYa / Bizard）"；V-22 最富（DIY GSEA/GO×3/KEGG）；V-15/20/21 无匹配如实标注；V-17 顺手加 CellChatCirclePlot（专属圈图优于通用 circos）。范围外 11 卡未动。
- **giscus**：repo Discussions 已启用（gh PATCH）；**2026 版 material 主题系统重写致 custom_dir 失效**（Unrecognised configuration name），改客户端 JS 注入 `docs/assets/giscus.js`（document$ 订阅兼容 instant navigation）——经验：uvx 解析到的 mkdocs 是 1.6.1 但 material 2026 版不再走 override partial。
- **周检**：`.github/workflows/weekly-check.yml`（周一 03:00 UTC + 手动）+ `scripts/url_check.py`（标准库；403/429 记疑似反爬不计失败——沿用 v2 核验经验）。**脚本首版有元组索引错位 bug（r[2] 取到 URL）本地试跑即抓出修复**；本地+Actions 双端实测 ok=72/0 失败；`weekly-check` label 预创建；README 加 badge。
- **挂起**：giscus App 若未安装到仓库，页面评论区将不出现——首次验证需用户在 https://github.com/apps/giscus 安装到 xenium-code-atlas。

## 2026-09-27 · 绘图呈现层建成（横向层）

- **决策**：绘图呈现不设 A10 串行模块，建为横向呈现层 `02_工作流开发/绘图呈现/`（与做法登记册同构）——绘图消费所有模块产出，排在 A9 之后语义不对。
- **三层结构**：数据层 `01_资料库/图形类型书目.csv`（91 篇 269 条"绘图借鉴"派生，`scripts/build_figure_catalog.py` 唯一事实源；归一化规则=内容类先于形式类，32 条人工 override 均注明依据）→ 卡片层 V-01~V-22（按论证链 5 组：数据可信/构成身份/空间结构/通讯动态/叙事整合）→ 手册层 `docs/07-绘图与呈现.md`（论证链 mermaid 地图+速查表）。
- **口径说明**：书目归一化分布与同日探查报告存在细节差异（探查为"首个面板"口径、脚本为关键词有序规则），以脚本输出为准；探查报告仅作设计依据。
- **FigureYa 接入**：11/22 图族有候选模板 ID（检索自 319 目录模板）；Source Pack 未配置（0 可 materialize），卡内标注"待检索+建议 query"或"需配置后落地"；用图时按铁律 13 复制到 scripts/ 微调并注明来源。
- **关键发现**：细胞通讯图 20/269 排第三但 72 仓无专门方法仓（呼应一期"A4 缺位"结论）——图热码冷，二期迭代机会。
- **挂钩**：高级模块 README 增"横向层"映射表；整合流程 组装原则增第 5 条（输出层=绘图呈现层）；迭代入库 SOP 增"新图形类型"节；mkdocs nav 学习手册 tab 增 07 章、工作流开发 tab 增绘图呈现。
- **挂起**：卡片撰写 agent 三次环境超时（Captcha），V-10~V-22 由主会话直接撰写、批次 A（V-01~V-09）为 agent 撰写——两批风格一致性待终审抽查；FigureYa 待检索图族（V-01/02/12/13/14/15/16/20/21/22）补检；V-20 参考素材【待补充：自建 SVG 素材库】。

## 2026-09-12 · 决策剧场审查 P2 缺陷修复（四项 + 一行文档）

- **QC tier 语义单测落地**：`scripts/test_qc_tiers.py`（零依赖纯断言, venv 无 pytest 不新增依赖）——40×30 合成矩阵四细胞群, 三档期望全手算字面量锁死; P-001 回归用例（高深度低广度基因必须被 min_cells 滤掉、高广度低深度必须存活、min_counts=25 边界含等号）共 9 项断言。配套 DRY：run_tier/run_control 重复的 filter 块提取为 `apply_qc_filters()`（docstring 写明四参数语义）。有趣记录：三轮失败全是测试作者手算期望值错（B 群抬广度/C 群双段表达/基因广度塌缩未重算）, 实现每次都对——恰证此类测试价值在锁语义而非验直觉。
- **调色板统一**：python `CLUSTER_PALETTE` 索引 20 重复色 `#31A354` → `#17BECF`; SPA `PAL` 由 14 色扩为与 Python 逐色一致的 24 色（修复 BRCA res=1.0 十五簇在播放器中撞色+图例省略）; 图例逐类阈值 14→16; coords 新增 `anno_colors` 下发, 播放器 anno 模式与 anno PNG 同色。已出货 PNG 不重算（最大 15 簇仅用索引 0-14, 视觉零变化）。
- **spread 修复收尾**：mountPlayer 内 `mm()` 大数组安全 min/max 提升为公共辅助, gene 上色分支残留的 `Math.max(...gv)` 改用之（3 万+元素 spread 爆栈风险清除）。
- **结算表改答语义**：`chooseOption` 按 step 替换而非追加, 改答在结算镜像表标注"（改选，原选：X）", 一节点一行。
- **文档**：指南 §七补 `--strict` 语义说明与单测命令; AGENT.md §9 审查项扩为"validate 全绿 + 单测通过"; HANDOFF 复跑段同步。

## 2026-09-05 · 决策剧场模拟器一期建成（二期模块 1）

- **新增互动模块**：`docs/simulator/`（单文件 SPA 引擎 + 液态玻璃设计系统，vanilla JS 零依赖零构建链），mkdocs nav 新增顶级 tab「决策剧场」，配套 `docs/06-决策剧场指南.md`（玩法 + 教学地图 + 诚实性三级说明）。
- **游戏设计**：分支收敛制（每步 ≤3 选项全部收敛主干，路径差异=参数+图+文案）；主流程七步=手册 §1–§7 的可玩化；坑事件系统 P-001~P-006 全部提炼自 27 份精读「坑与限制」实读发现，双证据链（精读笔记 + 被审仓 文件:行号 GitHub blob 锚点，行号已逐一复核）。
- **诚实性三级**：T1 真实重算（HCC 162,628 细胞×474 基因全量三档 QC×三分辨率 + 健康肝 zarr 对照 239,271 细胞；BRCA 10x 官方 Rep1 167,780 细胞×313 基因；CRC 10x Addon FFPE 480 基因）/ T2 文献结论参数化重绘 / T3 示意（右下角「模拟示意」角标）；每图强制三行式标注（来源/性质/参考文献）登记 manifest.json，`scripts/validate_scenario.py` 五类校验守门。版权红线：文献图一律重绘不搬运。
- **反编造执行记录**：UC/CROHN 论文定量数值无可溯源来源 → 拒绝伪造比例图，降级为路线示意（T3）并在剧本内诚实声明；HCC marker 集逐一对照 panel 实际 474 基因清单重写（ALB/KRT19 不在 panel，改用 CYP2A7/CYP3A4/HAMP 等功能基因组）；ZXM onboard UMAP 仅覆盖 1,189,658/1,196,822 细胞 → 按 Barcode 对齐而非位置对齐。
- **CRC 数据核实（计划期→执行期）**：Nat Genet 2025（10.1038/s41588-025-02193-3）配套主线为 Visium HD（=库内 LIT-026），无专设 Xenium 5K CRC 集 → 采用 10x 官方 Xenium_V1_Human_Colorectal_Cancer_Addon_FFPE（cf.10xgenomics.com 直链）保住 T1；三级降级链记录于指南 §5。
- **ZXM 本地专属关**：预计算产物入 `docs/simulator/assets/ZXM_local/`（.gitignore 排除，课题数据不出本机），公开站入口探测 404 即显示「本地版可用」；教学主线=大样本 onboard 复用（官方线 large_sample_reuse 同构）。
- **预计算工程**：`scripts/precompute_simulator.py`（--dataset/--step 参数化，tier 缓存，QC 标准档=PATTERN-047 统一核心 50/10/1/10）、`precompute_simulator_zxm.py`（onboard 复用+3 万细胞抽样）、`precompute_lit_redraw.py`（T1-lite 示意）；中间缓存 `F:\xenium数据\ov工作流测试\simulator_precompute\`（不入 git）；scanpy filter_cells 一次只收一个阈值参数、sys.unraisablehook 静音第三方析构刷屏两坑已记入实现。
- **红线事故与修复（同日）**：首次 `mkdocs gh-deploy` 把 gitignore 掉的 ZXM_local 资产带上了 gh-pages（gh-deploy 从磁盘构建，gitignore 管不住部署）→ 三层修复：mkdocs.yml `exclude_docs` 构建层排除 + `scripts/serve_simulator_local.py`（本地预览才注入 ZXM 资产）+ 孤儿提交强推 gh-pages 清除历史泄露；线上复验 ZXM_local=404。
- **待办池新增**：见底部。

## 2026-09-04 · 一期建成（V0）

- **建库**：72 仓全量浅克隆锁定 SHA（1 仓 IN-DEPTH 因上游尾随空格目录名部分 checkout，sparse-checkout 绕过，档案卡已注）。
- **定级**：S 27 / A 34 / B 11。
- **分类修订**（含 agent 复核改判，均有档案卡佐证）：
  - SPATCH P3→P0（亚细胞平台基准为主旨）
  - sharp P8→P0（SCING WDL/Cromwell 管线）
  - sc_MTOP P8→P7（HoVer-Net WSI 分割+形态特征）
  - CoCo-ST P8→P3、SPACE P8→P3、Spatial_PF P6→P3（均生态位/域方法）
  - cadasSTre P8→P0（测序式 ST 预处理评测）、ATX_epigenomics P2→P0（平台管线）
  - tnbc-chemo、Kidney-Map 升 S（手册双轨模式 / niche 全家桶）
- **License 更正**：snp2cell=BSD-3；ImagePseudo=UT Southwestern 学术专用。
- **核心结论**：共性骨架收敛（读取→QC→归一化→降维→聚类→注释→绘图/导出）；工程质量均值 8.3/14、工业级仅 11%——二期"文献给模块、我们造外壳"。
- **待人工核验**（分类分析报告 §9）：QuKunLab LIT 映射、ATX 映射、PHM 去留、10Xmapping 归类。
- **二期入口**：整合流程 V0 占位 → 按报告 §8 五层骨架组装 V1.0 → 用户终审。

## 待办池

- [ ] 二期：场景路线（A9/TME、纤维化、UC 课题专线）成文
- [ ] 二期：整合流程 V1.0 组装 + V1 肝癌 smoke
- [ ] 三期：A1–A9 模块逐个实操测试
- [ ] 观察项：Xenium Ranger 4.0.1 大细胞分割对用户数据的收益评估
- [ ] 观察项：ov `cellseg()` 更名迁移 + RAPIDS 补丁重验（升级 OV 时）
