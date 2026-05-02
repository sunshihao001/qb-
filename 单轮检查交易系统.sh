#!/usr/bin/env bash
set -euo pipefail

cd /root/sikk-gmgn

python3 sikk_live_run.py \
  --output-root data/gmgn_candidates_live_run \
  --limit 50 \
  --quote-sources okx \
  --default-quote-amount-sol 0.01 \
  --mode once
