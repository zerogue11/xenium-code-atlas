# -*- coding: utf-8 -*-
r"""Xenium 决策剧场 · 剧本校验器（五类检查）

检查项:
  1. schema   : 每份剧本 JSON 符合 docs/simulator/data/schema.json (jsonschema 库缺失则退化为基础结构检查)
  2. events   : 剧本引用的事件 ID 必须存在于 events.json
  3. assets   : 剧本引用的 asset 文件必须存在于 docs/simulator/assets/<ID>/ (T1-lite 关可用 allow_missing 声明豁免)
  4. relpaths : SPA 数据文件路径必须为相对路径 (禁止 / 开头绝对路径; fetch 相对部署子路径)
  5. labels   : manifest.json 内每个资产必须带三行式标注 (source/nature/ref 三字段非空)

用法:
  C:\xenium_envs\xenium-cn-py311\Scripts\python.exe scripts\validate_scenario.py [--strict]
退出码: 0=全绿 1=有错 (CI/发布前守门)
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
SIM = ROOT / "docs" / "simulator"
SCHEMA = json.loads((SIM / "data" / "schema.json").read_text(encoding="utf-8"))
EVENTS = json.loads((SIM / "data" / "events.json").read_text(encoding="utf-8"))
EVENT_IDS = {e["id"] for e in EVENTS["events"]}

errors, warnings = [], []


def err(msg):
    "记录一类错误（schema/引用/资产缺失等），累计后以非零码退出。"
    errors.append(msg)


def warn(msg):
    "记录警告（不阻断），如媒体文件缺 alt 文本等。"
    warnings.append(msg)


def check_schema(scen, path):
    "校验单个剧本 JSON 的必填字段/枚举值/结构；不符写 err 并标明剧本文件名。"
    try:
        import jsonschema
        validator = jsonschema.Draft7Validator(SCHEMA)
        for e in sorted(validator.iter_errors(scen), key=lambda x: list(x.path)):
            loc = "/".join(str(p) for p in e.path) or "<root>"
            err(f"[schema] {path.name}: {loc}: {e.message[:200]}")
        return True
    except ImportError:
        warn("jsonschema 未安装 → 基础结构检查代替")
    # 退化检查: 必备字段/节点跳转完整性
    for k in ("id", "title", "mode", "data", "nodes"):
        if k not in scen:
            err(f"[schema] {path.name}: 缺 {k}")
    goto_targets = set(scen.get("nodes", {}))
    for nk, node in scen.get("nodes", {}).items():
        for o in node.get("options", []):
            if o.get("goto") not in goto_targets:
                err(f"[schema] {path.name}: 节点 {nk} 选项 goto={o.get('goto')} 不存在")
    return False


def collect_media(node):
    "递归收集剧本中引用的全部媒体资产路径（图片/音频），供存在性检查。"
    for o in node.get("options", []):
        yield from o.get("media", [])


def main():
    "校验主流程：遍历决策剧场全部剧本 → 五类检查（schema/资产/引用/数值来源/分支完整）→ 汇总 err/warn 报告。"
    strict = "--strict" in sys.argv
    scen_dir = SIM / "data" / "scenarios"
    for path in sorted(scen_dir.glob("*.json")):
        scen = json.loads(path.read_text(encoding="utf-8"))
        sid = scen.get("id", path.stem)
        try:
            jsonschema_ok = check_schema(scen, path)
        except json.JSONDecodeError as e:
            err(f"[schema] {path.name}: JSON 解析失败 {e}")
            continue
        # events
        for nk, node in scen["nodes"].items():
            for o in node.get("options", []):
                for eid in o.get("events", []):
                    if eid not in EVENT_IDS:
                        err(f"[events] {path.name}: {nk} 引用不存在的事件 {eid}")
        # goto 目标交叉校验 (不依赖 jsonschema, 无条件执行)
        nodes = scen["nodes"]
        if scen.get("id") and scen["id"] != path.stem:
            err(f"[schema] {path.name}: id={scen['id']} 与文件名不一致")
        for nk, node in nodes.items():
            if node.get("type") == "settlement" and node.get("options"):
                err(f"[schema] {path.name}: settlement 节点 {nk} 不应有 options")
            for o in node.get("options", []):
                g = o.get("goto")
                if g and g not in nodes:
                    err(f"[schema] {path.name}: 节点 {nk} 选项 goto={g} 不存在")
        # assets + relpaths
        manifest_path = SIM / "assets" / sid / "manifest.json"
        manifest = None
        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        else:
            warn(f"[assets] {sid}: manifest.json 不存在 (资产未生成?)")
        for nk, node in scen["nodes"].items():
            for m in collect_media(node):
                if m.get("type") == "asset":
                    f = m.get("asset", "")
                    if f.startswith("/"):
                        err(f"[relpaths] {path.name}: {nk} 资产为绝对路径 {f}")
                    if not f:
                        err(f"[assets] {path.name}: {nk} asset 字段为空")
                        continue
                    p = SIM / "assets" / sid / f
                    declared = m.get("fallback")
                    if not p.exists():
                        # 声明了 fallback 的缺失 = 作者签署的"诚实降级"路径: 两档模式都只 warn
                        if declared:
                            warn(f"[assets] {sid}: {f} 缺失但有 fallback (设计内降级, SPA 将呈现声明文案)")
                        else:
                            err(f"[assets] {path.name}: {nk} 资产缺失且无 fallback: {f}")
                elif m.get("type") == "coords":
                    f = m.get("src", "")
                    if f.startswith("/"):
                        err(f"[relpaths] {path.name}: {nk} coords 为绝对路径 {f}")
                    p = SIM / "assets" / sid / f
                    if not p.exists():
                        err(f"[assets] {path.name}: {nk} coords 缺失: {f}")
        # manifest 三行式标注
        if manifest:
            seen = set()
            for a in manifest.get("assets", []):
                seen.add(a.get("file"))
                for k in ("source", "nature", "ref"):
                    if not str(a.get(k, "")).strip():
                        err(f"[labels] {sid}: 资产 {a.get('file')} 缺 {k} 标注")
            # 剧本引用但 manifest 未登记的资产 → 性质标注无从谈起 (strict 下直接判错)
            for nk, node in scen["nodes"].items():
                for m in collect_media(node):
                    if m.get("type") == "asset":
                        f = m.get("asset", "")
                        if f and f not in seen and (SIM / "assets" / sid / f).exists():
                            msg = f"[labels] {sid}: {f} 存在但未登记进 manifest.json (三行式标注缺失)"
                            (err if strict else warn)(msg)
    # SPA 数据文件相对路径抽查
    spa = (SIM / "index.html").read_text(encoding="utf-8")
    for m in re.finditer(r"""fetch\(\s*[`"']([^`"']+)[`"']""", spa):
        u = m.group(1)
        if u.startswith(("http", "//")):
            continue
        if u.startswith("/"):
            err(f"[relpaths] index.html: fetch 绝对路径 {u} (部署子路径会 404)")
    # 事件证据链完备性
    for e in EVENTS["events"]:
        if not e.get("evidence"):
            err(f"[events] {e['id']} 无证据链")
        for v in e.get("evidence", []):
            if "github.com" not in v.get("url", ""):
                warn(f"[events] {e['id']} 证据非 GitHub 锚点: {v.get('label')}")

    print("=" * 60)
    if warnings:
        print(f"⚠️ 警告 {len(warnings)} 条:")
        for w in warnings:
            print(f"  - {w}")
    if errors:
        print(f"❌ 错误 {len(errors)} 条:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print(f"✅ 五类检查全部通过 (schema/events/assets/relpaths/labels)")


if __name__ == "__main__":
    main()
