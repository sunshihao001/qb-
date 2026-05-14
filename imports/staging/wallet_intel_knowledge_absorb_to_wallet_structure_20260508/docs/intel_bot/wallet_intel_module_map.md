# Intel Bot 钱包小模块体系

## 1. wallet_source_reader
- 输入：legacy raw archive + GMGN export files
- 输出：source event bundle + provenance records
- 核心字段：source_type, source_file, source_timestamp, raw_field_refs, retrieval_status
- 规则：read-only；no inference beyond extraction；preserve provenance
- 禁止事项：swap；broadcast；sign；state_machine writes；private key access
- 依赖模块：legacy archive manifest, raw snapshot files
- 验收标准：Can enumerate source artifacts and keep path-level traceability.
- 后续扩展点：support additional upstream wallet providers, support incremental refresh logs

## 2. wallet_normalized_adapter
- 输入：source event bundle
- 输出：wallet_structure_normalized records
- 核心字段：token_address, wallet_address, snapshot_time, first_buy_time, last_sell_time, holding_amount, holding_pct, roi, pnl
- 规则：normalize without judging；missing values must stay null/UNKNOWN；no reverse inference from display layers
- 禁止事项：trade decisions；paper status；live state writes
- 依赖模块：wallet_source_reader
- 验收标准：Produces one normalized record schema shared by all downstream analyzers.
- 后续扩展点：support new wallet providers, support richer fallback provenance

## 3. wallet_entity_profiler
- 输入：normalized wallet records
- 输出：wallet entity profile + role candidates
- 核心字段：wallet_age, is_new_wallet, is_active, gmgn_tags, entity_tags, evidence_level
- 规则：do not say庄家；use疑似结构角色；GMGN tags only as auxiliary evidence
- 禁止事项：direct buy/sell signals；single-field role verdicts
- 依赖模块：wallet_normalized_adapter
- 验收标准：Outputs explainable profile and candidate role labels.
- 后续扩展点：historical role drift scoring, entity clustering

## 4. current_token_behavior_analyzer
- 输入：wallet entity profile + token trade snapshot
- 输出：current token behavior table
- 核心字段：first_buy_time, last_sell_time, buy_delay, holding_pct, sold_pct, trade_count, roi, pnl
- 规则：current-token-only evidence；no transaction authorization；evidence not verdict
- 禁止事项：state machine writes；PAPER_READY generation
- 依赖模块：wallet_entity_profiler
- 验收标准：Can summarize wallet behavior per token with a consistent evidence tier.
- 后续扩展点：multiple time-window behavior trendlines

## 5. same_source_group_analyzer
- 输入：entity profile + current token behavior + source traces
- 输出：same-source candidate groups + relation edges
- 核心字段：relation_type, group_id, edge_strength, evidence_grade, conflict_notes
- 规则：no forced同源 verdict；track conflicting evidence explicitly
- 禁止事项：hard same-source claims without support
- 依赖模块：wallet_entity_profiler, current_token_behavior_analyzer
- 验收标准：Groups are reproducible from relation evidence, not from narrative labels.
- 后续扩展点：graph-based relation scoring, cross-token reuse

## 6. chip_transfer_analyzer
- 输入：same-source groups + holder/trader deltas
- 输出：chip migration / backflow / distribution decision support
- 核心字段：transfer_direction, backflow_flag, distribution_flag, pressure_score, change_reason
- 规则：analyze movement, not trade authorization；maintain evidence chain
- 禁止事项：swap execution；rewarding pressure with buy signal
- 依赖模块：same_source_group_analyzer
- 验收标准：Can describe chip migration direction and pressure change with reasons.
- 后续扩展点：multi-round delta modeling

## 7. historical_wallet_profiler
- 输入：legacy archive + address recurrence history
- 输出：historical address profile + recurrence records
- 核心字段：address, seen_tokens, role_history, repetition_pattern, review_plan
- 规则：legacy-only data remains legacy；cross-token recurrence must be explicit
- 禁止事项：live merge into current wallet structure
- 依赖模块：wallet_source_reader, wallet_entity_profiler
- 验收标准：Can answer historical address and role queries from legacy data.
- 后续扩展点：address reputation trends, watchlists

## 8. wallet_structure_scorer
- 输入：profile + behavior + chip transfer + history
- 输出：wallet_structure_score + evidence levels + risk levels
- 核心字段：wallet_structure_score, wallet_risk_score, counterparty_pressure_score, data_quality_score, wallet_evidence_level
- 规则：scores must be explainable；single field cannot decide
- 禁止事项：paper/blocked direct routing for Intel Bot
- 依赖模块：wallet_entity_profiler, current_token_behavior_analyzer, chip_transfer_analyzer, historical_wallet_profiler
- 验收标准：Produces auditable scores with evidence-level rationale.
- 后续扩展点：scenario-specific weights

