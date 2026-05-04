#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK Case File 字段来源映射与只读回填。

把分散在 state/token_status/index/wallet/quote/security/paper 的字段按优先级合并到
paper position，用于生成更完整的 Case File。只读文件，不执行真实 swap、不签名、不广播。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Tuple

BOUNDARY_NOTE = "只读字段回填；不执行真实 swap，不读取私钥，不签名，不广播。"


def read_json(path: str | Path) -> Any:
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def first_value(row: Mapping[str, Any], *keys: str) -> Any:
    for key in keys:
        value = row.get(key)
        if value not in (None, "", []):
            return value
    return ""


def token_address_of(row: Mapping[str, Any]) -> str:
    return str(first_value(row, "token_address", "代币地址", "token", "address", "mint"))


def position_id_of(row: Mapping[str, Any]) -> str:
    return str(first_value(row, "position_id", "仓位编号", "id"))


def rows_from_payload(payload: Any, keys: Iterable[str]) -> list[Dict[str, Any]]:
    if isinstance(payload, list):
        return [dict(r) for r in payload if isinstance(r, Mapping)]
    if not isinstance(payload, Mapping):
        return []
    for key in keys:
        rows = payload.get(key)
        if isinstance(rows, list):
            return [dict(r) for r in rows if isinstance(r, Mapping)]
    return []


def index_rows(rows: Iterable[Mapping[str, Any]]) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        token = token_address_of(row)
        pid = position_id_of(row)
        if token:
            out.setdefault(token, {}).update(dict(row))
        if pid:
            out.setdefault(pid, {}).update(dict(row))
    return out


FIELD_SOURCE_MAP: Dict[str, Tuple[str, ...]] = {
    # 基础字段
    "position_id": ("position_id", "仓位编号"),
    "token_symbol": ("token_symbol", "代币符号", "symbol"),
    "token_address": ("token_address", "代币地址", "token", "address", "mint"),
    "status": ("status", "状态"),
    # 发现阶段
    "candidate_discovered_at": ("candidate_discovered_at", "发现时间", "created_at", "open_time"),
    "discovery_source": ("discovery_source", "来源分类", "source"),
    "discovery_price": ("discovery_price", "发现价格", "price", "current_price"),
    "discovery_market_cap_usd": ("discovery_market_cap_usd", "发现市值USD", "当前市值USD", "market_cap", "market_cap_usd", "mc", "fdv"),
    "discovery_liquidity_usd": ("discovery_liquidity_usd", "发现流动性USD", "流动性USD", "liquidity", "liquidity_usd"),
    "discovery_holder_count": ("discovery_holder_count", "发现持有人数", "holder_count", "holders"),
    # 信号阶段
    "signal_time": ("signal_time", "信号时间", "generated_at"),
    "signal_level": ("signal_level", "信号等级"),
    "signal_type": ("signal_type", "strategy_type", "信号类型"),
    "signal_price": ("signal_price", "signal_entry_price", "信号价格"),
    "signal_market_cap_usd": ("signal_market_cap_usd", "信号市值USD"),
    "signal_reason": ("signal_reason", "信号原因", "状态原因"),
    # 钱包结构
    "wallet_decision_time": ("wallet_decision_time", "钱包决策时间", "generated_at", "snapshot_time"),
    "wallet_structure_status": ("wallet_structure_status", "钱包结构结论"),
    "wallet_structure_score": ("wallet_structure_score", "钱包结构评分"),
    "wallet_risk_score": ("wallet_risk_score", "钱包风险评分"),
    "counterparty_pressure_score": ("counterparty_pressure_score", "对手盘压力评分"),
    "data_quality_score": ("data_quality_score", "数据质量评分"),
    "early_wallet_remaining_pct": ("early_wallet_remaining_pct", "早期钱包剩余_pct"),
    "early_wallet_sold_pct": ("early_wallet_sold_pct", "早期钱包卖出_pct"),
    "same_source_sync_sell_score": ("same_source_sync_sell_score", "同源同步卖出评分"),
    "wallet_support_signals": ("wallet_support_signals", "钱包支持信号"),
    "wallet_risk_signals": ("wallet_risk_signals", "钱包风险信号"),
    "wallet_structure_reason": ("wallet_structure_reason", "钱包结构原因", "状态原因"),
    # quote/security
    "quote_check_time": ("quote_check_time", "报价检查时间", "generated_at"),
    "quote_gate": ("quote_gate", "quote_security_state", "最终权限", "quote_security_permission"),
    "quote_source": ("quote_source", "entry_quote_source", "报价来源"),
    "quote_price": ("quote_price", "报价价格"),
    "gmgn_price": ("gmgn_price", "GMGN价格"),
    "okx_price": ("okx_price", "OKX价格"),
    "kline_close_price": ("kline_close_price", "K线收盘价"),
    "price_deviation_pct": ("price_deviation_pct", "价格偏差_pct"),
    "security_gate": ("security_gate", "交易前状态", "security_permission"),
    "security_risk_level": ("security_risk_level", "安全风险等级", "risk_level"),
    "security_flags": ("security_flags", "安全标记"),
    # 入场/当前/退出
    "paper_entry_time": ("paper_entry_time", "entry_time", "入场时间"),
    "entry_price": ("entry_price", "paper_entry_price", "入场价格"),
    "entry_market_cap_usd": ("entry_market_cap_usd", "paper_entry_market_cap_usd", "入场市值USD"),
    "paper_size_sol": ("paper_size_sol", "position_sol", "模拟仓位SOL"),
    "paper_size_usd": ("paper_size_usd", "模拟仓位USD"),
    "estimated_token_amount": ("estimated_token_amount", "估算Token数量"),
    "current_price": ("current_price", "last_price", "当前价格"),
    "current_market_cap_usd": ("current_market_cap_usd", "当前市值USD"),
    "unrealized_pnl_pct": ("unrealized_pnl_pct", "当前收益率_pct", "纸面浮盈_pct"),
    "max_floating_profit_pct": ("max_floating_profit_pct", "最大浮盈_pct"),
    "max_drawdown_pct": ("max_drawdown_pct", "最大浮亏_pct"),
    "exit_time": ("exit_time", "退出时间"),
    "exit_price": ("exit_price", "退出价格"),
    "exit_market_cap_usd": ("exit_market_cap_usd", "退出市值USD"),
    "net_pnl_pct": ("net_pnl_pct", "最终收益率_pct"),
    "exit_reason": ("exit_reason", "failure_reason", "退出原因"),
    "failure_type": ("failure_type", "exit_reason_code", "失败归因"),
}


