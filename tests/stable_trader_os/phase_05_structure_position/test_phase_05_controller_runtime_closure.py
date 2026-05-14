from __future__ import annotations

import csv
import json
from pathlib import Path

from modules.stable_trader_os.phase_05_structure_position_controller import Phase05StructurePositionController


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _healthy_position_rows() -> list[dict]:
    return [
        {"time": "1", "open": 1.00, "high": 1.05, "low": 0.95, "close": 1.00, "volume_usd": 1000},
        {"time": "2", "open": 1.00, "high": 1.55, "low": 0.98, "close": 1.48, "volume_usd": 3200},
        {"time": "3", "open": 1.48, "high": 1.62, "low": 1.18, "close": 1.25, "volume_usd": 2400},
        {"time": "4", "open": 1.25, "high": 1.38, "low": 1.08, "close": 1.18, "volume_usd": 2600},
        {"time": "5", "open": 1.18, "high": 1.42, "low": 1.04, "close": 1.34, "volume_usd": 3600},
        {"time": "6", "open": 1.34, "high": 1.52, "low": 1.28, "close": 1.46, "volume_usd": 4200},
    ]


def _overextended_rows() -> list[dict]:
    return [
        {"time": "1", "open": 1.0, "high": 1.1, "low": 0.9, "close": 1.0, "volume_usd": 1000},
        {"time": "2", "open": 1.0, "high": 1.6, "low": 0.95, "close": 1.45, "volume_usd": 2000},
        {"time": "3", "open": 1.45, "high": 1.5, "low": 1.08, "close": 1.15, "volume_usd": 1800},
        {"time": "4", "open": 1.15, "high": 2.8, "low": 1.12, "close": 2.65, "volume_usd": 9000},
        {"time": "5", "open": 2.65, "high": 3.5, "low": 2.55, "close": 3.35, "volume_usd": 12000},
    ]


