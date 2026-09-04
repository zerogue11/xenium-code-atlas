# -*- coding: utf-8 -*-
r"""全量浅克隆主表中的 72 仓到 03_开源项目/<owner>__<repo>，锁定 SHA 与默认分支。

- 断点续跑：已存在 .git 的目录只补 SHA/分支，不重复克隆。
- 失败自动用镜像前缀 https://ghfast.top/ 重试一次。
- 结束后回写 代码资源主表.csv 并输出 clone_log.csv。
用法: python scripts/clone_all.py [--workers 6]
"""
import csv
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTER = os.path.join(ROOT, "01_资料库", "代码资源主表.csv")
CLONE_DIR = os.path.join(ROOT, "03_开源项目")
MIRROR = "https://ghfast.top/"
LOG = os.path.join(ROOT, "01_资料库", "clone_log.csv")

GIT_ENV = dict(os.environ, GIT_TERMINAL_PROMPT="0", GIT_LFS_SKIP_SMUDGE="1")
# 全局 git 配置了 http.proxy=127.0.0.1:7890（Clash 类），代理未开时 git 全挂。
# 克隆命令一律先临时覆盖为直连（不动用户全局配置），失败再退回全局配置。
GIT_OVERRIDE = ["-c", "http.proxy=", "-c", "https.proxy="]


def run(args, timeout=900, override=True):
    cmd = ["git", *(GIT_OVERRIDE if override else []), *args]
    return subprocess.run(cmd, env=GIT_ENV, timeout=timeout,
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace")


def clone_one(row):
    url, owner, repo = row["URL"], row["owner"], row["repo"]
    dest = os.path.join(CLONE_DIR, f"{owner}__{repo}")
    t0 = time.time()
    if os.path.isdir(os.path.join(dest, ".git")):
        method = "已存在"
    else:
        attempts = [("直连", url, True), ("全局代理", url, False),
                    ("镜像ghfast", MIRROR + url, True)]
        method = "失败"
        r = None
        for method, u, ov in attempts:
            r = run(["clone", "--depth", "1", "--single-branch", u, dest],
                    override=ov)
            if r.returncode == 0:
                break
            subprocess.run(["rmdir", "/s", "/q", dest], capture_output=True,
                           shell=True)
        if r.returncode != 0:
            err = (r.stderr or "").strip().splitlines()
            return row, {"status": f"失败: {err[-1][:120] if err else 'unknown'}",
                         "sha": "", "branch": "", "method": "失败",
                         "secs": round(time.time() - t0, 1)}
    sha_r = run(["git", "-C", dest, "rev-parse", "HEAD"], 60)
    br_r = run(["git", "-C", dest, "symbolic-ref", "--short", "HEAD"], 60)
    return row, {"status": "已克隆", "sha": (sha_r.stdout or "").strip(),
                 "branch": (br_r.stdout or "").strip(), "method": method,
                 "secs": round(time.time() - t0, 1)}


def main():
    workers = 6
    if "--workers" in sys.argv:
        workers = int(sys.argv[sys.argv.index("--workers") + 1])
    os.makedirs(CLONE_DIR, exist_ok=True)
    with open(MASTER, encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    print(f"待处理 {len(rows)} 仓，workers={workers}", flush=True)

    results, log = {}, []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(clone_one, r): r for r in rows}
        for i, fut in enumerate(as_completed(futs), 1):
            row, res = fut.result()
            results[(row["owner"], row["repo"])] = res
            log.append([f"{row['owner']}/{row['repo']}", res["status"],
                        res["method"], res["secs"]])
            print(f"[{i}/{len(rows)}] {row['owner']}/{row['repo']} -> "
                  f"{res['status']} ({res['method']}, {res['secs']}s)", flush=True)

    for r in rows:
        res = results[(r["owner"], r["repo"])]
        r["克隆状态"], r["锁定SHA"], r["默认分支"] = res["status"], res["sha"], res["branch"]
        if res["method"] == "镜像ghfast":
            r["备注"] = (r["备注"] + ";" if r["备注"] else "") + "经镜像克隆"

    with open(MASTER, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    with open(LOG, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["repo", "status", "method", "seconds"])
        w.writerows(log)

    ok = sum(1 for v in results.values() if v["status"] == "已克隆")
    print(f"完成: 成功 {ok}/{len(rows)}", flush=True)


if __name__ == "__main__":
    main()