def load_context_rows(base_dir: str | Path) -> Dict[str, Dict[str, Any]]:
    base = Path(base_dir)
    sources: Dict[str, Dict[str, Any]] = {}

    source_specs = [
        ("state_machine/candidate_states.json", ("候选状态", "candidates", "tokens")),
        ("gmgn_new_token_filter/token_candidates.json", ("候选列表", "candidates", "tokens")),
        ("candidate_signal_outputs/candidate_signal_summary.json", ("信号结果", "处理结果", "results")),
        ("wallet_structure/candidate_wallet_structure_summary.json", ("处理结果", "wallet_structure_results", "results")),
        ("quote_security/candidate_quote_security_summary.json", ("处理结果", "quote_security_results", "results")),
        ("index/position_index.json", ("positions", "open_positions", "closed_positions", "仓位列表")),
        ("index/token_detail_index.json", ("tokens", "token_details", "候选详情")),
        ("live_state.json", ("tokens", "候选状态")),
    ]
    for rel, keys in source_specs:
        path = base / rel
        for row in rows_from_payload(read_json(path), keys):
            token = token_address_of(row)
            pid = position_id_of(row)
            source_row = {**row, "_sikk_source_file": str(path)}
            for key in (token, pid):
                if not key:
                    continue
                bucket = sources.setdefault(key, {})
                field_map = bucket.setdefault("_sikk_field_source_map", {})
                for field, value in source_row.items():
                    if field.startswith("_sikk_"):
                        continue
                    bucket[field] = value
                    if value not in (None, "", []):
                        field_map[field] = str(path)
                bucket["_sikk_source_file"] = str(path)

    for path in sorted((base / "tokens").glob("*/token_status.json")):
        row = read_json(path)
        if isinstance(row, Mapping):
            token = token_address_of(row) or path.parent.name
            bucket = sources.setdefault(token, {})
            field_map = bucket.setdefault("_sikk_field_source_map", {})
            for field, value in dict(row).items():
                bucket[field] = value
                if value not in (None, "", []):
                    field_map[field] = str(path)
            bucket["_sikk_source_file"] = str(path)
    for path in sorted((base / "wallet_structure").glob("*/wallet_structure_decision.json")):
        row = read_json(path)
        if isinstance(row, Mapping):
            token = token_address_of(row) or path.parent.name
            bucket = sources.setdefault(token, {})
            field_map = bucket.setdefault("_sikk_field_source_map", {})
            for field, value in dict(row).items():
                bucket[field] = value
                if value not in (None, "", []):
                    field_map[field] = str(path)
            bucket["_sikk_source_file"] = str(path)
    return sources


def enrich_position_for_case_file(position: Mapping[str, Any], base_dir: str | Path) -> Dict[str, Any]:
    """按字段来源映射补齐 position，并附加字段来源/缺失清单。"""
    base = Path(base_dir)
    context = load_context_rows(base)
    token = token_address_of(position)
    pid = position_id_of(position)
    candidate_sources = []
    if token and token in context:
        candidate_sources.append(context[token])
    if pid and pid in context:
        candidate_sources.append(context[pid])
    candidate_sources.append(dict(position))  # position 自身最高优先级，最后覆盖

    merged: Dict[str, Any] = {}
    field_sources: Dict[str, str] = {}
    missing: list[str] = []
    # 先放入原始字段，避免丢字段
    for source in candidate_sources:
        merged.update({k: v for k, v in source.items() if not k.startswith("_sikk_")})
    for target, aliases in FIELD_SOURCE_MAP.items():
        value = ""
        source_file = ""
        for source in candidate_sources:
            value = first_value(source, *aliases)
            if value not in (None, "", []):
                field_map = source.get("_sikk_field_source_map") if isinstance(source.get("_sikk_field_source_map"), Mapping) else {}
                source_file = ""
                for alias in aliases:
                    if source.get(alias) not in (None, "", []):
                        source_file = str(field_map.get(alias) or source.get("_sikk_source_file") or "paper_position_json")
                        break
                break
        # position 自身优先级修正
        own = first_value(position, *aliases)
        if own not in (None, "", []):
            value = own
            source_file = "paper_position_json"
        if value not in (None, "", []):
            merged[target] = value
            field_sources[target] = source_file or "derived_context"
        else:
            missing.append(target)
    merged["case_field_sources"] = field_sources
    merged["case_missing_fields"] = missing
    merged["case_field_source_boundary"] = BOUNDARY_NOTE
    return merged


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="SIKK Case File 字段来源映射检查")
    parser.add_argument("--base-dir", default="data/gmgn_candidates_live_run")
    parser.add_argument("--position-json", required=True)
    args = parser.parse_args()
    payload = read_json(args.position_json)
    if isinstance(payload, Mapping):
        print(json.dumps(enrich_position_for_case_file(payload, args.base_dir), ensure_ascii=False, indent=2))
