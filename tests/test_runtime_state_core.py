import json
from pathlib import Path

import pytest

from modules.runtime.candidate_state import CandidateState, create_candidate_state
from modules.runtime.contract_validator import ContractValidator
from modules.runtime.hard_negative_engine import HardNegativeEngine
from modules.runtime.phase_runner import PhaseRunner


def test_create_candidate_state_has_required_evidence_and_handoff_fields():
    state = create_candidate_state(
        token_address="Token111111111111111111111111111111111111",
        mode="manual",
        current_phase="phase_01_data_fact_layer",
        previous_phase="phase_00_system_constitution",
        next_phase="phase_02_wallet_structure_layer",
        status_code="DATA_WEAK",
        positive_evidence=[{"field": "raw_wallet_rows", "value": 3}],
        negative_evidence=[{"field": "kline_ohlcv", "reason": "missing"}],
        counter_evidence=[{"rule": "insufficient_market_data"}],
        missing_fields=["kline_ohlcv"],
    )

    payload = state.to_dict()

    assert payload["token_address"] == "Token111111111111111111111111111111111111"
    assert payload["status_family"] == "PAUSE"
    assert payload["hard_negative_trigger"] is None
    assert payload["confidence_level"] == "low"
    assert payload["invalidation_condition"] == "counter_evidence_or_hard_negative_triggered"
    assert payload["next_phase"] == "phase_02_wallet_structure_layer"
    assert "positive_evidence" in payload
    assert "negative_evidence" in payload
    assert "counter_evidence" in payload


def test_contract_validator_reports_missing_required_fields(tmp_path):
    contract = tmp_path / "contract.json"
    payload = tmp_path / "input.json"
    contract.write_text(json.dumps({"required_fields": ["token_address", "wallet_rows", "kline_ohlcv"]}))
    payload.write_text(json.dumps({"token_address": "Token111", "wallet_rows": []}))

    result = ContractValidator().validate_file(payload, contract)

    assert result.ok is False
    assert result.status_code == "DATA_WEAK"
    assert result.missing_fields == ["kline_ohlcv"]
    assert result.positive_evidence[0]["field"] == "token_address"
    assert result.negative_evidence[0]["field"] == "kline_ohlcv"


def test_contract_validator_invalid_json_blocks(tmp_path):
    contract = tmp_path / "contract.json"
    payload = tmp_path / "input.json"
    contract.write_text(json.dumps({"required_fields": ["token_address"]}))
    payload.write_text("not-json")

    result = ContractValidator().validate_file(payload, contract)

    assert result.ok is False
    assert result.status_code == "DATA_INVALID"
    assert result.hard_negative_trigger == "INVALID_JSON"


def test_hard_negative_engine_blocks_paper_ready_when_trigger_matches_registry():
    registry = {
        "rules": [
            {
                "code": "DATA_INVALID",
                "match_status_codes": ["DATA_INVALID"],
                "block_status_family": "BLOCK",
                "reason": "数据无效",
            },
            {
                "code": "FATIGUE_BLOCK",
                "match_status_codes": ["FATIGUE_BLOCK"],
                "block_status_family": "BLOCK",
                "reason": "疲劳拖延硬否决",
            },
        ]
    }

    result = HardNegativeEngine(registry).evaluate({"status_code": "FATIGUE_BLOCK"})

    assert result.blocked is True
    assert result.trigger == "FATIGUE_BLOCK"
    assert result.status_family == "BLOCK"
    assert "疲劳" in result.reason


def test_phase_runner_writes_candidate_state_output_and_audit(tmp_path):
    root = tmp_path / "sikk"
    phase_dir = root / "research_loop" / "phase_01_data_fact_layer"
    contract_dir = root / "contracts" / "phase_01_data_fact_layer"
    phase_dir.mkdir(parents=True)
    contract_dir.mkdir(parents=True)
    (phase_dir / "04_output_contract.md").write_text("core output: data_quality_summary.json")
    (contract_dir / "input_contract.json").write_text(json.dumps({"required_fields": ["token_address", "wallet_rows"]}))

    input_file = root / "input.json"
    input_file.write_text(json.dumps({"token_address": "Token111", "wallet_rows": [{"wallet": "A"}]}))

    result = PhaseRunner(root).run(
        phase="phase_01_data_fact_layer",
        mode="manual",
        token="Token111",
        input_file=input_file,
    )

    assert result.status_code == "DATA_OK"
    assert result.output_path.exists()
    assert result.audit_path.exists()
    output = json.loads(result.output_path.read_text())
    assert output["current_phase"] == "phase_01_data_fact_layer"
    assert output["status_family"] == "ALLOW"
    assert output["next_phase"] == "phase_02_wallet_structure_layer"
    assert output["positive_evidence"]
    assert "读取输入" in result.audit_path.read_text()


def test_phase_runner_missing_field_writes_pause_state(tmp_path):
    root = tmp_path / "sikk"
    contract_dir = root / "contracts" / "phase_01_data_fact_layer"
    contract_dir.mkdir(parents=True)
    (contract_dir / "input_contract.json").write_text(json.dumps({"required_fields": ["token_address", "wallet_rows", "kline_ohlcv"]}))

    input_file = root / "input.json"
    input_file.write_text(json.dumps({"token_address": "Token111", "wallet_rows": []}))

    result = PhaseRunner(root).run(
        phase="phase_01_data_fact_layer",
        mode="manual",
        token="Token111",
        input_file=input_file,
    )

    output = json.loads(result.output_path.read_text())
    assert result.status_code == "DATA_WEAK"
    assert output["status_family"] == "PAUSE"
    assert output["missing_fields"] == ["kline_ohlcv"]
    assert output["counter_evidence"]
