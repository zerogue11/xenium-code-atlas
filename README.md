# xenium-code-atlas — Xenium 文献公开代码整合提炼库

> 从 91 篇 Xenium/空间转录组文献的**公开代码资源**中蒸馏可复现、可迭代的教科书级分析范式。
> 种子数据：v2 知识工程资源核验表（634 条资源全量联网核验，2026-09-04 冻结），其中代码类 114 条 → **72 个 GitHub 仓库**（全部可访问）+ 17 条 Zenodo 归档 + 21 个工具网页。

## 这是什么 / What is this

**中文**：本项目把空间转录组（Xenium 为主）文献中公开的分析代码系统化归档：全量浅克隆锁定版本 → 逐仓档案卡 → 精选精读（含工程质量审计）→ 归纳共性骨架与场景路线 → 组装可迭代的整合式 pipeline。目标是"学习复现 → 内化为自己的范式 → 持续迭代"，避免重复造轮子。

**English (TL;DR)**: A curated, versioned atlas of public analysis code from 91 Xenium/spatial-omics papers (72 GitHub repos, all verified accessible), with per-repo dossier cards, engineering-quality audits, distilled common workflow patterns, and iteratively assembled reference pipelines. Third-party code is **mirrored locally only** — this public repo contains our own written knowledge layer, linking upstream repos by URL + pinned commit.

## 三阶段路线

| 阶段 | 内容 | 状态 |
|---|---|---|
| 一期 | 归档 72 仓 + 分类 + 精读分析 + 本知识仓上线 | 进行中 |
| 二期 | 范式蒸馏：共性骨架 / 场景路线 / 整合 pipeline V1.0（终审冻结） | 未开始 |
| 三期 | 实操测试：readiness→smoke→V1 肝癌回归→ZXM 递进 | 未开始 |

## 目录导航

| 路径 | 内容 |
|---|---|
| [AGENT.md](AGENT.md) | 项目宪法（红线、分类体系、工程审计维度、版本纪律） |
| `01_资料库/` | 代码资源主表、仓库体检表、档案卡（72 张）、分类分析报告 |
| `02_工作流开发/` | 候选流程池（官方线/OV线）、范式登记册、场景路线、整合 pipeline |
| `docs/` | 中文学习手册（mkdocs 站点源） |
| `scripts/` | 资源派生 / 克隆 / 体检脚本（自写） |
| `03_开源项目/` | 72 仓本地镜像（**不入公开仓**，.gitignore 排除） |

## 纪律声明

- 第三方代码只做本地学习镜像，公开仓中以「原仓库链接 + 锁定 commit SHA」引用，规避许可证风险。
- 所有结论以实测为准，查不到的标【待补充】；禁止编造（学术诚信底线）。
- 上游种子库与既有工作区只读；新结果不覆盖旧版本。