def _phase05_package(
    tmp_path: Path,
    *,
    scenario_status: str = "SCENARIO_SECOND_STAGE_CANDIDATE",
    primary_scenario: str = "SCENARIO_SECOND_STAGE_EXPANSION_CANDIDATE",
    rows: list[dict] | None = None,
    chip_status: str = "CONTROL_RETAINED",
    wallet_status: str = "WALLET_SUPPORT",
) -> Path:
    run = tmp_path / "run"
    p04 = run / "04_scenario_recognition"
    p03 = run / "03_chip_control" / "chip_control"
    p02 = run / "02_wallet_structure" / "wallet_structure"
    p01 = run / "01_data_fact" / "normalized"
    token = "[REDACTED]"
    rows = rows or _healthy_position_rows()

    primary = {
        "phase": "phase_04_scenario_recognition",
        "token_address": token,
        "token_symbol": "TST",
        "snapshot_id": "snap-p5-test",
        "primary_scenario": primary_scenario,
        "scenario_status": scenario_status,
        "positive_evidence": ["phase04_positive"],
        "counter_evidence": [],
        "hard_negative_triggered": scenario_status in {"SCENARIO_BLOCK", "SCENARIO_DISTRIBUTION_RISK", "SCENARIO_TRAP_RISK"},
        "hard_negative_reasons": ["risk_scene"] if scenario_status in {"SCENARIO_BLOCK", "SCENARIO_DISTRIBUTION_RISK", "SCENARIO_TRAP_RISK"} else [],
        "allowed_next_stage": "phase_05_structure_position_controller" if scenario_status not in {"SCENARIO_BLOCK", "SCENARIO_REVIEW_ONLY"} else "blocked",
        "handoff_status": "HANDOFF_READY" if scenario_status not in {"SCENARIO_BLOCK", "SCENARIO_REVIEW_ONLY"} else "HANDOFF_BLOCKED",
    }
    counter = {"counter_evidence_items": [], "hard_negative_items": []}
    hard = {"hard_negative_triggered": primary["hard_negative_triggered"], "hard_negative_reasons": primary["hard_negative_reasons"]}
    market = {"token_address": token, "token_symbol": "TST", "discovery_market_cap_usd": 100000, "current_market_cap_usd": 260000, "token_age_minutes": 180}
    chip = {"token_address": token, "chip_control_status": chip_status, "chip_transfer_status": "CHIP_RETAINED", "counterparty_pressure_score": 12}
    wallet = {"phase_status": wallet_status, "wallet_structure_status": wallet_status, "hard_negative_triggered": wallet_status == "WALLET_BLOCK"}

    _write_json(p04 / "scenario_decision" / "primary_scenario.json", primary)
    _write_json(p04 / "scenario_decision" / "scenario_counter_evidence.json", counter)
    _write_json(p04 / "scenario_decision" / "scenario_hard_negative_checklist.json", hard)
    _write_json(p04 / "scenario_scores" / "scenario_scores.json", {"scenarios": []})
    _write_json(p03 / "chip_control_summary.json", chip)
    _write_json(p02 / "wallet_structure_decision.json", wallet)
    _write_json(p01 / "token_market_context.json", market)
    _write_csv(p01 / "kline_normalized.csv", rows)

    handoff = {
        "phase": "phase_04_scenario_recognition",
        "token_address": token,
        "token_symbol": "TST",
        "snapshot_id": "snap-p5-test",
        "snapshot_time": "2026-05-09T00:00:00Z",
        "scenario_status": scenario_status,
        "primary_scenario": primary_scenario,
        "handoff_files": {
            "primary_scenario": str(p04 / "scenario_decision" / "primary_scenario.json"),
            "scenario_scores": str(p04 / "scenario_scores" / "scenario_scores.json"),
            "scenario_counter_evidence": str(p04 / "scenario_decision" / "scenario_counter_evidence.json"),
            "scenario_hard_negative_checklist": str(p04 / "scenario_decision" / "scenario_hard_negative_checklist.json"),
            "kline_normalized": str(p01 / "kline_normalized.csv"),
            "token_market_context": str(p01 / "token_market_context.json"),
            "chip_control_summary": str(p03 / "chip_control_summary.json"),
            "wallet_structure_decision": str(p02 / "wallet_structure_decision.json"),
        },
        "phase_05_required_context": {
            "requires_avwap_completion_check": True,
            "requires_poc_context_check": True,
            "requires_failure_test_check": True,
            "requires_fatigue_filter": True,
            "requires_position_overextension_check": True,
            "blocked_position_confirmation": scenario_status in {"SCENARIO_BLOCK", "SCENARIO_REVIEW_ONLY", "SCENARIO_DISTRIBUTION_RISK", "SCENARIO_TRAP_RISK"},
        },
        "allowed_next_stage": primary["allowed_next_stage"],
        "handoff_status": primary["handoff_status"],
        "block_reason": "risk_scene" if primary["hard_negative_triggered"] else "",
        "degrade_reason": "",
    }
    handoff_path = p04 / "handoff" / "phase_04_handoff_packet.json"
    _write_json(handoff_path, handoff)
    return handoff_path


def test_phase05_ready_input_writes_required_artifacts_and_handoff(tmp_path: Path):
    handoff = _phase05_package(tmp_path)
    result = Phase05StructurePositionController().run(phase04_handoff_file=handoff, output_dir=tmp_path / "out")
    assert result["phase"] == "phase_05_structure_position_controller"
    artifacts = result["artifacts"]
    required = [
        "scenario_position_constraints",
        "poc_context",
        "fixed_range_volume_profile",
        "avwap_anchor_context",
        "avwap_acceptance",
        "retracement_context",
        "position_volume_confirmation",
        "adx_noise_filter",
        "failure_test_result",
        "avwap_completion_gate",
        "fatigue_filter_result",
        "position_overextension_check",
        "structure_position_hard_negative_checklist",
        "structure_position_decision",
        "handoff_packet",
        "audit_report",
    ]
    for key in required:
        assert key in artifacts
        assert Path(artifacts[key]).exists(), key
    decision = json.loads(Path(artifacts["structure_position_decision"]).read_text(encoding="utf-8"))
    assert decision["completion_status"] == "COMPLETION_PASS"
    assert decision["structure_position_status"] == "POSITION_VALID"
    assert decision["completion_passed_count"] >= 2
    assert decision["allowed_next_stage"] == "phase_06_strategy_gate_controller"
    handoff_out = json.loads(Path(artifacts["handoff_packet"]).read_text(encoding="utf-8"))
    assert handoff_out["allowed_next_stage"] == "phase_06_strategy_gate_controller"
    assert handoff_out["phase_06_required_context"]["completion_status"] == "COMPLETION_PASS"


