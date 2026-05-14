# SIKK-SOL v1.2 主导侧生命周期 + 行为动机推断设计

> 来源：ChatGPT share `69f602fb-f4c4-83ab-9e7b-f5b4beebb05c` 中关于纸面交易优化、钱包结构接入、主导侧生命周期、主导侧行为动机推断的方案整理。
>
> 目标：把“盘型 + 钱包筹码 + 主导侧生命周期 + 行为动机 + 对手盘心理 + quote/security + paper 复盘”统一成可工程化、可测试、可复盘的 SIKK-SOL v1.2 判断框架。
>
> 安全边界：本设计只服务候选分析、纸面交易、状态机门禁和复盘；不执行真实 swap，不签名，不广播交易。

## 1. 为什么要新增生命周期层

现有系统已经具备：

- GMGN 新币候选发现
- K线 / 吸筹窗口 / 控盘箱体
- SIKK 信号
- 候选状态机
- 钱包结构 observe/soft/hard 旁路门禁
- OKX quote/security
- paper live runner
- Hindsight retain/recall

但如果只用“盘型”和“钱包结构”，会出现误判：

- 长时间横盘可能是控筹，也可能是死亡横盘。
- 放量突破可能是二段启动，也可能是借量派发。
- 早期钱包卖出可能是部分兑现，也可能是最终派发。
- 老 token 可能已死亡，也可能正在再激活。

因此 v1.2 增加更高层的：

```text
dominant_side_lifecycle
主导侧生命周期
```

它回答：

```text
结构资金当前处于吸筹、控筹、一段拉升、部分派发、再吸筹、二段、主动派发、崩塌、死亡横盘，还是再激活？
```

## 2. v1.2 总体判断顺序

```text
1. token 时间上下文
2. market_pattern_type：盘型识别
3. dominant_side_lifecycle：主导侧生命周期
4. wallet_structure：钱包筹码证据
5. wallet_pattern_alignment：钱包行为是否匹配当前盘型/生命周期
6. dominant_side_intent：主导侧行为动机推断
7. counterparty_state：对手盘状态
8. structure_defense_status：结构位防守状态
9. trap_risk_type：诱导/陷阱风险
10. K线 / 成交量确认
11. quote / security / liquidity
12. 状态机决策
13. paper 复盘校准
```

最终不是：

```text
钱包好 → 买
盘型好 → 买
```

而是：

```text
盘型说明当前外观
钱包说明筹码行为
生命周期说明结构资金阶段
行为动机说明主导侧可能在做什么
对手盘状态说明谁在给谁提供流动性
quote/security/liquidity 说明能不能执行
paper 复盘验证规则是否有效
```

## 3. 新增核心字段

应加入：

```text
dominant_side_lifecycle
lifecycle_confidence
accumulation_progress_score
distribution_progress_score
control_retention_score
phase_transition_signal
lifecycle_risk_level
lifecycle_reason

dominant_side_intent
intent_confidence
counterparty_state
liquidity_intent
structure_defense_status
trap_risk_type
evidence_level
alternative_hypothesis
invalid_conditions
```

建议写入这些输出：

```text
lifecycle/dominant_lifecycle_summary.json
lifecycle/dominant_lifecycle_summary.csv
lifecycle/dominant_lifecycle_summary.md
lifecycle/<token>/dominant_lifecycle_decision.json
candidate_states.json
paper_positions_open.json
paper_positions_closed.json
failure_attribution.jsonl
live_state.json
live_board.md
```

## 4. dominant_side_lifecycle 枚举

```text
EARLY_ACCUMULATION             早期吸筹
FAST_ACCUMULATION_LAUNCH       快速吸筹拉升
CONTROL_BOX_ACCUMULATION       箱体控筹
FIRST_STAGE_EXPANSION          一段拉升
PARTIAL_DISTRIBUTION           部分派发
REACCUMULATION                 再吸筹 / 再控筹
SECOND_STAGE_PREPARATION       二段准备
SECOND_STAGE_EXPANSION         二段放量
ACTIVE_DISTRIBUTION            主动派发
FINAL_DISTRIBUTION             最终派发
STRUCTURE_COLLAPSE             结构崩塌
DEAD_SIDEWAYS                  死亡横盘
REACTIVATION                   老盘再激活
UNKNOWN                        不明确
```

## 5. 生命周期交易语义

### 只观察 / 高优先级观察

```text
EARLY_ACCUMULATION
CONTROL_BOX_ACCUMULATION
PARTIAL_DISTRIBUTION
REACCUMULATION
SECOND_STAGE_PREPARATION
REACTIVATION
```

默认动作：

```text
WATCHING / HIGH_PRIORITY_WATCHING
```

