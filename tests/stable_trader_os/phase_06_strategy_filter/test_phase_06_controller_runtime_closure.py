from __future__ import annotations

import csv
import json
from pathlib import Path

from modules.stable_trader_os.phase_06_strategy_gate_controller import Phase06StrategyGateController


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


def _phase06_package(
    tmp_path: Path,
    *,
    data_status: str = "DATA_OK",
    wallet_status: str = "WALLET_SUPPORT",
    chip_status: str = "CONTROL_RETAINED",
    scenario_status: str = "SCENARIO_SECOND_STAGE_CANDIDATE",
    position_status: str = "POSITION_VALID",
    completion_status: str = "COMPLETION_PASS",
    fatigue_status: str = "FATIGUE_PASS",
    extension_status: str = "POSITION_NORMAL",
    missing_required: bool = False,
) -> Path:
    run = tmp_path / "run"
    p01 = run / "01_data_fact" / "normalized"
    p01_audit = run / "01_data_fact" / "audit"
    p01_handoff = run / "01_data_fact" / "handoff"
    p02 = run / "02_wallet_structure"
    p02_norm = p02 / "normalized"
    p02_handoff = p02 / "handoff"
    p03 = run / "03_chip_control"
    p03_chip = p03 / "chip_control"
    p03_handoff = p03 / "handoff"
    p04 = run / "04_scenario_recognition"
    p04_decision = p04 / "scenario_decision"
    p04_handoff = p04 / "handoff"
    p05 = run / "05_structure_position"
    p05_decision = p05 / "position_decision"
    p05_handoff = p05 / "handoff"
    token = "[REDACTED]"

    phase01_handoff_packet = {
        "phase": "phase_01_data_fact_controller",
        "token_address": token,
        "snapshot_id": "snap-p6-test",
        "phase_status": data_status,
        "gate_status": "PASS" if data_status == "DATA_OK" else "BLOCK",
        "handoff_status": "HANDOFF_READY" if data_status != "DATA_INVALID" else "HANDOFF_BLOCKED",
        "hard_negative_triggered": data_status == "DATA_INVALID",
        "hard_negative_reasons": [data_status] if data_status == "DATA_INVALID" else [],
        "missing_fields": [],
    }
    data_quality_summary = {
        "phase_status": data_status,
        "data_quality_status": data_status,
        "quality_score": 92 if data_status == "DATA_OK" else 20,
        "missing_fields": [],
        "hard_negative_triggered": data_status == "DATA_INVALID",
    }
    token_market_context = {
        "token_address": token,
        "token_symbol": "TST",
        "snapshot_id": "snap-p6-test",
        "discovery_market_cap_usd": 100000,
        "current_market_cap_usd": 260000,
        "token_age_minutes": 180,
    }
    quote_security = {
        "quote_valid": True,
        "security_status": "SECURITY_OK",
        "liquidity_usd": 120000,
        "slippage_bps_estimate": 120,
        "honeypot_risk": False,
    }
    _write_json(p01_handoff / "phase_01_handoff_packet.json", phase01_handoff_packet)
    _write_json(p01_handoff / "phase_01_to_phase_02_handoff_packet.json", phase01_handoff_packet)
    _write_json(p01_audit / "data_quality_summary.json", data_quality_summary)
    _write_json(p01 / "token_market_context.json", token_market_context)
    _write_json(p01 / "quote_security_normalized.json", quote_security)

    wallet_decision = {
        "phase_status": wallet_status,
        "wallet_structure_status": wallet_status,
        "evidence_level": "E4" if wallet_status == "WALLET_SUPPORT" else "E1",
        "risk_level": "LOW" if wallet_status == "WALLET_SUPPORT" else "HIGH",
        "positive_evidence": ["same-source accumulation evidence"] if wallet_status == "WALLET_SUPPORT" else [],
        "negative_evidence": [],
        "counter_evidence": [],
        "hard_negative_triggered": wallet_status == "WALLET_BLOCK",
        "hard_negative_reasons": [wallet_status] if wallet_status == "WALLET_BLOCK" else [],
        "allowed_next_stage": "phase_03_chip_control_controller" if wallet_status != "WALLET_BLOCK" else "blocked",
    }
    _write_json(p02 / "wallet_structure_decision.json", wallet_decision)
    _write_csv(p02_norm / "wallet_classification.csv", [
        {"wallet_address": "[REDACTED]", "role": "same_source_group", "evidence_level": "E4", "risk_level": "LOW"},
        {"wallet_address": "[REDACTED]", "role": "result_wallet", "evidence_level": "E3", "risk_level": "LOW"},
    ])
    _write_json(p02_handoff / "phase_02_handoff_packet.json", {
        "phase": "phase_02_wallet_structure_controller",
        "phase_status": wallet_status,
        "handoff_status": "HANDOFF_READY" if wallet_status != "WALLET_BLOCK" else "HANDOFF_BLOCKED",
        "hard_negative_triggered": wallet_status == "WALLET_BLOCK",
        "block_reason": wallet_status if wallet_status == "WALLET_BLOCK" else "",
    })

    chip_summary = {
        "chip_control_status": chip_status,
        "dominant_side_status": "DOMINANT_SIDE_RETAINED" if chip_status == "CONTROL_RETAINED" else "DOMINANT_SIDE_DISTRIBUTING",
        "chip_transfer_status": "CHIP_RETAINED" if chip_status != "TRANSFER_TO_COUNTERPARTY" else "CHIP_TRANSFER_TO_COUNTERPARTY",
        "counterparty_pressure_score": 12 if chip_status == "CONTROL_RETAINED" else 85,
        "distribution_risk_score": 15 if chip_status == "CONTROL_RETAINED" else 90,
        "positive_evidence": ["early wallet retention"] if chip_status == "CONTROL_RETAINED" else [],
        "negative_evidence": [],
        "missing_fields": [],
    }
    _write_json(p03_chip / "chip_control_summary.json", chip_summary)
    _write_json(p03_chip / "dominant_side_status.json", {"dominant_side_status": chip_summary["dominant_side_status"]})
    _write_json(p03_chip / "chip_transfer_status.json", {"chip_transfer_status": chip_summary["chip_transfer_status"]})
    _write_json(p03_chip / "counterparty_pressure.json", {"counterparty_pressure_score": chip_summary["counterparty_pressure_score"]})
    _write_json(p03_handoff / "phase_03_handoff_packet.json", {
        "phase": "phase_03_chip_control",
        "chip_control_status": chip_status,
        "handoff_status": "HANDOFF_READY" if chip_status not in {"STRUCTURE_COLLAPSE"} else "HANDOFF_BLOCKED",
        "hard_negative_triggered": chip_status in {"ACTIVE_DISTRIBUTION", "TRANSFER_TO_COUNTERPARTY", "STRUCTURE_COLLAPSE"},
    })

    primary_scenario = {
        "primary_scenario": "SCENARIO_SECOND_STAGE_EXPANSION_CANDIDATE" if scenario_status == "SCENARIO_SECOND_STAGE_CANDIDATE" else "SCENARIO_EXIT_LIQUIDITY_TRAP",
        "scenario_status": scenario_status,
        "positive_evidence": ["scenario supports second-stage candidate"] if scenario_status == "SCENARIO_SECOND_STAGE_CANDIDATE" else [],
        "counter_evidence": [],
        "hard_negative_triggered": scenario_status in {"SCENARIO_BLOCK", "SCENARIO_TRAP_RISK", "SCENARIO_DISTRIBUTION_RISK"},
        "hard_negative_reasons": [scenario_status] if scenario_status in {"SCENARIO_BLOCK", "SCENARIO_TRAP_RISK", "SCENARIO_DISTRIBUTION_RISK"} else [],
        "allowed_next_stage": "phase_05_structure_position_controller" if scenario_status not in {"SCENARIO_BLOCK", "SCENARIO_TRAP_RISK", "SCENARIO_DISTRIBUTION_RISK"} else "blocked",
    }
    _write_json(p04_decision / "primary_scenario.json", primary_scenario)
    _write_json(p04_decision / "scenario_counter_evidence.json", {"counter_evidence_items": []})
    _write_json(p04_decision / "scenario_hard_negative_checklist.json", {"hard_negative_triggered": primary_scenario["hard_negative_triggered"], "hard_negative_reasons": primary_scenario["hard_negative_reasons"]})
    _write_json(p04_handoff / "phase_04_handoff_packet.json", {
        "phase": "phase_04_scenario_recognition",
        "scenario_status": scenario_status,
        "handoff_status": "HANDOFF_READY" if not primary_scenario["hard_negative_triggered"] else "HANDOFF_BLOCKED",
        "hard_negative_triggered": primary_scenario["hard_negative_triggered"],
    })

    position_decision = {
        "structure_position_status": position_status,
        "completion_status": completion_status,
        "fatigue_status": fatigue_status,
        "position_extension_status": extension_status,
        "completion_passed_count": 3 if completion_status == "COMPLETION_PASS" else 0,
        "positive_evidence": ["AVWAP acceptance", "failure test passed", "POC accepted"] if completion_status == "COMPLETION_PASS" else [],
        "negative_evidence": [],
        "counter_evidence": [],
        "hard_negative_triggered": completion_status == "COMPLETION_FAIL" or fatigue_status == "FATIGUE_BLOCK" or extension_status == "POSITION_OVEREXTENDED",
        "hard_negative_reasons": [x for x in [completion_status if completion_status == "COMPLETION_FAIL" else "", fatigue_status if fatigue_status == "FATIGUE_BLOCK" else "", extension_status if extension_status == "POSITION_OVEREXTENDED" else ""] if x],
        "allowed_next_stage": "phase_06_strategy_gate_controller" if position_status == "POSITION_VALID" and completion_status == "COMPLETION_PASS" and fatigue_status != "FATIGUE_BLOCK" and extension_status != "POSITION_OVEREXTENDED" else "blocked",
        "handoff_status": "HANDOFF_READY" if position_status == "POSITION_VALID" and completion_status == "COMPLETION_PASS" and fatigue_status != "FATIGUE_BLOCK" and extension_status != "POSITION_OVEREXTENDED" else "HANDOFF_BLOCKED",
    }
    _write_json(p05_decision / "structure_position_decision.json", position_decision)
    _write_json(p05_decision / "avwap_completion_gate.json", {"completion_status": completion_status, "completion_passed_count": position_decision["completion_passed_count"]})
    _write_json(p05_decision / "failure_test_result.json", {"failure_test_status": "FAILURE_TEST_PASS" if completion_status == "COMPLETION_PASS" else "FAILURE_TEST_FAIL"})
    _write_json(p05_decision / "fatigue_filter_result.json", {"fatigue_status": fatigue_status})
    _write_json(p05_decision / "position_overextension_check.json", {"position_extension_status": extension_status})

    handoff_files = {
        "phase_01_handoff_packet": str(p01_handoff / "phase_01_handoff_packet.json"),
        "data_quality_summary": str(p01_audit / "data_quality_summary.json"),
        "phase_02_handoff_packet": str(p02_handoff / "phase_02_handoff_packet.json"),
        "wallet_structure_decision": str(p02 / "wallet_structure_decision.json"),
        "wallet_classification": str(p02_norm / "wallet_classification.csv"),
        "phase_03_handoff_packet": str(p03_handoff / "phase_03_handoff_packet.json"),
        "chip_control_summary": str(p03_chip / "chip_control_summary.json"),
        "dominant_side_status": str(p03_chip / "dominant_side_status.json"),
        "chip_transfer_status": str(p03_chip / "chip_transfer_status.json"),
        "counterparty_pressure": str(p03_chip / "counterparty_pressure.json"),
        "phase_04_handoff_packet": str(p04_handoff / "phase_04_handoff_packet.json"),
        "primary_scenario": str(p04_decision / "primary_scenario.json"),
        "scenario_counter_evidence": str(p04_decision / "scenario_counter_evidence.json"),
        "scenario_hard_negative_checklist": str(p04_decision / "scenario_hard_negative_checklist.json"),
        "phase_05_handoff_packet": str(p05_handoff / "phase_05_handoff_packet.json"),
        "structure_position_decision": str(p05_decision / "structure_position_decision.json"),
        "avwap_completion_gate": str(p05_decision / "avwap_completion_gate.json"),
        "failure_test_result": str(p05_decision / "failure_test_result.json"),
        "fatigue_filter_result": str(p05_decision / "fatigue_filter_result.json"),
        "position_overextension_check": str(p05_decision / "position_overextension_check.json"),
        "quote_security_normalized": str(p01 / "quote_security_normalized.json"),
        "token_market_context": str(p01 / "token_market_context.json"),
    }
    if missing_required:
        handoff_files.pop("wallet_structure_decision")
    phase05_handoff = {
        "phase": "phase_05_structure_position_controller",
        "token_address": token,
        "token_symbol": "TST",
        "snapshot_id": "snap-p6-test",
        "completion_status": completion_status,
        "structure_position_status": position_status,
        "position_extension_status": extension_status,
        "handoff_files": handoff_files,
        "phase_06_required_context": {
            "completion_status": completion_status,
            "structure_position_status": position_status,
            "requires_a_plus_check": True,
            "requires_p1_position_check": True,
            "requires_hard_negative_check": True,
            "requires_execution_risk_gate": True,
        },
        "allowed_next_stage": position_decision["allowed_next_stage"],
        "handoff_status": position_decision["handoff_status"],
        "hard_negative_triggered": position_decision["hard_negative_triggered"],
        "block_reason": ";".join(position_decision["hard_negative_reasons"]),
        "degrade_reason": "",
    }
    handoff_path = p05_handoff / "phase_05_handoff_packet.json"
    _write_json(handoff_path, phase05_handoff)
    return handoff_path


