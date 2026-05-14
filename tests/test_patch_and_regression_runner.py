from __future__ import annotations

import json
from pathlib import Path

from modules.runtime.patch_and_regression_runner import run_patch_and_regression


def test_patch_and_regression_runner_writes_gap_aware_repair_artifacts(tmp_path):
    issues = [
        {
            "issue_id": "PHASE_09_LOW_CONFIDENCE_REPLAY",
            "severity": "degraded",
            "reason": "mock replay evidence only",
        }
    ]

    result = run_patch_and_regression(
        root=tmp_path,
        issues=issues,
        output_dir=tmp_path / "patch_loop",
        mode="dry-run",
        source_result_path="reports/system_audit/full_system_automation_result.json",
    )

    assert result["task_id"] == "task_6_patch_regression_loop"
    assert result["final_status"] == "PATCH_REGRESSION_READY_WITH_GAPS"
    assert result["runtime_apply_allowed"] is False
    assert result["safety_boundary"]["real_trade"] == "forbidden"
    assert result["resume_contract"]["supports_rerun_failed_wave"] is True
    assert result["regression_plan"][0]["issue_id"] == "PHASE_09_LOW_CONFIDENCE_REPLAY"
    assert result["regression_plan"][0]["target"] == "phase_09"
    assert result["regression_plan"][0]["rerun_scope"] == "single_phase_then_downstream_wave_replay"
    assert result["regression_plan"][0]["rerun_targets"] == ["phase_09", "full_system_e2e", "patch_and_regression"]
    assert result["gap_closure_package"]["closure_status"] == "open_with_gaps"
    assert result["gap_closure_package"]["runtime_apply_allowed"] is False

    artifacts = result["artifacts"]
    for key in ["patch_result", "patch_state", "patch_gap_register", "patch_handoff", "patch_audit", "gap_closure_package"]:
        assert Path(artifacts[key]).exists(), key

    handoff = json.loads(Path(artifacts["patch_handoff"]).read_text(encoding="utf-8"))
    assert handoff["next_allowed_task"] in {"rerun_failed_wave_or_full_system_e2e", "FULL_SYSTEM_AUTOMATION_READY"}
    assert handoff["runtime_apply_allowed"] is False
    assert handoff["requires_manual_confirmation"] is True


def test_patch_and_regression_rejects_blocking_issues_without_autofix(tmp_path):
    result = run_patch_and_regression(
        root=tmp_path,
        issues=[{"issue_id": "WAVE4_REJECTED", "severity": "blocking", "reason": "missing handoff"}],
        output_dir=tmp_path / "patch_loop_blocked",
        mode="dry-run",
    )

    assert result["final_status"] == "PATCH_REGRESSION_REJECTED"
    assert result["blocking_issue_count"] == 1
    assert result["next_allowed_task"] == "manual_review_required"
    assert result["runtime_apply_allowed"] is False
