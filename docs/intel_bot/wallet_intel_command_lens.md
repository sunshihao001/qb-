# Intel Bot 分析命令镜头

这些命令面向 Telegram 查询与报告展示，不连接交易执行。

## /SCAN_WALLET_SOURCE
- 用途：scan source provenance and catalog legacy wallet artifacts
- 输入：archive path, source manifest, query scope
- 输出：source inventory, provenance bundle, trace refs
- 安全用途：read-only inventory and validation

## /DEEP_WALLET_ROLE
- 用途：deep role profiling for a wallet or address
- 输入：wallet address, token scope, history window
- 输出：role candidate, evidence grade, role rationale
- 安全用途：address profiling only, no execution hints

## /TRACE_SAME_SOURCE
- 用途：trace same-source candidates and relation edges
- 输入：address set, token set
- 输出：group id, relation edges, conflict notes
- 安全用途：for relation analysis and grouping

## /TRACE_BACKFLOW
- 用途：trace chip backflow and source reversal patterns
- 输入：wallet set, token window
- 输出：backflow flags, backflow path, pressure score
- 安全用途：for migration analysis only

## /DELTA_CHIP
- 用途：compare multi-round chip deltas
- 输入：snapshot A, snapshot B
- 输出：delta table, direction summary, evidence notes
- 安全用途：historical delta comparison

## /HYP_DOMINANT_INTENT
- 用途：hypothesize dominant intent from multi-layer evidence；专业表达为主导侧行为动机推断，不称为“庄家心理”
- 输入：holder cluster, profile, behavior, lifecycle, cost zone, inventory, distribution progress, counterparty pressure, pattern alignment
- 输出：dominant_intent_decision, confidence, evidence breakdown
- 输出枚举：ACCUMULATE, CONTROL, WASHOUT, BREAKOUT_TEST, MARKUP, PARTIAL_DISTRIBUTION, ACTIVE_DISTRIBUTION, REACCUMULATION, REACTIVATION, ABANDONMENT
- 安全用途：hypothesis only, not execution guidance；不能直接 PAPER_READY/BLOCKED，不能开仓/止损/止盈，不能改状态机

## /ANGLE_WALLET_PATTERN
- 用途：summarize wallet pattern angles for review
- 输入：wallet data bundle
- 输出：pattern angles, review notes, anomaly hints
- 安全用途：pattern summarization and dashboard display

## /CHALLENGE_SCORE
- 用途：challenge or inspect score robustness
- 输入：wallet score, evidence bundle
- 输出：score stress test, weakness points
- 安全用途：score audit and robustness check

## /BUILD_GMGN_NOTE
- 用途：build GMGN note table rows from evidence
- 输入：wallet decision, role profile
- 输出：gmgn_note_table rows
- 安全用途：reporting/export only

## /BUILD_WALLET_DECISION
- 用途：assemble wallet_structure_decision from all evidence layers
- 输入：all evidence layers
- 输出：wallet_structure_decision artifact
- 安全用途：trading-side handoff file generation only
