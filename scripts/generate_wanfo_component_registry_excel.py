#!/usr/bin/env python3
"""Generate the Wanfo Hall component registry Excel as a derived artifact.

Canonical input:
  docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json

Outputs:
  docs/evidence/zhenguo_wanfo/derived/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.xlsx
  docs/evidence/zhenguo_wanfo/derived/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_<VERSION>.xlsx
  docs/evidence/zhenguo_wanfo/derived/P3_WANFO_COMPONENT_EXCEL_SYNC_MANIFEST.json

The Excel files are derived views. Never edit them as canonical project facts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.table import Table, TableStyleInfo


GENERATOR_VERSION = "1.0.2"
GENERATOR_REPO_PATH = "scripts/generate_wanfo_component_registry_excel.py"
DEFAULT_INPUT = Path("docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json")
DEFAULT_OUTPUT_DIR = Path("docs/evidence/zhenguo_wanfo/derived")
MANIFEST_NAME = "P3_WANFO_COMPONENT_EXCEL_SYNC_MANIFEST.json"
CURRENT_XLSX_NAME = "P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.xlsx"

BASE_COLUMNS = [
    ("system", "系统"),
    ("component", "构件/对象"),
    ("id", "实例/记录ID"),
    ("location", "具体位置"),
    ("count_status", "数量/状态口径"),
    ("stage1_disposition", "Stage1处置"),
    ("master_coverage_status", "Master状态"),
    ("master_reference", "Master引用"),
    ("evidence", "证据依据"),
    ("variant", "变体"),
    ("direction", "方向"),
    ("type", "类型"),
    ("section", "截面"),
    ("section_mm", "截面(mm)"),
    ("dimensions_mm", "尺寸(mm)"),
    ("length_rule", "长度规则"),
    ("length_mm", "长度(mm)"),
    ("width_mm", "宽度(mm)"),
    ("thickness_mm", "厚度(mm)"),
    ("scope", "适用范围"),
    ("rows", "阵列/陇数"),
    ("note", "备注"),
    ("details_json", "其他字段(JSON)"),
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def scalar_text(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, (str, int, float, bool)):
        return value
    return json_text(value)


def normalize_item(item: dict[str, Any]) -> list[Any]:
    known = {key for key, _ in BASE_COLUMNS if key != "details_json"}
    values: list[Any] = []
    for key, _ in BASE_COLUMNS:
        if key == "details_json":
            extra = {k: v for k, v in item.items() if k not in known}
            values.append(json_text(extra) if extra else "")
        else:
            values.append(scalar_text(item.get(key)))
    return values


def style_header(ws, row: int, start_col: int, end_col: int, fill: str = "4A3A30") -> None:
    for cell in ws.iter_cols(min_col=start_col, max_col=end_col, min_row=row, max_row=row):
        c = cell[0]
        c.fill = PatternFill("solid", fgColor=fill)
        c.font = Font(color="FFFFFF", bold=True)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)


def set_widths(ws, widths: dict[str, float]) -> None:
    for col, width in widths.items():
        ws.column_dimensions[col].width = width


def build_workbook(registry: dict[str, Any], source_path: Path, source_commit: str, source_sha: str, generator_sha: str) -> Workbook:
    wb = Workbook()
    overview = wb.active
    overview.title = "进度总览"

    progress = registry.get("stage1_master_progress_summary", {})
    overview.merge_cells("A1:D1")
    overview["A1"] = "万佛殿 V008｜Stage 1 Master 进度总览"
    overview["A1"].font = Font(size=16, bold=True, color="FFFFFF")
    overview["A1"].fill = PatternFill("solid", fgColor="3E342C")
    overview["A1"].alignment = Alignment(horizontal="center", vertical="center")
    overview.row_dimensions[1].height = 28

    overview.append([])
    overview.append(["指标", "当前值", "口径/说明", "状态"])
    kpi_rows = [
        ["登记记录数", progress.get("registry_record_count", len(registry.get("items", []))), "V008登记行数；包含实体、系统、拓扑、族边界等记录，不等于整殿物理构件总件数", "INFO"],
        ["登记对象类型", progress.get("registered_object_type_count", ""), "V008当前登记的不同构件/对象类型", "INFO"],
        ["Stage1 Master范围", progress.get("master_scope_object_type_count", ""), "需要或已经具有Master的对象类型数；作为Master完成度分母", "TRACKED"],
        ["已批准 Master", progress.get("approved_master_count", ""), "PRODUCT_OWNER_APPROVED Master available", "COMPLETE"],
        ["待完成 Master", progress.get("pending_master_object_type_count", ""), "Master范围 - 已批准Master", "PENDING"],
        ["Master完成度", progress.get("master_completion_percent", ""), "已批准Master / Stage1 Master范围", "PROGRESS"],
        ["已绑定Master的登记记录", progress.get("master_covered_registry_record_count", ""), "仅表示V008登记行覆盖数，不等于物理构件总件数", "INFO"],
        ["PENDING_SOURCE_BINDING", progress.get("pending_source_binding_count", len(registry.get("pending_source_binding", []))), "仍在V008之外、不得静默视为已覆盖的对象", "PENDING"],
    ]
    for row in kpi_rows:
        overview.append(row)

    style_header(overview, 3, 1, 4, fill="6B4F3A")
    overview["B9"].number_format = '0.0"%"'
    if isinstance(overview["B9"].value, (int, float)):
        overview["B9"] = float(overview["B9"].value) / 100.0
    set_widths(overview, {"A": 26, "B": 18, "C": 72, "D": 18})
    for row in overview.iter_rows(min_row=4, max_row=11):
        for c in row:
            c.alignment = Alignment(vertical="top", wrap_text=True)
    complete_fill = PatternFill("solid", fgColor="D9EAD3")
    pending_fill = PatternFill("solid", fgColor="FFF2CC")
    for row in range(4, 12):
        if overview.cell(row, 4).value == "COMPLETE":
            overview.cell(row, 2).fill = complete_fill
        elif overview.cell(row, 4).value == "PENDING":
            overview.cell(row, 2).fill = pending_fill

    overview["A13"] = "构件 / 对象 Master 覆盖状态"
    overview["A13"].font = Font(bold=True, size=12)
    overview.append(["构件/对象", "Stage1处置", "Master状态", "Master引用", "登记记录数"])
    style_header(overview, 14, 1, 5, fill="4A3A30")
    grouped: dict[str, dict[str, Any]] = {}
    for item in registry.get("items", []):
        comp = str(item.get("component", ""))
        if not comp:
            continue
        g = grouped.setdefault(comp, {"records": 0, "dispositions": set(), "statuses": set(), "masters": set()})
        g["records"] += 1
        if item.get("stage1_disposition"):
            g["dispositions"].add(str(item["stage1_disposition"]))
        if item.get("master_coverage_status"):
            g["statuses"].add(str(item["master_coverage_status"]))
        if item.get("master_reference"):
            g["masters"].add(str(item["master_reference"]))
    for comp in sorted(grouped):
        g = grouped[comp]
        overview.append([
            comp,
            " / ".join(sorted(g["dispositions"])),
            " / ".join(sorted(g["statuses"])),
            " / ".join(sorted(g["masters"])),
            g["records"],
        ])
    for row in overview.iter_rows(min_row=15):
        for c in row:
            c.alignment = Alignment(vertical="top", wrap_text=True)
        status = str(row[2].value or "")
        if "APPROVED_MASTER_AVAILABLE" in status:
            row[2].fill = complete_fill
        elif "MASTER_REQUIRED_PENDING" in status:
            row[2].fill = pending_fill
    overview.freeze_panes = "A4"
    set_widths(overview, {"A": 26, "B": 30, "C": 38, "D": 42, "E": 14})
    overview.auto_filter.ref = "A14:E{}".format(overview.max_row)

    ws = wb.create_sheet("实例登记")

    headers = [label for _, label in BASE_COLUMNS]
    ws.append(headers)
    for item in registry.get("items", []):
        ws.append(normalize_item(item))

    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    style_header(ws, 1, 1, len(headers))
    set_widths(ws, {
        "A": 16, "B": 18, "C": 34, "D": 38, "E": 26, "F": 24, "G": 34, "H": 40,
        "I": 32, "J": 20, "K": 16, "L": 16, "M": 24, "N": 26, "O": 34, "P": 28,
        "Q": 14, "R": 14, "S": 14, "T": 28, "U": 18, "V": 40, "W": 52,
    })
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(vertical="top", wrap_text=True)

    if ws.max_row >= 2:
        end_col = ws.cell(row=1, column=len(headers)).column_letter
        table = Table(displayName="WanfoComponentRegistry", ref="A1:{}{}".format(end_col, ws.max_row))
        table.tableStyleInfo = TableStyleInfo(
            name="TableStyleMedium2",
            showFirstColumn=False,
            showLastColumn=False,
            showRowStripes=True,
            showColumnStripes=False,
        )
        ws.add_table(table)

    summary = wb.create_sheet("统计摘要")
    summary.append(["统计维度", "名称", "记录数"])
    system_counts = Counter(str(x.get("system", "")) for x in registry.get("items", []))
    component_counts = Counter(str(x.get("component", "")) for x in registry.get("items", []))
    status_counts = Counter(str(x.get("count_status", "")) for x in registry.get("items", []))
    for name, count in sorted(system_counts.items()):
        summary.append(["系统", name, count])
    for name, count in sorted(component_counts.items()):
        summary.append(["构件/对象", name, count])
    for name, count in sorted(status_counts.items()):
        summary.append(["数量/状态口径", name, count])
    summary.freeze_panes = "A2"
    style_header(summary, 1, 1, 3, fill="6B4F3A")
    set_widths(summary, {"A": 20, "B": 36, "C": 14})

    meta = wb.create_sheet("版本与来源")
    meta_rows = [
        ["字段", "值"],
        ["文件性质", "派生表格视图 / 非独立事实源"],
        ["唯一事实源", str(source_path).replace("\\", "/")],
        ["登记版本", registry.get("schema_version", "")],
        ["登记日期", registry.get("date", "")],
        ["登记状态", registry.get("status", "")],
        ["记录数", len(registry.get("items", []))],
        ["登记对象类型", registry.get("stage1_master_progress_summary", {}).get("registered_object_type_count", "")],
        ["Stage1 Master范围", registry.get("stage1_master_progress_summary", {}).get("master_scope_object_type_count", "")],
        ["已批准Master", registry.get("stage1_master_progress_summary", {}).get("approved_master_count", "")],
        ["待完成Master", registry.get("stage1_master_progress_summary", {}).get("pending_master_object_type_count", "")],
        ["Master完成度", str(registry.get("stage1_master_progress_summary", {}).get("master_completion_percent", "")) + "%"],
        ["源 GitHub 提交", source_commit or "UNKNOWN"],
        ["源 JSON SHA-256", source_sha],
        ["生成器版本", GENERATOR_VERSION],
        ["生成器 SHA-256", generator_sha],
        ["同步规则", "JSON先更新；Excel由自动流程生成。禁止人工修改Excel作为事实更新。"],
        ["版本规则", "CURRENT.xlsx对应CURRENT.json；Vxxx.xlsx对应同版本Vxxx.json快照。"],
        ["失败规则", "自动生成失败时保持旧Excel并标记同步失败；不得假装已同步。"],
    ]
    for row in meta_rows:
        meta.append(row)
    style_header(meta, 1, 1, 2, fill="3E342C")
    set_widths(meta, {"A": 28, "B": 88})
    for row in meta.iter_rows():
        for c in row:
            c.alignment = Alignment(vertical="top", wrap_text=True)

    rules = wb.create_sheet("使用规则")
    rule_rows = [
        ["规则", "内容"],
        ["R1", "构件登记 JSON 是唯一主数据；Excel 只读派生，不得人工回写为事实。"],
        ["R2", "任何正式数据变更必须先创建/更新版本化 JSON，并同步 CURRENT.json。"],
        ["R3", "自动流程从 CURRENT.json 生成 CURRENT.xlsx 和同版本 Vxxx.xlsx。"],
        ["R4", "Excel 必须记录登记版本、源 GitHub 提交、JSON SHA-256 与生成器 SHA-256。"],
        ["R5", "JSON/Excel 版本或哈希不一致时视为同步失败，禁止将 Excel 当作当前视图。"],
        ["R6", "历史版本 Excel/JSON 保留；CURRENT 始终代表当前正式登记。"],
    ]
    for row in rule_rows:
        rules.append(row)
    style_header(rules, 1, 1, 2, fill="7A563F")
    set_widths(rules, {"A": 12, "B": 100})
    for row in rules.iter_rows():
        for c in row:
            c.alignment = Alignment(vertical="top", wrap_text=True)

    wb.properties.title = "万佛殿整殿构件实例总表 {}".format(registry.get("schema_version", ""))
    wb.properties.subject = "Derived from canonical component registry JSON"
    wb.properties.creator = "ARCH3D-001 automated generator"
    wb.properties.description = "Derived artifact with Stage1 Master progress overview. Canonical truth remains the GitHub component registry JSON; Master approval authority remains the Stage1 Component Master Catalog."
    date_text = str(registry.get("date", "2026-01-01"))
    try:
        fixed_date = datetime.strptime(date_text, "%Y-%m-%d")
        wb.properties.created = fixed_date
        wb.properties.modified = fixed_date
    except ValueError:
        pass
    return wb


def validate_snapshot(registry: dict[str, Any], input_path: Path) -> Path:
    version = str(registry.get("schema_version", "")).strip()
    if not version:
        raise SystemExit("FAIL_CLOSED: schema_version missing")
    versioned = input_path.with_name("P3_WANFO_COMPONENT_INSTANCE_REGISTRY_{}.json".format(version))
    if not versioned.exists():
        raise SystemExit("FAIL_CLOSED: versioned snapshot missing: {}".format(versioned))
    snap = json.loads(versioned.read_text(encoding="utf-8"))
    if snap != registry:
        raise SystemExit("FAIL_CLOSED: CURRENT registry does not equal versioned snapshot {}".format(version))
    return versioned


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--source-commit", default="")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    manifest_path = output_dir / MANIFEST_NAME
    current_xlsx = output_dir / CURRENT_XLSX_NAME

    raw = input_path.read_bytes()
    registry = json.loads(raw.decode("utf-8"))
    versioned_json = validate_snapshot(registry, input_path)

    version = str(registry["schema_version"])
    versioned_xlsx = output_dir / "P3_WANFO_COMPONENT_INSTANCE_REGISTRY_{}.xlsx".format(version)
    source_sha = sha256_bytes(raw)
    generator_sha = sha256_file(Path(__file__))

    if manifest_path.exists() and current_xlsx.exists() and versioned_xlsx.exists():
        try:
            old = json.loads(manifest_path.read_text(encoding="utf-8"))
            if old.get("source_json_sha256") == source_sha and old.get("generator_sha256") == generator_sha:
                print("UP_TO_DATE: source JSON and generator unchanged")
                return 0
        except Exception:
            pass

    output_dir.mkdir(parents=True, exist_ok=True)
    wb = build_workbook(registry, input_path, args.source_commit, source_sha, generator_sha)
    wb.save(versioned_xlsx)
    shutil.copyfile(versioned_xlsx, current_xlsx)

    # Fail-closed validation of the generated workbook.
    check = load_workbook(versioned_xlsx, read_only=True, data_only=False)
    expected = {"进度总览", "实例登记", "统计摘要", "版本与来源", "使用规则"}
    if set(check.sheetnames) != expected:
        raise SystemExit("FAIL_CLOSED: generated workbook sheets mismatch")
    rows = check["实例登记"].max_row - 1
    progress = registry.get("stage1_master_progress_summary", {})
    if check["进度总览"]["B4"].value != progress.get("registry_record_count"):
        raise SystemExit("FAIL_CLOSED: overview registry count mismatch")
    if check["进度总览"]["B7"].value != progress.get("approved_master_count"):
        raise SystemExit("FAIL_CLOSED: overview approved Master count mismatch")
    check.close()
    if rows != len(registry.get("items", [])):
        raise SystemExit("FAIL_CLOSED: generated row count mismatch")

    manifest = {
        "schema_version": "1.0",
        "status": "SYNCED",
        "registry_version": version,
        "source_json": str(input_path).replace("\\", "/"),
        "versioned_json_snapshot": str(versioned_json).replace("\\", "/"),
        "source_commit": args.source_commit or "UNKNOWN",
        "source_json_sha256": source_sha,
        "generator": GENERATOR_REPO_PATH,
        "generator_version": GENERATOR_VERSION,
        "generator_sha256": generator_sha,
        "record_count": len(registry.get("items", [])),
        "current_excel": str(current_xlsx).replace("\\", "/"),
        "current_excel_sha256": sha256_file(current_xlsx),
        "versioned_excel": str(versioned_xlsx).replace("\\", "/"),
        "versioned_excel_sha256": sha256_file(versioned_xlsx),
        "canonical_truth": "JSON",
        "excel_role": "DERIVED_VIEW",
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
