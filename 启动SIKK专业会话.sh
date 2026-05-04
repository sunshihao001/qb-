#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="/root/sikk-gmgn"
OUTPUT_DIR="data/gmgn_candidates_live_run"
SITE_PORT="8080"
PUBLIC_IP="96.126.130.99"

create_session() {
  local session_name="$1"
  local command_text="$2"

  if tmux has-session -t "$session_name" 2>/dev/null; then
    echo "[已存在] $session_name"
  else
    tmux new-session -d -s "$session_name" -c "$PROJECT_DIR" "$command_text"
    echo "[已创建] $session_name"
  fi
}

create_session "sikk-live" "bash -lc 'cd /root/sikk-gmgn; ./启动交易系统.sh'"
create_session "sikk-dashboard" "bash -lc 'cd /root/sikk-gmgn; python3 -m http.server 8080 --bind 0.0.0.0 -d data/gmgn_candidates_live_run/site'"
create_session "sikk-builder" "bash"
create_session "sikk-verifier" "bash"
create_session "sikk-logs" "bash"
create_session "sikk-telegram" "bash"

echo
printf '== SIKK tmux 会话 ==\n'
tmux ls || true

echo
printf '== 可打开网站 ==\n'
printf 'http://%s:%s/\n' "$PUBLIC_IP" "$SITE_PORT"

echo
printf '== 固定职责 ==\n'
printf '%s\n' \
  'sikk-live：只跑 sikk_live_run.py 单入口 loop' \
  'sikk-dashboard：只跑只读静态网站服务' \
  'sikk-builder：只做 Hermes/Codex/Claude 开发' \
  'sikk-verifier：只跑测试、编译、安全检查' \
  'sikk-logs：只看 live_board/events/日报' \
  'sikk-telegram：预留 Telegram 广播/状态检查'

echo
printf '安全边界：默认只做候选发现、钱包结构、报价/安全、纸面交易、日报和静态观测；不真实 swap、不签名、不广播。\n'
