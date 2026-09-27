# -*- coding: utf-8 -*-
r"""从 v2 知识工程库 91 篇提取 JSON 派生「图形类型书目」（269 条绘图借鉴条目）。

种子数据（只读）: F:\我的科研\xenium-knowledge-tree\01_资料库\extract\LIT-*.json
  （编号无 LIT-083、含 LIT-092，按实际文件遍历）
字段: 每篇顶层 "绘图借鉴" = list[dict]{图号, 图形类型, 借鉴}

产出: 01_资料库/图形类型书目.csv
  列: 文献ID, 题名, 期刊, 年份, 图号, 原始图形类型, 规范类型, 借鉴, 对应repo
归一化规则: 有序关键词表（先特异后一般），首命中生效；未命中=未归类（人工并入）。
注意: 探查阶段的统计（2026-09-27 agent 报告）与本脚本实现存在口径细节差异时，
      以本脚本输出为准（唯一可复跑事实源）。
用法: python scripts/build_figure_catalog.py
"""
import csv
import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEED_GLOB = r"F:\我的科研\xenium-knowledge-tree\01_资料库\extract\LIT-*.json"
OUT = os.path.join(ROOT, "01_资料库", "图形类型书目.csv")
MASTER = os.path.join(ROOT, "01_资料库", "代码资源主表.csv")

# 归一化规则：顺序即优先级，每条首个命中关键词生效。
# 设计原则：内容类（空间/通讯/邻域等描述"画的是什么生物学内容"）先于
# 形式类（点图/热图/小提琴等只描述"画成什么形状"）——组合描述
# 如"邻域富集热图""空间细胞类型点图"应归内容类（与探查口径一致）。
RULES = [
    ("机制/流程示意图", ["示意图", "流程图", "工作流", "概念图", "总览", "架构",
                        "graphical abstract", "schematic", "study design", "实验设计",
                        "分析策略", "方法概览", "流水线图", "决策图", "路线图"]),
    ("桑基/冲积图", ["桑基", "sankey", "冲积", "alluvial"]),
    ("细胞比例/构成图", ["比例", "构成", "堆叠", "占比", "组成", "细胞分数",
                        "proportion", "stacked", "fraction", "饼图", "pie"]),
    ("空间域/生态位分区图", ["niche", "空间域", "生态位", "空间聚类", "超像素",
                          "分区", "domain", "社区发现", "区域划分", "空间分层",
                          "分层注释", "因子图", "dbscan", "集群图", "tls"]),
    ("细胞邻域/共定位分析图", ["邻域", "共定位", "邻近", "邻接", "共现",
                            "neighborhood", "nhood", "coloc", "clq"]),
    ("距离分箱/空间梯度定量图", ["距离", "分箱", "径向", "梯度", "沿轴", "深度",
                             "band", "binned", "最近邻", "border", "margin",
                             "invasion", "侵入前沿", "肿瘤边界", "半径"]),
    ("细胞通讯图", ["通讯", "弦图", "圈图", "互作", "配体", "受体", "connectome",
                   "cellchat", "cellphone", "ligand", "crosstalk", "chord", "circos",
                   "信号网络", "信号通路图", "网络图"]),
    ("轨迹/拟时序图", ["轨迹", "拟时序", "pseudotime", "pseudo-time", "paga",
                      "velocity", "时序", "分化路径", "发育轨迹"]),
    ("克隆/谱系追踪图", ["克隆", "谱系", "系统发育", "tcr", "bcr", "亚克隆",
                        "进化树", "克隆型", "克隆扩增", "phylo"]),
    ("组织学/多模态对齐图", ["h&e", "he染色", "组织学", "病理图", "配准", "对齐",
                          "多模态", "图像叠加", "形态学", "切片成像", "ihc",
                          "荧光显微", "跨模态"]),
    ("3D/跨切片连续图", ["3d", "三维", "跨切片", "连续切片", "堆叠切片", "重建"]),
    ("基准/性能对比图", ["基准", "性能", "对比评估", "一致性", "roc", "auc",
                       "评分对比", "accuracy", "shap", "benchmark", "方法对比",
                       "推断基因", "实测基因"]),
    ("QC/技术评估图", ["qc", "质量", "噪声", "探针", "计数分布", "检出率"]),
    ("富集/通路分析图", ["富集", "通路", "gsea", "go 富集", "kegg", "module",
                       " hallmark"]),
    ("火山/差异统计图", ["火山", "volcano", "森林图", "forest", "差异基因",
                        "差异表达", "deg", "milo", "beeswarm"]),
    ("空间细胞定位图", ["细胞定位", "细胞类型空间", "空间分布", "空间散点",
                       "细胞类型分布", "空间作图", "细胞映射", "解卷积空间",
                       "xenium空间", "空间细胞", "细胞空间", "组织空间",
                       "多边形空间", "核扩展"]),
    ("空间基因表达图", ["空间表达", "基因表达", "转录本", "表达量", "marker",
                       "表达图", "空间基因", "原位表达", "空间映射", "叠加空间",
                       "表达空间"]),
    ("降维嵌入图", ["umap", "tsne", "t-sne", "t sne", "降维", "聚类散点",
                   "嵌入空间", "流形"]),
    ("点图/气泡图", ["dotplot", "dot plot", "点图", "气泡", "bubble"]),
    ("热图/矩阵图", ["热图", "heatmap", "heat map", "矩阵图", "矩阵"]),
    ("小提琴/箱线图", ["小提琴", "箱线", "盒形", "violin", "box"]),
    ("多面板组合图", ["多面板", "组合图", "panel", "四联", "三联", "阵列",
                     "多图联动", "并列验证", "对照图"]),
    ("折线/趋势/排序图", ["折线", "趋势", "排序", "曲线", "rank", "时间序列图"]),
]

