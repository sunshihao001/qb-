# Intel Bot 钱包结构研究工作流执行计划

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** 将 legacy SIKK-GMGN 钱包情报整理成 Intel Bot 的只读结构研究子系统，先补标准化合同，再补源接入、实体画像、行为分析、同源分析、迁移分析、历史画像、决策装配、GMGN 备注与反馈闭环。

**Architecture:**
先建立统一的 legacy 钱包情报索引与 `wallet_structure_normalized` 合约，再按层拆分成 source reader → normalized adapter → entity profiler → current-token behavior analyzer → same-source analyzer → chip-transfer analyzer → historical wallet profiler → scorer → decision builder → note exporter → review feedback。全程只读，不接交易、不改状态机、不碰 paper runner。

**Tech Stack:** Python, markdown/json artifacts, legacy archive under `data/wallet_intelligence/legacy/`, Telegram query/export surface, existing SIKK-GMGN reports as read-only inputs.

---

## Task 1: 固化 wallet_structure_normalized 合约

**Objective:** 定义统一字段合同，作为所有钱包分析模块的共同数据骨架。

**Files:**
- Create: `docs/intel_bot/wallet_structure_normalized_contract.md`
- Create: `data/gmgn_candidates_live_run/intel-bot/logs/legacy_intel_bot/wallet_structure_normalized_contract.json`

**Step 1: 写合同草案**

包含字段：
- `token_address`
- `wallet_address`
- `snapshot_time`
- `first_buy_time`
- `last_sell_time`
- `holding_amount`
- `holding_pct`
- `sold_pct`
- `roi`
- `pnl`
- `gmgn_tags`
- `source_refs`
- `evidence_level`
- `risk_level`

**Step 2: 校验字段边界**

要求：
- 缺失值保持 `null` / `UNKNOWN`
- 不允许从 dashboard / paper / report 反推事实源
- 不允许写入交易动作

**Step 3: 验证**

检查合同是否能覆盖 legacy 包中的钱包结构汇总与后续分析需要。

---

## Task 2: 建立 wallet_source_reader

**Objective:** 统一读取 legacy 历史包与相关只读导出，保留 provenance。

**Files:**
- Create: `docs/intel_bot/wallet_source_reader_spec.md`
- Create: `data/gmgn_candidates_live_run/intel-bot/logs/legacy_intel_bot/wallet_source_index.json`

**Step 1: 定义输入源**

只允许 legacy 包、manifest、报告、导出文件。

**Step 2: 定义 provenance 结构**

每条记录至少包含：
- `source_file`
- `source_tag`
- `source_time`
- `source_type`
- `raw_field_refs`

**Step 3: 验证**

能列出历史包内所有文件并追溯来源路径。

---

## Task 3: 复原 wallet_entity_profiler

**Objective:** 将单钱包升级为实体画像和疑似结构角色候选。

**Files:**
- Create: `docs/intel_bot/wallet_entity_profiler_spec.md`
- Create: `data/gmgn_candidates_live_run/intel-bot/logs/legacy_intel_bot/wallet_entity_profiles.json`

**Step 1: 定义实体字段**

包含：钱包年龄、新钱包标记、活跃度、GMGN 标签、证据等级。

**Step 2: 定义角色边界**

只输出“疑似结构角色”，不直接说“庄家”。

**Step 3: 验证**

对 legacy 样本可输出一致的实体摘要。

---

## Task 4: 复原 current_token_behavior_analyzer

**Objective:** 只在当前 token 内分析首次买入、卖出、持仓、收益与交易次数。

**Files:**
- Create: `docs/intel_bot/current_token_behavior_analyzer_spec.md`
- Create: `data/gmgn_candidates_live_run/intel-bot/logs/legacy_intel_bot/current_token_behavior.json`

**Step 1: 定义行为字段**

含 `first_buy_time`、`last_sell_time`、`holding_pct`、`sold_pct`、`roi`、`pnl`。

**Step 2: 验证时间边界**

不能从 paper / dashboard 反推买入事实。

**Step 3: 验证**

能产出 token 行为证据表。

---

## Task 5: 设计 same_source_group_analyzer

**Objective:** 复原同源候选、关系边和冲突说明。

**Files:**
- Create: `docs/intel_bot/same_source_group_analyzer_spec.md`
- Create: `data/gmgn_candidates_live_run/intel-bot/logs/legacy_intel_bot/same_source_groups.json`

