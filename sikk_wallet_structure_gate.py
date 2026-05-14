#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK-SOL v1.0 钱包结构门禁层。

本模块把早期钱包结构、筹码迁移和对手盘压力压缩成状态机可消费的门禁：
WALLET_BLOCK / WALLET_PAUSE / WALLET_SUPPORT / WALLET_NEUTRAL。

边界：
- 不输出“庄家钱包”结论，只输出证据化角色、game_side 和筹码控制权状态。
- 钱包结构是门禁，不是独立买入信号。
- WALLET_SUPPORT 不能绕过 K线、quote、安全扫描。
- 本模块不执行真实 swap，只服务 paper trading / future confirmation ticket。
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, Iterable, List

from sikk_chip_control_state_machine import evaluate_chip_control_state

WALLET_ROLES = {
    "EARLY_BUYER",
    "EARLY_EXIT",
    "PARTIAL_HOLDER",
    "HIGH_RESULT_WALLET",
    "SAME_SOURCE_GROUP",
    "DISTRIBUTION_SELLER",
    "BAGHOLDER_WHALE",
    "RETAIL_NOISE",
}
GAME_SIDES = {
    "STRUCTURE_SIDE",
    "EXECUTION_SIDE",
    "DISTRIBUTION_SIDE",
    "COUNTERPARTY_SIDE",
    "NOISE_SIDE",
    "UNKNOWN_SIDE",
}

ROLE_ALIASES = {
    "早期买入钱包": "EARLY_BUYER",
    "疑似早期结构钱包": "EARLY_BUYER",
    "早期结构钱包": "EARLY_BUYER",
    "新钱包狙击": "EARLY_BUYER",
    "临时执行钱包": "EARLY_BUYER",
    "早期清仓钱包": "EARLY_EXIT",
    "已清仓早期钱包": "EARLY_EXIT",
    "部分持有钱包": "PARTIAL_HOLDER",
    "结果钱包": "HIGH_RESULT_WALLET",
    "高结果鲸鱼": "HIGH_RESULT_WALLET",
    "同源执行组": "SAME_SOURCE_GROUP",
    "分发派发钱包": "DISTRIBUTION_SELLER",
    "分发卖出钱包": "DISTRIBUTION_SELLER",
    "分发接收钱包": "DISTRIBUTION_SELLER",
    "Token接收钱包": "DISTRIBUTION_SELLER",
    "Token 接收钱包": "DISTRIBUTION_SELLER",
    "接盘鲸鱼": "BAGHOLDER_WHALE",
    "套牢钱包": "BAGHOLDER_WHALE",
    "普通交易钱包": "RETAIL_NOISE",
    "散户噪音": "RETAIL_NOISE",
}

DEFAULT_SIDE_BY_ROLE = {
    "EARLY_BUYER": "STRUCTURE_SIDE",
    "EARLY_EXIT": "DISTRIBUTION_SIDE",
    "PARTIAL_HOLDER": "STRUCTURE_SIDE",
    "HIGH_RESULT_WALLET": "STRUCTURE_SIDE",
    "SAME_SOURCE_GROUP": "EXECUTION_SIDE",
    "DISTRIBUTION_SELLER": "DISTRIBUTION_SIDE",
    "BAGHOLDER_WHALE": "COUNTERPARTY_SIDE",
    "RETAIL_NOISE": "NOISE_SIDE",
}

STATUS_TO_STATE = {
    "WALLET_BLOCK": "BLOCKED",
    "WALLET_PAUSE": "PAUSE_OR_WATCHING",
    "WALLET_SUPPORT": "ALLOW_PAPER_READY_IF_OTHER_GATES_PASS",
    "WALLET_NEUTRAL": "NO_WALLET_ADJUSTMENT",
}


