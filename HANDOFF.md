# HANDOFF — 交接文档

> 交接时间：2026-09-05（一期收尾）。交接对象：用户（zerogue11）或后续任何 agent。开工前必读 `AGENT.md`。

## 项目当前状态（一期完成）

| 交付物 | 位置 | 状态 |
|---|---|---|
| 72 仓本地镜像（浅克隆，SHA 锁定） | `03_开源项目/`（约 5.8GB，不入 git） | ✅ 71 完整 + 1 部分 checkout（IN-DEPTH，上游尾随空格目录名） |
| 代码资源主表（72 行台账） | `01_资料库/代码资源主表.csv` | ✅ 分类/精选级/SHA/license 全 |
| 档案卡 72 张 | `01_资料库/档案卡/` | ✅ |
| 精读笔记 27 份 + 精读汇总 | `01_资料库/精读笔记/`、`精读汇总.csv` | ✅ 含 7 维工程审计 |
| 范式登记册 46 卡 | `02_工作流开发/范式登记册/` | ✅ PATTERN-001~053（有号段空洞，宁缺毋滥） |
| 分类分析报告（一期核心结论） | `01_资料库/分类分析报告_一期.md` | ✅ |
| 中文学习手册站 | `docs/` + `mkdocs.yml` → GitHub Pages | ✅ 已发布 |
| GitHub 公开仓 | `zerogue11/xenium-code-atlas` | ✅ main + gh-pages |
| 迭代机制 | `01_资料库/迭代入库SOP.md`、根 `ITERATION_LOG.md` | ✅ |
| 决策剧场模拟器（二期模块 1） | `docs/simulator/`、`docs/06-决策剧场指南.md`、`scripts/precompute_*.py`、`scripts/validate_scenario.py` | ✅ 五场景+ZXM 本地关；T1 预计算（HCC/BRCA/CRC）+ T1-lite（UC/CROHN）；ZXM_local 不入 git |
| 二/三期路线 | `docs/04-实操测试计划.md`、整合 pipeline 占位 V0 | 待执行 |

## 怎么复跑（自助）

```bash
# 环境
#  主 Python: C:/xenium_envs/xenium-cn-py311/Scripts/python.exe（venv）
#  文档工具: uvx --from mkdocs-material mkdocs（uv 隔离，不落全局）
#  gh CLI: 已登录 zerogue11

# 1. 资源派生（上游种子只读：F:\我的科研\xenium-knowledge-tree\01_资料库）
C:/xenium_envs/xenium-cn-py311/Scripts/python.exe scripts/build_master_table.py

# 2. 全量浅克隆（断点续跑；直连优先，失败退全局代理/镜像；全局代理未开时脚本已自动绕过）
C:/xenium_envs/xenium-cn-py311/Scripts/python.exe scripts/clone_all.py --workers 6

# 3. 体检（体积/语言/license/README摘要 → 仓库体检表.csv，回填主表）
C:/xenium_envs/xenium-cn-py311/Scripts/python.exe scripts/health_check.py

# 4. 站点（fresh clone 后先重建 docs 联接）
cmd /c scripts\setup_docs_links.cmd
uvx --from mkdocs-material mkdocs serve        # 本地预览
uvx --from mkdocs-material mkdocs gh-deploy    # 发布

# 5. 决策剧场资产与校验（详情见 docs/06-决策剧场指南.md §七）
#  预计算: python scripts/precompute_simulator.py --dataset hcc|brca|crc
#          python scripts/precompute_lit_redraw.py        (UC/CROHN 示意)
#          python scripts/precompute_simulator_zxm.py     (本地关, 课题数据)
#  校验:   python scripts/validate_scenario.py --strict
```

## 关键决策记录（为什么是这样）

1. **公开仓不含第三方代码**：33/72 无 LICENSE + 4 个限制性许可（见分类分析报告 §1），只推自写知识层 + 链接+SHA。
2. **基础流程不定死**：候选池并列（官方线/OV 线/文献仓模式），二期蒸馏共性骨架后组装整合 pipeline V1.0，用户终审冻结。
3. **工程质量结论**：均值 8.3/14、工业级 11% —— 文献仓当"模块与路线参考"，工程外壳自研（已给五层骨架草案，报告 §8）。
4. **克隆代理坑**：本机 git 全局配置 127.0.0.1:7890 代理常未开——克隆脚本已内置绕过（`-c http.proxy=`），不动全局配置。

## 待人工核验（反编造留痕）

1. QuKunLab/SpatialBenchmarking ↔ LIT-088 映射存疑（主表已注）。
2. atlasxomics/ATX_epigenomics ↔ LIT-039 映射存疑（已改 P0 并注）。
3. natsuhiko/PHM 非空间仓，终审去留。
4. ding-lab/10Xmapping 归类矛盾（P6 vs 变异映射功能）。

## 下一步入口

- 二期：按 `01_资料库/分类分析报告_一期.md` §8 五层骨架组装整合 pipeline V1.0；场景路线（UC 专线第一参照 = UCSF colitis 仓）。
- 三期：`docs/04-实操测试计划.md`（T0 readiness → T1 基础流程 smoke → T2 模块 smoke → T3 ZXM 递进）。
