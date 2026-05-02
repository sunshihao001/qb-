import json
from pathlib import Path

import pytest


def test_trade_types_can_serialize_readiness_result():
    from sikk_auto_trade_types import (
        RiskGateResult,
        SignalLevel,
        SignalResult,
        TradePermission,
        readiness_to_dict,
    )

    risk = RiskGateResult(
        permission=TradePermission.ALLOW_PAPER_TRADE,
        risk_level="低",
        block_reasons=[],
        pause_reasons=[],
        allow_reasons=["安全层通过"],
        missing_evidence=[],
    )
    signal = SignalResult(
        signal_level=SignalLevel.S3,
        strategy_type="SIKK-B 控盘箱体突破回踩",
        signal_time="2026-04-27 16:37:00",
        signal_price=0.00023386184,
        confidence_score=72.0,
        evidence=["突破控盘上沿"],
        invalidation_reasons=[],
    )

    payload = readiness_to_dict(risk_gate=risk, signal=signal)
    assert payload["risk_gate"]["permission"] == "ALLOW_PAPER_TRADE_允许纸面交易"
    assert payload["signal"]["signal_level"] == "S3_策略观察信号"
    json.dumps(payload, ensure_ascii=False)


def test_risk_gate_blocks_critical_honeypot_and_allows_clean_paper_mode():
    from sikk_auto_risk_gate import evaluate_risk_gate
    from sikk_auto_trade_types import TradePermission

    blocked = evaluate_risk_gate(
        {
            "security_risk_level": "CRITICAL",
            "is_honeypot": True,
            "can_sell": False,
            "quote_available": True,
            "liquidity_usd": 50000,
            "slippage_pct": 3,
            "price_impact_pct": 2,
            "mode": "paper",
        }
    )
    assert blocked.permission == TradePermission.BLOCK_BUY
    assert "安全风险为 CRITICAL" in blocked.block_reasons
    assert "检测到 Honeypot/貔貅风险" in blocked.block_reasons

    allowed = evaluate_risk_gate(
        {
            "security_risk_level": "LOW",
            "is_honeypot": False,
            "can_sell": True,
            "quote_available": True,
            "liquidity_usd": 80000,
            "slippage_pct": 2,
            "price_impact_pct": 1,
            "mode": "paper",
        }
    )
    assert allowed.permission == TradePermission.ALLOW_PAPER_TRADE
    assert allowed.block_reasons == []


def test_signal_engine_detects_sikk_b_breakout_retest_and_invalid_breakdown():
    from sikk_auto_signal_engine import evaluate_signal
    from sikk_auto_trade_types import SignalLevel, TradePermission, RiskGateResult

    risk_gate = RiskGateResult(
        permission=TradePermission.ALLOW_PAPER_TRADE,
        risk_level="低",
        block_reasons=[],
        pause_reasons=[],
        allow_reasons=["安全层通过"],
        missing_evidence=[],
    )
    s3 = evaluate_signal(
        {
            "control_box_ready": True,
            "close": 0.00023386184,
            "control_high": 0.00022980137,
            "low": 0.00019342888,
            "fib_0236": 0.000186449324276,
            "fib_0382": 0.000159629838362,
            "avwap": 0.0002200,
            "obv_state": "增强",
            "cmf_state": "转正",
            "early_wallet_clearout_ratio": 0.25,
            "break_lh": False,
            "formed_hl_hh": False,
            "signal_time": "2026-04-27 16:37:00",
        },
        risk_gate,
    )
    assert s3.signal_level == SignalLevel.S3
    assert s3.strategy_type == "SIKK-B 控盘箱体突破回踩"
    assert s3.signal_price == 0.00023386184

    sx = evaluate_signal(
        {
            "control_box_ready": True,
            "close": 0.000040,
            "control_low": 0.000046106261,
            "poc": 0.000137,
            "volume_ratio": 2.1,
            "avwap": 0.00012,
            "obv_state": "持续下降",
            "cmf_state": "持续小于0",
            "early_wallet_clearout_ratio": 0.85,
        },
        risk_gate,
    )
    assert sx.signal_level == SignalLevel.SX
    assert "跌破控盘底" in sx.invalidation_reasons


