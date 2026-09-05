# ITERATION_LOG — 范式级决策与迭代记录

> 记录：结构性决策、分类修订、模式升级、pipeline 版本事件。新条目加在最上面。

## 2026-09-05 · 决策剧场模拟器一期建成（二期模块 1）

- **新增互动模块**：`docs/simulator/`（单文件 SPA 引擎 + 液态玻璃设计系统，vanilla JS 零依赖零构建链），mkdocs nav 新增顶级 tab「决策剧场」，配套 `docs/06-决策剧场指南.md`（玩法 + 教学地图 + 诚实性三级说明）。
- **游戏设计**：分支收敛制（每步 ≤3 选项全部收敛主干，路径差异=参数+图+文案）；主干七步=手册 §1–§7 的可玩化；坑事件系统 P-001~P-006 全部提炼自 27 份精读「坑与限制」实读发现，双证据链（精读笔记 + 被审仓 文件:行号 GitHub blob 锚点，行号已逐一复核）。
- **诚实性三级**：T1 真实重算（HCC 162,628 细胞×474 基因全量三档 QC×三分辨率 + 健康肝 zarr 对照 239,271 细胞；BRCA 10x 官方 Rep1 167,780 细胞×313 基因；CRC 10x Addon FFPE 480 基因）/ T2 文献结论参数化重绘 / T3 示意（右下角「模拟示意」角标）；每图强制三行式标注（来源/性质/参考文献）登记 manifest.json，`scripts/validate_scenario.py` 五类校验守门。版权红线：文献图一律重绘不搬运。
- **反编造执行记录**：UC/CROHN 论文定量数值无可溯源来源 → 拒绝伪造比例图，降级为路线示意（T3）并在剧本内诚实声明；HCC marker 集逐一对照 panel 实际 474 基因清单重写（ALB/KRT19 不在 panel，改用 CYP2A7/CYP3A4/HAMP 等功能基因组）；ZXM onboard UMAP 仅覆盖 1,189,658/1,196,822 细胞 → 按 Barcode 对齐而非位置对齐。
- **CRC 数据核实（计划期→执行期）**：Nat Genet 2025（10.1038/s41588-025-02193-3）配套主线为 Visium HD（=库内 LIT-026），无专设 Xenium 5K CRC 集 → 采用 10x 官方 Xenium_V1_Human_Colorectal_Cancer_Addon_FFPE（cf.10xgenomics.com 直链）保住 T1；三级降级链记录于指南 §5。
- **ZXM 本地专属关**：预计算产物入 `docs/simulator/assets/ZXM_local/`（.gitignore 排除，课题数据不出本机），公开站入口探测 404 即显示「本地版可用」；教学主线=大样本 onboard 复用（官方线 large_sample_reuse 同构）。
- **预计算工程**：`scripts/precompute_simulator.py`（--dataset/--step 参数化，tier 缓存，QC 标准档=PATTERN-047 统一核心 50/10/1/10）、`precompute_simulator_zxm.py`（onboard 复用+3 万细胞抽样）、`precompute_lit_redraw.py`（T1-lite 示意）；中间缓存 `F:\xenium数据\ov工作流测试\simulator_precompute\`（不入 git）；scanpy filter_cells 一次只收一个阈值参数、sys.unraisablehook 静音第三方析构刷屏两坑已记入实现。
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
- **二期入口**：整合 pipeline V0 占位 → 按报告 §8 五层骨架组装 V1.0 → 用户终审。

## 待办池

- [ ] 二期：场景路线（A9/TME、纤维化、UC 课题专线）成文
- [ ] 二期：整合 pipeline V1.0 组装 + V1 肝癌 smoke
- [ ] 三期：A1–A9 模块逐个实操测试
- [ ] 观察项：Xenium Ranger 4.0.1 大细胞分割对用户数据的收益评估
- [ ] 观察项：ov `cellseg()` 更名迁移 + RAPIDS 补丁重验（升级 OV 时）
