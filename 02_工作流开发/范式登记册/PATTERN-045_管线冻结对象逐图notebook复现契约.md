# PATTERN-045 · 管线冻结对象+逐图 notebook 复现契约
- 来源: Goldrathlab/Spatial-TRM-paper（LIT-035）相对/路径:行号 `Figure_2/2e.ipynb` cell2-3（`adata = sc.read_h5ad("../data/adata/timecourse.h5ad")` 后仅 `sc.pp.normalize_total`+`sc.pp.log1p`）；README Figures 节逐图链接表
- 场景: 论文级复现仓/多人协作大项目：上游产数管线重、下游出图碎。需要"产数一次冻结、出图只读不重算"，且 reviewer 能按图号直达代码。
- 做法: 仓库分两层。产数层=编号 notebook 链（01_…14_）+私有 core_functions 包，终点统一写冻结 h5ad（data/adata/*.h5ad，文件名=数据集语义名如 timecourse/human/perturb）；出图层=每图一 notebook，命名即图号（2abc.ipynb、5h_part1…），首个数据 cell 固定为 `sc.read_h5ad("../data/adata/<对象>.h5ad")`，随后只做浅变换（normalize_total/log1p）与绘图，绝不重跑聚类/整合。README 用 markdown 表维护"图号→notebook 链接"映射。
  ```python
  # Figure_2/2e.ipynb（全文骨架）
  adata = sc.read_h5ad("../data/adata/timecourse.h5ad")
  sc.pp.normalize_total(adata, target_sum=1e4)
  sc.pp.log1p(adata)
  # 之后全是绘图 cell
  ```
- 搬运条件: 依赖 AnnData/scanpy；BSD-3 类许可（仓含 LICENSE）。需改造点：①我们项目里冻结对象路径应换成 conventions 定版库路径（PATTERN-028 locked 命名）；②figure notebook 需补 seed 与输出三件套（PNG+PDF+CSV）契约；③硬编码 /mnt/sata1 路径改相对/配置。
- 工程评价: 双层分离+README 图号索引是该仓 10/14 分的主要来源；但产数层 core_functions 按管线复制（4 份近重复）、冻结对象无版本号，是我们移植时必须补的短板。
- 迭代记录: 2026-09-04 收录(一期精读批次E)
