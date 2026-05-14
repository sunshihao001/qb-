#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK Runtime static HTML dashboard builder."""

from __future__ import annotations

import csv
import html
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping

DEFAULT_BASE_DIR = Path("data/gmgn_candidates_live_run")


def _read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path, limit: int | None = None) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    rows: List[Dict[str, Any]] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    if limit is not None:
        lines = lines[-limit:]
    for line in lines:
        try:
            row = json.loads(line)
        except Exception:
            continue
        if isinstance(row, dict):
            rows.append(row)
    return rows


def _read_csv_rows(path: Path) -> List[Dict[str, Any]]:
    if not path.exists() or not path.read_text(encoding="utf-8-sig").strip():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(row) for row in csv.DictReader(f)]


def _read_events(base_dir: Path, limit: int = 40) -> List[Dict[str, Any]]:
    path = base_dir / "events" / "live_events.jsonl"
    return _read_jsonl(path, limit=limit)


def _esc(value: Any) -> str:
    return html.escape(str(value if value is not None else ""))


def _token_key(row: Mapping[str, Any]) -> str:
    return str(row.get("token_address") or row.get("代币地址") or row.get("token") or row.get("address") or "")


def _index_by_token(rows: Iterable[Mapping[str, Any]]) -> Dict[str, Dict[str, Any]]:
    indexed: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        token = _token_key(row)
        if token:
            indexed[token] = dict(row)
    return indexed


def _paper_indexes(base_dir: Path) -> Dict[str, Dict[str, Dict[str, Any]]]:
    paper_dir = base_dir / "paper_live"
    open_payload = _read_json(paper_dir / "paper_positions_open.json")
    closed_payload = _read_json(paper_dir / "paper_positions_closed.json")
    open_rows = open_payload.get("open_positions", []) if isinstance(open_payload.get("open_positions", []), list) else []
    closed_rows = closed_payload.get("closed_positions", []) if isinstance(closed_payload.get("closed_positions", []), list) else []
    if not closed_rows:
        closed_rows = _read_csv_rows(paper_dir / "paper_positions_closed.csv")
    failure_rows = _read_jsonl(paper_dir / "failure_attribution.jsonl")
    return {"open": _index_by_token(open_rows), "closed": _index_by_token(closed_rows), "failure": _index_by_token(failure_rows)}


def _pick(*sources: Mapping[str, Any], keys: Iterable[str]) -> Any:
    for source in sources:
        if not isinstance(source, Mapping):
            continue
        for key in keys:
            value = source.get(key)
            if value is not None and value != "":
                return value
    return None


def _display(value: Any) -> str:
    return _esc(value if value is not None and value != "" else "待补")


def _fmt_money(value: Any) -> str:
    if value is None or value == "":
        return "待补"
    try:
        return f"${float(value):,.4f}"
    except (TypeError, ValueError):
        return _esc(value)


def _fmt_pct(value: Any) -> str:
    if value is None or value == "":
        return "待补"
    try:
        return f"{float(value):.4f}%"
    except (TypeError, ValueError):
        return _esc(value)


