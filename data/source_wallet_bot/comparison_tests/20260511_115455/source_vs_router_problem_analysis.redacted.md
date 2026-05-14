# Source vs Phase01 Router 对比问题定位（redacted）

对象：`[REDACTED_CA]`
对比目录：`/root/sikk-gmgn/data/source_wallet_bot/comparison_tests/20260511_115455`

## 1. 两套输出是否都跑通

- 旧 source/full-auto readonly：`PASS`
  - stage_outputs_checked: 6
  - state_outputs_checked: 1
  - candidate_count: 1
  - final_state: WATCHING
  - strategy_status: PAPER_READY_CANDIDATE
- 当前八组/router Phase01：`PASS`
  - recommended_action: analysis_allowed_read_standard_fact_assets
  - missing_required_assets_count: 0
  - missing_optional_assets_count: 0
  - contamination_status: PASS

## 2. 数据输出差距

### 旧 source 输出

- 更像“策略/状态机候选输出”。
- 有 candidate、stage gate、final_state、strategy_status。
- 输出中包含：
  - wallet_structure_status: WALLET_SUPPORT
  - kline_status: RAW_KLINE_PENDING
  - strategy_status: PAPER_READY_CANDIDATE
  - final_state: WATCHING
  - transition_reason: 证据不足，保持观察。
- 但缺少标准事实层核心产物：
  - wallet_trade_normalized: False
  - wallet_entity_profile_normalized: False
  - wallet_intelligence_decision: False
  - same_source_evidence: False
  - bot2_handoff: False
  - missing_field_contract: False

### 当前八组/router 输出

- 更像“Phase01 标准事实缓存 + 下游交接物”。
- 标准事实产物存在并通过 gate：
  - required_assets: bot2_handoff_packet, raw_source_manifest, same_source_evidence_normalized, wallet_entity_profile_normalized, wallet_intelligence_decision, wallet_trade_normalized
- 事实记录量：
  - wallet_trade_records: 28
  - wallet_profile_records: 28
  - wallet_intelligence_records: 28
  - same_source_candidate_groups: 2
- 证据等级：{'E2': 10, 'E3': 17, 'E0': 1}
- 风险等级：{'R2': 25, 'R1': 2, 'R0': 1}
- 同源候选证据等级：{'E3': 2}
- 仍需补查字段：['funding_source_address', 'wallet_first_seen_time']
- 缺字段影响钱包数：2

## 3. 快照差异不是核心问题

两套 market/stage 都能抓到数据，但快照值不同：

- market_cap：旧 501176.6401830906 / 当前 488879.6324018165
- holders_count：旧 50 / 当前 8
- traders_count：旧 50 / 当前 8

解释：这是实时数据源和 limit/快照时点造成的差异，不是核心系统问题。核心问题是“旧输出是状态机候选摘要，当前输出是事实层标准产物”。

## 4. 问题根因

### 根因 A：旧 source 混合了事实层、结构判断层、策略状态层

旧输出直接出现 `PAPER_READY_CANDIDATE`、`WATCHING`、`transition_reason` 这类状态机字段。
这对交易/观察流程有用，但不适合作为 Phase01 的标准事实交接物。

### 根因 B：旧 source 输出摘要可读，但事实不可追溯

旧输出能快速告诉人“这个 token 进入什么状态”，但没有标准化交接资产：

- 没有 wallet_trade_normalized。
- 没有 wallet_entity_profile_normalized。
- 没有 wallet_intelligence_decision。
- 没有 same_source_evidence。
- 没有 bot2_handoff。
- 没有 missing field contract。

所以旧 source 的问题不是“完全没数据”，而是“有结论摘要，缺标准事实底座”。

### 根因 C：当前八组/router 有事实底座，但展示层还不够像旧 source 一样直观

当前输出的数据更完整、更合规，但如果直接把 router/index 结果展示给用户，会显得像系统文件清单，而不是“代币数据分析结果”。

因此真正差距在展示层：

- 旧 source：人类可读强，但边界污染。
- 当前 router：机器交接强，但需要一个 Phase01 专用的人类展示模板。

### 根因 D：当前 role_candidate_distribution 汇总脚本字段读取错位

复核 `wallet_intelligence_decision.json` 后确认：标准产物里实际存在 `role_candidates` 字段，例如“疑似接盘鲸鱼 / 疑似结构执行钱包 / 疑似结果钱包”。
之前对比汇总脚本只读取了 `role_candidate`、`wallet_role_candidate`、`decision_label` 等单数字段，所以错误汇总成 28 条 UNKNOWN。
这不是采集失败，也不是标准产物缺角色候选；是展示/汇总脚本没有兼容数组字段 `role_candidates`。

## 5. 修复方向

1. 保留当前 Phase01 router/fact store 作为主线，不回退到旧 source。
2. 从旧 source 借鉴“人类摘要展示方式”，但删除/隔离策略状态字段。
3. 新增一个 Phase01 token data display 模板，固定输出：
   - 基础行情事实。
   - 采集范围与记录数。
   - 钱包交易事实。
   - 钱包画像事实。
   - 证据等级/风险等级分布。
   - 同源候选组。
   - 缺失字段和待补查字段。
   - 质量状态与污染扫描。
4. 修复 wallet role candidate 字段映射，避免 28 条记录全显示 UNKNOWN。
5. 明确禁止在 Phase01 展示模板里出现：
   - PAPER_READY_CANDIDATE
   - WATCHING / BUY / SELL 等状态机字段
   - trade_allowed / execute_now / buy_signal / sell_signal

## 6. 最终判断

这次对比说明：

- 旧 source 的优势：输出像“结论摘要”，用户一眼能看懂。
- 旧 source 的问题：混入状态机和策略字段，缺少标准事实交接物。
- 当前八组/router 的优势：事实层完整、质量门禁明确、handoff 可用、污染扫描通过。
- 当前八组/router 的问题：需要补一个“代币数据展示层”，否则用户看到的是系统产物清单，而不是可读分析结果。

应采用的方向：

`当前 Phase01 fact store + 旧 source 可读摘要风格 - 旧 source 策略/状态污染 = 正确的新代币数据输出层`