# 人工并入（2026-09-27 逐条判定；键=(文献ID, 图号)，值=规范类型 or "其他"）
MANUAL_OVERRIDES = {
    ("LIT-005", "Fig.3E"): "空间域/生态位分区图",     # Visium spot分层注释图
    ("LIT-009", "Fig.1"): "空间细胞定位图",           # Xenium空间细胞分布图
    ("LIT-010", "Fig.7"): "多面板组合图",             # 分子-功能并列验证图
    ("LIT-011", "Fig.1"): "其他",                     # 数值模拟流场图（罕见，保留观察）
    ("LIT-011", "Fig.4"): "空间基因表达图",           # Xenium单细胞原位表达空间图
    ("LIT-012", "Fig.5"): "组织学/多模态对齐图",      # 荧光显微图+Xenium注释叠加
    ("LIT-017", "Fig.2"): "空间细胞定位图",           # 力导向图+核扩展多边形空间图
    ("LIT-018", "Fig.2h"): "其他",                    # ATAC coverage+eGRN loop（表观特殊图）
    ("LIT-020", "Fig.3A"): "组织学/多模态对齐图",     # 多标记IHC并排对照
    ("LIT-021", "Fig.6B"): "基准/性能对比图",         # 推断基因vs实测基因ROI对照
    ("LIT-024", "Figure 1F"): "空间域/生态位分区图",  # 像素级无分割因子图
    ("LIT-037", "Fig.6E"): "空间域/生态位分区图",     # DBSCAN免疫集群图
    ("LIT-038", "Fig.6a-g"): "机制/流程示意图",       # TLS亚型空间分析流水线图
    ("LIT-039", "Fig.7F-G"): "空间基因表达图",        # TF motif偏差评分空间映射
    ("LIT-046", "Fig.5a"): "细胞通讯图",              # 互作网络图（tnbc-chemo语境）
    ("LIT-050", "Fig.4c"): "空间细胞定位图",          # 组织空间图(tissue plot)
    ("LIT-051", "Fig.5A"): "空间基因表达图",          # 血管ROI细胞-基因叠加空间图
    ("LIT-054", "Fig.5D-G"): "细胞通讯图",            # 圆形信号网络图
    ("LIT-058", "Fig.1c"): "其他",                    # 词云图（罕见）
    ("LIT-064", "Fig.5B"): "空间细胞定位图",          # 高分辨空间细胞分布+局部放大
    ("LIT-067", "Fig.6g-h"): "组织学/多模态对齐图",   # 跨模态插值空间映射
    ("LIT-070", "Fig.5C-D"): "其他",                  # 三元图（罕见）
    ("LIT-082", "Fig.3I"): "细胞通讯图",              # 网络图（免疫调节语境）
    ("LIT-084", "Fig.2g-h"): "组织学/多模态对齐图",   # 跨模态空间对照图
    ("LIT-087", "Fig.1"): "基准/性能对比图",          # 方法对比分组条形图
    ("LIT-088", "Fig.4"): "机制/流程示意图",          # 预处理路径决策图
    ("LIT-092", "Fig.4"): "空间基因表达图",           # 连续值空间映射图
    ("LIT-092", "Fig.1"): "距离分箱/空间梯度定量图",  # 半径编码环形图
    # 2026-09-27 二批（借"借鉴"原文判定）：密度类空间图按内容归位
    ("LIT-013", "Fig.4"): "空间细胞定位图",           # 成纤维细胞密度着色+切片计数
    ("LIT-026", "Fig.4d"): "空间细胞定位图",          # 两巨噬亚群kernel density并排
    ("LIT-033", "Fig.2C"): "距离分箱/空间梯度定量图", # 相对距离核密度+厚度量化
    ("LIT-035", "Fig.1a/2d"): "距离分箱/空间梯度定量图", # crypt-villus轴+距离双坐标IMAP
}


