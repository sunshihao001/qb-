#!/usr/bin/env bash
set -euo pipefail

ENV_FILE="/root/.hindsight/.env"
PROVIDER="${1:-openai}"
MODEL="${2:-gpt-4o-mini}"
MODE="${3:-default}"

mkdir -p "$(dirname "$ENV_FILE")"
chmod 700 "$(dirname "$ENV_FILE")"

printf '请输入临时 Hindsight LLM API key（输入不会回显，不会写入命令历史）：' >&2
IFS= read -r -s API_KEY
printf '\n' >&2

if [ -z "$API_KEY" ]; then
  echo "未输入 API key，已退出。" >&2
  exit 2
fi

umask 077
cat > "$ENV_FILE" <<EOF
HINDSIGHT_API_LLM_PROVIDER=$PROVIDER
HINDSIGHT_API_LLM_API_KEY=$API_KEY
HINDSIGHT_API_LLM_MODEL=$MODEL
EOF

if [ "$MODE" = "chunks" ]; then
  cat >> "$ENV_FILE" <<EOF
HINDSIGHT_API_RETAIN_EXTRACTION_MODE=chunks
EOF
fi

chmod 600 "$ENV_FILE"
echo "Hindsight LLM env 已写入 $ENV_FILE（key 未打印）。provider=$PROVIDER model=$MODEL mode=$MODE"
