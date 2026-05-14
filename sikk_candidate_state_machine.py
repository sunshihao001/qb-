#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK Candidate State Machine v0.9

把 GMGN 新币筛选、候选 K线管道、候选信号管道的离散输出合并成统一状态机。

状态定义：
- DISCOVERED：GMGN 筛选进入候选池。
- WATCHING：S1/S2 观察候选，或信号尚未进入策略准备。
- ACCUMULATING：已出现 T_start，吸筹窗口仍 pending。
- READY_TO_BUY：吸筹窗口 valid，SIKK 信号达到 S3/S4。
- PAPER_READY：READY_TO_BUY 且风险门禁允许纸面交易，纸面仓位 > 0。
- BLOCKED：风险门禁 BLOCK，或信号 SX，或吸筹窗口 invalid。
- FAILED：上游数据/文件/管道失败。
- EXITED：第一版预留。

重要边界：本模块只管理候选状态，不执行真实 swap，不构建实盘交易命令。
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

from sikk_wallet_trade_adapter import apply_wallet_gate, normalize_wallet_decision


STATE_ORDER = [
    "DISCOVERED",
    "WATCHING",
    "ACCUMULATING",
    "READY_TO_BUY",
    "PAPER_READY",
    "BLOCKED",
    "FAILED",
    "EXITED",
]


