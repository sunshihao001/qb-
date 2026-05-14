# Paper-only Decision Report

- created_at: 2026-05-14T20:34:54Z
- token: TROLLIEN `ECgweD7xkMj4bm8CcM9rusxKjyQGgdosCvVmhGUupump`
- decision: PAPER_ONLY_ALLOWED_EXISTING_RUNTIME_RESULT_CONSUMED
- P07 gate: PAPER_READY
- P08 quote/security permission: ALLOW_CONFIRMATION_LAYER
- paper result source: `data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json`
- paper result: position `paper-ECgweD7xkMj4bm8CcM9rusxKjyQGgdosCvVmhGUupump-2026-05-04T12:40:33Z` closed with pnl `0.0` and exit_reason `命中纸面止损`

## Safety
- no_real_swap: true
- no_signing: true
- no_broadcast: true
- no_private_key: true

## Gate caveat
Wallet runtime says `WALLET_BLOCK` / `would_block=true`, but wallet mode was observe-only. This is accepted only as PASS_WITH_GAPS and must enter issue registry, not a live rule mutation.