### 可进入 PAPER_READY 候选

```text
FAST_ACCUMULATION_LAUNCH
SECOND_STAGE_EXPANSION
REACTIVATION
```

但仍必须同时满足：

```text
signal_gate = ALLOW
wallet_pattern_alignment != PATTERN_CONFLICT
wallet_structure_status != WALLET_BLOCK
counterparty_pressure_score < threshold
quote_gate = ALLOW
security_gate = ALLOW
liquidity_gate = ALLOW
freshness_gate = ALLOW
```

### 必须阻断

```text
ACTIVE_DISTRIBUTION
FINAL_DISTRIBUTION
STRUCTURE_COLLAPSE
```

默认动作：

```text
BLOCKED
```

### 默认冷却

```text
DEAD_SIDEWAYS
```

默认动作：

```text
COOLING
```

但若出现有效二段信号：

```text
second_stage_valid = true
```

可转：

```text
REACTIVATION
```

## 6. 三个生命周期评分

### accumulation_progress_score：吸筹进度分

回答：结构侧是否已经完成足够筹码控制？

建议权重：

```text
早期钱包进入密度              20
同源买入同步度                20
早期钱包剩余比例              20
箱体压缩质量                  15
成交量收缩质量                10
Top Holder 稳定性             10
数据质量                       5
```

解释：

```text
>=70  吸筹较充分
50-69 吸筹中
30-49 弱吸筹
<30   无明显吸筹
```

### distribution_progress_score：派发进度分

回答：结构侧是否已经派发到后期？

建议权重：

```text
早期钱包卖出比例              25
高结果钱包退出比例            20
同源组同步卖出                20
Top Holder 下降               10
晚期大额承接增加              10
holder_count 增加但价格弱      10
价格跌破结构位                 5
```

解释：

```text
>=80  派发接近完成
60-79 主动派发中
40-59 部分派发
<40   派发不明显
```

### control_retention_score：控制权保留分

回答：结构侧是否还保留继续推动的筹码和动机？

建议权重：

```text
early_wallet_remaining_pct       25
high_result_remaining_pct        20
same_source_group_remaining_pct  20
same_source_sync_sell_score 反向  15
counterparty_pressure_score 反向 10
箱体/AVWAP/POC 是否守住          10
```

解释：

```text
>=70  控制权保留较强
50-69 控制权部分保留
30-49 控制权减弱
<30   控制权明显丧失
```

## 7. 主导侧行为动机推断

系统中不要写“读庄家心理”，建议统一命名为：

```text
dominant_side_intent
主导侧行为动机推断
```

它只能基于可观察证据推断，不能直接断言。

枚举：

```text
ACCUMULATE                 疑似吸筹
CONTROL                    疑似控盘
WASHOUT                    疑似洗盘
LIQUIDITY_TEST             疑似测试流动性
BREAKOUT_TEST              疑似测试突破
MARKUP                     疑似推进拉升
PARTIAL_DISTRIBUTION       疑似部分派发
ACTIVE_DISTRIBUTION        疑似主动派发
REACCUMULATION             疑似再吸筹
REACTIVATION               疑似老盘再激活
ABANDONMENT                疑似放弃维护
UNKNOWN                    不明确
```

关键原则：

```text
1. 不凭单一字段判断意图。
2. early_wallet_sold_pct 不能单独解释为派发。
3. 放量突破不能单独解释为拉升。
4. 横盘不能单独解释为控筹。
5. 每个意图都必须给 alternative_hypothesis。
6. 每个机会都必须给 invalid_conditions。
7. 所有意图判断必须进入 paper 复盘统计。
```

## 8. 对手盘 / 流动性 / 结构防守 / 陷阱字段

### counterparty_state

```text
NO_COUNTERPARTY_PRESSURE       对手盘压力低
RETAIL_CHASING                 散户追涨
WHALE_ABSORBING                大户承接
TRAPPED_COUNTERPARTY           对手盘被套
EXIT_LIQUIDITY_FORMING         出货流动性形成
PANIC_SELLING                  恐慌抛售
UNKNOWN                        不明确
```

### liquidity_intent

```text
BUILD_POSITION_LIQUIDITY       建仓流动性
TEST_BUY_DEPTH                 测试买盘深度
TEST_SELL_PRESSURE             测试抛压
CREATE_BREAKOUT_LIQUIDITY      制造突破流动性
DISTRIBUTE_INTO_DEMAND         借需求派发
DEFEND_STRUCTURE_LEVEL         防守结构位
ABANDON_LIQUIDITY_SUPPORT      放弃流动性维护
UNKNOWN
```

### structure_defense_status