def _utc_now_text() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _read_json(path: str | Path | None) -> Dict[str, Any]:
    if not path:
        return {}
    p = Path(path)
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: str | Path, payload: Dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_jsonl(path: str | Path, rows: Iterable[Dict[str, Any]]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


def _write_csv(path: str | Path, rows: Iterable[Dict[str, Any]]) -> None:
    rows = list(rows)
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        p.write_text("", encoding="utf-8")
        return
    fieldnames: List[str] = []
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)
    with p.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _candidate_rows(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """兼容不同候选池 JSON key。"""

    for key in ["候选结果", "候选列表", "处理结果", "tokens", "candidates", "results"]:
        rows = payload.get(key)
        if isinstance(rows, list):
            return rows
    if isinstance(payload, list):
        return payload
    return []


def _index_by_token(rows: Iterable[Dict[str, Any]], key: str = "代币地址") -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        token = str(row.get(key) or row.get("token_address") or row.get("代币地址") or row.get("token") or row.get("address") or "")
        if token:
            out[token] = row
    return out


def _load_accumulation(item: Dict[str, Any]) -> Dict[str, Any]:
    path = item.get("吸筹窗口输出") or item.get("accumulation_output") or item.get("accumulation_json")
    return _read_json(path)


def _wallet_structure_rows(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows = payload.get("处理结果") or payload.get("wallet_structure_results") or payload.get("results") or []
    return rows if isinstance(rows, list) else []


def _trade_gate_rows(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows = payload.get("处理结果") or payload.get("trade_gate_results") or payload.get("results") or payload.get("tokens") or []
    return rows if isinstance(rows, list) else []


def _apply_wallet_structure_gate(
    state: str,
    reason: str,
    detail: Dict[str, Any],
    wallet_item: Dict[str, Any] | None,
    wallet_structure_mode: str = "observe",
) -> Tuple[str, str, Dict[str, Any]]:
    if not wallet_item:
        detail.update({
            "钱包结构结论": "未接入",
            "钱包结构系数": "",
            "钱包结构评分": "",
            "钱包风险评分": "",
            "对手盘压力评分": "",
            "数据质量评分": "",
            "钱包证据等级": "",
            "钱包结构原因": "",
            "钱包门禁模式": wallet_structure_mode,
            "钱包门禁效果": "NO_WALLET_INPUT",
            "would_block": False,
            "would_pause": False,
            "wallet_decision_stale": False,
        })
        return state, reason, detail

    decision = normalize_wallet_decision(wallet_item)
    token_status = {"state": state, "当前状态": state}
    gated = apply_wallet_gate(token_status, decision, mode=wallet_structure_mode)
    new_state = str(gated.get("state") or state)
    wallet_reason = str(decision.get("reason") or "")
    effect = str(gated.get("wallet_gate_effect") or "")

    detail.update({
        "钱包结构结论": decision.get("wallet_structure_status", ""),
        "钱包结构系数": decision.get("wallet_structure_factor", ""),
        "钱包结构评分": decision.get("wallet_structure_score", ""),
        "钱包风险评分": decision.get("wallet_risk_score", ""),
        "对手盘压力评分": decision.get("counterparty_pressure_score", ""),
        "数据质量评分": decision.get("data_quality_score", ""),
        "钱包证据等级": decision.get("wallet_evidence_level", ""),
        "钱包结构原因": wallet_reason,
        "钱包门禁模式": wallet_structure_mode,
        "钱包门禁效果": effect,
        "would_block": bool(gated.get("would_block")),
        "would_pause": bool(gated.get("would_pause")),
        "wallet_decision_stale": bool(gated.get("wallet_decision_stale")),
    })

    if new_state != state:
        if effect in {"HARD_BLOCK", "SOFT_BLOCK"}:
            return new_state, f"钱包结构门禁阻断：{wallet_reason or effect}", detail
        if effect in {"HARD_PAUSE", "HARD_PAUSE_UNKNOWN"}:
            return "WATCHING", f"钱包结构门禁暂停：{wallet_reason or effect}", detail
    return state, reason, detail

def _apply_trade_gate_runtime(
    state: str,
    reason: str,
    detail: Dict[str, Any],
    trade_gate_item: Dict[str, Any] | None,
) -> Tuple[str, str, Dict[str, Any]]:
    if not trade_gate_item:
        detail.update({
            "交易门控状态": "未接入",
            "交易门控决策": "",
            "交易权限": "",
            "合约门控权限": "",
            "真实交易允许": False,
            "交易执行动作": "",
            "资金状态": "",
            "交易门控风险等级": "",
            "交易门控原因码": [],
        })
        return state, reason, detail

    final_status = str(trade_gate_item.get("final_status") or trade_gate_item.get("交易门控状态") or "")
    decision = str(trade_gate_item.get("decision") or trade_gate_item.get("交易门控决策") or "")
    permission = str(trade_gate_item.get("permission") or trade_gate_item.get("交易权限") or "")
    contract_permission = str(trade_gate_item.get("contract_permission") or trade_gate_item.get("合约门控权限") or "")
    real_trade_enabled = bool(trade_gate_item.get("real_trade_enabled") is True)
    reason_codes = trade_gate_item.get("reason_codes") or trade_gate_item.get("交易门控原因码") or []
    if isinstance(reason_codes, str):
        reason_codes = [reason_codes]

    detail.update({
        "交易门控状态": final_status,
        "交易门控决策": decision,
        "交易权限": permission,
        "合约门控权限": contract_permission,
        "真实交易允许": real_trade_enabled,
        "交易执行动作": trade_gate_item.get("execution_action") or trade_gate_item.get("交易执行动作") or "",
        "资金状态": trade_gate_item.get("funding_status") or trade_gate_item.get("资金状态") or "",
        "交易门控风险等级": trade_gate_item.get("risk_level") or trade_gate_item.get("交易门控风险等级") or "",
        "交易门控原因码": list(reason_codes) if isinstance(reason_codes, list) else [],
    })

    status_upper = final_status.upper()
    decision_upper = decision.upper()
    permission_upper = permission.upper()
    contract_upper = contract_permission.upper()
    blocked = status_upper == "BLOCK" or "BLOCK_REAL_TRADE_AND_OBSERVE" in permission_upper or "BLOCK_REAL_TRADE_AND_OBSERVE" in contract_upper
    paused = (
        status_upper in {"OBSERVE", "PAUSE", "PAUSED"}
        or decision_upper in {"OBSERVE_ONLY", "PAPER_ONLY"}
        or "PAUSE" in contract_upper
        or "BLOCK_REAL_TRADE" in permission_upper
        or "BLOCK_REAL_TRADE" in contract_upper
    )

    if blocked:
        return "BLOCKED", f"交易门控阻断：{decision or permission or final_status}", detail
    if paused:
        return "WATCHING", f"交易门控暂停：{decision or contract_permission or final_status}", detail
    if real_trade_enabled:
        # Runtime contract 当前仍为 paper-only；这里保留字段，不提升到真实交易状态。
        return state, f"{reason}；交易门控显示可纸面验证，真实交易仍需外部人工确认", detail
    return state, reason, detail


def _derive_state(
    candidate: Dict[str, Any],
    kline_item: Dict[str, Any] | None,
    signal_item: Dict[str, Any] | None,
    skipped_signal: Dict[str, Any] | None,
) -> Tuple[str, str, Dict[str, Any]]:
    """根据三层输出推导当前状态。"""

    token_level = str(candidate.get("筛选等级") or "")
    symbol = candidate.get("代币符号", "")

    detail: Dict[str, Any] = {
        "代币符号": symbol,
        "候选筛选等级": token_level,
        "吸筹窗口状态": "",
        "T_start": "",
        "T_end": "",
        "信号等级": "",
        "风险门禁": "",
        "建议纸面仓位SOL": 0.0,
    }

    # S2/S1 默认观察；后续若已有更强信号再覆盖。
    base_state = "DISCOVERED"
    base_reason = "GMGN 新币筛选进入候选池"
    if "S1" in token_level or "S2" in token_level:
        base_state = "WATCHING"
        base_reason = "候选筛选等级为观察层，等待更多 K线/结构证据"

    if skipped_signal:
        detail["信号等级"] = "SKIPPED"
        return "FAILED", skipped_signal.get("原因") or "信号管道跳过", detail

    if kline_item is not None and kline_item.get("状态") not in {"ok", "OK", "success", "SUCCESS"}:
        return "FAILED", kline_item.get("错误") or "K线管道失败", detail

    if kline_item is None:
        return base_state, base_reason, detail

    accumulation = _load_accumulation(kline_item)
    window_status = str(accumulation.get("window_status") or accumulation.get("窗口状态") or "")
    detail.update({
        "吸筹窗口状态": window_status,
        "T_start": accumulation.get("T_start", ""),
        "T_end": accumulation.get("T_end", ""),
        "POC_price": accumulation.get("POC_price", ""),
    })

    if window_status == "invalid":
        return "BLOCKED", "吸筹窗口 invalid，进入风险阻断观察", detail
    if window_status == "pending" and accumulation.get("T_start"):
        base_state = "ACCUMULATING"
        base_reason = "已出现 T_start，但吸筹窗口仍 pending"
    elif window_status == "valid":
        base_state = "WATCHING"
        base_reason = "吸筹窗口 valid，等待 SIKK 信号确认"

    if signal_item is None:
        return base_state, base_reason, detail

    signal_level = str(signal_item.get("信号等级") or "")
    risk_gate = str(signal_item.get("风险门禁") or "")
    position_sol = _as_float(signal_item.get("建议纸面仓位SOL"), 0.0)
    detail.update({
        "信号等级": signal_level,
        "风险门禁": risk_gate,
        "建议纸面仓位SOL": position_sol,
        "策略类型": signal_item.get("策略类型", ""),
        "信号时间": signal_item.get("信号时间", ""),
        "信号价格": signal_item.get("信号价格", ""),
    })

    if "BLOCK_BUY" in risk_gate or signal_level.startswith("SX"):
        return "BLOCKED", "风险门禁阻断或 SIKK 信号 SX", detail
    if window_status == "valid" and (signal_level.startswith("S3") or signal_level.startswith("S4")):
        if "ALLOW_PAPER_TRADE" in risk_gate and position_sol > 0:
            return "PAPER_READY", "吸筹窗口 valid + SIKK S3/S4 + 允许纸面交易 + 仓位大于0", detail
        return "READY_TO_BUY", "吸筹窗口 valid + SIKK S3/S4，但尚未满足纸面仓位/门禁条件", detail
    if signal_level.startswith("S1") or signal_level.startswith("S2"):
        return "WATCHING", "SIKK 信号仍为观察/预备层", detail
    return base_state, base_reason, detail


def run_candidate_state_machine(
    *,
    candidates_path: str | Path,
    kline_summary_path: str | Path | None = None,
    signal_summary_path: str | Path | None = None,
    wallet_structure_summary_path: str | Path | None = None,
    trade_gate_summary_path: str | Path | None = None,
    wallet_structure_mode: str = "observe",
    output_dir: str | Path = "data/gmgn_candidates/state_machine",
) -> Dict[str, str]:
    """运行候选币状态机并写出四类文件。"""

    candidates_payload = _read_json(candidates_path)
    kline_payload = _read_json(kline_summary_path)
    signal_payload = _read_json(signal_summary_path)
    wallet_structure_payload = _read_json(wallet_structure_summary_path)
    trade_gate_payload = _read_json(trade_gate_summary_path)

    candidates = _candidate_rows(candidates_payload)
    kline_index = _index_by_token(kline_payload.get("处理结果", []))
    signal_index = _index_by_token(signal_payload.get("信号结果", []))
    skipped_signal_index = _index_by_token(signal_payload.get("跳过结果", []))
    wallet_structure_index = _index_by_token(_wallet_structure_rows(wallet_structure_payload))
    trade_gate_index = _index_by_token(_trade_gate_rows(trade_gate_payload))

    now = _utc_now_text()
    states: List[Dict[str, Any]] = []
    events: List[Dict[str, Any]] = []

    for candidate in candidates:
        token = str(candidate.get("代币地址") or candidate.get("address") or candidate.get("token") or "")
        if not token:
            continue
        kline_item = kline_index.get(token)
        signal_item = signal_index.get(token)
        skipped_signal = skipped_signal_index.get(token)
        wallet_item = wallet_structure_index.get(token)
        trade_gate_item = trade_gate_index.get(token)
        state, reason, detail = _derive_state(candidate, kline_item, signal_item, skipped_signal)
        state, reason, detail = _apply_wallet_structure_gate(state, reason, detail, wallet_item, wallet_structure_mode=wallet_structure_mode)
        state, reason, detail = _apply_trade_gate_runtime(state, reason, detail, trade_gate_item)
        row = {
            "代币地址": token,
            "代币符号": detail.get("代币符号") or candidate.get("代币符号", ""),
            "当前状态": state,
            "状态原因": reason,
            "候选筛选等级": detail.get("候选筛选等级", ""),
            "吸筹窗口状态": detail.get("吸筹窗口状态", ""),
            "T_start": detail.get("T_start", ""),
            "T_end": detail.get("T_end", ""),
            "信号等级": detail.get("信号等级", ""),
            "风险门禁": detail.get("风险门禁", ""),
            "建议纸面仓位SOL": detail.get("建议纸面仓位SOL", 0.0),
            "钱包结构结论": detail.get("钱包结构结论", "未接入"),
            "钱包结构系数": detail.get("钱包结构系数", ""),
            "钱包结构评分": detail.get("钱包结构评分", ""),
            "钱包风险评分": detail.get("钱包风险评分", ""),
            "对手盘压力评分": detail.get("对手盘压力评分", ""),
            "数据质量评分": detail.get("数据质量评分", ""),
            "钱包证据等级": detail.get("钱包证据等级", ""),
            "钱包结构原因": detail.get("钱包结构原因", ""),
            "钱包门禁模式": detail.get("钱包门禁模式", wallet_structure_mode),
            "钱包门禁效果": detail.get("钱包门禁效果", ""),
            "would_block": detail.get("would_block", False),
            "would_pause": detail.get("would_pause", False),
            "wallet_decision_stale": detail.get("wallet_decision_stale", False),
            "交易门控状态": detail.get("交易门控状态", "未接入"),
            "交易门控决策": detail.get("交易门控决策", ""),
            "交易权限": detail.get("交易权限", ""),
            "合约门控权限": detail.get("合约门控权限", ""),
            "真实交易允许": detail.get("真实交易允许", False),
            "交易执行动作": detail.get("交易执行动作", ""),
            "资金状态": detail.get("资金状态", ""),
            "交易门控风险等级": detail.get("交易门控风险等级", ""),
            "交易门控原因码": detail.get("交易门控原因码", []),
            "策略类型": detail.get("策略类型", ""),
            "更新时间": now,
            "模式": "paper/readiness",
        }
        states.append(row)
        events.append({
            "event_time": now,
            "token": token,
            "symbol": row["代币符号"],
            "from_state": "UNKNOWN",
            "to_state": state,
            "reason": reason,
            "mode": "paper/readiness",
        })

    counts = Counter(row["当前状态"] for row in states)
    status_counts = {state: counts.get(state, 0) for state in STATE_ORDER}
    output_path = Path(output_dir)
    states_json = output_path / "candidate_states.json"
    states_csv = output_path / "candidate_states.csv"
    events_jsonl = output_path / "state_events.jsonl"
    summary_md = output_path / "state_summary.md"

    payload = {
        "模块": "SIKK Candidate State Machine v0.9",
        "更新时间": now,
        "输入文件": {
            "候选池": str(candidates_path),
            "K线管道": str(kline_summary_path or ""),
            "信号管道": str(signal_summary_path or ""),
            "钱包结构门禁": str(wallet_structure_summary_path or ""),
            "交易系统门控": str(trade_gate_summary_path or ""),
            "钱包结构模式": wallet_structure_mode,
        },
        "状态统计": status_counts,
        "候选状态": states,
        "说明": "本状态机只管理候选生命周期与纸面准备状态，不执行真实 swap。",
    }
    _write_json(states_json, payload)
    _write_csv(states_csv, states)
    _write_jsonl(events_jsonl, events)

    md_lines = [
        "# SIKK 候选币状态机汇总",
        "",
        f"- 更新时间：{now}",
        f"- 候选数量：{len(states)}",
        "- 执行边界：只管理状态与纸面准备，不执行真实 swap。",
        "",
        "## 状态统计",
        "",
    ]
    for state in STATE_ORDER:
        md_lines.append(f"- {state}：{status_counts[state]}")
    md_lines.extend(["", "## 候选状态", ""])
    for row in states:
        md_lines.extend([
            f"- 代币：{row['代币符号']} / {row['代币地址']}",
            f"  - 当前状态：{row['当前状态']}",
            f"  - 状态原因：{row['状态原因']}",
            f"  - 信号等级：{row['信号等级']}",
            f"  - 风险门禁：{row['风险门禁']}",
            f"  - 钱包结构结论：{row.get('钱包结构结论', '未接入')}",
            f"  - 交易门控：{row.get('交易门控决策', '')} / {row.get('交易门控状态', '未接入')}",
        ])
    summary_md.parent.mkdir(parents=True, exist_ok=True)
    summary_md.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    return {
        "states_json": str(states_json),
        "states_csv": str(states_csv),
        "events_jsonl": str(events_jsonl),
        "summary_md": str(summary_md),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SIKK Candidate State Machine v0.9")
    parser.add_argument("--candidates", required=True, help="token_candidates.json")
    parser.add_argument("--kline-summary", default=None, help="candidate_kline_pipeline_summary.json")
    parser.add_argument("--signal-summary", default=None, help="candidate_signal_summary.json")
    parser.add_argument("--wallet-structure-summary", default=None, help="candidate_wallet_structure_summary.json")
    parser.add_argument("--trade-gate-summary", default=None, help="trade_gate_runtime_summary.json")
    parser.add_argument("--wallet-structure-mode", choices=["off", "observe", "soft", "hard"], default="observe", help="钱包结构交易接入模式，默认 observe 只记录不阻断")
    parser.add_argument("--output-dir", default="data/gmgn_candidates/state_machine")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_candidate_state_machine(
        candidates_path=args.candidates,
        kline_summary_path=args.kline_summary,
        signal_summary_path=args.signal_summary,
        wallet_structure_summary_path=args.wallet_structure_summary,
        trade_gate_summary_path=args.trade_gate_summary,
        wallet_structure_mode=args.wallet_structure_mode,
        output_dir=args.output_dir,
    )
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
