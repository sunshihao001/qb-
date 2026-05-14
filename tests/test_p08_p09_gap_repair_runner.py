from __future__ import annotations

import json
from pathlib import Path

from modules.runtime.p08_p09_gap_repair_runner import run_p08_p09_gap_repair_closure


ROOT = Path(__file__).resolve().parents[1]


def _load(path: str | Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_p08_p09_gap_repair_closure_generates_runtime_artifacts_and_preserves_paper_only(tmp_path: Path):
    result = run_p08_p09_gap_repair_closure(
        root=ROOT,
        output_dir=tmp_path / "repair",
        mode="dry-run",
        issues_file=ROOT / "runtime_logs/full_system_runtime/current_degraded_issues.json",
        route_file=ROOT / "runtime_logs/full_system_runtime/p08_p09_gap_repair_route.json",
    )

    assert result["task_id"] == "task_7_p08_p09_gap_repair_closure"
    assert result["final_status"] == "TASK_7_READY"
    assert result["paper_only"] is True
    assert result["runtime_apply_allowed"] is False
    assert result["safety_boundary"] == {
        "real_trade": "forbidden",
        "signing": "forbidden",
        "broadcast": "forbidden",
        "secret_read": "forbidden",
        "runtime_apply": "forbidden",
        "strategy_auto_modify": "forbidden",
    }
    assert result["covered_gap_count"] == 5
    assert result["remaining_gap_count"] == 0
    assert set(result["repair_items_completed"]) == {
        "PHASE08_EVIDENCE_CHAIN_REPAIR",
        "PHASE09_KNOWN_SUCCESS_REGRESSION_FIXTURE",
        "PHASE09_SHADOW_ROLLBACK_VALIDATION_CLOSURE",
        "COLLECTOR_AND_REPLAY_FIXTURE_CLOSURE",
    }

    required_artifacts = {
        "p08_evidence_chain_manifest",
        "p09_known_success_registry",
        "p09_validation_package",
        "collector_replay_fixture_manifest",
        "repair_state",
        "repair_audit",
        "repair_result",
        "repair_handoff",
    }
    assert required_artifacts <= set(result["artifacts"])
    for key in required_artifacts:
        assert Path(result["artifacts"][key]).exists(), key

    state = _load(result["artifacts"]["repair_state"])
    assert state["status"] == "TASK_7_READY"
    assert state["next_allowed_task"] == "full_system_no_checkpoint_replay"
    assert state["runtime_apply_allowed"] is False
    assert state["paper_only"] is True
    assert state["remaining_gaps"] == []

    handoff = _load(result["artifacts"]["repair_handoff"])
    assert handoff["handoff_status"] == "HANDOFF_READY"
    assert handoff["next_allowed_task"] == "full_system_no_checkpoint_replay"
    assert handoff["required_files_for_next_stage"]["p09_validation_package"].endswith("p09_validation_package.json")
    assert handoff["runtime_apply_allowed"] is False

    audit_text = Path(result["artifacts"]["repair_audit"]).read_text(encoding="utf-8")
    assert "TASK_7 / P08-P09 Gap Repair Closure" in audit_text
    assert "paper-only" in audit_text
    assert "runtime_apply: 禁止" in audit_text


def test_p08_p09_gap_repair_closure_artifact_semantics_close_phase08_phase09_and_replay_fixtures(tmp_path: Path):
    result = run_p08_p09_gap_repair_closure(
        root=ROOT,
        output_dir=tmp_path / "repair",
        mode="replay",
        issues_file=ROOT / "runtime_logs/full_system_runtime/current_degraded_issues.json",
        route_file=ROOT / "runtime_logs/full_system_runtime/p08_p09_gap_repair_route.json",
    )

    p08_manifest = _load(result["artifacts"]["p08_evidence_chain_manifest"])
    assert p08_manifest["closure_status"] == "P08_EVIDENCE_CHAIN_CLOSED"
    assert p08_manifest["evidence_chain_status"] == "EVIDENCE_CHAIN_COMPLETE"
    assert p08_manifest["required_phase_count"] == 7
    assert p08_manifest["present_phase_count"] == 7
    assert p08_manifest["missing_evidence_chain"] == []
    assert p08_manifest["absolute_conclusion_allowed"] is False
    assert all(link["present"] is True for link in p08_manifest["links"])

    registry = _load(result["artifacts"]["p09_known_success_registry"])
    assert registry["registry_status"] == "KNOWN_SUCCESS_FIXTURE_READY"
    assert registry["known_success_case_count"] >= 1
    assert registry["regression_fixture_required"] is True
    assert registry["runtime_apply_allowed"] is False
    assert all(case["preservation_decision"] == "PRESERVE_BEFORE_UPGRADE" for case in registry["protected_cases"])

    validation = _load(result["artifacts"]["p09_validation_package"])
    assert validation["validation_status"] == "P09_VALIDATION_PACKAGE_READY"
    assert validation["known_success_status"] == "KNOWN_SUCCESS_PRESERVED"
    assert validation["regression_status"] == "REGRESSION_TEST_PASS"
    assert validation["shadow_mode_status"] == "SHADOW_MODE_REQUIRED"
    assert validation["rollback_validation_status"] == "ROLLBACK_VALID"
    assert validation["runtime_apply_allowed"] is False
    assert validation["signing_allowed"] is False
    assert validation["broadcast_allowed"] is False

    replay = _load(result["artifacts"]["collector_replay_fixture_manifest"])
    assert replay["fixture_status"] == "COLLECTOR_REPLAY_FIXTURE_READY"
    assert replay["phase_range"] == ["P01", "P02", "P03", "P04", "P05", "P06", "P07", "P08", "P09"]
    assert replay["checkpoint_reuse_allowed"] is False
    assert replay["no_checkpoint_replay_required"] is True
    assert replay["fixture_contract"]["token_redacted"] is True
    assert replay["fixture_contract"]["real_trade_actions"] == []


def test_p08_p09_gap_repair_cli_smoke(tmp_path: Path):
    import subprocess

    cmd = [
        "python3",
        "-m",
        "modules.runtime.p08_p09_gap_repair_runner",
        "--root",
        str(ROOT),
        "--issues-file",
        str(ROOT / "runtime_logs/full_system_runtime/current_degraded_issues.json"),
        "--route-file",
        str(ROOT / "runtime_logs/full_system_runtime/p08_p09_gap_repair_route.json"),
        "--output-dir",
        str(tmp_path / "cli_repair"),
        "--mode",
        "dry-run",
    ]
    completed = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=True)
    payload = json.loads(completed.stdout)
    assert payload["final_status"] == "TASK_7_READY"
    assert payload["remaining_gap_count"] == 0
    assert Path(payload["artifacts"]["repair_result"]).exists()
