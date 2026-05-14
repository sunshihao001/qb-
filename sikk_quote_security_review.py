"""SIKK v0.4 报价 + 安全扫描 + 确认单统一输出。

本模块生成交易前审查所需的 5 个文件：
- trade_confirmation_ticket.md
- trade_confirmation_ticket.json
- quote_snapshot.json
- security_scan_report.json
- quote_security_decision.json

安全边界：只聚合报价与安全扫描结果，不执行真实交易、不广播交易、不构造真实 swap execute 命令。
"""

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from sikk_execution_adapter_base import PreTradeSecurityDecision, QuoteResult, SecurityScanResult
from sikk_pre_trade_security_checker import evaluate_pre_trade_security
from sikk_trade_confirmation_ticket import build_trade_confirmation_ticket_from_readiness_payload, write_trade_confirmation_ticket


MAX_PRICE_IMPACT_BLOCK_PCT = 10.0
MAX_PRICE_IMPACT_PAUSE_PCT = 5.0
MAX_QUOTE_DEVIATION_PAUSE_PCT = 5.0


def _serialize(value: Any) -> Any:
    """递归序列化 dataclass / Enum / list / dict。"""

    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {key: _serialize(val) for key, val in asdict(value).items()}
    if isinstance(value, list):
        return [_serialize(item) for item in value]
    if isinstance(value, dict):
        return {key: _serialize(val) for key, val in value.items()}
    return value


