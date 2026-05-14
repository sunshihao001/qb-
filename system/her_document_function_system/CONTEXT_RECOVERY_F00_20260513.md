# HER-DFAFS / F00 Context Recovery Anchor

created_at: 2026-05-13T13:17:39.542987Z
recovery_reason: 用户重置后请求恢复文档系统上下文到 F00 标准阶段文件包 + SIKK 集成目录位置。

## Canonical Root

`/root/sikk-gmgn/system/her_document_function_system/`

该路径下 README 明确声明：

- Controllers: `/root/sikk-gmgn/system/her_document_function_system/controllers/`
- Runtime data: `/root/sikk-gmgn/data/her_document_function_system/`
- F00 controller: `/root/sikk-gmgn/system/her_document_function_system/controllers/F00_function_realization_controller/`
- Legacy standalone root `/root/her_document_function_system/` retained as reference/bootstrap material.

## F00 Controller Canonical Path

`/root/sikk-gmgn/system/her_document_function_system/controllers/F00_function_realization_controller/`

## Verified Shape

- file_count: 20
- json_files: 11
- json_errors: []
- state.status: `NOT_EXECUTED`
- state.phase_id: `F00`

## Files

- `00_f00_controller_design_v1.md`
- `01_f00_manifest.yaml`
- `02_f00_context_pack.md`
- `03_f00_objective_tree.yaml`
- `04_f00_input_contract.json`
- `05_f00_output_contract.json`
- `06_f00_execution_protocol.md`
- `07_f00_acceptance_gate.yaml`
- `08_f00_state.json`
- `09_f00_handoff_packet.schema.json`
- `10_concept_to_function_map.schema.json`
- `11_function_asset_plan.schema.json`
- `12_field_model.schema.json`
- `13_rule_logic.schema.json`
- `14_implementation_decision.schema.json`
- `15_test_replay_evidence.schema.json`
- `16_runner_binding.schema.json`
- `17_recovery_policy.md`
- `18_trace_audit_spec.yaml`
- `19_f00_final_report_template.md`


## Current Truthful Status

- `F00_STANDARD_FILE_PACKAGE_WRITTEN`
- `SIKK_CANONICAL_INTEGRATION_PATH_EXISTS`
- `F00_JSON_SCHEMA_FILES_PARSE_OK`
- `F00_STATE_NOT_EXECUTED`

Do not claim yet:

- `F00_EXECUTED`
- `FUNCTION_MAPPED`
- `TESTED`
- `REPLAY_TESTED`
- `RUNNER_BOUND`
- `ACCEPTANCE_PASSED`

## Important Context Restored

F00 is the HER-DFAFS Function Realization Controller. It is not a document summarizer. It receives K00 accepted/ready-with-gaps materials and converts them into function requirements, field models, rule logic, schema/contract requirements, implementation decisions, asset plans, test/replay requirements, runner binding requirements, trace/audit requirements, acceptance evidence, and downstream handoff.

F00 must rely on formal inputs/state/handoff, not chat context.

## Directory Difference / Recovery Note

There are two F00 roots present:

1. Canonical SIKK-integrated root:
   `/root/sikk-gmgn/system/her_document_function_system/controllers/F00_function_realization_controller/`
   - 20 files, 11 JSON, no JSON parse errors.
   - This is the active canonical root for new controller assets.

2. Legacy/bootstrap standalone root:
   `/root/her_document_function_system/04_function_realization/F00_function_realization_controller/`
   - Retained as reference/bootstrap material.
   - Do not treat it as the new canonical SIKK write path unless explicitly migrating/syncing.

## Next Safe Entry

Next professional step is not theory expansion. It is one of:

1. Sync latest stricter F00 input contract rules into the canonical SIKK path if needed.
2. Create minimal executable F00 validator/runner under SIKK canonical system path.
3. Add replay fixture and tests proving F00 contract validation behavior.
4. Generate an F00 acceptance/handoff sample from a real K00 handoff packet.

Recommended next route:

`F00_CONTRACT_SYNC_AND_VALIDATOR_RUNNER_IMPLEMENTATION`

Boundary: still no live runtime, no wallet signing, no auto deploy, no production rule direct change.
