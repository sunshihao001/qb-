# HER_DOC S02 闭环任务包：runner registry 与 phase binding closure

## 0. 本轮任务定位
- task_name: `S02_runner_registry_and_phase_binding_closure`
- source_previous_stage: `S01_runtime_absorption_single_token_replay`
- previous_status: `S01_READY_WITH_GAPS`
- 目标：把 S01 已扫描登记的真实 runtime runner 从报告草案推进到 HER / Stable Trader OS 可消费的正式控制面资产草案，并通过 HER_DOC safe-mode 管线形成 K00/F00/V00/A00/H00/U00/G00 证据。
- 边界：safe-mode、paper-only、document-governance + control-binding only；不触发真实 swap、不签名、不 broadcast、不声明 production ready。

## 1. 输入证据
- S01_acceptance_report: `reports/her_doc_full_system_gap_scan/S01_runtime_absorption_single_token_replay/S01_acceptance_report.md`
- S01_runtime_asset_inventory: `reports/her_doc_full_system_gap_scan/S01_runtime_absorption_single_token_replay/S01_runtime_asset_inventory.yaml`
- S01_runner_absorption_map: `reports/her_doc_full_system_gap_scan/S01_runtime_absorption_single_token_replay/S01_runner_absorption_map.yaml`
- S01_phase_runner_binding_draft: `reports/her_doc_full_system_gap_scan/S01_runtime_absorption_single_token_replay/S01_phase_runner_binding_draft.yaml`
- S01_single_token_replay_result: `reports/her_doc_full_system_gap_scan/S01_runtime_absorption_single_token_replay/S01_single_token_replay_result.yaml`
- S01_issue_registry: `reports/her_doc_full_system_gap_scan/S01_runtime_absorption_single_token_replay/S01_issue_registry.yaml`
- S01_task_packets: `reports/her_doc_full_system_gap_scan/S01_runtime_absorption_single_token_replay/S01_task_packets.yaml`
- S00 unified standard: `system/unified_standardization/`
- HER-DFAFS controllers: `system/her_document_function_system/controllers/`
- Stable Trader OS phase controllers: `sikk_stable_trader_os/02_phase_controllers/`

## 2. 必须关闭或降级的 S01 gap
1. `ISSUE_S01_003`: formal runner registry / phase binding missing。
2. `ISSUE_S01_004`: runtime phase trace matrix missing。
3. `ISSUE_S01_005`: runtime acceptance evidence binder missing。
4. `ISSUE_S01_006`: handoff consumption status missing。
5. `ISSUE_S01_007`: P08 permission ticket contract not proven。
6. `ISSUE_S01_009`: P10 upgrade candidate / shadow validation / regression / rollback not proven。

## 3. HER_DOC 处理流程

### O00
- 建立本轮 S02 run。
- 不允许把 S01_READY_WITH_GAPS 升格为 ACCEPTED。
- 调度 K00/F00/V00/A00/H00/U00/G00 safe-mode 输出。

### K00
- 摄取本文件与 operator goal。
- 将 S01 产物作为 evidence_refs。
- 生成 S02 document passport、system mapping、corpus index、handoff packet。

### F00
- 将 S01 runner draft 转成正式控制面资产任务：
  - `sikk_stable_trader_os/07_runners/runner_registry.yaml`
  - `sikk_stable_trader_os/07_runners/phase_runner_binding.yaml`
  - `sikk_stable_trader_os/00_trace/runtime_phase_trace_matrix.yaml`
  - `sikk_stable_trader_os/08_acceptance/runtime_acceptance_result.yaml`
  - `sikk_stable_trader_os/09_handoff/handoff_consumption_status.yaml`
  - `sikk_stable_trader_os/11_permission_gate_p08/p08_permission_ticket.schema.json`
  - `sikk_stable_trader_os/12_review_upgrade_p09_p10/p10_upgrade_candidate_shadow_package.yaml`

### V00
- 验证文件存在、YAML/JSON 可解析。
- 验证每个 runner 绑定 phase、input/output evidence、paper-only boundary。
- 验证 P08 permission ticket 是 P07→P08→paper runner 的前置 gate。
- 验证 P09/P10 只生成 candidate/shadow/rollback，不直接修改实时规则。

### A00
- 文件级：目标文件存在。
- 结构级：runner、phase、trace、acceptance、handoff、P08、P10 资产齐全。
- 语义级：runner 不绕过 Phase Controller，paper runner 不绕过 P08。
- 消费级：本轮只允许证明 control-binding draft 可消费；未实跑完整 live pipeline 则保持 READY_WITH_GAPS。
- 运行级：safe-mode 验证通过；不得声明 production/live accepted。

### H00
- 输出下一轮队列：
  - S03: 用 formal registry 驱动单 token phase-controller replay。
  - S04: wallet_structure canonical summary 修复。
  - S05: P10 shadow validation / regression / rollback 执行验证。

### U00/G00
- U00: 把 S01 gap 根因沉淀为 review case 和 upgrade candidates。
- G00: 生成候选治理规则：任何 runtime runner 必须有 phase binding、trace、acceptance、handoff、permission boundary。

## 4. 禁止事项
- 不执行真实交易、真实 swap、真实下单。
- 不读取/写入/保存私钥。
- 不签名，不 broadcast。
- 不破坏 legacy runtime，只登记、包装、绑定、收编。
- 不让 paper runner 绕过 P08 permission gate。
- 不让 P09/P10 复盘结果直接修改实时规则。
- 不把 READY_WITH_GAPS 声称为 ACCEPTED。

## 5. 预期状态
- 合法预期：`S02_CONTROL_BINDING_READY_WITH_GAPS` 或 `HER_DOC_FUNCTION_PIPELINE_RUNNABLE_WITH_GAPS`。
- 只有在 formal asset 文件存在、解析通过、且 safe-mode 验证通过时，才允许声明 S02 控制面绑定草案完成。
- 仍不得声明 `LIVE_READY`、`PRODUCTION_READY`、`PIPELINE_ACCEPTED`。
