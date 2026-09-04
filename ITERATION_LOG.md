# ITERATION_LOG — 范式级决策与迭代记录

> 记录：结构性决策、分类修订、模式升级、pipeline 版本事件。新条目加在最上面。

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
