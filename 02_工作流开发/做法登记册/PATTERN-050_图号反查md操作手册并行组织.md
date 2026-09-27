# PATTERN-050 · 图号反查 md 操作手册（手册与脚本两条线并行）
- 来源: navinlabcode/tnbc-chemo（LIT-046）相对/路径:行号 `analysis/README.md`（分析项、md 手册、相关图号的索引表）+ `analysis/ecotype.md`（四段式手册全文）
- 场景: 论文复现或大项目要交结果时：代码在 scripts/ 里"能跑"，但 reviewer/合作者需要"按论文图号找到做法、按步骤重跑、按预期图验收"。任何要用 md 操作手册管理的项目。
- 做法: 两条路线：`analysis/*.md` 手册层 + `analysis/scripts/<主题>/` 脚本层。总 README 用表维护分析项、手册链接、相关图号三者的对应；每份手册固定四段，按顺序为：**Related figures（图号）、Rscript file path（kbd+仓库相对链接）、Synopsis（编号执行步骤）、Output（预期图网格，直链 website_images）**。脚本侧配套的固定要求：step 编号（step0/2a/2b/2c）、`.winner` 后缀标定终版、helper 函数独立成文件。
  ```markdown
  ## Ecotype analysis
  **Related figures**: Fig. 5, Fig. S8
  **Rscript file path**:
  - `analysis/scripts/ecotype/ecotype_1_define.R`
  **Synopsis**
  1. Run `ecotype_0_create_feature_corr.R` 创建 metaprogram×TME 相关矩阵
  2. Run `ecotype_1_define.R` 定义生态型（分辨率扫描择优）
  **Output**（预期图 2×2 表格直链）
  ```
- 移植条件: 纯 markdown+文件组织约定，零依赖，任何语言环境都能照搬。需改造点：①手册模板并入我们项目 conventions（zoro-pm 项目结构）；②补"预期输出"时我们按 PNG+PDF+CSV 三件套约定执行；③原仓缺环境锁，我们的手册四段式应加第五段"怎么跑的"（脚本路径+参数+环境，对应全局规则 12）。
- 质量评价: 该仓 ⑦验证要求 拿满分全靠这套组织：手册即计划、预期图即验收、winner 即人工确认终版后留下的记录；是五仓中唯一"代码本身不可移植、管理做法完全可移植"的案例。
- 修订记录: 2026-09-04 收录(一期精读批次E)
