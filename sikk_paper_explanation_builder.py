#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK Paper Position Case File / natural-language explanation builder.

只把 paper position 的结构化字段转换为单笔实战档案；不执行真实 swap、不签名、不广播。
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional

from sikk_case_field_source_map import enrich_position_for_case_file
from sikk_operator_psychology_engine import evaluate_operator_psychology

BOUNDARY_NOTE = "纸面验证档案；不执行真实 swap，不读取私钥，不签名，不广播。"


def read_json(path: str | Path, default: Any) -> Any:
    p = Path(path)
    if not p.exists():
        return default
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return default


def write_json(path: str | Path, payload: Mapping[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def read_jsonl(path: str | Path) -> List[Dict[str, Any]]:
    p = Path(path)
    if not p.exists():
        return []
    rows: List[Dict[str, Any]] = []
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            if isinstance(obj, dict):
                rows.append(obj)
        except Exception:
            rows.append({"raw": line})
    return rows


def val(row: Mapping[str, Any], *keys: str, default: Any = "") -> Any:
    for key in keys:
        value = row.get(key)
        if value is not None and value != "":
            return value
    return default


def num(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except Exception:
        return default


def pct_text(value: Any) -> str:
    if value is None or value == "":
        return "待补"
    return f"{num(value):.4g}%"


def money_text(value: Any) -> str:
    if value is None or value == "":
        return "待补"
    return f"{num(value):,.4g} USD"


def slug(text: Any) -> str:
    raw = str(text or "unknown")
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", raw)[:140] or "unknown"


def _result_type(pnl: Any) -> str:
    v = num(pnl, 0.0)
    if v >= 100:
        return "BIG_WIN"
    if v > 0:
        return "WIN"
    if v < 0:
        return "LOSS"
    return "FLAT"


def _failure_type(position: Mapping[str, Any]) -> Any:
    pnl = num(val(position, "net_pnl_pct", "最终收益率_pct", "live_pnl_pct", default=0), 0.0)
    failure = val(position, "failure_type", default=None)
    if pnl > 0:
        return None
    return failure or val(position, "exit_reason_code", "exit_reason", default="UNCLASSIFIED")


def _discovery_explanation(position: Mapping[str, Any]) -> str:
    symbol = val(position, "token_symbol", "代币符号", default="该 token")
    cap = money_text(val(position, "discovery_market_cap_usd", default=""))
    liq = money_text(val(position, "discovery_liquidity_usd", default=""))
    holders = val(position, "discovery_holder_count", default="待补")
    reason = val(position, "discovery_reason", default="进入 GMGN/SIKK 候选观察池，等待盘型、信号和钱包结构进一步确认。")
    return f"系统在 {val(position,'candidate_discovered_at', default='待补')} 发现 {symbol}。发现时市值 {cap}，流动性 {liq}，持有人 {holders}。纳入观察原因：{reason}"


def _pattern_explanation(position: Mapping[str, Any]) -> str:
    pattern = val(position, "pattern_type", "strategy_name", "strategy_type", default="SIKK-B 控盘箱体突破回踩")
    low = val(position, "control_box_low", default="待补")
    high = val(position, "control_box_high", default="待补")
    avwap = val(position, "avwap_price", default="待补")
    status = val(position, "price_structure_status", default="待补")
    return f"当前盘型记录为 {pattern}。控制箱体区间 low={low}、high={high}，AVWAP={avwap}，价格结构状态={status}。该解释用于确认是否属于结构性回踩，而不是简单追涨。"


def _signal_explanation(position: Mapping[str, Any]) -> str:
    return f"信号在 {val(position,'signal_time', default='待补')} 触发，等级为 {val(position,'signal_level', default='待补')}，类型为 {val(position,'signal_type','strategy_type', default='待补')}。信号价 {val(position,'signal_price','signal_entry_price', default='待补')}，信号时市值 {money_text(val(position,'signal_market_cap_usd', default=''))}。失效条件：{val(position,'invalid_conditions','invalid_level', default='跌破关键结构位或钱包结构转弱。')}"


def _wallet_explanation(position: Mapping[str, Any]) -> str:
    status = val(position, "entry_wallet_structure_status", "wallet_structure_status", default="待补")
    score = val(position, "entry_wallet_structure_score", "wallet_structure_score", default="待补")
    risk = val(position, "entry_wallet_risk_score", "wallet_risk_score", default="待补")
    cp = val(position, "entry_counterparty_pressure_score", "counterparty_pressure_score", default="待补")
    quality = val(position, "entry_data_quality_score", "data_quality_score", default="待补")
    reason = val(position, "entry_wallet_reason", "wallet_structure_reason", default="未记录具体钱包说明。")
    return f"钱包结构在 {val(position,'wallet_decision_time', default='待补')} 给出 {status}。结构分 {score}，风险分 {risk}，对手盘压力 {cp}，数据质量 {quality}。钱包解释：{reason}。钱包结构在这里是纸面验证门禁，不是实盘买入授权。"


def _quote_security_explanation(position: Mapping[str, Any]) -> str:
    return f"Quote/Security 检查状态：quote_gate={val(position,'quote_gate','quote_security_state', default='待补')}，quote_source={val(position,'quote_source','entry_quote_source', default='待补')}，价格偏差={pct_text(val(position,'price_deviation_pct', default=''))}，security_gate={val(position,'security_gate', default='待补')}。该层只确认纸面可执行性，不触发真实交易。"


def _entry_explanation(position: Mapping[str, Any]) -> str:
    change = val(position, "entry_market_cap_change_from_discovery_pct", default="")
    context = val(position, "market_cap_context_status", default="UNKNOWN_ENTRY")
    return (
        f"纸面仓位在 {val(position,'paper_entry_time','entry_time', default='待补')} 入场。"
        f"入场模式 {val(position,'entry_price_mode', default='待补')}，原始报价 {val(position,'entry_raw_quote_price','live_entry_price', default='待补')}，"
        f"模拟入场价 {val(position,'entry_simulated_price','paper_entry_price','entry_price', default='待补')}，滑点 {val(position,'entry_slippage_pct', default='待补')}%。"
        f"入场时市值 {money_text(val(position,'entry_market_cap_usd','paper_entry_market_cap_usd', default=''))}，"
        f"相对发现时市值变化 {pct_text(change)}，上下文为 {context}。"
        f"本次纸面规模 {val(position,'paper_size_sol','position_sol', default='待补')} SOL，约 {money_text(val(position,'paper_size_usd', default=''))}，"
        f"估算 token 数量 {val(position,'estimated_token_amount', default='待补')}。入场依据：{val(position,'entry_reason_summary', default='盘型、信号、钱包结构和 quote/security 同时满足纸面验证条件。')}"
    )


def _holding_explanation(journal: List[Mapping[str, Any]]) -> str:
    if not journal:
        return "暂无持仓过程 journal；后续每轮 paper update 会写入价格、市值、浮盈回撤、钱包状态和动作。"
    last = journal[-1]
    return f"持仓过程已记录 {len(journal)} 条 journal。最近一次 {val(last,'time', default='待补')}，价格 {val(last,'current_price', default='待补')}，浮动收益 {pct_text(val(last,'unrealized_pnl_pct', default=''))}，动作 {val(last,'paper_action', default='待补')}，原因 {val(last,'monitor_reason', default='待补')}。"


def _exit_explanation(position: Mapping[str, Any]) -> str:
    if not val(position, "exit_time", default="") and str(val(position,"status",default="")).upper() == "OPEN":
        return "该仓位仍处于 OPEN，尚未退出；退出解释将在止损、钱包结构、时间止损或其他纸面退出触发后生成。"
    return f"纸面仓位在 {val(position,'exit_time', default='待补')} 退出，退出价 {val(position,'exit_price', default='待补')}，退出市值 {money_text(val(position,'exit_market_cap_usd', default=''))}。退出触发 {val(position,'exit_trigger', default='待补')}，原因码 {val(position,'exit_reason_code','failure_type', default='待补')}，原因：{val(position,'exit_reason','failure_reason', default='待补')}。"


def _post_trade_review(position: Mapping[str, Any]) -> str:
    pnl = val(position, "net_pnl_pct", "最终收益率_pct", "live_pnl_pct", default="")
    result = _result_type(pnl)
    if result in {"WIN", "BIG_WIN"}:
        return f"本次结果为 {result}，收益 {pct_text(pnl)}。盈利交易不自动写 failure_type；需要继续判断收益是否来自策略证据链，还是右尾偶然。"
    if result == "LOSS":
        return f"本次结果为 LOSS，收益 {pct_text(pnl)}。需要重点复查入场是否追高、钱包结构是否误判、quote/security 是否延迟，以及退出是否过慢。"
    return "本次结果暂为 FLAT/未完成，需要继续观察持仓路径和退出触发。"


def _strategy_adjustment(position: Mapping[str, Any]) -> str:
    context = val(position, "market_cap_context_status", default="UNKNOWN_ENTRY")
    exit_action = val(position, "wallet_exit_action", "wallet_position_action", default="")
    suggestions = []
    if context in {"LATE_ENTRY", "CHASE_ENTRY"}:
        suggestions.append("入场市值相对发现时涨幅偏高，后续应提高追高过滤或降低仓位。")
    if exit_action == "EXIT_MONITOR":
        suggestions.append("钱包结构已进入 EXIT_MONITOR，后续需要用多轮 delta 与价格结构确认，避免过早强退。")
    if not suggestions:
        suggestions.append("继续积累同类样本，按入场市值分桶、钱包结构状态和退出原因统计策略稳定性。")
    return "；".join(suggestions)


def _operator_psychology_section(position: Mapping[str, Any]) -> Dict[str, Any]:
    psychology = evaluate_operator_psychology(position)
    raw_invalidators = psychology.get("invalidation_conditions") or []
    if isinstance(raw_invalidators, str):
        invalidators = [raw_invalidators]
    else:
        invalidators = list(raw_invalidators)
    return {
        "operator_lifecycle_stage": psychology.get("operator_lifecycle_stage", "UNKNOWN"),
        "operator_psychology": psychology.get("operator_psychology", "DATA_INSUFFICIENT"),
        "operator_psychology_label": psychology.get("operator_psychology_label", "证据不足 / 待复查"),
        "dominant_side_intent": psychology.get("dominant_side_intent", "UNKNOWN"),
        "counterparty_psychology": psychology.get("counterparty_psychology", "UNKNOWN"),
        "liquidity_intent": psychology.get("liquidity_intent", "UNKNOWN"),
        "trap_risk_type": psychology.get("trap_risk_type", "UNKNOWN"),
        "structure_defense_status": psychology.get("structure_defense_status", "UNKNOWN"),
        "chip_control_state": psychology.get("chip_control_state", "CONTROL_UNCLEAR"),
        "paper_trade_alignment": psychology.get("paper_trade_alignment", "DATA_INSUFFICIENT"),
        "psychology_evidence_level": psychology.get("psychology_evidence_level", "E1"),
        "psychology_explanation": psychology.get("psychology_reason", "主导侧心理解释：证据不足，待复查。"),
        "next_observation_focus": psychology.get("next_observation_focus", "复查生命周期、钱包结构、市值上下文。"),
        "invalidation_conditions": invalidators,
        "scope_note": psychology.get("scope_note", BOUNDARY_NOTE),
    }


def _case_quality(position: Mapping[str, Any], journal: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    checks = {
        "发现时市值": val(position, "discovery_market_cap_usd", default=""),
        "入场市值": val(position, "entry_market_cap_usd", "paper_entry_market_cap_usd", default=""),
        "钱包结构状态": val(position, "entry_wallet_structure_status", "wallet_structure_status", default=""),
        "钱包结构分数": val(position, "entry_wallet_structure_score", "wallet_structure_score", default=""),
        "对手盘压力": val(position, "entry_counterparty_pressure_score", "counterparty_pressure_score", default=""),
        "主导侧生命周期": val(position, "operator_lifecycle_stage", "dominant_side_lifecycle", "dominant_side_intent", "wallet_structure_status", default=""),
        "纸面入场时间": val(position, "paper_entry_time", "entry_time", default=""),
        "paper entry snapshot": val(position, "paper_entry_snapshot", "entry_market_cap_usd", "paper_entry_market_cap_usd", default=""),
        "持仓 journal": journal,
    }
    if str(val(position, "status", default="")).upper() == "CLOSED":
        checks.update({
            "退出时间": val(position, "exit_time", default=""),
            "退出价格": val(position, "exit_price", default=""),
            "失败/退出归因": val(position, "failure_type", "exit_reason_code", "exit_reason", default=""),
        })
    missing = [label for label, value in checks.items() if value in (None, "", [])]
    total = len(checks)
    completeness = round((total - len(missing)) / total * 100.0, 4) if total else 0.0
    if completeness >= 85 and not missing:
        level = "E3_可复盘"
    elif completeness >= 60:
        level = "E2_部分可复盘"
    else:
        level = "E1_记录型样本"
    suggestions = []
    if missing:
        suggestions.append("补齐 paper entry snapshot 硬字段：发现/信号/钱包/入场市值、流动性、holder、quote/security 与延迟。")
        suggestions.append("补齐钱包结构、主导侧生命周期、持仓 journal、退出证据和 failure attribution 后再作为策略样本。")
    else:
        suggestions.append("核心复盘字段已齐备，可进入策略分桶统计；仍需检查样本独立性与 shadow hold。")
    return {
        "case_quality_level": level,
        "completeness_pct": completeness,
        "case_completeness_score": completeness,
        "missing_core_fields": missing,
        "evidence_missing_fields": missing,
        "strategy_review_eligible": level == "E3_可复盘",
        "next_action": "进入策略分桶统计" if level == "E3_可复盘" else "补齐缺失证据后再进入核心策略统计",
        "repair_suggestions": suggestions,
        "scope_note": "E1 只能作为记录型样本；E2 部分复盘；E3 才可进入高质量策略复盘。",
    }


def _paper_entry_snapshot(position: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "candidate_discovered_at": val(position, "candidate_discovered_at", default=""),
        "discovery_market_cap_usd": val(position, "discovery_market_cap_usd", default=""),
        "signal_time": val(position, "signal_time", default=""),
        "signal_level": val(position, "signal_level", default=""),
        "signal_market_cap_usd": val(position, "signal_market_cap_usd", default=""),
        "wallet_decision_time": val(position, "wallet_decision_time", default=""),
        "wallet_structure_status": val(position, "entry_wallet_structure_status", "wallet_structure_status", default=""),
        "wallet_structure_score": val(position, "entry_wallet_structure_score", "wallet_structure_score", default=""),
        "wallet_risk_score": val(position, "entry_wallet_risk_score", "wallet_risk_score", default=""),
        "counterparty_pressure_score": val(position, "entry_counterparty_pressure_score", "counterparty_pressure_score", default=""),
        "data_quality_score": val(position, "entry_data_quality_score", "data_quality_score", default=""),
        "quote_security_state": val(position, "quote_security_state", "quote_gate", default=""),
        "entry_quote_source": val(position, "entry_quote_source", "quote_source", default=""),
        "entry_raw_quote_price": val(position, "entry_raw_quote_price", "live_entry_price", default=""),
        "entry_simulated_price": val(position, "entry_simulated_price", "paper_entry_price", "entry_price", default=""),
        "paper_entry_time": val(position, "paper_entry_time", "entry_time", default=""),
        "paper_size_sol": val(position, "paper_size_sol", "position_sol", default=""),
        "paper_size_usd": val(position, "paper_size_usd", default=""),
        "estimated_token_amount": val(position, "estimated_token_amount", default=""),
        "entry_market_cap_usd": val(position, "entry_market_cap_usd", "paper_entry_market_cap_usd", default=""),
        "entry_liquidity_usd": val(position, "entry_liquidity_usd", default=""),
        "entry_holder_count": val(position, "entry_holder_count", default=""),
        "entry_delay_from_discovery_sec": val(position, "entry_delay_from_discovery_sec", default=""),
        "entry_delay_from_signal_sec": val(position, "entry_delay_from_signal_sec", default=""),
        "entry_market_cap_change_from_discovery_pct": val(position, "entry_market_cap_change_from_discovery_pct", default=""),
        "entry_market_cap_change_from_signal_pct": val(position, "entry_market_cap_change_from_signal_pct", default=""),
    }


def build_case_file_payload(position: Mapping[str, Any], *, holding_journal: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    journal = holding_journal or []
    position_id = val(position, "position_id", default=f"paper-{val(position,'token_address','代币地址', default='unknown')}")
    token_address = val(position, "token_address", "代币地址", default="")
    token_symbol = val(position, "token_symbol", "代币符号", default=token_address[:8] or "UNKNOWN")
    pnl = val(position, "net_pnl_pct", "最终收益率_pct", "live_pnl_pct", default="")
    operator_psychology = _operator_psychology_section(position)

    explanations = {
        "discovery_explanation": _discovery_explanation(position),
        "pattern_explanation": _pattern_explanation(position),
        "signal_explanation": _signal_explanation(position),
        "wallet_explanation": _wallet_explanation(position),
        "quote_security_explanation": _quote_security_explanation(position),
        "entry_explanation": _entry_explanation(position),
        "holding_explanation": _holding_explanation(journal),
        "exit_explanation": _exit_explanation(position),
        "post_trade_review": _post_trade_review(position),
        "strategy_adjustment_suggestion": val(position, "strategy_adjustment_suggestion", default=_strategy_adjustment(position)),
        "open_questions": val(position, "open_questions", default="退出是否过早、钱包结构是否过敏、入场市值分桶是否需要调整，均需继续用 paper 样本验证。"),
    }

    payload: Dict[str, Any] = {
        "case_quality": _case_quality(position, journal),
        "basic": {
            "position_id": position_id,
            "token_symbol": token_symbol,
            "token_address": token_address,
            "status": val(position, "status", default="OPEN"),
            "strategy_name": val(position, "strategy_name", "strategy_type", default="SIKK-B 控盘箱体突破回踩"),
            "signal_level": val(position, "signal_level", default=""),
            "boundary": BOUNDARY_NOTE,
        },
        "discovery": {
            "candidate_discovered_at": val(position, "candidate_discovered_at", default=""),
            "discovery_source": val(position, "discovery_source", default="gmgn_new_token_filter"),
            "discovery_price": val(position, "discovery_price", default=""),
            "discovery_market_cap_usd": val(position, "discovery_market_cap_usd", default=""),
            "discovery_liquidity_usd": val(position, "discovery_liquidity_usd", default=""),
            "discovery_holder_count": val(position, "discovery_holder_count", default=""),
            "discovery_volume_5m": val(position, "discovery_volume_5m", default=""),
            "discovery_volume_1h": val(position, "discovery_volume_1h", default=""),
            "discovery_age_minutes": val(position, "discovery_age_minutes", default=""),
            "discovery_reason": val(position, "discovery_reason", default=""),
            "discovery_explanation": explanations["discovery_explanation"],
        },
        "pattern": {
            "pattern_type": val(position, "pattern_type", "strategy_type", default=""),
            "lifecycle_phase": val(position, "lifecycle_phase", default=""),
            "control_box_high": val(position, "control_box_high", default=""),
            "control_box_low": val(position, "control_box_low", default=""),
            "control_box_mid": val(position, "control_box_mid", default=""),
            "poc_price": val(position, "poc_price", default=""),
            "avwap_price": val(position, "avwap_price", default=""),
            "ema20": val(position, "ema20", default=""),
            "ema50": val(position, "ema50", default=""),
            "volume_state": val(position, "volume_state", default=""),
            "volatility_state": val(position, "volatility_state", default=""),
            "price_structure_status": val(position, "price_structure_status", default=""),
            "pattern_explanation": explanations["pattern_explanation"],
        },
        "signal": {
            "signal_time": val(position, "signal_time", default=""),
            "signal_level": val(position, "signal_level", default=""),
            "signal_type": val(position, "signal_type", "strategy_type", default=""),
            "signal_gate": val(position, "signal_gate", default=""),
            "signal_price": val(position, "signal_price", "signal_entry_price", default=""),
            "signal_market_cap_usd": val(position, "signal_market_cap_usd", default=""),
            "signal_liquidity_usd": val(position, "signal_liquidity_usd", default=""),
            "signal_kline_interval": val(position, "signal_kline_interval", default=""),
            "signal_reason": val(position, "signal_reason", default=""),
            "invalid_level": val(position, "invalid_level", default=""),
            "confirmation_conditions": val(position, "confirmation_conditions", default=""),
            "signal_explanation": explanations["signal_explanation"],
        },
        "wallet_entry": {
            "wallet_decision_time": val(position, "wallet_decision_time", default=""),
            "wallet_structure_status": val(position, "entry_wallet_structure_status", "wallet_structure_status", default=""),
            "wallet_structure_score": val(position, "entry_wallet_structure_score", "wallet_structure_score", default=""),
            "wallet_risk_score": val(position, "entry_wallet_risk_score", "wallet_risk_score", default=""),
            "counterparty_pressure_score": val(position, "entry_counterparty_pressure_score", "counterparty_pressure_score", default=""),
            "data_quality_score": val(position, "entry_data_quality_score", "data_quality_score", default=""),
            "early_wallet_remaining_pct": val(position, "entry_early_wallet_remaining_pct", "early_wallet_remaining_pct", default=""),
            "early_wallet_sold_pct": val(position, "entry_early_wallet_sold_pct", "early_wallet_sold_pct", default=""),
            "same_source_sync_sell_score": val(position, "entry_same_source_sync_sell_score", "same_source_sync_sell_score", default=""),
            "high_result_wallet_remaining_pct": val(position, "entry_high_result_wallet_remaining_pct", default=""),
            "wallet_support_signals": val(position, "entry_wallet_support_signals", "wallet_support_signals", default=""),
            "wallet_risk_signals": val(position, "entry_wallet_risk_signals", "wallet_risk_signals", default=""),
            "wallet_reason": val(position, "entry_wallet_reason", "wallet_structure_reason", default=""),
            "wallet_explanation": explanations["wallet_explanation"],
        },
        "quote_security": {
            "quote_check_time": val(position, "quote_check_time", default=""),
            "quote_gate": val(position, "quote_gate", "quote_security_state", default=""),
            "quote_source": val(position, "quote_source", "entry_quote_source", default=""),
            "quote_price": val(position, "quote_price", default=""),
            "gmgn_price": val(position, "gmgn_price", default=""),
            "okx_price": val(position, "okx_price", default=""),
            "kline_close_price": val(position, "kline_close_price", default=""),
            "price_deviation_pct": val(position, "price_deviation_pct", default=""),
            "quote_reason": val(position, "quote_reason", default=""),
            "security_gate": val(position, "security_gate", default=""),
            "security_risk_level": val(position, "security_risk_level", default=""),
            "security_flags": val(position, "security_flags", default=""),
            "security_reason": val(position, "security_reason", default=""),
            "quote_security_explanation": explanations["quote_security_explanation"],
        },
        "entry": {
            "paper_entry_time": val(position, "paper_entry_time", "entry_time", default=""),
            "entry_decision_time": val(position, "entry_decision_time", default=""),
            "entry_price_mode": val(position, "entry_price_mode", default=""),
            "entry_quote_source": val(position, "entry_quote_source", default=""),
            "entry_raw_quote_price": val(position, "entry_raw_quote_price", "live_entry_price", default=""),
            "entry_simulated_price": val(position, "entry_simulated_price", "paper_entry_price", "entry_price", default=""),
            "entry_slippage_pct": val(position, "entry_slippage_pct", default=""),
            "entry_fee_sol": val(position, "entry_fee_sol", default=""),
            "entry_market_cap_usd": val(position, "entry_market_cap_usd", "paper_entry_market_cap_usd", default=""),
            "entry_liquidity_usd": val(position, "entry_liquidity_usd", default=""),
            "entry_holder_count": val(position, "entry_holder_count", default=""),
            "paper_size_sol": val(position, "paper_size_sol", "position_sol", default=""),
            "paper_size_usd": val(position, "paper_size_usd", default=""),
            "estimated_token_amount": val(position, "estimated_token_amount", default=""),
            "entry_position_type": val(position, "entry_position_type", default="paper"),
            "entry_reason_summary": val(position, "entry_reason_summary", default=""),
            "entry_evidence_chain": val(position, "entry_evidence_chain", default=""),
            "entry_invalid_conditions": val(position, "entry_invalid_conditions", "invalid_conditions", default=""),
            "entry_market_cap_change_from_discovery_pct": val(position, "entry_market_cap_change_from_discovery_pct", default=""),
            "entry_market_cap_change_from_signal_pct": val(position, "entry_market_cap_change_from_signal_pct", default=""),
            "market_cap_context_status": val(position, "market_cap_context_status", default="UNKNOWN_ENTRY"),
            "paper_entry_snapshot": _paper_entry_snapshot(position),
            "entry_explanation": explanations["entry_explanation"],
        },
        "holding_journal": journal,
        "operator_psychology": operator_psychology,
        "exit": {
            "exit_time": val(position, "exit_time", default=""),
            "exit_price": val(position, "exit_price", default=""),
            "exit_market_cap_usd": val(position, "exit_market_cap_usd", default=""),
            "exit_liquidity_usd": val(position, "exit_liquidity_usd", default=""),
            "exit_trigger": val(position, "exit_trigger", default=""),
            "exit_reason_code": val(position, "exit_reason_code", "failure_type", default=""),
            "exit_reason": val(position, "exit_reason", "failure_reason", default=""),
            "exit_wallet_structure_status": val(position, "exit_wallet_structure_status", default=""),
            "exit_wallet_structure_score": val(position, "exit_wallet_structure_score", default=""),
            "exit_wallet_risk_score": val(position, "exit_wallet_risk_score", default=""),
            "exit_counterparty_pressure_score": val(position, "exit_counterparty_pressure_score", default=""),
            "net_pnl_pct": pnl,
            "net_pnl_sol": val(position, "net_pnl_sol", default=""),
            "trade_result_type": val(position, "trade_result_type", default=_result_type(pnl)),
            "failure_type": _failure_type(position),
            "wallet_exit_action": val(position, "wallet_exit_action", "wallet_position_action", default=""),
            "wallet_exit_confidence": val(position, "wallet_exit_confidence", default=""),
            "wallet_exit_evidence": val(position, "wallet_exit_evidence", default=""),
            "false_exit_flag": val(position, "false_exit_flag", default=""),
            "avoided_drawdown_pct": val(position, "avoided_drawdown_pct", default=""),
            "missed_profit_pct": val(position, "missed_profit_pct", default=""),
            "exit_explanation": explanations["exit_explanation"],
        },
        "review": {
            "trade_result_type": val(position, "trade_result_type", default=_result_type(pnl)),
            "failure_type": _failure_type(position),
            "holding_explanation": explanations["holding_explanation"],
            "post_trade_review": explanations["post_trade_review"],
        },
        "adjustment": {
            "strategy_adjustment_suggestion": explanations["strategy_adjustment_suggestion"],
            "open_questions": explanations["open_questions"],
        },
        "field_sources": val(position, "case_field_sources", default={}),
        "evidence_missing_fields": val(position, "case_missing_fields", default=[]),
        "source_boundary": val(position, "case_field_source_boundary", default=BOUNDARY_NOTE),
    }
    return payload


def _md_table(rows: Iterable[tuple[str, Any]]) -> str:
    out = ["| 字段 | 数值 |", "|---|---|"]
    for k, v in rows:
        out.append(f"| {k} | {v if v not in {None, ''} else '待补'} |")
    return "\n".join(out)


def render_case_markdown(payload: Mapping[str, Any]) -> str:
    b = payload["basic"]; d = payload["discovery"]; p = payload["pattern"]; s = payload["signal"]
    w = payload["wallet_entry"]; q = payload["quote_security"]; e = payload["entry"]; x = payload["exit"]
    cq = payload.get("case_quality", {})
    op = payload.get("operator_psychology", {})
    r = payload["review"]; a = payload["adjustment"]
    field_sources = payload.get("field_sources") or {}
    evidence_missing_fields = payload.get("evidence_missing_fields") or []
    source_rows = []
    for key, source in sorted(field_sources.items())[:80]:
        source_rows.append(f"| {key} | {source} |")
    if not source_rows:
        source_rows.append("| 待补 | 暂无字段来源映射 |")
    journal = payload.get("holding_journal") or []
    journal_rows = []
    for item in journal[-20:]:
        journal_rows.append(f"| {val(item,'time',default='待补')} | {val(item,'current_price',default='待补')} | {val(item,'current_market_cap_usd',default='待补')} | {val(item,'unrealized_pnl_pct',default='待补')} | {val(item,'wallet_structure_status',default='待补')} | {val(item,'paper_action',default='待补')} | {val(item,'monitor_reason',default='待补')} |")
    if not journal_rows:
        journal_rows.append("| 待补 | 待补 | 待补 | 待补 | 待补 | 待补 | 暂无 journal |")
    return f"""# Paper Case File: ${b.get('token_symbol')}

> {BOUNDARY_NOTE}

## 1. 基础信息

{_md_table([
('Position ID', b.get('position_id')), ('Token', b.get('token_symbol')), ('Address', b.get('token_address')), ('状态', b.get('status')), ('策略', b.get('strategy_name')), ('信号等级', b.get('signal_level')), ('入场时间', e.get('paper_entry_time')), ('退出时间', x.get('exit_time')), ('纸面仓位', str(e.get('paper_size_sol')) + ' SOL'), ('入场市值', e.get('entry_market_cap_usd')), ('退出市值', x.get('exit_market_cap_usd')), ('净收益', x.get('net_pnl_pct')),
])}

---

## 1.5 Case File 质量

{_md_table([
('质量等级', cq.get('case_quality_level')), ('完整度', str(cq.get('completeness_pct', '待补')) + '%'), ('缺失核心字段', '、'.join(cq.get('missing_core_fields') or []) or '无'), ('质量说明', cq.get('scope_note')),
])}

- 修复建议：{'；'.join(cq.get('repair_suggestions') or []) or '暂无'}

---

## 2. 候选发现

{d.get('discovery_explanation')}

---

## 3. 盘型判断

- pattern_type：{p.get('pattern_type') or '待补'}
- lifecycle_phase：{p.get('lifecycle_phase') or '待补'}
- control_box_low：{p.get('control_box_low') or '待补'}
- control_box_high：{p.get('control_box_high') or '待补'}
- AVWAP：{p.get('avwap_price') or '待补'}
- POC：{p.get('poc_price') or '待补'}

{p.get('pattern_explanation')}

---

## 4. 入场信号

{s.get('signal_explanation')}

---

## 5. 钱包结构门禁

{_md_table([
('wallet_structure_status', w.get('wallet_structure_status')), ('wallet_structure_score', w.get('wallet_structure_score')), ('wallet_risk_score', w.get('wallet_risk_score')), ('counterparty_pressure_score', w.get('counterparty_pressure_score')), ('data_quality_score', w.get('data_quality_score')),
])}

{w.get('wallet_explanation')}

---

## 6. Quote / Security

{q.get('quote_security_explanation')}

---

## 7. 纸面入场

{_md_table([
('入场市值', e.get('entry_market_cap_usd')), ('发现时市值', d.get('discovery_market_cap_usd')), ('信号时市值', s.get('signal_market_cap_usd')), ('从发现到入场市值变化', str(e.get('entry_market_cap_change_from_discovery_pct')) + '%'), ('从信号到入场市值变化', str(e.get('entry_market_cap_change_from_signal_pct')) + '%'), ('入场上下文', e.get('market_cap_context_status')), ('买入规模', str(e.get('paper_size_sol')) + ' SOL'), ('估算 token 数量', e.get('estimated_token_amount')),
])}

{e.get('entry_explanation')}

---

## 8. 主导侧心理与生命周期

{_md_table([
('主导侧生命周期', op.get('operator_lifecycle_stage')), ('主导侧心理', op.get('operator_psychology_label')), ('行为动机', op.get('dominant_side_intent')), ('对手盘心理', op.get('counterparty_psychology')), ('流动性意图', op.get('liquidity_intent')), ('陷阱风险', op.get('trap_risk_type')), ('结构防守', op.get('structure_defense_status')), ('筹码控制权', op.get('chip_control_state')), ('纸面入场匹配度', op.get('paper_trade_alignment')), ('证据等级', op.get('psychology_evidence_level')),
])}

{op.get('psychology_explanation') or '主导侧心理解释：证据不足，待复查。'}

- 下一步观察：{op.get('next_observation_focus') or '待补'}
- 失效条件：{'；'.join(op.get('invalidation_conditions') or []) if isinstance(op.get('invalidation_conditions'), list) else (op.get('invalidation_conditions') or '待补')}

---

## 9. 持仓过程

{r.get('holding_explanation')}

| 时间 | 价格 | 市值 | 浮盈 | 钱包状态 | 动作 | 原因 |
|---|---:|---:|---:|---|---|---|
{chr(10).join(journal_rows)}

---

## 10. 退出

{x.get('exit_explanation')}

---

## 11. 策略复盘

本次交易结果：{r.get('trade_result_type')}  
失败归因：{r.get('failure_type') or '无 / 不适用'}

{r.get('post_trade_review')}

---

## 12. 策略调整建议

{a.get('strategy_adjustment_suggestion')}

---

## 13. 需要继续观察的问题

{a.get('open_questions')}

---

## 14. 字段来源追踪

| 字段 | 来源文件 |
|---|---|
{chr(10).join(source_rows)}

---

## 15. 仍然缺失的字段清单

- Case 缺失字段：{'、'.join(evidence_missing_fields) if evidence_missing_fields else '无'}
- 质量层缺失字段：{'、'.join(cq.get('evidence_missing_fields') or cq.get('missing_core_fields') or []) or '无'}
- 下一步动作：{cq.get('next_action') or '待补'}
- 是否进入核心策略统计：{'是' if cq.get('strategy_review_eligible') else '否'}
"""


def _position_rows(paper_dir: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    open_payload = read_json(paper_dir / "paper_positions_open.json", {"open_positions": []})
    closed_payload = read_json(paper_dir / "paper_positions_closed.json", {"closed_positions": []})
    if isinstance(open_payload, Mapping):
        rows.extend([dict(r) for r in open_payload.get("open_positions", []) if isinstance(r, Mapping)])
    if isinstance(closed_payload, Mapping):
        rows.extend([dict(r) for r in closed_payload.get("closed_positions", []) if isinstance(r, Mapping)])
    return rows


def build_case_files(*, paper_dir: str | Path, base_dir: str | Path, output_dir: str | Path) -> Dict[str, Any]:
    paper = Path(paper_dir)
    base = Path(base_dir)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    manifest: List[Dict[str, Any]] = []
    for position in _position_rows(paper):
        enriched_position = enrich_position_for_case_file(position, base)
        position_id = val(enriched_position, "position_id", default=f"paper-{val(enriched_position,'token_address','代币地址', default='unknown')}")
        journal = read_jsonl(paper / "position_journal" / f"{position_id}.jsonl")
        payload = build_case_file_payload(enriched_position, holding_journal=journal)
        filename = slug(position_id)
        json_path = out / f"{filename}.json"
        md_path = out / f"{filename}.md"
        write_json(json_path, payload)
        md_path.write_text(render_case_markdown(payload), encoding="utf-8")
        manifest.append({
            "position_id": position_id,
            "token_address": payload["basic"].get("token_address"),
            "token_symbol": payload["basic"].get("token_symbol"),
            "case_file_json": str(json_path),
            "case_file_md": str(md_path),
            "status": payload["basic"].get("status"),
            "case_quality_level": payload.get("case_quality", {}).get("case_quality_level"),
            "case_completeness_score": payload.get("case_quality", {}).get("case_completeness_score"),
            "evidence_missing_fields": payload.get("case_quality", {}).get("evidence_missing_fields"),
        })
    manifest_path = out / "case_files_manifest.json"
    write_json(manifest_path, {"case_files": manifest, "boundary": BOUNDARY_NOTE})
    return {
        "case_files_manifest": str(manifest_path),
        "case_json_count": len(manifest),
        "case_md_count": len(manifest),
        "output_dir": str(out),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成 SIKK Paper Position Case File")
    parser.add_argument("--paper-dir", default="data/gmgn_candidates_live_run/paper_live")
    parser.add_argument("--base-dir", default="data/gmgn_candidates_live_run")
    parser.add_argument("--output-dir", default="data/gmgn_candidates_live_run/paper_live/case_files")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = build_case_files(paper_dir=args.paper_dir, base_dir=args.base_dir, output_dir=args.output_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
