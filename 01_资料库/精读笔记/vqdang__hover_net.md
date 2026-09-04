# 精读笔记 · vqdang__hover_net

- repo: vqdang/hover_net
- 来源文献: LIT-081（HoVer-Net: Simultaneous Segmentation and Classification of Nuclei in Multi-Tissue Histology Images, Med Image Anal 2019）
- 锁定SHA: 67e2ce5e3f1a64a2ece77ad1c24233653a9e0901（2023-10-27，PyTorch 主线）
- 复核分类: 分割/ISS 工具链（S 级）——HoVer-Net 官方 PyTorch 核分割/分型实现（TensorFlow 原版在另一 branch）

## 代码结构走读

目录 → 模块职责（实读）：
- `run_infer.py`（186 行）/ `run_tile.sh` / `run_wsi.sh`：CLI 薄入口，docopt 双层解析（顶层选 tile/wsi 子命令，子层各占一段 usage 字符串），把参数整理成 method_args/run_args 后实例化 `InferManager`。
- `infer/base.py`（94 行）：`InferManager.__load_model` 用 `import_module("models.hovernet.net_desc")` → `create_model` 工厂创建网络 → `torch.load()["desc"]` → `convert_pytorch_checkpoint` → `load_state_dict(strict=True)` → DataParallel 上 GPU；再动态 import `run_desc.infer_step` 与 `post_proc.process` 挂到 self（base.py:56-78）。**延迟加载、无 import 副作用**。
- `infer/tile.py`（388 行）：tile 模式。`_prepare_patching` reflect padding + 网格坐标展开；主循环按 `psutil` 可用内存×mem_usage 决定缓存几张图（tile.py:236-282），DataLoader 批推理后按 uid 重拆，`ProcessPoolExecutor` 并行做 patch 重拼装+后处理+回调落盘（mat/json/overlay/qupath 四格式）。
- `infer/wsi.py`（753 行）：WSI 模式。chunk→tile→patch 三级网格（`_get_tile_info` 的 ambiguous_size 边界带重复推理再合并，wsi.py:92-146），open-slide 读取、组织掩码过滤、结果按 chunk 汇总。
- `models/hovernet/net_desc.py`（154 行）：HoVerNet 网络——ResNet50 主干 + np/hv(/tp) 三解码支，`original`（270/80）与 `fast`（256/164）双模式，forward 内 /255 归一化与 crop_op 对齐 TF 行为（net_desc.py:101-145）。
- `models/hovernet/post_proc.py`（186 行）：HoVer 后处理——NP 概率二值化→去小对象→h/v 图 Sobel 梯度谷→距离变换分水岭（`__proc_np_hv`），再逐实例取矩心/轮廓/类型投票（`process`）。
- `dataloader/`（train_loader 194 行 + augs 109 行 + infer_loader）：训练增强（imgaug）与推理序列化数据集。
- `run_train.py`（305 行）+ `config.py`（69 行）+ `models/hovernet/opt.py`（142 行）：两阶段训练（先 freeze 主干训 decoder 50 epoch，再解冻），seed 管理、StepLR(25)、loss 字典 np(bce+dice)/hv(mse+msge)/tp(bce+dice)。
- `compute_stats.py`（248 行）+ `metrics/`：AJI/PQ 等指标。
- `dataset.py`（109 行）：Kumar/CPM17/CoNSeP 三数据集解析类 + `get_dataset` 工厂。

## 关键脚本清单

| 文件 | 行数 | 一句话 |
|---|---|---|
| run_infer.py | 186 | docopt 双层 CLI，组装参数后分派 tile/wsi 推理 |
| infer/base.py | 94 | 工厂创建模型+strict 加载 checkpoint+挂 infer_step/post_proc |
| infer/tile.py | 388 | 内存感知缓存+批量推理+并行重拼装/后处理/落盘 |
| models/hovernet/net_desc.py | 154 | HoVerNet 网络定义（original/fast 双模式） |
| models/hovernet/post_proc.py | 186 | 梯度谷分水岭实例分离+逐实例类型投票 |
| run_train.py | 305 | 两阶段训练编排（freeze→unfreeze）+ seed 链 |
| compute_stats.py | 248 | AJI/PQ 指标主计算脚本 |

