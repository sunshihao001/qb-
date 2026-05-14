# -*- coding: utf-8 -*-
"""Wallet/chip structure gate for lightweight personal replay."""
from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List


def num(row: Dict[str, Any], *keys: str, default: float = 0.0) -> float:
    for key in keys:
        value = row.get(key)
        if value in (None, "", [], {}):
            continue
        try:
            value = float(value)
            if key.lower().endswith("percentage") and value > 1:
                value = value / 100.0
            return value
        except Exception:
            continue
    return default


def text(row: Dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = row.get(key)
        if value not in (None, "", [], {}):
            if isinstance(value, list):
                return ",".join(str(x) for x in value)
            return str(value)
    return ""


def classify_wallet(row: Dict[str, Any]) -> Dict[str, Any]:
    tag_text = text(row, "GMGN标签", "tags", "maker_token_tags", "tag", "role_candidates", "当前角色", "role_candidate").lower()
    hold = num(row, "持仓占比", "holding_ratio", "amount_percentage", "balance_ratio", "percentage")
    sell = num(row, "卖出占比", "sell_ratio", "sell_amount_percentage", "sold_ratio")
    profit = num(row, "profit", "total_profit", "pnl", "收益", default=0.0)
    addr = text(row, "钱包地址", "wallet_address", "address", "wallet", "owner", "holder_address")

    role = "普通/未知钱包"
    evidence = "E1"
    risk = 0
    reasons: List[str] = []
    if any(k in tag_text for k in ["bundler", "bundle", "insider", "sniper", "fresh", "new wallet", "新钱包"]):
        role = "疑似庄家早期/结构钱包候选"
        evidence = "E3"
        risk += 2
        reasons.append("GMGN早期/捆绑/新钱包标签")
    if any(k in tag_text for k in ["transfer", "分发", "接收"]):
        role = "分发/接收钱包候选"
        evidence = "E3"
        risk += 1
        reasons.append("存在transfer/分发接收特征")
    if sell >= 0.7:
        role = "高卖出/疑似派发钱包"
        evidence = "E4"
        risk += 2
        reasons.append(f"卖出占比高({sell:.2f})")
    if hold >= 0.03:
        risk += 1
        reasons.append(f"单钱包持仓占比较高({hold:.2f})")
    if profit > 0 and sell >= 0.5:
        reasons.append("盈利钱包已明显卖出")
    return {
        "address": addr,
        "role": role,
        "evidence_level": evidence,
        "risk_score": risk,
        "holding_ratio": hold,
        "sell_ratio": sell,
        "profit": profit,
        "tags": tag_text,
        "reason": "；".join(reasons) if reasons else "证据不足，仅保留观察",
        "source_row": row,
    }


def evaluate_wallet_structure(context: Dict[str, Any]) -> Dict[str, Any]:
    rows = context.get("wallet_rows") or []
    classified = [classify_wallet(r) for r in rows if isinstance(r, dict)]
    top_hold = sum(sorted([x["holding_ratio"] for x in classified], reverse=True)[:10])
    high_sell = [x for x in classified if x["sell_ratio"] >= 0.7]
    early_struct = [x for x in classified if "结构钱包" in x["role"] or "庄家早期" in x["role"]]
    distribute = [x for x in classified if "派发" in x["role"] or "分发" in x["role"]]
    whales = [x for x in classified if x["holding_ratio"] >= 0.03]
    role_counts = Counter(x["role"] for x in classified)

    evidence: List[str] = []
    counter: List[str] = []
    missing: List[str] = []
    if not rows:
        missing.append("wallet_rows")
        counter.append("没有可用钱包结构数据，不能形成强结构判断")
    if early_struct:
        evidence.append(f"发现 {len(early_struct)} 个疑似早期/结构钱包候选")
    else:
        counter.append("未发现明确早期结构钱包候选")
    if high_sell:
        evidence.append(f"发现 {len(high_sell)} 个高卖出/派发钱包")
    if top_hold >= 0.25:
        evidence.append(f"Top钱包持仓集中度偏高({top_hold:.2%})")
    elif rows:
        counter.append(f"Top钱包持仓集中度未达到强集中阈值({top_hold:.2%})")

    same_source_hint = len(early_struct) >= 3 or sum(1 for x in classified if "bundler" in x["tags"] or "fresh" in x["tags"]) >= 3
    structure_retreat = len(high_sell) >= 3 or (distribute and sum(x["sell_ratio"] for x in distribute) / max(1, len(distribute)) >= 0.6)
    buyer_pressure = len(whales) >= 3 and structure_retreat

    risk_score = min(100, len(early_struct) * 12 + len(high_sell) * 10 + int(top_hold * 100) + (20 if structure_retreat else 0))
    support_score = min(100, len(early_struct) * 15 + int(top_hold * 80) - len(high_sell) * 8)

    if not rows:
        status = "NO_DATA"
    elif structure_retreat and buyer_pressure:
        status = "EXIT_LIQUIDITY_RISK"
    elif support_score >= 45 and risk_score < 70:
        status = "STRUCTURE_OBSERVABLE"
    elif risk_score >= 70:
        status = "HIGH_RISK_STRUCTURE"
    else:
        status = "WEAK_STRUCTURE"

    return {
        "status": status,
        "classified_wallets": classified[:80],
        "role_counts": dict(role_counts),
        "top_holder_concentration_estimate": top_hold,
        "same_source_hint": same_source_hint,
        "sync_buy_sell_hint": same_source_hint and (len(high_sell) > 0),
        "early_control_hint": bool(early_struct and top_hold >= 0.15),
        "structure_retreat_hint": bool(structure_retreat),
        "buyer_whale_pressure_hint": bool(buyer_pressure),
        "chip_concentrated": top_hold >= 0.25,
        "chip_distribution_hint": bool(distribute or high_sell),
        "chip_cleared_hint": len(high_sell) >= max(3, len(classified) // 4) if classified else False,
        "second_accumulation_hint": bool(early_struct and not structure_retreat and 0.08 <= top_hold < 0.35),
        "exit_liquidity_risk": bool(structure_retreat and buyer_pressure),
        "risk_score": risk_score,
        "support_score": support_score,
        "evidence": evidence,
        "counter_evidence": counter,
        "missing_fields": missing,
    }
