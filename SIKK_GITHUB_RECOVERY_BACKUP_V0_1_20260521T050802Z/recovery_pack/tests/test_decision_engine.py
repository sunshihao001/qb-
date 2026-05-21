from __future__ import annotations

from pathlib import Path

from core.decision_engine import build_decision_ticket

RUN_DIR = Path("data/runs/4pMsh7JF5wXjkx8sK6gJgv14xkBy1kUoMv4ixN8npump/skill_raw_handoff_probe")
STRATEGY = Path("contracts/strategy_contract.json")


def test_build_decision_ticket_watch_due_to_quote_slippage_missing():
    ticket, evidence, counter, report = build_decision_ticket(RUN_DIR, STRATEGY)
    assert ticket["contract_hash"]
    assert ticket["feature_snapshot_path"].endswith("feature_snapshot.json")
    assert ticket["decision_status"] == "WATCH"
    assert ticket["paper_ready"] is False
    assert "quote_slippage_missing" in ticket["reason_codes"]
    assert ticket["risk_boundary"]["live_trading_enabled"] is False
    assert ticket["risk_boundary"]["swap_allowed"] is False
    assert ticket["risk_boundary"]["private_key_required"] is False
    assert evidence["supporting_fields"]
    assert any(item["reason_code"] == "gmgn_track_not_token_specific_not_used_as_strong_evidence" for item in counter)
    assert report["forbidden_downstream_created"] is False


def test_decision_ticket_does_not_create_trade_instruction():
    ticket, _, _, _ = build_decision_ticket(RUN_DIR, STRATEGY)
    forbidden = {"swap_instruction", "trade_instruction", "paper_position", "backtest_result"}
    assert forbidden.isdisjoint(ticket.keys())
