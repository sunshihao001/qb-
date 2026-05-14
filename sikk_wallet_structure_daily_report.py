#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK 钱包结构纸面交易日报。

汇总 paper runner 输出的关闭仓位与 failure_attribution，按钱包结构状态、失败归因、
钱包结构状态 × 信号等级统计胜率/收益/回撤。只用于纸面复盘，不执行真实 swap。
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median
from typing import Any, Dict, Iterable, List, Mapping


def _num(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, ""):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _read_csv(path: str | Path) -> List[Dict[str, Any]]:
    p = Path(path)
    if not p.exists():
        return []
    with p.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(row) for row in csv.DictReader(f)]


def _read_jsonl(path: str | Path) -> List[Dict[str, Any]]:
    p = Path(path)
    if not p.exists():
        return []
    rows: List[Dict[str, Any]] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_csv(path: Path, rows: Iterable[Mapping[str, Any]]) -> None:
    rows = [dict(row) for row in rows]
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    if not fieldnames:
        fieldnames = ["统计类型", "分组", "关闭仓位数", "胜率_pct", "平均收益率_pct"]
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _closed_return(row: Mapping[str, Any]) -> float:
    return _num(row.get("最终收益率_pct") or row.get("net_pnl_pct") or row.get("收益率_pct"), 0.0)


def _wallet_status(row: Mapping[str, Any]) -> str:
    return str(row.get("wallet_structure_status") or row.get("钱包结构结论") or "UNKNOWN")


def _signal_level(row: Mapping[str, Any]) -> str:
    return str(row.get("signal_level") or row.get("信号等级") or "UNKNOWN")


def _failure_type(row: Mapping[str, Any]) -> str:
    return str(row.get("failure_type") or row.get("exit_reason") or row.get("出场原因") or "UNKNOWN")


def _position_size(row: Mapping[str, Any]) -> float:
    return _num(row.get("paper_position_sol") or row.get("paper_size_sol") or row.get("position_sol") or row.get("模拟仓位SOL"), 0.0)


def _token(row: Mapping[str, Any]) -> str:
    return str(row.get("token_address") or row.get("代币地址") or row.get("token") or row.get("address") or row.get("mint") or "")


def _audit_statistics(closed_rows: List[Mapping[str, Any]], failure_rows: List[Mapping[str, Any]]) -> Dict[str, Any]:
    tokens = [_token(row) for row in closed_rows if _token(row)]
    token_counter = Counter(tokens)
    duplicates = {token: count for token, count in token_counter.items() if count > 1}
    weighted_num = 0.0
    weighted_den = 0.0
    for row in closed_rows:
        size = _position_size(row)
        if size <= 0:
            size = 1.0
        weighted_num += _closed_return(row) * size
        weighted_den += size
    force_events = [row for row in failure_rows if str(row.get("事件类型") or row.get("event_type") or row.get("recommended_paper_action") or "").upper() == "FORCE_PAPER_EXIT"]
    exit_counter = Counter(_failure_type(row) for row in closed_rows)
    shadow_ready = [row for row in closed_rows if any(row.get(k) not in (None, "") for k in ["shadow_hold_price_15m", "shadow_hold_price_30m", "shadow_hold_price_60m", "missed_profit_pct", "avoided_drawdown_pct"])]
    return {
        "样本独立性审计": {
            "position_count": len(closed_rows),
            "unique_token_count": len(token_counter),
            "duplicate_token_count": len(duplicates),
            "duplicate_tokens": duplicates,
            "audit_note": "同一 token 多笔重复会抬高统计权重，策略结论应优先看 unique token 与分桶表现。",
        },
        "加权收益审计": {
            "position_size_weighted_return_pct": round(weighted_num / weighted_den, 4) if weighted_den else 0.0,
            "weight_source": "paper_position_sol/paper_size_sol/position_sol；缺失时按 1 等权。",
        },
        "退出政策审计": {
            "force_paper_exit_count": len(force_events),
            "force_paper_exit_rate_pct": round(len(force_events) / len(closed_rows) * 100.0, 4) if closed_rows else 0.0,
            "exit_reason_counts": dict(sorted(exit_counter.items())),
            "audit_note": "FORCE_PAPER_EXIT 过多时必须复查是否从 EXIT_MONITOR 过早升级。",
        },
        "shadow_hold审计": {
            "shadow_hold_ready_count": len(shadow_ready),
            "shadow_hold_missing_count": max(len(closed_rows) - len(shadow_ready), 0),
            "audit_note": "force exit 后应跟踪 shadow hold 15m/30m/60m，判断错杀右尾或规避回撤。",
        },
    }


def _summarize(rows: List[Mapping[str, Any]]) -> Dict[str, Any]:
    returns = [_closed_return(row) for row in rows]
    pnl_sols = [_num(row.get("net_pnl_sol") or row.get("收益SOL"), 0.0) for row in rows]
    max_floating = [_num(row.get("最大浮盈_pct"), 0.0) for row in rows]
    max_drawdown = [_num(row.get("最大浮亏_pct") or row.get("max_drawdown_pct"), 0.0) for row in rows]
    wins = [value for value in returns if value > 0]
    if not rows:
        return {
            "关闭仓位数": 0,
            "盈利仓位数": 0,
            "胜率_pct": 0.0,
            "平均收益率_pct": 0.0,
            "中位数收益率_pct": 0.0,
            "总收益SOL": 0.0,
            "平均最大浮盈_pct": 0.0,
            "平均最大浮亏_pct": 0.0,
            "最佳单笔_pct": 0.0,
            "最差单笔_pct": 0.0,
        }
    return {
        "关闭仓位数": len(rows),
        "盈利仓位数": len(wins),
        "胜率_pct": round(len(wins) / len(rows) * 100.0, 4),
        "平均收益率_pct": round(mean(returns), 4),
        "中位数收益率_pct": round(median(returns), 4),
        "总收益SOL": round(sum(pnl_sols), 8),
        "平均最大浮盈_pct": round(mean(max_floating), 4) if max_floating else 0.0,
        "平均最大浮亏_pct": round(mean(max_drawdown), 4) if max_drawdown else 0.0,
        "最佳单笔_pct": round(max(returns), 4),
        "最差单笔_pct": round(min(returns), 4),
    }


