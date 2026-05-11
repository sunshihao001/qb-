#!/usr/bin/env python3
"""Tests for Hermes Judgment Governance Layer.

These tests intentionally define V1.6 governance behavior before implementation.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "09_scripts" / "hermes_judgment_governance_run.py"


def test_judgment_governance_assets_exist_and_policy_names_core_gates():
    required = [
        ROOT / "HERMES_HARNESS_V1_6_JUDGMENT_GOVERNANCE_LAYER.md",
        ROOT / "01_control_plane" / "judgment_governance_policy_v1_6.md",
        ROOT / "11_workflows" / "judgment_governance.workflow.md",
        ROOT / "15_judgment_governance" / "README.md",
        ROOT / "15_judgment_governance" / "templates" / "judgment_governance_state_template.json",
        RUNNER,
    ]
    for path in required:
        assert path.exists(), f"missing {path.relative_to(ROOT)}"

    policy = (ROOT / "01_control_plane" / "judgment_governance_policy_v1_6.md").read_text(encoding="utf-8")
    for phrase in [
        "problem triage",
        "evidence sufficiency",
        "abstention gate",
        "meta verification",
        "anti self-deception",
        "memory lifecycle",
        "human override",
        "complexity brake",
    ]:
        assert phrase in policy.lower()


def test_state_template_has_required_governance_schema_fields():
    template = json.loads((ROOT / "15_judgment_governance" / "templates" / "judgment_governance_state_template.json").read_text(encoding="utf-8"))
    assert template["artifact_type"] == "judgment_governance_state"
    required_fields = {
        "problem_triage",
        "evidence_sufficiency",
        "abstention_decision",
        "solution_cost_review",
        "meta_verification",
        "anti_self_deception_audit",
        "causal_graph",
        "memory_lifecycle_review",
        "operator_decision_gate",
        "judgment_error_tracking",
        "governance_decision",
    }
    assert required_fields.issubset(template.keys())


def test_runner_dry_run_outputs_governance_contract_and_artifacts():
    problem = "Hermes 任务经常把 dry-run 当成真实完成，并把文件存在当成验证通过。"
    proc = subprocess.run(
        [sys.executable, str(RUNNER), "--dry-run", "--problem", problem, "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    payload = json.loads(proc.stdout.strip().splitlines()[-1])
    assert payload["status"] == "COMPLETED"
    assert payload["route"] == "hermes_judgment_governance_layer"
    assert payload["overall_passed"] is True
    assert payload["governance_decision"] in {"continue", "abstain", "observe", "human_handoff", "reduce_scope"}
    run_dir = Path(payload["run_dir"])
    assert run_dir.exists()
    for name in [
        "judgment_governance_state.json",
        "problem_triage.json",
        "evidence_sufficiency_matrix.json",
        "abstention_decision.md",
        "solution_cost_review.json",
        "meta_verification_report.md",
        "anti_self_deception_audit.md",
        "causal_graph.json",
        "memory_lifecycle_review.json",
        "operator_decision_gate.md",
        "judgment_governance_report.md",
    ]:
        assert (run_dir / name).exists(), name
    state = json.loads((run_dir / "judgment_governance_state.json").read_text(encoding="utf-8"))
    assert state["anti_self_deception_audit"]["fake_completion_risk"] in {"low", "medium", "high"}
    assert "verification_quality_score" in state["meta_verification"]


def test_runtime_hook_runner_includes_judgment_governance_hook():
    source = (ROOT / "09_scripts" / "hermes_runtime_hook_run.py").read_text(encoding="utf-8")
    assert "judgment_governance_hook" in source
    assert "hermes_judgment_governance_run.py" in source