@dataclass
class WalletStructureDecision:
    token: str
    symbol: str
    wallet_structure_status: str
    wallet_structure_factor: float
    wallet_structure_score: int
    wallet_risk_score: int
    counterparty_pressure_score: int
    data_quality_score: int
    chip_control_state: str
    data_quality_status: str = "UNKNOWN"
    decision_at: str = ""
    action_code: str = ""
    wallet_gate_result: str = ""
    paper_gate_effect: str = ""
    risk_level: str = ""
    reason_codes: List[str] = field(default_factory=list)
    missing_fields: List[str] = field(default_factory=list)
    source_files: List[str] = field(default_factory=list)
    valid_until: str = ""
    reasons: List[str] = field(default_factory=list)
    role_counts: Dict[str, int] = field(default_factory=dict)
    game_side_counts: Dict[str, int] = field(default_factory=dict)
    evidence_counts: Dict[str, int] = field(default_factory=dict)
    early_wallet_count: int = 0
    has_concentrated_clearout: bool = False
    has_same_source_sync_sell: bool = False
    max_sync_buy_score: int = 0
    max_sync_sell_score: int = 0
    has_distribution: bool = False
    recommendation: str = ""
    wallet_evidence_level: str = "E0"

    # Backward-compatible aliases used by older orchestrator/tests.
    @property
    def structure_score(self) -> int:
        return self.wallet_structure_score

    @property
    def risk_score(self) -> int:
        return self.wallet_risk_score

    @property
    def has_clearout(self) -> bool:
        return self.has_concentrated_clearout

    @property
    def has_same_source_candidate(self) -> bool:
        return self.has_same_source_sync_sell or self.role_counts.get("SAME_SOURCE_GROUP", 0) > 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "代币地址": self.token,
            "代币符号": self.symbol,
            "wallet_structure_status": self.wallet_structure_status,
            "wallet_structure_score": self.wallet_structure_score,
            "wallet_risk_score": self.wallet_risk_score,
            "counterparty_pressure_score": self.counterparty_pressure_score,
            "data_quality_score": self.data_quality_score,
            "data_quality_status": self.data_quality_status,
            "decision_at": self.decision_at,
            "action_code": self.action_code,
            "wallet_gate_result": self.wallet_gate_result,
            "paper_gate_effect": self.paper_gate_effect,
            "risk_level": self.risk_level,
            "reason_codes": self.reason_codes,
            "missing_fields": self.missing_fields,
            "source_files": self.source_files,
            "token_address": self.token,
            "symbol": self.symbol,
            "wallet_gate_result_cn": STATUS_TO_STATE[self.wallet_structure_status],
            "钱包结构结论": self.wallet_structure_status,
            "钱包结构系数": self.wallet_structure_factor,
            "钱包结构评分": self.wallet_structure_score,
            "钱包风险评分": self.wallet_risk_score,
            "对手盘压力评分": self.counterparty_pressure_score,
            "数据质量评分": self.data_quality_score,
            "筹码控制权状态": self.chip_control_state,
            "钱包证据等级": self.wallet_evidence_level,
            "早期钱包数量": self.early_wallet_count,
            "角色计数": self.role_counts,
            "game_side计数": self.game_side_counts,
            "证据计数": self.evidence_counts,
            "是否存在分发派发": "是" if self.has_distribution else "否",
            "是否存在集中清仓": "是" if self.has_concentrated_clearout else "否",
            "是否存在同源组同步卖出": "是" if self.has_same_source_sync_sell else "否",
            "最高同步买入分": self.max_sync_buy_score,
            "最高同步卖出分": self.max_sync_sell_score,
            "建议状态调整": self.recommendation,
            "状态机建议": STATUS_TO_STATE[self.wallet_structure_status],
            "状态调整原因": "；".join(self.reasons),
            "PAPER_READY允许说明": "钱包结构支持但不绕过 K线/quote/安全扫描；只有 signal_gate、quote_gate、security_gate 都通过，才允许 PAPER_READY。",
            "wallet_structure_status": self.wallet_structure_status,
            "wallet_structure_score": self.wallet_structure_score,
            "wallet_risk_score": self.wallet_risk_score,
            "counterparty_pressure_score": self.counterparty_pressure_score,
            "data_quality_score": self.data_quality_score,
            "data_quality_status": self.data_quality_status,
            "decision_at": self.decision_at,
            "action_code": self.action_code,
            "wallet_gate_result": self.wallet_gate_result,
            "paper_gate_effect": self.paper_gate_effect,
            "risk_level": self.risk_level,
            "reason_codes": self.reason_codes,
            "missing_fields": self.missing_fields,
            "source_files": self.source_files,
            "valid_until": self.valid_until,
            "wallet_structure_factor": self.wallet_structure_factor,
            "wallet_structure_reason": "；".join(self.reasons),
            "wallet_evidence_level": self.wallet_evidence_level,
            "说明": "钱包结构门禁只影响纸面/确认层状态，不执行真实 swap。",
        }


