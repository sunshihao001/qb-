def _pre_execution_decision():
    from sikk_execution_state_machine import ExecutionGateDecision

    return ExecutionGateDecision(
        permission="PRE_EXECUTION_READY",
        execution_authorized=True,
        next_state="PRE_EXECUTION_READY",
        reasons=["执行前门禁通过；本模块仍未广播交易"],
        required_next_action="调用独立执行适配器前必须重新报价与二次安全扫描",
        token="Token111111111111111111111111111111111111",
        order_status="READY_NOT_SUBMITTED",
    )


def test_broadcast_guard_blocks_automatic_broadcast_by_default():
    from sikk_transaction_broadcast_guard import evaluate_broadcast_gate

    result = evaluate_broadcast_gate(
        execution_gate_decision=_pre_execution_decision(),
        signed_transaction="base64-signed-tx-placeholder",
        enable_broadcast=False,
        broadcast_confirmation_text="CONFIRM_BROADCAST_TRANSACTION",
    )

    assert result.permission == "BROADCAST_DISABLED"
    assert result.broadcast_authorized is False
    assert result.order_status == "READY_NOT_BROADCAST"
    assert result.broadcasted is False
    assert any("默认禁用自动广播" in reason for reason in result.reasons)


def test_broadcast_guard_requires_pre_execution_ready_and_signed_payload():
    from sikk_execution_state_machine import ExecutionGateDecision
    from sikk_transaction_broadcast_guard import evaluate_broadcast_gate

    blocked_decision = ExecutionGateDecision(
        permission="DRY_RUN_ONLY",
        execution_authorized=False,
        next_state="AWAITING_REAL_ENABLE",
        reasons=["默认 dry-run"],
        required_next_action="显式开启真实执行开关",
        token="Token111111111111111111111111111111111111",
    )
    result = evaluate_broadcast_gate(
        execution_gate_decision=blocked_decision,
        signed_transaction="base64-signed-tx-placeholder",
        enable_broadcast=True,
        broadcast_confirmation_text="CONFIRM_BROADCAST_TRANSACTION",
    )
    assert result.permission == "BROADCAST_BLOCKED"
    assert any("执行前门禁未授权" in reason for reason in result.reasons)

    missing_payload = evaluate_broadcast_gate(
        execution_gate_decision=_pre_execution_decision(),
        signed_transaction="",
        enable_broadcast=True,
        broadcast_confirmation_text="CONFIRM_BROADCAST_TRANSACTION",
    )
    assert missing_payload.permission == "BROADCAST_BLOCKED"
    assert any("缺少已签名交易负载" in reason for reason in missing_payload.reasons)


def test_broadcast_guard_uses_manual_broadcast_not_autonomous_runner_call():
    from sikk_transaction_broadcast_guard import evaluate_broadcast_gate

    calls = []

    def fake_runner(_payload):
        calls.append(_payload)
        return {"txid": "SHOULD_NOT_BE_CALLED"}

    result = evaluate_broadcast_gate(
        execution_gate_decision=_pre_execution_decision(),
        signed_transaction="base64-signed-tx-placeholder",
        enable_broadcast=True,
        broadcast_confirmation_text="CONFIRM_BROADCAST_TRANSACTION",
        runner=fake_runner,
    )

    assert result.permission == "MANUAL_BROADCAST_READY"
    assert result.broadcast_authorized is True
    assert result.broadcasted is False
    assert result.order_status == "READY_FOR_MANUAL_BROADCAST"
    assert calls == []
    assert "不自动调用 runner" in result.required_next_action


def test_broadcast_review_files_state_no_transaction_was_broadcast(tmp_path):
    import json
    from pathlib import Path

    from sikk_transaction_broadcast_guard import evaluate_broadcast_gate, write_broadcast_gate_review

    result = evaluate_broadcast_gate(
        execution_gate_decision=_pre_execution_decision(),
        signed_transaction="base64-signed-tx-placeholder",
        enable_broadcast=True,
        broadcast_confirmation_text="CONFIRM_BROADCAST_TRANSACTION",
    )
    paths = write_broadcast_gate_review(tmp_path, result)

    assert set(paths) == {"broadcast_gate_decision_json", "broadcast_gate_review_md", "broadcast_monitor_json"}
    monitor = json.loads(Path(paths["broadcast_monitor_json"]).read_text(encoding="utf-8"))
    assert monitor["是否自动广播"] is False
    assert monitor["是否已广播交易"] is False
    assert monitor["广播状态"] == "READY_FOR_MANUAL_BROADCAST"
    md = Path(paths["broadcast_gate_review_md"]).read_text(encoding="utf-8")
    assert "不会自动广播交易" in md
