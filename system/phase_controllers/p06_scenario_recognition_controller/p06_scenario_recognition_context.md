# P06 Scenario Recognition Controller Context v3.0

P06 将 P05 evidence bundle、反证、未知、冲突与替代解释转为可追踪、可否定、可冲突处理、可交接给 P07 的场景识别对象。

## Boundary
- P06 只输出场景候选/主次场景/冲突/否定/未知/置信度/失效条件/P07 data request/P06→P07 handoff。
- P06 不输出买卖建议、paper_ready、执行许可、开仓、止盈止损或实盘确认。
- P06 只能交接给 P07 Strategy Gate Controller。

## Required startup checks
1. P05 acceptance passed.
2. P05→P06 handoff exists.
3. Evidence bundle usage permission checked.
4. Conflict/unknown/rejection paths enabled.
5. Runtime/paper/live all blocked.