def _event_fields(token: Mapping[str, Any], paper_open: Mapping[str, Any], paper_closed: Mapping[str, Any], failure: Mapping[str, Any]) -> Dict[str, Any]:
    wallet = token.get("wallet_structure", {}) if isinstance(token.get("wallet_structure", {}), Mapping) else {}
    signal = token.get("signal", {}) if isinstance(token.get("signal", {}), Mapping) else {}
    quote = token.get("quote", {}) if isinstance(token.get("quote", {}), Mapping) else {}
    paper = token.get("paper", {}) if isinstance(token.get("paper", {}), Mapping) else {}
    okx_cluster = token.get("okx_cluster", {}) if isinstance(token.get("okx_cluster", {}), Mapping) else {}
    source = paper_open or paper_closed
    monitor_action = _pick(token, paper, source, failure, keys=("wallet_position_action", "事件类型"))
    return {
        "discovered_at": _pick(token, keys=("discovered_at", "发现时间", "created_at", "last_update")),
        "discovery_market_cap_usd": _pick(token, keys=("discovery_market_cap_usd", "发现市值USD", "initial_market_cap_usd", "market_cap_usd")),
        "discovery_liquidity_usd": _pick(token, keys=("discovery_liquidity_usd", "发现流动性USD", "liquidity_usd")),
        "first_signal_at": _pick(token, signal, source, keys=("first_signal_at", "信号时间", "signal_time", "entry_time")),
        "first_signal_type": _pick(token, signal, source, keys=("first_signal_type", "信号类型", "策略类型", "strategy_type", "signal_level")),
        "signal_market_cap_usd": _pick(token, signal, keys=("signal_market_cap_usd", "信号市值USD", "market_cap_usd")),
        "wallet_decision_at": _pick(token, wallet, keys=("wallet_decision_at", "钱包决策时间", "decision_time", "last_update")),
        "wallet_decision_market_cap_usd": _pick(token, wallet, keys=("wallet_decision_market_cap_usd", "钱包决策市值USD", "market_cap_usd")),
        "wallet_structure_status": _pick(token, wallet, source, keys=("wallet_structure_status", "钱包结构结论")),
        "paper_entry_at": _pick(token, paper, source, keys=("paper_entry_at", "entry_time", "入场时间")),
        "paper_entry_market_cap_usd": _pick(token, paper, source, keys=("paper_entry_market_cap_usd", "入场市值USD", "entry_market_cap_usd")),
        "paper_entry_price": _pick(token, paper, source, keys=("paper_entry_price", "entry_price", "入场价格")),
        "paper_entry_amount_sol": _pick(token, paper, source, keys=("paper_entry_amount_sol", "position_sol", "仓位SOL", "建议纸面仓位SOL")),
        "paper_entry_amount_usd": _pick(token, paper, source, keys=("paper_entry_amount_usd", "position_usd", "仓位USD")),
        "paper_token_amount": _pick(token, paper, source, keys=("paper_token_amount", "token_amount", "代币数量")),
        "current_market_cap_usd": _pick(token, quote, paper, source, keys=("current_market_cap_usd", "当前市值USD", "market_cap_usd")),
        "current_price": _pick(token, quote, paper, source, keys=("current_price", "last_price", "price", "当前价格")),
        "unrealized_pnl_sol": _pick(token, paper, source, keys=("unrealized_pnl_sol", "net_pnl_sol", "未实现收益SOL")),
        "unrealized_pnl_pct": _pick(token, paper, source, keys=("unrealized_pnl_pct", "当前收益率_pct", "live_pnl_pct", "net_pnl_pct", "最终收益率_pct")),
        "exit_monitor_at": _pick(token, paper, source, failure, keys=("exit_monitor_at", "事件时间", "last_update_time")) if monitor_action in {"EXIT_MONITOR", "PAPER_FORCE_EXIT"} else _pick(token, paper, keys=("exit_monitor_at",)),
        "paper_exit_at": _pick(token, paper, paper_closed, keys=("paper_exit_at", "exit_time", "退出时间")),
        "exit_reason": _pick(token, paper, paper_closed, failure, keys=("exit_reason", "退出原因", "failure_reason", "原因")),
        "failure_attribution_type": _pick(token, paper, paper_closed, failure, keys=("failure_attribution_type", "failure_type")),
        "okx_cluster_status": _pick(token, okx_cluster, keys=("okx_cluster_status",)),
        "okx_cluster_score": _pick(token, okx_cluster, keys=("okx_cluster_score",)),
        "okx_cluster_risk_score": _pick(token, okx_cluster, keys=("okx_cluster_risk_score",)),
        "okx_cluster_distribution_score": _pick(token, okx_cluster, keys=("okx_cluster_distribution_score",)),
        "okx_cluster_control_retention_score": _pick(token, okx_cluster, keys=("okx_cluster_control_retention_score",)),
        "largest_cluster_holding_pct": _pick(token, okx_cluster, keys=("largest_cluster_holding_pct",)),
        "top300_total_holding_pct": _pick(token, okx_cluster, keys=("top300_total_holding_pct",)),
        "cluster_holding_pct_delta": _pick(token, okx_cluster, keys=("cluster_holding_pct_delta",)),
        "largest_cluster_holding_pct_delta": _pick(token, okx_cluster, keys=("largest_cluster_holding_pct_delta",)),
    }


