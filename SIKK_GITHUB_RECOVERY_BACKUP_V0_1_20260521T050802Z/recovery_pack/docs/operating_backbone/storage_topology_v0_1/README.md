# SIKK Storage Topology Contract v0.1

Purpose: define where SIKK artifacts may live, who may read them, and what cannot be mixed before GMGN/raw evidence enters the system.

This is a control-plane governance pack. It does not call GMGN, does not generate features, does not generate structure signals, and does not run replay/backtest/paper-only.

Core rule:

```text
runs/<run_id> is evidence storage, not automatic truth.
canonical/current is approved pointer space, not a scratch area.
Downstream modules must read through manifest/index/gate-approved pointers, not glob arbitrary latest files.
```

Files:

- `STORAGE_TOPOLOGY_CONTRACT.json`
- `ARTIFACT_CLASSIFICATION_MATRIX.json`
- `RUN_DIRECTORY_CONTRACT.json`
- `CANONICAL_PROMOTION_POLICY.json`
- `ARTIFACT_INDEX_POLICY.json`
- `CONTAMINATION_PREVENTION_RULES.json`
- `ACCEPTANCE_CHECKLIST.json`
- `VERSION.json`
