#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK wallet-structure → trading-system adapter.

本模块只读取已有钱包结构系统输出并转换为交易状态机 / paper runner 可消费的
标准字段；不调用钱包采集过程，不签名，不广播，不执行真实 swap。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Mapping

VALID_WALLET_MODES = {"off", "observe", "soft", "hard"}


def _read_json(path: str | Path | None) -> Dict[str, Any]:
    if not path:
        return {}
    p = Path(path)
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _as_bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if value is None or value == "":
        return default
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "stale", "过期"}
    return bool(value)


def _pick(mapping: Mapping[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        value = mapping.get(key)
        if value is not None and value != "":
            return value
    return default


def missing_wallet_decision(token_address: str = "", reason: str = "wallet_structure_decision_missing") -> Dict[str, Any]:
    return {
        "token_address": token_address,
        "wallet_structure_status": "WALLET_UNKNOWN",
        "decision_action": "NO_DECISION",
        "wallet_structure_score": 0,
        "wallet_risk_score": 0,
        "counterparty_pressure_score": 0,
        "data_quality_score": 0,
        "wallet_structure_factor": 1.0,
        "reason": reason,
        "is_stale": True,
    }


def normalize_wallet_decision(raw: Mapping[str, Any] | None, token_address: str = "") -> Dict[str, Any]:
    """Normalize Chinese-first wallet summary rows or decision JSON into stable keys."""

    if not raw:
        return missing_wallet_decision(token_address)
    reason = str(_pick(raw, "reason", "钱包结构原因", "状态调整原因", "wallet_structure_reason", default="") or "")
    status = str(_pick(raw, "wallet_structure_status", "钱包结构结论", default="WALLET_UNKNOWN") or "WALLET_UNKNOWN")
    factor = _as_float(_pick(raw, "wallet_structure_factor", "钱包结构系数", default=1.0), 1.0)
    if factor <= 0 and status != "WALLET_BLOCK":
        factor = 1.0
    decision = dict(raw)
    decision.update({
        "token_address": str(_pick(raw, "token_address", "代币地址", "token", "address", default=token_address) or token_address),
        "token_symbol": str(_pick(raw, "token_symbol", "代币符号", "symbol", default="") or ""),
        "wallet_structure_status": status,
        "decision_action": str(_pick(raw, "decision_action", "建议动作", "建议状态调整", default="") or ""),
        "wallet_structure_score": _as_float(_pick(raw, "wallet_structure_score", "钱包结构评分", default=0), 0.0),
        "wallet_risk_score": _as_float(_pick(raw, "wallet_risk_score", "钱包风险评分", default=0), 0.0),
        "counterparty_pressure_score": _as_float(_pick(raw, "counterparty_pressure_score", "对手盘压力评分", default=0), 0.0),
        "data_quality_score": _as_float(_pick(raw, "data_quality_score", "数据质量评分", default=0), 0.0),
        "wallet_structure_factor": factor,
        "wallet_evidence_level": str(_pick(raw, "wallet_evidence_level", "钱包证据等级", default="") or ""),
        "dominant_side_status": str(_pick(raw, "dominant_side_status", "主导侧状态", default="") or ""),
        "chip_transfer_status": str(_pick(raw, "chip_transfer_status", "筹码迁移状态", default="") or ""),
        "reason": reason,
        "decision_age_sec": _as_float(_pick(raw, "decision_age_sec", "wallet_decision_age_sec", default=0), 0.0),
        "is_stale": _as_bool(_pick(raw, "is_stale", "wallet_decision_stale", default=False), False),
    })
    return decision


def load_wallet_decision(token_address: str, wallet_structure_dir: str | Path | None) -> Dict[str, Any]:
    """Read `wallet_structure/<token>/wallet_structure_decision.json` with safe fallback."""

    if not wallet_structure_dir:
        return missing_wallet_decision(token_address)
    path = Path(wallet_structure_dir) / token_address / "wallet_structure_decision.json"
    payload = _read_json(path)
    if not payload:
        return missing_wallet_decision(token_address)
    return normalize_wallet_decision(payload, token_address)


def apply_wallet_gate(token_status: Mapping[str, Any], wallet_decision: Mapping[str, Any] | None, mode: str = "observe") -> Dict[str, Any]:
    """Apply wallet decision to a token status without ever authorizing real execution."""

    mode = (mode or "observe").lower()
    if mode not in VALID_WALLET_MODES:
        mode = "observe"
    decision = normalize_wallet_decision(wallet_decision, str(_pick(token_status, "token_address", "代币地址", default="") or ""))
    out = dict(token_status)
    state = str(_pick(out, "state", "当前状态", default="") or "")
    wallet_status = str(decision.get("wallet_structure_status") or "WALLET_UNKNOWN")
    reason = str(decision.get("reason") or "")
    risk_score = _as_float(decision.get("wallet_risk_score"), 0.0)
    counterparty_score = _as_float(decision.get("counterparty_pressure_score"), 0.0)
    is_stale = _as_bool(decision.get("is_stale"), False)

    out.update({
        "state": state,
        "wallet_structure_mode": mode,
        "wallet_gate": wallet_status,
        "wallet_structure_status": wallet_status,
        "wallet_structure_score": decision.get("wallet_structure_score"),
        "wallet_risk_score": risk_score,
        "counterparty_pressure_score": counterparty_score,
        "data_quality_score": decision.get("data_quality_score"),
        "wallet_structure_factor": decision.get("wallet_structure_factor"),
        "wallet_structure_reason": reason,
        "wallet_decision_stale": is_stale,
        "would_block": wallet_status == "WALLET_BLOCK",
        "would_pause": wallet_status in {"WALLET_PAUSE", "WALLET_UNKNOWN"} or is_stale,
        "wallet_support": wallet_status == "WALLET_SUPPORT",
    })

    if mode == "off":
        out["wallet_gate_effect"] = "OFF"
        return out
    if mode == "observe":
        out["wallet_gate_effect"] = "OBSERVE_ONLY"
        return out
    if mode == "soft":
        if wallet_status == "WALLET_BLOCK" and (risk_score >= 75 or counterparty_score >= 70):
            out["state"] = "BLOCKED"
            out["当前状态"] = "BLOCKED"
            out["block_reason"] = reason or "钱包结构高置信风险阻断"
            out["wallet_gate_effect"] = "SOFT_BLOCK"
        else:
            out["wallet_gate_effect"] = "SOFT_OBSERVE"
        return out

    # hard mode
    if wallet_status == "WALLET_BLOCK":
        out["state"] = "BLOCKED"
        out["当前状态"] = "BLOCKED"
        out["block_reason"] = reason or "钱包结构门禁阻断"
        out["wallet_gate_effect"] = "HARD_BLOCK"
    elif wallet_status in {"WALLET_PAUSE", "WALLET_UNKNOWN"} or is_stale:
        out["state"] = "PAUSE"
        out["当前状态"] = "PAUSE"
        out["pause_reason"] = reason or "钱包结构缺失/过期，hard 模式暂停"
        out["wallet_gate_effect"] = "HARD_PAUSE_UNKNOWN" if wallet_status == "WALLET_UNKNOWN" or is_stale else "HARD_PAUSE"
    elif wallet_status == "WALLET_SUPPORT":
        out["wallet_gate_effect"] = "ALLOW_NEXT_GATES"
    else:
        out["wallet_gate_effect"] = "NO_EFFECT"
    return out


def attach_wallet_factor_to_position(position: Mapping[str, Any], wallet_decision: Mapping[str, Any] | None) -> Dict[str, Any]:
    decision = normalize_wallet_decision(wallet_decision, str(_pick(position, "代币地址", "token_address", default="") or ""))
    out = dict(position)
    out.update({
        "wallet_structure_status": decision.get("wallet_structure_status"),
        "wallet_structure_score": decision.get("wallet_structure_score"),
        "wallet_risk_score": decision.get("wallet_risk_score"),
        "counterparty_pressure_score": decision.get("counterparty_pressure_score"),
        "data_quality_score": decision.get("data_quality_score"),
        "wallet_structure_factor": decision.get("wallet_structure_factor", 1.0),
        "wallet_structure_reason": decision.get("reason", ""),
        "wallet_evidence_level": decision.get("wallet_evidence_level", ""),
        "dominant_side_status": decision.get("dominant_side_status", ""),
        "chip_transfer_status": decision.get("chip_transfer_status", ""),
        "wallet_decision_age_sec": decision.get("decision_age_sec", 0),
        "wallet_decision_stale": decision.get("is_stale", False),
    })
    return out


def evaluate_wallet_change_for_open_position(position: Mapping[str, Any], current_wallet_decision: Mapping[str, Any] | None) -> Dict[str, Any]:
    """Evaluate current wallet decision against entry-time wallet fields for paper actions."""

    decision = normalize_wallet_decision(current_wallet_decision, str(_pick(position, "代币地址", default="") or ""))
    status = str(decision.get("wallet_structure_status") or "")
    dominant = str(decision.get("dominant_side_status") or "")
    chip = str(decision.get("chip_transfer_status") or "")

    def force(reason: str, failure_type: str) -> Dict[str, Any]:
        return {
            "action": "FORCE_PAPER_EXIT",
            "failure_type": failure_type,
            "reason": reason,
            "scope_note": "纸面阶段模拟退出；不执行真实 swap。",
        }

    if status == "WALLET_BLOCK":
        return force("钱包结构状态变为 WALLET_BLOCK", "STRUCTURE_WEAKENING")
    if dominant == "DISTRIBUTION_ACTIVE":
        return force("结构主导侧转为分发活跃", "DISTRIBUTION_ACTIVE")
    if chip == "DISTRIBUTION_TO_COUNTERPARTY":
        return force("筹码向对手盘迁移", "COUNTERPARTY_ABSORBING")

    entry_structure = _as_float(_pick(position, "wallet_structure_score", default=0), 0.0)
    entry_risk = _as_float(_pick(position, "wallet_risk_score", default=0), 0.0)
    entry_counterparty = _as_float(_pick(position, "counterparty_pressure_score", default=0), 0.0)
    cur_structure = _as_float(decision.get("wallet_structure_score"), 0.0)
    cur_risk = _as_float(decision.get("wallet_risk_score"), 0.0)
    cur_counterparty = _as_float(decision.get("counterparty_pressure_score"), 0.0)

    if (entry_structure and entry_structure - cur_structure >= 20) or cur_risk - entry_risk >= 20 or cur_counterparty - entry_counterparty >= 25:
        return {
            "action": "EXIT_MONITOR",
            "failure_type": "STRUCTURE_WEAKENING",
            "reason": "钱包结构评分/风险/对手盘压力相对入场明显恶化",
            "scope_note": "纸面阶段进入退出观察；不执行真实 swap。",
        }
    return {
        "action": "HOLD",
        "failure_type": None,
        "reason": "钱包结构未触发持仓退出条件",
        "scope_note": "继续纸面持仓观察；不执行真实 swap。",
    }