```text
DEFENDING_CONTROL_BOX          防守箱体
DEFENDING_AVWAP                防守 AVWAP
DEFENDING_POC                  防守 POC
FAILED_DEFENSE                 防守失败
NO_DEFENSE_OBSERVED            未观察到防守
UNKNOWN
```

### trap_risk_type

```text
NO_TRAP_OBSERVED
FAKE_BREAKOUT_TRAP             假突破诱多
BREAKDOWN_SHAKEOUT             跌破洗盘
LIQUIDITY_GRAB                 流动性扫单
PUMP_TO_DISTRIBUTE             拉升派发
DEAD_CAT_REACTIVATION          假复活
UNKNOWN
```

## 9. 证据等级

```text
E0：无证据
E1：单一弱证据
E2：多字段一致
E3：钱包 + K线 + 成交量一致
E4：多轮快照连续验证
```

示例：

```text
同源组同步卖 + top10 下降 + 晚期接盘增加 + 价格失去推进 = E3 派发风险
```

## 10. 失效条件思维

每个 PAPER_READY 候选必须带 invalid_conditions。

例如二段放量盘失效条件：

```text
price_below_control_box_high
counterparty_pressure_score >= 70
same_source_sync_sell_score >= 70
top10_holder_pct_delta <= -5
wallet_structure_status 转 WALLET_BLOCK
```

没有失效条件，不允许升级为强 PAPER_READY。

## 11. 新增脚本建议

```text
sikk_dominant_lifecycle_classifier.py
tests/test_sikk_dominant_lifecycle_classifier.py
```

输入：

```text
gmgn_new_token_filter/token_candidates.json
candidate_signal_outputs/candidate_signal_summary.json
state_machine/candidate_states.json
wallet_structure/candidate_wallet_structure_summary.json
wallet_structure/<token>/wallet_structure_decision.json
wallet_structure/<token>/snapshots/latest_delta.json
kline_pipeline/candidate_kline_pipeline_summary.json
```

输出：

```text
lifecycle/dominant_lifecycle_summary.json
lifecycle/dominant_lifecycle_summary.csv
lifecycle/dominant_lifecycle_summary.md
lifecycle/<token>/dominant_lifecycle_decision.json
```

标准单 token 输出：

```json
{
  "token_address": "TOKEN",
  "token_symbol": "SYMBOL",
  "market_pattern_type": "CONTROL_BOX_ACCUMULATION",
  "dominant_side_lifecycle": "SECOND_STAGE_PREPARATION",
  "lifecycle_confidence": 0.72,
  "accumulation_progress_score": 68,
  "distribution_progress_score": 36,
  "control_retention_score": 64,
  "phase_transition_signal": "PRE_SECOND_STAGE",
  "lifecycle_risk_level": "MEDIUM",
  "dominant_side_intent": "BREAKOUT_TEST",
  "intent_confidence": 0.68,
  "counterparty_state": "NO_COUNTERPARTY_PRESSURE",
  "liquidity_intent": "TEST_BUY_DEPTH",
  "structure_defense_status": "DEFENDING_CONTROL_BOX",
  "trap_risk_type": "NO_TRAP_OBSERVED",
  "evidence_level": "E2",
  "alternative_hypothesis": "也可能只是低量横盘后的普通反弹，需等待放量突破和回踩确认",
  "invalid_conditions": [
    "price_below_control_box_low",
    "same_source_sync_sell_score >= 70",
    "counterparty_pressure_score >= 70"
  ],
  "allowed_action": "HIGH_PRIORITY_WATCHING",
  "reason": "长时间箱体横盘，成交量收缩，结构筹码未确认同步派发，接近箱体上沿，疑似二段前测试突破。"
}
```

## 12. 状态机接入建议

`candidate_states.json` 增加字段：

```text
主导侧生命周期
生命周期置信度
吸筹进度分
派发进度分
控制权保留分
阶段转换信号
生命周期风险等级
主导侧行为动机
行为动机置信度
对手盘状态
流动性意图
结构防守状态
陷阱风险类型
证据等级
替代假设
失效条件
生命周期原因
```

状态机规则：

```text
ACTIVE_DISTRIBUTION / FINAL_DISTRIBUTION / STRUCTURE_COLLAPSE → BLOCKED
DEAD_SIDEWAYS → COOLING / WATCHING_LOW_PRIORITY
EARLY_ACCUMULATION / CONTROL_BOX_ACCUMULATION / PARTIAL_DISTRIBUTION / REACCUMULATION / SECOND_STAGE_PREPARATION → WATCHING 或 HIGH_PRIORITY_WATCHING
SECOND_STAGE_EXPANSION / FAST_ACCUMULATION_LAUNCH / REACTIVATION → 允许进入 PAPER_READY 候选，但必须通过 signal/wallet/quote/security/liquidity/freshness
```

