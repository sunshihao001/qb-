# 旧目录 → 标准钱包数据体系 映射表 V1

## 目标
把过去分散在多个旧目录里的：
- 钱包数据采集
- 钱包事实
- 同源证据
- 结构分析
- 行为推断
- handoff 包
- 报告输出
统一映射到一个新的标准数据体系。

## 新标准体系建议
```text
standard_wallet_data/
├─ ingest/
├─ facts/
├─ evidence/
├─ inference/
├─ handoff/
├─ reports/
└─ index/
```

## 1. 钱包数据采集

### 旧目录
- `data/gmgn_candidates_live_run/intel-bot/logs/wallet_structure/<token>/snapshots/`
- `data/gmgn_candidates_live_run/intel-bot/logs/wallet_structure/<token>/structure_analysis/snapshots/`
- `modules/source_wallet_bot/`
- `docs/intel_bot/`
- `钱包数据分析/sunqbfemxbot/sessions/`

### 旧文件类型
- `snapshot_*.json`
- `delta_*.json`
- `latest_delta.json`
- `gmgn_wallet_rows_raw.json`
- `gmgn_wallet_trade_input.json`
- `gmgn_wallet_profile_input.json`

### 新体系目标目录
- `standard_wallet_data/ingest/`

### 建议落点
- `ingest/raw/`：原始采集快照
- `ingest/source_packets/`：原始输入包
- `ingest/manifests/`：采集清单

### 保留原则
- 原始字段保留
- 不做结论
- 不覆盖旧采集

---

## 2. 钱包事实

### 旧目录
- `modules/wallet_structure/`
- `modules/source_wallet_bot/`
- `data/gmgn_candidates_live_run/wallet_structure/<token>/structure_analysis/`
- `data/gmgn_candidates_live_run/tokens/*/token_status.json`

### 旧文件类型
- `wallet_trade_normalized.json`
- `wallet_entity_profile_normalized.json`
- `wallet_structure_decision.json`
- `candidate_wallet_structure_summary.json`
- `token_status.json`

### 新体系目标目录
- `standard_wallet_data/facts/`

### 建议落点
- `facts/wallet_entity/`
- `facts/wallet_trade/`
- `facts/wallet_state/`

### 保留原则
- 一行一地址 / 一行一事实
- 事实层不直接下最终角色
- 钱包事实必须可回溯到采集层

---

## 3. 同源证据

### 旧目录
- `modules/wallet_structure/`
- `modules/source_wallet_bot/`
- `data/gmgn_candidates_live_run/wallet_structure/<token>/structure_analysis/`
- `data/gmgn_candidates_live_run/index/`

### 旧文件类型
- `same_source_evidence_normalized.json`
- `candidate_groups.csv`
- `bot2_handoff_packet.json` 内的 source groups

### 新体系目标目录
- `standard_wallet_data/evidence/`

### 建议落点
- `evidence/same_source/`
- `evidence/funding_path/`
- `evidence/token_transfer/`

### 保留原则
- 同源只做候选证据
- 未查资金路径时写“资金待查”
- 不把候选同源直接写成确定同源

---

## 4. 结构分析

### 旧目录
- `data/gmgn_candidates_live_run/wallet_structure/<token>/structure_analysis/`
- `modules/wallet_structure/`
- `data/gmgn_candidates_live_run/state_machine/`

### 旧文件类型
- `wallet_classification.csv`
- `wallet_structure_summary.md`
- `wallet_structure_decision.json`
- `candidate_wallet_structure_summary.csv`
- `candidate_wallet_structure_summary.md`

### 新体系目标目录
- `standard_wallet_data/inference/`

### 建议落点
- `inference/wallet_structure/`
- `inference/role_classification/`
- `inference/chip_control/`

### 保留原则
- 结构分析是推断层
- 允许候选角色
- 禁止过早绝对定性

---

## 5. 行为推断

### 旧目录
- `modules/wallet_structure/`
- `modules/source_wallet_bot/`
- `data/gmgn_candidates_live_run/state_machine/`
- `data/gmgn_candidates_live_run/paper_live/`

### 旧文件类型
- `wallet_intelligence_decision.json`
- `bot2_handoff_packet.json`
- `candidate_states.json`
- `paper_positions_open.json`
- `paper_positions_closed.json`
- `failure_attribution.jsonl`

### 新体系目标目录
- `standard_wallet_data/inference/`

### 建议落点
- `inference/behavior/`
- `inference/lifecycle/`
- `inference/dominant_side/`

### 保留原则
- 行为推断和结构分析同属推断层，但应分文件夹
- 生命周期推断不要和原始事实混放

---

## 6. handoff 包

### 旧目录
- `modules/source_wallet_bot/`
- `data/gmgn_candidates_live_run/index/`
- `data/gmgn_candidates_live_run/paper_live/`

### 旧文件类型
- `bot2_handoff_packet.json`
- `case_files/`
- `telegram_callback_index.json`
- `system_index.json`

### 新体系目标目录
- `standard_wallet_data/handoff/`

### 建议落点
- `handoff/bot2/`
- `handoff/case_packet/`
- `handoff/telegram_packet/`

### 保留原则
- handoff 包是交接，不是结论
- 必须可直接喂给下游系统

---

## 7. 报告输出

### 旧目录
- `reports/`
- `data/gmgn_candidates_live_run/reports/`
- `data/gmgn_candidates_live_run/paper_live/case_files/`
- `data/gmgn_candidates_live_run/site/`
- `hermes_harness/08_reports/project_governance/`

### 旧文件类型
- `*.md`
- `*.json`
- `*.csv`
- `case_files/*`
- dashboard / site 输出

### 新体系目标目录
- `standard_wallet_data/reports/`

### 建议落点
- `reports/summary/`
- `reports/case/`
- `reports/daily/`
- `reports/audit/`

### 保留原则
- 报告层只承接已完成的事实 / 证据 / 推断
- 报告不能反向污染原始层

---

## 8. 索引层

### 旧目录
- `data/gmgn_candidates_live_run/index/`

### 旧文件类型
- `system_index.json`
- `telegram_callback_index.json`
- token / position / review / case 索引文件

### 新体系目标目录
- `standard_wallet_data/index/`

### 建议落点
- `index/system_index.json`
- `index/token_index.json`
- `index/wallet_index.json`
- `index/handoff_index.json`
- `index/report_index.json`

### 保留原则
- 索引只做路由，不承载事实本体
- 索引应稳定、可重建、可回查

---

## 9. 推荐的统一写入规则

```text
原始采集 → ingest
标准事实 → facts
同源证据 → evidence
结构/行为推断 → inference
交接包 → handoff
人类报告 → reports
统一路由 → index
```

---

## 10. 简短结论

现在这些旧目录已经可以按层归位：

- 采集层：`ingest`
- 事实层：`facts`
- 证据层：`evidence`
- 推断层：`inference`
- 交接层：`handoff`
- 报告层：`reports`
- 索引层：`index`

