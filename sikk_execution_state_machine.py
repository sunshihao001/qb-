"""SIKK v0.7 执行前状态机门禁 / 熔断器 / 订单监控骨架。

本模块位于确认单之后、真实执行适配器之前：
- 默认 dry-run，不执行、不广播、不构造真实 swap 命令；
- 只判断是否“具备进入执行适配器前置条件”；
- 输出执行前门禁决策与订单监控占位文件，供后续人工/极小仓阶段接入。
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

REQUIRED_CONFIRMATION_TEXT = "CONFIRM_REAL_TRADE"
MAX_PRICE_IMPACT_CIRCUIT_BREAKER_PCT = 10.0
MAX_CONSECUTIVE_FAILURES = 3


@dataclass
class ExecutionGateDecision:
    """执行前门禁结果。

    `execution_authorized=True` 只表示允许进入“独立执行适配器前”的最后准备状态；
    本模块本身不会广播交易。
    """

    permission: str
    execution_authorized: bool
    next_state: str
    reasons: List[str]
    required_next_action: str
    token: str = ""
    order_status: str = "DRY_RUN_NOT_SUBMITTED"
    circuit_breaker_triggered: bool = False
    scope_note: str = "SIKK v0.7 只做执行前门禁/熔断/订单监控骨架，不执行真实 swap。"
    metadata: Dict[str, Any] = field(default_factory=dict)


def _get(obj: Any, key: str, default: Any = None) -> Any:
    """兼容 dict / dataclass 的字段读取。"""

    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _parse_utc(text: Optional[str]) -> Optional[datetime]:
    """解析 ISO UTC 文本。"""

    if not text:
        return None
    try:
        normalized = str(text).replace("Z", "+00:00")
        parsed = datetime.fromisoformat(normalized)
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except ValueError:
        return None


def _quote_age_seconds(quote_snapshot: Dict[str, Any], current_time: Optional[str]) -> Optional[float]:
    """计算报价年龄秒数；无法计算时返回 None。"""

    snapshot_dt = _parse_utc(str(quote_snapshot.get("snapshot_time") or ""))
    current_dt = _parse_utc(current_time) if current_time else datetime.now(timezone.utc)
    if snapshot_dt is None or current_dt is None:
        return None
    return (current_dt - snapshot_dt).total_seconds()


def _token_from_inputs(confirmation_ticket: Any, quote_security_decision: Dict[str, Any], quote_snapshot: Dict[str, Any]) -> str:
    return str(
        _get(confirmation_ticket, "token", "")
        or quote_security_decision.get("token", "")
        or quote_snapshot.get("token", "")
    )


def evaluate_execution_gate(
    *,
    candidate_state: str,
    confirmation_ticket: Any,
    quote_security_decision: Dict[str, Any],
    quote_snapshot: Dict[str, Any],
    user_confirmation_text: str = "",
    current_time: Optional[str] = None,
    enable_real_execution: bool = False,
    consecutive_failures: int = 0,
) -> ExecutionGateDecision:
    """评估是否允许进入真实执行适配器前置状态。

    默认 `enable_real_execution=False`，即使用户输入确认文本也只返回 DRY_RUN_ONLY。
    """

    reasons: List[str] = []
    breaker_reasons: List[str] = []
    token = _token_from_inputs(confirmation_ticket, quote_security_decision, quote_snapshot)

    if candidate_state != "READY_FOR_CONFIRMATION":
        breaker_reasons.append(f"候选状态不是 READY_FOR_CONFIRMATION：{candidate_state}")

    if not bool(_get(confirmation_ticket, "real_execution_allowed", False)):
        block_reasons = _get(confirmation_ticket, "block_reasons", []) or []
        breaker_reasons.append("确认单未允许进入人工确认层")
        breaker_reasons.extend(str(reason) for reason in block_reasons)

    final_permission = str(quote_security_decision.get("final_permission", "UNKNOWN"))
    if final_permission != "ALLOW_CONFIRMATION_LAYER":
        breaker_reasons.append(f"报价安全决策阻断或暂停：{final_permission}")

    if quote_snapshot.get("quote_status") != "AVAILABLE" or int(quote_snapshot.get("source_count", 0) or 0) <= 0:
        breaker_reasons.append("报价缺失或报价源数量为 0")

    quote_age = _quote_age_seconds(quote_snapshot, current_time)
    max_age = int(quote_snapshot.get("max_quote_age_seconds", 30) or 30)
    if quote_age is None:
        breaker_reasons.append("无法计算报价时效，触发熔断")
    elif quote_age < 0:
        breaker_reasons.append("报价时间晚于当前时间，触发熔断")
    elif quote_age > max_age:
        breaker_reasons.append(f"报价已过期：{int(quote_age)}s > {max_age}s")

    impact = quote_snapshot.get("max_price_impact_pct")
    if impact is not None and float(impact) > MAX_PRICE_IMPACT_CIRCUIT_BREAKER_PCT:
        breaker_reasons.append(f"价格影响触发熔断：{impact}% > {MAX_PRICE_IMPACT_CIRCUIT_BREAKER_PCT}%")

    if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
        breaker_reasons.append(f"连续失败次数触发熔断：{consecutive_failures} >= {MAX_CONSECUTIVE_FAILURES}")

    if user_confirmation_text.strip() != REQUIRED_CONFIRMATION_TEXT:
        reasons.append("缺少明确人工确认 CONFIRM_REAL_TRADE")

    if breaker_reasons:
        return ExecutionGateDecision(
            permission="CIRCUIT_BREAKER",
            execution_authorized=False,
            next_state="BLOCKED",
            reasons=breaker_reasons + reasons,
            required_next_action="停止执行准备，重新报价/安全扫描/人工复查",
            token=token,
            order_status="BLOCKED_NOT_SUBMITTED",
            circuit_breaker_triggered=True,
            metadata={"candidate_state": candidate_state, "quote_age_seconds": quote_age},
        )

    if reasons:
        return ExecutionGateDecision(
            permission="PAUSE_NEED_CONFIRM",
            execution_authorized=False,
            next_state="PAUSE",
            reasons=reasons,
            required_next_action="等待人工确认文本后重新评估",
            token=token,
            order_status="PAUSED_NOT_SUBMITTED",
            metadata={"candidate_state": candidate_state, "quote_age_seconds": quote_age},
        )

    if not enable_real_execution:
        return ExecutionGateDecision(
            permission="DRY_RUN_ONLY",
            execution_authorized=False,
            next_state="AWAITING_REAL_ENABLE",
            reasons=["默认 dry-run：未显式开启 enable_real_execution，禁止进入真实执行适配器"],
            required_next_action="如需极小仓真实执行，需重新运行并显式开启真实执行开关",
            token=token,
            order_status="DRY_RUN_NOT_SUBMITTED",
            metadata={"candidate_state": candidate_state, "quote_age_seconds": quote_age},
        )

    return ExecutionGateDecision(
        permission="PRE_EXECUTION_READY",
        execution_authorized=True,
        next_state="PRE_EXECUTION_READY",
        reasons=["执行前门禁通过；本模块仍未广播交易"],
        required_next_action="调用独立执行适配器前必须重新报价与二次安全扫描",
        token=token,
        order_status="READY_NOT_SUBMITTED",
        metadata={"candidate_state": candidate_state, "quote_age_seconds": quote_age},
    )


def _decision_to_dict(decision: ExecutionGateDecision) -> Dict[str, Any]:
    """转中文优先输出，同时保留少量机器字段。"""

    data = asdict(decision)
    data.update({
        "代币地址": decision.token,
        "门禁权限": decision.permission,
        "是否授权进入执行适配器": decision.execution_authorized,
        "下一状态": decision.next_state,
        "订单状态": decision.order_status,
        "是否触发熔断": decision.circuit_breaker_triggered,
        "原因列表": decision.reasons,
        "下一步动作": decision.required_next_action,
        "说明": decision.scope_note,
    })
    return data


def _markdown(decision: ExecutionGateDecision) -> str:
    lines = [
        "# SIKK v0.7 执行前门禁审查",
        "",
        f"- 代币地址：{decision.token}",
        f"- 门禁权限：{decision.permission}",
        f"- 下一状态：{decision.next_state}",
        f"- 订单状态：{decision.order_status}",
        f"- 是否授权进入执行适配器：{decision.execution_authorized}",
        f"- 是否触发熔断：{decision.circuit_breaker_triggered}",
        "- 执行边界：本模块只做执行前门禁/熔断/订单监控骨架，不执行真实 swap。",
        "",
        "## 原因",
    ]
    for reason in decision.reasons:
        lines.append(f"- {reason}")
    lines.extend([
        "",
        "## 下一步",
        f"- {decision.required_next_action}",
    ])
    return "\n".join(lines) + "\n"


def _order_monitor_stub(decision: ExecutionGateDecision, token: str) -> Dict[str, Any]:
    return {
        "代币地址": token,
        "订单状态": decision.order_status,
        "是否广播交易": False,
        "是否真实成交": False,
        "门禁权限": decision.permission,
        "下一状态": decision.next_state,
        "监控说明": "订单监控占位文件；当前未提交任何真实订单，不执行真实 swap。",
        "事件": [
            {
                "event_type": "execution_gate_evaluated",
                "permission": decision.permission,
                "order_status": decision.order_status,
                "broadcasted": False,
            }
        ],
    }


def write_execution_gate_review(output_dir: str | Path, decision: ExecutionGateDecision, *, token: Optional[str] = None) -> Dict[str, str]:
    """写出 v0.7 执行前门禁三文件。"""

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    actual_token = token or decision.token
    decision_json = out / "execution_gate_decision.json"
    review_md = out / "execution_gate_review.md"
    order_stub_json = out / "order_monitor_stub.json"

    decision_json.write_text(json.dumps(_decision_to_dict(decision), ensure_ascii=False, indent=2), encoding="utf-8")
    review_md.write_text(_markdown(decision), encoding="utf-8")
    order_stub_json.write_text(json.dumps(_order_monitor_stub(decision, actual_token), ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "execution_gate_decision_json": str(decision_json),
        "execution_gate_review_md": str(review_md),
        "order_monitor_stub_json": str(order_stub_json),
    }
