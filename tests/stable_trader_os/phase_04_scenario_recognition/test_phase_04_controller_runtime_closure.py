from __future__ import annotations

import csv
import json
from pathlib import Path

from modules.stable_trader_os.phase_04_scenario_recognition_controller import Phase04ScenarioRecognitionController


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = []
    for r in rows:
        for k in r:
            if k not in fields:
                fields.append(k)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def _make_phase03_package(tmp_path: Path, *, chip_status="CONTROL_RETAINED", transfer_status="CHIP_RETAINED", cp_score=10, wallet_status="WALLET_SUPPORT", cap_current=260000, kline_mode="second_stage") -> Path:
    run = tmp_path / "run"
    p03 = run / "03_chip_control"
    chip = p03 / "chip_control"
    fact = run / "01_data_fact" / "normalized"
    p02 = run / "02_wallet_structure" / "wallet_structure"
    token = "[REDACTED]"

    summary = {
        "token_address": token,
        "token_symbol": "TST",
        "snapshot_id": "snap-p4-test",
        "chip_control_status": chip_status,
        "dominant_side_status": "DOMINANT_SIDE_RETAINED" if chip_status == "CONTROL_RETAINED" else "DOMINANT_SIDE_DISTRIBUTING",
        "chip_transfer_status": transfer_status,
        "counterparty_pressure_score": cp_score,
        "early_wallet_exit_ratio": 0.1 if chip_status == "CONTROL_RETAINED" else 0.7,
        "distribution_risk_score": 15 if chip_status == "CONTROL_RETAINED" else 85,
        "market_cap_context_status": "MARKET_CAP_EXPANDED",
        "volume_chip_status": "VOLUME_SUPPORTS_CONTROL" if chip_status == "CONTROL_RETAINED" else "VOLUME_SUPPORTS_DISTRIBUTION",
        "positive_evidence": ["test_positive"],
        "negative_evidence": [],
        "missing_fields": [],
        "allowed_next_stage": "phase_04_scenario_recognition_controller",
        "handoff_status": "HANDOFF_READY",
    }
    dominant = {"token_address": token, "dominant_side_status": summary["dominant_side_status"], "reason": chip_status}
    transfer = {"token_address": token, "chip_transfer_status": transfer_status, "reason": chip_status}
    counterparty = {"token_address": token, "counterparty_pressure_score": cp_score, "counterparty_pressure_status": "COUNTERPARTY_PRESSURE_HIGH" if cp_score >= 55 else "COUNTERPARTY_PRESSURE_LOW"}
    distribution = {"token_address": token, "distribution_sell_status": "DISTRIBUTION_ACTIVE_SELL" if chip_status in {"ACTIVE_DISTRIBUTION", "PARTIAL_DISTRIBUTION"} else "DISTRIBUTION_INACTIVE"}
    backflow = {"token_address": token, "backflow_risk_status": "NO_BACKFLOW"}
    market = {"token_address": token, "discovery_market_cap_usd": 100000, "current_market_cap_usd": cap_current, "token_age_minutes": 180}
    wallet = {"phase_status": wallet_status, "hard_negative_triggered": wallet_status == "WALLET_BLOCK"}

    if kline_mode == "failed_breakout":
        rows = [
            {"time": "1", "open": 1, "high": 1.1, "low": 0.9, "close": 1.0, "volume_usd": 1000},
            {"time": "2", "open": 1.0, "high": 3.2, "low": 0.95, "close": 1.8, "volume_usd": 5000},
            {"time": "3", "open": 1.8, "high": 2.0, "low": 0.9, "close": 1.05, "volume_usd": 12000},
        ]
    elif kline_mode == "downtrend":
        rows = [
            {"time": "1", "open": 3, "high": 3.2, "low": 2.7, "close": 3.0, "volume_usd": 5000},
            {"time": "2", "open": 3, "high": 3.1, "low": 1.7, "close": 1.8, "volume_usd": 7000},
            {"time": "3", "open": 1.8, "high": 1.9, "low": 1.1, "close": 1.2, "volume_usd": 9000},
        ]
    else:
        rows = [
            {"time": "1", "open": 1, "high": 1.2, "low": 0.9, "close": 1.0, "volume_usd": 1000},
            {"time": "2", "open": 1.0, "high": 1.7, "low": 0.95, "close": 1.5, "volume_usd": 1500},
            {"time": "3", "open": 1.5, "high": 1.8, "low": 1.25, "close": 1.3, "volume_usd": 2600},
        ]

    _write_json(chip / "chip_control_summary.json", summary)
    _write_json(chip / "dominant_side_status.json", dominant)
    _write_json(chip / "chip_transfer_status.json", transfer)
    _write_json(chip / "counterparty_pressure.json", counterparty)
    _write_json(chip / "distribution_sell_state.json", distribution)
    _write_json(chip / "backflow_risk_state.json", backflow)
    _write_json(fact / "token_market_context.json", market)
    _write_json(p02 / "wallet_structure_decision.json", wallet)
    _write_csv(fact / "kline_normalized.csv", rows)

    handoff = {
        "phase": "phase_03_chip_control",
        "token_address": token,
        "token_symbol": "TST",
        "snapshot_id": "snap-p4-test",
        "chip_control_status": chip_status,
        "dominant_side_status": summary["dominant_side_status"],
        "chip_transfer_status": transfer_status,
        "handoff_files": {
            "chip_control_summary": str(chip / "chip_control_summary.json"),
            "dominant_side_status": str(chip / "dominant_side_status.json"),
            "chip_transfer_status": str(chip / "chip_transfer_status.json"),
            "counterparty_pressure": str(chip / "counterparty_pressure.json"),
            "distribution_sell_state": str(chip / "distribution_sell_state.json"),
            "backflow_risk_state": str(chip / "backflow_risk_state.json"),
            "wallet_structure_decision": str(p02 / "wallet_structure_decision.json"),
            "kline_normalized": str(fact / "kline_normalized.csv"),
            "token_market_context": str(fact / "token_market_context.json"),
        },
        "forced_scenario_checks": [],
        "allowed_next_stage": "phase_04_scenario_recognition_controller",
        "handoff_status": "HANDOFF_READY",
        "block_reason": "",
        "degrade_reason": "",
    }
    handoff_path = p03 / "handoff" / "phase_03_handoff_packet.json"
    _write_json(handoff_path, handoff)
    return handoff_path


