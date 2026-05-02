#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK System Audit v0.1.

只读系统审计层：扫描 live run 根目录与既有候选/状态机/钱包结构/纸面交易/dashboard
输出，汇总缺失文件、缺失字段、模块成功/失败/跳过数量、卡住 token、钱包结构降级、
状态机冲突、dashboard/复盘缺字段与下一步建议。

安全边界：本模块不采集、不报价、不交易、不签名、不广播，只读取本地文件并写审计报告。
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence

DEFAULT_LIVE_RUN_DIR = Path("data/gmgn_candidates_live_run")

CANDIDATE_FIELDS = ["代币地址"]
STATE_FIELDS = ["代币地址", "当前状态", "状态原因"]
WALLET_FIELDS = [
    "token_address",
    "wallet_structure_status",
    "wallet_structure_score",
    "wallet_gate_result",
    "paper_gate_effect",
    "reason_codes",
    "data_quality_status",
]
DASHBOARD_FIELDS = [
    "discovered_at",
    "discovery_market_cap_usd",
    "first_signal_at",
    "wallet_decision_at",
    "paper_entry_at",
    "paper_entry_market_cap_usd",
    "current_market_cap_usd",
    "current_price",
    "exit_monitor_at",
    "paper_exit_at",
    "exit_reason",
    "failure_attribution_type",
]
REPLAY_FIELDS = [
    "entry_time",
    "entry_price",
    "exit_time",
    "exit_price",
    "exit_reason",
    "paper_entry_market_cap_usd",
    "current_market_cap_usd",
    "failure_type",
    "failure_reason",
]
STUCK_STATES = {"DISCOVERED", "WATCHING", "ACCUMULATING", "READY_TO_BUY", "PAPER_READY", "READY_FOR_CONFIRMATION"}
TERMINAL_STATES = {"BLOCKED", "FAILED", "EXITED", "PAPER_OPEN", "PAPER_EXITED"}


