# F00 Execution Protocol

1. Load `04_f00_input_contract.json` and validate K00 handoff input.
2. Read source references only through K00-approved refs; do not bypass raw/registry/passport chain.
3. Extract source concepts that imply system behavior, rules, fields, contracts, tests, runner entries, or handoff requirements.
4. Write `concept_to_function_map` records conforming to `10_concept_to_function_map.schema.json`.
5. For each required function, decide one implementation path: IMPLEMENT_NOW, DESIGN_ONLY, EXTEND_EXISTING, UPDATE_SCHEMA_ONLY, UPDATE_CONTRACT_ONLY, ADD_TEST_ONLY, ADD_REPORT_ONLY, ADD_KV_ONLY, ADD_TRACE_ONLY, BLOCKED_BY_MISSING_DATA, BLOCKED_BY_PRODUCTION_RISK, BLOCKED_BY_UNKNOWN_CODEBASE, DEFER_TO_DOWNSTREAM_PHASE.
6. Generate asset plans conforming to `11_function_asset_plan.schema.json`.
7. Generate test/replay evidence requirements conforming to `15_test_replay_evidence.schema.json`.
8. Update `08_f00_state.json`.
9. Generate downstream handoff conforming to `09_f00_handoff_packet.schema.json`.
10. Do not mark F00 complete unless the acceptance gate passes.

## Input Contract Gate

Before any concept extraction or function realization work, F00 must evaluate `04_f00_input_contract.json` using the following hard rules:

- No `k00_handoff_packet` → `F00_BLOCKED`.
- No `document_passport_refs` → `F00_BLOCKED`.
- No `corpus_index_refs` → `F00_BLOCKED`.
- No `system_mapping_refs` → `F00_READY_WITH_GAPS` or `F00_BLOCKED`, depending on gap severity.
- No `gap_detection_refs` → `F00_BLOCKED`.
- No `kv_retrieval_refs` → continue only with explicit `KV_GAP`; KV is auxiliary memory, not contract authority.
- No `repo_root` → `DESIGN_ONLY`.
- No `write_policy` → no file writes; `DESIGN_ONLY` only.
- No `execution_boundary` → `F00_BLOCKED`.

F00 must not read chat context as input. The legal route is K00 handoff → passport/index/mapping/gap refs → F00 contract validation → F00 execution.

## Output Contract Gate

F00 must produce file-backed outputs defined in `05_f00_output_contract.json`.

Required output assets:

- `outputs/concept_to_function_map.json`
- `outputs/implementation_decision.json`
- `outputs/repo_scan_result.json`
- `outputs/function_asset_plan.json`
- `outputs/field_model.json`
- `outputs/rule_logic.json`
- `outputs/schema_contract_plan.json`
- `outputs/patch_plan.json`
- `outputs/test_replay_plan.json`
- `outputs/runner_binding_plan.json`
- `outputs/f00_trace.jsonl`
- `outputs/f00_audit.jsonl`
- `outputs/f00_acceptance_result.json`
- `outputs/f00_to_downstream_handoff_packet.json`
- `outputs/f00_final_report.md`

Acceptance rule:

- Missing required output => `F00_OUTPUT_BLOCKED`.
- Placeholder `NOT_GENERATED` output does not satisfy acceptance.
- `f00_to_downstream_handoff_packet.json` cannot become `READY` until `f00_acceptance_result.json` is accepted.
- Chat-only output is forbidden; every required output must be present as a file.

## Document To Actual Function Requirement Mapping Gate

F00 must execute the full method wheel before claiming completion:

```text
入口识别 → K00 摄取 → 系统位置映射 → 功能需求映射 → 功能资产拆解 → 字段模型 → 判断逻辑 → schema / contract → code module → test / replay → runner binding → 功能完整性审计 → acceptance → handoff
```

Hard requirements:

