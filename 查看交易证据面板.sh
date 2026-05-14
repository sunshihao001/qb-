#!/usr/bin/env bash
set -euo pipefail

cd /root/sikk-gmgn

python3 - <<'PY'
from pathlib import Path
import json
from collections import Counter

ROOT = Path('data/gmgn_candidates_live_run')
OUT = ROOT / 'reports' / '交易证据面板.md'
OUT.parent.mkdir(parents=True, exist_ok=True)

def load_json(rel, default):
    p = ROOT / rel
    if not p.exists():
        return default
    try:
        return json.loads(p.read_text(encoding='utf-8'))
    except Exception:
        return default

def fmt_time(v):
    if not v:
        return '—'
    s = str(v)
    if len(s) > 10 and s[10] == 'T':
        s = s[:10] + ' ' + s[11:]
    if s.endswith('Z'):
        s = s[:-1] + ' UTC'
    return s

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

def fmt_num(v, digits=8):
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

def pct_change(now, base):
    try:
        now = float(now); base = float(base)
        if base == 0:
            return None
        return (now - base) / base * 100
    except Exception:
        return None

def first(*vals):
    for v in vals:
        if v is not None and v != '':
            return v
    return None

def short_addr(a):
    if not a:
        return '—'
    a = str(a)
    return a[:6] + '…' + a[-6:] if len(a) > 16 else a

