# Phase 01 Acceptance Standard

## 必须生成的目录

- `schemas/stable_trader_os/phase_01_data_fact/`
- `configs/stable_trader_os/phase_01_data_fact/`
- `contracts/stable_trader_os/phase_01_data_fact/`
- `examples/stable_trader_os/phase_01_data_fact/`
- `tests/stable_trader_os/phase_01_data_fact/`

## 必须生成的 Schema

- phase_01_field_schema.json
- token_fact_schema.json
- wallet_fact_table_schema.json
- trade_fact_table_schema.json
- holder_fact_table_schema.json
- transfer_fact_table_schema.json
- kline_fact_table_schema.json
- quote_fact_schema.json
- security_fact_schema.json
- phase_01_quality_gate_schema.json

## 必须生成的 Config

- source_capability_matrix.json
- field_source_priority.json
- missing_field_policy.json
- quality_gate_rules.json
- anomaly_detection_rules.json
- unit_normalization_rules.json
- time_normalization_rules.json
- legacy_bridge_registry.json

## 必须生成的 Contract

- phase_01_input_contract.json
- phase_01_output_contract.json
- phase_01_to_phase_02_contract.json
- phase_01_forbidden_judgement_contract.md

## 必须生成的 Example

- mock_phase_01_input.json
- mock_raw_gmgn_traders.json
- mock_raw_gmgn_holders.json
- mock_raw_kline.json
- expected_token_fact.json
- expected_wallet_fact_table.csv
- expected_trade_fact_table.csv
- expected_phase_01_quality_gate.json

## 必须生成的 Test

- test_phase_01_schema_validation.py
- test_phase_01_missing_field_policy.py
- test_phase_01_quality_gate.py
- test_phase_01_handoff_contract.py
- test_phase_01_forbidden_judgement.py

## 禁止判断清单

Phase 01 禁止输出市场解释、机会判断、交易信号、主导侧意图判断。

## 验收命令

```bash
cd /root/sikk-gmgn && python3 -m pytest tests/stable_trader_os/phase_01_data_fact -q
```

## 验收失败处理

- Schema 缺字段：补 schema，不改测试绕过。
- Contract 指向错误阶段：修正到 `phase_02_wallet_structure_controller`。
- 旧目录策略错误：恢复 read_only_keep_in_place。
- 出现交易判断词：移除越级判断，只保留 forbidden contract 中的禁止清单。
