# Legacy Mapping: old SIKK-GMGN wallet report system → SIKK Source & Wallet Intelligence Bot

## 1. Mapping purpose
This document maps the legacy single-token report system and wallet-structure outputs into the new Source & Wallet Intelligence Bot asset graph.

## 2. What the old system already had

### Fact-side and candidate-side assets
- `sikk_gmgn_token_report.py`
- `sikk_gmgn_new_token_filter.py`
- `sikk_candidate_wallet_structure_pipeline.py`
- `sikk_wallet_structure_gate.py`
- `sikk_wallet_structure_snapshot.py`
- `sikk_gmgn_token_report.py` produced CSV/MD/ZIP evidence bundles

### Existing output families from the token report
- `01_analysis_depth.csv`
- `02_token_basic.csv`
- `03_structure_metrics.csv`
- `04_key_address_matrix.csv`
- `05_infrastructure_registry.csv`
- `06_low_weight_scope.csv`
- `07_review_plan.csv`
- `08_summary.csv`
- `sikk_gmgn_report.md`
- bundled `.zip`

### Existing wallet-structure pipeline outputs
- `candidate_wallet_structure_summary.json`
- `candidate_wallet_structure_summary.csv`
- `candidate_wallet_structure_summary.md`
- `candidate_states.json`
- `candidate_states.csv`
- `state_summary.md`
- `candidate_signal_summary.json`
- `candidate_signal_summary.csv`
- `candidate_kline_pipeline_summary.json`
- `candidate_quote_security_summary.json`

## 3. Legacy capability mapping

### Old single-token report script capabilities
- Scan token basics
- Read GMGN metrics
- Read holders / traders
- Read quote/security context
- Build per-wallet classification rows
- Produce review plan
- Export report bundle

### Old wallet-structure pipeline capabilities
- Read candidate state machine
- Build wallet structure gate
- Build same-source grouping
- Build snapshot and delta
- Write wallet structure summaries
- Produce paper-readiness adjacent gate artifacts

## 4. How to map to the new bot

### Old facts → new Source Bot responsibilities
- token discovery → candidates normalized
- token basic info → token market snapshot / source registry
- quote/security → quote_security normalized
- K line outputs → kline normalized
- wallet classification rows → wallet_structure normalized
- infrastructure registry → source registry / relationship registry
- review plan → evidence packet handoff metadata

### Old pipeline artifacts → new role
- `candidate_states.json` → historical state evidence only; never a live state-machine input
- `candidate_signal_summary.json` → historical signal sample only; not a fact source
- `pipeline_manifest.json` → import audit / source manifest sample
- `pipeline_report.md` → review/audit sample only

## 5. Boundary rule
Legacy outputs may be used as historical samples, review references, or import samples.
They must not be promoted to live fact sources and must not overwrite new runtime outputs.

## 6. New bot responsibility framing
The new Source & Wallet Intelligence Bot owns:
- fact-source ingestion
- compressed package import
- field normalization
- wallet profiling
- current token wallet behavior
- funding paths
- same-source groups
- distribution / dispatch / backflow
- wallet structure role classification
- GMGN notes/watchlist
- bot2 handoff packet

It does not own dominant-side control, second-rally motive, PAPER_READY, or BLOCKED decisions.


## 7. File-level audit highlights

### `sikk_gmgn_token_report.py`
- Single-token report generator.
- Aggregates token basics, security metrics, wallet classification, and review-plan outputs.
- Produces CSV, Markdown, and ZIP evidence bundles.
- Useful as a historical evidence-shape seed, not a live fact source.

### `sikk_candidate_wallet_structure_pipeline.py`
- Candidate-state driven wallet structure pipeline.
- Handles same-source grouping.
- Writes snapshot/delta outputs.
- Emits wallet-structure gate summaries.
- Useful as a historical wallet-intelligence layer seed.

### `candidate_states.json` / `.csv`
- State machine-adjacent historical outputs.
- Must stay legacy-only.

### `candidate_quote_security_summary.json`
- Historical quote/security scan summary.
- Must not be reversed into current quote_time or live liquidity truth.
