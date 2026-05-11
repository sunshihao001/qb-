---
artifact_type: semantic_layer_judgement_table
status: verified
version: v2.0-stage3
generated_at: 2026-05-07T05:59:20Z
task_type: wallet_intel_semantic_integration
---
# Wallet-Intel 数据层级判断表 V2.0 — 阶段 3

## 1. 判断总表

| 输入内容 / 字段类型 | 归属层级 | 是否可直接引用 | 必填约束 | 禁止事项 |
|---|---|---:|---|---|
| wallet_address | 钱包事实层 | 是 | token_id/source_ref | 不得附带角色判断 |
| buy_time / sell_time | 钱包事实层 | 是 | tx_hash/source_ref | 不得解释为控筹/派发 |
| buy_amount / sell_amount | 钱包事实层 | 是 | unit/currency/source_ref | 不得单独推断动机 |
| current_balance / holding_pct | 钱包事实层 | 是 | snapshot_time/source_ref | Top Holder 不等于控筹 |
| funding_source | 钱包事实层 | 是 | source_status/depth/source_ref | 资金待查时不得强判同源 |
| top_holder_flag / rank | 钱包事实层 | 是 | snapshot_time/source_ref | 不得直接写控筹 |
| transfer_in / transfer_out | 钱包事实层 | 是 | counterparty/source_ref | 转入不是分发结论 |
| 同步买入/卖出 | 结构证据层 | 否，需证据等级 | evidence_level/fact_refs | 不得写确定同源 |
| 候选钱包组 | 结构证据层 | 否，需证据等级 | group_id/member_refs/fact_refs | 不得写确认同伙 |
| 资金路径相似 | 结构证据层 | 否，需证据等级 | funding_refs/confidence | 不得确认同一人 |
| 筹码分布集中 | 结构证据层 | 否，需证据等级 | holder_refs/snapshot_time | 不得直接写控盘 |
| 接盘路径 | 结构证据层 | 否，需证据等级 | buy_stage/price_context/fact_refs | 不得写必然套牢 |
| 主导侧生命周期 | 行为推断层 | 否 | uncertainty/evidence_refs | 不得写成事实 |
| 控筹状态 | 行为推断层 | 否 | evidence_level/uncertainty/invalidation | 不得写确定控盘 |
| 派发状态 | 行为推断层 | 否 | sell_refs/holding_delta/refutation | 不得写确认出货 |
| 二次扩张动机 | 行为推断层 | 否 | uncertainty/conditions | 不得写必涨/马上拉升 |
| 对手盘压力 | 行为推断层 | 否 | evidence_refs/counter_evidence | 不得写确定接盘 |
| SUPPORT / PAUSE / BLOCK | 策略交接层 | 否 | boundary/valid_until/invalidation | 不得作为真实交易指令 |
| paper_gate_handoff | 策略交接层 | 否 | source_inference/fact_refs | 不得单独作为买入依据 |
| state_machine_handoff | 策略交接层 | 否 | action_scope/review_window | 不得绕过 quote/security |
| gmgn_remark_handoff | 策略交接层 | 否 | remark_reason/evidence_level | 不得写确定庄家 |

## 2. 层级判断伪代码

```text
if record describes observable wallet event:
    layer = wallet_facts
elif record groups facts as structural support and has evidence refs:
    layer = structural_evidence
elif record explains possible behavior/state/motivation:
    layer = behavioral_inference
elif record is meant for downstream gate/state/paper/dashboard/remark:
    layer = strategy_handoff
else:
    layer = unknown_needs_review
```

## 3. 降级规则

```text
缺 fact_refs → 结构证据降级为 unknown_needs_review。
缺 evidence_level → 结构证据不得进入推断。
缺 uncertainty → 行为推断不得进入 handoff。
缺 boundary/invalidation → 策略交接不得进入状态机。
资金待查 → 同源最多为候选，不得强判。
```
