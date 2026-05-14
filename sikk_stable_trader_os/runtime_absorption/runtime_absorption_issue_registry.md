# Runtime Absorption Issue Registry

- created_at: 2026-05-14T20:34:54Z
- token: TROLLIEN `ECgweD7xkMj4bm8CcM9rusxKjyQGgdosCvVmhGUupump`
- scope: only issues exposed by this single-token replay

## ISSUE-001
- phase: P02/P03/P04/P07
- severity: HIGH
- issue: wallet_structure_decision reports missing wallet_address, role, game_side, evidence_level
- next_fix_task: 补齐 wallet row-level canonical export；保持旧路径 fallback；不改实时策略阈值
- realtime_rule_mutation_allowed: false

## ISSUE-002
- phase: P07/P08
- severity: HIGH
- issue: wallet gate observe-only allowed PAPER_READY while would_block=true / WALLET_BLOCK
- next_fix_task: 下一轮只评估 observe->enforce 的 Phase Controller 门禁参数，不直接改 live 策略
- realtime_rule_mutation_allowed: false

## ISSUE-003
- phase: P06
- severity: MEDIUM
- issue: scenario recognition is reconstructed from runtime outputs, not a native P06 bound runner output
- next_fix_task: 绑定现有 signal/kline/wallet outputs 到 P06 wrapper；仅生成被 replay 消费的输出
- realtime_rule_mutation_allowed: false

## ISSUE-004
- phase: P08
- severity: MEDIUM
- issue: quote_security_decision max_price_impact_pct is null
- next_fix_task: 补 quote/security 缺字段状态化与来源标记
- realtime_rule_mutation_allowed: false

## ISSUE-005
- phase: P09
- severity: MEDIUM
- issue: failure_attribution.jsonl 无该 token 专属 failure row，但 paper closed result 有 stop closure
- next_fix_task: 让 paper runner 对每个 closed position 写 token-level failure/review row
- realtime_rule_mutation_allowed: false

## ISSUE-006
- phase: P01-P09
- severity: HIGH
- issue: 部分既有 runner 原生 writes_handoff=false / trace 不是 Phase Controller 统一格式
- next_fix_task: 以 Phase Controller wrapper 收口 trace/handoff，不允许 runner 直连 paper
- realtime_rule_mutation_allowed: false
