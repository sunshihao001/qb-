#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK Live Runtime v0.2 orchestrator.

持续运行层：候选 → 模块调用 → token_status → process_trace → live_board/dashboard/events。
默认只做分析、纸面与只读采集，不执行真实 swap。
"""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional

from sikk_dashboard_builder import write_dashboard
from sikk_module_runner import run_external_modules_for_token
from sikk_notifier import notify_event
from sikk_token_skip_policy import should_process_token
from sikk_trace_logger import write_process_trace

DEFAULT_BASE_DIR = Path("data/gmgn_candidates_live_run")


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _append_jsonl(path: Path, row: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _token_address(token: Mapping[str, Any]) -> str:
    return str(token.get("token_address") or token.get("代币地址") or "")


def _token_symbol(token: Mapping[str, Any]) -> str:
    return str(token.get("token_symbol") or token.get("代币符号") or token.get("symbol") or "")


def load_existing_token_status(token: Mapping[str, Any], base_dir: str | Path = DEFAULT_BASE_DIR) -> Optional[Dict[str, Any]]:
    path = Path(base_dir) / "tokens" / _token_address(token) / "token_status.json"
    payload = _read_json(path)
    return payload or None


def emit_event(
    *,
    base_dir: str | Path,
    event_type: str,
    message: str,
    token: Optional[Mapping[str, Any]] = None,
    data: Optional[Mapping[str, Any]] = None,
    level: str = "INFO",
    config: Optional[Mapping[str, Any]] = None,
    event_time: Optional[str] = None,
) -> Dict[str, Any]:
    event = {
        "time": event_time or iso_now(),
        "event_type": event_type,
        "level": level,
        "token_address": _token_address(token or {}),
        "token_symbol": _token_symbol(token or {}),
        "message": message,
        "data": dict(data or {}),
    }
    _append_jsonl(Path(base_dir) / "events" / "live_events.jsonl", event)
    try:
        notify_event(event, config or {})
    except Exception:
        pass
    return event


def build_token_status(token: Mapping[str, Any], module_result: Mapping[str, Any], *, now: Optional[str] = None) -> Dict[str, Any]:
    module_results = module_result.get("module_results", []) if isinstance(module_result.get("module_results", []), list) else []
    error_modules = [row for row in module_results if row.get("status") == "ERROR"]
    wallet_row = next((row for row in module_results if row.get("module") == "wallet_structure"), {})

    if error_modules:
        current_state = "ERROR"
        latest_reason = "; ".join(f"{row.get('module')}:{row.get('reason')}" for row in error_modules)
    else:
        current_state = "WATCHING"
        latest_reason = "Runtime 模块调用完成，等待状态机/钱包/quote/paper 进一步确认"

    wallet_status = "UNKNOWN"
    if wallet_row.get("status") == "OK":
        wallet_status = "WALLET_CHECKED"
    elif wallet_row.get("status") == "SKIPPED":
        wallet_status = "WALLET_SKIPPED"
    elif wallet_row.get("status") == "ERROR":
        wallet_status = "WALLET_ERROR"

    return {
        "token_address": _token_address(token),
        "token_symbol": _token_symbol(token),
        "current_state": current_state,
        "last_update": now or iso_now(),
        "latest_action": "MODULES_FINISHED",
        "latest_reason": latest_reason,
        "wallet_structure": {"wallet_structure_status": wallet_status},
        "signal": {"signal_gate": "UNKNOWN"},
        "quote": {"quote_gate": "UNKNOWN"},
        "security": {"security_gate": "UNKNOWN"},
        "paper": {"paper_status": "UNKNOWN"},
        "module_result": dict(module_result),
        "scope_note": "Runtime 状态只用于监控与纸面流程，不执行真实 swap。",
    }


def write_token_status_files(status: Mapping[str, Any], *, base_dir: str | Path = DEFAULT_BASE_DIR) -> Dict[str, str]:
    base = Path(base_dir)
    token = str(status.get("token_address") or "")
    token_dir = base / "tokens" / token
    json_path = token_dir / "token_status.json"
    md_path = token_dir / "token_status.md"
    _write_json(json_path, status)
    md_lines = [
        f"# Token 状态：{status.get('token_symbol')} / {status.get('token_address')}",
        "",
        f"- 当前状态：{status.get('current_state')}",
        f"- 更新时间：{status.get('last_update')}",
        f"- 最新动作：{status.get('latest_action')}",
        f"- 最新原因：{status.get('latest_reason')}",
        "- 边界：Runtime 只做监控、分析、纸面流程，不执行真实 swap。",
    ]
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    return {"token_status_json": str(json_path), "token_status_md": str(md_path)}


def write_live_state(status_rows: List[Mapping[str, Any]], *, base_dir: str | Path = DEFAULT_BASE_DIR, now: Optional[str] = None) -> str:
    path = Path(base_dir) / "live_state.json"
    payload = {"last_update": now or iso_now(), "token_count": len(status_rows), "tokens": list(status_rows), "scope_note": "Live state 不代表真实交易授权。"}
    _write_json(path, payload)
    return str(path)


def write_latest_events_md(*, base_dir: str | Path = DEFAULT_BASE_DIR, limit: int = 20) -> str:
    base = Path(base_dir)
    events_path = base / "events" / "live_events.jsonl"
    out = base / "events" / "latest_events.md"
    rows: List[Mapping[str, Any]] = []
    if events_path.exists():
        for line in events_path.read_text(encoding="utf-8").splitlines()[-limit:]:
            try:
                rows.append(json.loads(line))
            except Exception:
                continue
    lines = ["# SIKK 最新运行事件", "", "- 边界：事件只用于运行监控和纸面流程，不代表真实交易授权。", ""]
    for row in rows:
        lines.append(f"- {row.get('time')}｜{row.get('event_type')}｜{row.get('token_symbol') or '-'}｜{row.get('message')}")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return str(out)


def _status_rank(row: Mapping[str, Any]) -> tuple:
    state = str(row.get("current_state") or "UNKNOWN").upper()
    wallet = row.get("wallet_structure", {}) if isinstance(row.get("wallet_structure", {}), Mapping) else {}
    wallet_status = str(wallet.get("wallet_structure_status") or "").upper()
    order = {
        "PAPER_OPEN": 0,
        "PAPER_READY": 1,
        "READY_FOR_CONFIRMATION": 1,
        "WALLET_SUPPORT": 2,
        "PAUSE": 3,
        "WATCHING": 4,
        "BLOCKED": 5,
        "MISSING": 6,
        "ERROR": 7,
    }
    rank = order.get(state, order.get(wallet_status, 8))
    def num(value, default=0):
        try:
            return float(value)
        except Exception:
            return default
    return (rank, -num(wallet.get("wallet_structure_score")), num(wallet.get("counterparty_pressure_score")), -num(wallet.get("data_quality_score")), str(row.get("token_symbol") or ""))


def _priority_level(row: Mapping[str, Any]) -> str:
    if row.get("priority_level"):
        return str(row.get("priority_level"))
    state = str(row.get("current_state") or "UNKNOWN").upper()
    wallet = row.get("wallet_structure", {}) if isinstance(row.get("wallet_structure", {}), Mapping) else {}
    wallet_status = str(wallet.get("wallet_structure_status") or "").upper()
    if state == "PAPER_OPEN":
        return "P0_ACTIVE_POSITION"
    if state in {"PAPER_READY", "READY_FOR_CONFIRMATION"}:
        return "P1_PAPER_READY"
    if wallet_status == "WALLET_SUPPORT":
        return "P2_STRUCTURE_SUPPORT"
    if state == "PAUSE":
        return "P4_PAUSE"
    if state == "BLOCKED" or wallet_status == "WALLET_BLOCK":
        return "P5_BLOCKED"
    if wallet_status in {"MISSING", "UNKNOWN", ""}:
        return "P6_DATA_MISSING"
    return "P3_WATCHING"


def _next_action(row: Mapping[str, Any]) -> str:
    if row.get("latest_action"):
        return str(row.get("latest_action"))
    state = str(row.get("current_state") or "UNKNOWN").upper()
    wallet = row.get("wallet_structure", {}) if isinstance(row.get("wallet_structure", {}), Mapping) else {}
    wallet_status = str(wallet.get("wallet_structure_status") or "").upper()
    quote = row.get("quote", {}) if isinstance(row.get("quote", {}), Mapping) else {}
    security = row.get("security", {}) if isinstance(row.get("security", {}), Mapping) else {}
    paper = row.get("paper", {}) if isinstance(row.get("paper", {}), Mapping) else {}
    if state == "PAPER_OPEN":
        return "EXIT_MONITOR" if wallet_status in {"WALLET_PAUSE", "WALLET_BLOCK"} else "HOLD"
    if state in {"PAPER_READY", "READY_FOR_CONFIRMATION"}:
        return "OPEN_PAPER_POSITION"
    if wallet_status in {"MISSING", "UNKNOWN", ""}:
        return "FIX_DATA_SOURCE"
    if wallet_status == "WALLET_BLOCK" or state == "BLOCKED":
        return "COOLING"
    if str(quote.get("quote_gate") or "").upper() in {"MISSING", "PAUSE", "ERROR"}:
        return "WAIT_QUOTE"
    if str(security.get("security_gate") or "").upper() in {"MISSING", "PAUSE", "ERROR"}:
        return "WAIT_SECURITY"
    if str(paper.get("paper_status") or "").upper() in {"READY"}:
        return "READY_FOR_PAPER"
    return "WAIT_SIGNAL"


def _reason(row: Mapping[str, Any]) -> str:
    wallet = row.get("wallet_structure", {}) if isinstance(row.get("wallet_structure", {}), Mapping) else {}
    state = str(row.get("current_state") or "UNKNOWN")
    return str(row.get("latest_reason") or wallet.get("missing_reason") or wallet.get("wallet_structure_reason") or f"{state} 状态待下一轮复查")


def write_live_board(status_rows: List[Mapping[str, Any]], *, base_dir: str | Path = DEFAULT_BASE_DIR, now: Optional[str] = None) -> str:
    from collections import Counter

    path = Path(base_dir) / "live_board.md"
    rows = sorted([dict(row) for row in status_rows], key=_status_rank)
    state_counts = Counter(str(row.get("current_state") or "UNKNOWN") for row in rows)
    wallet_counts = Counter(str((row.get("wallet_structure") if isinstance(row.get("wallet_structure"), Mapping) else {}).get("wallet_structure_status") or "MISSING") for row in rows)
    wallet_covered = sum(1 for row in rows if str((row.get("wallet_structure") if isinstance(row.get("wallet_structure"), Mapping) else {}).get("wallet_structure_status") or "").upper() not in {"", "UNKNOWN", "MISSING"})
    open_positions = sum(1 for row in rows if str((row.get("paper") if isinstance(row.get("paper"), Mapping) else {}).get("paper_status") or row.get("current_state") or "").upper() in {"OPEN", "PAPER_OPEN"})

    missing_reasons = Counter()
    entry_reasons = Counter()
    for row in rows:
        wallet = row.get("wallet_structure", {}) if isinstance(row.get("wallet_structure", {}), Mapping) else {}
        signal = row.get("signal", {}) if isinstance(row.get("signal", {}), Mapping) else {}
        quote = row.get("quote", {}) if isinstance(row.get("quote", {}), Mapping) else {}
        security = row.get("security", {}) if isinstance(row.get("security", {}), Mapping) else {}
        paper = row.get("paper", {}) if isinstance(row.get("paper", {}), Mapping) else {}
        wallet_status = str(wallet.get("wallet_structure_status") or "MISSING").upper()
        if wallet_status in {"MISSING", "UNKNOWN", ""}:
            missing_reasons[str(wallet.get("missing_reason") or _reason(row))] += 1
            entry_reasons["wallet_structure_missing"] += 1
        if wallet_status == "WALLET_BLOCK":
            entry_reasons["wallet_block"] += 1
        if str(signal.get("signal_gate") or "").upper() not in {"PASS", "ALLOW"} and str(row.get("current_state") or "").upper() not in {"PAPER_OPEN", "PAPER_READY"}:
            entry_reasons["signal_not_ready"] += 1
        if str(quote.get("quote_gate") or "").upper() in {"MISSING", "PAUSE", "ERROR", ""}:
            entry_reasons["quote_not_ready"] += 1
        if str(security.get("security_gate") or "").upper() in {"MISSING", "PAUSE", "ERROR", ""}:
            entry_reasons["security_not_ready"] += 1
        if str(paper.get("paper_status") or "").upper() in {"NONE", "", "MISSING"} and str(row.get("current_state") or "").upper() in {"PAPER_READY", "READY_FOR_CONFIRMATION"}:
            entry_reasons["paper_runner_not_called"] += 1
        if str(row.get("current_state") or "").upper() not in {"PAPER_READY", "PAPER_OPEN", "READY_FOR_CONFIRMATION"}:
            entry_reasons["state_not_ready"] += 1

    def token_line(row: Mapping[str, Any]) -> str:
        wallet = row.get("wallet_structure", {}) if isinstance(row.get("wallet_structure", {}), Mapping) else {}
        signal = row.get("signal", {}) if isinstance(row.get("signal", {}), Mapping) else {}
        quote = row.get("quote", {}) if isinstance(row.get("quote", {}), Mapping) else {}
        security = row.get("security", {}) if isinstance(row.get("security", {}), Mapping) else {}
        paper = row.get("paper", {}) if isinstance(row.get("paper", {}), Mapping) else {}
        return (
            f"- {row.get('token_symbol') or '-'} / {row.get('token_address')}\n"
            f"  - Priority：{_priority_level(row)}\n"
            f"  - State：{row.get('current_state')}\n"
            f"  - Signal：{signal.get('signal_level') or '-'} / {signal.get('signal_gate') or '-'}\n"
            f"  - Wallet：{wallet.get('wallet_structure_status') or 'MISSING'} / score={wallet.get('wallet_structure_score', '-')} / risk={wallet.get('wallet_risk_score', '-')} / counterparty={wallet.get('counterparty_pressure_score', '-')} / data={wallet.get('data_quality_score', '-')}\n"
            f"  - Quote/Security：{quote.get('quote_gate') or '-'} / {security.get('security_gate') or '-'}\n"
            f"  - Paper：{paper.get('paper_status') or '-'} / PnL={paper.get('unrealized_pnl_pct') or paper.get('net_pnl_pct') or '-'}\n"
            f"  - 主原因：{_reason(row)}\n"
            f"  - Next：{_next_action(row)}"
        )

    opportunity = [row for row in rows if str(row.get("current_state") or "").upper() in {"PAPER_OPEN", "PAPER_READY", "READY_FOR_CONFIRMATION"} or str((row.get("wallet_structure") if isinstance(row.get("wallet_structure"), Mapping) else {}).get("wallet_structure_status") or "").upper() == "WALLET_SUPPORT"]
    blocked_pause = [row for row in rows if str(row.get("current_state") or "").upper() in {"BLOCKED", "PAUSE", "WATCHING"} or str((row.get("wallet_structure") if isinstance(row.get("wallet_structure"), Mapping) else {}).get("wallet_structure_status") or "").upper() in {"WALLET_BLOCK", "MISSING", "WALLET_PAUSE"}]
    paper_rows = [row for row in rows if str((row.get("paper") if isinstance(row.get("paper"), Mapping) else {}).get("paper_status") or row.get("current_state") or "").upper() in {"OPEN", "PAPER_OPEN", "READY"}]

    lines = [
        "# SIKK Live Board",
        "",
        f"- 更新时间：{now or iso_now()}",
        "- 运行状态：正常生成",
        "- 边界：只做持续监控、分析、quote/security、纸面流程和复盘，不执行真实 swap。",
        "",
        "## 1. 系统总览",
        f"- 本轮 Token 数：{len(rows)}",
        f"- WATCHING：{state_counts.get('WATCHING', 0)}",
        f"- PAUSE：{state_counts.get('PAUSE', 0)}",
        f"- BLOCKED：{state_counts.get('BLOCKED', 0)}",
        f"- PAPER_READY：{state_counts.get('PAPER_READY', 0)}",
        f"- PAPER_OPEN：{state_counts.get('PAPER_OPEN', 0)}",
        f"- 钱包结构接入率：{wallet_covered} / {len(rows)}",
        f"- 当前开放仓位：{open_positions}",
        "- 样本可信度：低（以关闭仓位统计为准）",
        "",
        "## 2. 重点机会",
    ]
    lines.extend([token_line(row) for row in opportunity] or ["- 当前无 PAPER_READY / WALLET_SUPPORT token。"])
    lines.extend(["", "## 3. 钱包结构状态"])
    for status in ["WALLET_SUPPORT", "WALLET_PAUSE", "WALLET_BLOCK", "WALLET_NEUTRAL", "MISSING"]:
        lines.append(f"- {status}：{wallet_counts.get(status, 0)}")
    lines.extend(["", "### 钱包结构未接入原因"])
    lines.extend([f"- {reason}：{count}" for reason, count in missing_reasons.most_common()] or ["- 无"])
    lines.extend(["", "## 4. 阻断 / 暂停原因"])
    lines.extend([token_line(row) for row in blocked_pause] or ["- 暂无阻断 / 暂停 token。"])
    lines.extend(["", "## 5. 当前纸面仓位"])
    lines.extend([token_line(row) for row in paper_rows] or ["- 当前无纸面仓位。"])
    lines.extend(["", "## 6. 未入场原因 Top"])
    for key in ["wallet_structure_missing", "wallet_block", "signal_not_ready", "quote_not_ready", "security_not_ready", "paper_runner_not_called", "state_not_ready"]:
        lines.append(f"- {key}：{entry_reasons.get(key, 0)}")
    lines.extend(["", "## 7. 今日纸面验证", f"- 当前开放仓位：{open_positions}", "- 累计关闭仓位：0", "- 已关闭胜率：样本不足", "- 已关闭平均收益：样本不足", "- 样本可信度：低", "", "## 8. 最新事件", "- 事件详见 events/live_events.jsonl"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return str(path)


def run_once(
    *,
    candidates: Iterable[Mapping[str, Any]],
    base_dir: str | Path = DEFAULT_BASE_DIR,
    config: Optional[Mapping[str, Any]] = None,
    module_runner: Callable[..., Mapping[str, Any]] = run_external_modules_for_token,
    force: bool = False,
    now: Optional[str] = None,
) -> Dict[str, str]:
    base = Path(base_dir)
    cfg = dict(config or {})
    cfg.setdefault("base_dir", str(base))
    run_time = now or iso_now()
    statuses: List[Mapping[str, Any]] = []

    for token in candidates:
        process, reason = should_process_token(token, base_dir=base, force=force, now=run_time)
        if not process:
            emit_event(base_dir=base, event_type="TOKEN_SKIPPED", message=reason, token=token, config=cfg, event_time=run_time)
            old = load_existing_token_status(token, base_dir=base)
            if old:
                statuses.append(old)
            continue

        emit_event(base_dir=base, event_type="TOKEN_DISCOVERED", message=f"发现/处理候选 {_token_symbol(token)}", token=token, config=cfg, event_time=run_time)
        module_result = dict(module_runner(token=token, config=cfg, force=force))
        emit_event(base_dir=base, event_type="MODULES_FINISHED", message=f"{_token_symbol(token)} 模块调用完成", token=token, data=module_result, config=cfg, event_time=run_time)
        status = build_token_status(token, module_result, now=run_time)
        write_process_trace(token=token, current_status=status, module_result=module_result, base_dir=base)
        write_token_status_files(status, base_dir=base)
        statuses.append(status)

    live_state = write_live_state(statuses, base_dir=base, now=run_time)
    live_board = write_live_board(statuses, base_dir=base, now=run_time)
    dashboard = write_dashboard(base_dir=base)
    latest_events = write_latest_events_md(base_dir=base)
    return {"live_state_json": live_state, "live_board_md": live_board, "live_dashboard_html": dashboard, "latest_events_md": latest_events, "events_jsonl": str(base / "events" / "live_events.jsonl")}


def load_candidates_from_file(path: str | Path) -> List[Dict[str, Any]]:
    payload = _read_json(Path(path))
    rows = payload.get("候选列表") or payload.get("candidates") or payload.get("tokens") or []
    return rows if isinstance(rows, list) else []


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SIKK Live Runtime v0.2")
    parser.add_argument("--mode", choices=["once", "loop"], default="once")
    parser.add_argument("--candidates", default="data/gmgn_candidates_live_run/gmgn_new_token_filter/token_candidates.json")
    parser.add_argument("--base-dir", default=str(DEFAULT_BASE_DIR))
    parser.add_argument("--interval-sec", type=int, default=600)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    while True:
        candidates = load_candidates_from_file(args.candidates)
        paths = run_once(candidates=candidates, base_dir=args.base_dir, force=args.force)
        print(json.dumps(paths, ensure_ascii=False, indent=2))
        if args.mode == "once":
            break
        time.sleep(args.interval_sec)


if __name__ == "__main__":
    main()