def test_phase06_ready_a_plus_p1_writes_gate_artifacts_and_handoff(tmp_path: Path):
    handoff = _phase06_package(tmp_path)
    result = Phase06StrategyGateController().run(phase05_handoff_file=handoff, output_dir=tmp_path / "out")
    assert result["phase"] == "phase_06_strategy_gate_controller"
    artifacts = result["artifacts"]
    required = [
        "upstream_state_summary",
        "upstream_state_matrix",
        "hard_negative_checklist",
        "structure_quality_assessment",
        "position_quality_assessment",
        "strategy_template_match",
        "risk_reward_check",
        "evidence_chain_check",
        "multi_dimensional_strategy_scores",
        "a_plus_p1_result",
        "strategy_gate_decision",
        "handoff_packet",
        "audit_report",
    ]
    for key in required:
        assert key in artifacts
        assert Path(artifacts[key]).exists(), key
    decision = json.loads(Path(artifacts["strategy_gate_decision"]).read_text(encoding="utf-8"))
    assert decision["strategy_gate_status"] in {"PAPER_READY", "READY_FOR_CONFIRMATION", "A_PLUS_P1_PASS"}
    assert decision["a_plus_structure_pass"] is True
    assert decision["p1_position_pass"] is True
    assert decision["hard_negative_triggered"] is False
    assert decision["invalidation_conditions"]
    assert decision["required_execution_checks"]
    assert decision["allowed_next_stage"] == "phase_07_execution_risk_controller"
    forbidden_words = ["买入", "开仓", "实盘执行", "现在上车", "buy now", "execute now"]
    assert not any(word in json.dumps(decision, ensure_ascii=False).lower() for word in forbidden_words)
    handoff_out = json.loads(Path(artifacts["handoff_packet"]).read_text(encoding="utf-8"))
    assert handoff_out["phase"] == "phase_06_strategy_gate_controller"
    assert handoff_out["next_stage"] == "phase_07_execution_risk_controller"
    assert handoff_out["phase_status"] in {"PAPER_READY", "READY_FOR_CONFIRMATION", "A_PLUS_P1_PASS"}


