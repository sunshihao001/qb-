# Next Step Plan: Build P01_data_fact Phase Package

- generated_at: 2026-05-11T02:27:39Z
- current_verdict: `SYSTEM_DATA_REGISTRY_V2_ACCEPTED`
- next_allowed_work: `P01_data_fact_phase_package_runtime_runner`

## 1. 下一步目标

建立 `P01_data_fact` 的 HER 可执行阶段包，使它能够在不做交易判断的前提下完成事实接入、字段来源绑定、证据等级标注、缺失字段处理、验收门判定、phase_state 回写和 Phase02 handoff_packet 生成。

## 2. 禁止事项

- 不输出买入/卖出/交易允许信号。
- 不识别盘型场景；场景识别属于 P04。
- 不判断钱包角色确定性；钱包结构属于 P02。
- 不用 AI 推测补全缺失字段。
- 不把 Markdown report 作为机器判断来源。
- 不绕过 acceptance_gate 进入 P02。

## 3. P01 必须读取

- `00_system_registry/system_manifest.yaml`
- `00_system_registry/phase_registry.yaml`
- `00_system_registry/status_code_registry.yaml`
- `00_system_registry/evidence_registry.yaml`
- `00_system_registry/hard_negative_registry.yaml`
- `02_phase_controllers/P01_data_fact/phase_manifest.yaml`
- `02_phase_controllers/P01_data_fact/phase_objective_tree.yaml`
- `02_phase_controllers/P01_data_fact/phase_input_contract.json`
- `02_phase_controllers/P01_data_fact/phase_output_contract.json`
- `02_phase_controllers/P01_data_fact/phase_acceptance_gate.yaml`
- `02_phase_controllers/P01_data_fact/phase_state.json`
- `02_phase_controllers/P01_data_fact/phase_handoff_packet.schema.json`

## 4. P01 必须输出

建议 runtime 输出路径：

- `07_runtime_state/phase_progress/P01/<run_id>/phase_01_fact_summary.json`
- `07_runtime_state/phase_progress/P01/<run_id>/field_source_map.json`
- `07_runtime_state/phase_progress/P01/<run_id>/phase_01_gap_list.json`
- `07_runtime_state/phase_progress/P01/<run_id>/acceptance_gate_result.json`
- `08_handoff_packets/phase_handoff/P01_to_P02/<run_id>/phase_01_to_phase_02_handoff_packet.json`
- `09_reports/phase_reports/P01/<run_id>/phase_01_data_fact_report.md`

## 5. P01 状态机

`PHASE_NOT_STARTED -> PHASE_INPUT_LOADED -> PHASE_RUNNING -> ACCEPTANCE_PASS/ACCEPTANCE_PASS_WITH_WARNING/ACCEPTANCE_PAUSE/ACCEPTANCE_BLOCK -> HANDOFF_READY/HANDOFF_BLOCKED -> PHASE_READY/PHASE_WITH_GAPS/PHASE_PAUSED/PHASE_BLOCKED`

## 6. P01 验收门

P01 只有在以下条件满足时才能向 P02 交接：

1. input_contract 可解析。
2. required facts 不被 AI 猜测填充。
3. 每个输出字段包含 `field_source` 与 `evidence_level`。
4. counter_evidence 已检查并记录。
5. hard_negative 检查已执行。
6. `phase_01_to_phase_02_handoff_packet.json` 通过 schema。
7. `phase_state.json` 已回写为 `PHASE_READY` 或允许继承缺口的 `PHASE_WITH_GAPS`。

## 7. 建议验证命令

```bash
python3 /root/sikk-gmgn/sikk_stable_trader_os/06_tools/validators/validate_system_registry.py
python3 -m pytest tests/test_sikk_ca_runtime_pipeline.py tests/test_sikk_ca_phase_evidence_runner.py -q
```

## 8. 下一波完成定义

`P01_EXECUTABLE_PHASE_PACKAGE_READY_WITH_FIXTURE_PASS`

只有达到该定义，才继续专业化 P02 wallet structure。
