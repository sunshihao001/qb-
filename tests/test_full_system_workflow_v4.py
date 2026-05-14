from __future__ import annotations

import json
from pathlib import Path

import pytest

from modules.runtime.full_system_workflow_v4 import FullSystemWorkflowV4


EXPECTED_TASK_LAYERS = [
    "task_0_full_system_bundle_bootstrap",
    "task_1_wave_1_p01_p03_foundation_runtime",
    "task_2_wave_2_p04_p05_scenario_position_runtime",
    "task_3_wave_3_p06_p07_strategy_execution_risk_runtime",
    "task_4_wave_4_p08_p09_review_upgrade_runtime",
    "task_5_full_system_e2e_validation",
    "task_6_patch_regression_loop",
]


def _seed_minimal_bundle(root: Path) -> None:
    bundle_dir = root / "task_books" / "full_system_runtime_bundle"
    bundle_dir.mkdir(parents=True, exist_ok=True)
    (bundle_dir / "00_full_bundle_manifest.md").write_text(
        "# Manifest\n\n目标：P01-P09 full system runtime bundle\n", encoding="utf-8"
    )
    (bundle_dir / "04_stop_condition_protocol.md").write_text(
        "# Stop\n\n阻断：blocking issue -> Patch + Regression\n", encoding="utf-8"
    )
    (bundle_dir / "15_full_system_acceptance_protocol.md").write_text(
        "# E2E\n\nFull System E2E 准入与验收。\n", encoding="utf-8"
    )
    (bundle_dir / "patch_and_regression_loop.md").write_text(
        "# Patch And Regression Loop\n\n修复失败项并回归。\n", encoding="utf-8"
    )
    for phase in range(1, 10):
        (bundle_dir / f"p{phase:02d}_stage_data.md").write_text(
            f"# P{phase:02d} Stage Data\n\n输入 输出 handoff 状态码 missing 阻断 降级 验收 审计\n",
            encoding="utf-8",
        )
        (bundle_dir / f"p{phase:02d}_code_landing.md").write_text(
            f"# P{phase:02d} Code Landing\n\n代码骨架 目录 contracts schemas src tests fixtures replay handoff\n",
            encoding="utf-8",
        )
        (bundle_dir / f"p{phase:02d}_acceptance_check.md").write_text(
            f"# P{phase:02d} Acceptance Check\n\npytest replay handoff audit status no signing no broadcast\n",
            encoding="utf-8",
        )


def test_workflow_v4_bootstraps_seven_task_layers_and_generated_taskbooks(tmp_path):
    root = tmp_path
    _seed_minimal_bundle(root)

    result = FullSystemWorkflowV4(root).run(mode="plan-only")

    assert result["workflow_version"] == "full_system_workflow_v4"
    assert result["safety_boundary"] == {
        "paper_only": True,
        "real_trade_actions": [],
        "signing_enabled": False,
        "broadcast_enabled": False,
        "secret_access": "not_requested_not_used",
    }
    assert [layer["task_id"] for layer in result["task_layers"]] == EXPECTED_TASK_LAYERS
    assert result["final_status"] in {
        "FULL_SYSTEM_BUNDLE_READY",
        "FULL_SYSTEM_BUNDLE_READY_WITH_GAPS",
        "FULL_SYSTEM_BUNDLE_REJECTED",
    }
    assert result["final_status"] != "FULL_SYSTEM_BUNDLE_REJECTED"

    generated_dir = root / "task_books" / "full_system_runtime_bundle" / "generated" / "workflow_v4"
    assert (generated_dir / "task_0_full_system_bundle_bootstrap.md").exists()
    assert (generated_dir / "task_1_wave_1_p01_p03_foundation_runtime.md").exists()
    assert (generated_dir / "task_5_full_system_e2e_validation.md").exists()
    assert (generated_dir / "task_6_patch_regression_loop.md").exists()
    task_1_text = (generated_dir / "task_1_wave_1_p01_p03_foundation_runtime.md").read_text(encoding="utf-8")
    for required in ["目标", "边界", "输入", "输出", "handoff", "状态码", "missing", "阻断", "降级", "验收", "审计"]:
        assert required in task_1_text
    assert "真实交易" in task_1_text and "禁止" in task_1_text


def test_workflow_v4_scans_gaps_writes_audit_handoff_and_runtime_state(tmp_path):
    root = tmp_path
    _seed_minimal_bundle(root)
    # 故意制造一个缺口：缺少 P07 acceptance 文件，验证 scanner 不猜测，写入 gap register。
    (root / "task_books" / "full_system_runtime_bundle" / "p07_acceptance_check.md").unlink()

    result = FullSystemWorkflowV4(root).run(mode="plan-only")

    assert result["final_status"] == "FULL_SYSTEM_BUNDLE_READY_WITH_GAPS"
    assert any(gap["gap_id"] == "MISSING_PHASE_TASKBOOK_P07_ACCEPTANCE_CHECK" for gap in result["gap_register"])
    assert result["routing"]["current_allowed_task"] == "task_6_patch_regression_loop"
    assert result["routing"]["stop_condition_triggered"] is False

    runtime_state = json.loads(
        (root / "runtime_logs" / "full_system_runtime" / "workflow_v4_state.json").read_text(encoding="utf-8")
    )
    assert runtime_state["final_status"] == result["final_status"]
    assert runtime_state["task_layers"][0]["task_id"] == "task_0_full_system_bundle_bootstrap"
    assert runtime_state["routing"]["next_allowed_task"] == result["routing"]["next_allowed_task"]

    gap_register = (root / "reports" / "system_audit" / "full_system_workflow_v4_gap_register.json")
    audit_json = root / "reports" / "system_audit" / "full_system_workflow_v4_result.json"
    audit_md = root / "reports" / "system_audit" / "full_system_workflow_v4_audit.md"
    handoff_json = root / "shared_handoff" / "full_system_workflow_v4" / "workflow_v4_handoff_packet.json"
    for path in [gap_register, audit_json, audit_md, handoff_json]:
        assert path.exists(), path
    assert "MISSING_PHASE_TASKBOOK_P07_ACCEPTANCE_CHECK" in gap_register.read_text(encoding="utf-8")
    assert "Patch + Regression" in audit_md.read_text(encoding="utf-8")


def test_workflow_v4_cli_smoke(tmp_path):
    _seed_minimal_bundle(tmp_path)

    import subprocess
    import sys

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "modules.runtime.full_system_workflow_v4",
            "--root",
            str(tmp_path),
            "--mode",
            "plan-only",
        ],
        cwd="/root/sikk-gmgn",
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["workflow_version"] == "full_system_workflow_v4"
    assert Path(payload["audit_path"]).exists()
    assert Path(payload["runtime_state_path"]).exists()
