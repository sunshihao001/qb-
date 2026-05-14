# -*- coding: utf-8 -*-
"""Scenario classifier for the compressed P06 step."""
from __future__ import annotations

from typing import Any, Dict, List

SCENARIOS = [
    "吸筹", "二段扩张", "高位派发", "下跌再派发", "诱多反抽", "退出流动性陷阱", "假横盘", "再吸筹", "末端拉盘派发", "刷量假突破", "接盘鲸鱼陷阱", "证据不足观察",
]


def _num(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, ""):
            return default
        return float(value)
    except Exception:
        return default


def classify_scenario(context: Dict[str, Any], wallet_eval: Dict[str, Any]) -> Dict[str, Any]:
    kline = context.get("kline_rows") or []
    qs = context.get("quote_security") or {}
    liquidity = _num(qs.get("liquidity_usd") or qs.get("liquidity") or qs.get("流动性"), 0.0)
    market_cap = _num(context.get("token_basic", {}).get("market_cap_usd") or context.get("token_basic", {}).get("market_cap") or context.get("token_basic", {}).get("市值"), 0.0)
    risk = _num(wallet_eval.get("risk_score"), 0.0)
    support = _num(wallet_eval.get("support_score"), 0.0)
    scenario = "证据不足观察"
    confidence = 0.35
    reasons: List[str] = []

    if wallet_eval.get("exit_liquidity_risk"):
        scenario = "退出流动性陷阱"
        confidence = 0.72
        reasons.append("结构方撤退 + 接盘鲸鱼压力同时存在")
    elif wallet_eval.get("structure_retreat_hint") and risk >= 55:
        scenario = "高位派发"
        confidence = 0.66
        reasons.append("高卖出/派发钱包占比较高")
    elif wallet_eval.get("chip_cleared_hint"):
        scenario = "下跌再派发"
        confidence = 0.58
        reasons.append("多钱包出现清仓/高卖出特征")
    elif wallet_eval.get("second_accumulation_hint") and support >= 35:
        scenario = "再吸筹"
        confidence = 0.58
        reasons.append("存在结构钱包候选且未见明显撤退")
    elif wallet_eval.get("early_control_hint") and support >= 45:
        scenario = "吸筹"
        confidence = 0.62
        reasons.append("早期结构钱包候选 + 筹码集中")
    elif kline and support >= 35 and risk < 55:
        scenario = "二段扩张"
        confidence = 0.50
        reasons.append("有K线背景且结构支持分未被风险压倒")
    elif liquidity and market_cap and liquidity / max(market_cap, 1.0) < 0.02 and risk >= 45:
        scenario = "接盘鲸鱼陷阱"
        confidence = 0.55
        reasons.append("流动性/市值比例偏低且钱包风险存在")
    else:
        reasons.append("关键价格/钱包/成交字段不足，保持观察")

    counter = []
    if not kline:
        counter.append("缺少K线/成交量，无法确认突破、横盘、诱多反抽")
    if "quote_security" in (context.get("missing_fields") or []):
        counter.append("缺少quote/security，无法确认流动性陷阱强度")
    return {
        "scenario": scenario,
        "confidence": round(confidence, 2),
        "reasons": reasons,
        "counter_evidence": counter,
        "allowed_scenarios": SCENARIOS,
    }
