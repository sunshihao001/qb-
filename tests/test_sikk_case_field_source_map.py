import json
from pathlib import Path


def _write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def test_enrich_position_for_case_file_backfills_from_context_sources(tmp_path):
    from sikk_case_field_source_map import enrich_position_for_case_file

    root = tmp_path / "run"
    _write_json(root / "state_machine" / "candidate_states.json", {"候选状态": [{
        "代币地址": "TCASE",
        "代币符号": "CASE",
        "当前状态": "PAPER_READY",
        "discovery_market_cap_usd": 88888,
        "candidate_discovered_at": "2026-05-03T10:00:00Z",
        "signal_market_cap_usd": 99999,
        "signal_time": "2026-05-03T10:03:00Z",
    }]})
    _write_json(root / "wallet_structure" / "candidate_wallet_structure_summary.json", {"处理结果": [{
        "token_address": "TCASE",
        "wallet_structure_status": "WALLET_SUPPORT",
        "wallet_structure_score": 76,
        "wallet_risk_score": 24,
        "counterparty_pressure_score": 33,
        "data_quality_score": 82,
    }]})
    _write_json(root / "quote_security" / "candidate_quote_security_summary.json", {"处理结果": [{
        "代币地址": "TCASE",
        "最终权限": "ALLOW_CONFIRMATION_LAYER",
        "交易前状态": "READY_FOR_CONFIRMATION",
        "okx_price": 0.00012,
    }]})
    position = {
        "position_id": "paper-case-1",
        "token_address": "TCASE",
        "token_symbol": "CASE",
        "status": "OPEN",
        "paper_entry_time": "2026-05-03T10:04:00Z",
        "entry_market_cap_usd": 111111,
    }

    enriched = enrich_position_for_case_file(position, root)

    assert enriched["discovery_market_cap_usd"] == 88888
    assert enriched["signal_market_cap_usd"] == 99999
    assert enriched["wallet_structure_status"] == "WALLET_SUPPORT"
    assert enriched["wallet_structure_score"] == 76
    assert enriched["quote_gate"] == "ALLOW_CONFIRMATION_LAYER"
    assert enriched["security_gate"] == "READY_FOR_CONFIRMATION"
    assert enriched["entry_market_cap_usd"] == 111111
    assert enriched["case_field_sources"]["wallet_structure_score"].endswith("candidate_wallet_structure_summary.json")
    assert "discovery_market_cap_usd" not in enriched["case_missing_fields"]
    assert "不执行真实 swap" in enriched["case_field_source_boundary"]
