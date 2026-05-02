#!/usr/bin/env bash
set -euo pipefail

cd /root/sikk-gmgn

python3 - <<'PY'
import json
from pathlib import Path

root = Path('data/gmgn_candidates_live_run')
print('== 核心输出文件 ==')
for name in [
    'live_run_manifest.json',
    'live_state.json',
    'live_board.md',
    'live_dashboard.html',
    'events/live_events.jsonl',
]:
    path = root / name
    print(f'{name}: 存在={path.exists()} 大小={path.stat().st_size if path.exists() else 0}')

state_path = root / 'live_state.json'
if not state_path.exists():
    raise SystemExit('\nlive_state.json 尚未生成')

data = json.loads(state_path.read_text(encoding='utf-8'))
tokens = data.get('tokens') or data.get('token_statuses') or data.get('candidates') or []
if isinstance(tokens, dict):
    tokens = list(tokens.values())

状态统计 = {}
纸面统计 = {}
报价统计 = {}
安全统计 = {}
for row in tokens:
    状态 = row.get('current_state') or row.get('当前状态') or row.get('state') or 'UNKNOWN'
    纸面 = (row.get('paper') or {}).get('paper_status') or row.get('paper_status') or 'UNKNOWN'
    报价 = (row.get('quote') or {}).get('quote_gate') or row.get('quote_gate') or 'UNKNOWN'
    安全 = (row.get('security') or {}).get('security_gate') or row.get('security_gate') or 'UNKNOWN'
    状态统计[状态] = 状态统计.get(状态, 0) + 1
    纸面统计[纸面] = 纸面统计.get(纸面, 0) + 1
    报价统计[报价] = 报价统计.get(报价, 0) + 1
    安全统计[安全] = 安全统计.get(安全, 0) + 1

print('\n== 中文状态统计 ==')
print('Token总数:', len(tokens))
print('状态统计:', 状态统计)
print('纸面统计:', 纸面统计)
print('报价统计:', 报价统计)
print('安全统计:', 安全统计)

board = root / 'live_board.md'
print('\n== Live Board 摘要 ==')
print(board.read_text(encoding='utf-8')[:4000] if board.exists() else 'live_board.md 尚未生成')
PY
