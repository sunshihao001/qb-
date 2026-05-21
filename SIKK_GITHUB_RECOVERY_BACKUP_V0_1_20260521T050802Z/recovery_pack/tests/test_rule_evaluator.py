from __future__ import annotations

from core.rule_evaluator import evaluate_condition, evaluate_rule


def test_evaluate_numeric_rule_pass():
    feature = {"liquidity": {"liquidity_usd": {"value": "53159", "missing": False}}}
    rule = {"id": "r1", "field": "liquidity.liquidity_usd", "operator": ">=", "value": 20000, "reason_code": "ok"}
    result = evaluate_rule(rule, feature)
    assert result["status"] == "PASS"
    assert result["observed"] == "53159"


def test_missing_operator():
    assert evaluate_condition(None, True, "missing", True) is True
    assert evaluate_condition("x", False, "missing", True) is False


def test_missing_numeric_rule_fails():
    feature = {"quote": {"quote_slippage_estimate": {"value": None, "missing": True, "missing_reason": "missing"}}}
    rule = {"id": "r2", "field": "quote.quote_slippage_estimate", "operator": ">=", "value": 0, "reason_code": "missing"}
    result = evaluate_rule(rule, feature)
    assert result["status"] == "FAIL"
