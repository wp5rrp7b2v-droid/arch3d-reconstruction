#!/usr/bin/env python3
# AUTO-SYNC CONTRACT: derived Dashboard V2 from canonical project sources.
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "docs/project_control/project_state.json"
REG = ROOT / "docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json"
CATALOG = ROOT / "production/zhenguo_wanfo/registry/P3_3_STAGE1_COMPONENT_MASTER_LIBRARY_V001.json"
MATRIX = ROOT / "production/zhenguo_wanfo/registry/P3_3_STAGE1_MASTER_COVERAGE_DISPOSITION_MATRIX_V002.json"
OUT = ROOT / "docs/project_control/dashboard.html"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

state = load(STATE)
reg = load(REG)
catalog = load(CATALOG)
matrix = load(MATRIX)

progress = reg["stage1_master_progress_summary"]
approved = list(progress["approved_master_components"])
approved_set = set(approved)
scope = [row for row in matrix["rows"] if "Master" in str(row.get("disposition", ""))]
assert len(scope) == progress["master_scope_object_type_count"]
assert progress["approved_master_count"] == catalog["approved_master_count"]
pending = [row for row in scope if row["component"] not in approved_set]
pending = sorted(pending, key=lambda row: (999 if row.get("priority") is None else row["priority"], row["component"]))
next_target = pending[0]["component"] if pending else "NONE"
next_batch = [row["component"] for row in pending if (row.get("priority") or 999) <= 14]
later_batch = [row["component"] for row in pending if (row.get("priority") or 999) >= 15]

def chips(values, cls):
    return "".join('<span class="chip %s">%s</span>' % (cls, escape(v)) for v in values)

stages = [
    ("01","真实构件 Master 库","ACTIVE","%s / %s · %s%%" % (progress["approved_master_count"], progress["master_scope_object_type_count"], progress["master_completion_percent"])),
    ("02","构件变体与装配接口","NOT STARTED",""),
    ("03","代表性组合验证","NOT STARTED",""),
    ("04","整殿真实实例与拓扑","NOT STARTED",""),
    ("05","空间定位与标高规则","NOT STARTED",""),
    ("06","确定性整殿生成","NOT STARTED","T-018 在此重新决策"),
    ("07","整殿验收与 Gate Closure","NOT STARTED","")
]
stage_html = ""
for number, name, status, note in stages:
    cls = "stage active" if status == "ACTIVE" else "stage"
    detail = status + (("<br>" + escape(note)) if note else "")
    stage_html += '<div class="%s"><div class="stage-num">%s</div><strong>%s</strong><div class="small">%s</div></div>' % (cls, number, escape(name), detail)

pct = progress["master_completion_percent"]
last = state.get("last_completed_task", {})
pending_sources = reg.get("pending_source_binding", [])

html = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>中国古建筑3D复原｜Project Dashboard V2</title>
<style>
:root{--bg:#f3efe7;--paper:#fffdf8;--ink:#2b241f;--muted:#776b61;--line:#ded4c6;--red:#8b3428;--green:#376b48;--amber:#9a6a18;--soft:#eee7dc;--softgreen:#edf4ee;--softred:#f8eee7}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif}
main{max-width:1180px;margin:auto;padding:24px}.card{background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:20px;margin-bottom:16px;box-shadow:0 1px 0 rgba(0,0,0,.025)}
.grid{display:grid;grid-template-columns:1.2fr .8fr;gap:16px}.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.eyebrow{font-size:12px;font-weight:800;letter-spacing:.06em;color:var(--red)}
h1{font-size:30px;margin:8px 0 4px}h2{font-size:19px;margin:0 0 14px}h3{font-size:15px;margin:0 0 8px}.muted,.small{color:var(--muted)}.small{font-size:12px;line-height:1.5}
.statusline,.chips{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}.pill,.chip{padding:7px 10px;border-radius:999px;font-size:12px;font-weight:750;background:var(--soft)}.ok{color:var(--green)}.hold{color:var(--red)}.warn{color:var(--amber)}
.journey{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:18px}.node{border:1px solid var(--line);background:#faf7f1;border-radius:12px;padding:10px 12px;font-size:12px}.node.done{background:var(--softgreen);color:#315b3d}.node.active{background:var(--softred);border:2px solid #caa797;color:#6f3429}.arrow{color:#a39689;font-weight:700}
.stages{display:grid;grid-template-columns:repeat(7,1fr);gap:8px}.stage{min-height:94px;border:1px solid var(--line);border-radius:12px;padding:11px;background:#faf7f1}.stage.active{border:2px solid #8a5b47;background:var(--softred)}.stage-num{font-size:12px;color:var(--muted);margin-bottom:8px}.stage strong{font-size:13px}
.big{font-size:38px;font-weight:800;line-height:1}.progress{height:14px;background:#e6ded2;border-radius:999px;overflow:hidden;margin:12px 0 8px}.progress div{height:100%%;background:#4d7658}
.metric{padding:14px;border:1px solid var(--line);border-radius:13px;background:#faf7f1}.metric b{display:block;font-size:25px;margin-bottom:3px}.callout{border-left:4px solid var(--red);padding:12px 14px;background:var(--softred);border-radius:8px}.callout.okbox{border-left-color:var(--green);background:var(--softgreen)}
.kv{display:grid;grid-template-columns:145px 1fr;gap:8px;font-size:13px;line-height:1.45}.kv div:nth-child(odd){color:var(--muted)}.chip.done{background:#e6f0e8;color:#315b3d}.chip.next{background:#f3dfd2;color:#7a3327}.chip.future{background:#eee9e1;color:#625a52}
.batch{padding:12px 0;border-top:1px solid var(--line)}.batch:first-of-type{border-top:0;padding-top:0}.note{border:1px dashed #cfc2b4;border-radius:12px;padding:12px;background:#faf7f1}.footer{font-size:11px;color:var(--muted);padding:4px}
@media(max-width:900px){.grid,.grid3{grid-template-columns:1fr}.stages{grid-template-columns:1fr 1fr}}@media(max-width:600px){main{padding:12px}.stages{grid-template-columns:1fr}h1{font-size:24px}}
</style>
</head>
<body><main>
<section class="card">
<div class="eyebrow">ARCH3D-001 · Dashboard V2 · State %s · %s</div>
<h1>中国古建筑3D复原｜平遥镇国寺万佛殿</h1>
<div class="muted">目标：从真实构件证据出发，完成可追溯、可重复生成的整殿三维复原。</div>
<div class="journey">
<div class="node done">P2 工程基线<br><strong>✓ CLOSED</strong></div><div class="arrow">→</div>
<div class="node done">P3.0<br><strong>✓ CLOSED</strong></div><div class="arrow">→</div>
<div class="node done">P3.1<br><strong>✓ CLOSED</strong></div><div class="arrow">→</div>
<div class="node done">P3.2<br><strong>✓ CLOSED</strong></div><div class="arrow">→</div>
<div class="node active">P3.3 构件驱动整殿重建<br><strong>ACTIVE</strong></div>
</div>
<div class="statusline"><span class="pill ok">当前主线无 Blocker</span><span class="pill warn">P3.3｜Stage 1 ACTIVE</span><span class="pill hold">T-018 HOLD 至 Stage 6 再决策</span></div>
</section>

<div class="grid">
<section class="card"><h2>P3.3｜七阶段总路线</h2><div class="stages">%s</div>
<div class="note small" style="margin-top:12px"><strong>读法：</strong>%s%% 是 Stage 1 的 Master 完成度，不是整个 P3.3 的总完成率。P3.3 的 7 个 Stage 当前尚未有一个整体关闭。</div></section>
<section class="card"><h2>当前最重要的数字</h2><div class="big">%s / %s</div><div class="muted">Stage 1 Master 已批准 · %s%%</div><div class="progress"><div style="width:%s%%"></div></div>
<div class="grid3" style="margin-top:12px"><div class="metric"><b>%s</b><span class="small">Master 待完成</span></div><div class="metric"><b>%s</b><span class="small">已覆盖 Registry records</span></div><div class="metric"><b>%s</b><span class="small">V008 总登记 records</span></div></div>
</section></div>

<div class="grid">
<section class="card"><h2>当前焦点与下一里程碑</h2>
<div class="callout okbox"><strong>刚完成：%s｜%s</strong><br><span class="small">%s</span></div>
<div class="callout" style="margin-top:12px"><strong>下一目标：%s</strong><br><span class="small">先完成 D-099 A1/A2 资料核查 + D-076 视觉/形制 Gate。通过前不创建新 T-task，不运行 Blender。</span></div></section>
<section class="card"><h2>风险 / HOLD / 待补证据</h2><div class="kv">
<div>Active blocker</div><div><strong>NONE</strong></div><div>T-018</div><div>HOLD；Stage 6 再决定 rebaseline 或 supersede</div>
<div>Pending source binding</div><div>%s 项：%s</div><div>事实主权</div><div>V008 Component Registry JSON</div><div>Master 主权</div><div>Stage1 Component Master Catalog</div><div>Excel</div><div>DERIVED_VIEW，不可覆盖 JSON</div>
</div></section></div>

<section class="card"><h2>Stage 1｜28 个 Master Scope 的大进展</h2>
<div class="batch"><h3>已完成｜%s</h3><div class="chips">%s</div></div>
<div class="batch"><h3>下一批｜%s</h3><div class="chips">%s</div></div>
<div class="batch"><h3>后续构件组｜%s</h3><div class="chips">%s</div></div>
</section>

<section class="card"><h2>Dashboard 的职责</h2><div class="grid3">
<div class="metric"><h3>首页只看</h3><span class="small">项目位置 · Gate/Stage · 完成度 · 下一里程碑 · Blocker/HOLD</span></div>
<div class="metric"><h3>不再堆在首页</h3><span class="small">Run ID · SHA · PR Patch · Review Patch · validator 逐项日志</span></div>
<div class="metric"><h3>需要追溯时</h3><span class="small">进入 Project Control · Task Lifecycle · Decision Log · Evidence / Registry</span></div>
</div></section>
<div class="footer">Dashboard v200 · DERIVED_VISUALIZATION · %s / D-105 · V008 · Catalog %s approved · Dashboard 本身不是事实主权源。</div>
</main></body></html>
""" % (
    escape(state["state_revision"]), escape(progress["snapshot_date"]), stage_html, pct,
    progress["approved_master_count"], progress["master_scope_object_type_count"], pct, pct,
    progress["pending_master_object_type_count"], progress["master_covered_registry_record_count"], progress["registry_record_count"],
    escape(last.get("id","NONE")), escape(last.get("component","")), escape(last.get("status","")),
    escape(next_target), len(pending_sources), escape("、".join(pending_sources)),
    len(approved), chips([x + " ✓" for x in approved], "done"),
    len(next_batch), chips(([next_target + " ← NEXT"] + [x for x in next_batch if x != next_target]), "next"),
    len(later_batch), chips(later_batch, "future"),
    escape(state["state_revision"]), catalog["approved_master_count"]
)

OUT.write_text(html, encoding="utf-8")
print("DASHBOARD_GENERATED", OUT)
print("STATE", state["state_revision"], "STAGE1", progress["approved_master_count"], "/", progress["master_scope_object_type_count"], "NEXT", next_target)
