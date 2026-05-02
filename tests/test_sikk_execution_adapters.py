import pytest


def test_gmgn_quote_adapter_builds_quote_command_not_swap_command():
    from sikk_gmgn_quote_adapter import GMGNQuoteAdapter

    adapter = GMGNQuoteAdapter()
    req = adapter.make_quote_request(
        chain="sol",
        wallet_address="Wallet1111111111111111111111111111111111",
        input_token="So11111111111111111111111111111111111111112",
        output_token="Token11111111111111111111111111111111111",
        amount_smallest_unit="10000000",
        slippage=0.3,
    )
    command = adapter.build_quote_command(req)
    assert command[:4] == ["gmgn-cli", "order", "quote", "--chain"]
    assert "swap" not in command
    assert "--amount" in command
    assert "10000000" in command


def test_okx_quote_adapter_builds_readonly_quote_command_not_execute():
    from sikk_okx_quote_adapter import OKXQuoteAdapter

    adapter = OKXQuoteAdapter()
    req = adapter.make_quote_request(
        chain="solana",
        wallet_address="Wallet1111111111111111111111111111111111",
        input_token="11111111111111111111111111111111",
        output_token="Token11111111111111111111111111111111111",
        readable_amount="0.01",
    )
    command = adapter.build_quote_command(req)
    assert command[:3] == ["onchainos", "swap", "quote"]
    assert "execute" not in command
    assert "--readable-amount" in command
    assert "0.01" in command


def test_pre_trade_security_checker_blocks_critical_buy_and_warns_sell():
    from sikk_pre_trade_security_checker import evaluate_pre_trade_security
    from sikk_execution_adapter_base import SecurityScanResult, TokenSide

    buy_result = SecurityScanResult(
        source="OKX",
        token_address="BAD",
        token_side=TokenSide.BUY,
        risk_level="CRITICAL",
        triggered_labels=["honeypot"],
        raw={},
    )
    decision = evaluate_pre_trade_security([buy_result])
    assert decision.permission == "BLOCK_BUY"
    assert "买入侧 CRITICAL 风险" in decision.reasons[0]

    sell_result = SecurityScanResult(
        source="OKX",
        token_address="BAD",
        token_side=TokenSide.SELL,
        risk_level="CRITICAL",
        triggered_labels=["honeypot"],
        raw={},
    )
    decision = evaluate_pre_trade_security([sell_result])
    assert decision.permission == "WARN_ALLOW_SELL"


def test_pre_trade_security_checker_pauses_high_risk_buy():
    from sikk_pre_trade_security_checker import evaluate_pre_trade_security
    from sikk_execution_adapter_base import SecurityScanResult, TokenSide

    result = SecurityScanResult(
        source="GMGN",
        token_address="RISKY",
        token_side=TokenSide.BUY,
        risk_level="HIGH",
        triggered_labels=["low_liquidity"],
        raw={},
    )
    decision = evaluate_pre_trade_security([result])
    assert decision.permission == "PAUSE_NEED_CONFIRM"
    assert decision.requires_user_confirmation is True


def test_real_trade_guard_requires_explicit_confirmation_and_blocks_auto_by_default():
    from sikk_real_trade_guard import RealTradeGuard, TradePlan

    guard = RealTradeGuard()
    plan = TradePlan(
        mode="real",
        chain="sol",
        wallet_address="Wallet1111111111111111111111111111111111",
        input_token="SOL",
        output_token="TOKEN",
        human_amount="0.01",
        strategy_type="SIKK-B 控盘箱体突破回踩",
        signal_level="S4_强确认信号",
        max_slippage_pct=10,
    )
    denied = guard.authorize(plan, user_confirmation_text="")
    assert denied.allowed is False
    assert "缺少明确人工确认" in denied.reason

    allowed = guard.authorize(plan, user_confirmation_text="CONFIRM_REAL_TRADE")
    assert allowed.allowed is True


def test_real_trade_guard_rejects_paper_mode_for_real_execution():
    from sikk_real_trade_guard import RealTradeGuard, TradePlan

    guard = RealTradeGuard()
    plan = TradePlan(
        mode="paper",
        chain="sol",
        wallet_address="Wallet1111111111111111111111111111111111",
        input_token="SOL",
        output_token="TOKEN",
        human_amount="0.01",
        strategy_type="SIKK-B 控盘箱体突破回踩",
        signal_level="S4_强确认信号",
        max_slippage_pct=10,
    )
    denied = guard.authorize(plan, user_confirmation_text="CONFIRM_REAL_TRADE")
    assert denied.allowed is False
    assert "paper 模式禁止真实执行" in denied.reason
