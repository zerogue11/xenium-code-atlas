# `kateyliu/ImagePseudo`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\kateyliu__ImagePseudo`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-023：基于图像的肿瘤细胞轨迹推断（README 英文原题 "Image-based inference of tumor cell trajectories enables large-scale cancer progression analysis"，Sci Adv 2025；一作 Yang Liu, UT Southwestern） |
| 精选级 | S |
| 主分类 | P7 图像组学·多模态（复核确认：WSI→形态学特征→伪时序→适应度，图像组学典型链路；与初判一致） |
| 次要用途 | （可空）肿瘤进化/进展速度量化，贴近 P8 应用叙事 |
| 一句话功能 | 三步 CLI 流水：GradePrediction.py 用预训练 ViT 对 WSI 切 patch（224px、步长 400）提特征并逐 patch 预测肿瘤分级（G1-G4/other 五类）→ Pseudotime.py 用 scanpy PCA+leiden+PAGA+DPT 把 patch 特征图转伪时序 → Fitness.py 推断肿瘤生长速度、多样性与进展适应度 |
| License | 复核更正：UT Southwestern 自定义"学术研究专用"许可——BSD 条款文本 + 明文禁止任何商业用途/营利实体使用；主表填"MIT"与 LICENSE 文本不符，建议更正 |
| 语言与规模 | Python；主表 Pythonx4；116 MB（assets 示意图 + example_result 示例输出） |
| 运行入口 | 三个 py 脚本顺序执行；conda python=3.9 + `pip install -r requirement.txt` + conda 另装 openslide/python-igraph/leidenalg；预训练模型 model.pt 与示例 svs 从 Zenodo（记录 16376974）下载解压到 model/ |
| 复现难度 | 低-中 — 步骤少、参数简单、有示例数据与示例输出三件套；扣分项：需外链 Zenodo 下模型，且有 scipy 版本硬冲突需手工绕（见坑①） |
| 与范式的关系 | "HE 形态→拟时序→肿瘤进化动力学"范式，与 zoro-spatial 的 HE→表达预测支线互补（一个出轨迹、一个出表达）；候选池 |
| 坑提示 | ① segmentation_functions.py 顶部 `import scipy.misc`（该模块已随 SciPy 移除），与 requirement.txt 固定的 scipy==1.12.0 直接冲突，Step1 会 ImportError——需降级 scipy 或改写 import【冲突属实，运行未实测】；② Pseudotime.py 根节点硬编码 start_class=4，注释写 "G1 as root" 但 GradePrediction.py 的类映射中 4=other，根节点语义需人工核对【待验证】；③ 依赖版本锁得较死（transformers==4.38.2、scanpy==1.9.8 等），openslide 三件走 conda 不走 pip；④ 支持 svs/tif/tiff/dicom/ndpi，整文件夹作输入 |
| 锁定 SHA | 65dd85fa47f9bd47d064108e07bc68a763d07983（主表） |

## 结构速览

- 三入口：GradePrediction.py（ViT 特征+分级）、Pseudotime.py（PAGA+DPT 伪时序）、Fitness.py（生长速度/多样性/适应度 → results.csv）
- segmentation_functions.py：Kaggle 2018 DSB 改的核分割/掩膜函数（被 GradePrediction 调用）
- `assets/`（流程图）、`example_result/`（示例特征 csv/png、h5ad、results.csv）、`requirement.txt` + `LICENSE`
- 关联：无同作者/同文献其他仓在库；HE→空间预测支线对照 hisplan/sharp（P7）

## README/代码实读要点

- 论文出处、Zenodo 模型/示例数据链接与 model/ 目录摆放方式写得很具体
- 每步输入输出有文件名示例（如 example.svs_286cols_210rows.csv → .h5ad → results.csv），特征图即"伪时序地图"
- TroubleShooting 章节存在但为空

## 抽读实录

- 读 README 全文；head Pseudotime.py（30 行，确认 PAGA/DPT 与硬编码根节点）、GradePrediction.py（30 行，确认 ViTModel/openslide/类映射）、segmentation_functions.py（15 行，确认 scipy.misc）；sed LICENSE 6-30 行。

## 复用建议

- 复跑前先把 scipy 降到 <1.10 或改 import，并核对根节点类号；思路（patch 特征→PAGA/DPT→适应度）可拆出来接到自己的 WSI 管线；注意非商用许可。