def ts_to_utc(ts):
    if not ts:
        return '—'
    try:
        from datetime import datetime, timezone
        return datetime.fromtimestamp(float(ts), tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    except Exception:
        return str(ts)

def estimate_mc_from_price(row, price):
    if price is None or price == '':
        return None
    try:
        supply = float(row.get('总供应量') or 0)
        price = float(price)
        if supply > 0 and price > 0:
            return supply * price
    except Exception:
        pass
    return None

def market_cap_context(change_pct):
    if change_pct is None:
        return 'UNKNOWN｜缺少可比市值'
    if change_pct <= -30:
        return 'PULLBACK_AFTER_DISCOVERY｜发现后明显回撤'
    if change_pct <= 50:
        return 'EARLY_DISCOVERY｜仍接近发现区间'
    if change_pct <= 200:
        return 'NORMAL_EXPANSION｜正常扩张'
    if change_pct <= 500:
        return 'LATE_CHASING｜偏晚追涨风险'
    return 'OVEREXTENDED｜过度扩张风险'

candidates = load_json('gmgn_new_token_filter/token_candidates.json', {}).get('候选列表', [])
states = load_json('state_machine/candidate_states.json', {}).get('候选状态', [])
signals = load_json('candidate_signal_outputs/candidate_signal_summary.json', {}).get('信号结果', [])
quotes = load_json('quote_security/candidate_quote_security_summary.json', {}).get('处理结果', [])
wallets = load_json('wallet_structure/candidate_wallet_structure_summary.json', {}).get('处理结果', [])
open_pos = load_json('paper_live/paper_positions_open.json', {}).get('open_positions', [])
closed_pos = load_json('paper_live/paper_positions_closed.json', {}).get('closed_positions', [])
live = load_json('live_state.json', {})

by_c = {x.get('代币地址'): x for x in candidates if x.get('代币地址')}
by_s = {x.get('代币地址'): x for x in states if x.get('代币地址')}
by_sig = {x.get('代币地址'): x for x in signals if x.get('代币地址')}
by_q = {x.get('代币地址'): x for x in quotes if x.get('代币地址')}
by_w = {x.get('代币地址'): x for x in wallets if x.get('代币地址')}
by_live = {x.get('token_address'): x for x in live.get('tokens', []) if x.get('token_address')}
open_by_addr = {}
for p in open_pos:
    open_by_addr.setdefault(p.get('代币地址'), []).append(p)
closed_by_addr = {}
for p in closed_pos:
    closed_by_addr.setdefault(p.get('代币地址'), []).append(p)

# 重点展示：OPEN、PAPER_READY、最近关闭，再补充 BLOCKED/ WATCHING 的摘要原因。
important = []
seen = set()
for p in open_pos:
    a = p.get('代币地址')
    if a and a not in seen:
        important.append(a); seen.add(a)
for st in states:
    if st.get('当前状态') == 'PAPER_READY':
        a = st.get('代币地址')
        if a and a not in seen:
            important.append(a); seen.add(a)
for p in sorted(closed_pos, key=lambda x: str(x.get('exit_time') or x.get('last_update_time') or ''), reverse=True)[:5]:
    a = p.get('代币地址')
    if a and a not in seen:
        important.append(a); seen.add(a)

lines = []
lines.append('# SIKK 交易证据面板｜Token 全生命周期')
lines.append('')
lines.append(f'- 更新时间：{fmt_time(live.get("last_update"))}')
lines.append('- 定位：展示“发现/扫描 → 信号 → 钱包结构 → quote/security → 纸面入场 → 持仓/退出”的证据链。')
lines.append('- 安全边界：全部为纸面验证与只读证据，不是真实成交，不执行真实 swap、不签名、不广播。')
lines.append('')
state_counter = Counter(x.get('当前状态','UNKNOWN') for x in states)
lines.append('## 一、总览')
lines.append(f'- Token 总数：{len(states) or len(candidates)}')
lines.append(f'- 状态统计：{dict(state_counter)}')
lines.append(f'- 当前 OPEN 纸面持仓：{len(open_pos)}')
lines.append(f'- 最近 CLOSED 纸面持仓记录：{len(closed_pos)}')
lines.append('')

lines.append('## 二、重点 Token 生命周期明细')
if not important:
    lines.append('- 当前没有 OPEN / PAPER_READY / 最近 CLOSED 可展示。')
for idx, addr in enumerate(important, 1):
    c = by_c.get(addr, {})
    st = by_s.get(addr, {})
    sig = by_sig.get(addr, {})
    q = by_q.get(addr, {})
    w = by_w.get(addr, {})
    lv = by_live.get(addr, {})
    op = (open_by_addr.get(addr) or [None])[0]
    latest_closed = None
    if closed_by_addr.get(addr):
        latest_closed = sorted(closed_by_addr[addr], key=lambda x: str(x.get('exit_time') or x.get('last_update_time') or ''), reverse=True)[0]
    pos = op or latest_closed or {}
    symbol = first(c.get('代币符号'), st.get('代币符号'), pos.get('代币符号'), lv.get('token_symbol'), '—')
    current_mc = c.get('当前市值USD')
    current_price = first(pos.get('last_price'), None)
    signal_mc = estimate_mc_from_price(c, sig.get('信号价格'))
    entry_mc = estimate_mc_from_price(c, pos.get('entry_price'))
    exit_mc = estimate_mc_from_price(c, pos.get('exit_price')) if latest_closed else None
    # 当前候选扫描市值作为当前/最近扫描市值。项目当前还没有真正 first_seen/discovery 快照；这里明确标记。
    discovery_mc = c.get('当前市值USD')
    mc_change_from_entry = pct_change(current_mc, entry_mc) if entry_mc else None
    lines.append(f'### #{idx} {symbol}')
    lines.append(f'- 代币地址：{addr}')
    lines.append(f'- 短地址：{short_addr(addr)}')
    lines.append(f'- 当前状态：{first(st.get("当前状态"), lv.get("current_state"), pos.get("status"), "—")}')
    lines.append(f'- 最新原因：{first(st.get("状态原因"), lv.get("latest_reason"), "—")}')
    lines.append('')
    lines.append('#### 1）发现 / 候选扫描')
    lines.append(f'- 开盘时间：{ts_to_utc(c.get("开盘时间戳"))}')
    lines.append(f'- 候选扫描时间：{fmt_time(c.get("扫描时间"))}')
    lines.append(f'- 发现/扫描市值：{fmt_money(discovery_mc)}')
    lines.append(f'- 当前/最近扫描市值：{fmt_money(current_mc)}')
    lines.append(f'- 流动性：{fmt_money(c.get("流动性USD"))}')
    lines.append(f'- 24H 成交额：{fmt_money(c.get("24H成交额USD"))}')
    lines.append(f'- 24H 净买入：{fmt_money(c.get("24H净买入USD"))}')
    lines.append(f'- Top10 / Dev 持仓：{fmt_pct((c.get("Top10持仓率") or 0)*100 if c.get("Top10持仓率") is not None else None)} / {fmt_pct((c.get("Dev持仓率") or 0)*100 if c.get("Dev持仓率") is not None else None)}')
    lines.append('- 说明：当前项目还没有独立持久化 `discovered_at + discovery_market_cap_usd` 快照；这里先使用候选扫描时间/扫描市值展示，后续应升级为真正首次发现快照。')
    lines.append('')
    lines.append('#### 2）K线 / 信号')
    lines.append(f'- 信号时间：{fmt_time(sig.get("信号时间"))}')
    lines.append(f'- 信号等级：{first(sig.get("信号等级"), st.get("信号等级"), "—")}')
    lines.append(f'- 策略类型：{first(sig.get("策略类型"), st.get("策略类型"), "—")}')
    lines.append(f'- 信号价格：{fmt_num(sig.get("信号价格"), 10)}')
    lines.append(f'- 信号时估算市值：{fmt_money(signal_mc)}')
    lines.append(f'- 建议纸面仓位：{fmt_num(first(sig.get("建议纸面仓位SOL"), st.get("建议纸面仓位SOL")), 6)} SOL')
    lines.append(f'- 风险门禁：{first(sig.get("风险门禁"), st.get("风险门禁"), "—")}')
    lines.append('')
    lines.append('#### 3）钱包结构 / 筹码证据')
    wallet_time = None
    if addr:
        decision = ROOT / 'wallet_structure' / addr / 'wallet_structure_decision.json'
        if decision.exists():
            try:
                wallet_time = json.loads(decision.read_text(encoding='utf-8')).get('生成时间')
            except Exception:
                pass
    lines.append(f'- 钱包判断时间：{fmt_time(wallet_time)}')
    lines.append(f'- 钱包结构：{first(w.get("钱包结构结论"), st.get("钱包结构结论"), (lv.get("wallet_structure") or {}).get("wallet_structure_status"), "未接入")}')
    lines.append(f'- 钱包结构分 / 风险分 / 对手盘压力：{first(w.get("钱包结构评分"), st.get("钱包结构评分"), "—")} / {first(w.get("钱包风险评分"), st.get("钱包风险评分"), "—")} / {first(w.get("对手盘压力评分"), st.get("对手盘压力评分"), "—")}')
    lines.append(f'- 数据质量 / 证据等级：{first(w.get("数据质量评分"), st.get("数据质量评分"), "—")} / {first(w.get("钱包证据等级"), st.get("钱包证据等级"), "—")}')
    lines.append(f'- 筹码控制权状态：{w.get("筹码控制权状态", "—")}')
    lines.append(f'- 钱包结构原因：{first(w.get("钱包结构原因"), st.get("钱包结构原因"), "—")}')
    lines.append('')
    lines.append('#### 4）Quote / 安全扫描')
    quote_time = None
    if q.get('quote_security_decision_json'):
        p = Path(q['quote_security_decision_json'])
        if not p.is_absolute(): p = Path('/root/sikk-gmgn') / p
        if p.exists():
            try:
                quote_time = json.loads(p.read_text(encoding='utf-8')).get('snapshot_time')
            except Exception:
                pass
    lines.append(f'- Quote 检查时间：{fmt_time(quote_time)}')
    lines.append(f'- Quote 权限：{first(q.get("quote_security_permission"), (lv.get("quote") or {}).get("quote_gate"), "—")}')
    lines.append(f'- 报价状态：{q.get("报价状态", "—")}')
    lines.append(f'- 安全权限 / 风险等级：{q.get("安全权限", "—")} / {q.get("安全风险等级", "—")}')
    lines.append(f'- 最大价格影响 / 报价偏离：{fmt_pct(q.get("最大价格影响_pct"))} / {fmt_pct(q.get("报价偏离_pct"))}')
    lines.append(f'- Quote/Security 原因：{q.get("原因", "—")}')
    lines.append('')
    lines.append('#### 5）纸面入场 / 持仓')
    if pos:
        entry_amount_usd = None
        try:
            # 使用 0.01 SOL 报价来源中的 SOL 单价不可总是可得，这里只保留 SOL 金额；USD 后续接 SOL 价格快照。
            entry_amount_usd = pos.get('position_usd')
        except Exception:
            pass
        lines.append(f'- 纸面买入时间：{fmt_time(pos.get("entry_time"))}')
        lines.append(f'- 纸面买入金额：{fmt_num(pos.get("position_sol"), 6)} SOL')
        lines.append(f'- 买入金额 USD：{fmt_money(entry_amount_usd)}')
        lines.append(f'- 买入价格：{fmt_num(pos.get("entry_price"), 10)}')
        lines.append(f'- 买入时估算市值：{fmt_money(entry_mc)}')
        lines.append(f'- 当前价格：{fmt_num(pos.get("last_price"), 10)}')
        lines.append(f'- 当前/最近扫描市值：{fmt_money(current_mc)}')
        lines.append(f'- 从入场估算市值变化：{fmt_pct(mc_change_from_entry)}')
        lines.append(f'- 市值上下文：{market_cap_context(mc_change_from_entry)}')
        lines.append(f'- 当前收益率：{fmt_pct(first(pos.get("当前收益率_pct"), pos.get("live_pnl_pct"), pos.get("最终收益率_pct")))}')
        lines.append(f'- 最大浮盈 / 最大浮亏：{fmt_pct(pos.get("最大浮盈_pct"))} / {fmt_pct(pos.get("最大浮亏_pct"))}')
        lines.append(f'- 剩余仓位：{fmt_num(pos.get("remaining_pct"), 2)}%')
        lines.append(f'- 止损价格：{fmt_num(pos.get("stop_price"), 10)}')
        lines.append(f'- 已触发止盈次数：{pos.get("已触发止盈次数", len(pos.get("triggered_tps") or []))}')
        if latest_closed:
            lines.append(f'- 纸面退出时间：{fmt_time(latest_closed.get("exit_time"))}')
            lines.append(f'- 退出价格：{fmt_num(latest_closed.get("exit_price"), 10)}')
            lines.append(f'- 退出时估算市值：{fmt_money(exit_mc)}')
            lines.append(f'- 退出原因：{latest_closed.get("exit_reason", "—")}')
            lines.append(f'- 失败归因：{latest_closed.get("failure_type", "—")} / {latest_closed.get("failure_reason", "—")}')
    else:
        lines.append('- 尚无纸面入场记录。')
    lines.append('')

lines.append('## 三、字段缺口 / 下一步工程升级')
lines.append('- 需要新增真正的首次发现快照：`discovered_at`、`discovery_market_cap_usd`、`discovery_liquidity_usd`、`discovery_holder_count`。')
lines.append('- 需要在信号、钱包、quote、paper position 中固化阶段市值：`market_cap_at_signal_usd`、`market_cap_at_wallet_decision_usd`、`market_cap_at_quote_usd`、`market_cap_at_paper_entry_usd`。')
lines.append('- 需要新增市值上下文状态：`EARLY_DISCOVERY / NORMAL_EXPANSION / LATE_CHASING / OVEREXTENDED / PULLBACK_AFTER_DISCOVERY / REACTIVATION_AFTER_DRAWDOWN`。')
lines.append('- 需要把 `market_pattern_type`、`dominant_side_lifecycle`、`dominant_side_intent`、`wallet_pattern_alignment` 接入状态机和面板，但第一步先 observe 记录，不直接 hard block。')
lines.append('')
lines.append('## 四、安全边界')
lines.append('- 本面板只读取本地 JSON/CSV 输出。')
lines.append('- 本面板展示的是纸面交易证据链，不是真实买卖流水。')
lines.append('- 不执行真实 swap，不签名，不广播，不自动卖出。')

text = '\n'.join(lines) + '\n'
OUT.write_text(text, encoding='utf-8')
print(text)
print(f'\n已写入：{OUT}')
PY
