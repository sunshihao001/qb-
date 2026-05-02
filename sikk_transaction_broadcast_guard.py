"""SIKK v0.8 交易广播门禁 / 手动广播准备层。

安全边界：
- 本模块不托管私钥、不签名、不自动广播；
- 即使 `enable_broadcast=True`，也只返回 MANUAL_BROADCAST_READY；
- runner 只作为后续人工流程占位参数，当前不会被调用；
- 目标是把“自动广播交易”降级为可审计、可熔断、默认禁用的广播前检查。
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from sikk_execution_state_machine import ExecutionGateDecision

REQUIRED_BROADCAST_CONFIRMATION_TEXT = "CONFIRM_BROADCAST_TRANSACTION"


@dataclass
class BroadcastGateDecision:
    """广播门禁结果。"""

    permission: str
    broadcast_authorized: bool
    broadcasted: bool
    order_status: str
    reasons: List[str]
    required_next_action: str
    token: str = ""
    txid: Optional[str] = None
    scope_note: str = "SIKK v0.8 只做广播前门禁与手动广播准备；不会自动广播交易。"
    metadata: Dict[str, Any] = field(default_factory=dict)


def _has_payload(signed_transaction: Optional[str]) -> bool:
    return bool(str(signed_transaction or "").strip())


def evaluate_broadcast_gate(
    *,
    execution_gate_decision: ExecutionGateDecision,
    signed_transaction: Optional[str] = None,
    enable_broadcast: bool = False,
    broadcast_confirmation_text: str = "",
    runner: Optional[Callable[[str], Dict[str, Any]]] = None,
) -> BroadcastGateDecision:
    """评估是否进入人工广播准备状态。

    注意：当前版本永远不会调用 `runner`，因此不会自动广播交易。
    """

    reasons: List[str] = []
    token = execution_gate_decision.token

    if not execution_gate_decision.execution_authorized or execution_gate_decision.permission != "PRE_EXECUTION_READY":
        reasons.append("执行前门禁未授权，禁止进入广播层")

    if not _has_payload(signed_transaction):
        reasons.append("缺少已签名交易负载，禁止广播")

    if broadcast_confirmation_text.strip() != REQUIRED_BROADCAST_CONFIRMATION_TEXT:
        reasons.append("缺少明确广播确认文本 CONFIRM_BROADCAST_TRANSACTION")

    if reasons:
        return BroadcastGateDecision(
            permission="BROADCAST_BLOCKED",
            broadcast_authorized=False,
            broadcasted=False,
            order_status="BROADCAST_BLOCKED_NOT_SUBMITTED",
            reasons=reasons,
            required_next_action="停止广播准备，重新执行门禁/签名/人工复查",
            token=token,
            metadata={
                "execution_permission": execution_gate_decision.permission,
                "runner_supplied": runner is not None,
            },
        )

    if not enable_broadcast:
        return BroadcastGateDecision(
            permission="BROADCAST_DISABLED",
            broadcast_authorized=False,
            broadcasted=False,
            order_status="READY_NOT_BROADCAST",
            reasons=["默认禁用自动广播；需要显式 enable_broadcast=True 才能进入手动广播准备"],
            required_next_action="保持不广播；如需进入人工广播准备，重新运行并显式开启广播门禁",
            token=token,
            metadata={
                "execution_permission": execution_gate_decision.permission,
                "runner_supplied": runner is not None,
            },
        )

    return BroadcastGateDecision(
        permission="MANUAL_BROADCAST_READY",
        broadcast_authorized=True,
        broadcasted=False,
        order_status="READY_FOR_MANUAL_BROADCAST",
        reasons=["广播前门禁通过；当前实现不会自动调用 runner，也不会自动广播交易"],
        required_next_action="进入人工广播准备；不自动调用 runner，广播前必须再次确认链、钱包、金额、滑点与交易摘要",
        token=token,
        metadata={
            "execution_permission": execution_gate_decision.permission,
            "runner_supplied": runner is not None,
            "signed_payload_present": True,
        },
    )


def _decision_to_dict(decision: BroadcastGateDecision) -> Dict[str, Any]:
    data = asdict(decision)
    data.update({
        "代币地址": decision.token,
        "广播权限": decision.permission,
        "是否授权广播准备": decision.broadcast_authorized,
        "是否已广播交易": decision.broadcasted,
        "广播状态": decision.order_status,
        "原因列表": decision.reasons,
        "下一步动作": decision.required_next_action,
        "说明": decision.scope_note,
    })
    return data


def _markdown(decision: BroadcastGateDecision) -> str:
    lines = [
        "# SIKK v0.8 广播前门禁审查",
        "",
        f"- 代币地址：{decision.token}",
        f"- 广播权限：{decision.permission}",
        f"- 广播状态：{decision.order_status}",
        f"- 是否授权广播准备：{decision.broadcast_authorized}",
        f"- 是否已广播交易：{decision.broadcasted}",
        "- 执行边界：本模块只做广播前门禁与手动广播准备，不会自动广播交易。",
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


def _broadcast_monitor(decision: BroadcastGateDecision) -> Dict[str, Any]:
    return {
        "代币地址": decision.token,
        "广播状态": decision.order_status,
        "是否自动广播": False,
        "是否已广播交易": decision.broadcasted,
        "交易哈希": decision.txid,
        "广播权限": decision.permission,
        "监控说明": "广播监控占位文件；当前未自动广播交易，未提交链上交易。",
        "事件": [
            {
                "event_type": "broadcast_gate_evaluated",
                "permission": decision.permission,
                "broadcasted": decision.broadcasted,
                "auto_broadcast": False,
            }
        ],
    }


def write_broadcast_gate_review(output_dir: str | Path, decision: BroadcastGateDecision) -> Dict[str, str]:
    """写出 v0.8 广播门禁三文件。"""

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    decision_json = out / "broadcast_gate_decision.json"
    review_md = out / "broadcast_gate_review.md"
    monitor_json = out / "broadcast_monitor.json"

    decision_json.write_text(json.dumps(_decision_to_dict(decision), ensure_ascii=False, indent=2), encoding="utf-8")
    review_md.write_text(_markdown(decision), encoding="utf-8")
    monitor_json.write_text(json.dumps(_broadcast_monitor(decision), ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "broadcast_gate_decision_json": str(decision_json),
        "broadcast_gate_review_md": str(review_md),
        "broadcast_monitor_json": str(monitor_json),
    }