def test_scenario_block_cannot_be_repaired_by_position_layer(tmp_path: Path):
    handoff = _phase05_package(tmp_path, scenario_status="SCENARIO_BLOCK", primary_scenario="SCENARIO_EXIT_LIQUIDITY_TRAP")
    result = Phase05StructurePositionController().run(phase04_handoff_file=handoff, output_dir=tmp_path / "out")
    decision = json.loads(Path(result["artifacts"]["structure_position_decision"]).read_text(encoding="utf-8"))
    assert decision["completion_status"] == "COMPLETION_BLOCKED"
    assert decision["handoff_status"] == "HANDOFF_BLOCKED"
    assert decision["hard_negative_triggered"] is True
    assert any("phase04" in r or "SCENARIO_BLOCK" in r for r in decision["hard_negative_reasons"])


def test_adx_alone_never_passes_completion_gate(tmp_path: Path):
    rows = [
        {"time": "1", "open": 1.0, "high": 1.4, "low": 0.9, "close": 1.3, "volume_usd": 1000},
        {"time": "2", "open": 1.3, "high": 1.45, "low": 1.0, "close": 1.05, "volume_usd": 1500},
        {"time": "3", "open": 1.05, "high": 1.5, "low": 1.0, "close": 1.12, "volume_usd": 4500},
        {"time": "4", "open": 1.12, "high": 1.55, "low": 1.02, "close": 1.16, "volume_usd": 5000},
    ]
    handoff = _phase05_package(tmp_path, rows=rows)
    result = Phase05StructurePositionController().run(phase04_handoff_file=handoff, output_dir=tmp_path / "out")
    gate = json.loads(Path(result["artifacts"]["avwap_completion_gate"]).read_text(encoding="utf-8"))
    assert gate["adx_noise_rejected"] is True
    assert gate["avwap_acceptance_pass"] is False or gate["failure_test_pass"] is False
    assert gate["completion_status"] != "COMPLETION_PASS"


def test_overextended_position_blocks_or_reviews_next_stage(tmp_path: Path):
    handoff = _phase05_package(tmp_path, rows=_overextended_rows())
    result = Phase05StructurePositionController().run(phase04_handoff_file=handoff, output_dir=tmp_path / "out")
    decision = json.loads(Path(result["artifacts"]["structure_position_decision"]).read_text(encoding="utf-8"))
    assert decision["position_extension_status"] in {"POSITION_OVEREXTENDED", "POSITION_CHASING_RISK"}
    assert decision["handoff_status"] == "HANDOFF_BLOCKED"
    assert decision["allowed_next_stage"] in {"blocked", "review_only"}


def test_phase05_static_contract_schema_controller_files_exist():
    root = Path("/root/sikk-gmgn")
    required = [
        root / "contracts/stable_trader_os/phase_05_structure_position/phase_05_input_contract.json",
        root / "contracts/stable_trader_os/phase_05_structure_position/phase_05_output_contract.json",
        root / "contracts/stable_trader_os/phase_05_structure_position/required_fields.md",
        root / "contracts/stable_trader_os/phase_05_structure_position/handoff_rules.md",
        root / "schemas/stable_trader_os/phase_05_structure_position/structure_position_decision.schema.json",
        root / "schemas/stable_trader_os/phase_05_structure_position/phase_05_handoff_packet.schema.json",
        root / "configs/stable_trader_os/phase_05_structure_position/phase_05_status_codes.json",
        root / "modules/stable_trader_os/phase_05_structure_position_controller/runner.py",
        root / "skills/sikk_stable_trader_os/phase_controllers/phase_05_structure_position_controller.md",
    ]
    missing = [str(p) for p in required if not p.exists() or p.stat().st_size == 0]
    assert not missing
