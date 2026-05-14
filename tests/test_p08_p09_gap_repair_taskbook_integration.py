from __future__ import annotations

import json
from pathlib import Path


ROOT = Path("/root/sikk-gmgn")


REQUIRED_GAPS = {
    "PHASE_09_LOW_CONFIDENCE_REPLAY",
    "PHASE08_NEXT_STAGE_BLOCKED_GAP_AWARE_PROGRESSION",
    "PHASE08_DEGRADE_REASON",
    "PHASE08_MISSING_FIELDS",
    "PHASE09_SYSTEM_UPGRADE_BLOCKED_GAP_AWARE_PROGRESSION",
}


REQUIRED_REPAIR_ITEMS = {
    "PHASE08_EVIDENCE_CHAIN_REPAIR",
    "PHASE09_KNOWN_SUCCESS_REGRESSION_FIXTURE",
    "PHASE09_SHADOW_ROLLBACK_VALIDATION_CLOSURE",
    "COLLECTOR_AND_REPLAY_FIXTURE_CLOSURE",
}


def test_p08_p09_gap_repair_taskbook_is_indexed_and_gap_mapped():
    taskbook = ROOT / "task_books/full_system_runtime_bundle/18_p08_p09_gap_repair_taskbook.md"
    assert taskbook.exists()
    text = taskbook.read_text(encoding="utf-8")

    for gap_id in REQUIRED_GAPS:
        assert gap_id in text
    for repair_item in REQUIRED_REPAIR_ITEMS:
        assert repair_item in text

    assert "TASK_7_READY" in text
    assert "TASK_7_READY_WITH_GAPS" in text
    assert "TASK_7_REJECTED" in text
    assert "Full-system acceptance replay" in text
    assert "[REDACTED]" in text

    bundle_index = json.loads((ROOT / "task_books/full_system_runtime_bundle/full_system_runtime_bundle_index.json").read_text(encoding="utf-8"))
    repair_index = bundle_index["p08_p09_gap_repair_closure"]
    assert repair_index["task_id"] == "task_7_p08_p09_gap_repair_closure"
    assert repair_index["taskbook"] == "task_books/full_system_runtime_bundle/18_p08_p09_gap_repair_taskbook.md"
    assert set(repair_index["covered_gap_ids"]) == REQUIRED_GAPS
    assert repair_index["next_allowed_task"] == "task_7_p08_p09_gap_repair_closure"
    assert "paper-only" in repair_index["safety_boundary"]


def test_p08_p09_gap_repair_route_is_runtime_consumable_and_safe():
    route = json.loads((ROOT / "runtime_logs/full_system_runtime/p08_p09_gap_repair_route.json").read_text(encoding="utf-8"))

    assert route["route_id"] == "task_7_p08_p09_gap_repair_closure_route"
    assert route["source_status"] == "FULL_SYSTEM_BUNDLE_READY_WITH_GAPS"
    assert route["current_allowed_task"] == "task_7_p08_p09_gap_repair_closure"
    assert route["next_allowed_task"] == "task_7_p08_p09_gap_repair_closure"
    assert set(route["covered_gap_ids"]) == REQUIRED_GAPS
    assert set(route["repair_items"]) == REQUIRED_REPAIR_ITEMS
    assert route["live_apply_allowed"] is False
    assert route["safety_boundary"]["paper_only"] is True
    assert route["safety_boundary"]["signing_enabled"] is False
    assert route["safety_boundary"]["broadcast_enabled"] is False
    assert route["safety_boundary"]["real_trade_enabled"] is False

    runtime_state = json.loads((ROOT / "runtime_logs/full_system_runtime/runtime_task_state.json").read_text(encoding="utf-8"))
    assert runtime_state["repair_next_allowed_task"] == "task_7_p08_p09_gap_repair_closure"
    assert runtime_state["p08_p09_gap_repair_route"] == "runtime_logs/full_system_runtime/p08_p09_gap_repair_route.json"
    assert runtime_state["gap_repair_taskbook"] == "task_books/full_system_runtime_bundle/18_p08_p09_gap_repair_taskbook.md"


def test_p08_p09_gap_repair_planbook_is_in_planbook_repository_index():
    planbook = ROOT / "research_loop/plan_books/active/p08_p09_gap_repair_closure_planbook.md"
    assert planbook.exists()
    text = planbook.read_text(encoding="utf-8")
    assert "planbook_id: `p08_p09_gap_repair_closure_planbook`" in text
    assert "status: `RUNTIME_CONSUMABLE`" in text
    assert "paper-only / no signing / no broadcast / no real trade" in text

    index = json.loads((ROOT / "research_loop/plan_books/index/planbook_index.json").read_text(encoding="utf-8"))
    planbooks = {item["metadata"]["planbook_id"]: item for item in index["planbooks"]}
    assert "p08_p09_gap_repair_closure_planbook" in planbooks
    assert planbooks["p08_p09_gap_repair_closure_planbook"]["status"] == "PLANBOOK_READY"
    assert index["final_status"] == "PLANBOOK_REPOSITORY_READY"
