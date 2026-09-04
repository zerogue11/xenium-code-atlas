# -*- coding: utf-8 -*-
r"""从 v2 资源核验表派生代码资源主表 / 附属表 / 文献速查表。

种子数据（只读）:
  F:\我的科研\xenium-knowledge-tree\01_资料库\资源明细_v2_核验.csv
  F:\我的科研\xenium-knowledge-tree\01_资料库\extract\LIT-*.json
产出:
  01_资料库/代码资源主表.csv   72 仓去重主表
  01_资料库/代码资源附属表.csv Zenodo/网页等非 GitHub 代码资源
  01_资料库/文献速查表.csv     91 篇文献 LIT-ID -> 题名/期刊/方法工具
用法: python scripts/build_master_table.py
"""
import csv
import json
import os
import re
import sys
from collections import OrderedDict

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEED_DIR = r"F:\我的科研\xenium-knowledge-tree\01_资料库"
SEED_CSV = os.path.join(SEED_DIR, "资源明细_v2_核验.csv")
EXTRACT_DIR = os.path.join(SEED_DIR, "extract")
OUT_DIR = os.path.join(ROOT, "01_资料库")

# 核验表列（位置索引，表头有重复列名故不用 DictReader）
COL = {"lit": 0, "cat": 1, "src": 2, "acc": 3, "verify_url": 6, "http": 7,
       "status": 8, "detail": 10}

MASTER_COLS = ["文献IDs", "主分类初判", "owner", "repo", "URL", "验证状态", "HTTP",
               "精选级", "克隆状态", "锁定SHA", "默认分支", "LICENSE", "主语言",
               "体积MB", "运行入口", "备注"]
SUB_COLS = ["文献ID", "来源类型", "accession或URL", "核验URL", "验证状态", "HTTP详情", "备注"]
LIT_COLS = ["文献ID", "中文题名", "英文题名", "期刊", "年份", "方法工具", "公开代码URL数"]

GITHUB_RE = re.compile(r"github\.com/([^/\s]+)/([^/\s?#]+)", re.I)

# 主分类初判：关键词作用于 owner/repo 小写字符串，按顺序首个命中生效
CLASS_RULES = [
    ("P0", ["benchmark", "comparison", "compare", "spatialqm", "ist_benchmarking",
            "quality", "preprocess", "postprocess", "decoding"]),
    ("P1", ["mushroom", "hover", "segment", "nuclei", "membrane", "morph",
            "iss_patcher"]),
    ("P2", ["atlas", "ecotyper", "typist", "annot"]),
    ("P3", ["niche", "domain", "community", "spatch", "ecosystem"]),
    ("P4", ["cellchat", "communic", "ligand", "interaction", "crosstalk"]),
    ("P5", ["drug2cell", "snp2cell", "subcell", "bento", "rnaloc", "spatial_loc"]),
    ("P6", ["3d", "mapping", "register", "align", "spatial_pf"]),
    ("P7", ["image", "histopath", "multiplex", "codex", "imaging", "pseudo"]),
    ("P8", []),
]


def classify(name: str) -> str:
    low = name.lower()
    for cls, kws in CLASS_RULES:
        if not kws:
            continue
        for kw in kws:
            if kw in low:
                return cls
    return "P8"


def clean_repo(url: str):
    """从 URL 提取 (owner, repo)；无法解析返回 None。"""
    m = GITHUB_RE.search(url or "")
    if not m:
        return None
    owner, repo = m.group(1), m.group(2)
    repo = re.sub(r"\.git$", "", repo, flags=re.I)
    repo = re.sub(r"[^\w.\-]", "", repo)  # 去掉混入的中文括号备注等
    if not owner or not repo:
        return None
    return owner, repo


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    with open(SEED_CSV, encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.reader(fh))
    rows = rows[1:]  # 表头

    code_rows = [r for r in rows if len(r) > COL["cat"] and r[COL["cat"]] == "代码/工具"]
    print(f"代码/工具类资源: {len(code_rows)} 条")

    repos = OrderedDict()   # (owner,repo_lower) -> dict
    sub_rows = []
    n_gh = 0
    for r in code_rows:
        url = (r[COL["verify_url"]] or "").strip() or (r[COL["acc"]] or "").strip()
        lit = r[COL["lit"]]
        status = r[COL["status"]]
        detail = r[COL["detail"]]
        parsed = clean_repo(url) if "github.com" in url.lower() else None
        if parsed:
            n_gh += 1
            owner, repo = parsed
            key = (owner.lower(), repo.lower())
            if key not in repos:
                repos[key] = {
                    "owner": owner, "repo": repo, "URL": f"https://github.com/{owner}/{repo}",
                    "lits": [], "statuses": set(), "初判": classify(f"{owner}/{repo}"),
                }
            if lit not in repos[key]["lits"]:
                repos[key]["lits"].append(lit)
            repos[key]["statuses"].add(status)
        else:
            note = "" if parsed else ("非仓库GitHub链接" if "github.com" in url.lower() else "")
            sub_rows.append([lit, "GitHub" if "github.com" in url.lower() else r[COL["src"]],
                             r[COL["acc"]], url, status, detail, note])

    print(f"GitHub 仓库行: {n_gh} 条 -> 去重 {len(repos)} 仓")

    master_path = os.path.join(OUT_DIR, "代码资源主表.csv")
    with open(master_path, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(MASTER_COLS)
        for key in sorted(repos, key=lambda k: (min(repos[k]["lits"]), k[0])):
            info = repos[key]
            w.writerow([";".join(info["lits"]), info["初判"], info["owner"], info["repo"],
                        info["URL"], "/".join(sorted(info["statuses"])), 200,
                        "待定", "待克隆", "", "", "", "", "", "", ""])
    print(f"主表 -> {master_path}")

    sub_path = os.path.join(OUT_DIR, "代码资源附属表.csv")
    with open(sub_path, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(SUB_COLS)
        w.writerows(sub_rows)
    print(f"附属表 -> {sub_path}（{len(sub_rows)} 条）")

    # 文献速查表
    lit_rows = []
    if os.path.isdir(EXTRACT_DIR):
        for fn in sorted(os.listdir(EXTRACT_DIR)):
            if not fn.endswith(".json"):
                continue
            with open(os.path.join(EXTRACT_DIR, fn), encoding="utf-8") as jf:
                d = json.load(jf)
            lit_rows.append([
                d.get("文献ID", fn[:-5]), d.get("中文题名", ""), d.get("英文题名", ""),
                d.get("期刊", ""), d.get("年份", ""),
                ";".join(d.get("方法工具", []) if isinstance(d.get("方法工具"), list)
                         else [str(d.get("方法工具", ""))]),
                len(re.findall(r"https?://\S+", str(d.get("公开代码资源", "")))),
            ])
    lit_path = os.path.join(OUT_DIR, "文献速查表.csv")
    with open(lit_path, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(LIT_COLS)
        w.writerows(lit_rows)
    print(f"文献速查表 -> {lit_path}（{len(lit_rows)} 篇）")

    # 分类分布速览
    from collections import Counter
    dist = Counter(v["初判"] for v in repos.values())
    print("主分类初判分布:", dict(sorted(dist.items())))


if __name__ == "__main__":
    main()