def test_phase04_ready_input_writes_required_artifacts(tmp_path: Path):
    handoff = _make_phase03_package(tmp_path)
    result = Phase04ScenarioRecognitionController().run(phase03_handoff_file=handoff, output_dir=tmp_path / "out")
    assert result["phase"] == "phase_04_scenario_recognition_controller"
    artifacts = result["artifacts"]
    required = [
        "market_lifecycle_context",
        "price_structure_state",
        "volume_quality_state",
        "wallet_scenario_context",
        "chip_scenario_context",
        "market_cap_scenario_context",
        "scenario_scores",
        "primary_scenario",
        "scenario_counter_evidence",
        "scenario_hard_negative_checklist",
        "handoff_packet",
        "audit_report",
    ]
    for key in required:
        assert key in artifacts
        assert Path(artifacts[key]).exists(), key
    primary = json.loads(Path(artifacts["primary_scenario"]).read_text(encoding="utf-8"))
    assert primary["positive_evidence"]
    assert primary["allowed_next_stage"] == "phase_05_structure_position_controller"
    handoff_out = json.loads(Path(artifacts["handoff_packet"]).read_text(encoding="utf-8"))
    assert handoff_out["allowed_next_stage"] == "phase_05_structure_position_controller"
    assert handoff_out["phase_05_required_context"]["requires_avwap_completion_check"] is True