def _cls(value: Any) -> str:
    text = str(value or "").upper()
    if text in {"PAPER_OPEN", "PAPER_READY", "READY_FOR_CONFIRMATION", "WALLET_SUPPORT", "PASS", "READY"}:
        return "good"
    if text in {"WATCHING", "PAUSE", "WALLET_PAUSE", "WALLET_NEUTRAL"}:
        return "warn"
    if text in {"BLOCKED", "ERROR", "EXPIRED", "WALLET_BLOCK", "BLOCK"}:
        return "bad"
    return "neutral"


def build_dashboard_html(*, base_dir: str | Path = DEFAULT_BASE_DIR) -> str:
    base = Path(base_dir)
    state = _read_json(base / "live_state.json")
    tokens = state.get("tokens", []) if isinstance(state.get("tokens", []), list) else []
    events = _read_events(base)
    paper_index = _paper_indexes(base)
    counts: Dict[str, int] = {}
    wallet_counts: Dict[str, int] = {}
    for token in tokens:
        current = str(token.get("current_state") or "UNKNOWN")
        counts[current] = counts.get(current, 0) + 1
        wallet = token.get("wallet_structure", {}) if isinstance(token.get("wallet_structure", {}), dict) else {}
        wallet_status = str(wallet.get("wallet_structure_status") or "MISSING")
        wallet_counts[wallet_status] = wallet_counts.get(wallet_status, 0) + 1

    cards = [f'<div class="card"><div class="card-title">{_esc(k)}</div><div class="card-num">{v}</div></div>' for k, v in sorted(counts.items())]
    wallet_options = ''.join(f'<option value="{_esc(k)}">{_esc(k)}</option>' for k in sorted(wallet_counts))
    state_options = ''.join(f'<option value="{_esc(k)}">{_esc(k)}</option>' for k in sorted(counts))
    rows = []
    for token in tokens:
        token_addr = str(token.get('token_address') or '')
        wallet = token.get("wallet_structure", {}) if isinstance(token.get("wallet_structure", {}), dict) else {}
        signal = token.get("signal", {}) if isinstance(token.get("signal", {}), dict) else {}
        quote = token.get("quote", {}) if isinstance(token.get("quote", {}), dict) else {}
        security = token.get("security", {}) if isinstance(token.get("security", {}), dict) else {}
        paper = token.get("paper", {}) if isinstance(token.get("paper", {}), dict) else {}
        event = _event_fields(
            token,
            paper_index["open"].get(token_addr, {}),
            paper_index["closed"].get(token_addr, {}),
            paper_index["failure"].get(token_addr, {}),
        )
        current_state = str(token.get('current_state') or 'UNKNOWN')
        wallet_status = str(wallet.get('wallet_structure_status') or 'MISSING')
        search_text = " ".join(str(v or "") for v in [token.get('token_symbol'), token.get('token_address'), current_state, wallet_status, token.get('latest_reason'), token.get('latest_action')])
        rows.append(
            f"<tr data-state='{_esc(current_state)}' data-wallet='{_esc(wallet_status)}' data-search='{_esc(search_text).lower()}'>"
            f"<td>{_esc(token.get('token_symbol'))}</td>"
            f"<td>{_esc(token.get('token_address'))}</td>"
            f"<td>{_esc(token.get('priority_level'))}</td>"
            f"<td class='{_cls(current_state)}'>{_esc(current_state)}</td>"
            f"<td>{_esc(signal.get('signal_level'))}</td>"
            f"<td>{_esc(signal.get('signal_gate'))}</td>"
            f"<td class='{_cls(wallet_status)}'>{_esc(wallet_status)}</td>"
            f"<td>{_esc(wallet.get('wallet_structure_score'))}</td>"
            f"<td>{_esc(wallet.get('wallet_risk_score'))}</td>"
            f"<td>{_esc(wallet.get('counterparty_pressure_score'))}</td>"
            f"<td>{_esc(wallet.get('data_quality_score'))}</td>"
            f"<td>{_esc(quote.get('quote_gate'))}</td>"
            f"<td>{_esc(security.get('security_gate'))}</td>"
            f"<td>{_esc(paper.get('paper_status'))}</td>"
            f"<td>{_esc(paper.get('unrealized_pnl_pct') or paper.get('net_pnl_pct') or '')}</td>"
            f"<td>{_display(event['discovered_at'])}</td>"
            f"<td>{_fmt_money(event['discovery_market_cap_usd'])}</td>"
            f"<td>{_fmt_money(event['discovery_liquidity_usd'])}</td>"
            f"<td>{_display(event['first_signal_at'])}</td>"
            f"<td>{_display(event['first_signal_type'])}</td>"
            f"<td>{_fmt_money(event['signal_market_cap_usd'])}</td>"
            f"<td>{_display(event['wallet_decision_at'])}</td>"
            f"<td>{_fmt_money(event['wallet_decision_market_cap_usd'])}</td>"
            f"<td>{_display(event['paper_entry_at'])}</td>"
            f"<td>{_fmt_money(event['paper_entry_market_cap_usd'])}</td>"
            f"<td>{_display(event['paper_entry_price'])}</td>"
            f"<td>{_display(event['paper_entry_amount_sol'])}</td>"
            f"<td>{_display(event['paper_entry_amount_usd'])}</td>"
            f"<td>{_display(event['paper_token_amount'])}</td>"
            f"<td>{_fmt_money(event['current_market_cap_usd'])}</td>"
            f"<td>{_display(event['current_price'])}</td>"
            f"<td>{_display(event['unrealized_pnl_sol'])}</td>"
            f"<td>{_fmt_pct(event['unrealized_pnl_pct'])}</td>"
            f"<td>{_display(event['exit_monitor_at'])}</td>"
            f"<td>{_display(event['paper_exit_at'])}</td>"
            f"<td>{_display(event['exit_reason'])}</td>"
            f"<td>{_display(event['failure_attribution_type'])}</td>"
            f"<td>{_display(event['okx_cluster_status'])}</td>"
            f"<td>{_display(event['okx_cluster_score'])}</td>"
            f"<td>{_display(event['okx_cluster_risk_score'])}</td>"
            f"<td>{_display(event['okx_cluster_distribution_score'])}</td>"
            f"<td>{_display(event['okx_cluster_control_retention_score'])}</td>"
            f"<td>{_fmt_pct(event['largest_cluster_holding_pct'])}</td>"
            f"<td>{_fmt_pct(event['top300_total_holding_pct'])}</td>"
            f"<td>{_fmt_pct(event['cluster_holding_pct_delta'])}</td>"
            f"<td>{_fmt_pct(event['largest_cluster_holding_pct_delta'])}</td>"
            f"<td>{_esc(token.get('latest_reason'))}</td>"
            f"<td>{_esc(token.get('latest_action'))}</td>"
            "</tr>"
        )
    event_items = [f"<li><b>{_esc(e.get('time'))}</b> <span>{_esc(e.get('event_type'))}</span> {_esc(e.get('token_symbol'))} {_esc(e.get('message'))}</li>" for e in events]
    return f"""<!doctype html>
<html lang="zh"><head><meta charset="utf-8"><title>SIKK-SOL Live Dashboard</title>
<style>
body{{font-family:Arial,sans-serif;background:#0f1115;color:#e7e7e7;margin:24px}}.table-wrap{{overflow:auto;max-height:75vh;border:1px solid #2a2f3a;border-radius:10px}}table{{width:100%;border-collapse:collapse;background:#151820;min-width:3200px}}td,th{{border-bottom:1px solid #2a2f3a;padding:8px;text-align:left;font-size:13px;vertical-align:top}}th{{background:#202532;position:sticky;top:0;z-index:1}}.cards{{display:flex;gap:12px;flex-wrap:wrap;margin:16px 0}}.card{{background:#1a1d24;border-radius:10px;padding:12px 18px;min-width:110px}}.card-title{{color:#9aa0a6;font-size:12px}}.card-num{{font-size:26px}}.good{{color:#61d394;font-weight:bold}}.warn{{color:#ffd166;font-weight:bold}}.bad{{color:#ef476f;font-weight:bold}}.neutral{{color:#cfd2d6}}.toolbar{{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0}}input,select{{background:#151820;color:#e7e7e7;border:1px solid #2a2f3a;border-radius:8px;padding:8px}}
</style></head><body>
<h1>SIKK-SOL Live Dashboard</h1>
<p>更新时间：{_esc(state.get('last_update'))}</p>
<p>边界：只做候选发现、结构分析、quote/security、纸面交易和复盘，不执行真实 swap。</p>
<div class="cards"><div class="card"><div class="card-title">Token 总数</div><div class="card-num">{_esc(state.get('token_count', len(tokens)))}</div></div>{''.join(cards)}</div>
<div class="toolbar"><input id="token-search" placeholder="搜索 Token / 地址 / 原因"><select id="state-filter"><option value="">全部 State</option>{state_options}</select><select id="wallet-filter"><option value="">全部 Wallet</option>{wallet_options}</select></div>
<h2>Token 状态 / 事件链路</h2><p>缺失字段统一显示“待补”，用于审计发现→判断→入场→持仓→退出链路。</p><div class="table-wrap"><table><thead><tr><th>符号</th><th>地址</th><th>Priority</th><th>State</th><th>Signal Level</th><th>Signal Gate</th><th>Wallet</th><th>结构分</th><th>风险分</th><th>对手盘</th><th>数据质量</th><th>Quote</th><th>Security</th><th>Paper</th><th>PnL</th><th>discovered_at</th><th>discovery_market_cap_usd</th><th>discovery_liquidity_usd</th><th>first_signal_at</th><th>first_signal_type</th><th>signal_market_cap_usd</th><th>wallet_decision_at</th><th>wallet_decision_market_cap_usd</th><th>paper_entry_at</th><th>paper_entry_market_cap_usd</th><th>paper_entry_price</th><th>paper_entry_amount_sol</th><th>paper_entry_amount_usd</th><th>paper_token_amount</th><th>current_market_cap_usd</th><th>current_price</th><th>unrealized_pnl_sol</th><th>unrealized_pnl_pct</th><th>exit_monitor_at</th><th>paper_exit_at</th><th>exit_reason</th><th>failure_attribution_type</th><th>okx_cluster_status</th><th>okx_cluster_score</th><th>okx_cluster_risk_score</th><th>okx_cluster_distribution_score</th><th>okx_cluster_control_retention_score</th><th>largest_cluster_holding_pct</th><th>top300_total_holding_pct</th><th>cluster_holding_pct_delta</th><th>largest_cluster_holding_pct_delta</th><th>Reason</th><th>Next</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
<h2>最新事件</h2><ul>{''.join(event_items)}</ul>
<script>
function applyFilters(){{
  const q=document.getElementById('token-search').value.toLowerCase();
  const s=document.getElementById('state-filter').value;
  const w=document.getElementById('wallet-filter').value;
  document.querySelectorAll('tbody tr').forEach(r=>{{
    const ok=(!q||r.dataset.search.includes(q))&&(!s||r.dataset.state===s)&&(!w||r.dataset.wallet===w);
    r.style.display=ok?'':'none';
  }});
}}
['token-search','state-filter','wallet-filter'].forEach(id=>document.getElementById(id).addEventListener('input',applyFilters));
</script>
</body></html>"""


def write_dashboard(*, base_dir: str | Path = DEFAULT_BASE_DIR, output_path: str | Path | None = None) -> str:
    base = Path(base_dir)
    path = Path(output_path) if output_path else base / "live_dashboard.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(build_dashboard_html(base_dir=base), encoding="utf-8")
    return str(path)


if __name__ == "__main__":
    print(write_dashboard())
