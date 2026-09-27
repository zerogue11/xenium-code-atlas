# -*- coding: utf-8 -*-
r"""独立审核·事实元素硬对比：改写前后逐文件提取不该变的内容并求差集。

对比对象（git 内容级，非工作区）：
  BEFORE = e429399^（去黑话改写提交的父）
  AFTER  = HEAD
提取四类元素：数字序列、反引号内路径/文件名、markdown 链接 URL、代码块（要求逐块一致）；
另比对每个文件的 markdown 表格行数序列。
改名文件按 MOVES 映射对齐前后路径；输出差集报告供人工/agent 复核。
用法: python scripts/audit_rewrite.py
"""
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BEFORE, AFTER = "e429399^", "HEAD"

# 改名对齐（旧路径 -> 新路径）
MOVES = {
    "02_工作流开发/范式登记册": "02_工作流开发/做法登记册",
    "02_工作流开发/候选流程池": "02_工作流开发/候选流程对比",
    "02_工作流开发/整合pipeline": "02_工作流开发/整合流程",
    "docs/01-基础范式主干.md": "docs/01-基础流程.md",
    "02_工作流开发/范式登记册/PATTERN-003_统一CLI契约多方法包装.md":
        "02_工作流开发/做法登记册/PATTERN-003_统一CLI约定多方法包装.md",
    "02_工作流开发/范式登记册/PATTERN-026_CellCharter_niche发现契约.md":
        "02_工作流开发/做法登记册/PATTERN-026_CellCharter_niche发现约定.md",
    "02_工作流开发/范式登记册/PATTERN-028_locked冻结命名纪律.md":
        "02_工作流开发/做法登记册/PATTERN-028_定稿命名规则.md",
    "02_工作流开发/范式登记册/PATTERN-045_管线冻结对象逐图notebook复现契约.md":
        "02_工作流开发/做法登记册/PATTERN-045_结果存盘后逐图出图的流程.md",
    "02_工作流开发/范式登记册/PATTERN-050_图号反查md操作手册双轨组织.md":
        "02_工作流开发/做法登记册/PATTERN-050_图号反查md操作手册并行组织.md",
}
# 精改文件（前后同路径）
FILES = [
    "docs/index.md", "docs/00-开始这里.md", "docs/01-基础流程.md",
    "docs/02-高级模块地图.md", "docs/03-精读方法论.md", "docs/04-实操测试计划.md",
    "docs/05-项目治理.md", "docs/06-决策剧场指南.md", "docs/07-绘图与呈现.md",
    "02_工作流开发/高级模块/README.md", "02_工作流开发/整合流程/README.md",
    "02_工作流开发/候选流程对比/README.md",
    "02_工作流开发/候选流程对比/官方线_官方教程中文优化.md",
    "02_工作流开发/候选流程对比/OV线_WSL_strict_GPU.md",
    "02_工作流开发/做法登记册/README.md", "02_工作流开发/场景路线/README.md",
    "02_工作流开发/绘图呈现/README.md",
    "01_资料库/分类分析报告_一期.md", "01_资料库/迭代入库SOP.md",
    "01_资料库/生态与官方资源.md",
    "02_工作流开发/做法登记册/PATTERN-045_结果存盘后逐图出图的流程.md",
    "02_工作流开发/做法登记册/PATTERN-050_图号反查md操作手册并行组织.md",
    "02_工作流开发/绘图呈现/V-20_机制流程示意图.md",
]


def git_show(rev, path):
    r = subprocess.run(["git", "show", f"{rev}:{path}"], cwd=ROOT,
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    return r.stdout if r.returncode == 0 else None


def old_path(new_path):
    # 最长新路径优先，避免目录级映射截胡具体文件映射
    for o, n in sorted(MOVES.items(), key=lambda kv: -len(kv[1])):
        if new_path == n or new_path.startswith(n + "/"):
            return new_path.replace(n, o, 1)
    return new_path


NUM = re.compile(r"\d+(?:\.\d+)?%?")
BACKTICK = re.compile(r"`([^`\n]+)`")
LINK = re.compile(r"\]\(([^)\s]+)\)")
CODE = re.compile(r"```[^\n]*\n(.*?)```", re.S)
TABLE_ROWS = re.compile(r"^\|.*\|$", re.M)


def elements(text):
    return {
        "num": sorted(NUM.findall(text)),
        "bt": sorted(BACKTICK.findall(text)),
        "link": sorted(LINK.findall(text)),
        "code": CODE.findall(text),
        "trow": TABLE_ROWS.findall(text),
    }


def multiset_diff(old_list, new_list):
    """返回 (old 独有, new 独有)。"""
    from collections import Counter
    co, cn = Counter(old_list), Counter(new_list)
    gone = list((co - cn).elements())
    added = list((cn - co).elements())
    return gone, added


def main():
    report = []
    for new_path in FILES:
        old_path_p = old_path(new_path)
        old_t = git_show(BEFORE, old_path_p)
        new_t = git_show(AFTER, new_path)
        if old_t is None:
            report.append(f"[!] BEFORE 无文件: {old_path_p}")
            continue
        if new_t is None:
            report.append(f"[!] AFTER 无文件: {new_path_p}")
            continue
        oe, ne = elements(old_t), elements(new_t)
        issues = []
        # 代码块：逐块一致（硬校验）
        if oe["code"] != ne["code"]:
            gone, added = multiset_diff(oe["code"], ne["code"])
            issues.append(f"代码块变化 {len(gone)} 消失/{len(added)} 新增")
            for g in gone[:3]:
                issues.append("  [代码消失] " + g.strip().replace("\n", " ")[:100])
            for a in added[:3]:
                issues.append("  [代码新增] " + a.strip().replace("\n", " ")[:100])
        # 表格行数
        if len(oe["trow"]) != len(ne["trow"]):
            issues.append(f"表格行数 {len(oe['trow'])} -> {len(ne['trow'])}")
        # 链接（路径改名造成的有意变化需人工确认，全列出让 agent 判）
        lg, la = multiset_diff(oe["link"], ne["link"])
        if lg:
            issues.append(f"链接消失 {len(lg)}: " + "; ".join(lg[:6]))
        if la:
            issues.append(f"链接新增 {len(la)}: " + "; ".join(la[:6]))
        # 反引号内容（路径/文件名/命令；名称改动的有意变化会出现在这里）
        bg, ba = multiset_diff(oe["bt"], ne["bt"])
        # 过滤：反引号差异中，纯名称映射相关的归为"预期"
        expect = {"范式登记册", "候选流程池", "整合pipeline", "基础范式主干"}
        bg_suspect = [x for x in bg if not any(e in x for e in expect)]
        ba_suspect = [x for x in ba if not any(e in x for e in expect)]
        if bg_suspect:
            issues.append(f"反引号消失(可疑) {len(bg_suspect)}: " + "; ".join(bg_suspect[:8]))
        if ba_suspect:
            issues.append(f"反引号新增(可疑) {len(ba_suspect)}: " + "; ".join(ba_suspect[:8]))
        # 数字
        ng, na = multiset_diff(oe["num"], ne["num"])
        if ng:
            issues.append(f"数字消失 {len(ng)}: " + ", ".join(ng[:15]))
        if na:
            issues.append(f"数字新增 {len(na)}: " + ", ".join(na[:15]))
        if issues:
            report.append(f"== {new_path}")
            report.extend("  " + i for i in issues)
    out = "\n".join(report) or "全部文件事实元素无差异"
    print(out)
    with open(os.path.join(ROOT, "interim_硬对比审计.txt"), "w", encoding="utf-8") as fh:
        fh.write(out)


if __name__ == "__main__":
    main()
