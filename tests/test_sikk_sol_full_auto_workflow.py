import json
import subprocess
import sys
from pathlib import Path

from sikk_sol_full_auto_workflow import run_full_auto_workflow


def test_full_auto_workflow_runs_all_layers_and_writes_reports(tmp_path):
    result = run_full_auto_workflow(output_root=tmp_path, mode="sample", max_candidates=3)

    assert result["safety_boundary"]["paper_only"] is True
    assert result["safety_boundary"]["real_swap_enabled"] is False
    assert result["workflow_status"] == "COMPLETED_WITH_VERIFICATION"

    required = [
        "active_task_state_json",
        "execution_log_jsonl",
        "verification_report_json",
        "final_report_md",
        "state_machine_json",
        "workflow_manifest_json",
    ]
    for key in required:
        assert Path(result[key]).exists(), key

    verification = json.loads(Path(result["verification_report_json"]).read_text(encoding="utf-8"))
    assert verification["overall_status"] == "PASS"
    assert verification["no_real_trading"] is True
    assert verification["stage_outputs_checked"] >= 5

    state_payload = json.loads(Path(result["state_machine_json"]).read_text(encoding="utf-8"))
    states = {row["token_address"]: row["final_state"] for row in state_payload["states"]}
    assert states["SAFEPASS111111111111111111111111111111111111"] == "PAPER_READY"
    assert states["SAFEBLOCK2222222222222222222222222222222222"] == "EXCLUDE"
    assert states["MARKETWATCH33333333333333333333333333333333"] == "WATCHING"

    md = Path(result["final_report_md"]).read_text(encoding="utf-8")
    assert "兼容路线 one-shot 工作流" in md
    assert "不是钱包结构分析主入口" in md
    assert "不执行真实交易" in md
    assert "PAPER_READY" in md


def test_full_auto_workflow_cli_sample_mode(tmp_path):
    completed = subprocess.run(
        [
            sys.executable,
            "sikk_sol_full_auto_workflow.py",
            "--output-root",
            str(tmp_path),
            "--mode",
            "sample",
            "--max-candidates",
            "2",
            "--paper-only",
        ],
        cwd="/root/sikk-gmgn",
        text=True,
        capture_output=True,
        check=True,
    )
    payload = json.loads(completed.stdout)
    assert payload["workflow_status"] == "COMPLETED_WITH_VERIFICATION"
    assert Path(payload["workflow_manifest_json"]).exists()
    assert payload["safety_boundary"]["broadcast_enabled"] is False
    assert payload["compatibility_route"]["not_primary_entry"] is True
    assert "sikk_candidate_wallet_structure_pipeline.py" in payload["compatibility_route"]["canonical_wallet_system"]
    assert Path(payload["readiness_json"]).exists()
    assert Path(payload["collector_command_plan_json"]).exists()


def test_full_auto_workflow_auto_readonly_no_network_uses_adapter(tmp_path):
    token = "So11111111111111111111111111111111111111112"
    result = run_full_auto_workflow(output_root=tmp_path, mode="auto-readonly", max_candidates=5, token_address=token, allow_network=False)
    assert result["safety_boundary"]["paper_only"] is True
    assert result["workflow_status"] in {"COMPLETED_WITH_VERIFICATION", "COMPLETED_WITH_VALIDATION_FAILURES"}
    adapter_path = tmp_path / "source_wallet_bot" / "paper" / token / "wallet_data" / "normalized" / "gmgn_okx_raw_stage_outputs.json"
    assert adapter_path.exists()
    manifest = tmp_path / "source_wallet_bot" / "paper" / token / "manifest" / "token_output_manifest.json"
    assert manifest.exists()
    text = adapter_path.read_text(encoding="utf-8") + manifest.read_text(encoding="utf-8")
    assert "swap execute" not in text
    assert "private_key" not in text
    assert "broadcast" not in text


def test_full_auto_workflow_refuses_without_paper_only_cli(tmp_path):
    completed = subprocess.run(
        [sys.executable, "sikk_sol_full_auto_workflow.py", "--output-root", str(tmp_path), "--mode", "sample"],
        cwd="/root/sikk-gmgn",
        text=True,
        capture_output=True,
    )
    assert completed.returncode != 0
    assert "必须显式传入 --paper-only" in completed.stderr or "必须显式传入 --paper-only" in completed.stdout



def test_full_auto_workflow_manifest_marks_legacy_compat_route(tmp_path):
    result = run_full_auto_workflow(output_root=tmp_path, mode="sample", max_candidates=1)
    manifest = json.loads(Path(result["workflow_manifest_json"]).read_text(encoding="utf-8"))
    assert manifest["compatibility_route"]["route_type"] == "legacy_compat_one_shot"
    assert manifest["compatibility_route"]["not_primary_entry"] is True
    assert manifest["compatibility_route"]["canonical_wallet_system"][0] == "modules/source_wallet_bot"
    assert "wallet_structure pipeline" in manifest["compatibility_route"]["compat_policy"]