def test_position_sizer_returns_zero_for_block_and_scales_s3_position():
    from sikk_auto_position_sizer import calculate_position_plan
    from sikk_auto_trade_types import SignalLevel, TradePermission, RiskGateResult, SignalResult

    blocked_gate = RiskGateResult(TradePermission.BLOCK_BUY, "高", ["安全风险"], [], [], [])
    signal = SignalResult(SignalLevel.S3, "SIKK-B 控盘箱体突破回踩", None, 0.0002, 70, [], [])
    blocked_plan = calculate_position_plan(
        account_equity_sol=10,
        risk_per_trade_pct=0.25,
        entry_price=0.0002,
        stop_price=0.00015,
        signal=signal,
        risk_gate=blocked_gate,
    )
    assert blocked_plan.suggested_position_sol == 0

    allowed_gate = RiskGateResult(TradePermission.ALLOW_PAPER_TRADE, "低", [], [], ["通过"], [])
    allowed_plan = calculate_position_plan(
        account_equity_sol=10,
        risk_per_trade_pct=0.25,
        entry_price=0.00023386184,
        stop_price=0.000186449324276,
        signal=signal,
        risk_gate=allowed_gate,
        max_position_sol=0.2,
    )
    assert 0 < allowed_plan.suggested_position_sol <= 0.2
    assert allowed_plan.stop_type == "结构止损"


def test_exit_planner_builds_sikk_b_exit_plan():
    from sikk_auto_exit_planner import build_exit_plan

    plan = build_exit_plan(
        strategy_type="SIKK-B 控盘箱体突破回踩",
        entry_price=0.00023386184,
        control_low=0.000046106261,
        fib_0236=0.000186449324276,
        fib_0382=0.000159629838362,
    )
    assert plan.hard_stop_price == pytest.approx(0.000186449324276)
    assert len(plan.take_profit_rules) == 3
    assert plan.take_profit_rules[0]["触发收益率"] == 50
    assert "早期钱包集中清仓" in plan.emergency_exit_rules


def test_runner_does_not_apply_later_accumulation_poc_to_early_breakout():
    from sikk_auto_readiness_runner import build_runner_context

    rows = [
        {"timestamp": "1", "datetime_utc": "t1", "open": 1, "high": 1.1, "low": 0.9, "close": 1.0},
        {"timestamp": "2", "datetime_utc": "t2", "open": 1, "high": 1.2, "low": 0.95, "close": 1.1},
        {"timestamp": "3", "datetime_utc": "t3", "open": 1, "high": 1.3, "low": 0.96, "close": 1.2},
        {"timestamp": "4", "datetime_utc": "t4", "open": 1, "high": 1.4, "low": 0.97, "close": 1.3},
        {"timestamp": "5", "datetime_utc": "t5", "open": 1, "high": 1.5, "low": 0.98, "close": 1.4},
        {"timestamp": "6", "datetime_utc": "t6", "open": 1, "high": 1.6, "low": 1.0, "close": 1.5},
        {"timestamp": "7", "datetime_utc": "t7", "open": 1.5, "high": 1.8, "low": 1.55, "close": 1.7},
    ]
    context = build_runner_context(rows, {"T_start_timestamp": 100, "POC_price": 99}, {})
    assert context["signal_input"]["signal_time"] == "t7"
    assert context["signal_input"]["poc"] != 99


def test_paper_trading_engine_simulates_take_profit_before_final_exit():
    from sikk_auto_exit_planner import build_exit_plan
    from sikk_paper_trading_engine import simulate_paper_trade

    bars = [
        {"timestamp": "t0", "open": 1.0, "high": 1.05, "low": 0.98, "close": 1.0},
        {"timestamp": "t1", "open": 1.0, "high": 1.55, "low": 0.99, "close": 1.4},
        {"timestamp": "t2", "open": 1.4, "high": 2.1, "low": 1.3, "close": 2.0},
        {"timestamp": "t3", "open": 2.0, "high": 3.2, "low": 1.8, "close": 3.0},
    ]
    exit_plan = build_exit_plan("SIKK-B 控盘箱体突破回踩", 1.0, control_low=0.2, fib_0236=0.8, fib_0382=0.7)
    result = simulate_paper_trade(
        token="TEST",
        bars=bars,
        entry_time="t0",
        entry_price=1.0,
        position_sol=0.1,
        exit_plan=exit_plan,
        signal_level="S3",
        strategy_type="SIKK-B 控盘箱体突破回踩",
    )
    assert result["是否命中止盈"] is True
    assert result["最大浮盈_pct"] >= 200
    assert result["最终R倍数"] > 0
