# -*- coding: utf-8 -*-
r"""Xenium 决策剧场 · UC/CROHN T1-lite 资产生成（T3 示意, 零编造数值）

诚实性说明: 两篇文献的具体定量结果在本库审计记录中无可靠数值来源——按反编造红线,
本脚本只生成「文献路线图/定性结论示意」(T3), 不伪造比例图冒充 T2 参数化重绘。
每张图 manifest 标注 nature="示意(文献定性结论可视化, 未使用论文数值)"。

产出:
  docs/simulator/assets/UC/uc_route_map.png + manifest.json
  docs/simulator/assets/CROHN/crohn_route_map.png + manifest.json
用法:
  C:\xenium_envs\xenium-cn-py311\Scripts\python.exe scripts\precompute_lit_redraw.py
"""
import json
import os
import sys
from pathlib import Path

import matplotlib
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS = ROOT / "docs" / "simulator" / "assets"


def route_map(out: Path, title, steps, conclusion, note, colors):
    fig, ax = plt.subplots(figsize=(9.6, 4.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.6)
    ax.axis("off")
    n = len(steps)
    w, h, gap = 1.72, 0.78, 0.28
    x0 = (10 - n * w - (n - 1) * gap) / 2
    for i, (label, sub) in enumerate(steps):
        x = x0 + i * (w + gap)
        box = FancyBboxPatch((x, 2.6), w, h, boxstyle="round,pad=0.06",
                             fc=colors[i % len(colors)], ec="#666", lw=0.8)
        ax.add_patch(box)
        ax.text(x + w / 2, 3.12, label, ha="center", va="center", fontsize=8.2, weight="bold")
        ax.text(x + w / 2, 2.86, sub, ha="center", va="center", fontsize=6.4, color="#444")
        if i < n - 1:
            ax.add_patch(FancyArrowPatch((x + w + 0.03, 3.0), (x + w + gap - 0.03, 3.0),
                                         arrowstyle="-|>", mutation_scale=10, color="#888"))
    ax.text(5, 4.28, title, ha="center", fontsize=11, weight="bold")
    ax.text(5, 1.7, "结论（文献定性表述）", ha="center", fontsize=8.6, color="#555", weight="bold")
    ax.text(5, 1.15, conclusion, ha="center", fontsize=8.6, color="#222", wrap=True)
    ax.text(5, 0.35, note, ha="center", fontsize=7, color="#999")
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=110, facecolor="white")
    plt.close(fig)
    print(f"  -> {out} ({out.stat().st_size // 1024} KB)", flush=True)


def main():
    # ---- UC (LIT-053 UCSF DSCOLAB) ----
    uc_out = ASSETS / "UC" / "uc_route_map.png"
    route_map(
        uc_out,
        "UCSF DSCOLAB · 结肠炎 Xenium 研究路线（示意还原）",
        [("FFPE 活检", "炎症/非炎症配对"), ("装载", "read_10x_h5+cells"),
         ("统一 QC 核心", "50/10/1/10+补丁"), ("归一化+PCA", "固定默认"),
         ("聚类+注释", "区室→亚群"), ("IAF 识别", "成纤维亚群"),
         ("细胞网络", "炎症 vs 非炎症")],
        "炎症相关成纤维细胞（IAF）定位于离散空间位置，与上皮损伤区构成炎症细胞网络",
        "示意（文献定性结论可视化, 未使用论文数值）· Mennillo et al. bioRxiv 10.1101/2024.11.11.623014 → JCI 2026",
        ["#FDF6E9", "#EAF0FF", "#F4EAF0", "#EAF0FF", "#EFF7EE", "#F4EAF0", "#EFF7EE"],
    )
    uc_manifest = dict(dataset="UC", generated="2026-09-05", seed=0,
                       source="文献结论模式：UCSF DSCOLAB 结肠炎 Xenium 研究（LIT-053；bioRxiv 2024.11.11.623014，已发表 JCI 2026）",
                       nature="T1-lite：示意（文献定性结论可视化, 未使用论文数值）",
                       ref="Mennillo E, et al. doi:10.1101/2024.11.11.623014 → JCI 2026（jci.org/articles/view/202488）；方法参照本库 LIT-053 档案卡与 PATTERN-047",
                       doc="01_资料库/精读笔记/UCSF-DSCOLAB__spatial_transcriptomics_colitis_analysis_2024.md",
                       assets=[dict(file="uc_route_map.png", kind="T3", node="6-downstream",
                                    title="文献路线与结论总览（示意）",
                                    source="LIT-053 UCSF-DSCOLAB（文献还原）",
                                    nature="示意（文献定性结论可视化, 未使用论文数值）",
                                    ref="Mennillo et al. doi:10.1101/2024.11.11.623014 → JCI 2026")],
                       flags={"mode": "T1-lite", "t2_upgrade": "数据放出后接入 precompute_simulator.py 同构管线"})
    (ASSETS / "UC" / "manifest.json").write_text(json.dumps(uc_manifest, ensure_ascii=False, indent=1), encoding="utf-8")

    # ---- CROHN (LIT-066 Teichlab) ----
    cr_out = ASSETS / "CROHN" / "crohn_route_map.png"
    route_map(
        cr_out,
        "Teichlab · 克罗恩 Xenium 5K 链路线（示意还原）",
        [("预整合 h5ad", "64.6万×5001 复用"), ("元数据审计", "QC 列尽职调查"),
         ("scVI 潜空间", "批次对齐"), ("celltypist", "megagut 迁移"),
         ("人工映射", "低置信兜底"), ("cellcharter", "niche 发现"),
         ("生态型分析", "纤维化叙事")],
        "纤维化区基质细胞生态型扩张；scVI→celltypist→人工映射三段式注释迁移链（PATTERN-025 原型）",
        "示意（文献定性结论可视化, 未使用论文数值）· Teichlab crohns-fibroblast-atlas（MIT, LIT-066）",
        ["#EAF7F6", "#EAF0FF", "#F4EAF0", "#EFF7EE", "#FDF6E9", "#EAF0FF", "#EFF7EE"],
    )
    cr_manifest = dict(dataset="CROHN", generated="2026-09-05", seed=0,
                       source="文献结论模式：Teichlab crohns-fibroblast-atlas Xenium 5K 链镜像（LIT-066，MIT，有精读）",
                       nature="T1-lite：示意（文献定性结论可视化, 未使用论文数值）",
                       ref="Teichlab crohns-fibroblast-atlas（github.com/Teichlab/crohns-fibroblast-atlas）；本库精读 1a→8 逐 notebook 走读",
                       doc="01_资料库/精读笔记/Teichlab__crohns-fibroblast-atlas.md",
                       assets=[dict(file="crohn_route_map.png", kind="T3", node="6-downstream",
                                    title="文献路线与结论总览（示意）",
                                    source="LIT-066 Teichlab crohns-fibroblast-atlas（文献还原）",
                                    nature="示意（文献定性结论可视化, 未使用论文数值）",
                                    ref="Teichlab crohns-fibroblast-atlas（MIT）")],
                       flags={"mode": "T1-lite"})
    (ASSETS / "CROHN" / "manifest.json").write_text(json.dumps(cr_manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    print("lit_redraw 完成")


if __name__ == "__main__":
    main()