1. Every explanatory concept must become at least one `required_function` or an explicit `NOT_IMPLEMENTABLE_WITH_REASON` gap.
2. Every `required_function` must declare one function type from the core enum: `NEW_FUNCTION`, `MODIFY_FUNCTION`, `ENHANCE_FUNCTION`, `HARD_BLOCK_RULE`, `SOFT_SCORE_RULE`, `STATE_MACHINE_RULE`, `SCHEMA_UPDATE`, `CONTRACT_UPDATE`, `TRACE_REQUIREMENT`, `REPORT_REQUIREMENT`, `TEST_REQUIREMENT`, `RUNNER_BINDING`, `GOVERNANCE_RULE`, `REVIEW_RULE`.
3. Every function must specify input fields, field sources, output fields, judgement logic, schema, contract, code module, tests, replay, trace, report, KV, handoff, runner binding, and acceptance criteria.
4. Missing implementation evidence must be represented as `DESIGN_ONLY`, `PLANNED_NOT_WRITTEN`, `TEST_GAP`, `REPLAY_GAP`, `RUNNER_BINDING_GAP`, or `HANDOFF_GAP`; missing evidence cannot be silently ignored.
5. `K00_ACCEPTED` is never equivalent to function completion.
6. No test evidence means no `READY`.
7. No runner binding evidence means no `RUNNABLE`.
8. No handoff packet means no downstream transition.
9. live runtime, wallet signing, and auto deploy are forbidden from this controller.

Final output must include: `doc_id`, `target_phase`, `system_mapping`, `function_mapping`, `required_functions`, `implementation_assets`, `field_model`, `rule_logic`, `schema_contract_changes`, `code_modules`, `test_replay_plan`, `runner_binding_plan`, `missing_function_audit`, `gap_list`, `acceptance_result`, `handoff_result`, `final_status`.

<!-- updated_at: 2026-05-13T14:04:37 -->
## F00 Internal Subphase Protocol

F00 must account for all internal subphases before closure:

- F00.0 Preflight Gate: validate K00 handoff, execution boundary, write policy, repo root, and forbidden scopes.
- F00.1 Repository State Scanner: scan existing controllers, schemas, contracts, tests, runners, reports, configs, legacy paths, and docs.
- F00.2 Document Function Intent Extractor: extract capability/rule/field/schema/contract/state/trace/report/runner/governance/recovery intents.
- F00.3 Concept-to-Function Compiler: compile every core concept into required_function or explicit NOT_IMPLEMENTABLE_WITH_REASON gap.
- F00.4 Implementation Decision Gate: decide IMPLEMENT_NOW, DESIGN_ONLY, EXTEND_EXISTING, UPDATE_SCHEMA_ONLY, UPDATE_CONTRACT_ONLY, ADD_TEST_ONLY, ADD_REPORT_ONLY, ADD_KV_ONLY, ADD_TRACE_ONLY, PLAN_ONLY, BLOCKED, or DEFER.
- F00.5 Function Asset Planner: decompose required_function into schema, contract, controller, module, test, replay, trace, report, KV, recovery, and handoff assets.
- F00.6 Field Model Builder: create field model with source, type, missing policy, evidence level, output targets, KV and trace flags.
- F00.7 Rule Logic Builder: create rule_id, condition, counter evidence, confidence logic, failure condition, output status, and trace requirement.
- F00.8 Schema / Contract Realization Planner: plan or update schema/contract files and validation requirements.
- F00.9 Patch / Code Realization Planner: only plan/apply patches after repo scan and write_policy; never touch live/signing/deploy paths.
- F00.10 Test / Replay Planner: define unit, schema, contract, rule, gap, handoff, failure-case and replay tests.
- F00.11 Runner Binding Planner: plan CLI/HER/orchestrator/Telegram/report/review/dashboard binding without starting live runtime.
- F00.12 Acceptance & Handoff Writer: collect evidence, preserve gaps, write acceptance result and downstream handoff.