def _utc_now_text() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _read_json(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # defensive audit path
        return {"__read_error__": str(exc)}


def _read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    rows: List[Dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            item = json.loads(line)
            if isinstance(item, dict):
                rows.append(item)
        except Exception:
            rows.append({"__read_error__": line[:200]})
    return rows


def _read_csv(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    try:
        with path.open(encoding="utf-8-sig", newline="") as f:
            return [dict(row) for row in csv.DictReader(f)]
    except Exception as exc:
        return [{"__read_error__": str(exc)}]


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _token(row: Mapping[str, Any]) -> str:
    return str(
        row.get("代币地址")
        or row.get("token_address")
        or row.get("token")
        or row.get("address")
        or row.get("mint")
        or ""
    )


def _symbol(row: Mapping[str, Any]) -> str:
    return str(row.get("代币符号") or row.get("token_symbol") or row.get("symbol") or "")


def _rows_from_payload(payload: Any, keys: Sequence[str]) -> List[Dict[str, Any]]:
    if payload is None:
        return []
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if not isinstance(payload, dict):
        return []
    for key in keys:
        rows = payload.get(key)
        if isinstance(rows, list):
            return [row for row in rows if isinstance(row, dict)]
    return []


def _missing_fields(row: Mapping[str, Any], fields: Sequence[str]) -> List[str]:
    return [field for field in fields if row.get(field) in (None, "", [])]


def _module_status(rows: Iterable[Mapping[str, Any]]) -> Dict[str, int]:
    counts = Counter({"success": 0, "failed": 0, "skipped": 0})
    for row in rows:
        text = " ".join(str(row.get(k, "")) for k in ["状态", "status", "当前状态", "final_status", "结果", "result", "原因"])
        upper = text.upper()
        if any(mark in upper for mark in ["SKIP", "跳过", "NO_INPUT"]):
            counts["skipped"] += 1
        elif any(mark in upper for mark in ["FAIL", "ERROR", "FAILED", "BLOCK", "失败"]):
            counts["failed"] += 1
        else:
            counts["success"] += 1
    return dict(counts)


def _existing_first(base: Path, names: Sequence[str]) -> Path:
    for name in names:
        p = base / name
        if p.exists():
            return p
    return base / names[0]


def _candidate_file(base: Path) -> Path:
    return _existing_first(base, [
        "candidate_pool/token_candidates.json",
        "token_candidates.json",
        "candidates/token_candidates.json",
        "filter/token_candidates.json",
        "candidate_outputs/token_candidates.json",
    ])


def _state_file(base: Path) -> Path:
    return _existing_first(base, ["state_machine/candidate_states.json", "candidate_states.json"])


def _kline_file(base: Path) -> Path:
    return _existing_first(base, ["kline/candidate_kline_pipeline_summary.json", "candidate_kline_pipeline_summary.json"])


def _signal_file(base: Path) -> Path:
    return _existing_first(base, ["signals/candidate_signal_summary.json", "candidate_signal_summary.json"])


def _quote_file(base: Path) -> Path:
    return _existing_first(base, ["quote_security/candidate_quote_security_summary.json", "candidate_quote_security_summary.json"])


def _wallet_file(base: Path) -> Path:
    return _existing_first(base, [
        "wallet_structure/candidate_wallet_structure_summary.json",
        "candidate_wallet_structure_summary.json",
        "wallet_structure_decision.json",
    ])


def _paper_dir(base: Path) -> Path:
    p = base / "paper_live"
    return p if p.exists() else base


def _dashboard_file(base: Path) -> Path:
    return _existing_first(base, ["live_state.json", "dashboard/live_state.json"])


def _collect_wallet_rows(base: Path, summary_payload: Any) -> List[Dict[str, Any]]:
    rows = _rows_from_payload(summary_payload, ["处理结果", "wallet_structure_results", "results", "decisions"])
    if rows:
        return rows
    root = base / "wallet_structure"
    if not root.exists():
        return []
    out: List[Dict[str, Any]] = []
    for path in sorted(root.glob("**/wallet_structure_decision.json")):
        payload = _read_json(path)
        if isinstance(payload, dict):
            row = dict(payload)
            row.setdefault("token_address", path.parent.name)
            out.append(row)
    return out


def _detect_state_conflicts(state_rows: Sequence[Mapping[str, Any]], paper_open: Sequence[Mapping[str, Any]], paper_closed: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    conflicts: List[Dict[str, Any]] = []
    state_by_token = {_token(row): row for row in state_rows if _token(row)}
    open_tokens = {_token(row) for row in paper_open if _token(row)}
    closed_tokens = {_token(row) for row in paper_closed if _token(row)}
    for token in sorted(open_tokens):
        state = str(state_by_token.get(token, {}).get("当前状态") or state_by_token.get(token, {}).get("current_state") or "")
        if state in {"BLOCKED", "FAILED", "EXITED"}:
            conflicts.append({"token": token, "conflict": "open_position_with_terminal_state", "state": state})
    for token in sorted(closed_tokens & open_tokens):
        conflicts.append({"token": token, "conflict": "token_in_open_and_closed_positions"})
    for token, row in state_by_token.items():
        state = str(row.get("当前状态") or row.get("current_state") or "")
        reason = str(row.get("状态原因") or row.get("latest_reason") or "")
        if state == "PAPER_READY" and token not in open_tokens and "阻断" in reason:
            conflicts.append({"token": token, "conflict": "paper_ready_with_block_reason", "reason": reason})
    return conflicts


def _dashboard_missing(live_state_payload: Any) -> Dict[str, Any]:
    tokens = _rows_from_payload(live_state_payload, ["tokens", "候选状态"])
    per_token = []
    missing_counter: Counter[str] = Counter()
    for row in tokens:
        missing = _missing_fields(row, DASHBOARD_FIELDS)
        nested = {
            "wallet_structure_status": (row.get("wallet_structure") or {}).get("wallet_structure_status") if isinstance(row.get("wallet_structure"), dict) else row.get("wallet_structure_status"),
            "signal_level": (row.get("signal") or {}).get("signal_level") if isinstance(row.get("signal"), dict) else row.get("signal_level"),
            "paper_status": (row.get("paper") or {}).get("paper_status") if isinstance(row.get("paper"), dict) else row.get("paper_status"),
        }
        for key, value in nested.items():
            if value in (None, "", []):
                missing.append(key)
        missing_counter.update(missing)
        if missing:
            per_token.append({"token": _token(row), "symbol": _symbol(row), "missing_fields": missing})
    return {"token_count": len(tokens), "missing_field_counts": dict(missing_counter), "tokens_with_missing_fields": per_token[:50]}


def _replay_unavailable(open_rows: Sequence[Mapping[str, Any]], closed_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    rows = list(open_rows) + list(closed_rows)
    per_token = []
    counter: Counter[str] = Counter()
    for row in rows:
        missing = _missing_fields(row, REPLAY_FIELDS)
        counter.update(missing)
        if missing:
            per_token.append({"token": _token(row), "symbol": _symbol(row), "missing_fields": missing})
    if not failure_rows:
        counter["failure_attribution_events"] += 1
    return {"missing_field_counts": dict(counter), "positions_with_unavailable_replay_fields": per_token[:50], "failure_attribution_event_count": len(failure_rows)}


def _recommendations(payload: Mapping[str, Any]) -> List[str]:
    recs: List[str] = []
    if payload["missing_files"]:
        recs.append("补齐 live run 标准输出目录：候选池、K线、信号、状态机、钱包结构、quote/security、paper_live、live_state/dashboard。")
    if payload["missing_fields"]:
        recs.append("按审计列出的 missing_fields 修补上游输出合约，字段缺失时显式写 DEGRADED/MISSING 而不是空值。")
    if payload["stuck_tokens"]:
        recs.append("优先排查卡住 token：确认其 K线/信号/quote/security/wallet 决策是否缺失或被跳过。")
    if payload["wallet_bypass_or_degraded"]:
        recs.append("修复钱包结构旁路/降级：标准化 wallet_structure_decision.json 并保留 reason_codes/data_quality_status。")
    if payload["state_machine_conflicts"]:
        recs.append("处理状态机冲突：开放纸面仓位不得同时处于 BLOCKED/FAILED/EXITED，关闭与开放仓位索引需去重。")
    if payload["dashboard_missing_fields"].get("missing_field_counts"):
        recs.append("升级 dashboard live_state 事件级字段，覆盖发现→判断→入场→持仓→退出。")
    if payload["replay_unavailable_fields"].get("missing_field_counts"):
        recs.append("补齐复盘字段：市值、入场/退出时间价格、failure_type/failure_reason。")
    if not recs:
        recs.append("当前 fake/live 输出未发现阻断级审计问题，继续保持 paper-only 并接入解释层复核。")
    recs.append("保持 paper-only：审计层不得调用采集、gmgn_swap/gmgn_cooking、交易广播或 yolo。")
    return recs


def _markdown(payload: Mapping[str, Any]) -> str:
    lines = [
        "# SIKK 系统审计报告",
        "",
        f"- 审计时间：{payload['audit_time']}",
        f"- live run 根目录：`{payload['live_run_dir']}`",
        "- 安全边界：只读审计；不采集、不交易、不签名、不广播。",
        f"- 当前候选数：{payload['candidate_count']}",
        "",
        "## 模块统计",
    ]
    for name, counts in payload["module_counts"].items():
        lines.append(f"- {name}：success={counts.get('success', 0)} failed={counts.get('failed', 0)} skipped={counts.get('skipped', 0)}")
    lines.extend(["", "## 缺失文件"])
    lines.extend([f"- `{p}`" for p in payload["missing_files"]] or ["- 无"])
    lines.extend(["", "## 缺失字段"])
    if payload["missing_fields"]:
        for item in payload["missing_fields"][:80]:
            lines.append(f"- {item['scope']} {item.get('token', '')}：{', '.join(item['missing_fields'])}")
    else:
        lines.append("- 无")
    lines.extend(["", "## 卡住 token"])
    lines.extend([f"- {x.get('symbol','')} `{x.get('token','')}` state={x.get('state')} reason={x.get('reason','')}" for x in payload["stuck_tokens"]] or ["- 无"])
    lines.extend(["", "## 钱包结构旁路/降级"])
    lines.extend([f"- `{x.get('token','')}` status={x.get('status','')} effect={x.get('effect','')} reason={x.get('reason','')}" for x in payload["wallet_bypass_or_degraded"]] or ["- 无"])
    lines.extend(["", "## 状态机冲突"])
    lines.extend([f"- `{x.get('token','')}` {x.get('conflict')} {x.get('state','')} {x.get('reason','')}" for x in payload["state_machine_conflicts"]] or ["- 无"])
    lines.extend(["", "## Dashboard 缺字段", f"- token_count：{payload['dashboard_missing_fields'].get('token_count', 0)}"])
    for key, value in sorted(payload["dashboard_missing_fields"].get("missing_field_counts", {}).items()):
        lines.append(f"- {key}：{value}")
    if not payload["dashboard_missing_fields"].get("missing_field_counts"):
        lines.append("- 无")
    lines.extend(["", "## 复盘不可用字段"])
    for key, value in sorted(payload["replay_unavailable_fields"].get("missing_field_counts", {}).items()):
        lines.append(f"- {key}：{value}")
    if not payload["replay_unavailable_fields"].get("missing_field_counts"):
        lines.append("- 无")
    lines.extend(["", "## 下一步建议"])
    lines.extend([f"- {rec}" for rec in payload["recommendations"]])
    return "\n".join(lines) + "\n"


def run_system_audit(*, live_run_dir: str | Path = DEFAULT_LIVE_RUN_DIR, output_dir: str | Path | None = None) -> Dict[str, str]:
    base = Path(live_run_dir)
    out = Path(output_dir) if output_dir else base
    paths = {
        "candidates": _candidate_file(base),
        "kline": _kline_file(base),
        "signals": _signal_file(base),
        "quote_security": _quote_file(base),
        "state_machine": _state_file(base),
        "wallet_structure": _wallet_file(base),
        "live_state": _dashboard_file(base),
        "dashboard_html": base / "live_dashboard.html",
        "paper_open": _paper_dir(base) / "paper_positions_open.json",
        "paper_closed": _paper_dir(base) / "paper_positions_closed.json",
        "paper_metrics": _paper_dir(base) / "strategy_metrics.json",
        "failure_attribution": _paper_dir(base) / "failure_attribution.jsonl",
    }
    missing_files = [str(path) for path in paths.values() if not path.exists()]

    candidates_payload = _read_json(paths["candidates"])
    kline_payload = _read_json(paths["kline"])
    signal_payload = _read_json(paths["signals"])
    quote_payload = _read_json(paths["quote_security"])
    state_payload = _read_json(paths["state_machine"])
    wallet_payload = _read_json(paths["wallet_structure"])
    live_state_payload = _read_json(paths["live_state"])
    paper_open_payload = _read_json(paths["paper_open"])
    paper_closed_payload = _read_json(paths["paper_closed"])
    paper_metrics_payload = _read_json(paths["paper_metrics"])

    candidate_rows = _rows_from_payload(candidates_payload, ["候选结果", "候选列表", "tokens", "candidates", "results"])
    kline_rows = _rows_from_payload(kline_payload, ["处理结果", "results"])
    signal_rows = _rows_from_payload(signal_payload, ["信号结果", "results"])
    signal_skipped = _rows_from_payload(signal_payload, ["跳过结果", "skipped"])
    quote_rows = _rows_from_payload(quote_payload, ["处理结果", "results"])
    state_rows = _rows_from_payload(state_payload, ["候选状态", "states", "tokens"])
    wallet_rows = _collect_wallet_rows(base, wallet_payload)
    open_rows = _rows_from_payload(paper_open_payload, ["open_positions"])
    closed_rows = _rows_from_payload(paper_closed_payload, ["closed_positions"])
    failure_rows = _read_jsonl(paths["failure_attribution"])

    missing_fields: List[Dict[str, Any]] = []
    for scope, rows, fields in [
        ("candidate", candidate_rows, CANDIDATE_FIELDS),
        ("state_machine", state_rows, STATE_FIELDS),
        ("wallet_structure", wallet_rows, WALLET_FIELDS),
    ]:
        for row in rows:
            missing = _missing_fields(row, fields)
            if missing:
                missing_fields.append({"scope": scope, "token": _token(row), "missing_fields": missing})

    module_counts = {
        "candidates": {"success": len(candidate_rows), "failed": 0, "skipped": 0},
        "kline": _module_status(kline_rows),
        "signals": _module_status(signal_rows + signal_skipped),
        "quote_security": _module_status(quote_rows),
        "state_machine": _module_status(state_rows),
        "wallet_structure": _module_status(wallet_rows),
        "paper_runner": dict((paper_metrics_payload or {}).get("统计", {})) if isinstance(paper_metrics_payload, dict) and paper_metrics_payload.get("统计") else {"success": len(open_rows) + len(closed_rows), "failed": len(_read_jsonl(_paper_dir(base) / "risk_events.jsonl")), "skipped": 0},
    }

    stuck_tokens = []
    for row in state_rows:
        state = str(row.get("当前状态") or row.get("current_state") or "")
        if state in STUCK_STATES:
            stuck_tokens.append({"token": _token(row), "symbol": _symbol(row), "state": state, "reason": row.get("状态原因") or row.get("latest_reason") or ""})

    wallet_bypass_or_degraded = []
    for row in wallet_rows + state_rows:
        status = str(row.get("wallet_structure_status") or row.get("钱包结构结论") or row.get("data_quality_status") or "")
        effect = str(row.get("wallet_gate_effect") or row.get("paper_gate_effect") or row.get("钱包门禁效果") or "")
        reason = row.get("reason") or row.get("钱包结构原因") or row.get("降级原因") or row.get("reason_codes") or ""
        if any(x in (status + effect).upper() for x in ["MISSING", "DEGRADED", "NO_WALLET_INPUT", "BYPASS", "未接入"]):
            wallet_bypass_or_degraded.append({"token": _token(row), "status": status, "effect": effect, "reason": reason})

    payload: Dict[str, Any] = {
        "audit_time": _utc_now_text(),
        "live_run_dir": str(base),
        "paper_only": True,
        "readonly_note": "只读系统审计；不采集、不交易、不调用 gmgn_swap/gmgn_cooking、不广播、不 yolo。",
        "input_paths": {key: str(value) for key, value in paths.items()},
        "candidate_count": len(candidate_rows) if candidate_rows else len(state_rows),
        "module_counts": module_counts,
        "missing_files": missing_files,
        "missing_fields": missing_fields,
        "stuck_tokens": stuck_tokens,
        "wallet_bypass_or_degraded": wallet_bypass_or_degraded,
        "state_machine_conflicts": _detect_state_conflicts(state_rows, open_rows, closed_rows),
        "dashboard_missing_fields": _dashboard_missing(live_state_payload),
        "replay_unavailable_fields": _replay_unavailable(open_rows, closed_rows, failure_rows),
    }
    payload["recommendations"] = _recommendations(payload)

    json_path = out / "system_audit.json"
    md_path = out / "system_audit.md"
    _write_json(json_path, payload)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(_markdown(payload), encoding="utf-8")
    return {"system_audit_json": str(json_path), "system_audit_md": str(md_path)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SIKK 只读系统审计层")
    parser.add_argument("--live-run-dir", default=str(DEFAULT_LIVE_RUN_DIR))
    parser.add_argument("--output-dir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = run_system_audit(live_run_dir=args.live_run_dir, output_dir=args.output_dir)
    print(json.dumps(paths, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
