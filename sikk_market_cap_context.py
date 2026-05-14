#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK-SOL v0.3 市值上下文标准化模块。

把 discovery/signal/wallet/paper/current/exit 的市值字段统一成可审计合约。
缺字段只标记 MISSING/待补，不编造。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

MARKET_CAP_FIELDS = [
    "discovery_market_cap_usd",
    "signal_market_cap_usd",
    "wallet_decision_market_cap_usd",
    "paper_entry_market_cap_usd",
    "current_market_cap_usd",
    "exit_market_cap_usd",
]


@dataclass
class MarketCapContext:
    token_address: str = ""
    token_symbol: str = ""
    discovery_market_cap_usd: float | None = None
    signal_market_cap_usd: float | None = None
    wallet_decision_market_cap_usd: float | None = None
    paper_entry_market_cap_usd: float | None = None
    current_market_cap_usd: float | None = None
    exit_market_cap_usd: float | None = None
    market_cap_change_from_discovery_pct: float | None = None
    market_cap_change_from_signal_pct: float | None = None
    market_cap_change_from_wallet_decision_pct: float | None = None
    market_cap_context_quality: str = "MISSING"
    market_cap_missing_fields: list[str] = field(default_factory=list)
    scope_note: str = "市值上下文只用于复盘发现/信号/钱包判断/paper/退出链路，不代表交易授权。"

    def to_dict(self) -> dict[str, Any]:
        return {
            "token_address": self.token_address,
            "token_symbol": self.token_symbol,
            "market_cap_context": {
                "discovery_market_cap_usd": self.discovery_market_cap_usd,
                "signal_market_cap_usd": self.signal_market_cap_usd,
                "wallet_decision_market_cap_usd": self.wallet_decision_market_cap_usd,
                "paper_entry_market_cap_usd": self.paper_entry_market_cap_usd,
                "current_market_cap_usd": self.current_market_cap_usd,
                "exit_market_cap_usd": self.exit_market_cap_usd,
                "market_cap_change_from_discovery_pct": self.market_cap_change_from_discovery_pct,
                "market_cap_change_from_signal_pct": self.market_cap_change_from_signal_pct,
                "market_cap_change_from_wallet_decision_pct": self.market_cap_change_from_wallet_decision_pct,
                "market_cap_context_quality": self.market_cap_context_quality,
                "market_cap_missing_fields": self.market_cap_missing_fields,
                "scope_note": self.scope_note,
            },
            "discovery_market_cap_usd": self.discovery_market_cap_usd,
            "signal_market_cap_usd": self.signal_market_cap_usd,
            "wallet_decision_market_cap_usd": self.wallet_decision_market_cap_usd,
            "paper_entry_market_cap_usd": self.paper_entry_market_cap_usd,
            "current_market_cap_usd": self.current_market_cap_usd,
            "exit_market_cap_usd": self.exit_market_cap_usd,
            "market_cap_change_from_discovery_pct": self.market_cap_change_from_discovery_pct,
            "market_cap_change_from_signal_pct": self.market_cap_change_from_signal_pct,
            "market_cap_change_from_wallet_decision_pct": self.market_cap_change_from_wallet_decision_pct,
            "market_cap_context_quality": self.market_cap_context_quality,
            "market_cap_missing_fields": self.market_cap_missing_fields,
            "说明": self.scope_note,
        }


def _first(mapping: Mapping[str, Any] | None, *keys: str, default: Any = None) -> Any:
    if not isinstance(mapping, Mapping):
        return default
    for key in keys:
        value = mapping.get(key)
        if value not in (None, "", [], {}):
            return value
    return default


