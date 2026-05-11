# 标准钱包数据体系目录树 V1 — 具体文件规范

## 总原则
- 只读采集与标准化分层存放。
- 每层只做自己该做的事情。
- 原始层永远保留，推断层不得反写原始层。
- 新体系以 token 为主键，以 wallet_address 为次级主键，以 analysis_id / batch_id 串联。

## 1. ingest/

### 1.1 raw/
放原始输入，不做分析。

建议文件：
- `gmgn_wallet_rows_raw.json`
- `gmgn_wallet_trade_input.json`
- `gmgn_wallet_profile_input.json`
- `snapshot_YYYYMMDDTHHMMSSZ.json`
- `delta_YYYYMMDDTHHMMSSZ__YYYYMMDDTHHMMSSZ.json`
- `raw_api_response.json`
- `raw_csv_import.csv`
- `raw_ocr_text.txt`

### 1.2 source_packets/
放原始输入包，便于多轮 AI 读取。

建议文件：
- `source_packet_<analysis_id>.json`
- `wallet_source_packet_<token>.json`
- `token_source_packet_<token>.json`

### 1.3 manifests/
放采集来源、hash、时间、批次。

建议文件：
- `ingest_manifest_<analysis_id>.json`
- `source_manifest_<batch_id>.json`
- `capture_manifest_<token>.json`

### 1.4 staging/
放轻度标准化但还未进入事实层的数据。

建议文件：
- `raw_snapshot_staged.csv`
- `raw_snapshot_staged.jsonl`
- `field_map_staged.json`

## 2. facts/

### 2.1 wallet_entity/
放钱包实体事实。

建议文件：
- `wallet_entity_fact.csv`
- `wallet_entity_fact.jsonl`
- `wallet_entity_profile_normalized.json`
- `wallet_entity_summary.md`

### 2.2 wallet_trade/
放交易事实。

建议文件：
- `wallet_trade_fact.csv`
- `wallet_trade_fact.jsonl`
- `wallet_trade_normalized.json`
- `wallet_trade_summary.md`

### 2.3 wallet_state/
放状态事实。

建议文件：
- `wallet_state_fact.csv`
- `wallet_state_fact.jsonl`
- `wallet_status.json`
- `wallet_state_summary.md`

### 2.4 token_facts/
放代币事实。

建议文件：
- `token_fact.csv`
- `token_fact.jsonl`
- `token_profile.json`
- `token_state.json`

## 3. evidence/

### 3.1 same_source/
放同源候选证据。

建议文件：
- `same_source_evidence.json`
- `same_source_evidence.csv`
- `same_source_group_summary.md`

### 3.2 funding_path/
放资金路径证据。

建议文件：
- `funding_path_evidence.json`
- `funding_path_graph.json`
- `funding_path_summary.md`

### 3.3 token_transfer/
放 Token 转入/转出证据。

建议文件：
- `token_transfer_evidence.json`
- `token_transfer_evidence.csv`
- `token_transfer_summary.md`

### 3.4 counterparty_evidence/
放对手盘证据。

建议文件：
- `counterparty_evidence.json`
- `counterparty_pressure_summary.md`
- `counterparty_evidence.csv`

## 4. inference/

### 4.1 wallet_structure/
放钱包结构推断结果。

建议文件：
- `wallet_structure_decision.json`
- `wallet_structure_summary.md`
- `wallet_structure_score.csv`
- `candidate_wallet_structure_summary.json`

### 4.2 role_classification/
放角色分类。

建议文件：
- `wallet_role_classification.json`
- `wallet_role_classification.csv`
- `role_classification_summary.md`

### 4.3 behavior_inference/
放行为推断。

建议文件：
- `behavior_inference.json`
- `behavior_inference.csv`
- `behavior_summary.md`

### 4.4 lifecycle/
放生命周期判断。

建议文件：
- `candidate_states.json`
- `dominant_lifecycle.json`
- `lifecycle_summary.md`

### 4.5 chip_control/
放筹码控制权状态。

建议文件：
- `chip_control_state.json`
- `chip_control_summary.md`
- `control_transition_log.jsonl`

## 5. handoff/

### 5.1 bot2/
放 bot 间交接包。

建议文件：
- `bot2_handoff_packet.json`
- `bot2_handoff_summary.md`

### 5.2 case_packet/
放 case 交接包。

建议文件：
- `case_packet.json`
- `case_packet.md`
- `case_packet_index.json`

### 5.3 telegram_packet/
放 Telegram 展示包。

建议文件：
- `telegram_packet.json`
- `telegram_packet.md`
- `telegram_view_payload.json`

### 5.4 review_packet/
放复核交接包。

建议文件：
- `review_packet.json`
- `review_packet.md`
- `review_ticket.json`

## 6. reports/

### 6.1 summary/
放总览报告。

建议文件：
- `project_summary.md`
- `wallet_summary.md`
- `system_summary.md`

### 6.2 case/
放单 token case 报告。

建议文件：
- `case_<token>.md`
- `case_<token>.json`
- `case_<token>_appendix.md`

### 6.3 daily/
放日报。

建议文件：
- `daily_report_YYYYMMDD.md`
- `daily_report_YYYYMMDD.json`
- `daily_report_YYYYMMDD.csv`

### 6.4 audit/
放审计报告。

建议文件：
- `audit_report_YYYYMMDD.md`
- `audit_report_YYYYMMDD.json`
- `audit_findings.csv`

### 6.5 dashboard/
放看板输出。

建议文件：
- `dashboard_data.json`
- `dashboard_summary.md`
- `dashboard_cards.jsonl`

## 7. index/

建议文件：
- `system_index.json`
- `token_index.json`
- `wallet_index.json`
- `handoff_index.json`
- `report_index.json`
- `search_index.json`
- `route_index.json`

## 8. 文件命名约束

- token 维度统一使用 `token_address` 作为主键。
- 钱包维度统一使用 `wallet_address` 作为主键。
- 批次维度统一使用 `analysis_id` 或 `batch_id`。
- 报告文件尽量使用 `YYYYMMDD` 或 `token` 后缀。
- JSON 用于机器读取，MD 用于人类阅读，CSV 用于表格导出。
- 原始文件不得被推断文件覆盖。

## 9. 最小落地优先级

先落这 8 类文件：
1. `ingest/manifests/`
2. `ingest/raw/`
3. `facts/wallet_entity/`
4. `facts/wallet_trade/`
5. `evidence/same_source/`
6. `inference/wallet_structure/`
7. `handoff/bot2/`
8. `reports/case/`

## 10. 结论

这个目录树的核心不是“多放文件”，而是把旧系统里的混杂数据拆成可回溯、可重建、可复盘的七层结构。
