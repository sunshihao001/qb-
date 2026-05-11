# SIKK-GMGN Slim Cleanup Direction — 2026-05-11

## User-corrected principle

The useful assets are not the accumulated bulk runtime data. The useful assets are:

1. HER ontology / bottom runtime logic
   - control plane
   - task routing
   - contracts
   - verification/recovery
   - audit/state/handoff patterns
   - runtime closure logic

2. Project document-processing methodology
   - how documents are ingested
   - how scattered docs become contracts/schemas/task packages
   - how reports are separated from machine-readable artifacts
   - how reusable theory/methodology is promoted into skills/modules

3. SIKK trading-analysis theory and actual calculation formulas
   - wallet/chip/structure formulas
   - LP/pool dynamics formulas
   - token cluster/association formulas
   - scenario/risk formulas
   - strategy gate formulas
   - execution-risk formulas

4. Thin API-driven runtime implementation
   - exchange / trading-platform data interfaces can re-fetch current data
   - historical bulky run outputs are lower value unless used as regression fixtures
   - preserve only small representative fixtures, not all runs

## Cleanup posture

Do not keep the project as a giant data warehouse. Convert it to:

- HER bottom logic system
- document-to-contract processing system
- formula/theory library
- API adapters
- small replay/regression fixtures
- minimal audit examples

## Strong keep

- `/root/sikk-gmgn/hermes_harness/`
- `/root/sikk-gmgn/sikk_stable_trader_os/`
- `/root/sikk-gmgn/docs/` only control-plane / constitution / routing / processing docs
- `/root/sikk-gmgn/skills/`
- `/root/sikk-gmgn/modules/` useful code modules only
- `/root/sikk-gmgn/contracts/`
- `/root/sikk-gmgn/schemas/`
- `/root/sikk-gmgn/tests/`
- `/root/sikk-gmgn/tools/`
- `/root/sikk-gmgn/scripts/`
- `/root/sikk-gmgn/knowledge/` if it contains theory/methodology
- `/root/sikk-gmgn/research_loop/methodology/`
- `/root/sikk-gmgn/research_loop/mappings/`
- `/root/sikk-gmgn/research_loop/total_control/`
- `/root/sikk-gmgn/research_loop/acceptance/`

## Keep only as tiny fixture samples

For each category below, keep at most 1-3 representative token/case fixtures after backup:

- `data/source_wallet_bot/`
- `data/gmgn_candidates_live_run/`
- `data/stable_trader_os/`
- `reports/system_audit/`
- `reports/runtime/`
- `legacy_compat/`

## Archive then remove from active workspace

These are mostly bulky historical state/run outputs. Back up first, then move out of active workspace:

- `research_loop/state/wallet_data_semantic_classification_v2/`
- `research_loop/state/wallet_data_copy_v7/`
- `research_loop/state/wallet_data_token_index_v3/`
- `research_loop/state/wallet_data_legacy_mapping_v6/`
- `research_loop/state/wallet_data_recon_v1/`
- `reports/review_ops_bot/`
- old timestamped runs under `data/*_2026*`
- `runtime_logs/`
- `outputs/`
- root-level generated reports/runs not used by import paths

## Delete/quarantine candidates after backup

- `__pycache__/`
- `.pytest_cache/`
- repeated generated dashboards if API can regenerate them
- duplicate reports that are not acceptance/audit exemplars

## New target architecture

```text
/root/sikk-gmgn/
  hermes_harness/                 # HER ontology/runtime bottom logic
  sikk_stable_trader_os/           # thin SIKK control registry
  docs/                            # constitution/routes/document-processing specs only
  modules/
    api_adapters/                  # exchange/trading-platform data interfaces
    formulas/                      # theory + calculation formulas
    runtime/                       # thin orchestration
  contracts/
  schemas/
  tests/
    fixtures/                      # tiny replay examples only
  research_loop/
    methodology/                   # theory/method docs
    mappings/                      # doc->contract maps
    plans/                         # cleanup/system plans
  data/
    fixtures/                      # small selected fixtures, not huge history
```

## Next cleanup action

1. Run backup script first.
2. Generate a second-stage `archive_then_remove_paths.txt`.
3. Move bulky historical data to `/root/sikk-archive/` instead of deleting immediately.
4. Keep a few fixtures and formula/theory docs.
5. Build API-driven formula modules instead of accumulating more raw datasets.
