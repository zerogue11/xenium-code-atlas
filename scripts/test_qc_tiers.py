# -*- coding: utf-8 -*-
r"""QC tier 语义单元测试（零依赖纯断言, P-001 防回归）

被测对象: scripts/precompute_simulator.py 的 apply_qc_filters + QC_TIERS。
背景: 模拟器 P-001 坑事件教的就是「filter_cells 与 filter_genes 的阈值语义不可错位」
(ist_benchmarking st_utils.py:70 曾把细胞阈值塞给基因过滤), 本测试把该语义锁死。

合成矩阵设计(40 细胞 × 30 基因, 四个细胞群手算期望):
  A 群 22 细胞: G00-G19 各 10 counts → total 200 / 20 基因 (三档全过的"强细胞")
  B 群  8 细胞: G00-G24 各  1 count → total  25 / 25 基因 (恰在 loose min_counts=25 边界, 验证阈值含等号)
  B2 群 6 细胞: G00-G14 各  4 counts → total  60 / 15 基因 (过 standard、被 strict 双阈值拦下)
  C 群  4 细胞: G20-G29 各 25 counts → total 250 / 10 基因 (恰在 standard min_genes=10 边界)
基因广度(被多少细胞表达):
  G00-G14: 22+8+6 = 36 | G15-G19: 22+8 = 30 | G20-G24: 8+4 = 12 | G25-G29: 仅 4 (P-001 语义用例)

期望存活(手算字面量, 逐格核对):
  loose   (25/5;  基因 5/1) → 40 细胞 × 25 基因 (四群全过细胞关; 仅 G25-29 广度 4<5 被滤)
  standard(50/10; 基因 1/10) → 32 细胞 × 20 基因 (B 群 25<50 出局; C 群恰 10 基因压线过关;
                               基因关在 32 细胞上重算: G20-29 仅剩 C 群 4 细胞表达, 广度塌缩全出局)
  strict  (100/20;基因 1/20) → 22 细胞 × 20 基因 (仅 A 群; G00-19 广度 22≥20 压线存活)

用法:
  C:\xenium_envs\xenium-cn-py311\Scripts\python.exe scripts\test_qc_tiers.py
退出码: 0=全部通过, 1=有断言失败
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # 便于直接 import 同目录模块

import numpy as np
from scipy.sparse import csr_matrix
import anndata as ad

from precompute_simulator import QC_TIERS, apply_qc_filters

N_CELLS, N_GENES = 40, 30


def build_matrix():
    """构造 40x30 确定性合成计数矩阵(稀疏 CSR AnnData), 群体设计见模块 docstring。"""
    X = np.zeros((N_CELLS, N_GENES), dtype=np.float32)
    X[0:22, 0:20] = 10     # A 群: 强细胞, 三档全过
    X[22:30, 0:25] = 1     # B 群: 25 total, 恰在 loose 边界
    X[30:36, 0:15] = 4     # B2 群: 过 standard、不过 strict
    X[36:40, 20:30] = 25   # C 群: G20-G29 各 25 counts → total 250 / 10 基因(恰过 standard min_genes 边界)
    adata = ad.AnnData(X=csr_matrix(X))
    adata.var_names = [f"G{i:02d}" for i in range(N_GENES)]
    adata.obs_names = [f"c{i:02d}" for i in range(N_CELLS)]
    return adata


# 三档期望存活 (n_cells, n_vars) —— 手算字面量, 不允许用实现来反推
EXPECTED = {"loose": (40, 25), "standard": (32, 20), "strict": (22, 20)}


def main():
    checks = 0
    # 1) 三档存活性精确断言
    for tier, (n_cells, n_genes) in EXPECTED.items():
        adata = build_matrix()
        apply_qc_filters(adata, QC_TIERS[tier])
        assert adata.n_obs == n_cells, f"[{tier}] 存活细胞 {adata.n_obs} != 期望 {n_cells} (min_counts/min_genes 语义漂移?)"
        assert adata.n_vars == n_genes, f"[{tier}] 存活基因 {adata.n_vars} != 期望 {n_genes} (gene_min_cells/gene_min_counts 语义漂移?)"
        checks += 2
    # 2) P-001 回归: G25 深度 100(total counts) 远超 gene_min_counts=1,
    #    但广度 4 细胞 < gene_min_cells=5 → 必须被过滤; 若它存活即语义错位事故重演
    adata = build_matrix()
    apply_qc_filters(adata, QC_TIERS["loose"])
    assert "G25" not in list(adata.var_names), "G25(高深度低广度)在 loose 存活 → gene 阈值语义错位 (P-001 事故)"
    checks += 1
    # 3) 反向语义: G00 靠广度(36 细胞, 其中 B 群仅 1 count)存活 → min_cells 按"表达细胞数"计而非计数总量
    assert "G00" in list(adata.var_names), "G00(高广度低单细胞深度)在 loose 被误滤 → min_cells 被当成了 min_counts"
    checks += 1
    # 4) 边界含等号: B 群 total=25 恰等于 loose min_counts=25 → 全部 8 个 B 细胞存活 (scanpy 阈值为 ≥)
    assert all(f"c{i:02d}" in list(adata.obs_names) for i in range(22, 30)), "B 群边界细胞被误滤 → min_counts 边界语义变化"
    checks += 1
    print(f"✅ QC tier 语义单测通过 ({checks} 项断言, 矩阵 {N_CELLS}x{N_GENES}, 三档期望全部命中)")


if __name__ == "__main__":
    main()
