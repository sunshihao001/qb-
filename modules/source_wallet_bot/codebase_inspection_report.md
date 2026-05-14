# Codebase Inspection Report

## 1. Goal
Audit the legacy SIKK-GMGN single-token report and wallet-structure related files, then map them into the new Source & Wallet Intelligence Bot asset model.

## 2. Audited files
- `sikk_gmgn_token_report.py`
- `sikk_gmgn_new_token_filter.py`
- `sikk_candidate_wallet_structure_pipeline.py`
- `sikk_wallet_structure_gate.py`
- `sikk_wallet_structure_snapshot.py`
- `candidate_states.json` / `candidate_states.csv`
- `candidate_wallet_structure_summary.json` / `.csv` / `.md`
- `candidate_quote_security_summary.json` / `.csv` / `.md`
- `candidate_signal_summary.json` / `.csv`
- `pipeline_manifest.json`
- `pipeline_report.md`

## 3. Findings

### 3.1 The old system already had evidence-oriented output files
The report script writes a bundle of CSVs plus Markdown and ZIP packaging. That is structurally compatible with a wallet-intelligence archive, but it is not yet the new fact-source bot.

### 3.2 The old wallet-structure pipeline already encodes wallet structure gate logic
The pipeline consumes candidate states, builds same-source groups, writes snapshots and deltas, and emits wallet-structure summaries. This is a strong historical seed for the new wallet intelligence layer.

### 3.3 The old system still conflates some report / state / summary artifacts with operational flow
For the new architecture, those outputs must be reclassified as legacy evidence, review evidence, or historical sample material rather than as facts or live state inputs.

### 3.4 The old system is useful, but the new bot boundary must be stricter
The new Source & Wallet Intelligence Bot must explicitly separate:
- fact-source collection
- normalization
- wallet intelligence
- handoff packet generation
- historical archive import
from:
- state-machine decisions
- paper gating
- execution logic
- dominant-side / control-side inference

## 4. Old-system assets worth preserving
- candidate discovery logic
- wallet classification outputs
- structure gate outputs
- snapshot/delta output shape
- review-plan output shape
- infrastructure registry shape
- quote/security summary shape

## 5. Assets that must be downgraded to legacy-only usage
- state-machine outputs
- pipeline report summaries
- paper/readiness labels
- anything derived from simulated execution flow

## 6. Recommended new module layering
- `modules/source_wallet_bot/`
  - import and package passport
  - source registry
  - schema plan
  - evidence taxonomy
  - handoff packet builder
- `data/source_wallet_bot/`
  - imported legacy packages
  - normalized facts
  - audit artifacts
  - schemas
- `reports/source_wallet_bot/`
  - human-readable archive / review reports

## 7. Conclusion
The legacy codebase already contains many wallet-intelligence ingredients. The new bot should reuse its evidence shapes, but the final system must be data-fact first, read-only archive aware, and explicitly non-trading.


## 8. Direct mapping from legacy capabilities to the new bot

- `sikk_gmgn_token_report.py` → source-side token fact bundle, token basics, infrastructure registry, review-plan evidence, and wallet-report archive shape.
- `sikk_gmgn_new_token_filter.py` → candidates_normalized seed.
- `sikk_candidate_wallet_structure_pipeline.py` → wallet_structure_normalized, same-source evidence, and snapshot/delta evidence shape.
- `sikk_wallet_structure_gate.py` → evidence-level and role-classification seed, but not final dominant-side control.
- `sikk_wallet_structure_snapshot.py` → wallet snapshot and delta archive seed.

## 9. Audit conclusion for Source Bot build
The old system is structurally rich enough to seed the new Source & Wallet Intelligence Bot, but the new bot must remain strictly read-only at the archive layer and strictly non-trading at the runtime boundary.