## 9. wallet_decision_builder
- 输入：scoring result + evidence bundle
- 输出：wallet_structure_decision
- 核心字段：wallet_structure_decision, reason_codes, valid_until, paper_gate_effect, action_code
- 规则：decision is the trading-side handoff file only；no direct PAPER_READY/BLOCKED in Intel Bot
- 禁止事项：trade execution；state machine mutation
- 依赖模块：wallet_structure_scorer
- 验收标准：Produces the standard decision artifact without taking execution actions.
- 后续扩展点：versioned decision schema

## 10. gmgn_note_exporter
- 输入：wallet decision + role profile
- 输出：gmgn_note_table
- 核心字段：address, gmgn_note, reason, action
- 规则：notes are for monitoring and review；not a buy/sell recommendation
- 禁止事项：trade hints；execution routing
- 依赖模块：wallet_decision_builder
- 验收标准：Can generate stable note rows for Telegram display and export.
- 后续扩展点：templated notes by role class

## 11. token_cluster_analyzer
- 输入：holder snapshot + same-source groups + funding traces + wallet role profiles
- 输出：token cluster intelligence bundle
- 核心字段：holder_cluster, same_source_group, funding_source, top_holder_concentration, early_wallet_group, distribution_receiver, bagholder_whale, counterparty_wallet
- 规则：代币集群分析全部归入 Intel Bot；cluster 只是结构情报，不是交易建议
- 禁止事项：single cluster verdict；trade trigger generation；state machine writes
- 依赖模块：wallet_normalized_adapter, wallet_entity_profiler, current_token_behavior_analyzer, same_source_group_analyzer, chip_transfer_analyzer
- 验收标准：Can explain holder clusters, same-source groups, funding paths, early wallets, receivers, bagholder whales, and counterparty wallets with evidence refs.
- 后续扩展点：graph-based cluster scoring, cross-token cluster recurrence

## 12. dominant_cost_zone_calculator
- 输入：normalized wallet records + same-source groups + trade distribution bands + box range
- 输出：dominant cost zone estimate + confidence band + cost position status
- 核心字段：wallet_avg_cost, same_source_group_cost_low, same_source_group_cost_mid, same_source_group_cost_high, same_source_group_cost_confidence, dominant_cost_low, dominant_cost_mid, dominant_cost_high, dominant_cost_confidence, market_cost_mid, box_cost_mid, current_price, price_to_dominant_cost_pct, cost_position_status_zh
- 规则：cost is a zone not a point；do not infer buy point；keep evidence chain from wallet behavior and grouped cost bands
- 禁止事项：trade signal emission；state machine writes；paper runner writes
- 依赖模块：wallet_normalized_adapter, wallet_entity_profiler, same_source_group_analyzer, current_token_behavior_analyzer
- 验收标准：Can explain where the suspicious dominant-side cost zone sits and how current price relates to it.
- 后续扩展点：VWAP bands, multi-window cost drift, cost-zone decay

## 13. structure_inventory_estimator
- 输入：entity profile + same-source groups + current holdings + role stability
- 输出：structure inventory estimate + remaining percentage + inventory status
- 核心字段：structure_max_inventory, structure_current_inventory, structure_inventory_remaining_pct, early_wallet_remaining_pct, same_source_group_remaining_pct, top_holder_structure_stability_score, inventory_status_zh
- 规则：estimate remaining chip inventory only；do not convert into entry advice
- 禁止事项：buy recommendation；execution routing
- 依赖模块：wallet_entity_profiler, current_token_behavior_analyzer, same_source_group_analyzer
- 验收标准：Can quantify how much suspicious structure-side inventory is still present.
- 后续扩展点：inventory decay by time-window, top-holder retention curves

## 14. distribution_progress_estimator
- 输入：early wallets + same-source groups + receiver wallets + backflow paths
- 输出：distribution progress score + Chinese progress status
- 核心字段：structure_sold_pct, early_wallet_sold_pct, same_source_group_sold_pct, distribution_receiver_sold_pct, backflow_confirmed_pct, distribution_progress_score, distribution_progress_status_zh
- 规则：measure distribution progress only；do not map to buy/sell timing
- 禁止事项：trade trigger generation
- 依赖模块：same_source_group_analyzer, chip_transfer_analyzer, historical_wallet_profiler
- 验收标准：Can explain whether distribution is partial, aggressive, or near completion.
- 后续扩展点：multi-round sell synchronization, receiver churn metrics

