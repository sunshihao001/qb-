#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK Runtime static HTML dashboard builder."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any, Dict, List

DEFAULT_BASE_DIR = Path("data/gmgn_candidates_live_run")


def _read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _read_events(base_dir: Path, limit: int = 40) -> List[Dict[str, Any]]:
    path = base_dir / "events" / "live_events.jsonl"
    if not path.exists():
        return []
    events = []
    for line in path.read_text(encoding="utf-8").splitlines()[-limit:]:
        try:
            events.append(json.loads(line))
        except Exception:
            continue
    return events


def _esc(value: Any) -> str:
    return html.escape(str(value if value is not None else ""))


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
        wallet = token.get("wallet_structure", {}) if isinstance(token.get("wallet_structure", {}), dict) else {}
        signal = token.get("signal", {}) if isinstance(token.get("signal", {}), dict) else {}
        quote = token.get("quote", {}) if isinstance(token.get("quote", {}), dict) else {}
        security = token.get("security", {}) if isinstance(token.get("security", {}), dict) else {}
        paper = token.get("paper", {}) if isinstance(token.get("paper", {}), dict) else {}
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
            f"<td>{_esc(token.get('latest_reason'))}</td>"
            f"<td>{_esc(token.get('latest_action'))}</td>"
            "</tr>"
        )
    event_items = [f"<li><b>{_esc(e.get('time'))}</b> <span>{_esc(e.get('event_type'))}</span> {_esc(e.get('token_symbol'))} {_esc(e.get('message'))}</li>" for e in events]
    return f"""<!doctype html>
<html lang="zh"><head><meta charset="utf-8"><title>SIKK-SOL Live Dashboard</title>
<style>
body{{font-family:Arial,sans-serif;background:#0f1115;color:#e7e7e7;margin:24px}}table{{width:100%;border-collapse:collapse;background:#151820}}td,th{{border-bottom:1px solid #2a2f3a;padding:8px;text-align:left;font-size:13px}}th{{background:#202532;position:sticky;top:0}}.cards{{display:flex;gap:12px;flex-wrap:wrap;margin:16px 0}}.card{{background:#1a1d24;border-radius:10px;padding:12px 18px;min-width:110px}}.card-title{{color:#9aa0a6;font-size:12px}}.card-num{{font-size:26px}}.good{{color:#61d394;font-weight:bold}}.warn{{color:#ffd166;font-weight:bold}}.bad{{color:#ef476f;font-weight:bold}}.neutral{{color:#cfd2d6}}.toolbar{{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0}}input,select{{background:#151820;color:#e7e7e7;border:1px solid #2a2f3a;border-radius:8px;padding:8px}}
</style></head><body>
<h1>SIKK-SOL Live Dashboard</h1>
<p>更新时间：{_esc(state.get('last_update'))}</p>
<p>边界：只做候选发现、结构分析、quote/security、纸面交易和复盘，不执行真实 swap。</p>
<div class="cards"><div class="card"><div class="card-title">Token 总数</div><div class="card-num">{_esc(state.get('token_count', len(tokens)))}</div></div>{''.join(cards)}</div>
<div class="toolbar"><input id="token-search" placeholder="搜索 Token / 地址 / 原因"><select id="state-filter"><option value="">全部 State</option>{state_options}</select><select id="wallet-filter"><option value="">全部 Wallet</option>{wallet_options}</select></div>
<h2>Token 状态</h2><table><thead><tr><th>符号</th><th>地址</th><th>Priority</th><th>State</th><th>Signal Level</th><th>Signal Gate</th><th>Wallet</th><th>结构分</th><th>风险分</th><th>对手盘</th><th>数据质量</th><th>Quote</th><th>Security</th><th>Paper</th><th>PnL</th><th>Reason</th><th>Next</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
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
