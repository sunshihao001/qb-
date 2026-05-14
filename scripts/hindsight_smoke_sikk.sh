#!/usr/bin/env bash
set -euo pipefail
cd /root/sikk-gmgn

python3 scripts/hindsight_retain_sikk.py \
  --file data/gmgn_candidates_live_run/orchestrator/pipeline_report.md \
  --context "SIKK live pipeline report: candidate discovery, wallet structure, quote/security, paper/readiness summary" \
  --document-id "sikk-live-run-latest" \
  --tag topic:runtime \
  --tag topic:wallet-structure \
  --tag type:run-report

python3 scripts/hindsight_recall_sikk.py \
  "本轮 SIKK pipeline 有多少 PAPER_READY，钱包结构结果是什么？" \
  --include-chunks \
  --limit 5
