# SIKK Stable Trader OS System Data Registry v2.0 Audit Report

- system: SIKK Stable Trader OS
- root: `/root/sikk-gmgn/sikk_stable_trader_os/`
- generated_at: 2026-05-11T02:27:39Z
- audit_verdict: `SYSTEM_DATA_REGISTRY_V2_ACCEPTED`
- task_boundary: 本任务只建立 HER 可执行的系统数据注册层；不编写交易判断逻辑；不把阶段说明文档当作完成。

## 1. 验收结论

`PASS`

系统数据注册层已满足本次验收标准：目录完整、10 个系统注册文件完整、P00-P09 顺序/依赖/输入输出关系可读、状态码/证据等级/hard negative/目录边界已注册，并建立了 validator 与下一步 P01_data_fact phase package 计划。

## 2. 目录验收

- `00_system_registry/`: system data registry; source for HER global read order；边界：write only registry yaml/json; no runtime facts; no reports as judgement source
- `01_total_control_skill/`: thin master control entry mirror/reference；边界：route/control only; no detailed trading logic
- `02_phase_controllers/`: phase runtime task packages；边界：each phase owns manifest/context/objective/contracts/protocol/gate/state/handoff_schema
- `03_atomic_skills/`: atomic capability registrations/candidate specs；边界：candidate reusable capabilities only; cannot bypass phase controller
- `04_schemas/`: local schema mirrors/indexes；边界：schema definitions only; no generated token reports
- `05_contracts/`: local contract mirrors/indexes；边界：I/O and handoff contracts only
- `06_tools/`: runners validators replay report builders；边界：deterministic tools only; no secret/sign/swap tool
- `07_runtime_state/`: current status, active task, runtime logs, errors；边界：machine state source; JSON/JSONL preferred
- `08_handoff_packets/`: phase/skill/final handoff outputs；边界：machine handoff packets only; schema validated before downstream
- `09_reports/`: human-readable reports generated from JSON/audit；边界：not allowed as machine judgement input
- `10_tests/`: fixtures/unit/integration/replay validation；边界：tests and fixtures only

## 3. 系统注册文件验收

共 10 个：

- `00_system_registry/atomic_skill_registry.yaml`
- `00_system_registry/contract_registry.yaml`
- `00_system_registry/directory_registry.yaml`
- `00_system_registry/evidence_registry.yaml`
- `00_system_registry/hard_negative_registry.yaml`
- `00_system_registry/phase_registry.yaml`
- `00_system_registry/schema_registry.yaml`
- `00_system_registry/status_code_registry.yaml`
- `00_system_registry/system_manifest.yaml`
- `00_system_registry/tool_registry.yaml`

## 4. Phase Registry 验收

Phase Controller 已定义为可调度阶段运行单元，而不是 Markdown 模板。全局规则：

- all_phases_are_schedulable_units: `True`
- acceptance_gate_decides_completion: `True`
- handoff_packet_required_for_downstream: `True`
- missing_required_fact_policy: `do_not_infer; mark_gap_or_block_by_contract`
- report_policy: `human_readable_only; never_machine_judgement_source`

P00-P09 顺序：

- `P00` `P00_system_boundary` → next: `P01_data_fact`；input: `system_boundary_input.json`；output: `system_boundary_handoff_packet.json`
- `P01` `P01_data_fact` → next: `P02_wallet_structure`；input: `token_or_run_raw_input.json`；output: `phase_01_to_phase_02_handoff_packet.json`
- `P02` `P02_wallet_structure` → next: `P03_chip_control`；input: `phase_01_to_phase_02_handoff_packet.json`；output: `phase_02_to_phase_03_handoff_packet.json`
- `P03` `P03_chip_control` → next: `P04_scenario_recognition`；input: `phase_02_to_phase_03_handoff_packet.json`；output: `phase_03_to_phase_04_handoff_packet.json`
- `P04` `P04_scenario_recognition` → next: `P05_structure_position`；input: `phase_03_to_phase_04_handoff_packet.json`；output: `phase_04_to_phase_05_handoff_packet.json`
- `P05` `P05_structure_position` → next: `P06_strategy_gate`；input: `phase_04_to_phase_05_handoff_packet.json`；output: `phase_05_to_phase_06_handoff_packet.json`
- `P06` `P06_strategy_gate` → next: `P07_execution_risk`；input: `phase_05_to_phase_06_handoff_packet.json`；output: `phase_06_to_phase_07_handoff_packet.json`
- `P07` `P07_execution_risk` → next: `P08_review_learning`；input: `phase_06_to_phase_07_handoff_packet.json`；output: `phase_07_to_phase_08_handoff_packet.json`
- `P08` `P08_review_learning` → next: `P09_system_upgrade`；input: `phase_07_to_phase_08_handoff_packet.json`；output: `phase_08_to_phase_09_handoff_packet.json`
- `P09` `P09_system_upgrade` → next: `None`；input: `phase_08_to_phase_09_handoff_packet.json`；output: `phase_09_final_audit_packet.json`