def test_phase06_upstream_hard_negative_cannot_be_overridden(tmp_path: Path):
    handoff = _phase06_package(tmp_path, chip_status="ACTIVE_DISTRIBUTION")
    result = Phase06StrategyGateController().run(phase05_handoff_file=handoff, output_dir=tmp_path / "out")
    decision = json.loads(Path(result["artifacts"]["strategy_gate_decision"]).read_text(encoding="utf-8"))
    hard = json.loads(Path(result["artifacts"]["hard_negative_checklist"]).read_text(encoding="utf-8"))
    assert decision["strategy_gate_status"] in {"STRATEGY_BLOCK", "REVIEW_ONLY", "STRATEGY_PAUSE"}
    assert decision["strategy_gate_status"] != "PAPER_READY"
    assert decision["hard_negative_triggered"] is True
    assert hard["hard_negative_triggered"] is True
    assert any("ACTIVE_DISTRIBUTION" in reason for reason in decision["hard_negative_reasons"])
    assert decision["allowed_next_stage"] in {"blocked", "review_only"}


def test_phase06_position_overextended_blocks_paper_ready(tmp_path: Path):
    handoff = _phase06_package(tmp_path, extension_status="POSITION_OVEREXTENDED")
    result = Phase06StrategyGateController().run(phase05_handoff_file=handoff, output_dir=tmp_path / "out")
    decision = json.loads(Path(result["artifacts"]["strategy_gate_decision"]).read_text(encoding="utf-8"))
    assert decision["strategy_gate_status"] in {"STRATEGY_BLOCK", "REVIEW_ONLY"}
    assert decision["strategy_gate_status"] != "PAPER_READY"
    assert decision["block_reason"]
    assert any("POSITION_OVEREXTENDED" in reason for reason in decision["hard_negative_reasons"])


