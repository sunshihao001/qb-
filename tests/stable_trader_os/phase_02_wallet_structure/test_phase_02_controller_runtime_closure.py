from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from modules.stable_trader_os.phase_02_wallet_structure_controller.runner import Phase02WalletStructureController

TOKEN = "So11111111111111111111111111111111111111112"


def _write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def _write_wallet_rows(path: Path, rows: list[dict]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path


def _base_handoff(wallet_file: Path, **overrides) -> dict:
    packet = {
        "phase": "phase_01_data_fact_controller",
        "token_address": TOKEN,
        "token_symbol": "TEST",
        "chain": "sol",
        "snapshot_id": "snapshot-test-001",
        "phase_status": "DATA_OK",
        "allow_next_stage": True,
        "next_stage": "phase_02_wallet_structure_controller",
        "required_files_for_next_stage": {"gmgn_traders": str(wallet_file)},
        "missing_fields": [],
        "hard_negative_triggered": False,
    }
    packet.update(overrides)
    return packet


def test_phase02_ready_input_writes_standard_artifacts_and_handoff(tmp_path: Path):
    wallet_file = _write_wallet_rows(
        tmp_path / "wallet_trade_normalized.csv",
        [
            {
                "wallet_address": "wallet_alpha",
                "address": "wallet_alpha",
                "token_address": TOKEN,
                "token_symbol": "TEST",
                "buy_amount_usd": "1200",
                "sell_amount_usd": "100",
                "profit": "500",
                "gmgn_tags": "smart_money",
                "funding_source_address": "fund_src_1",
                "first_buy_seconds": "45",
            },
            {
                "wallet_address": "wallet_beta",
                "address": "wallet_beta",
                "token_address": TOKEN,
                "token_symbol": "TEST",
                "buy_amount_usd": "900",
                "sell_amount_usd": "50",
                "profit": "300",
                "gmgn_tags": "new_wallet",
                "funding_source_address": "fund_src_1",
                "first_buy_seconds": "55",
            },
        ],
    )
    handoff_file = _write_json(tmp_path / "phase_01_handoff_packet.json", _base_handoff(wallet_file))

    result = Phase02WalletStructureController().run(phase01_handoff_file=handoff_file, output_dir=tmp_path / "run")

    assert result["phase"] == "phase_02_wallet_structure_controller"
    assert result["phase_status"] in {
        "WALLET_SUPPORT",
        "WALLET_PAUSE",
        "WALLET_BLOCK",
        "WALLET_UNKNOWN",
        "WALLET_DATA_WEAK",
        "WALLET_SAME_SOURCE_DETECTED",
        "WALLET_DISTRIBUTION_DETECTED",
        "WALLET_BACKFLOW_DETECTED",
        "WALLET_COUNTERPARTY_PRESSURE",
    }
    artifacts = result["artifacts"]
    for key in [
        "wallet_cleaning_result",
        "excluded_address_list",
        "wallet_entity_profile",
        "current_token_behavior",
        "same_source_groups",
        "distribution_paths",
        "backflow_paths",
        "wallet_classification",
        "gmgn_note_table",
        "wallet_structure_decision",
        "handoff_packet",
        "audit_report",
        "output_validation_report",
        "handoff_validation_report",
        "missing_fields_report",
        "gaps",
    ]:
        assert Path(artifacts[key]).exists(), key

    decision = json.loads(Path(artifacts["wallet_structure_decision"]).read_text(encoding="utf-8"))
    for field in [
        "positive_evidence",
        "negative_evidence",
        "counter_evidence",
        "hard_negative_triggered",
        "hard_negative_reasons",
        "missing_fields",
        "confidence_level",
        "risk_level",
        "evidence_level",
        "allowed_next_stage",
        "blocked_next_stage_reason",
    ]:
        assert field in decision

    handoff = json.loads(Path(artifacts["handoff_packet"]).read_text(encoding="utf-8"))
    assert handoff["next_stage"] == "phase_03_chip_control_controller"
    assert handoff["phase_status"] == result["phase_status"]
    assert set(handoff["required_files_for_next_stage"]).issuperset(
        {"wallet_structure_decision", "wallet_classification", "same_source_groups", "distribution_paths", "backflow_paths", "gmgn_note_table"}
    )


def test_phase02_blocks_when_phase01_handoff_is_hard_negative(tmp_path: Path):
    wallet_file = _write_wallet_rows(tmp_path / "wallet_trade_normalized.csv", [{"wallet_address": "wallet_alpha", "address": "wallet_alpha"}])
    handoff_file = _write_json(
        tmp_path / "phase_01_handoff_packet.json",
        _base_handoff(wallet_file, phase_status="DATA_INVALID", allow_next_stage=False, hard_negative_triggered=True),
    )

    result = Phase02WalletStructureController().run(phase01_handoff_file=handoff_file, output_dir=tmp_path / "run")
    handoff = json.loads(Path(result["artifacts"]["handoff_packet"]).read_text(encoding="utf-8"))

    assert result["phase_status"] == "WALLET_BLOCK"
    assert handoff["allow_next_stage"] is False
    assert handoff["hard_negative_triggered"] is True
    assert "upstream_data_invalid" in handoff["block_reason"]


def test_phase02_gmgn_tag_alone_does_not_decide_role_or_support(tmp_path: Path):
    wallet_file = _write_wallet_rows(
        tmp_path / "wallet_trade_normalized.csv",
        [
            {"wallet_address": "wallet_tag_only", "address": "wallet_tag_only", "token_address": TOKEN, "gmgn_tags": "smart_money"},
        ],
    )
    handoff_file = _write_json(tmp_path / "phase_01_handoff_packet.json", _base_handoff(wallet_file))

    result = Phase02WalletStructureController().run(phase01_handoff_file=handoff_file, output_dir=tmp_path / "run")
    classification = Path(result["artifacts"]["wallet_classification"])
    with classification.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    assert rows
    assert result["phase_status"] != "WALLET_SUPPORT"
    assert all(row.get("role_name") != "确定庄家" for row in rows)
    decision = json.loads(Path(result["artifacts"]["wallet_structure_decision"]).read_text(encoding="utf-8"))
    assert decision["evidence_level"] in {"E0", "E1", "E2", "E3", "E4", "E5"}


def test_phase02_missing_wallet_fact_entry_degrades_or_blocks_with_audit(tmp_path: Path):
    handoff_file = _write_json(
        tmp_path / "phase_01_handoff_packet.json",
        _base_handoff(tmp_path / "missing.csv", required_files_for_next_stage={}),
    )

    result = Phase02WalletStructureController().run(phase01_handoff_file=handoff_file, output_dir=tmp_path / "run")
    assert result["phase_status"] in {"WALLET_DATA_WEAK", "WALLET_BLOCK"}
    audit = Path(result["artifacts"]["audit_report"]).read_text(encoding="utf-8")
    missing = Path(result["artifacts"]["missing_fields_report"]).read_text(encoding="utf-8")
    assert "missing_wallet_trade_fact_entry" in audit
    assert "Missing Fields" in missing


def test_phase02_contract_and_schema_files_exist_and_define_required_fields():
    root = Path("/root/sikk-gmgn")
    required = [
        root / "contracts/stable_trader_os/phase_02_wallet_structure/phase_02_input_contract.json",
        root / "contracts/stable_trader_os/phase_02_wallet_structure/phase_02_output_contract.json",
        root / "contracts/stable_trader_os/phase_02_wallet_structure/phase_02_to_phase_03_contract.json",
        root / "contracts/stable_trader_os/phase_02_wallet_structure/phase_02_acceptance_matrix.json",
        root / "schemas/stable_trader_os/phase_02_wallet_structure/wallet_structure_decision.schema.json",
        root / "schemas/stable_trader_os/phase_02_wallet_structure/phase_02_handoff_packet.schema.json",
        root / "configs/stable_trader_os/phase_02_wallet_structure/phase_02_status_codes.json",
        root / "configs/stable_trader_os/phase_02_wallet_structure/hard_negative_rules.json",
    ]
    for path in required:
        assert path.exists(), path
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data

    decision_schema = json.loads((root / "schemas/stable_trader_os/phase_02_wallet_structure/wallet_structure_decision.schema.json").read_text(encoding="utf-8"))
    required_fields = set(decision_schema.get("required", []))
    assert {"positive_evidence", "negative_evidence", "counter_evidence", "hard_negative_triggered", "missing_fields"}.issubset(required_fields)