def _num(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(str(value).replace("$", "").replace(",", "").strip())
    except (TypeError, ValueError):
        return None


def _pct(start: float | None, end: float | None) -> float | None:
    if start is None or end is None or start <= 0:
        return None
    return round((end - start) / start * 100, 4)


def _nested_market_cap(source: Mapping[str, Any] | None, key: str) -> Any:
    if not isinstance(source, Mapping):
        return None
    nested = source.get("market_cap_context")
    if isinstance(nested, Mapping):
        value = nested.get(key)
        if value not in (None, ""):
            return value
    return None


def build_market_cap_context(
    *,
    discovery_row: Mapping[str, Any] | None = None,
    signal_row: Mapping[str, Any] | None = None,
    wallet_row: Mapping[str, Any] | None = None,
    paper_row: Mapping[str, Any] | None = None,
    current_row: Mapping[str, Any] | None = None,
    exit_row: Mapping[str, Any] | None = None,
) -> MarketCapContext:
    token = str(
        _first(discovery_row, "token_address", "代币地址", default="")
        or _first(signal_row, "token_address", "代币地址", default="")
        or _first(wallet_row, "token_address", "代币地址", default="")
        or _first(paper_row, "token_address", "代币地址", default="")
        or _first(current_row, "token_address", "代币地址", default="")
        or _first(exit_row, "token_address", "代币地址", default="")
    )
    symbol = str(
        _first(discovery_row, "token_symbol", "symbol", "代币符号", default="")
        or _first(signal_row, "token_symbol", "symbol", "代币符号", default="")
        or _first(wallet_row, "token_symbol", "symbol", "代币符号", default="")
        or _first(paper_row, "token_symbol", "symbol", "代币符号", default="")
        or _first(current_row, "token_symbol", "symbol", "代币符号", default="")
        or _first(exit_row, "token_symbol", "symbol", "代币符号", default="")
    )

    discovery_mc = _num(_nested_market_cap(discovery_row, "discovery_market_cap_usd") or _first(discovery_row, "discovery_market_cap_usd", "发现市值USD", "发现市值", "initial_market_cap_usd", "market_cap_usd", "market_cap"))
    signal_mc = _num(_nested_market_cap(signal_row, "signal_market_cap_usd") or _first(signal_row, "signal_market_cap_usd", "信号市值USD", "信号市值", "market_cap_usd", "market_cap"))
    wallet_mc = _num(_nested_market_cap(wallet_row, "wallet_decision_market_cap_usd") or _first(wallet_row, "wallet_decision_market_cap_usd", "钱包决策市值USD", "钱包判断市值", "market_cap_usd", "market_cap"))
    paper_entry_mc = _num(_nested_market_cap(paper_row, "paper_entry_market_cap_usd") or _first(paper_row, "paper_entry_market_cap_usd", "入场市值USD", "entry_market_cap_usd", "market_cap_usd"))
    current_mc = _num(_nested_market_cap(current_row, "current_market_cap_usd") or _first(current_row, "current_market_cap_usd", "当前市值USD", "market_cap_usd", "market_cap"))
    exit_mc = _num(_nested_market_cap(exit_row, "exit_market_cap_usd") or _first(exit_row, "exit_market_cap_usd", "退出市值USD", "exit_market_cap_usd", "market_cap_usd"))

    values = {
        "discovery_market_cap_usd": discovery_mc,
        "signal_market_cap_usd": signal_mc,
        "wallet_decision_market_cap_usd": wallet_mc,
        "paper_entry_market_cap_usd": paper_entry_mc,
        "current_market_cap_usd": current_mc,
        "exit_market_cap_usd": exit_mc,
    }
    missing = [key for key, value in values.items() if value is None]
    present_count = len(values) - len(missing)
    if present_count == 0:
        quality = "MISSING"
    elif present_count < 3:
        quality = "PARTIAL"
    elif missing:
        quality = "DEGRADED"
    else:
        quality = "OK"

    return MarketCapContext(
        token_address=token,
        token_symbol=symbol,
        discovery_market_cap_usd=discovery_mc,
        signal_market_cap_usd=signal_mc,
        wallet_decision_market_cap_usd=wallet_mc,
        paper_entry_market_cap_usd=paper_entry_mc,
        current_market_cap_usd=current_mc,
        exit_market_cap_usd=exit_mc,
        market_cap_change_from_discovery_pct=_pct(discovery_mc, current_mc),
        market_cap_change_from_signal_pct=_pct(signal_mc, current_mc),
        market_cap_change_from_wallet_decision_pct=_pct(wallet_mc, current_mc),
        market_cap_context_quality=quality,
        market_cap_missing_fields=missing,
    )


def merge_market_cap_context(target: dict[str, Any], context: MarketCapContext | Mapping[str, Any]) -> dict[str, Any]:
    payload = context.to_dict() if isinstance(context, MarketCapContext) else dict(context)
    market_cap_context = payload.get("market_cap_context", payload)
    target["market_cap_context"] = dict(market_cap_context)
    for key in MARKET_CAP_FIELDS + [
        "market_cap_change_from_discovery_pct",
        "market_cap_change_from_signal_pct",
        "market_cap_change_from_wallet_decision_pct",
        "market_cap_context_quality",
        "market_cap_missing_fields",
    ]:
        if key in market_cap_context:
            target[key] = market_cap_context[key]
    return target


__all__ = ["MARKET_CAP_FIELDS", "MarketCapContext", "build_market_cap_context", "merge_market_cap_context"]
