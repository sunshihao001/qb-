#!/usr/bin/env bash
set -euo pipefail

ENV_FILE="/root/.hindsight/.env"
IMAGE="ghcr.io/vectorize-io/hindsight:latest"
NAME="hindsight"
VOLUME="hindsight_pg0"

if [ ! -f "$ENV_FILE" ]; then
  echo "Missing $ENV_FILE. Create it first." >&2
  exit 2
fi

if grep -qE 'HINDSIGHT_API_LLM_API_KEY=(fill_me_in_locally|your-|sk-xxxxxxxx|gsk_xxxxxxxxx)' "$ENV_FILE"; then
  echo "Hindsight env 仍是占位 key。请编辑 $ENV_FILE 填入真实 HINDSIGHT_API_LLM_API_KEY 后再运行。" >&2
  exit 3
fi

mkdir -p /root/.hindsight
chmod 700 /root/.hindsight
chmod 600 "$ENV_FILE"

docker rm -f "$NAME" >/dev/null 2>&1 || true
docker volume create "$VOLUME" >/dev/null

docker run -d \
  --name "$NAME" \
  --restart unless-stopped \
  --env-file "$ENV_FILE" \
  -p 127.0.0.1:8888:8888 \
  -p 127.0.0.1:9999:9999 \
  -v "$VOLUME:/home/hindsight/.pg0" \
  "$IMAGE"

echo "Hindsight container started."
docker ps --filter name="$NAME" --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
