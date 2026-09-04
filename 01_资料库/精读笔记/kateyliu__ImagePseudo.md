# 精读笔记 · kateyliu/ImagePseudo

- repo: https://github.com/kateyliu/ImagePseudo
- 来源文献: LIT-023 / Liu Y et al., "Image-based inference of tumor cell trajectories enables large-scale cancer progression analysis", Sci Adv 11(29):eadv9466 (2025)（README:10）
- 锁定SHA: `65dd85fa47f9bd47d064108e07bc68a763d07983`（2025-10-14）
- 复核分类: 图像组 · WSI→ViT 特征→PAGA/DPT 伪时序 · MIT（LICENSE）

## 代码结构走读（实际读了什么）

1404 行 Python，四脚本管线，无包无测试：
- `GradePrediction.py`（195 行，入口1）：`ViTModel.from_pretrained("owkin/phikon")` 冻结抽取器 + 自定义 5 类头（768→128→5，:52-66）→ `extract_feature_from_WSI`（:69）：openslide 读片 → `get_mask_for_slide_image` 组织掩码 → 按 STEP_SIZE=400 网格逐 patch，20x 片 resize 到 224 → 每patch存 768 维特征+预测分级 → 生成 (n_rows,n_cols) 分级图 PNG + CSV（n_col,n_row,pred_class,x0..x767）。
- `Pseudotime.py`（71 行，入口2）：CSV 特征列(3:) 作 X、前三列作 obs 建 AnnData → PCA(arpack) → neighbors(4,20) → leiden(1) → PAGA → `start_class=4` 硬编码根（:23，注释掉了原来的 min(pred_class)）→ DPT → 按伪时序排序的坐标欧氏距离归一化 → 写 h5ad。
- `Fitness.py`（98 行，入口3）：读 h5ad → leiden 簇丰度 Shannon 熵 → leiden×pred_class 组内均值坐标的两两欧氏距离/伪时序差 = 速度 → `fitness = speed × shannon_index` → 汇总 CSV。
- `segmentation_functions.py`（1040 行）：**Kaggle 2018 核分割代码直接搬入**，颜色反卷积/otsu/watershed/XML 掩码等 40+ 函数大杂烩，:7 `import scipy.misc`。

**scipy 冲突核实（任务点名项）——实锤**：`segmentation_functions.py:7` 顶层 `import scipy.misc`；:491/:541 使用 `misc.imsave`（scipy.misc.imsave 早在 scipy 1.2 就已移除，整个 misc 模块在 1.12 移除）；而 `requirement.txt` 明确钉 `scipy==1.12.0`。`GradePrediction.py:18` `from segmentation_functions import get_mask_for_slide_image` 顶层导入 → 在锁定环境装完依赖后运行入口1即抛 `ModuleNotFoundError: No module named 'scipy.misc'`。修复只需删 import 并把两处 imsave 换 `skimage.io.imsave`/`imageio.imwrite`。

## 关键脚本清单

| 文件 | 行数 | 一句话 |
|---|---|---|
| GradePrediction.py | 195 | phikon ViT 逐 patch 特征+分级预测，出分级热图与特征 CSV |
| Pseudotime.py | 71 | 特征 CSV→AnnData→PCA/leiden/PAGA/DPT→伪时序 h5ad |
| Fitness.py | 98 | leiden 多样性(Shannon) × 空间速度 = 肿瘤 fitness |
| segmentation_functions.py | 1040 | 组织掩码/核分割函数库（Kaggle 遗产，含 scipy.misc 炸弹） |
| requirement.txt | 17 | 版本锁定（scipy==1.12.0 与代码冲突） |
| example_result/ | - | 示例输入输出四件套（csv/h5ad/png/results.csv） |

## 技术路线还原（固定清单勾选）

1. **数据读取**（WSI：svs/tif/tiff/dicom/ndpi，openslide）
2. **质控QC**（组织掩码过滤非组织 patch，GradePrediction.py:96-101）
3. **注释**（patch 级 G1-G4/other 分级预测，pred_class 写入 obs）
4. **降维**（PCA arpack，Pseudotime.py:14）
5. **聚类**（leiden resolution=1，Pseudotime.py:16）
6. **绘图**（WSI 分级图 PNG，GradePrediction.py:140-144）
7. **导出**（特征 CSV / h5ad / fitness CSV）

**骨架步骤数：7**（PAGA/DPT 伪时序不在固定清单，为该仓核心方法层）。

## 工程审计表（7 维 × 0-2，共 5/14）

| 维度 | 分 | 证据 |
|---|---|---|
| ①职责单一/模块化 | 1 | 三入口+一函数库分工清楚，但 segmentation_functions.py 是 1040 行无主大杂烩（40+ 函数松散堆放） |
| ②命名规范 | 0 | `dpt_pesudotime` 拼写错误贯穿写读两侧（Fitness.py:17,33,57 vs h5ad obs）；死函数 `testf()`（segmentation_functions.py:30）；`pred_WSI` 与 `Shinkage` 注释拼写 |
| ③安全性 | 2 | 无凭据/绝对路径，默认相对路径 os.getcwd |
| ④最简化 | 0 | 未用 import 一排（ET/re/sys/time/random 等，segmentation_functions.py:20-26）；GradePrediction.py:100-119 `if mask is None` 死分支（mask 早已必然赋值）；phikon 抽取器全局+MyModel 内部双份加载（:36,:52） |
| ⑤逻辑健壮性 | 0 | 整函数 `except Exception as e: print(e)` 吞掉全部错误（GradePrediction.py:147-148），单张片失败静默跳过；`args.model` 默认是目录路径传 torch.load 必失败（:166）；speed 除零未防（Fitness.py:24） |
| ⑥可复现性 | 1 | requirement.txt 锁版本（但锁出冲突）；leiden 依赖 scanpy 默认 random_state 未显式；PAGA 根节点 `start_class=4` 硬编码（Pseudotime.py:23-24），换数据集语义即漂移 |
| ⑦验证纪律 | 1 | example_result/ 提供完整示例输入输出对照（最低限验证痕迹）；无测试无 CI |

## 可搬运模式

- PATTERN-037：WSI 网格 patch 特征→AnnData 空间伪时序映射链（n_row/n_col 网格坐标与特征列并表是链的关键约定）。

## 坑与限制（实读发现）

- **scipy.misc 与 scipy==1.12 硬冲突（已核实）**，见上；装好环境第一行 import 就炸，属"开箱即坏"。
- 根节点硬编码 pred_class==4（"other" 类），与论文叙述的起点选择耦合，跨癌种需改源码。
- GradePrediction 主循环逐行 `slide_df.loc[i] = newRow`（:135-137），O(n²) 追加，大 WSI 显著慢，应改 list append + concat。
- 特征与预测用同一 `patch_tensor`，但 `Extractor` 与 `model.extractor` 是两个独立 phikon 实例，显存/时间双倍浪费。
- `mask` resize 后以 `<1` 判定过滤（:113），阈值语义依赖 resize 的 order=0 取整，边界 patch 行为不直观。
- Fitness 的 speed 取 log 后直接乘 Shannon 熵，量纲为经验组合，无稳定性分析。
- 论文级别结果依赖其训练好的分级模型权重（仓库未附带 model/，README 只给结构）。

## 一句总评

思路清晰（病理图→ViT 特征→拟时序→适应度）但工程执行粗糙：一个必炸的 scipy.misc import、满地死代码、吞错的裸 except——当作方法论文的代码附件读可以，直接复用前需先做一轮清创。
