import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import sikk_full_auto_orchestrator as full_auto


def test_full_auto_orchestrator_is_compatibility_wrapper_for_live_run():
    wrapper = Path("/root/sikk-gmgn/sikk_full_auto_orchestrator.py")
    assert wrapper.exists()
    text = wrapper.read_text(encoding="utf-8")
    assert "from sikk_live_run import run_live_once" in text
    assert "兼容入口" in text
    assert "不创建新的并行主循环" in text
    assert "real_swap" not in text.lower().replace("real_swap_enabled", "")


def test_full_auto_orchestrator_accepts_user_command_shape(tmp_path):
    script = Path("/root/sikk-gmgn/sikk_full_auto_orchestrator.py")
    completed = subprocess.run(
        [
            sys.executable,
            str(script),
            "--base-dir",
            str(tmp_path),
            "--mode",
            "once",
            "--limit",
            "1",
            "--quote-sources",
            "none",
            "--default-quote-amount-sol",
            "0.01",
            "--paper-only",
            "--dry-run",
        ],
        cwd="/root/sikk-gmgn",
        text=True,
        capture_output=True,
        check=True,
    )
    payload = json.loads(completed.stdout)
    assert payload["dry_run"] is True
    assert payload["canonical_entrypoint"] == "sikk_live_run.py"
    assert payload["mapped_args"]["output_root"] == str(tmp_path)
    assert payload["mapped_args"]["limit"] == 1
    assert payload["mapped_args"]["quote_sources"] == ["none"]
    assert payload["safety_boundary"]["paper_only"] is True
    assert payload["safety_boundary"]["real_swap_enabled"] is False
    assert payload["safety_boundary"]["broadcast_enabled"] is False


def test_full_automation_v1_contract_declares_required_layers_and_artifacts():
    contract = full_auto.build_full_automation_contract()
    layer_names = [layer["name"] for layer in contract["layers"]]
    assert layer_names == [
        "Runtime Orchestrator",
        "Data Source Layer",
        "Structure Intelligence Layer",
        "State Machine Layer",
        "Paper Trading Layer",
        "Case File Layer",
        "Review Layer",
        "Interaction Layer",
        "Audit Layer",
        "Reporting Layer",
    ]
    artifact_keys = {artifact["key"] for artifact in contract["required_artifacts"]}
    for key in [
        "candidate_discovery",
        "signal_analysis",
        "wallet_structure",
        "okx_cluster",
        "quote_security",
        "state_machine",
        "paper_runner",
        "case_backfill",
        "auto_review",
        "unified_index",
        "dashboard",
        "telegram_callback_index",
        "reports",
        "events",
    ]:
        assert key in artifact_keys
    assert contract["safety_boundary"]["real_swap_enabled"] is False
    assert contract["safety_boundary"]["signing_enabled"] is False
    assert contract["safety_boundary"]["broadcast_enabled"] is False


def test_loop_dry_run_accepts_runtime_cadence_flags(tmp_path):
    script = Path("/root/sikk-gmgn/sikk_full_auto_orchestrator.py")
    completed = subprocess.run(
        [
            sys.executable,
            str(script),
            "--base-dir", str(tmp_path),
            "--mode", "loop",
            "--interval-sec", "600",
            "--paper-update-sec", "180",
            "--health-check-sec", "300",
            "--limit", "50",
            "--quote-sources", "okx",
            "--default-quote-amount-sol", "0.01",
            "--paper-only",
            "--dry-run",
        ],
        cwd="/root/sikk-gmgn",
        text=True,
        capture_output=True,
        check=True,
    )
    payload = json.loads(completed.stdout)
    assert payload["dry_run"] is True
    assert payload["loop_config"] == {
        "mode": "loop",
        "interval_sec": 600,
        "paper_update_sec": 180,
        "health_check_sec": 300,
    }
    assert payload["full_automation_contract"]["version"] == "SIKK Full Automation System v1.0"


def test_run_loop_from_args_invokes_once_repeatedly_and_writes_health_report(tmp_path, monkeypatch):
    calls = []
    sleeps = []

    def fake_run_once(args):
        calls.append(args.mode)
        return {
            "canonical_entrypoint": "sikk_live_run.py",
            "safety_boundary": full_auto.SAFETY_BOUNDARY,
            "result": {"live_run_manifest_json": str(tmp_path / "live_run_manifest.json")},
        }

    monkeypatch.setattr(full_auto, "run_once_from_args", fake_run_once)
    monkeypatch.setattr(full_auto.time, "sleep", lambda seconds: sleeps.append(seconds))

    args = SimpleNamespace(
        base_dir=str(tmp_path),
        mode="loop",
        interval_sec=600,
        paper_update_sec=180,
        health_check_sec=300,
        max_loops=2,
        paper_only=True,
        dry_run=False,
    )
    payload = full_auto.run_loop_from_args(args)

    assert calls == ["loop", "loop"]
    assert sleeps == [600]
    assert payload["loop_summary"]["completed_iterations"] == 2
    assert payload["loop_config"]["paper_update_sec"] == 180
    report = tmp_path / "full_automation" / "FULL_AUTOMATION_V1_HEALTH.json"
    assert report.exists()
    report_payload = json.loads(report.read_text(encoding="utf-8"))
    assert report_payload["safety_boundary"]["real_swap_enabled"] is False
    assert report_payload["loop_summary"]["target_runtime_hours"] == 5
