import json
from pathlib import Path


def _readiness_payload():
    return {
        "token": "TOKEN",
        "risk_gate": {
            "permission": "ALLOW_PAPER_TRADE_允许纸面交易",
            "risk_level": "低",
            "block_reasons": [],
            "pause_reasons": [],
            "allow_reasons": ["安全层通过"],
            "missing_evidence": [],
        },
        "signal": {
            "signal_level": "S4_强确认信号",
            "strategy_type": "SIKK-B 控盘箱体突破回踩",
            "signal_time": "2026-04-27 16:37:00 UTC",
            "signal_price": 0.00023386184,
            "confidence_score": 99,
            "evidence": ["突破控盘箱体"],
            "invalidation_reasons": [],
        },
        "position_plan": {
            "suggested_position_sol": 0.1,
            "max_position_sol": 0.2,
            "risk_per_trade_sol": 0.025,
            "stop_price": 0.00018,
            "stop_type": "结构止损",
            "position_reason": "按风险计算",
        },
        "exit_plan": {
            "hard_stop_price": 0.00018,
            "time_stop_minutes": 30,
            "take_profit_rules": [],
            "trailing_stop_rule": {},
            "emergency_exit_rules": [],
        },
    }


def test_v04_writes_five_pre_trade_review_files(tmp_path):
    from sikk_execution_adapter_base import QuoteResult, SecurityScanResult, TokenSide
    from sikk_quote_security_review import build_and_write_pre_trade_review

    paths = build_and_write_pre_trade_review(
        output_dir=tmp_path,
        readiness_payload=_readiness_payload(),
        chain="sol",
        wallet_address="Wallet1111111111111111111111111111111111",
        human_amount="0.01 SOL",
        quote_results=[
            QuoteResult("GMGN", "SOL", "TOKEN", "0.01", "1000", "980", 1.2, {"mock": True}),
            QuoteResult("OKX", "SOL", "TOKEN", "0.01", "990", "970", 1.4, {"mock": True}),
        ],
        security_scan_results=[
            SecurityScanResult("GMGN", "TOKEN", TokenSide.BUY, "LOW", [], {"mock": True}),
            SecurityScanResult("OKX", "TOKEN", TokenSide.BUY, "LOW", [], {"mock": True}),
        ],
        snapshot_time="2026-04-30T00:00:00Z",
    )

    assert set(paths) == {
        "trade_confirmation_ticket_md",
        "trade_confirmation_ticket_json",
        "quote_snapshot_json",
        "security_scan_report_json",
        "quote_security_decision_json",
    }
    for path in paths.values():
        assert Path(path).exists()
    assert json.loads(Path(paths["quote_security_decision_json"]).read_text(encoding="utf-8"))["final_permission"] == "ALLOW_CONFIRMATION_LAYER"


def test_quote_security_decision_pauses_when_quote_missing_or_scan_missing():
    from sikk_quote_security_review import build_quote_snapshot, build_security_scan_report, build_quote_security_decision

    quote_snapshot = build_quote_snapshot(
        token="TOKEN",
        chain="sol",
        wallet_address="Wallet1111111111111111111111111111111111",
        human_amount="0.01 SOL",
        quote_results=[],
        snapshot_time="2026-04-30T00:00:00Z",
    )
    security_report = build_security_scan_report(token="TOKEN", chain="sol", scan_results=[])
    decision = build_quote_security_decision(quote_snapshot, security_report)

    assert decision["final_permission"] == "PAUSE_NEED_CONFIRM"
    assert "缺少有效报价" in decision["reasons"]
    assert "安全扫描结果缺失" in "；".join(decision["reasons"])


def test_quote_security_decision_blocks_high_price_impact():
    from sikk_execution_adapter_base import QuoteResult, SecurityScanResult, TokenSide
    from sikk_quote_security_review import build_quote_snapshot, build_security_scan_report, build_quote_security_decision

    quote_snapshot = build_quote_snapshot(
        token="TOKEN",
        chain="sol",
        wallet_address="Wallet1111111111111111111111111111111111",
        human_amount="0.01 SOL",
        quote_results=[QuoteResult("GMGN", "SOL", "TOKEN", "0.01", "1000", "980", 12.5, {})],
        snapshot_time="2026-04-30T00:00:00Z",
    )
    security_report = build_security_scan_report(
        token="TOKEN",
        chain="sol",
        scan_results=[SecurityScanResult("OKX", "TOKEN", TokenSide.BUY, "LOW", [], {})],
    )
    decision = build_quote_security_decision(quote_snapshot, security_report)

    assert decision["final_permission"] == "BLOCK_BUY"
    assert any("价格影响过高" in reason for reason in decision["reasons"])


def test_quote_and_security_reports_write_standard_time_anchors():
    from sikk_execution_adapter_base import QuoteResult, SecurityScanResult, TokenSide
    from sikk_quote_security_review import build_quote_snapshot, build_security_scan_report, build_quote_security_decision

    quote_snapshot = build_quote_snapshot(
        token="TOKEN",
        chain="sol",
        wallet_address="Wallet1111111111111111111111111111111111",
        human_amount="0.01 SOL",
        quote_results=[
            QuoteResult("GMGN", "SOL", "TOKEN", "0.01", "1000", "980", 1.2, {"timestamp": "2026-05-04T11:59:58Z"}),
            QuoteResult("OKX", "SOL", "TOKEN", "0.01", "990", "970", 1.4, {}),
        ],
        snapshot_time="2026-05-04T12:00:00Z",
    )
    assert quote_snapshot["token_address"] == "TOKEN"
    assert quote_snapshot["quote_requested_at"] == "2026-05-04T12:00:00Z"
    assert quote_snapshot["quote_received_at"] == "2026-05-04T12:00:00Z"
    assert quote_snapshot["quote_time"] == "2026-05-04T11:59:58Z"
    assert quote_snapshot["quote_time_source"] == "provider_timestamp"
    assert quote_snapshot["quotes"][0]["quote_source"] == "GMGN"
    assert quote_snapshot["quotes"][1]["quote_time_source"] == "received_at_fallback"

    security_report = build_security_scan_report(
        token="TOKEN",
        chain="sol",
        scan_results=[SecurityScanResult("OKX", "TOKEN", TokenSide.BUY, "LOW", [], {"scanTime": "2026-05-04T11:59:59Z"})],
        snapshot_time="2026-05-04T12:00:01Z",
    )
    assert security_report["token_address"] == "TOKEN"
    assert security_report["security_scan_started_at"] == "2026-05-04T12:00:01Z"
    assert security_report["security_scan_finished_at"] == "2026-05-04T12:00:01Z"
    assert security_report["security_scan_time"] == "2026-05-04T11:59:59Z"
    assert security_report["security_scan_created_at"] == "2026-05-04T12:00:01Z"
    assert security_report["security_scan_time_source"] == "provider_timestamp"

    decision = build_quote_security_decision(quote_snapshot, security_report)
    assert decision["quote_time"] == "2026-05-04T11:59:58Z"
    assert decision["security_scan_time"] == "2026-05-04T11:59:59Z"
