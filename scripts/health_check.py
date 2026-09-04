# -*- coding: utf-8 -*-
r"""对 03_开源项目 下已克隆仓库做自动体检，产出 仓库体检表.csv 并回填主表。

体检字段：体积MB、文件数、主语言、LICENSE（无则标"仅可学习不可转载"）、env文件、
notebook数、R脚本数、最后提交时间、README摘要(<=500字)、顶层内容。
用法: python scripts/health_check.py
"""
import csv
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLONE_DIR = os.path.join(ROOT, "03_开源项目")
MASTER = os.path.join(ROOT, "01_资料库", "代码资源主表.csv")
OUT = os.path.join(ROOT, "01_资料库", "仓库体检表.csv")

LANG_MAP = {".py": "Python", ".ipynb": "Python", ".r": "R", ".rmd": "R",
            ".qmd": "R", ".jl": "Julia", ".cpp": "C++", ".cc": "C++",
            ".h": "C/C++头", ".sh": "Shell", ".m": "MATLAB", ".scala": "Scala"}
LICENSE_RE = re.compile(r"MIT|BSD|Apache|GPL|LGPL|Creative Commons|Artistic|MPL",
                        re.I)
LICENSE_NAMES = ("license", "copying", "licence", "copyright")
ENV_NAMES = ("requirements", "environment", "pyproject", "setup.py", "setup.cfg",
             "description", "dockerfile", "renv.lock", "conda.yaml", "poetry.lock")


def walk_stats(dest):
    total = nfiles = n_ipynb = 0
    langs, envs = {}, set()
    for base, dirs, files in os.walk(dest):
        if ".git" in dirs:
            dirs.remove(".git")
        for f in files:
            nfiles += 1
            try:
                total += os.path.getsize(os.path.join(base, f))
            except OSError:
                pass
            ext = os.path.splitext(f)[1].lower()
            if ext == ".ipynb":
                n_ipynb += 1
            if ext in LANG_MAP:
                langs[LANG_MAP[ext]] = langs.get(LANG_MAP[ext], 0) + 1
            low = f.lower()
            if any(low.startswith(n) or n in low for n in ENV_NAMES):
                envs.add(f)
    return total, nfiles, langs, sorted(envs), n_ipynb


def detect_license(dest, files):
    for f in files:
        low = f.lower()
        if low.startswith(LICENSE_NAMES) and os.path.isfile(os.path.join(dest, f)):
            try:
                with open(os.path.join(dest, f), encoding="utf-8", errors="replace") as fh:
                    head = fh.read(400)
                m = LICENSE_RE.search(head)
                return m.group(0).upper() if m else "自定义LICENSE(需人工核)"
            except OSError:
                return "LICENSE存在(读取失败)"
    return "无LICENSE(仅可学习不可转载)"


def read_readme(dest):
    for f in os.listdir(dest):
        if f.lower().startswith("readme"):
            try:
                with open(os.path.join(dest, f), encoding="utf-8", errors="replace") as fh:
                    text = fh.read(4000)
            except OSError:
                return ""
            lines = [ln.strip() for ln in text.splitlines()
                     if ln.strip() and not ln.strip().startswith(("<img", "[!["))]
            words = " ".join(lines)
            words = re.sub(r"[#*`>|]", "", words)
            return words[:500]
    return "(无README)"


def git_log(dest):
    r = subprocess.run(["git", "-C", dest, "log", "-1", "--format=%ci"],
                       capture_output=True, text=True, timeout=30)
    return (r.stdout or "").strip()[:19]


def main():
    with open(MASTER, encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    out_rows = []
    for r in rows:
        dest = os.path.join(CLONE_DIR, f"{r['owner']}__{r['repo']}")
        if not os.path.isdir(os.path.join(dest, ".git")):
            out_rows.append({"repo": f"{r['owner']}/{r['repo']}", "状态": "未克隆"})
            continue
        files = os.listdir(dest)
        total, nfiles, langs, envs, n_ipynb = walk_stats(dest)
        lang_str = "/".join(f"{k}x{v}" for k, v in
                            sorted(langs.items(), key=lambda x: -x[1])[:3]) or "非代码"
        license_s = detect_license(dest, files)
        top = ",".join(files[:12])
        rec = {"repo": f"{r['owner']}/{r['repo']}", "状态": "已克隆",
               "体积MB": round(total / 1048576, 1), "文件数": nfiles,
               "主语言": lang_str, "LICENSE": license_s,
               "env文件": ";".join(envs)[:200],
               "notebook数": n_ipynb,
               "最后提交": git_log(dest), "README摘要": read_readme(dest),
               "顶层内容": top}
        out_rows.append(rec)
        r["LICENSE"], r["主语言"], r["体积MB"] = license_s, lang_str, str(rec["体积MB"])

    cols = ["repo", "状态", "体积MB", "文件数", "主语言", "LICENSE", "env文件",
            "notebook数", "最后提交", "README摘要", "顶层内容"]
    with open(OUT, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for rec in out_rows:
            w.writerow({c: rec.get(c, "") for c in cols})
    with open(MASTER, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    ok = sum(1 for r in out_rows if r["状态"] == "已克隆")
    no_lic = sum(1 for r in out_rows if r.get("LICENSE", "").startswith("无"))
    print(f"体检完成: {ok}/{len(out_rows)} 已克隆；无LICENSE {no_lic} 仓")
    big = sorted((r for r in out_rows if r.get("体积MB")), key=lambda x: -x["体积MB"])[:5]
    print("体积TOP5:", [(r["repo"], r["体积MB"]) for r in big])


if __name__ == "__main__":
    main()
