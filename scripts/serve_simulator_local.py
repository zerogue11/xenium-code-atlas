# -*- coding: utf-8 -*-
r"""决策剧场 · 本地预览服务器（含 ZXM 本地关资产注入）

背景: mkdocs.yml 已用 exclude_docs 在构建层排除 docs/simulator/assets/ZXM_local/
(课题数据红线, 保证 gh-deploy 永远不带出去)。本地要玩 ZXM 关时, 用本脚本:
  1) mkdocs build 构建站点到 site/
  2) 把 ZXM_local 资产拷进 site/simulator/assets/ZXM_local/ (仅本地副本)
  3) http.server 起本地服务 → 模拟器首页即显示 ZXM 入口"本地资产已就绪"

用法:
  C:\xenium_envs\xenium-cn-py311\Scripts\python.exe scripts\serve_simulator_local.py [--port 8765] [--no-build]
"""
import argparse
import http.server
import os
import shutil
import socketserver
import subprocess
import sys
from functools import partial
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCS_ZXM = ROOT / "docs" / "simulator" / "assets" / "ZXM_local"
SITE_ZXM = ROOT / "site" / "simulator" / "assets" / "ZXM_local"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--no-build", action="store_true", help="跳过 mkdocs build (站点已构建时)")
    args = ap.parse_args()

    if not args.no_build:
        print(">> mkdocs build …", flush=True)
        r = subprocess.run(["uvx", "--from", "mkdocs-material", "mkdocs", "build"],
                           cwd=str(ROOT), capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout[-2000:]); print(r.stderr[-2000:])
            sys.exit(1)

    if DOCS_ZXM.exists():
        if SITE_ZXM.exists():
            shutil.rmtree(SITE_ZXM)
        shutil.copytree(DOCS_ZXM, SITE_ZXM)
        print(f">> ZXM 本地资产已注入 site/ ({sum(1 for _ in SITE_ZXM.rglob('*') if _.is_file())} 个文件)", flush=True)
    else:
        print(">> 提示: docs/simulator/assets/ZXM_local/ 不存在, 先跑 scripts/precompute_simulator_zxm.py", flush=True)

    site = ROOT / "site"
    handler = partial(http.server.SimpleHTTPRequestHandler, directory=str(site))
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", args.port), handler) as httpd:
        url = f"http://127.0.0.1:{args.port}/simulator/"
        print(f">> 本地模拟器: {url}  (Ctrl+C 停止)", flush=True)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n>> 已停止", flush=True)


if __name__ == "__main__":
    main()
