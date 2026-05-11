# V1.0 → V1.1 Migration Map

## Canonical V1.1 root
`/root/sikk-gmgn/hermes_harness/`

## Legacy V1.0 root
`/root/sikk-gmgn/docs/harness/ai_harness_system/`

## Migration rule
V1.0 is retained as historical documentation. V1.1 is the runtime-oriented canonical Harness root.

## Major mappings
- `00_control_plane/` → `01_control_plane/`
- `01_goals/` → `02_task_intake/`
- `04_task_plans/` + `05_execution_runs/` → `03_task_runtime/`
- `03_context_governance/*memory*` → `04_memory/`
- `10_templates/` → `05_templates/`
- `06_verification/` → `06_verification/`
- `07_recovery/` → `07_recovery/`
- `09_reports/` → `08_reports/`
- script files → `09_scripts/`
- `08_audit/` → `10_audit/`
