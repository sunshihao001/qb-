#!/usr/bin/env python3
"""Tests for Hermes Harness V1.7 Reliability Calibration Layer.

V1.7 turns V1.6 judgment governance outputs into measurable reliability feedback:
expected outcome -> observed outcome -> calibration delta -> benchmark update -> rule/memory candidate.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "09_scripts" / "hermes_reliability_calibration_run.py"


def test_reliability_calibration_assets_exist_and_policy_names_core_gates():
    required = [
        ROOT / "HERMES_HARNESS_V1_7_RELIABILITY_CALIBRATION_LAYER.md",
        ROOT / "01_control_plane" / "reliability_calibration_policy_v1_7.md",
        ROOT / "11_workflows" / "reliability_calibration.workflow.md",
        ROOT / "16_reliability_calibration" / "README.md",
        ROOT / "16_reliability_calibration" / "templates" / "reliability_calibration_state_template.json",
        RUNNER,
    ]
    for path in required:
        assert path.exists(), f"missing {path.relative_to(ROOT)}"

    policy = (ROOT / "01_control_plane" / "reliability_calibration_policy_v1_7.md").read_text(encoding="utf-8")
    for phrase in [
        "expected outcome",
        "observed outcome",
        "calibration delta",
        "judgment error rate",
        "benchmark update",
        "rule adjustment",
        "memory candidate",
        "revalidation window",
    ]:
        assert phrase in policy.lower()


def test_state_template_has_required_calibration_schema_fields():
    template = json.loads((ROOT / "16_reliability_calibration" / "templates" / "reliability_calibration_state_template.json").read_text(encoding="utf-8"))
    assert template["artifact_type"] == "reliability_calibration_state"
    required_fields = {
        "expected_outcome",
        "observed_outcome",
        "evidence_links",
        "calibration_delta",
        "judgment_error_rate",
        "benchmark_update",
        "rule_adjustment_candidate",
        "memory_candidate_review",
        "revalidation_window",
        "next_run_bias_correction",
        "calibration_decision",
    }
    assert required_fields.issubset(template.keys())


def test_runner_dry_run_outputs_calibration_contract_and_artifacts():
    problem = "Hermes 已经生成 V1.6 判断治理产物，但需要知道下一轮是否真的更可靠。"
    proc = subprocess.run(
        [sys.executable, str(RUNNER), "--dry-run", "--problem", problem, "--expected", "下一轮降低假闭环", "--observed", "dry-run 仅证明链路可运行", "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    payload = json.loads(proc.stdout.strip().splitlines()[-1])
    assert payload["status"] == "COMPLETED"
    assert payload["route"] == "hermes_reliability_calibration_layer"
    assert payload["overall_passed"] is True
    assert payload["calibration_decision"] in {"improve", "hold", "degrade", "needs_revalidation"}
    run_dir = Path(payload["run_dir"])
    assert run_dir.exists()
    for name in [
        "reliability_calibration_state.json",
        "expected_vs_observed.json",
        "calibration_delta.json",
        "judgment_error_rate.json",
        "benchmark_update.json",
        "rule_adjustment_candidate.md",
        "memory_candidate_review.json",
        "revalidation_window.md",
        "next_run_bias_correction.md",
        "reliability_calibration_report.md",
    ]:
        assert (run_dir / name).exists(), name
    state = json.loads((run_dir / "reliability_calibration_state.json").read_text(encoding="utf-8"))
    assert "delta_score" in state["calibration_delta"]
    assert state["memory_candidate_review"]["verified_memory_allowed"] is False


def test_runtime_hook_runner_includes_reliability_calibration_hook():
    source = (ROOT / "09_scripts" / "hermes_runtime_hook_run.py").read_text(encoding="utf-8")
    assert "reliability_calibration_hook" in source
    assert "hermes_reliability_calibration_run.py" in source
