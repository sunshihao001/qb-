from pathlib import Path
import json
import csv

from modules.stable_trader_os.phase_01_data_fact import Phase01Runner, Phase01Validator

ROOT = Path(__file__).resolve().parents[3]
EXAMPLE = ROOT / "examples" / "stable_trader_os" / "phase_01_data_fact" / "mock_phase_01_input.json"


def test_phase_01_runner_generates_professional_runtime_artifacts(tmp_path):
    runner = Phase01Runner(ROOT)
    result = runner.run(EXAMPLE, tmp_path / "run")

    assert result["status"] in {"PASS", "PASS_WITH_WARNING", "PAUSE", "BLOCK"}
    assert result["phase_state"] in {"P01_COMPLETE", "P01_PAUSED", "P01_BLOCKED"}
    assert result["handoff_packet"].endswith("phase_01_to_phase_02_handoff_packet.json")

    required = [
        "01_data_fact/raw/raw_source_manifest.json",
        "01_data_fact/normalized/token_fact.json",
        "01_data_fact/normalized/wallet_fact_table.csv",
        "01_data_fact/normalized/trade_fact_table.csv",
        "01_data_fact/normalized/holder_fact_table.csv",
        "01_data_fact/normalized/kline_fact_table.csv",
        "01_data_fact/normalized/quote_fact.json",
        "01_data_fact/audit/phase_01_quality_gate.json",
        "01_data_fact/audit/missing_fields_report.md",
        "01_data_fact/audit/anomaly_fields_report.csv",
        "01_data_fact/audit/phase_01_runtime_trace.jsonl",
        "01_data_fact/audit/output_validation_report.json",
        "01_data_fact/audit/handoff_validation_report.json",
        "01_data_fact/audit/gaps.md",
        "01_data_fact/handoff/phase_01_to_phase_02_handoff_packet.json",
        "01_data_fact/reports/phase_01_data_fact_report.md",
        "01_data_fact/run_manifest.json",
    ]
    for rel in required:
        assert (tmp_path / "run" / rel).exists(), rel

    handoff = json.loads((tmp_path / "run" / "01_data_fact/handoff/phase_01_to_phase_02_handoff_packet.json").read_text())
    assert handoff["next_stage"] == "phase_02_wallet_structure_controller"
    assert handoff["phase"] == "phase_01_data_fact_controller"
    assert "buy_signal" not in json.dumps(handoff)
    assert "certain_dealer" not in json.dumps(handoff)

    quality = json.loads((tmp_path / "run" / "01_data_fact/audit/phase_01_quality_gate.json").read_text())
    assert quality["gate_status"] == result["status"]
    assert isinstance(quality["positive_evidence"], list)
    assert isinstance(quality["negative_evidence"], list)
    assert isinstance(quality["counter_evidence"], list)
    assert quality["forbidden_judgement_leakage"] is False

    trace_lines = (tmp_path / "run" / "01_data_fact/audit/phase_01_runtime_trace.jsonl").read_text().strip().splitlines()
    assert len(trace_lines) >= 8
    assert any(json.loads(line)["event"] == "handoff_written" for line in trace_lines)


def test_phase_01_validator_blocks_forbidden_judgement_leakage(tmp_path):
    bad_input = tmp_path / "bad_phase_01_input.json"
    bad_input.write_text(json.dumps({
        "run_id": "bad_run",
        "token_address": "TOKEN",
        "chain": "solana",
        "run_mode": "mock",
        "data_snapshot_time": "2026-05-09T00:00:00Z",
        "buy_signal": True,
        "sources": {}
    }, ensure_ascii=False))

    validator = Phase01Validator(ROOT)
    verdict = validator.validate_input(bad_input)
    assert verdict["allowed"] is False
    assert verdict["gate_status"] == "BLOCK"
    assert "forbidden_judgement_leakage" in verdict["hard_negative_reasons"]


def test_phase_01_cli_smoke_generates_manifest(tmp_path):
    import subprocess
    cmd = [
        "python3", "-m", "modules.stable_trader_os.phase_01_data_fact.cli",
        "--root", str(ROOT),
        "--input", str(EXAMPLE),
        "--output-dir", str(tmp_path / "cli_run")
    ]
    completed = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=True)
    payload = json.loads(completed.stdout)
    assert payload["run_manifest"].endswith("01_data_fact/run_manifest.json")
    manifest = json.loads((tmp_path / "cli_run" / "01_data_fact/run_manifest.json").read_text())
    assert manifest["phase_id"] == "phase_01_data_fact_controller"
    assert manifest["professional_level"] == "runtime_executable_with_contract_validation"