def test_phase06_missing_required_input_blocks_with_missing_report(tmp_path: Path):
    handoff = _phase06_package(tmp_path, missing_required=True)
    result = Phase06StrategyGateController().run(phase05_handoff_file=handoff, output_dir=tmp_path / "out")
    decision = json.loads(Path(result["artifacts"]["strategy_gate_decision"]).read_text(encoding="utf-8"))
    assert decision["input_status"] == "PHASE_06_INPUT_BLOCKED"
    assert decision["strategy_gate_status"] == "STRATEGY_BLOCK"
    assert "wallet_structure_decision" in ",".join(decision["missing_fields"])
    assert Path(result["artifacts"]["missing_fields_report"]).exists()


def test_phase06_static_contract_schema_controller_files_exist():
    root = Path("/root/sikk-gmgn")
    required = [
        root / "research_loop/phase_06_strategy_filter_layer/README.md",
        root / "contracts/stable_trader_os/phase_06_strategy_filter/phase_06_input_contract.json",
        root / "contracts/stable_trader_os/phase_06_strategy_filter/phase_06_output_contract.json",
        root / "contracts/stable_trader_os/phase_06_strategy_filter/required_fields.md",
        root / "contracts/stable_trader_os/phase_06_strategy_filter/handoff_rules.md",
        root / "schemas/stable_trader_os/phase_06_strategy_filter/strategy_gate_decision.schema.json",
        root / "schemas/stable_trader_os/phase_06_strategy_filter/phase_06_handoff_packet.schema.json",
        root / "configs/stable_trader_os/phase_06_strategy_filter/phase_06_status_codes.json",
        root / "modules/stable_trader_os/phase_06_strategy_gate_controller/runner.py",
        root / "skills/sikk_stable_trader_os/phase_controllers/phase_06_strategy_gate_controller.md",
    ]
    missing = [str(p) for p in required if not p.exists() or p.stat().st_size == 0]
    assert not missing
