"""SIKK v0.3 半自动交易确认单生成器。

本模块只把 v0.1 自动交易准备结果与 v0.2 报价/安全扫描结果合并成
人工复核确认单，不执行、不广播、不构造真实 swap 命令。
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from sikk_auto_trade_types import ExitPlan, PositionPlan, RiskGateResult, SignalLevel, SignalResult, TradePermission


REQUIRED_CONFIRMATION_TEXT = "CONFIRM_REAL_TRADE"


@dataclass
class TradeConfirmationTicket:
    """半自动交易确认单。

    real_execution_allowed 只表示“是否满足进入人工确认层的前置条件”，
    不是执行授权；真实执行仍必须由后续 guard 再校验确认文本。
    """

    token: str
    chain: str
    wallet_address: str
    human_amount: str
    required_confirmation_text: str
    real_execution_allowed: bool
    block_reasons: List[str]
    summary: Dict[str, Any]
    risk_gate: Any
    signal: Any
    position_plan: Any
    exit_plan: Any
    security_decision: Any
    quote_results: List[Any]
    markdown: str

    def to_dict(self) -> Dict[str, Any]:
        """转为 JSON 可写结构。"""

        return {
            "token": self.token,
            "chain": self.chain,
            "wallet_address": self.wallet_address,
            "human_amount": self.human_amount,
            "required_confirmation_text": self.required_confirmation_text,
            "real_execution_allowed": self.real_execution_allowed,
            "block_reasons": self.block_reasons,
            "summary": _serialize(self.summary),
            "risk_gate": _serialize(self.risk_gate),
            "signal": _serialize(self.signal),
            "position_plan": _serialize(self.position_plan),
            "exit_plan": _serialize(self.exit_plan),
            "security_decision": _serialize(self.security_decision),
            "quote_results": _serialize(self.quote_results),
            "markdown": self.markdown,
            "scope_note": "SIKK v0.3 只生成半自动交易确认单，不执行真实 swap。",
        }


def _serialize(value: Any) -> Any:
    """递归序列化 dataclass / Enum / list / dict。"""

    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {k: _serialize(v) for k, v in asdict(value).items()}
    if isinstance(value, list):
        return [_serialize(v) for v in value]
    if isinstance(value, dict):
        return {k: _serialize(v) for k, v in value.items()}
    return value


def _enum_value(value: Any) -> str:
    """取 Enum 或普通字段的可读值。"""

    if isinstance(value, Enum):
        return str(value.value)
    return str(value)


def _trade_permission_from_value(value: Any) -> TradePermission:
    """从 JSON 字符串恢复交易权限枚举。"""

    if isinstance(value, TradePermission):
        return value
    for item in TradePermission:
        if value in {item.value, item.name}:
            return item
    raise ValueError(f"未知交易权限：{value}")


def _signal_level_from_value(value: Any) -> SignalLevel:
    """从 JSON 字符串恢复信号等级枚举。"""

    if isinstance(value, SignalLevel):
        return value
    for item in SignalLevel:
        if value in {item.value, item.name}:
            return item
    raise ValueError(f"未知信号等级：{value}")


def _readiness_sections_from_payload(payload: Dict[str, Any]) -> tuple[RiskGateResult, SignalResult, PositionPlan, ExitPlan]:
    """把 v0.1 readiness JSON 片段恢复为 dataclass。"""

    risk = payload["risk_gate"]
    signal = payload["signal"]
    position = payload["position_plan"]
    exit_plan = payload["exit_plan"]
    return (
        RiskGateResult(
            permission=_trade_permission_from_value(risk["permission"]),
            risk_level=risk.get("risk_level", "未知"),
            block_reasons=list(risk.get("block_reasons", [])),
            pause_reasons=list(risk.get("pause_reasons", [])),
            allow_reasons=list(risk.get("allow_reasons", [])),
            missing_evidence=list(risk.get("missing_evidence", [])),
        ),
        SignalResult(
            signal_level=_signal_level_from_value(signal["signal_level"]),
            strategy_type=signal.get("strategy_type", "未知策略"),
            signal_time=signal.get("signal_time"),
            signal_price=signal.get("signal_price"),
            confidence_score=float(signal.get("confidence_score", 0) or 0),
            evidence=list(signal.get("evidence", [])),
            invalidation_reasons=list(signal.get("invalidation_reasons", [])),
        ),
        PositionPlan(
            suggested_position_sol=float(position.get("suggested_position_sol", 0) or 0),
            max_position_sol=float(position.get("max_position_sol", 0) or 0),
            risk_per_trade_sol=float(position.get("risk_per_trade_sol", 0) or 0),
            stop_price=position.get("stop_price"),
            stop_type=position.get("stop_type", "未知"),
            position_reason=position.get("position_reason", ""),
        ),
        ExitPlan(
            hard_stop_price=exit_plan.get("hard_stop_price"),
            time_stop_minutes=int(exit_plan.get("time_stop_minutes", 0) or 0),
            take_profit_rules=list(exit_plan.get("take_profit_rules", [])),
            trailing_stop_rule=dict(exit_plan.get("trailing_stop_rule", {})),
            emergency_exit_rules=list(exit_plan.get("emergency_exit_rules", [])),
        ),
    )


def _get_attr(obj: Any, name: str, default: Any = None) -> Any:
    """兼容 dataclass 和 dict 的字段读取。"""

    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def _is_real_execution_candidate(risk_gate: Any, signal: Any, position_plan: Any, security_decision: Any) -> tuple[bool, List[str]]:
    """判断确认单是否具备进入人工确认层的条件。"""

    reasons: List[str] = []
    permission = _get_attr(risk_gate, "permission")
    signal_level = _get_attr(signal, "signal_level")
    suggested_position_sol = float(_get_attr(position_plan, "suggested_position_sol", 0.0) or 0.0)
    security_permission = str(_get_attr(security_decision, "permission", "UNKNOWN"))

    if permission not in {TradePermission.ALLOW_PAPER_TRADE, TradePermission.ALLOW_SMALL_REAL_WITH_CONFIRM}:
        reasons.append(f"风险门禁未放行：{_enum_value(permission)}")
    if signal_level not in {SignalLevel.S3, SignalLevel.S4}:
        reasons.append(f"信号等级不足或已失效：{_enum_value(signal_level)}")
    if suggested_position_sol <= 0:
        reasons.append("建议仓位为 0，禁止进入真实执行确认层")
    if security_permission in {"BLOCK_BUY", "BLOCK", "DENY"}:
        reasons.extend(_get_attr(security_decision, "reasons", []) or ["安全扫描阻断买入"])
    if security_permission == "PAUSE_NEED_CONFIRM":
        reasons.append("安全扫描需要额外人工确认，暂不自动放行")

    return len(reasons) == 0, reasons


def _quote_lines(quote_results: List[Any]) -> List[str]:
    """生成报价展示行。"""

    if not quote_results:
        return ["- 报价状态：暂无 GMGN/OKX 报价，真实执行前必须重新报价"]
    lines: List[str] = []
    for quote in quote_results:
        lines.extend([
            f"- 来源：{_get_attr(quote, 'source', '未知')}",
            f"  - 输入：{_get_attr(quote, 'input_amount', '')} {_get_attr(quote, 'input_token', '')}",
            f"  - 预估输出：{_get_attr(quote, 'output_amount', None)} {_get_attr(quote, 'output_token', '')}",
            f"  - 最小输出：{_get_attr(quote, 'min_output_amount', None)}",
            f"  - 价格影响：{_get_attr(quote, 'price_impact_pct', None)}%",
        ])
    return lines


def _markdown_for_ticket(
    *,
    token: str,
    chain: str,
    wallet_address: str,
    human_amount: str,
    real_execution_allowed: bool,
    block_reasons: List[str],
    risk_gate: Any,
    signal: Any,
    position_plan: Any,
    exit_plan: Any,
    security_decision: Any,
    quote_results: List[Any],
) -> str:
    """生成中文 Markdown 确认单。"""

    status = "允许进入人工确认层" if real_execution_allowed else "禁止真实执行"
    lines = [
        "# SIKK 半自动交易确认单",
        "",
        "## 基础信息",
        f"- 链：{chain}",
        f"- 代币地址：{token}",
        f"- 钱包地址：{wallet_address}",
        f"- 计划金额：{human_amount}",
        f"- 当前状态：{status}",
        "",
        "## 策略与风控摘要",
        f"- 风险门禁：{_enum_value(_get_attr(risk_gate, 'permission'))}",
        f"- 风险等级：{_get_attr(risk_gate, 'risk_level')}",
        f"- 信号等级：{_enum_value(_get_attr(signal, 'signal_level'))}",
        f"- 策略类型：{_get_attr(signal, 'strategy_type')}",
        f"- 信号时间：{_get_attr(signal, 'signal_time')}",
        f"- 信号价格：{_get_attr(signal, 'signal_price')}",
        f"- 建议纸面仓位SOL：{_get_attr(position_plan, 'suggested_position_sol')}",
        f"- 硬止损价：{_get_attr(exit_plan, 'hard_stop_price')}",
        "",
        "## 报价摘要",
        *_quote_lines(quote_results),
        "",
        "## 安全扫描摘要",
        f"- 安全权限：{_get_attr(security_decision, 'permission', 'UNKNOWN')}",
        f"- 安全等级：{_get_attr(security_decision, 'risk_level', 'UNKNOWN')}",
        f"- 数据源数量：{_get_attr(security_decision, 'source_count', 0)}",
    ]
    for reason in _get_attr(security_decision, "reasons", []) or []:
        lines.append(f"- 安全原因：{reason}")

    if block_reasons:
        lines.extend(["", "## 阻断原因"])
        for reason in block_reasons:
            lines.append(f"- {reason}")

    lines.extend([
        "",
        "## 人工确认要求",
        f"- 如后续需要进入真实执行层，必须人工输入：`{REQUIRED_CONFIRMATION_TEXT}`",
        "- 本确认单本身不执行真实交易，不广播交易，不创建 swap 命令。",
        "- 真实执行前必须重新校验报价、滑点、安全扫描和钱包权限。",
    ])
    return "\n".join(lines) + "\n"


def build_trade_confirmation_ticket(
    *,
    token: str,
    chain: str,
    wallet_address: str,
    human_amount: str,
    risk_gate: Any,
    signal: Any,
    position_plan: Any,
    exit_plan: Any,
    security_decision: Any,
    quote_results: Optional[List[Any]] = None,
) -> TradeConfirmationTicket:
    """构建 SIKK v0.3 半自动交易确认单。"""

    quotes = quote_results or []
    allowed, block_reasons = _is_real_execution_candidate(risk_gate, signal, position_plan, security_decision)
    summary = {
        "代币地址": token,
        "链": chain,
        "计划金额": human_amount,
        "风险门禁": _enum_value(_get_attr(risk_gate, "permission")),
        "信号等级": _enum_value(_get_attr(signal, "signal_level")),
        "策略类型": _get_attr(signal, "strategy_type"),
        "安全权限": _get_attr(security_decision, "permission", "UNKNOWN"),
        "是否允许进入人工确认层": allowed,
    }
    markdown = _markdown_for_ticket(
        token=token,
        chain=chain,
        wallet_address=wallet_address,
        human_amount=human_amount,
        real_execution_allowed=allowed,
        block_reasons=block_reasons,
        risk_gate=risk_gate,
        signal=signal,
        position_plan=position_plan,
        exit_plan=exit_plan,
        security_decision=security_decision,
        quote_results=quotes,
    )
    return TradeConfirmationTicket(
        token=token,
        chain=chain,
        wallet_address=wallet_address,
        human_amount=human_amount,
        required_confirmation_text=REQUIRED_CONFIRMATION_TEXT,
        real_execution_allowed=allowed,
        block_reasons=block_reasons,
        summary=summary,
        risk_gate=risk_gate,
        signal=signal,
        position_plan=position_plan,
        exit_plan=exit_plan,
        security_decision=security_decision,
        quote_results=quotes,
        markdown=markdown,
    )


def build_trade_confirmation_ticket_from_readiness_payload(
    *,
    readiness_payload: Dict[str, Any],
    chain: str,
    wallet_address: str,
    human_amount: str,
    security_decision: Any,
    quote_results: Optional[List[Any]] = None,
) -> TradeConfirmationTicket:
    """从 v0.1 readiness JSON + v0.2 安全/报价结果构建确认单。"""

    risk_gate, signal, position_plan, exit_plan = _readiness_sections_from_payload(readiness_payload)
    return build_trade_confirmation_ticket(
        token=readiness_payload.get("token", "UNKNOWN"),
        chain=chain,
        wallet_address=wallet_address,
        human_amount=human_amount,
        risk_gate=risk_gate,
        signal=signal,
        position_plan=position_plan,
        exit_plan=exit_plan,
        security_decision=security_decision,
        quote_results=quote_results or [],
    )


def write_trade_confirmation_ticket(ticket: TradeConfirmationTicket, output_dir: str | Path) -> Dict[str, str]:
    """写出确认单 Markdown 和 JSON。"""

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    md_path = out / "trade_confirmation_ticket.md"
    json_path = out / "trade_confirmation_ticket.json"
    md_path.write_text(ticket.markdown, encoding="utf-8")
    json_path.write_text(json.dumps(ticket.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    return {"markdown": str(md_path), "json": str(json_path)}
