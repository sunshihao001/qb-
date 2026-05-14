from __future__ import annotations

import csv
import json
from pathlib import Path

from modules.stable_trader_os.phase_03_chip_control_controller.runner import Phase03ChipControlController

TOKEN = "So11111111111111111111111111111111111111112"


def _write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def _write_csv(path: Path, rows: list[dict]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    if not fieldnames:
        fieldnames = ["wallet_address"]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path


def _base_phase02_package(tmp_path: Path, *, status: str = "WALLET_SUPPORT", hard_negative: bool = False) -> Path:
    wallet_classification = _write_csv(
        tmp_path / "phase02/address_classification.csv",
        [
            {
                "wallet_address": "wallet_alpha",
                "address": "wallet_alpha",
                "primary_role": "疑似结构执行钱包",
                "role_name": "same-source executor",
                "evidence_level": "E4",
                "risk_level": "R1",
                "first_buy_seconds": "45",
            },
            {
                "wallet_address": "wallet_beta",
                "address": "wallet_beta",
                "primary_role": "疑似结构执行钱包",
                "role_name": "new wallet executor",
                "evidence_level": "E4",
                "risk_level": "R1",
                "first_buy_seconds": "55",
            },
        ],
    )
    same_source = _write_csv(
        tmp_path / "phase02/same_source_groups.csv",
        [
            {"group_id": "G1", "wallet_address": "wallet_alpha"},
            {"group_id": "G1", "wallet_address": "wallet_beta"},
        ],
    )
    distribution = _write_csv(tmp_path / "phase02/distribution_paths.csv", [])
    backflow = _write_csv(tmp_path / "phase02/backflow_paths.csv", [])
    decision = _write_json(
        tmp_path / "phase02/wallet_structure_decision.json",
        {
            "phase_status": status,
            "positive_evidence": ["same_source_group_detected"],
            "negative_evidence": [],
            "counter_evidence": [],
            "hard_negative_triggered": hard_negative,
            "hard_negative_reasons": [],
        },
    )
    holder = _write_csv(
        tmp_path / "phase01/holder_normalized.csv",
        [
            {"wallet_address": "wallet_alpha", "current_token_balance": "900", "initial_token_amount": "1000"},
            {"wallet_address": "wallet_beta", "current_token_balance": "850", "initial_token_amount": "1000"},
        ],
    )
    market = _write_json(
        tmp_path / "phase01/token_market_context.json",
        {"token_address": TOKEN, "discovery_market_cap_usd": 100000, "current_market_cap_usd": 180000},
    )
    trades = _write_csv(
        tmp_path / "phase01/wallet_trade_normalized.csv",
        [
            {"wallet_address": "wallet_alpha", "buy_token_amount": "1000", "sell_token_amount": "100", "buy_amount_usd": "1000", "sell_amount_usd": "100"},
            {"wallet_address": "wallet_beta", "buy_token_amount": "1000", "sell_token_amount": "150", "buy_amount_usd": "900", "sell_amount_usd": "50"},
        ],
    )
    kline = _write_csv(tmp_path / "phase01/kline_normalized.csv", [{"volume_usd": "1000"}, {"volume_usd": "1200"}])
    handoff = {
        "phase": "phase_02_wallet_structure",
        "token_address": TOKEN,
        "token_symbol": "TEST",
        "snapshot_id": "snapshot-phase03-test",
        "phase_status": status,
        "allow_next_stage": not hard_negative,
        "next_stage": "phase_03_chip_control_controller",
        "required_files_for_next_stage": {
            "wallet_structure_decision": str(decision),
            "wallet_classification": str(wallet_classification),
            "same_source_groups": str(same_source),
            "distribution_paths": str(distribution),
            "backflow_paths": str(backflow),
            "holder_normalized": str(holder),
            "token_market_context": str(market),
            "wallet_trade_normalized": str(trades),
            "kline_normalized": str(kline),
        },
        "missing_fields": [],
        "hard_negative_triggered": hard_negative,
        "block_reason": "upstream_block" if hard_negative else "",
    }
    return _write_json(tmp_path / "phase02/handoff/phase_02_handoff_packet.json", handoff)


def test_phase03_ready_input_writes_standard_artifacts_and_handoff(tmp_path: Path):
    handoff_file = _base_phase02_package(tmp_path)

    result = Phase03ChipControlController().run(phase02_handoff_file=handoff_file, output_dir=tmp_path / "run")

    assert result["phase"] == "phase_03_chip_control_controller"
    assert result["phase_status"] in {
        "CONTROL_RETAINED",
        "CONTROL_WEAKENING",
        "PARTIAL_DISTRIBUTION",
        "ACTIVE_DISTRIBUTION",
        "TRANSFER_TO_COUNTERPARTY",
        "STRUCTURE_COLLAPSE",
        "RE_ACCUMULATION",
        "UNKNOWN_CONTROL",
    }
    artifacts = result["artifacts"]
    for key in [
        "structure_wallet_sets",
        "early_chip_state",
        "early_exit_detection",
        "same_source_group_chip_state",
        "distribution_sell_state",
        "backflow_risk_state",
        "counterparty_pressure",
        "dominant_side_status",
        "chip_transfer_status",
        "chip_control_summary",
        "handoff_packet",
        "chip_control_report",
        "audit_report",
        "output_validation_report",
        "handoff_validation_report",
        "missing_fields_report",
        "gaps",
    ]:
        assert Path(artifacts[key]).exists(), key

    summary = json.loads(Path(artifacts["chip_control_summary"]).read_text(encoding="utf-8"))
    for field in [
        "positive_evidence",
        "negative_evidence",
        "counter_evidence",
        "hard_negative_triggered",
        "hard_negative_reasons",
        "missing_fields",
        "allowed_next_stage",
        "handoff_status",
    ]:
        assert field in summary
    assert all("庄" not in str(value) and "买" not in str(value) for value in summary.values())

    handoff = json.loads(Path(artifacts["handoff_packet"]).read_text(encoding="utf-8"))
    assert handoff["allowed_next_stage"] in {"phase_04_scenario_recognition_controller", "blocked"}
    assert set(handoff["handoff_files"]).issuperset(
        {"chip_control_summary", "dominant_side_status", "chip_transfer_status", "counterparty_pressure", "distribution_sell_state", "backflow_risk_state"}
    )


def test_phase03_propagates_phase02_wallet_block_as_structure_collapse(tmp_path: Path):
    handoff_file = _base_phase02_package(tmp_path, status="WALLET_BLOCK", hard_negative=True)

    result = Phase03ChipControlController().run(phase02_handoff_file=handoff_file, output_dir=tmp_path / "run")
    handoff = json.loads(Path(result["artifacts"]["handoff_packet"]).read_text(encoding="utf-8"))

    assert result["phase_status"] == "STRUCTURE_COLLAPSE"
    assert handoff["handoff_status"] == "HANDOFF_BLOCKED"
    assert "phase_02_wallet_block_or_hard_negative" in handoff["block_reason"]


def test_phase03_distribution_cluster_sell_triggers_active_distribution(tmp_path: Path):
    handoff_file = _base_phase02_package(tmp_path)
    handoff = json.loads(handoff_file.read_text(encoding="utf-8"))
    distribution = _write_csv(
        tmp_path / "phase02/distribution_paths.csv",
        [
            {"receiver": "wallet_alpha", "from_address": "core"},
            {"receiver": "wallet_beta", "from_address": "core"},
        ],
    )
    trades = _write_csv(
        tmp_path / "phase01/wallet_trade_normalized.csv",
        [
            {"wallet_address": "wallet_alpha", "buy_token_amount": "1000", "sell_token_amount": "900", "sell_amount_usd": "900"},
            {"wallet_address": "wallet_beta", "buy_token_amount": "1000", "sell_token_amount": "850", "sell_amount_usd": "850"},
        ],
    )
    handoff["required_files_for_next_stage"]["distribution_paths"] = str(distribution)
    handoff["required_files_for_next_stage"]["wallet_trade_normalized"] = str(trades)
    handoff_file.write_text(json.dumps(handoff, ensure_ascii=False, indent=2), encoding="utf-8")

    result = Phase03ChipControlController().run(phase02_handoff_file=handoff_file, output_dir=tmp_path / "run")
    summary = json.loads(Path(result["artifacts"]["chip_control_summary"]).read_text(encoding="utf-8"))

    assert result["phase_status"] == "ACTIVE_DISTRIBUTION"
    assert summary["hard_negative_triggered"] is True
    assert "distribution_receivers_cluster_sell" in summary["hard_negative_reasons"]


def test_phase03_missing_optional_inputs_degrades_to_unknown_or_weak_evidence_with_audit(tmp_path: Path):
    handoff_file = _base_phase02_package(tmp_path)
    handoff = json.loads(handoff_file.read_text(encoding="utf-8"))
    for key in ["holder_normalized", "token_market_context", "wallet_trade_normalized", "same_source_groups", "distribution_paths", "backflow_paths"]:
        handoff["required_files_for_next_stage"].pop(key, None)
    handoff_file.write_text(json.dumps(handoff, ensure_ascii=False, indent=2), encoding="utf-8")

    result = Phase03ChipControlController().run(phase02_handoff_file=handoff_file, output_dir=tmp_path / "run")
    summary = json.loads(Path(result["artifacts"]["chip_control_summary"]).read_text(encoding="utf-8"))
    audit = Path(result["artifacts"]["audit_report"]).read_text(encoding="utf-8")

    assert result["phase_status"] in {"UNKNOWN_CONTROL", "CONTROL_WEAKENING", "CONTROL_RETAINED"}
    assert summary["missing_fields"]
    assert "Missing 字段" in audit


def test_phase03_contract_schema_config_files_exist_and_define_required_fields():
    root = Path("/root/sikk-gmgn")
    required = [
        root / "contracts/stable_trader_os/phase_03_chip_control/phase_03_input_contract.json",
        root / "contracts/stable_trader_os/phase_03_chip_control/phase_03_output_contract.json",
        root / "contracts/stable_trader_os/phase_03_chip_control/phase_03_acceptance_matrix.json",
        root / "contracts/stable_trader_os/phase_03_chip_control/required_fields.md",
        root / "contracts/stable_trader_os/phase_03_chip_control/handoff_rules.md",
        root / "schemas/stable_trader_os/phase_03_chip_control/chip_control_summary.schema.json",
        root / "schemas/stable_trader_os/phase_03_chip_control/phase_03_handoff_packet.schema.json",
        root / "configs/stable_trader_os/phase_03_chip_control/phase_03_status_codes.json",
        root / "configs/stable_trader_os/phase_03_chip_control/hard_negative_rules.json",
        root / "skills/sikk_stable_trader_os/phase_controllers/phase_03_chip_control_controller.md",
    ]
    for path in required:
        assert path.exists(), path
        assert path.read_text(encoding="utf-8").strip(), path

    summary_schema = json.loads((root / "schemas/stable_trader_os/phase_03_chip_control/chip_control_summary.schema.json").read_text(encoding="utf-8"))
    assert {"positive_evidence", "negative_evidence", "counter_evidence", "hard_negative_triggered", "missing_fields"}.issubset(
        set(summary_schema.get("required", []))
    )