每个阶段强制九件套：

- `phase_manifest.yaml`
- `phase_context_pack.md`
- `phase_objective_tree.yaml`
- `phase_input_contract.json`
- `phase_output_contract.json`
- `phase_execution_protocol.md`
- `phase_acceptance_gate.yaml`
- `phase_state.json`
- `phase_handoff_packet.schema.json`

## 5. Status Code Registry 验收

状态码数量：23

关键闭环规则：

- complete: `PHASE_RUNNING -> ACCEPTANCE_PASS -> HANDOFF_READY -> PHASE_READY`
- warning: `PHASE_RUNNING -> ACCEPTANCE_PASS_WITH_WARNING -> HANDOFF_READY -> PHASE_WITH_GAPS`
- pause: `any -> ACCEPTANCE_PAUSE/PHASE_PAUSED/HANDOFF_BLOCKED`
- block: `any -> ACCEPTANCE_BLOCK/PHASE_BLOCKED/DATA_INVALID`
- forbidden: `PHASE_READY without HANDOFF_READY; DATA_INVALID with downstream advance; report-only completion`

## 6. Evidence Registry 验收

证据等级：

- `EVIDENCE_A_STRONG`: machine-validated source + schema/contract pass + counter-evidence checked
- `EVIDENCE_B_MEDIUM`: source present and normalized but partial validation or optional context missing
- `EVIDENCE_C_WEAK`: incomplete source or degraded derivation
- `EVIDENCE_D_INSUFFICIENT`: missing or conflicted source
- `EVIDENCE_X_COUNTER`: counter evidence or invalidation evidence

强制记录字段：

- `field_name`
- `field_source`
- `source_path_or_api`
- `evidence_level`
- `counter_evidence`
- `missing`
- `normalization_rule`
- `acceptance_gate_ref`
- `audit_ref`

## 7. Hard Negative Registry 验收

全局硬否定规则数量：14

继承规则：`hard negatives are inherited downstream and cannot be erased by narrative scores`

- `DATA_INVALID` [P01+] 关键事实无效、冲突或无法解析 → write_gap_and_stop_downstream
- `WALLET_BLOCK` [P02+] 钱包结构出现不可接受风险实体/黑名单/伪造结构 → inherit_and_recheck_downstream
- `ACTIVE_DISTRIBUTION` [P03+] 活跃派发/出货结构成立 → inherit_as_negative
- `TRANSFER_TO_COUNTERPARTY` [P02+] 关键地址向对手盘/可疑归集转移 → inherit_as_negative
- `STRUCTURE_COLLAPSE` [P05+] 结构支撑崩塌 → stop_strategy_gate
- `SCENARIO_BLOCK` [P04+] 盘型场景触发阻断 → stop_downstream
- `SCENARIO_TRAP_RISK` [P04+] 陷阱/诱多风险 → observe_only
- `SCENARIO_DISTRIBUTION_RISK` [P04+] 派发风险场景 → observe_only_or_block
- `COMPLETION_FAIL` [P08+] 复盘目标失败且不可解释 → requires_review
- `FATIGUE_BLOCK` [P07+] 连续执行疲劳或风险预算耗尽 → stop_execution
- `POSITION_OVEREXTENDED` [P07+] 仓位/暴露超界 → stop_execution
- `STRATEGY_BLOCK` [P06+] 策略门禁拒绝 → no_execution
- `EXECUTION_BLOCK` [P07+] 执行安全条件不满足 → no_execution
- `REGRESSION_TEST_FAIL` [P09] 系统升级/回归测试失败 → do_not_promote

## 8. 机器判断边界

允许机器判断来源：

- input_contract
- output_contract
- schemas
- normalized_json
- runtime_trace
- acceptance_gate_result
- handoff_packet

禁止机器判断来源：

- human_markdown_report
- ai_guess
- unverified_missing_field
- downstream_inference_before_handoff

## 9. 安全边界

- 不执行真实 swap
- 不读取/写入/保存私钥
- 不自动签名
- 不 broadcast
- `BLOCK_REAL_TRADE` 为默认安全状态，不能被阶段分数解除

## 10. 下一步

下一步只允许建立 `P01_data_fact` 的可执行 phase package / runner：读取系统 registry → 读取 P01 九件套 → 运行数据事实验收 → 写入 phase_state → 生成 handoff_packet。不得跳过 P01 直接进入 P02-P09 的交易判断。