## 技术路线还原（勾选固定清单，按实际顺序）

1. 数据读取（tile.py:257 cv2 读图 + reflect padding 切 patch；wsi.py openslide 读全片）
2. 导出（tile.py:170-212 四格式落盘：.mat 实例图/uid/类型/矩心、.json 实例信息、overlay .png、QuPath .tsv）

未做（其余 14 项均不涉及——这是纯分割/分类模型仓，不含表达矩阵分析）：质控QC、归一化、HVG、降维、聚类、注释、去卷积、空间邻域/域、细胞通讯、亚细胞、空间统计、配准/3D、多样本整合、绘图（overlay 可视化不算分析性绘图）。

## 工程审计表（7 维，0-2 分）

| 维度 | 分 | 证据 |
|---|---|---|
| 职责单一/模块化 | 2 | dataloader/infer/metrics/misc/models/run_utils 六包分工，入口脚本薄（run_infer.py 全文仅组装参数） |
| 命名规范 | 2 | 一致 snake_case；私有函数双下划线（post_proc.py:26）；仅小 typo "chane"（post_proc.py:125 TODO 注释） |
| 安全性 | 2 | 无硬编码路径/凭据，全部 docopt 参数；model_path 缺失显式 raise（run_infer.py:121-122） |
| 最简化 | 1 | infer/tile.py:1-42 import 冗余（multiprocessing Lock/Pool 重复导入 L3/L20、argparse/glob 等未用）；少量注释死代码 |
| 逻辑健壮性 | 2 | assert 内存比例（tile.py:156）与文件非空（tile.py:162）；并行 future 异常轮询（tile.py:373-386）；轮廓 <3 点/异常形状跳过（post_proc.py:140-143）；模型 mode 断言（net_desc.py:24-25） |
| 可复现性 | 2 | check_manual_seed + worker 种子链注释（run_train.py:74-89, run_utils/utils.py:33-42）；requirements.txt 全 == 锁定；CHANGELOG 记录版本；输入顺序强制 sort（tile.py:161） |
| 验证纪律 | 1 | 无 CI/测试目录；有 debug 开关（config.py:23）与完整 metrics 脚本做离线验证，但无自动化回归 |

总分：12/14

## 可搬运模式

- PATTERN-013 工厂式延迟加载分割模型封装（对照 Moldia 反面教材）
- PATTERN-014 内存感知 tile 缓存 + 并行后处理推理流水线
- PATTERN-015 HoVer 梯度谷分水岭后处理

## 坑与限制

- `net = torch.nn.DataParallel(net); net.to("cuda")`（base.py:69-70）——推理硬编码要求 GPU，CPU 不可跑；DataParallel 也是过时方案（代码内 TODO 自认应换 DDP）。
- tile 模式 `expected_usage = sys.getsizeof(img) * 5`（tile.py:271）内存估算系数 5 是 HoVerNet 经验值，换模型需手调（代码注释自认 "only applicable for HoVerNet"）。
- post_proc.py:18-22 `warnings.warn = noop` 全局静默警告，调试时易掩盖问题。
- WSI 模式 cache 目录默认 `cache`（run_infer.py:62）需要 SSD ≥100GB，README 自述。
- 类型投票取第二多类兜底逻辑（post_proc.py:175-177）在只有背景+一种类时会返回 0，需注意。

## 一句总评

五仓中工程质量最高的参照物：延迟加载、strict 权重校验、seed 链、内存感知调度、双级 CLI 全都做对了，A1 分割模块的加载/推理封装直接按它抄即可。
