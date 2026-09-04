# `ding-lab/10Xmapping`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\ding-lab__10Xmapping`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-019：肿瘤 2D/3D 进化研究（10Xmapping 为肿瘤进化/亚克隆分析的配套小工具；README 未给出论文题名【待补充】） |
| 精选级 | B |
| 主分类 | P6 空间统计·配准·3D（维持：分类体系 P6 示例已列 10xmapping；复核备注：功能实为"体细胞变异→10X 条码映射"，非空间统计/配准/3D，按定义更贴 P8 疾病应用，终审定夺） |
| 次要用途 | 逐细胞基因型/VAF 计算（肿瘤进化、亚克隆基因分型） |
| 一句话功能 | 3 个 Perl 小脚本：从 scRNA-seq BAM 中提取包含体细胞变异 ref/var 等位基因的 reads，映射回 10X 细胞条码，并统计各细胞支持 reads 数与 VAF（step1 10Xmapping.pl --mapq --bam --maf --out → step2 parse_scrna_bc.pl → step3 rc.pl） |
| License | 无LICENSE(仅可学习不可转载) |
| 语言与规模 | Perl；3 个脚本共约 9 KB（主表体积 0.0 MB） |
| 运行入口 | 命令行三步流水（Perl 解释器直接跑）；作者 Song Cao（scao@wustl.edu）；BAM 处理的依赖（如 samtools/pysam）README 未说明【待补充】 |
| 复现难度 | 低（脚本极小、每步仅 2-4 个参数），但前提是拿到配对的 scRNA-seq BAM 与 MAF 体细胞变异列表——数据准备才是难点 |
| 与范式的关系 | 逐细胞基因型/亚克隆映射的最简参考实现（变异→条码→VAF 三步式）；B 级仅作学习参考，非候选池 |
| 坑提示 | ① 无 LICENSE、无依赖说明、无测试数据；② 输出质量取决于 scRNA BAM 在变异位点的覆盖深度（3' 10X 表达数据覆盖极浅，假阴性率高，属方法固有局限）；③ 脚本内部逻辑未逐行核对（B 级未深读）【待补充】 |
| 锁定 SHA | 8d6fc1602c49d94bbcf5944a1dad0ed86f85bb19（主表） |

## 结构速览

- `10Xmapping.pl`（约 7 KB）：step1 主脚本，按 MAF 变异从 BAM 抽 ref/var 支持 reads
- `parse_scrna_bc.pl`：step2，整理 ref/var 等位基因与 10X 条码对应表
- `rc.pl`：step3，逐条码计数支持 reads 并算 VAF；`README.md` 仅 6 段使用说明
- 关联仓：ding-lab/ST_subclone_publication、ding-lab/mushroom、ding-lab/morph（同文献 LIT-019 主线仓）

## README/代码实读要点

- README 即使用文档：三个 step 的参数与输入输出定义，无安装、无依赖、无示例
- 输入: --mapq（默认 0）--bam（scRNA BAM）--maf（体细胞变异列表）
- 作者联系信息直接写在 README 首部

## 抽读实录

- 读 README 全文；wc -c 三个 .pl 与 README；未逐行读 Perl 源码（B 级深度）。

## 复用建议

- 仅当需要"表达数据逐细胞基因分型"的最简代码参考时翻看；实际肿瘤进化分析在本项目应走 ding-lab 的 ST_subclone_publication/mushroom 主线仓。
