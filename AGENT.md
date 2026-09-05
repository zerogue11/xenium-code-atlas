# AGENT.md — xenium 文献代码库整理提炼计划（项目宪法）

> 任何 agent 在本目录工作前必读。创建：2026-09-04。上游种子：`F:\我的科研\xenium-knowledge-tree`（v2 知识工程，2026-09-04 冻结）。

## 1. 项目定位与三阶段

- **一期（当前）**：把 91 篇文献核验过的 114 条代码资源（去重后 72 个 GitHub 仓库 + Zenodo 归档 + 工具网页）克隆归档、分类、精读分析，产出可迭代的知识仓（GitHub 公开仓）。
- **二期**：范式蒸馏与整合——不选"唯一胜出 pipeline"，而是：归纳共性骨架、按场景分组路线、组装模块化整合 pipeline（附来源映射），用户终审后冻结。
- **三期**：实操测试，按 `F:\xenium数据\ov工作流测试\AGENT.md` 纪律：readiness→smoke（V1 肝癌公开数据回归）→递进扩样（ZXM）。

## 2. 红线（违反即停）

1. **第三方代码绝不推送公开仓**：`03_开源项目/` 下的一切是本地学习镜像，已被 .gitignore 排除。公开仓只含自写内容（主表、档案卡、报告、手册、自写脚本）。档案卡必须注明 license 状态；无 LICENSE 的仓库标注"仅可学习、不可转载"。
2. **既有资产只读**：`F:\我的科研\xenium-knowledge-tree`、`F:\xenium数据` 下各工作区（ov工作流测试、xenium官方教程及测试、ZXM、资源、文献库）一律不修改。引用其成果时注明来源路径与版本。
3. **目录命名**：`03_开源项目/` 下一律 ASCII `<owner>__<repo>`（保留原大小写）。文档目录沿用全盘 00–05 编号惯例。
4. **编码纪律**：所有自写脚本开头 `sys.stdout/stderr.reconfigure(encoding="utf-8")`；Python 用 `C:/xenium_envs/xenium-cn-py311/python.exe`（PATH 上的 python 是 Microsoft Store 别名，禁用）。
5. **反编造**：星标、日期、license、语言、功能描述均以实测（克隆体检/README/代码）为准；查不到写【待补充】，禁止推测填充。

## 3. 分类体系

`E` 生态基础设施｜`F` 官方资源｜`P0` 流程基准与质控｜`P1` 分割与重分割｜`P2` 注释与图谱｜`P3` 空间域·生态位｜`P4` 细胞通讯｜`P5` 亚细胞·转录本定位｜`P6` 空间统计·配准·3D｜`P7` 图像组学·多模态｜`P8` 疾病应用范式｜`Z` Zenodo 归档代码。

判定规则：按仓库**最高频用途**单选主分类；多用途时其余用途写入档案卡"次要用途"。详见 `01_资料库/分类体系.md`。

## 4. 精选级

- **S**：精读仓（~25 个）——代码走读 + 工程审计 + 范式登记。
- **A**：建档仓——README 级档案卡。
- **B**：登记仓——仅链接与元数据。

## 5. 版本与迭代纪律

- 整合 pipeline 自 **V1.0** 起版本化；实质变更（新增/替换模块、参数策略变化）必须升版本号并写 CHANGELOG，禁止静默改（全盘规则 20）。
- 新文献/新仓入库走 `01_资料库/迭代入库SOP.md`；范式级决策记入根目录 `ITERATION_LOG.md`。
- 候选流程**并列登记**于 `02_工作流开发/候选流程池/`，不预设唯一主线；主线由用户终审后冻结。

## 6. 工程审计维度（S 级精读必填）

每项 0–2 分（0=缺失，1=部分，2=到位），**必须附 文件:行号 证据**：
①SOLID·职责单一 ②命名规范 ③安全性（路径/凭据） ④最简化（无冗余） ⑤逻辑健壮性（错误处理/断言） ⑥可复现性（seed/版本/metadata） ⑦验证纪律（计划→实现→验证的流程痕迹）。

## 7. 环境与工具

- Python：`C:/xenium_envs/xenium-cn-py311/Scripts/python.exe`（venv 布局，python.exe 在 Scripts/ 下）。
- gh 已登录 **zerogue11**（repo 权限）；git 协议 https；GitHub 直连正常。
- 克隆失败备用镜像：`https://ghfast.top/https://github.com/...` 前缀重试。
- mkdocs 站点构建用 `uvx --from mkdocs-material mkdocs` 隔离运行，不污染分析环境。

## 8. 产出清单（一期）

- `01_资料库/`：代码资源主表.csv、代码资源附属表.csv、仓库体检表.csv、文献速查表.csv、档案卡/×72、分类分析报告_一期.md
- `02_工作流开发/`：候选流程池登记卡、范式登记册、场景路线（占位）、整合pipeline（占位 V0）
- `scripts/`：build_master_table.py、clone_all.py、health_check.py
- 根：AGENT.md、README.md、ITERATION_LOG.md、HANDOFF.md、mkdocs.yml、index.md、docs/

## 8b. 产出清单（二期模块 1 · 决策剧场）

- `docs/simulator/`：index.html（单文件 SPA 引擎）、data/（schema.json、events.json、scenarios/×5）、assets/（HCC/BRCA/CRC T1 + UC/CROHN 示意 + coords）
- `docs/06-决策剧场指南.md` + mkdocs nav「决策剧场」tab
- `scripts/`：precompute_simulator.py、precompute_simulator_zxm.py（本地关）、precompute_lit_redraw.py、validate_scenario.py
- 红线：`assets/ZXM_local/` 课题数据不入公开仓；每图三行式标注（来源/性质/参考文献）；文献图一律重绘不搬运

## 9. 收尾审查清单

- [ ] 主表 72 仓与实际克隆数一致，SHA 全锁定
- [ ] 档案卡 72 张齐全，无编造字段，【待补充】项已列明
- [ ] S 级精读笔记含工程审计评分与 文件:行号 证据
- [ ] 范式登记册每卡有来源仓与搬运条件
- [ ] `git status` / 推送内容不含任何 `03_开源项目` 内容
- [ ] GitHub 推送前 `git log --stat` 抽查确认无第三方代码
- [ ] 决策剧场：`validate_scenario.py --strict` 全绿；assets/ZXM_local 未入 git；每张图三行式标注齐全
