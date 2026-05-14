# Phase 01 Professional Data Design Report

生成时间：2026-05-09T04:37:57Z

## 1. 新增/更新文件列表

- `schemas/stable_trader_os/phase_01_data_fact/phase_01_field_schema.json`
- `docs/stable_trader_os/schemas/phase_01_field_schema.md`
- `schemas/stable_trader_os/phase_01_data_fact/token_fact_schema.json`
- `schemas/stable_trader_os/phase_01_data_fact/wallet_fact_table_schema.json`
- `schemas/stable_trader_os/phase_01_data_fact/trade_fact_table_schema.json`
- `schemas/stable_trader_os/phase_01_data_fact/holder_fact_table_schema.json`
- `schemas/stable_trader_os/phase_01_data_fact/transfer_fact_table_schema.json`
- `schemas/stable_trader_os/phase_01_data_fact/kline_fact_table_schema.json`
- `schemas/stable_trader_os/phase_01_data_fact/quote_fact_schema.json`
- `schemas/stable_trader_os/phase_01_data_fact/security_fact_schema.json`
- `schemas/stable_trader_os/phase_01_data_fact/phase_01_quality_gate_schema.json`
- `configs/stable_trader_os/phase_01_data_fact/source_capability_matrix.json`
- `configs/stable_trader_os/phase_01_data_fact/field_source_priority.json`
- `configs/stable_trader_os/phase_01_data_fact/missing_field_policy.json`
- `configs/stable_trader_os/phase_01_data_fact/quality_gate_rules.json`
- `configs/stable_trader_os/phase_01_data_fact/anomaly_detection_rules.json`
- `configs/stable_trader_os/phase_01_data_fact/unit_normalization_rules.json`
- `configs/stable_trader_os/phase_01_data_fact/time_normalization_rules.json`
- `configs/stable_trader_os/phase_01_data_fact/legacy_bridge_registry.json`
- `contracts/stable_trader_os/phase_01_data_fact/phase_01_input_contract.json`
- `contracts/stable_trader_os/phase_01_data_fact/phase_01_output_contract.json`
- `contracts/stable_trader_os/phase_01_data_fact/phase_01_to_phase_02_contract.json`
- `contracts/stable_trader_os/phase_01_data_fact/phase_01_forbidden_judgement_contract.md`
- `schemas/shared/stable_trader_os/phase_01_to_phase_02_handoff_schema.json`
- `examples/stable_trader_os/phase_01_data_fact/mock_phase_01_input.json`
- `examples/stable_trader_os/phase_01_data_fact/mock_raw_gmgn_traders.json`
- `examples/stable_trader_os/phase_01_data_fact/mock_raw_gmgn_holders.json`
- `examples/stable_trader_os/phase_01_data_fact/mock_raw_kline.json`
- `examples/stable_trader_os/phase_01_data_fact/expected_token_fact.json`
- `examples/stable_trader_os/phase_01_data_fact/expected_wallet_fact_table.csv`
- `examples/stable_trader_os/phase_01_data_fact/expected_trade_fact_table.csv`
- `examples/stable_trader_os/phase_01_data_fact/expected_phase_01_quality_gate.json`
- `docs/stable_trader_os/phases/phase_01_professional_data_design.md`
- `docs/stable_trader_os/phases/phase_01_acceptance_standard.md`
- `tests/stable_trader_os/phase_01_data_fact/test_phase_01_schema_validation.py`
- `tests/stable_trader_os/phase_01_data_fact/test_phase_01_missing_field_policy.py`
- `tests/stable_trader_os/phase_01_data_fact/test_phase_01_quality_gate.py`
- `tests/stable_trader_os/phase_01_data_fact/test_phase_01_handoff_contract.py`
- `tests/stable_trader_os/phase_01_data_fact/test_phase_01_forbidden_judgement.py`
- `data/stable_trader_os/runs/mock_phase_01_run_001/01_data_fact/audit/phase_01_runtime_trace.jsonl`