## 15. markup_motivation_model
- 输入：cost position + inventory + distribution progress + liquidity + pattern control + counterparty pressure
- 输出：continue-progression / second-stage / maintenance motivation score
- 核心字段：remaining_inventory_score, unfinished_distribution_score, cost_position_score, pattern_control_score, liquidity_need_score, second_stage_condition_score, counterparty_pressure_penalty, same_source_exit_penalty, markup_motivation_score, markup_motivation_status_zh
- 规则：explain motivation strength only；do not assert inevitable push-up
- 禁止事项："一定要拉" style conclusions；buy point output
- 依赖模块：dominant_cost_zone_calculator, structure_inventory_estimator, distribution_progress_estimator, counterparty_pressure_quant_model, wallet_pattern_cost_alignment
- 验收标准：Can distinguish strong, medium, weak, exit-biased, or insufficient evidence motivation.
- 后续扩展点：scenario weighting, phase-conditioned scoring

## 15B. dominant_intent_inference
- 输入：holder cluster + wallet behavior + lifecycle + cost zone + inventory + distribution progress + counterparty pressure + pattern alignment
- 输出：dominant_intent_decision
- 核心字段：dominant_intent_code, dominant_intent_status_zh, dominant_intent_confidence, intent_evidence_breakdown, conflict_notes_zh
- 标准枚举：ACCUMULATE, CONTROL, WASHOUT, BREAKOUT_TEST, MARKUP, PARTIAL_DISTRIBUTION, ACTIVE_DISTRIBUTION, REACCUMULATION, REACTIVATION, ABANDONMENT
- 中文输出：疑似吸筹、疑似控盘、疑似洗盘、疑似测试突破、疑似推进拉升、疑似部分派发、疑似主动派发、疑似再吸筹、疑似再激活、疑似放弃维护
- 规则：专业系统里不叫“庄家心理”，统一称为主导侧行为动机推断；必须多字段综合推断，不能单字段裁决
- 禁止事项：不能输出开仓/止损/止盈；不能直接 PAPER_READY/BLOCKED；不能修改状态机
- 依赖模块：token_cluster_analyzer, dominant_cost_zone_calculator, structure_inventory_estimator, distribution_progress_estimator, counterparty_pressure_quant_model, wallet_pattern_cost_alignment
- 验收标准：Can produce a hypothesis-only intent decision with confidence and evidence/conflict breakdown.

## 16. counterparty_pressure_quant_model
- 输入：late-stage buyers + whale holders + retailization signs + early-to-late transfer flow + floating loss wallets
- 输出：counterparty pressure score + pressure status
- 核心字段：late_large_buyer_score, whale_bagholder_score, retailization_score, early_to_late_transfer_score, floating_loss_late_holder_score, counterparty_pressure_score, counterparty_pressure_status_zh
- 规则：measure whether structure-side chips are likely being transferred to counterparties
- 禁止事项：encouraging chase entries
- 依赖模块：same_source_group_analyzer, chip_transfer_analyzer, current_token_behavior_analyzer
- 验收标准：Can identify low/medium/high counterparty pressure and likely counterparty-taking patterns.
- 后续扩展点：late-buyer clustering, floating-loss persistence windows

## 17. wallet_pattern_cost_alignment
- 输入：cost zone + wallet behavior + price structure + distribution state
- 输出：pattern type + alignment score + Chinese alignment status
- 核心字段：pattern_type_zh, cost_pattern_match_score, wallet_behavior_match_score, alignment_status_zh, alignment_notes_zh
- 规则：judge whether cost zone, wallet behavior, and pattern are aligned
- 禁止事项：reclassifying alignment as buy signal
- 依赖模块：dominant_cost_zone_calculator, structure_inventory_estimator, distribution_progress_estimator
- 验收标准：Can distinguish 横盘控筹、二段放量、主动派发、结构崩塌、匹配度未知.
- 后续扩展点：pattern library, phase transition detection

## 18. quantitative_structure_report
- 输入：all above quantitative objects
- 输出：human-readable Chinese report for Strategy Gate Bot
- 核心字段：summary_zh, section summaries, evidence highlights, handoff note
- 规则：report is explanation only；no trade suggestion；no buy point
- 禁止事项：state machine mutation；paper runner writes；实盘提示
- 依赖模块：all quantitative structure models
- 验收标准：Can summarize the full structure judgment in Chinese and hand it to Strategy Gate Bot.
- 后续扩展点：auto-generated narrative templates, delta comparison by snapshot