def _now_utc_text() -> str:
    """当前 UTC 时间文本。"""

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _to_float(value: Any) -> Optional[float]:
    """把报价字符串尽量转为 float，失败返回 None。"""

    try:
        if value is None or value == "":
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _first_non_empty(data: Dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = data.get(key)
        if value not in (None, "", [], {}):
            return value
    return None


def _normal_time(value: Any) -> str:
    if value in (None, "", [], {}, 0, "0"):
        return ""
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return ""
        if "T" in text:
            return text.replace("+00:00", "Z")
        try:
            value = float(text)
        except ValueError:
            return text
    try:
        ts = float(value)
    except (TypeError, ValueError):
        return ""
    if ts > 10_000_000_000:
        ts = ts / 1000.0
    return datetime.fromtimestamp(ts, tz=timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _provider_time(raw: Dict[str, Any], *keys: str) -> str:
    data = raw.get("data") if isinstance(raw.get("data"), dict) else {}
    for key in keys:
        value = _first_non_empty(raw, key)
        if value not in (None, "", [], {}):
            return _normal_time(value)
        value = _first_non_empty(data, key)
        if value not in (None, "", [], {}):
            return _normal_time(value)
    return ""


def _enrich_quote(quote: QuoteResult, requested_at: str, received_at: str) -> Dict[str, Any]:
    row = _serialize(quote)
    provider_time = _provider_time(quote.raw or {}, "quote_time", "timestamp", "time", "createdAt", "created_at", "ts")
    quote_time = provider_time or received_at
    row.update({
        "token_address": quote.output_token,
        "quote_source": quote.source,
        "quote_requested_at": requested_at,
        "quote_received_at": received_at,
        "quote_time": quote_time,
        "quote_time_source": "provider_timestamp" if provider_time else "received_at_fallback",
    })
    return row


def _enrich_scan(scan: SecurityScanResult, started_at: str, finished_at: str) -> Dict[str, Any]:
    row = _serialize(scan)
    provider_time = _provider_time(scan.raw or {}, "security_scan_time", "scanTime", "scan_time", "timestamp", "time", "createdAt", "created_at", "ts")
    scan_time = provider_time or finished_at
    row.update({
        "token_address": scan.token_address,
        "security_scan_started_at": started_at,
        "security_scan_finished_at": finished_at,
        "security_scan_time": scan_time,
        "security_scan_created_at": finished_at,
        "security_scan_time_source": "provider_timestamp" if provider_time else "finished_at_fallback",
    })
    return row


def _quote_deviation_pct(quotes: List[QuoteResult]) -> Optional[float]:
    """用 output_amount 粗略计算多源报价偏离百分比。"""

    values = [_to_float(q.output_amount) for q in quotes]
    values = [v for v in values if v is not None and v > 0]
    if len(values) < 2:
        return None
    high = max(values)
    low = min(values)
    mid = (high + low) / 2
    if mid <= 0:
        return None
    return round((high - low) / mid * 100, 6)


def _max_price_impact(quotes: List[QuoteResult]) -> Optional[float]:
    """取所有报价中的最大价格影响。"""

    impacts = [q.price_impact_pct for q in quotes if q.price_impact_pct is not None]
    if not impacts:
        return None
    return max(float(v) for v in impacts)


def build_quote_snapshot(
    *,
    token: str,
    chain: str,
    wallet_address: str,
    human_amount: str,
    quote_results: Iterable[QuoteResult],
    snapshot_time: Optional[str] = None,
    max_quote_age_seconds: int = 30,
) -> Dict[str, Any]:
    """构建报价快照；输入为已获取的只读报价结果。"""

    quotes = list(quote_results)
    deviation_pct = _quote_deviation_pct(quotes)
    max_impact = _max_price_impact(quotes)
    requested_at = snapshot_time or _now_utc_text()
    received_at = requested_at
    enriched_quotes = [_enrich_quote(q, requested_at, received_at) for q in quotes]
    quote_time = ""
    quote_time_source = ""
    for row in enriched_quotes:
        if row.get("quote_time"):
            quote_time = row["quote_time"]
            quote_time_source = row.get("quote_time_source", "")
            if quote_time_source == "provider_timestamp":
                break
    if not quote_time:
        quote_time = received_at
        quote_time_source = "received_at_fallback"
    return {
        "token": token,
        "token_address": token,
        "chain": chain,
        "wallet_address": wallet_address,
        "human_amount": human_amount,
        "snapshot_time": requested_at,
        "quote_source": ",".join(q.source for q in quotes),
        "quote_requested_at": requested_at,
        "quote_received_at": received_at,
        "quote_time": quote_time,
        "quote_time_source": quote_time_source,
        "max_quote_age_seconds": max_quote_age_seconds,
        "quote_status": "AVAILABLE" if quotes else "MISSING",
        "source_count": len(quotes),
        "sources": [q.source for q in quotes],
        "max_price_impact_pct": max_impact,
        "quote_deviation_pct": deviation_pct,
        "quotes": enriched_quotes,
        "scope_note": "只读报价快照；不执行真实交易。",
    }


def build_security_scan_report(
    *,
    token: str,
    chain: str,
    scan_results: Iterable[SecurityScanResult],
    snapshot_time: Optional[str] = None,
) -> Dict[str, Any]:
    """构建安全扫描报告，并复用 v0.2 聚合器生成安全门禁。"""

    scans = list(scan_results)
    decision = evaluate_pre_trade_security(scans)
    started_at = snapshot_time or _now_utc_text()
    finished_at = started_at
    enriched_scans = [_enrich_scan(s, started_at, finished_at) for s in scans]
    scan_time = ""
    scan_time_source = ""
    for row in enriched_scans:
        if row.get("security_scan_time"):
            scan_time = row["security_scan_time"]
            scan_time_source = row.get("security_scan_time_source", "")
            if scan_time_source == "provider_timestamp":
                break
    if not scan_time:
        scan_time = finished_at
        scan_time_source = "finished_at_fallback"
    return {
        "token": token,
        "token_address": token,
        "chain": chain,
        "snapshot_time": started_at,
        "security_scan_started_at": started_at,
        "security_scan_finished_at": finished_at,
        "security_scan_time": scan_time,
        "security_scan_created_at": finished_at,
        "security_scan_time_source": scan_time_source,
        "scan_status": "AVAILABLE" if scans else "MISSING",
        "source_count": len(scans),
        "sources": [s.source for s in scans],
        "scan_results": enriched_scans,
        "pre_trade_security_decision": _serialize(decision),
        "scope_note": "安全扫描报告只用于交易前审查；扫描缺失不是安全通过。",
    }


def _security_decision_from_report(security_report: Dict[str, Any]) -> PreTradeSecurityDecision:
    """从报告恢复 PreTradeSecurityDecision。"""

    d = security_report["pre_trade_security_decision"]
    return PreTradeSecurityDecision(
        permission=d.get("permission", "PAUSE_NEED_CONFIRM"),
        risk_level=d.get("risk_level", "UNKNOWN"),
        requires_user_confirmation=bool(d.get("requires_user_confirmation", True)),
        reasons=list(d.get("reasons", [])),
        source_count=int(d.get("source_count", 0) or 0),
    )


def build_quote_security_decision(quote_snapshot: Dict[str, Any], security_report: Dict[str, Any]) -> Dict[str, Any]:
    """综合报价快照与安全扫描，生成交易前审查总决策。"""

    reasons: List[str] = []
    final_permission = "ALLOW_CONFIRMATION_LAYER"

    if quote_snapshot.get("quote_status") != "AVAILABLE" or int(quote_snapshot.get("source_count", 0) or 0) <= 0:
        final_permission = "PAUSE_NEED_CONFIRM"
        reasons.append("缺少有效报价")

    max_impact = quote_snapshot.get("max_price_impact_pct")
    if max_impact is not None:
        if float(max_impact) > MAX_PRICE_IMPACT_BLOCK_PCT:
            final_permission = "BLOCK_BUY"
            reasons.append(f"价格影响过高：{max_impact}% > {MAX_PRICE_IMPACT_BLOCK_PCT}%")
        elif float(max_impact) > MAX_PRICE_IMPACT_PAUSE_PCT and final_permission != "BLOCK_BUY":
            final_permission = "PAUSE_NEED_CONFIRM"
            reasons.append(f"价格影响偏高：{max_impact}% > {MAX_PRICE_IMPACT_PAUSE_PCT}%")

    deviation = quote_snapshot.get("quote_deviation_pct")
    if deviation is not None and float(deviation) > MAX_QUOTE_DEVIATION_PAUSE_PCT and final_permission != "BLOCK_BUY":
        final_permission = "PAUSE_NEED_CONFIRM"
        reasons.append(f"GMGN/OKX 多源报价偏离较大：{deviation}% > {MAX_QUOTE_DEVIATION_PAUSE_PCT}%")

    security_decision = _security_decision_from_report(security_report)
    if security_decision.permission == "BLOCK_BUY":
        final_permission = "BLOCK_BUY"
        reasons.extend(security_decision.reasons)
    elif security_decision.permission in {"PAUSE_NEED_CONFIRM", "WARN_CONTINUE", "WARN_ALLOW_SELL"} and final_permission != "BLOCK_BUY":
        final_permission = "PAUSE_NEED_CONFIRM"
        reasons.extend(security_decision.reasons)

    if security_report.get("scan_status") != "AVAILABLE" or security_decision.source_count <= 0:
        if final_permission != "BLOCK_BUY":
            final_permission = "PAUSE_NEED_CONFIRM"
        if not any("安全扫描结果缺失" in r for r in reasons):
            reasons.append("安全扫描结果缺失，需要人工确认")

    if not reasons:
        reasons.append("报价与安全扫描未触发硬阻断，可进入人工确认层")

    return {
        "token": quote_snapshot.get("token"),
        "token_address": quote_snapshot.get("token_address") or quote_snapshot.get("token"),
        "chain": quote_snapshot.get("chain"),
        "snapshot_time": quote_snapshot.get("snapshot_time"),
        "quote_source": quote_snapshot.get("quote_source"),
        "quote_requested_at": quote_snapshot.get("quote_requested_at"),
        "quote_received_at": quote_snapshot.get("quote_received_at"),
        "quote_time": quote_snapshot.get("quote_time"),
        "quote_time_source": quote_snapshot.get("quote_time_source"),
        "security_scan_started_at": security_report.get("security_scan_started_at"),
        "security_scan_finished_at": security_report.get("security_scan_finished_at"),
        "security_scan_time": security_report.get("security_scan_time"),
        "security_scan_created_at": security_report.get("security_scan_created_at"),
        "security_scan_time_source": security_report.get("security_scan_time_source"),
        "final_permission": final_permission,
        "requires_user_confirmation": final_permission != "BLOCK_BUY",
        "quote_status": quote_snapshot.get("quote_status"),
        "security_permission": security_decision.permission,
        "security_risk_level": security_decision.risk_level,
        "quote_source_count": quote_snapshot.get("source_count", 0),
        "security_source_count": security_decision.source_count,
        "max_price_impact_pct": max_impact,
        "quote_deviation_pct": deviation,
        "reasons": reasons,
        "scope_note": "quote_security_decision 只决定能否进入人工确认层，不执行真实交易。",
    }


def _decision_to_security_gate(decision: Dict[str, Any], security_report: Dict[str, Any]) -> PreTradeSecurityDecision:
    """把总决策转成确认单可消费的安全门禁对象。"""

    if decision["final_permission"] == "BLOCK_BUY":
        permission = "BLOCK_BUY"
    elif decision["final_permission"] == "ALLOW_CONFIRMATION_LAYER":
        permission = "ALLOW"
    else:
        permission = "PAUSE_NEED_CONFIRM"
    return PreTradeSecurityDecision(
        permission=permission,
        risk_level=decision.get("security_risk_level", "UNKNOWN"),
        requires_user_confirmation=decision.get("requires_user_confirmation", True),
        reasons=list(decision.get("reasons", [])),
        source_count=int(decision.get("security_source_count", 0) or 0),
    )


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    """写 JSON 文件。"""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def build_and_write_pre_trade_review(
    *,
    output_dir: str | Path,
    readiness_payload: Dict[str, Any],
    chain: str,
    wallet_address: str,
    human_amount: str,
    quote_results: Iterable[QuoteResult],
    security_scan_results: Iterable[SecurityScanResult],
    snapshot_time: Optional[str] = None,
) -> Dict[str, str]:
    """统一写出 v0.4 交易前审查五文件。"""

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    token = readiness_payload.get("token", "UNKNOWN")

    quote_list = list(quote_results)
    scan_list = list(security_scan_results)
    quote_snapshot = build_quote_snapshot(
        token=token,
        chain=chain,
        wallet_address=wallet_address,
        human_amount=human_amount,
        quote_results=quote_list,
        snapshot_time=snapshot_time,
    )
    security_report = build_security_scan_report(token=token, chain=chain, scan_results=scan_list, snapshot_time=snapshot_time)
    quote_security_decision = build_quote_security_decision(quote_snapshot, security_report)
    security_gate = _decision_to_security_gate(quote_security_decision, security_report)

    ticket = build_trade_confirmation_ticket_from_readiness_payload(
        readiness_payload=readiness_payload,
        chain=chain,
        wallet_address=wallet_address,
        human_amount=human_amount,
        security_decision=security_gate,
        quote_results=quote_list,
    )
    ticket_paths = write_trade_confirmation_ticket(ticket, out)

    quote_path = out / "quote_snapshot.json"
    security_path = out / "security_scan_report.json"
    decision_path = out / "quote_security_decision.json"
    _write_json(quote_path, quote_snapshot)
    _write_json(security_path, security_report)
    _write_json(decision_path, quote_security_decision)

    return {
        "trade_confirmation_ticket_md": ticket_paths["markdown"],
        "trade_confirmation_ticket_json": ticket_paths["json"],
        "quote_snapshot_json": str(quote_path),
        "security_scan_report_json": str(security_path),
        "quote_security_decision_json": str(decision_path),
    }
