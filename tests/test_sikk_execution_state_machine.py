import json
from pathlib import Path


def _ticket(real_allowed=True):
    return {
        "token": "Token111111111111111111111111111111111111",
        "chain": "sol",
        "wallet_address": "Wallet1111111111111111111111111111111111",
        "human_amount": "0.01 SOL",
        "required_confirmation_text": "CONFIRM_REAL_TRADE",
        "real_execution_allowed": real_allowed,
        "block_reasons": [] if real_allowed else ["确认单未放行"],
        "summary": {"信号等级": "S4_强确认信号"},
    }


def _quote_snapshot(snapshot_time="2026-05-01T00:00:00Z", impact=1.2, status="AVAILABLE"):
    return {
        "token": "Token111111111111111111111111111111111111",
        "chain": "sol",
        "wallet_address": "Wallet1111111111111111111111111111111111",
        "human_amount": "0.01 SOL",
        "snapshot_time": snapshot_time,
        "max_quote_age_seconds": 30,
        "quote_status": status,
        "source_count": 1 if status == "AVAILABLE" else 0,
        "max_price_impact_pct": impact,
        "scope_note": "只读报价快照；不执行真实交易。",
    }


def _quote_decision(permission="ALLOW_CONFIRMATION_LAYER"):
    return {
        "token": "Token111111111111111111111111111111111111",
        "chain": "sol",
        "snapshot_time": "2026-05-01T00:00:00Z",
        "final_permission": permission,
        "requires_user_confirmation": True,
        "quote_status": "AVAILABLE",
        "security_permission": "ALLOW",
        "security_risk_level": "LOW",
        "quote_source_count": 1,
        "security_source_count": 1,
        "max_price_impact_pct": 1.2,
        "reasons": ["报价与安全扫描未触发硬阻断，可进入人工确认层"],
    }


def test_execution_gate_defaults_to_dry_run_even_with_confirmation():
    from sikk_execution_state_machine import evaluate_execution_gate

    decision = evaluate_execution_gate(
        candidate_state="READY_FOR_CONFIRMATION",
        confirmation_ticket=_ticket(True),
        quote_security_decision=_quote_decision(),
        quote_snapshot=_quote_snapshot(),
        user_confirmation_text="CONFIRM_REAL_TRADE",
        current_time="2026-05-01T00:00:10Z",
    )

    assert decision.permission == "DRY_RUN_ONLY"
    assert decision.execution_authorized is False
    assert decision.next_state == "AWAITING_REAL_ENABLE"
    assert any("默认 dry-run" in reason for reason in decision.reasons)
    assert "不执行真实 swap" in decision.scope_note


def test_execution_gate_allows_pre_execution_only_when_explicitly_enabled_and_fresh():
    from sikk_execution_state_machine import evaluate_execution_gate

    decision = evaluate_execution_gate(
        candidate_state="READY_FOR_CONFIRMATION",
        confirmation_ticket=_ticket(True),
        quote_security_decision=_quote_decision(),
        quote_snapshot=_quote_snapshot(),
        user_confirmation_text="CONFIRM_REAL_TRADE",
        current_time="2026-05-01T00:00:10Z",
        enable_real_execution=True,
    )

    assert decision.permission == "PRE_EXECUTION_READY"
    assert decision.execution_authorized is True
    assert decision.next_state == "PRE_EXECUTION_READY"
    assert decision.required_next_action == "调用独立执行适配器前必须重新报价与二次安全扫描"


def test_execution_gate_circuit_breaks_stale_quote_and_blocked_decision():
    from sikk_execution_state_machine import evaluate_execution_gate

    stale = evaluate_execution_gate(
        candidate_state="READY_FOR_CONFIRMATION",
        confirmation_ticket=_ticket(True),
        quote_security_decision=_quote_decision(),
        quote_snapshot=_quote_snapshot(snapshot_time="2026-05-01T00:00:00Z"),
        user_confirmation_text="CONFIRM_REAL_TRADE",
        current_time="2026-05-01T00:01:01Z",
        enable_real_execution=True,
    )
    assert stale.permission == "CIRCUIT_BREAKER"
    assert stale.next_state == "BLOCKED"
    assert any("报价已过期" in reason for reason in stale.reasons)

    blocked = evaluate_execution_gate(
        candidate_state="READY_FOR_CONFIRMATION",
        confirmation_ticket=_ticket(True),
        quote_security_decision=_quote_decision("BLOCK_BUY"),
        quote_snapshot=_quote_snapshot(),
        user_confirmation_text="CONFIRM_REAL_TRADE",
        current_time="2026-05-01T00:00:10Z",
        enable_real_execution=True,
    )
    assert blocked.permission == "CIRCUIT_BREAKER"
    assert any("报价安全决策阻断" in reason for reason in blocked.reasons)


def test_execution_gate_writes_dry_run_order_monitor_files(tmp_path):
    from sikk_execution_state_machine import evaluate_execution_gate, write_execution_gate_review

    decision = evaluate_execution_gate(
        candidate_state="READY_FOR_CONFIRMATION",
        confirmation_ticket=_ticket(True),
        quote_security_decision=_quote_decision(),
        quote_snapshot=_quote_snapshot(),
        user_confirmation_text="CONFIRM_REAL_TRADE",
        current_time="2026-05-01T00:00:10Z",
    )
    paths = write_execution_gate_review(tmp_path, decision, token="Token111111111111111111111111111111111111")

    assert set(paths) == {"execution_gate_decision_json", "execution_gate_review_md", "order_monitor_stub_json"}
    for path in paths.values():
        assert Path(path).exists()
    order_stub = json.loads(Path(paths["order_monitor_stub_json"]).read_text(encoding="utf-8"))
    assert order_stub["订单状态"] == "DRY_RUN_NOT_SUBMITTED"
    assert order_stub["是否广播交易"] is False
    md = Path(paths["execution_gate_review_md"]).read_text(encoding="utf-8")
    assert "执行前门禁" in md
    assert "不执行真实 swap" in md
