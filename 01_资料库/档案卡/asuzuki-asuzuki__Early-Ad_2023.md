# `asuzuki-asuzuki/Early-Ad_2023`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\asuzuki-asuzuki__Early-Ad_2023`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-001：肺腺癌逐步进展 WGS。英文原题（README 引用）"Whole-genome sequencing reveals the molecular implications of the stepwise progression of lung adenocarcinoma"（Haga Y et al., Nat Commun 2023;14:8375, doi 10.1038/s41467-023-43732-y；76 例 NSCLC 含 48 例极早期腺癌，Noguchi 分型） |
| 精选级 | A |
| 主分类 | 复核维持 P8（肺腺癌进展，WGS 为主 + 空间支线） |
| 次要用途 | P2 边缘：Spatial/ 子目录的 PAGE 去卷积 + VIS topic 模型 + Xenium/Visium 处理脚本 |
| 一句话功能 | 肺腺癌早期→晚期 WGS 多组学论文代码，三分支：DNA_methylation（甲基化分析）、Phasing（突变定相到单倍型并推断突变发生顺序）、Spatial（Visium/Xenium 的 Seurat 处理、PAGE 细胞型去卷积、VIS_topic 主题模型、CellChat、公共 scRNA 参考，含 Deconv_byScRNA/Deconv_byXenium 双路线） |
| License | MIT |
| 语言与规模 | Pythonx12/Rx9；0.2 MB |
| 运行入口 | 各子目录脚本独立运行；无 env/数据说明【待补充】；Spatial/ 有自己的 README |
| 复现难度 | 高 — WGS 甲基化/定相主线工具链重（fastq 级）；Spatial 分支数据入口未见说明；脚本为论文自用风格 |
| 与范式的关系 | 用户肺腺癌课题的相关件：Spatial/ 的 PAGE 去卷积（非负最小二乘系）与 VIS topic 是与 RCTD/cell2location 并列的另一组去卷积/主题模型选择；Noguchi 分型进展叙事可借鉴 |
| 坑提示 | ① 三分支中只有 Spatial/ 与空间转录组相关，其余为 WGS/甲基化；② 仓内未见 env 与数据链接【待补充】；③ Deconv_byXenium vs Deconv_byScRNA 的参考选择逻辑需读脚本确认 |
| 锁定 SHA | c87dcb80f5ccfa9f07de9362f1be4619743f3a61（主表） |

## 结构速览

- DNA_methylation/：甲基化分析脚本
- Phasing/：突变-单倍型定相与突变顺序推断
- Spatial/：Cancer_TypeMarker.txt、Cell_Type_Col.txt、public_scRNA_ana.R、Visium_Seurat.R、Xenium_Seurat.R、PAGE.R、VIS_topic.R、Deconv_byScRNA.R、Deconv_byXenium.R、CellChat.R、SUB_function.R + README
- LICENSE（MIT）+ 顶层 README（研究摘要+引用）

## README/代码实读要点

- 顶层 README 三行目录导览：methylation / Phasing（突变定相与顺序）/ Spatial（含 deconvolution scripts）
- Spatial/ 子 README + 脚本命名显示完整空间分析链：公共 scRNA 参考 → 平台处理 → PAGE/topic 去卷积 → CellChat

## 抽读实录

- 读 README 全文；ls Spatial/（11 个文件）；未深读脚本。

## 复用建议

- 肺腺癌课题下只关注 Spatial/：PAGE.R + VIS_topic.R 可作为去卷积/主题模型的多候选之一与 zoro-spatial 现有方案对照；WGS 分支与用户空间主线无关。
