#!/usr/bin/env python3
"""只读核对 Dashboard 当前首页与 Project State；不生成、不修改任何项目文件。"""
from copy import deepcopy
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "docs/project_control/project_state.json"
DASHBOARD = ROOT / "docs/project_control/dashboard.html"


class CurrentSummaryParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = False
        self.section_depth = 0
        self.section_count = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag != "section":
            return
        if self.active:
            self.section_depth += 1
        elif dict(attrs).get("id") == "dashboard-current-state":
            self.active = True
            self.section_depth = 1
            self.section_count += 1

    def handle_endtag(self, tag):
        if tag == "section" and self.active:
            self.section_depth -= 1
            if self.section_depth == 0:
                self.active = False

    def handle_data(self, data):
        if self.active:
            self.parts.append(data)


def verify(state, html):
    """返回当前首页一致性问题；历史折叠区域不能满足当前状态核验。"""
    errors = []
    parsed = CurrentSummaryParser()
    parsed.feed(html)
    if parsed.section_count != 1 or parsed.section_depth != 0:
        return ["必须且只能有一个完整的 dashboard-current-state 当前摘要区"]
    current = re.sub(r"\s+", " ", " ".join(parsed.parts)).strip()

    def check(condition, message):
        if not condition:
            errors.append(message)

    try:
        revision = state["state_revision"]
        date = state["last_updated"]
        metadata = state["dashboard"]
        phase = state["phase"]
        gate = state["current_gate"]
        active_task = state["current_task"]
        completed = state["last_completed_task"]
        proposed = state["proposed_next_task"]

        check(metadata["state_revision"] == revision, "Project State 内部 dashboard.state_revision 不一致")
        check(bool(re.search(r"(?<![A-Za-z0-9])" + re.escape(revision) + r"(?![A-Za-z0-9])", current)), "首页状态版本与 Project State 不一致")
        check(date in current, "首页更新日期不一致")
        check(metadata["visualization_version"] in current, "首页 Dashboard 版本不一致")
        check("当前阶段：" + gate["id"] + "（" + phase["status"] + "）" in current, "首页当前阶段不一致")
        check("当前任务：" + active_task["name"] in current, "首页当前任务不一致")
        check("最近完成：" + completed["name"] in current, "首页最近完成记录不一致")
        check("下一任务：" + proposed["name"] in current, "首页下一任务不一致")

        if "WORK_STOPPED" in state["session_status"]:
            check("今日工程停止" in current, "首页缺少工程停止状态")

        approved = state.get("approved_curved_gong_v002")
        if approved and approved.get("main_publication") == "CANONICAL / PR62_MERGED":
            check("已批准V002" in current, "首页遗漏正式批准V002")
            check(str(approved["entity_count"]) + "实体" in current, "首页已批准V002实体数不一致")
            check("PR" + str(approved["registration_pr"]) + "已合并" in current, "首页V002发布状态不一致")
            if approved.get("formal_stage3_closed") is False:
                check("Stage3整体未关闭" in current, "首页Stage3关闭边界不一致")

        close_key = "daily_close_" + date.replace("-", "_")
        closeout = state.get(close_key)
        if closeout:
            if closeout.get("status") == "PASS_WITH_KNOWN_EXCEPTIONS":
                check("PASS WITH KNOWN EXCEPTIONS" in current, "首页每日收尾状态不一致")
            sync = closeout.get("local_sync", {}).get("status", "")
            if "PENDING" in sync:
                check("Mac同步待实际执行" in current, "首页Mac同步状态不一致")
            for item in closeout.get("known_exceptions", []):
                if item.get("id") == "THREE_MEMBER_FORM" and item.get("status", "").startswith("NOT_ESTABLISHED"):
                    check("完整外形尚未证实" in current, "首页未保留三构件外形未决边界")
    except (KeyError, TypeError, ValueError) as exc:
        errors.append("正式状态缺少所需核验字段：" + str(exc))
    return errors


def run_self_test(state, html):
    check_count = 0
    if verify(state, html):
        print("SELF_TEST_BASELINE_FAIL:", verify(state, html))
        return False
    print("SELF_TEST_BASELINE_PASS")
    cases = []
    changed = deepcopy(state)
    changed["state_revision"] = "R999_TEST"
    cases.append(("state_revision_changed", changed, html))
    changed = deepcopy(state)
    changed["current_task"]["name"] = "被篡改的当前任务"
    cases.append(("current_task_changed", changed, html))
    changed = deepcopy(state)
    changed["proposed_next_task"]["name"] = "被篡改的下一任务"
    cases.append(("next_task_changed", changed, html))
    changed = deepcopy(state)
    changed["approved_curved_gong_v002"]["entity_count"] = 64
    cases.append(("approved_entity_count_changed", changed, html))
    cases.append(("current_section_revision_removed_historical_not_substitute", state, html.replace(
        state["state_revision"], "R999_TEST", 1
    )))
    for name, case_state, case_html in cases:
        failures = verify(case_state, case_html)
        if not failures:
            print("SELF_TEST_FAIL_NO_DETECTION:", name)
            return False
        print("SELF_TEST_EXPECTED_REJECTION_PASS:", name)
        check_count += 1
    print("SELF_TEST_PASS:", check_count, "negative cases")
    return True


def main():
    state = json.loads(STATE.read_text(encoding="utf-8"))
    html = DASHBOARD.read_text(encoding="utf-8")
    issues = verify(state, html)
    if issues:
        for item in issues:
            print("DASHBOARD_CONSISTENCY_FAIL:", item)
        return 1
    print("DASHBOARD_CONSISTENCY_PASS:", state["state_revision"], "READ_ONLY")
    if "--self-test" in sys.argv:
        return 0 if run_self_test(state, html) else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
