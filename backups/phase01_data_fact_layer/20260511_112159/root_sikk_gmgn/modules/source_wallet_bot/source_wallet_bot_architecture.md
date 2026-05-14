# SIKK Source & Wallet Intelligence Bot Architecture

## Positioning
SIKK Source & Wallet Intelligence Bot is the top-upstream fact-source and wallet-intelligence layer.

It is not a normal data-source bot and not a trading bot.

It handles:
- fact-source ingestion
- compressed package import
- field normalization
- wallet profiling
- current token wallet behavior
- token source judgment
- funding source judgment
- same-source execution group evidence
- distribution / dispatch / backflow evidence
- profit recovery evidence
- counterparty whale candidate evidence
- historical address library
- wallet structure role classification
- evidence level
- risk level
- GMGN note / watchlist
- wallet_intelligence_decision
- bot2_handoff_packet

It does not handle:
- dominant-side control
- dominant-side motive
- counterparty comprehensive pressure
- second rally motive
- PAPER_READY
- BLOCKED
- final_trade_gate
- state machine
- paper runner
- real execution

## Source tiers
L0/L1 can be fact source. L2 is standardized fact. L3 is legacy sample only. L4 is review/audit only.

## Directory boundaries
Allowed write targets:
- `modules/source_wallet_bot/`
- `data/source_wallet_bot/`
- `data/source_wallet_bot/audit/`
- `data/source_wallet_bot/schemas/`
- `reports/source_wallet_bot/`
- `research_loop/checkpoints/`
- `imports/staging/`

Forbidden write targets:
- state machine runtime
- paper runner outputs
- real execution layer
- dashboard outputs
- old reports
- old runtime outputs

## Why dashboard / paper / report cannot be fact sources
They are downstream views, simulations, reports, or review artifacts. Using them as upstream facts creates circular evidence and temporal contamination.