def test_risk_scenario_overrides_second_stage_candidate(tmp_path: Path):
    handoff = _make_phase03_package(tmp_path, chip_status="ACTIVE_DISTRIBUTION", cp_score=40, cap_current=800000, kline_mode="second_stage")
    result = Phase04ScenarioRecognitionController().run(phase03_handoff_file=handoff, output_dir=tmp_path / "out")
    primary = json.loads(Path(result["artifacts"]["primary_scenario"]).read_text(encoding="utf-8"))
    assert primary["primary_scenario"] in {"SCENARIO_TERMINAL_PUMP_DISTRIBUTION", "SCENARIO_HIGH_DISTRIBUTION"}
    assert primary["scenario_status"] in {"SCENARIO_DISTRIBUTION_RISK", "SCENARIO_REVIEW_ONLY"}
    assert primary["primary_scenario"] != "SCENARIO_SECOND_STAGE_EXPANSION_CANDIDATE"
    assert primary["hard_negative_triggered"] is True


def test_counterparty_transfer_blocks_positive_path(tmp_path: Path):
    handoff = _make_phase03_package(tmp_path, chip_status="TRANSFER_TO_COUNTERPARTY", transfer_status="CHIP_TRANSFER_TO_COUNTERPARTY", cp_score=85, kline_mode="second_stage")
    result = Phase04ScenarioRecognitionController().run(phase03_handoff_file=handoff, output_dir=tmp_path / "out")
    primary = json.loads(Path(result["artifacts"]["primary_scenario"]).read_text(encoding="utf-8"))
    hard = json.loads(Path(result["artifacts"]["scenario_hard_negative_checklist"]).read_text(encoding="utf-8"))
    assert primary["primary_scenario"] in {"SCENARIO_EXIT_LIQUIDITY_TRAP", "SCENARIO_COUNTERPARTY_WHALE_TRAP"}
    assert primary["allowed_next_stage"] in {"blocked", "review_only"}
    assert hard["hard_negative_triggered"] is True


def test_missing_required_handoff_ref_blocks(tmp_path: Path):
    handoff = _make_phase03_package(tmp_path)
    packet = json.loads(handoff.read_text(encoding="utf-8"))
    packet["handoff_files"].pop("chip_control_summary")
    handoff.write_text(json.dumps(packet, ensure_ascii=False, indent=2), encoding="utf-8")
    result = Phase04ScenarioRecognitionController().run(phase03_handoff_file=handoff, output_dir=tmp_path / "out")
    primary = json.loads(Path(result["artifacts"]["primary_scenario"]).read_text(encoding="utf-8"))
    assert primary["scenario_status"] == "SCENARIO_BLOCK"
    assert primary["handoff_status"] == "HANDOFF_BLOCKED"
    assert "chip_control_summary" in ",".join(primary["missing_fields"])


def test_phase04_static_contract_schema_controller_files_exist():
    root = Path("/root/sikk-gmgn")
    required = [
        root / "contracts/stable_trader_os/phase_04_scenario_recognition/phase_04_input_contract.json",
        root / "contracts/stable_trader_os/phase_04_scenario_recognition/phase_04_output_contract.json",
        root / "contracts/stable_trader_os/phase_04_scenario_recognition/phase_04_acceptance_matrix.json",
        root / "contracts/stable_trader_os/phase_04_scenario_recognition/required_fields.md",
        root / "contracts/stable_trader_os/phase_04_scenario_recognition/handoff_rules.md",
        root / "schemas/stable_trader_os/phase_04_scenario_recognition/primary_scenario.schema.json",
        root / "schemas/stable_trader_os/phase_04_scenario_recognition/phase_04_handoff_packet.schema.json",
        root / "configs/stable_trader_os/phase_04_scenario_recognition/phase_04_status_codes.json",
        root / "modules/stable_trader_os/phase_04_scenario_recognition_controller/runner.py",
        root / "skills/sikk_stable_trader_os/phase_controllers/phase_04_scenario_recognition_controller.md",
    ]
    missing = [str(p) for p in required if not p.exists() or p.stat().st_size == 0]
    assert not missing
