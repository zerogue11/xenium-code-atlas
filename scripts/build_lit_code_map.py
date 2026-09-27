# -*- coding: utf-8 -*-
r"""生成「文献代码对照页」：91 篇文献 × 公开代码仓 × 本站档案卡的对照表。

数据（只读）：01_资料库/文献速查表.csv（91 篇）、01_资料库/代码资源主表.csv（72 仓）
产出：01_资料库/文献代码对照.md（站内页，mkdocs 收录）
新增文献后重跑本脚本即可更新对照页。
用法: python scripts/build_lit_code_map.py
"""
import csv
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LITS = os.path.join(ROOT, "01_资料库", "文献速查表.csv")
MASTER = os.path.join(ROOT, "01_资料库", "代码资源主表.csv")
OUT = os.path.join(ROOT, "01_资料库", "文献代码对照.md")

ATLAS_HOME = "https://zerogue11.github.io/xenium-code-atlas/"


def main():
    # 文献 -> [(owner/repo, URL, 档案卡目录, 精选级)]
    lit2repos = {}
    with open(MASTER, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            card = f"{r['owner']}__{r['repo']}"
            url = r["URL"]
            for lit in r["文献IDs"].split(";"):
                lit = lit.strip()
                if not lit:
                    continue
                lit2repos.setdefault(lit, []).append(
                    (f"{r['owner']}/{r['repo']}", url, card, r["精选级"]))

    lits = list(csv.DictReader(open(LITS, encoding="utf-8-sig")))
    buf = io.StringIO()
    buf.write("# 文献代码对照（91 篇 ↔ 公开代码仓）\n\n")
    buf.write("> 本站是**代码层**：每个仓的档案卡、精读审计与可照搬做法。\n")
    buf.write("> 姊妹站 **Xenium 学习网站**（文献知识层：91 篇逐篇详解、工具包选择器、资源库）"
              "目前在本机/私有仓，上线后此处换直链；本地路径 "
              "`F:\\我的科研\\xenium-knowledge-tree\\site\\Xenium交互式学习网站_v2.html`。\n\n")
    buf.write("| 编号 | 题名 | 期刊 · 年份 | 公开代码仓 | 本站档案卡 | 精选级 |\n")
    buf.write("|---|---|---|---|---|---|\n")
    n_with = n_without = 0
    for r in lits:
        lit = r["文献ID"]
        title = (r["中文题名"] or r["英文题名"] or "").replace("|", "/")[:40]
        journal = (r["期刊"] or "").replace("|", "/")[:20]
        year = r["年份"]
        repos = lit2repos.get(lit, [])
        if repos:
            n_with += 1
            cells = []
            for name, url, card, grade in repos:
                cells.append(f"[{name}]({url})（[档案卡](档案卡/{card}.md)）")
            repo_cell = "；".join(cells)
            grade_cell = "、".join(sorted({g for _, _, _, g in repos}))
        else:
            n_without += 1
            repo_cell = "无公开代码"
            grade_cell = "—"
        buf.write(f"| {lit} | {title} | {journal} · {year} | {repo_cell} | "
                  f"{'↑' if repos else '—'} | {grade_cell} |\n")
    buf.write(f"\n共 {len(lits)} 篇：{n_with} 篇有公开代码仓（含多仓文献），"
              f"{n_without} 篇无公开代码。\n\n")
    buf.write(f"姊妹站入口：{ATLAS_HOME} 为本站线上地址；学习站本地打开方式见上。\n")
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(buf.getvalue())
    print(f"产出 {OUT}（{n_with} 篇有仓 / {n_without} 篇无仓）")


if __name__ == "__main__":
    main()