def normalize(raw: str, lit: str = "", fig: str = "") -> str:
    """自由文本图形类型 → 规范类型；人工表优先，未命中返回 '未归类'。"""
    if lit and (lit, fig) in MANUAL_OVERRIDES:
        return MANUAL_OVERRIDES[(lit, fig)]
    low = (raw or "").lower()
    for name, kws in RULES:
        for kw in kws:
            if kw in low:
                return name
    return "未归类"


def main():
    # LIT -> repos 反查（来自主表 文献IDs 列，多仓分号；S 级带 (S) 标记）
    lit2repos = {}
    with open(MASTER, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            grade_tag = "" if r["精选级"] != "S" else "(S)"
            for lit in r["文献IDs"].split(";"):
                lit = lit.strip()
                if not lit:
                    continue
                lit2repos.setdefault(lit, []).append(f"{r['owner']}/{r['repo']}{grade_tag}")

    out_rows = []
    files = sorted(glob.glob(SEED_GLOB))
    for fp in files:
        with open(fp, encoding="utf-8") as jf:
            d = json.load(jf)
        lit = d.get("文献ID", os.path.basename(fp)[:-5])
        title = (d.get("中文题名") or d.get("英文题名") or "")[:30]
        journal, year = d.get("期刊", ""), d.get("年份", "")
        for item in d.get("绘图借鉴", []) or []:
            raw = str(item.get("图形类型", ""))
            fig_no = str(item.get("图号", ""))
            out_rows.append({
                "文献ID": lit, "题名": title, "期刊": journal, "年份": year,
                "图号": fig_no, "原始图形类型": raw,
                "规范类型": normalize(raw, lit, fig_no),
                "借鉴": str(item.get("借鉴", "")),
                "对应repo": ";".join(lit2repos.get(lit, [])),
            })

    cols = ["文献ID", "题名", "期刊", "年份", "图号", "原始图形类型",
            "规范类型", "借鉴", "对应repo"]
    with open(OUT, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(out_rows)

    # 分布对账
    from collections import Counter
    dist = Counter(r["规范类型"] for r in out_rows)
    print(f"条目总数: {len(out_rows)}（文献 {len(files)} 篇）")
    for name, n in dist.most_common():
        print(f"  {name:<16} {n}")
    un = [r for r in out_rows if r["规范类型"] == "未归类"]
    if un:
        print("\n未归类条目（需人工并入）:")
        for r in un:
            print(f"  {r['文献ID']} {r['图号']}: {r['原始图形类型'][:60]}")
    print(f"\n输出 -> {OUT}")


if __name__ == "__main__":
    main()