def _utc_now_text() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _text(row: Dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = row.get(key)
        if value not in (None, "", [], {}):
            return str(value)
    return ""


def _num(row: Dict[str, Any], *keys: str, default: float = 0.0) -> float:
    for key in keys:
        value = row.get(key)
        if value in (None, ""):
            continue
        try:
            return float(str(value).strip().rstrip("%"))
        except (TypeError, ValueError):
            continue
    return default


def _ratio(value: float) -> float:
    return value / 100.0 if value > 1 else value


def _role(row: Dict[str, Any]) -> str:
    raw = _text(row, "role", "钱包角色", "当前角色", "最终角色", "final_role", "current_role") or "RETAIL_NOISE"
    return raw if raw in WALLET_ROLES else ROLE_ALIASES.get(raw, "RETAIL_NOISE")


def _game_side(row: Dict[str, Any], role: str) -> str:
    raw = _text(row, "game_side", "筹码侧", "博弈侧")
    if raw in GAME_SIDES:
        return raw
    return DEFAULT_SIDE_BY_ROLE.get(role, "UNKNOWN_SIDE")


def _evidence_level(row: Dict[str, Any]) -> str:
    value = _text(row, "wallet_evidence_level", "证据等级", "evidence_level") or "E0"
    for prefix in ["E5", "E4", "E3", "E2", "E1", "E0", "R3", "R2", "R1"]:
        if value.startswith(prefix):
            return prefix
    return value


def _clearout(row: Dict[str, Any], role: str) -> bool:
    status = _text(row, "当前状态", "exit_status", "是否清仓")
    sell_ratio = _ratio(_num(row, "sell_ratio", "卖出占比", "sell_amount_percentage", default=0.0))
    return role == "EARLY_EXIT" or "清仓" in status or sell_ratio >= 0.7


def _highest_evidence(evidence_counts: Dict[str, int]) -> str:
    order = ["E5", "E4", "E3", "R3", "R2", "E2", "R1", "E1", "E0"]
    for item in order:
        if evidence_counts.get(item, 0) > 0:
            return item
    return "E0"


def _risk_level(status: str, risk_score: int, counterparty_score: int) -> str:
    if status == "WALLET_BLOCK" or risk_score >= 70 or counterparty_score >= 70:
        return "HIGH"
    if status == "WALLET_PAUSE" or risk_score >= 35 or counterparty_score >= 35:
        return "MEDIUM"
    if status == "WALLET_SUPPORT":
        return "LOW"
    return "INFO"


def _paper_gate_effect(status: str) -> str:
    if status == "WALLET_BLOCK":
        return "BLOCK_OR_PAUSE"
    if status == "WALLET_PAUSE":
        return "PAUSE_OR_REVIEW"
    if status == "WALLET_SUPPORT":
        return "REQUIRES_SIGNAL_QUOTE_SECURITY"
    return "OBSERVE_ONLY"


def _reason_codes(
    status: str,
    has_concentrated_clearout: bool,
    has_same_source_sync_sell: bool,
    data_quality_status: str,
    has_distribution: bool,
) -> List[str]:
    """Return stable machine-readable reason codes for wallet gate decisions."""
    codes: List[str] = []
    if status:
        codes.append(status)
    if has_concentrated_clearout:
        codes.append("CONCENTRATED_CLEAROUT")
    if has_same_source_sync_sell:
        codes.append("SAME_SOURCE_SYNC_SELL")
    if has_distribution:
        codes.append("DISTRIBUTION_ACTIVE")
    if data_quality_status in {"MISSING", "DEGRADED"}:
        codes.append(f"DATA_QUALITY_{data_quality_status}")
    if status == "WALLET_SUPPORT":
        codes.append("PAPER_ONLY_REQUIRES_OTHER_GATES")
    # Preserve order while avoiding duplicates.
    return list(dict.fromkeys(codes))


def _detect_missing_fields(rows: List[Dict[str, Any]]) -> List[str]:
    if not rows:
        return ["wallet_rows"]
    required = ["wallet_address", "role", "game_side", "evidence_level"]
    missing: List[str] = []
    for key in required:
        if not any(row.get(key) not in (None, "", [], {}) for row in rows):
            missing.append(key)
    return missing


def evaluate_wallet_structure_gate(*, token: str, symbol: str = "", wallet_rows: Iterable[Dict[str, Any]], candidate_groups: Iterable[Dict[str, Any]] | None = None) -> WalletStructureDecision:
    rows = list(wallet_rows)
    missing_fields = _detect_missing_fields(rows)
    role_counts: Dict[str, int] = {}
    side_counts: Dict[str, int] = {}
    evidence_counts: Dict[str, int] = {}
    group_sells: Dict[str, List[float]] = {}

    structure_score = 0
    risk_score = 0
    counterparty_score = 0
    complete_rows = 0
    clearout_count = 0
    distribution_count = 0
    unknown_side_count = 0

    for row in rows:
        role = _role(row)
        side = _game_side(row, role)
        evidence = _evidence_level(row)
        sell_ratio = _ratio(_num(row, "sell_ratio", "卖出占比", "sell_amount_percentage", default=0.0))
        holding_ratio = _ratio(_num(row, "holding_ratio", "持仓占比", "amount_percentage", default=0.0))
        unrealized_pct = _num(row, "unrealized_profit_pct", "未实现收益率", default=0.0)
        group_id = _text(row, "group_id", "组ID", "same_source_group")

        role_counts[role] = role_counts.get(role, 0) + 1
        side_counts[side] = side_counts.get(side, 0) + 1
        evidence_counts[evidence] = evidence_counts.get(evidence, 0) + 1
        if side == "UNKNOWN_SIDE":
            unknown_side_count += 1
        if role in WALLET_ROLES and side in GAME_SIDES and evidence not in {"", "E0"}:
            complete_rows += 1

        is_clearout = _clearout(row, role)
        if is_clearout:
            clearout_count += 1
        if role == "DISTRIBUTION_SELLER" or side == "DISTRIBUTION_SIDE":
            distribution_count += 1

        if role == "HIGH_RESULT_WALLET" and holding_ratio > 0.03 and sell_ratio < 0.5:
            structure_score += 28 if evidence in {"E4", "E5"} else 20
        elif role == "PARTIAL_HOLDER" and holding_ratio > 0.02 and sell_ratio < 0.55:
            structure_score += 18
        elif role == "EARLY_BUYER" and holding_ratio > 0.02 and sell_ratio < 0.5:
            structure_score += 16
        elif role == "SAME_SOURCE_GROUP" and sell_ratio < 0.5:
            structure_score += 14

        if role == "DISTRIBUTION_SELLER":
            risk_score += 32
        if role == "EARLY_EXIT" or (side == "DISTRIBUTION_SIDE" and is_clearout):
            risk_score += 22
        if role == "SAME_SOURCE_GROUP" and sell_ratio >= 0.7:
            risk_score += 20
        if is_clearout:
            risk_score += 10
        if role == "BAGHOLDER_WHALE":
            risk_score += 12
            counterparty_score += 24 + int(min(max(holding_ratio * 100, 0), 20))
            if unrealized_pct < -20:
                counterparty_score += 8
        elif side == "COUNTERPARTY_SIDE":
            counterparty_score += 12 + int(min(max(holding_ratio * 100, 0), 15))
        elif role == "RETAIL_NOISE" and side == "COUNTERPARTY_SIDE":
            counterparty_score += 8

        if role == "SAME_SOURCE_GROUP" and group_id:
            group_sells.setdefault(group_id, []).append(sell_ratio)

    row_count = len(rows)
    groups = list(candidate_groups or [])
    max_sync_buy_score = max([int(_num(group, "sync_buy_score", default=0)) for group in groups] or [0])
    max_sync_sell_score = max([int(_num(group, "sync_sell_score", default=0)) for group in groups] or [0])
    if max_sync_buy_score >= 70 and max_sync_sell_score < 40:
        structure_score += 18
    if max_sync_buy_score >= 70 and max_sync_sell_score >= 50:
        risk_score += 12
    if max_sync_sell_score >= 70:
        risk_score += 35
        counterparty_score += 35
    elif max_sync_sell_score >= 60:
        risk_score += 18
        counterparty_score += 20

    data_quality_score = 0 if row_count == 0 else int(round((complete_rows / row_count) * 100))
    if row_count < 2:
        data_quality_score = min(data_quality_score, 35)
    if unknown_side_count:
        data_quality_score = max(0, data_quality_score - int((unknown_side_count / max(row_count, 1)) * 30))

    if row_count == 0:
        data_quality_status = "MISSING"
    elif missing_fields or data_quality_score < 50:
        data_quality_status = "DEGRADED"
    else:
        data_quality_status = "OK"

    has_concentrated_clearout = row_count >= 3 and clearout_count / row_count >= 0.6
    has_same_source_sync_sell = (max_sync_sell_score >= 70) or any(len(values) >= 2 and sum(1 for v in values if v >= 0.7) / len(values) >= 0.6 for values in group_sells.values())
    has_distribution = distribution_count > 0

    structure_score = min(structure_score, 100)
    risk_score = min(risk_score + (25 if has_concentrated_clearout else 0) + (25 if has_same_source_sync_sell else 0), 100)
    counterparty_score = min(counterparty_score + (40 if has_concentrated_clearout else 0) + (35 if has_same_source_sync_sell else 0), 100)

    reasons: List[str] = []
    if has_concentrated_clearout:
        reasons.append("早期钱包集中清仓，筹码控制权疑似向分发/对手盘转移")
    if has_same_source_sync_sell:
        reasons.append("同源组同步卖出，执行侧筹码稳定性失效")
    if max_sync_sell_score >= 70:
        reasons.append("sync_sell_score>=70，同源/同步组卖出风险触发门禁阻断")
    elif max_sync_sell_score >= 60:
        reasons.append("sync_sell_score>=60，同源/同步组卖出风险触发暂停复核")
    if max_sync_buy_score >= 70 and max_sync_sell_score < 40:
        reasons.append("sync_buy_score 高且同步卖出低，疑似执行侧同步买入仍有结构支持")
    if has_distribution:
        reasons.append(f"发现分发侧钱包 {distribution_count} 个")
    if counterparty_score >= 50:
        reasons.append("对手盘压力高，接盘/套牢筹码占比偏高")
    if data_quality_score < 50:
        reasons.append("数据不足，钱包结构证据无法支撑放行")
    if structure_score >= 60 and risk_score < 30 and counterparty_score < 35:
        reasons.append("早期钱包仍持有，高结果钱包未退出，结构侧筹码仍有保留证据")
    if missing_fields:
        reasons.append(f"缺失字段：{', '.join(missing_fields)}")

    if has_concentrated_clearout or has_same_source_sync_sell or risk_score >= 70:
        status = "WALLET_BLOCK"
        factor = 0.0
        recommendation = "调整为 BLOCKED"
    elif data_quality_score < 50 or counterparty_score >= 50 or risk_score >= 35:
        status = "WALLET_PAUSE"
        factor = 0.3
        recommendation = "降级为 WATCHING/PAUSE，等待钱包结构、quote 或安全层复核"
    elif structure_score >= 60 and risk_score < 30 and counterparty_score < 35:
        status = "WALLET_SUPPORT"
        factor = 1.0
        recommendation = "仅在 signal_gate、quote_gate、security_gate 均通过时允许 PAPER_READY"
    else:
        status = "WALLET_NEUTRAL"
        factor = 0.6
        recommendation = "不加分、不阻断，继续走其他门禁"
        if not reasons:
            reasons.append("无明显结构证据，钱包侧保持中性")

    chip_decision = evaluate_chip_control_state(
        wallet_decision={
            "token_address": token,
            "symbol": symbol,
            "wallet_structure_status": status,
            "wallet_structure_score": structure_score,
            "wallet_risk_score": risk_score,
            "counterparty_pressure_score": counterparty_score,
            "data_quality_score": data_quality_score,
            "data_quality_status": data_quality_status,
            "max_sync_buy_score": max_sync_buy_score,
            "max_sync_sell_score": max_sync_sell_score,
            "has_concentrated_clearout": has_concentrated_clearout,
            "has_same_source_sync_sell": has_same_source_sync_sell,
            "has_distribution": has_distribution,
        }
    )
    chip_state = chip_decision.chip_control_state
    for chip_reason in chip_decision.reason_codes:
        if chip_reason not in reasons:
            reasons.append(f"筹码控制状态机：{chip_reason}")

    return WalletStructureDecision(
        token=token,
        symbol=symbol,
        wallet_structure_status=status,
        wallet_structure_factor=factor,
        wallet_structure_score=structure_score,
        wallet_risk_score=risk_score,
        counterparty_pressure_score=counterparty_score,
        data_quality_score=data_quality_score,
        chip_control_state=chip_state,
        data_quality_status=data_quality_status,
        decision_at=_utc_now_text(),
        action_code=status,
        wallet_gate_result=STATUS_TO_STATE[status],
        paper_gate_effect=_paper_gate_effect(status),
        risk_level=_risk_level(status, risk_score, counterparty_score),
        reason_codes=_reason_codes(status, has_concentrated_clearout, has_same_source_sync_sell, data_quality_status, has_distribution),
        missing_fields=missing_fields,
        source_files=["wallet_structure_decision.json"],
        valid_until=(datetime.now(timezone.utc) + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        reasons=reasons,
        role_counts=role_counts,
        game_side_counts=side_counts,
        evidence_counts=evidence_counts,
        early_wallet_count=row_count,
        has_concentrated_clearout=has_concentrated_clearout,
        has_same_source_sync_sell=has_same_source_sync_sell,
        max_sync_buy_score=max_sync_buy_score,
        max_sync_sell_score=max_sync_sell_score,
        has_distribution=has_distribution,
        recommendation=recommendation,
        wallet_evidence_level=_highest_evidence(evidence_counts),
    )


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_csv(path: Path, rows: List[Dict[str, Any]], fieldnames: List[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _gmgn_action(role: str, status: str) -> str:
    if status == "WALLET_BLOCK" or role in {"DISTRIBUTION_SELLER", "BAGHOLDER_WHALE", "EARLY_EXIT"}:
        return "risk_watch"
    if status == "WALLET_SUPPORT" and role in {"HIGH_RESULT_WALLET", "PARTIAL_HOLDER", "EARLY_BUYER"}:
        return "track"
    return "observe"


def evaluate_and_write_wallet_structure(*, token: str, symbol: str = "", wallet_rows: Iterable[Dict[str, Any]], output_dir: str | Path, candidate_groups: Iterable[Dict[str, Any]] | None = None) -> Dict[str, str]:
    rows = list(wallet_rows)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    decision = evaluate_wallet_structure_gate(token=token, symbol=symbol, wallet_rows=rows, candidate_groups=candidate_groups)
    now = _utc_now_text()

    raw_rows: List[Dict[str, Any]] = []
    classification_rows: List[Dict[str, Any]] = []
    gmgn_note_rows: List[Dict[str, Any]] = []
    group_map: Dict[str, List[str]] = {}

    for row in rows:
        role = _role(row)
        side = _game_side(row, role)
        wallet = _text(row, "wallet_address", "钱包地址", "address")
        evidence = _evidence_level(row)
        reason = _text(row, "主要原因", "role_reason", "wallet_structure_reason", "sikk_remark") or f"role={role}; side={side}"
        group_id = _text(row, "group_id", "组ID", "same_source_group")
        if group_id:
            group_map.setdefault(group_id, []).append(wallet)
        raw_rows.append({
            "钱包地址": wallet,
            "首次买入时间": _text(row, "first_buy_time", "首次买入时间"),
            "买入延迟": _text(row, "first_buy_delay", "买入延迟"),
            "所属时间窗口": _text(row, "time_window", "所属时间窗口"),
            "买入金额": _text(row, "buy_usd", "买入金额"),
            "卖出金额": _text(row, "sell_usd", "卖出金额"),
            "当前持仓": _text(row, "holding_ratio", "持仓占比", "当前持仓"),
            "卖出占比": _text(row, "sell_ratio", "卖出占比"),
            "钱包角色": role,
            "game_side": side,
            "资金来源状态": _text(row, "funding_status", "资金来源状态", "funding_source_type") or "资金待查",
            "原始证据引用": _text(row, "raw_unit_refs", "原始证据引用") or "暂无数据",
        })
        classification_rows.append({
            "钱包地址": wallet,
            "钱包角色": role,
            "game_side": side,
            "证据等级": evidence,
            "筹码解释": reason,
            "当前状态": _text(row, "当前状态", "exit_status") or ("已清仓" if _clearout(row, role) else "仍持有/待查"),
            "处理动作": _gmgn_action(role, decision.wallet_structure_status),
            "GMGN备注": _text(row, "GMGN备注", "gmgn_note") or f"{symbol or 'TOKEN'}-{role}-{evidence}-{side}",
            "原始证据引用": _text(row, "raw_unit_refs", "原始证据引用") or "暂无数据",
        })
        gmgn_note_rows.append({
            "address": wallet,
            "gmgn_note": _text(row, "GMGN备注", "gmgn_note") or f"{symbol or 'TOKEN'}-{role}-{evidence}-{side}",
            "reason": reason,
            "action": _gmgn_action(role, decision.wallet_structure_status),
        })

    candidate_groups = []
    for idx, (group_id, members) in enumerate(group_map.items(), start=1):
        candidate_groups.append({
            "组ID": group_id or f"G{idx}",
            "组类型": "同源同步候选组",
            "成员数量": len(members),
            "成员地址": ";".join(members),
            "组判断": "资金层待查，不强判同源；若同步卖出则作为门禁风险",
            "证据等级": decision.wallet_evidence_level,
            "备注": "资金层跳过/Token转入待复查",
        })
    if decision.has_distribution:
        candidate_groups.append({
            "组ID": "DISTRIBUTION_RISK",
            "组类型": "分发卖出组",
            "成员数量": decision.role_counts.get("DISTRIBUTION_SELLER", 0) + decision.role_counts.get("EARLY_EXIT", 0),
            "成员地址": "见 wallet_classification.csv",
            "组判断": "分发/清仓风险影响 PAPER_READY 门禁",
            "证据等级": "R2",
            "备注": "风险观察",
        })

    wallet_source_time = ""
    source_candidates = []
    for row in rows:
        value = _text(row, "wallet_source_time", "source_time", "snapshot_time", "updated_at", "last_seen_at", "首次买入时间", "first_buy_time")
        if value:
            source_candidates.append(value)
    if source_candidates:
        wallet_source_time = max(source_candidates)
    decision_payload = decision.to_dict()
    decision_payload.update({
        "wallet_snapshot_time": now,
        "wallet_decision_created_at": now,
        "wallet_delta_time": now,
        "wallet_source_time": wallet_source_time or now,
        "wallet_refresh_started_at": now,
        "wallet_refresh_finished_at": now,
    })
    decision_payload["生成时间"] = now
    decision_payload["模块"] = "SIKK-SOL v1.0 钱包结构门禁"
    decision_json = out / "wallet_structure_decision.json"
    raw_csv = out / "early_wallet_raw.csv"
    classification_csv = out / "wallet_classification.csv"
    groups_csv = out / "candidate_groups.csv"
    gmgn_csv = out / "gmgn_note_table.csv"
    summary_md = out / "wallet_structure_summary.md"

    _write_json(decision_json, decision_payload)
    _write_csv(raw_csv, raw_rows, ["钱包地址", "首次买入时间", "买入延迟", "所属时间窗口", "买入金额", "卖出金额", "当前持仓", "卖出占比", "钱包角色", "game_side", "资金来源状态", "原始证据引用"])
    _write_csv(classification_csv, classification_rows, ["钱包地址", "钱包角色", "game_side", "证据等级", "筹码解释", "当前状态", "处理动作", "GMGN备注", "原始证据引用"])
    _write_csv(groups_csv, candidate_groups, ["组ID", "组类型", "成员数量", "成员地址", "组判断", "证据等级", "备注"])
    _write_csv(gmgn_csv, gmgn_note_rows, ["address", "gmgn_note", "reason", "action"])

    md = [
        "# SIKK-SOL v1.0 钱包结构门禁",
        "",
        f"- 代币符号：{symbol}",
        f"- 代币地址：{token}",
        f"- 钱包结构结论：{decision.wallet_structure_status}",
        f"- 筹码控制权状态：{decision.chip_control_state}",
        f"- 钱包结构评分：{decision.wallet_structure_score}",
        f"- 钱包风险评分：{decision.wallet_risk_score}",
        f"- 对手盘压力评分：{decision.counterparty_pressure_score}",
        f"- 数据质量评分：{decision.data_quality_score}",
        f"- 钱包结构系数：{decision.wallet_structure_factor}",
        f"- 建议状态调整：{decision.recommendation}",
        f"- 状态调整原因：{'；'.join(decision.reasons)}",
        "- 边界：只做钱包结构门禁，不执行真实 swap；WALLET_SUPPORT 不能绕过 K线、quote、安全扫描。",
    ]
    summary_md.write_text("\n".join(md) + "\n", encoding="utf-8")

    return {
        "wallet_structure_decision_json": str(decision_json),
        "early_wallet_raw_csv": str(raw_csv),
        "wallet_classification_csv": str(classification_csv),
        "candidate_groups_csv": str(groups_csv),
        "gmgn_note_table_csv": str(gmgn_csv),
        "wallet_structure_summary_md": str(summary_md),
    }