## 2. 新增目录列表

- `schemas/stable_trader_os/phase_01_data_fact/`
- `configs/stable_trader_os/phase_01_data_fact/`
- `contracts/stable_trader_os/phase_01_data_fact/`
- `examples/stable_trader_os/phase_01_data_fact/`
- `tests/stable_trader_os/phase_01_data_fact/`
- `data/stable_trader_os/runs/mock_phase_01_run_001/01_data_fact/audit/`

## 3. 每类文件用途

- Schema：固定字段解释权、类型、来源、缺失值、下游使用者。
- Config：固定来源能力、来源优先级、missing 策略、质量门禁、异常处理、旧目录只读桥接。
- Contract：固定 Phase 01 输入、输出、Phase 02 handoff 与禁止判断。
- Example：提供 mock 输入与 expected 输出，支持离线验收。
- Test：防止只写文档，不验证系统数据是否可运行。
- Runtime trace：定义每次执行的步骤级状态沉淀格式。

## 4. Phase 01 当前专业化完成度

状态：`SYSTEM_DATA_PACKAGE_READY`

说明：已完成 HER 可读取的系统数据包；当前尚未实现真实采集/标准化 runtime module。

## 5. 尚未实现的代码部分

- 真实 GMGN/chain/quote/security collector。
- raw -> normalized 的 Phase 01 runner。
- anomaly_fields_report.csv 自动生成器。
- phase_01_to_phase_02_handoff_packet.json 自动写入器。

## 6. 尚未接入的数据源

- GMGN 实时接口：未在本轮接入。
- Solana RPC / explorer：未在本轮接入。
- Quote/security API：未在本轮接入。

## 7. 与旧目录兼容方式

旧目录 `/root/sikk-gmgn/data/gmgn_candidates_live_run` 保持 `read_only_keep_in_place`：不移动、不删除、不作为新 Phase 01 主写路径。

## 8. 是否允许进入 Phase 02

系统设计层面：允许进入 Phase 02 控制器设计。
真实 token 运行层面：必须先由 Phase 01 runner 生成 `phase_01_quality_gate.json`，且状态为 `PASS` 或 `PASS_WITH_WARNING`。

目标阶段：`phase_02_wallet_structure_controller`。

## 9. 下一步建议

1. 运行 pytest 验收。
2. 若通过，补 Phase 01 runner / validator。
3. 用 mock 数据跑出真实 `01_data_fact/` 目录。
4. 再进入 Phase 02 结构地址层控制器，不直接进入场景识别。


## 11. 按系统总目标与阶段目标补充（2026-05-09T04:47:35Z）

本轮新增目标对齐层，确保 Phase 01 不只是字段包，而是服务 Stable Trader OS 总目标的事实质量门禁。

新增资产：

- `docs/stable_trader_os/phases/phase_01_system_goal_alignment.md`
- `contracts/stable_trader_os/phase_01_data_fact/phase_01_goal_passport.json`
- `configs/stable_trader_os/phase_01_data_fact/phase_01_state_machine.json`
- `configs/stable_trader_os/phase_01_data_fact/phase_01_goal_to_quality_gate_matrix.json`
- `contracts/stable_trader_os/phase_01_data_fact/phase_01_acceptance_matrix.json`
- `docs/stable_trader_os/phases/phase_01_runtime_asset_index.md`
- `tests/stable_trader_os/phase_01_data_fact/test_phase_01_goal_alignment.py`
- `tests/stable_trader_os/phase_01_data_fact/test_phase_01_state_machine.py`

新增验收点：

- Phase 01 总目标护照存在。
- Phase 01 状态机存在。
- Phase 01 completion 只能进入 `phase_02_wallet_structure_controller`。
- fatal missing / source conflict / forbidden judgement 均可阻断。
- 接受矩阵把 schema、config、contract、example、test、runtime trace、goal passport 统一纳入完成定义。