**Step 1: 定义关系类型**

同资金来源、同步买入、同步卖出、Token 分发、利润回收、基础设施边。

**Step 2: 定义冲突处理**

“暂不强判同源”必须保留为可执行复核状态，不可直接合并为结论。

**Step 3: 验证**

能输出 group_id、edge_strength、evidence_grade。

---

## Task 6: 设计 chip_transfer_analyzer

**Objective:** 补齐筹码迁移、回流、分发和压力变化分析。

**Files:**
- Create: `docs/intel_bot/chip_transfer_analyzer_spec.md`
- Create: `data/gmgn_candidates_live_run/intel-bot/logs/legacy_intel_bot/chip_transfer_decisions.json`

**Step 1: 定义方向字段**

`transfer_direction`、`backflow_flag`、`distribution_flag`、`pressure_score`。

**Step 2: 验证**

不将压力变化误判为买入授权。

**Step 3: 验证**

可解释每个迁移判断的理由链。

---

## Task 7: 建立 historical_wallet_profiler

**Objective:** 建立历史地址库的可检索索引与复现轨迹。

**Files:**
- Create: `docs/intel_bot/historical_wallet_profiler_spec.md`
- Create: `data/gmgn_candidates_live_run/intel-bot/logs/legacy_intel_bot/historical_wallet_index.json`

**Step 1: 设计索引键**

`wallet_address`、`token_address`、`role_history`、`review_plan`。

**Step 2: 验证 legacy-only**

历史库只能做历史查询，不能回写 live 结构。

**Step 3: 验证**

可回答历史地址、角色、复盘计划问题。

---

## Task 8: 建立 wallet_structure_decision 合约

**Objective:** 让 wallet_structure_decision 成为交易侧唯一交接文件。

**Files:**
- Create: `docs/intel_bot/wallet_structure_decision_contract.md`
- Create: `data/gmgn_candidates_live_run/intel-bot/logs/legacy_intel_bot/wallet_structure_decision_schema.json`

**Step 1: 定义输出字段**

`wallet_structure_decision`、`reason_codes`、`valid_until`、`paper_gate_effect`、`action_code`。

**Step 2: 验证边界**

Intel Bot 只装配决策，不直接决定交易执行。

**Step 3: 验证**

该合同可被后续 final_trade_gate 消费。

---

## Task 9: 建立 GMGN 备注生成规则

**Objective:** 规范 gmgn_note_table 的展示和导出格式。

**Files:**
- Create: `docs/intel_bot/gmgn_note_rules.md`
- Create: `data/gmgn_candidates_live_run/intel-bot/logs/legacy_intel_bot/gmgn_note_table.json`

**Step 1: 定义备注字段**

`address`、`gmgn_note`、`reason`、`action`。

**Step 2: 验证用途**

备注仅用于监控、展示、复盘，不作为买卖建议。

**Step 3: 验证**

能对 legacy 样本生成稳定 note 行。

---

## Task 10: 建立 wallet_review_feedback

**Objective:** 把失败归因、缺口和人工复核转化为下一轮任务。

**Files:**
- Create: `docs/intel_bot/wallet_review_feedback_spec.md`
- Create: `data/gmgn_candidates_live_run/intel-bot/logs/legacy_intel_bot/wallet_review_feedback.json`

**Step 1: 定义反馈字段**

`gap_type`、`failure_mode`、`feedback`、`next_task`。

**Step 2: 验证**

反馈只能改进任务包，不能改历史事实。

**Step 3: 验证**

失败样本可回流到 next_tasks。

---

## Final Verification

Run:
- `test -f docs/intel_bot/wallet_research_scope.md`
- `test -f data/gmgn_candidates_live_run/intel-bot/logs/legacy_intel_bot/wallet_file_passports.json`
- `test -f data/gmgn_candidates_live_run/intel-bot/logs/legacy_intel_bot/wallet_intel_gap_inventory.json`
- `test -f data/gmgn_candidates_live_run/intel-bot/logs/legacy_intel_bot/wallet_intel_next_tasks.json`
- `python3 - <<'PY' ...` to inspect JSON keys and counts

## Delivery Rule

完成后按模块逐个落地，优先：
1. normalized contract
2. source reader
3. entity profiler
4. behavior analyzer
5. same-source analyzer
6. chip transfer analyzer
7. historical profiler
8. decision contract
9. GMGN note rules
10. review feedback