## 13. paper runner 接入建议

纸面仓位新增字段：

```text
dominant_side_lifecycle
lifecycle_confidence
dominant_side_intent
intent_confidence
counterparty_state
liquidity_intent
structure_defense_status
trap_risk_type
invalid_conditions
alternative_hypothesis
```

持仓管理：

```text
ACTIVE_DISTRIBUTION → EXIT_MONITOR 或 FORCE_PAPER_EXIT
FINAL_DISTRIBUTION → FORCE_PAPER_EXIT
STRUCTURE_COLLAPSE → FORCE_PAPER_EXIT
WASHOUT 且结构未崩 → HOLD / WATCH_CONFIRMATION
SECOND_STAGE_EXPANSION 且 quote/security 通过 → 可 paper open
```

## 14. failure_attribution 接入

新增归因类型：

```text
LIFECYCLE_MISCLASSIFIED
INTENT_MISREAD
FAKE_BREAKOUT_TRAP
PUMP_TO_DISTRIBUTE
REACCUMULATION_FAILED
SECOND_STAGE_FAILED
STRUCTURE_DEFENSE_FAILED
COUNTERPARTY_ABSORBING
ACTIVE_DISTRIBUTION_MISSED
DEAD_SIDEWAYS_FALSE_REACTIVATION
```

用于回答：

```text
这笔失败是因为生命周期判断错了，还是行为动机推断错了，还是钱包结构变化没及时进入退出管理？
```

## 15. Hermes / SIKK 专业调用顺序 v1.2

推荐命令层：

```text
/SIKK_STATUS
/SIKK_DISCOVER
/SIKK_PATTERN_CLASSIFY
/SIKK_WALLET_REFRESH
/SIKK_LIFECYCLE_CLASSIFY
/SIKK_RUN_ONCE_OBSERVE
/SIKK_STATUS
```

soft 模式：

```text
/SIKK_DISCOVER
/SIKK_PATTERN_CLASSIFY
/SIKK_WALLET_REFRESH
/SIKK_LIFECYCLE_CLASSIFY
/SIKK_RUN_ONCE_SOFT
/SIKK_STATUS
```

## 16. 第一阶段落地计划

### P0：先设计和测试

- 新建 `sikk_dominant_lifecycle_classifier.py`
- 新建 `tests/test_sikk_dominant_lifecycle_classifier.py`
- 定义枚举、评分函数、decision JSON schema
- 用 fake token 覆盖：
  - CONTROL_BOX_ACCUMULATION
  - SECOND_STAGE_EXPANSION
  - ACTIVE_DISTRIBUTION
  - STRUCTURE_COLLAPSE
  - DEAD_SIDEWAYS → REACTIVATION

### P1：旁路输出，不影响交易

- 在 pipeline 之后读取现有 state/wallet/kline/signal 输出
- 写 `lifecycle/` 输出
- 不改状态机结果
- live_board 增加生命周期字段

### P2：observe 接入状态机

- 状态机只记录生命周期字段
- 不阻断 PAPER_READY
- 写 would_block_by_lifecycle / would_pause_by_lifecycle

### P3：soft/hard 接入

- soft：只对 E3/E4 且阻断生命周期生效
- hard：ACTIVE_DISTRIBUTION / FINAL_DISTRIBUTION / STRUCTURE_COLLAPSE 直接阻断

### P4：paper runner 复盘

- paper positions 写入生命周期字段
- failure_attribution 写生命周期失败原因
- daily report 按 lifecycle/intent 统计收益和失败率

## 17. 验证命令草案

```bash
cd /root/sikk-gmgn
python3 -m pytest tests/test_sikk_dominant_lifecycle_classifier.py tests/test_sikk_wallet_trade_adapter.py tests/test_sikk_state_wallet_structure_integration.py tests/test_run_sikk_gmgn_pipeline.py -q
python3 -m py_compile sikk_dominant_lifecycle_classifier.py sikk_wallet_trade_adapter.py sikk_candidate_state_machine.py run_sikk_gmgn_pipeline.py
```

安全 grep：

```bash
grep -R "庄家\|gmgn-cli swap\|gmgn-cli multi-swap\|order strategy create\|onchainos swap execute\|private key\|api key\|bot_token\|webhook_url" \
  sikk_dominant_lifecycle_classifier.py tests/test_sikk_dominant_lifecycle_classifier.py | cat
```

预期：如出现“庄家”只能在方法论注释中，系统字段统一使用“主导侧 / dominant_side”。
