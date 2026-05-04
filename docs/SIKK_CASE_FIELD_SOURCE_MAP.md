# SIKK Case File 字段来源映射 v1.0

边界：本映射只用于 paper case 数据补全、证据回填、展示与复盘；不执行真实 swap、不读取私钥、不签名、不广播。

## 来源优先级

1. `paper_live/paper_positions_open.json` / `paper_positions_closed.json`
2. `state_machine/candidate_states.json`
3. `gmgn_new_token_filter/token_candidates.json`
4. `candidate_signal_outputs/candidate_signal_summary.json`
5. `wallet_structure/candidate_wallet_structure_summary.json`
6. `wallet_structure/<token>/wallet_structure_decision.json`
7. `quote_security/candidate_quote_security_summary.json`
8. `tokens/<token>/token_status.json`
9. `index/position_index.json` / `token_detail_index.json`
10. 既有 case JSON

## 字段组

- 基础字段：`position_id`、`token_symbol`、`token_address`、`status`
- 发现阶段：`candidate_discovered_at`、`discovery_source`、`discovery_price`、`discovery_market_cap_usd`、`discovery_liquidity_usd`、`discovery_holder_count`
- 信号阶段：`signal_time`、`signal_level`、`signal_type`、`signal_price`、`signal_market_cap_usd`、`signal_reason`
- 钱包结构：`wallet_decision_time`、`wallet_structure_status`、`wallet_structure_score`、`wallet_risk_score`、`counterparty_pressure_score`、`data_quality_score`
- Quote/Security：`quote_gate`、`quote_source`、`quote_price`、`gmgn_price`、`okx_price`、`price_deviation_pct`、`security_gate`
- 入场/当前/退出：`paper_entry_time`、`entry_price`、`entry_market_cap_usd`、`paper_size_sol`、`current_price`、`unrealized_pnl_pct`、`exit_time`、`net_pnl_pct`

## 输出合约

`sikk_case_field_source_map.enrich_position_for_case_file()` 输出：

- 原 position 字段
- 回填后的标准字段
- `case_field_sources`：字段 → 来源文件
- `case_missing_fields`：仍缺失字段
- `case_field_source_boundary`：paper-only 安全边界

Case File JSON/MD 额外展示：

- `case_completeness_score`
- `evidence_missing_fields`
- `strategy_review_eligible`
- `next_action`
- 字段来源追踪

## 验收命令

```bash
cd /root/sikk-gmgn
python3 -m py_compile sikk_case_field_source_map.py sikk_paper_explanation_builder.py
PYTHONPATH=. pytest -q tests/test_sikk_case_field_source_map.py tests/test_sikk_paper_explanation_builder.py -q
```
