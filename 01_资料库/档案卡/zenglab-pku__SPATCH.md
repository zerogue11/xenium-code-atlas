# `zenglab-pku/SPATCH`（档案卡）

> 由 agent 依据本地克隆实测撰写（2026-09-04）；不确定处一律【待补充】；禁止编造星标/日期/功能。
> 本地路径：`03_开源项目\zenglab-pku__SPATCH`

| 字段 | 内容 |
|---|---|
| 来源文献 | LIT-084：《高吞吐量亚细胞分辨率空间转录组平台的系统基准测试》（bioRxiv 2024）；LIT-090：《跨人肿瘤的高通量亚细胞分辨率空间转录组平台系统基准测试》（Nat Commun 2025） |
| 精选级 | S |
| 主分类 | P0 流程基准与质控（**复核调整：初判 P3 → P0**——仓库主旨即亚细胞平台基准测试与配套在线资源，P3 空间聚类仅为其 10 步之一环） |
| 次要用途 | P2 注释（9_st_annotation 跨工具注释迁移与一致性）、P3 空间域（7/10 聚类脚本）、P6 配准（3_registeration ST-CODEX 图像配准） |
| 一句话功能 | SPATCH（亚细胞/高通量 ST 平台基准资源，配在线数据门户 spatch.pku-genomics.org）的分析代码：多平台读入与 8µm bin 化、组织外信号去除、配准对齐相邻切片 CODEX 蛋白组、扩散效应评估、ST-CODEX 相关性、scRNA 预处理、聚类、细胞形态统计、注释迁移与一致性、空间聚类共 10 个编号脚本 |
| License | 无LICENSE(仅可学习不可转载)（主表值） |
| 语言与规模 | Python 为主 + R；py 9 个 + R 2 个；体积 0.1 MB（纯代码，数据全在在线门户） |
| 运行入口 | analysis/ 下按文件名编号 1→10 顺序手工执行（scanpy 读 raw/transcripts，8µm bin 或 cell 分辨率）；无环境文件【待补充】 |
| 复现难度 | 高 — 数据在在线门户与文献 supplementary，脚本间仅靠编号约定衔接、无 yml/requirements，且函数参数需按平台逐个适配 |
| 与范式的关系 | 与 LIT-086/088 同族的亚细胞平台基准：8µm bin 化函数、多平台读入归一、ST-蛋白(CODEX) 空间对齐相关性均为可直接抄的模块；候选池 |
| 坑提示 | ① 脚本头部带作者本机绝对路径痕迹（如 2_8um_bin.py 的 FilePath: /Users/morsouron/...），路径需全部自改；② 无 LICENSE、无环境锁；③ 脚本间 I/O 文件名约定需读代码确认，README 只给功能不给调用方式 |
| 锁定 SHA | `c20108f60660b86bc2740607d84fd825beaaceca`（主表锁定值；建卡时实测前缀 `c20108f606` 一致） |

## 结构速览

- `analysis/`：11 个编号脚本——1_load_data.py（scanpy 多平台读入存 h5ad）、2_8um_bin.py（Xenium/CosMx 8µm bin 化+组织外信号去除）、3_registeration.py（图像配准并变换 CODEX 通道/ST 坐标）、4_diffusion.py（相对扩散效应与组织内外最小距离）、5_correlation_with_codex.py（空间网格 ST-CODEX 相关）
- 续：6_scrna.r（scRNA 预处理）、7_cluster.py（ST 聚类）、8_cell_shape.py（细胞形态统计）、9_st_annotation.py（scRNA→ST 注释迁移）、9_st_annotation_consistency.r（注释工具一致性）、10_spatial_cluster.py（ST/CODEX 空间聚类与一致性）
- `analysis/README.md`：脚本级说明；顶层 README：Key points + 在线门户链接
- 无 LICENSE、无环境文件、无 notebook

## README/代码实读要点

- 定位：首个对"亚细胞分辨率+大 panel"最先进 ST 平台的基准，含分析工具基准与相邻切片 CODEX 空间蛋白交叉验证
- 2_8um_bin.py 的 bin 化实现：x_location×resolution 整除 8 取 binx/biny，groupby(binx,biny,feature_name) 计数后 unstack 成 8µm 矩阵，纯 pandas 实现、易移植
- 平台覆盖：Xenium 与 CosMx 显式出现在 2_8um_bin 的平台参数中【其余平台清单待读 1_load_data.py 确认】
- 脚本作者署名：Pengfei Ren（2_8um_bin.py 头部注释，2024-12-04）

## 抽读实录

- 读 README 全文（Key points、在线门户、10 个脚本说明）；ls analysis/；读 2_8um_bin.py 开头 25 行（bin 化函数签名与实现）。

## 复用建议

- 摘模块用：8µm bin 化函数直接移植 zoro-spatial 作"bin 模式"重分割选项；ST-CODEX 相关性思路留给未来蛋白验证段；整流程复跑需先拿到门户数据，成本高暂缓。