def _group_summary(rows: List[Mapping[str, Any]], key_fn) -> Dict[str, Dict[str, Any]]:
    groups: Dict[str, List[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[str(key_fn(row))].append(row)
    return {key: _summarize(list(value)) for key, value in sorted(groups.items())}


def _flatten_summary(summary: Mapping[str, Dict[str, Any]], stat_type: str) -> List[Dict[str, Any]]:
    rows = []
    for group, metrics in summary.items():
        rows.append({"统计类型": stat_type, "分组": group, **metrics})
    return rows


def _write_md(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# SIKK 钱包结构纸面交易日报",
        "",
        f"- 报告日期：{payload.get('报告日期')}",
        "- 边界：本报告只统计纸面交易、钱包结构变化和失败归因，不执行真实 swap。",
        "",
        "## 总体统计",
    ]
    total = payload.get("总体统计", {})
    for key, value in total.items():
        lines.append(f"- {key}：{value}")

    def append_group(title: str, section: Mapping[str, Any]) -> None:
        lines.extend(["", f"## {title}"])
        if not section:
            lines.append("- 暂无数据")
            return
        for group, metrics in section.items():
            lines.append(f"- {group}")
            lines.append(f"  - 关闭仓位数：{metrics.get('关闭仓位数', 0)}")
            lines.append(f"  - 胜率：{metrics.get('胜率_pct', 0)}%")
            lines.append(f"  - 平均收益率：{metrics.get('平均收益率_pct', 0)}%")
            lines.append(f"  - 平均最大浮亏：{metrics.get('平均最大浮亏_pct', 0)}%")

    append_group("按钱包结构状态统计", payload.get("按钱包结构状态", {}))
    append_group("按失败归因统计", payload.get("按失败归因", {}))
    append_group("按钱包结构状态与信号等级统计", payload.get("按钱包结构状态与信号等级", {}))

    lines.extend(["", "## failure_attribution 事件统计"])
    events = payload.get("failure_attribution事件统计", {})
    if not events:
        lines.append("- 暂无事件")
    else:
        for key, value in events.items():
            lines.append(f"- {key}：{value}")

    lines.extend(["", "## 审计统计"])
    audit = payload.get("审计统计", {})
    for title, metrics in audit.items():
        lines.append(f"- {title}")
        if isinstance(metrics, Mapping):
            for key, value in metrics.items():
                lines.append(f"  - {key}：{value}")
        else:
            lines.append(f"  - {metrics}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_wallet_structure_daily_report(
    *,
    closed_positions_path: str | Path,
    failure_attribution_path: str | Path,
    output_dir: str | Path,
    report_date: str,
) -> Dict[str, str]:
    closed_rows = _read_csv(closed_positions_path)
    failure_rows = _read_jsonl(failure_attribution_path)

    by_wallet = _group_summary(closed_rows, _wallet_status)
    by_failure = _group_summary(closed_rows, _failure_type)
    by_wallet_signal = _group_summary(closed_rows, lambda row: f"{_wallet_status(row)}|{_signal_level(row)}")
    failure_counter = Counter(str(row.get("failure_type") or "UNKNOWN") for row in failure_rows)

    payload = {
        "报告日期": report_date,
        "总体统计": _summarize(closed_rows),
        "按钱包结构状态": by_wallet,
        "按失败归因": by_failure,
        "按钱包结构状态与信号等级": by_wallet_signal,
        "failure_attribution事件统计": dict(sorted(failure_counter.items())),
        "审计统计": _audit_statistics(closed_rows, failure_rows),
        "说明": "只统计纸面交易与钱包结构失败归因，不执行真实 swap。",
    }

    out = Path(output_dir)
    summary_json = out / f"wallet_structure_daily_report_{report_date}.json"
    summary_csv = out / f"wallet_structure_daily_report_{report_date}.csv"
    summary_md = out / f"wallet_structure_daily_report_{report_date}.md"

    flat_rows: List[Dict[str, Any]] = []
    flat_rows.extend(_flatten_summary(by_wallet, "wallet_structure_status"))
    flat_rows.extend(_flatten_summary(by_failure, "failure_type"))
    flat_rows.extend(_flatten_summary(by_wallet_signal, "wallet_structure_status_x_signal_level"))

    _write_json(summary_json, payload)
    _write_csv(summary_csv, flat_rows)
    _write_md(summary_md, payload)
    return {"summary_json": str(summary_json), "summary_csv": str(summary_csv), "summary_md": str(summary_md)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SIKK 钱包结构纸面交易日报")
    parser.add_argument("--closed-positions", default="data/gmgn_candidates_live_run/paper_live/paper_positions_closed.csv")
    parser.add_argument("--failure-attribution", default="data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl")
    parser.add_argument("--output-dir", default="data/gmgn_candidates_live_run/reports")
    parser.add_argument("--report-date", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = build_wallet_structure_daily_report(
        closed_positions_path=args.closed_positions,
        failure_attribution_path=args.failure_attribution,
        output_dir=args.output_dir,
        report_date=args.report_date,
    )
    print(json.dumps(paths, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
