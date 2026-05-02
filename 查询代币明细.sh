#!/usr/bin/env bash
set -euo pipefail

cd /root/sikk-gmgn

python3 - <<'PY'
from pathlib import Path
import json
from datetime import datetime, timezone

ROOT = Path('data/gmgn_candidates_live_run')

def load_json(rel, default):
    p = ROOT / rel
    if not p.exists():
        return default
    try:
        return json.loads(p.read_text(encoding='utf-8'))
    except Exception as exc:
        return default

def fmt_money(v):
    if v is None or v == '':
        return '—'
    try:
        v = float(v)
    except Exception:
        return str(v)
    if abs(v) >= 1_000_000:
        return f'${v/1_000_000:.2f}M'
    if abs(v) >= 1_000:
        return f'${v/1_000:.1f}K'
    return f'${v:.2f}'

def fmt_num(v, digits=6):
    if v is None or v == '':
        return '—'
    try:
        v = float(v)
    except Exception:
        return str(v)
    if v == 0:
        return '0'
    if abs(v) < 0.000001:
        return f'{v:.10g}'
    if abs(v) < 0.01:
        return f'{v:.8f}'.rstrip('0').rstrip('.')
    return f'{v:.{digits}f}'.rstrip('0').rstrip('.')

def fmt_pct(v):
    if v is None or v == '':
        return '—'
    try:
        return f'{float(v):+.2f}%'
    except Exception:
        return str(v)

def fmt_time(v):
    if not v:
        return '—'
    s = str(v)
    # 只把 ISO 时间分隔符 T 替换为空格，不能把 UTC 里的 T 误替换掉。
    if len(s) > 10 and s[10] == 'T':
        s = s[:10] + ' ' + s[11:]
    if s.endswith('Z'):
        s = s[:-1] + ' UTC'
    return s

def short_addr(a):
    if not a:
        return '—'
    s=str(a)
    return s[:6] + '…' + s[-6:] if len(s) > 16 else s

def first(*vals):
    for v in vals:
        if v is not None and v != '':
            return v
    return None

live = load_json('live_state.json', {})
candidates = load_json('gmgn_new_token_filter/token_candidates.json', {}).get('候选列表', [])
signals = load_json('candidate_signal_outputs/candidate_signal_summary.json', {}).get('信号结果', [])
quotes = load_json('quote_security/candidate_quote_security_summary.json', {}).get('处理结果', [])
open_pos = load_json('paper_live/paper_positions_open.json', {}).get('open_positions', [])
closed_pos = load_json('paper_live/paper_positions_closed.json', {}).get('closed_positions', [])

cand_by_addr = {x.get('代币地址'): x for x in candidates if x.get('代币地址')}
sig_by_addr = {x.get('代币地址'): x for x in signals if x.get('代币地址')}
quote_by_addr = {x.get('代币地址'): x for x in quotes if x.get('代币地址')}
live_by_addr = {x.get('token_address'): x for x in live.get('tokens', []) if x.get('token_address')}

print('## SIKK 交易系统｜代币与纸面持仓明细')
print(f'更新时间: {fmt_time(live.get("last_update"))}')
print('说明: 以下全部为纸面验证/观察数据，不是真实买入记录，不执行真实 swap、不签名、不广播。')
print()

print('### 一、当前纸面持仓 OPEN')
if not open_pos:
    print('- 当前没有 OPEN 纸面持仓。')
else:
    for i, p in enumerate(open_pos, 1):
        addr = p.get('代币地址')
        c = cand_by_addr.get(addr, {})
        s = sig_by_addr.get(addr, {})
        q = quote_by_addr.get(addr, {})
        l = live_by_addr.get(addr, {})
        wallet = l.get('wallet_structure') or {}
        quote = l.get('quote') or {}
        sec = l.get('security') or {}
        paper = l.get('paper') or {}
        print(f'- #{i} {p.get("代币符号") or c.get("代币符号") or "—"}')
        print(f'  - 代币地址: {addr}')
        print(f'  - 短地址: {short_addr(addr)}')
        print(f'  - 纸面买入时间: {fmt_time(p.get("entry_time"))}')
        print(f'  - 纸面买入金额: {fmt_num(p.get("position_sol"), 6)} SOL')
        print(f'  - 剩余仓位: {fmt_num(p.get("remaining_pct"), 2)}%')
        print(f'  - 入场价格: {fmt_num(p.get("entry_price"), 10)}')
        print(f'  - 当前价格: {fmt_num(p.get("last_price"), 10)}')
        print(f'  - 止损价格: {fmt_num(p.get("stop_price"), 10)}')
        print(f'  - 当前收益率: {fmt_pct(first(p.get("当前收益率_pct"), p.get("live_pnl_pct"), paper.get("unrealized_pnl_pct")))}')
        print(f'  - 最大浮盈/浮亏: {fmt_pct(p.get("最大浮盈_pct"))} / {fmt_pct(p.get("最大浮亏_pct"))}')
        print(f'  - 已触发止盈次数: {p.get("已触发止盈次数", len(p.get("triggered_tps") or []))}')
        print(f'  - 当前市值: {fmt_money(c.get("当前市值USD"))}')
        print(f'  - 流动性: {fmt_money(c.get("流动性USD"))}')
        print(f'  - 24H成交额: {fmt_money(c.get("24H成交额USD"))}')
        print(f'  - 24H净买入: {fmt_money(c.get("24H净买入USD"))}')
        print(f'  - 信号等级: {first(p.get("signal_level"), s.get("信号等级"), "—")}')
        print(f'  - 策略类型: {first(p.get("strategy_type"), s.get("策略类型"), "—")}')
        print(f'  - 信号时间: {fmt_time(s.get("信号时间"))}')
        print(f'  - 信号价格: {fmt_num(s.get("信号价格"), 10)}')
        print(f'  - 钱包结构: {wallet.get("wallet_structure_status", "未接入")}')
        print(f'  - 报价状态: {first(quote.get("quote_gate"), q.get("quote_security_permission"), p.get("quote_security_state"), "—")}')
        print(f'  - 安全状态: {first(sec.get("security_gate"), q.get("安全权限"), "—")}')
        print(f'  - 最新状态: {first(l.get("current_state"), p.get("status"), "—")}')
        print(f'  - 最近更新时间: {fmt_time(first(p.get("last_update_time"), l.get("last_update")))}')

