# -*- coding: utf-8 -*-
r"""去黑话改造·机械层：目录/文件改名 + 全库引用与链接更新 + 表头统一替换。

映射表驱动；改名用 git mv（保留历史）；替换范围=项目内全部 .md；
ITERATION_LOG 同样替换（顶部对照表保证可追溯，由本脚本写入）。
用法: python scripts/apply_plain_rename.py [--dry]
"""
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1) 物理改名（git mv）：旧相对路径 -> 新相对路径
MOVES = [
    ("02_工作流开发/范式登记册", "02_工作流开发/做法登记册"),
    ("02_工作流开发/候选流程池", "02_工作流开发/候选流程对比"),
    ("02_工作流开发/整合pipeline", "02_工作流开发/整合流程"),
    ("docs/01-基础范式主干.md", "docs/01-基础流程.md"),
    ("02_工作流开发/做法登记册/PATTERN-003_统一CLI契约多方法包装.md",
     "02_工作流开发/做法登记册/PATTERN-003_统一CLI约定多方法包装.md"),
    ("02_工作流开发/做法登记册/PATTERN-026_CellCharter_niche发现契约.md",
     "02_工作流开发/做法登记册/PATTERN-026_CellCharter_niche发现约定.md"),
    ("02_工作流开发/做法登记册/PATTERN-028_locked冻结命名纪律.md",
     "02_工作流开发/做法登记册/PATTERN-028_定稿命名规则.md"),
    ("02_工作流开发/做法登记册/PATTERN-045_管线冻结对象逐图notebook复现契约.md",
     "02_工作流开发/做法登记册/PATTERN-045_结果存盘后逐图出图的流程.md"),
    ("02_工作流开发/做法登记册/PATTERN-050_图号反查md操作手册双轨组织.md",
     "02_工作流开发/做法登记册/PATTERN-050_图号反查md操作手册并行组织.md"),
]

# 2) 文本引用替换（全库 .md；按顺序生效，长串在前）
TEXT_REPL = [
    # 目录与文件引用（含链接路径与 nav）
    ("02_工作流开发/范式登记册", "02_工作流开发/做法登记册"),
    ("02_工作流开发/候选流程池", "02_工作流开发/候选流程对比"),
    ("02_工作流开发/整合pipeline", "02_工作流开发/整合流程"),
    ("01-基础范式主干.md", "01-基础流程.md"),
    ("范式登记册", "做法登记册"),
    ("候选流程池", "候选流程对比"),
    ("整合pipeline", "整合流程"),
    ("基础范式主干", "基础流程"),
    # 卡文件名引用
    ("PATTERN-003_统一CLI契约多方法包装", "PATTERN-003_统一CLI约定多方法包装"),
    ("PATTERN-026_CellCharter_niche发现契约", "PATTERN-026_CellCharter_niche发现约定"),
    ("PATTERN-028_locked冻结命名纪律", "PATTERN-028_定稿命名规则"),
    ("PATTERN-045_管线冻结对象逐图notebook复现契约", "PATTERN-045_结果存盘后逐图出图的流程"),
    ("PATTERN-050_图号反查md操作手册双轨组织", "PATTERN-050_图号反查md操作手册并行组织"),
    # PATTERN 卡表头（46 卡统一）
    ("搬运条件：", "移植条件："),
    ("工程评价：", "质量评价："),
    ("迭代记录：", "修订记录："),
    ("| 搬运条件 |", "| 移植条件 |"),
    ("| 工程评价 |", "| 质量评价 |"),
    ("| 迭代记录 |", "| 修订记录 |"),
    # 卡类型称谓
    ("范式卡", "做法卡"),
]

COMPARISON = """## 名称变更对照表（2026-09-27 去黑话改写）

| 旧名（此前记录中的写法） | 现名 |
|---|---|
| 范式登记册 | 做法登记册 |
| 范式卡 / PATTERN 卡 | 做法卡（PATTERN-XXX 编号不变） |
| 候选流程池 | 候选流程对比 |
| 整合pipeline | 整合流程 |
| 基础范式主干（docs/01） | 基础流程 |
| PATTERN-028_locked冻结命名纪律 | PATTERN-028_定稿命名规则 |
| PATTERN-045_管线冻结对象逐图notebook复现契约 | PATTERN-045_结果存盘后逐图出图的流程 |
| PATTERN-050_图号反查md操作手册双轨组织 | PATTERN-050_图号反查md操作手册并行组织 |

以下历史条目中出现的旧名均指上表现名。

"""


def git_mv(src, dst, dry):
    s, d = os.path.join(ROOT, src), os.path.join(ROOT, dst)
    if not os.path.exists(s):
        print(f"[跳过·不存在] {src}")
        return
    if os.path.exists(d):
        print(f"[跳过·已存在] {dst}")
        return
    if dry:
        print(f"[mv] {src} -> {dst}")
        return
    r = subprocess.run(["git", "mv", src, dst], cwd=ROOT,
                       capture_output=True, text=True, encoding="utf-8")
    print(f"[mv] {src} -> {dst} ({'ok' if r.returncode == 0 else r.stderr.strip()[:80]})")


def main():
    dry = "--dry" in sys.argv
    print("=== 1. 物理改名 ===")
    for src, dst in MOVES:
        git_mv(src, dst, dry)

    print("=== 2. 全库文本替换 ===")
    n_files = 0
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "site", "03_开源项目",
                                                "05_运行环境", ".zcode", "__pycache__")]
        for f in files:
            if not f.endswith(".md"):
                continue
            p = os.path.join(base, f)
            t = open(p, encoding="utf-8").read()
            t2 = t
            for a, b in TEXT_REPL:
                t2 = t2.replace(a, b)
            if t2 != t:
                n_files += 1
                print(f"[替换] {os.path.relpath(p, ROOT)}")
                if not dry:
                    open(p, "w", encoding="utf-8").write(t2)
    print(f"替换涉及 {n_files} 个文件")

    print("=== 3. ITERATION_LOG 顶部对照表 ===")
    log = os.path.join(ROOT, "ITERATION_LOG.md")
    t = open(log, encoding="utf-8").read()
    if "名称变更对照表" not in t:
        marker = "> 记录：结构性决策、分类修订、模式升级、pipeline 版本事件。新条目加在最上面。\n\n"
        t = t.replace(marker, marker + COMPARISON, 1)
        if not dry:
            open(log, "w", encoding="utf-8").write(t)
        print("[写入] 对照表")
    else:
        print("[跳过] 对照表已存在")

    print("=== 4. 旧名残留校验 ===")
    stale = []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "site", "03_开源项目",
                                                "05_运行环境", ".zcode", "__pycache__")]
        for f in files:
            if not f.endswith(".md"):
                continue
            p = os.path.join(base, f)
            t = open(p, encoding="utf-8").read()
            for w in ("范式登记册", "候选流程池", "整合pipeline", "基础范式主干"):
                if w in t and "对照表" not in os.path.relpath(p, ROOT):
                    stale.append((os.path.relpath(p, ROOT), w))
    print("\n".join(f"  残留: {a} -> {b}" for a, b in stale) or "  旧名零残留 ✓")


if __name__ == "__main__":
    main()
