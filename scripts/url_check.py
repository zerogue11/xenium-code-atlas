# -*- coding: utf-8 -*-
r"""周检脚本：核验代码资源主表 72 仓 URL 存活（GitHub Actions 定时任务用，也可本地跑）。

- 只用标准库（urllib），无第三方依赖，方便 CI 直接跑。
- 失败判定：连接错误 / 404 / 5xx；403/429 记"疑似反爬"不计失败（v2 核验经验：10x 官网常态 429）。
- 输出：markdown 报告到 --report 指定路径（供 $GITHUB_STEP_SUMMARY / artifact）。
- 退出码：失败数 >0 时 exit 1（供 workflow 的 issue 步骤 if: failure() 触发）。
用法: python scripts/url_check.py --report report.md
"""
import argparse
import csv
import io
import os
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTER = os.path.join(ROOT, "01_资料库", "代码资源主表.csv")
UA = "Mozilla/5.0 (xenium-code-atlas weekly-check)"  # 部分站点拒默认 UA
TIMEOUT = 20
WORKERS = 8


def check(url: str):
    """HEAD 优先，405/403 时降级 GET；返回 (url, 状态分类, 详情)。"""
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method,
                                         headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return url, "ok", f"HTTP {resp.status}"
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code in (405, 403):
                continue  # 换 GET 再试
            if e.code in (403, 429):
                return url, "ratelimit", f"HTTP {e.code}（疑似反爬/限流，不计失败）"
            return url, "fail", f"HTTP {e.code}"
        except Exception as e:  # 连接错误/DNS/超时
            return url, "fail", f"{type(e).__name__}: {e}"
    return url, "ratelimit", "HEAD 被拒且 GET 异常"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", default="report.md", help="markdown 报告输出路径")
    args = ap.parse_args()

    with open(MASTER, encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    targets = [(f"{r['owner']}/{r['repo']}", r["URL"]) for r in rows]

    results = []
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for (repo, url), (rurl, status, detail) in zip(
                targets, ex.map(lambda t: check(t[1]), targets)):
            results.append((repo, url, status, detail))

    fails = [r for r in results if r[2] == "fail"]
    limits = [r for r in results if r[2] == "ratelimit"]
    oks = [r for r in results if r[2] == "ok"]

    buf = io.StringIO()
    buf.write(f"# 代码资源周检报告（{len(results)} 仓）\n\n")
    buf.write(f"- ✅ 可访问: {len(oks)}\n- ⚠️ 疑似反爬(不计失败): {len(limits)}\n- ❌ 失败: {len(fails)}\n")
    if fails:
        buf.write("\n## 失败清单\n\n| 仓库 | URL | 详情 |\n|---|---|---|\n")
        for repo, url, _, detail in fails:
            buf.write(f"| {repo} | {url} | {detail} |\n")
    if limits:
        buf.write("\n## 疑似反爬清单（人工复核，非失败）\n\n| 仓库 | 详情 |\n|---|---|\n")
        for repo, _, _, detail in limits:
            buf.write(f"| {repo} | {detail} |\n")
    buf.write("\n> 判定规则：连接错误/404/5xx=失败；403/429=疑似反爬仅提示。修复后更新主表与档案卡。\n")
    with open(args.report, "w", encoding="utf-8") as fh:
        fh.write(buf.getvalue())
    print(f"ok={len(oks)} ratelimit={len(limits)} fail={len(fails)} -> {args.report}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