print()
print('### 二、当前 PAPER_READY / 待人工确认观察')
ready = [x for x in live.get('tokens', []) if x.get('current_state') == 'PAPER_READY']
if not ready:
    print('- 当前没有 PAPER_READY。')
else:
    for i, l in enumerate(ready, 1):
        addr = l.get('token_address')
        c = cand_by_addr.get(addr, {})
        s = sig_by_addr.get(addr, {})
        q = quote_by_addr.get(addr, {})
        wallet = l.get('wallet_structure') or {}
        quote = l.get('quote') or {}
        sec = l.get('security') or {}
        print(f'- #{i} {l.get("token_symbol") or c.get("代币符号") or "—"}')
        print(f'  - 代币地址: {addr}')
        print(f'  - 当前市值: {fmt_money(c.get("当前市值USD"))}')
        print(f'  - 流动性: {fmt_money(c.get("流动性USD"))}')
        print(f'  - 24H成交额: {fmt_money(c.get("24H成交额USD"))}')
        print(f'  - 24H净买入: {fmt_money(c.get("24H净买入USD"))}')
        print(f'  - 建议纸面仓位: {fmt_num(s.get("建议纸面仓位SOL"), 6)} SOL')
        print(f'  - 信号时间: {fmt_time(s.get("信号时间"))}')
        print(f'  - 信号价格: {fmt_num(s.get("信号价格"), 10)}')
        print(f'  - 信号等级: {first(s.get("信号等级"), (l.get("signal") or {}).get("signal_level"), "—")}')
        print(f'  - 策略类型: {s.get("策略类型", "—")}')
        print(f'  - 钱包结构: {wallet.get("wallet_structure_status", "未接入")}')
        print(f'  - 钱包风险分: {first(wallet.get("wallet_risk_score"), "—")}')
        print(f'  - 对手盘压力分: {first(wallet.get("counterparty_pressure_score"), "—")}')
        print(f'  - 报价状态: {first(quote.get("quote_gate"), q.get("quote_security_permission"), "—")}')
        print(f'  - 安全状态: {first(sec.get("security_gate"), q.get("安全权限"), "—")}')
        print(f'  - 状态原因: {l.get("latest_reason", "—")}')

print()
print('### 三、最近已关闭纸面持仓 CLOSED（最近10条）')
recent_closed = sorted(closed_pos, key=lambda x: str(x.get('exit_time') or x.get('last_update_time') or ''), reverse=True)[:10]
if not recent_closed:
    print('- 暂无已关闭纸面持仓。')
else:
    for i, p in enumerate(recent_closed, 1):
        addr = p.get('代币地址')
        c = cand_by_addr.get(addr, {})
        print(f'- #{i} {p.get("代币符号") or c.get("代币符号") or "—"}')
        print(f'  - 代币地址: {addr}')
        print(f'  - 纸面买入时间: {fmt_time(p.get("entry_time"))}')
        print(f'  - 纸面退出时间: {fmt_time(p.get("exit_time"))}')
        print(f'  - 纸面买入金额: {fmt_num(p.get("position_sol"), 6)} SOL')
        print(f'  - 入场/退出价格: {fmt_num(p.get("entry_price"), 10)} / {fmt_num(p.get("exit_price"), 10)}')
        print(f'  - 最终收益率: {fmt_pct(first(p.get("最终收益率_pct"), p.get("当前收益率_pct")))}')
        print(f'  - 最大浮盈/浮亏: {fmt_pct(p.get("最大浮盈_pct"))} / {fmt_pct(p.get("最大浮亏_pct"))}')
        print(f'  - 退出原因: {p.get("exit_reason", "—")}')
        print(f'  - 失败归因: {p.get("failure_type", "—")} / {p.get("failure_reason", "—")}')

print()
print('### 四、候选池统计摘要')
from collections import Counter
state_counter = Counter(x.get('current_state', 'UNKNOWN') for x in live.get('tokens', []))
paper_counter = Counter((x.get('paper') or {}).get('paper_status', 'UNKNOWN') for x in live.get('tokens', []))
wallet_counter = Counter((x.get('wallet_structure') or {}).get('wallet_structure_status', '未接入') for x in live.get('tokens', []))
print(f'- Token总数: {live.get("token_count", len(live.get("tokens", [])))}')
print(f'- 状态统计: {dict(state_counter)}')
print(f'- 纸面统计: {dict(paper_counter)}')
print(f'- 钱包统计: {dict(wallet_counter)}')
print()
print('安全边界: 本脚本只读本地 JSON 汇总文件；只展示纸面买入/观察细节，不执行真实交易。')
PY
