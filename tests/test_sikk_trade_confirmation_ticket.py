import json


def test_confirmation_ticket_requires_confirm_text_and_contains_no_execute_command():
    from sikk_auto_trade_types import RiskGateResult, SignalLevel, SignalResult, TradePermission, PositionPlan, ExitPlan
    from sikk_execution_adapter_base import PreTradeSecurityDecision, QuoteResult
    from sikk_trade_confirmation_ticket import build_trade_confirmation_ticket

    risk_gate = RiskGateResult(
        permission=TradePermission.ALLOW_PAPER_TRADE,
        risk_level="低",
        block_reasons=[],
        pause_reasons=[],
        allow_reasons=["安全层通过"],
        missing_evidence=[],
    )
    signal = SignalResult(
        signal_level=SignalLevel.S4,
        strategy_type="SIKK-B 控盘箱体突破回踩",
        signal_time="2026-04-27 16:37:00 UTC",
        signal_price=0.00023386184,
        confidence_score=99.0,
        evidence=["突破控盘箱体上沿"],
        invalidation_reasons=[],
    )
    position = PositionPlan(
        suggested_position_sol=0.123312,
        max_position_sol=0.2,
        risk_per_trade_sol=0.025,
        stop_price=0.000186449324276,
        stop_type="结构止损",
        position_reason="按风险计算",
    )
    exit_plan = ExitPlan(
        hard_stop_price=0.000186449324276,
        time_stop_minutes=30,
        take_profit_rules=[{"触发收益率": 50, "卖出比例": 25}],
        trailing_stop_rule={"峰值回撤_pct": 35},
        emergency_exit_rules=["跌破控盘底"],
    )
    security = PreTradeSecurityDecision(
        permission="ALLOW",
        risk_level="LOW",
        requires_user_confirmation=False,
        reasons=["多源安全扫描未发现 HIGH/CRITICAL 买入风险"],
        source_count=2,
    )
    quotes = [
        QuoteResult("GMGN", "SOL", "TOKEN", "10000000", "12345", "12000", 1.2, {"route": "gmgn"}),
        QuoteResult("OKX", "SOL", "TOKEN", "0.01", "12200", "11900", 1.5, {"route": "okx"}),
    ]

    ticket = build_trade_confirmation_ticket(
        token="TOKEN",
        chain="sol",
        wallet_address="Wallet1111111111111111111111111111111111",
        human_amount="0.01 SOL",
        risk_gate=risk_gate,
        signal=signal,
        position_plan=position,
        exit_plan=exit_plan,
        security_decision=security,
        quote_results=quotes,
    )

    assert ticket.required_confirmation_text == "CONFIRM_REAL_TRADE"
    assert ticket.real_execution_allowed is True
    assert "CONFIRM_REAL_TRADE" in ticket.markdown
    assert "onchainos swap execute" not in ticket.markdown
    assert "gmgn-cli swap" not in ticket.markdown
    assert ticket.summary["信号等级"] == "S4_强确认信号"
    json.dumps(ticket.to_dict(), ensure_ascii=False)


def test_confirmation_ticket_blocks_when_security_blocks_or_signal_invalid():
    from sikk_auto_trade_types import RiskGateResult, SignalLevel, SignalResult, TradePermission, PositionPlan, ExitPlan
    from sikk_execution_adapter_base import PreTradeSecurityDecision
    from sikk_trade_confirmation_ticket import build_trade_confirmation_ticket

    risk_gate = RiskGateResult(TradePermission.ALLOW_PAPER_TRADE, "低", [], [], ["通过"], [])
    signal = SignalResult(SignalLevel.SX, "风险监控", "t", 1.0, 0.0, [], ["跌破控盘底"])
    position = PositionPlan(0.0, 0.2, 0.025, None, "无", "信号不足")
    exit_plan = ExitPlan(None, 30, [], {}, [])
    security = PreTradeSecurityDecision("BLOCK_BUY", "CRITICAL", False, ["买入侧 CRITICAL 风险"], 1)

    ticket = build_trade_confirmation_ticket(
        token="TOKEN",
        chain="sol",
        wallet_address="Wallet1111111111111111111111111111111111",
        human_amount="0.01 SOL",
        risk_gate=risk_gate,
        signal=signal,
        position_plan=position,
        exit_plan=exit_plan,
        security_decision=security,
        quote_results=[],
    )

    assert ticket.real_execution_allowed is False
    assert "禁止真实执行" in ticket.markdown
    assert "买入侧 CRITICAL 风险" in ticket.markdown


def test_confirmation_ticket_can_write_markdown_and_json(tmp_path):
    from sikk_auto_trade_types import RiskGateResult, SignalLevel, SignalResult, TradePermission, PositionPlan, ExitPlan
    from sikk_execution_adapter_base import PreTradeSecurityDecision
    from sikk_trade_confirmation_ticket import build_trade_confirmation_ticket, write_trade_confirmation_ticket

    ticket = build_trade_confirmation_ticket(
        token="TOKEN",
        chain="sol",
        wallet_address="Wallet1111111111111111111111111111111111",
        human_amount="0.01 SOL",
        risk_gate=RiskGateResult(TradePermission.ALLOW_PAPER_TRADE, "低", [], [], ["通过"], []),
        signal=SignalResult(SignalLevel.S3, "SIKK-B 控盘箱体突破回踩", "t", 1.0, 70, ["e"], []),
        position_plan=PositionPlan(0.01, 0.2, 0.025, 0.8, "结构止损", "r"),
        exit_plan=ExitPlan(0.8, 30, [], {}, []),
        security_decision=PreTradeSecurityDecision("ALLOW", "LOW", False, ["ok"], 1),
        quote_results=[],
    )
    paths = write_trade_confirmation_ticket(ticket, tmp_path)
    assert paths["markdown"].endswith("trade_confirmation_ticket.md")
    assert paths["json"].endswith("trade_confirmation_ticket.json")
    assert "SIKK 半自动交易确认单" in (tmp_path / "trade_confirmation_ticket.md").read_text(encoding="utf-8")


def test_confirmation_ticket_can_be_built_from_readiness_payload_and_v02_security():
    from sikk_execution_adapter_base import PreTradeSecurityDecision, QuoteResult
    from sikk_trade_confirmation_ticket import build_trade_confirmation_ticket_from_readiness_payload

    readiness_payload = {
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
    ticket = build_trade_confirmation_ticket_from_readiness_payload(
        readiness_payload=readiness_payload,
        chain="sol",
        wallet_address="Wallet1111111111111111111111111111111111",
        human_amount="0.01 SOL",
        security_decision=PreTradeSecurityDecision("ALLOW", "LOW", False, ["ok"], 2),
        quote_results=[QuoteResult("GMGN", "SOL", "TOKEN", "0.01", "12000", "11800", 1.1, {})],
    )

    assert ticket.token == "TOKEN"
    assert ticket.real_execution_allowed is True
    assert ticket.summary["安全权限"] == "ALLOW"
    assert "GMGN" in ticket.markdown
