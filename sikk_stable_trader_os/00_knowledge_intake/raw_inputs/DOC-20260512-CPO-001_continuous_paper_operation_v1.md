# Continuous Paper-only Operation 专业版 v1.0

## 持续纸面验证运行、样本积累、周期复盘、升级候选审查与系统稳定性监控任务包

---

## 0. 核心定位

`Continuous Paper-only Operation` 不是 P11，也不是 I06。

它属于：

```text
Operational Program：持续运行计划
```

专业定义：

```text
Continuous Paper-only Operation 是在 I05 Review / Upgrade Closed Loop 达到 I05_READY 或 I05_READY_WITH_GAPS 且允许进入 paper-only operation 后，把 P01-P10 与 I01-I05 的系统闭环转入连续、定时、可审计、可暂停、可复盘、可升级候选审查的纸面运行制度。
```

一句话：

> **I01-I05 证明系统能闭环。**  
> **Continuous Paper-only Operation 负责让闭环连续运行，积累多轮样本，并持续验证系统是否稳定、是否过拟合、是否需要升级。**

---

# 1. 它不负责什么

持续纸面验证运行必须明确禁止：

```text
不新增业务判断阶段
不绕过 P01-P10
不绕过 I01-I05
不真实下单
不钱包签名
不自动 swap
不自动部署
不直接修改策略规则
不直接修改 schema / contract / policy
不把 P09 复盘结论直接变成生产规则
不把单样本直接变成全局规则
不允许 live execution
```

它只负责：

```text
定时运行 P01-P08
定时进入 Paper-only Runtime
定时生成纸面仓位和权益曲线
定时触发 P09 复盘
定时触发 P10 升级候选审查
积累样本库
生成日报 / 周报 / 周期报告
监控系统健康
监控风险事件
监控数据缺口
生成下一轮修复任务包
```

---

# 2. 阶段目标

持续纸面验证运行必须一次性解决 24 类问题：

|编号|问题|必须输出|
|---|---|---|
|1|是否允许进入持续纸面运行？|`operation_readiness_gate_record`|
|2|每轮运行如何调度？|`paper_operation_schedule_record`|
|3|每轮运行读取哪些索引和合约？|`operation_input_manifest`|
|4|每轮候选如何进入 P01-P08？|`operation_cycle_record`|
|5|纸面仓位如何持续更新？|`paper_position_runtime_cycle_record`|
|6|多轮样本如何积累？|`paper_sample_library_record`|
|7|如何处理重复 token、重复信号？|`operation_dedup_record`|
|8|如何暂停异常样本？|`operation_pause_record`|
|9|如何记录风险事件？|`operation_risk_event_record`|
|10|如何判断系统健康？|`operation_health_record`|
|11|如何判断数据质量下降？|`operation_data_quality_record`|
|12|如何判断 runner 是否稳定？|`runner_stability_record`|
|13|如何判断 paper 模型是否失真？|`paper_model_drift_record`|
|14|如何生成每日复盘？|`daily_paper_review_record`|
|15|如何生成周期复盘？|`cycle_paper_review_record`|
|16|如何触发 P09？|`scheduled_p09_review_trigger_record`|
|17|如何触发 P10？|`scheduled_p10_upgrade_review_trigger_record`|
|18|如何防止过度升级？|`upgrade_throttle_record`|
|19|如何进入修复 sprint？|`targeted_fix_sprint_trigger_record`|
|20|如何记录系统指标？|`operation_metrics_record`|
|21|如何输出 Telegram / 报告摘要？|`operation_broadcast_record`|
|22|如何归档运行结果？|`operation_archive_record`|
|23|如何生成下一轮任务？|`next_operation_task_packet`|
|24|是否继续、暂停、回退、修复？|`operation_control_decision_record`|

---

# 3. 底层逻辑

## 3.1 持续运行不是“自动交易”，而是“连续验证”

错误理解：

```text
系统连续跑 = 自动交易
```

正确理解：

```text
系统连续跑 = 连续生成可验证样本
连续生成可复盘账本
连续发现系统缺口
连续改进 paper-only 判断质量
```

核心目标不是马上赚钱，而是建立：

```text
可信样本库
失败归因库
成功归因库
误判案例库
硬否定规则候选库
参数校准候选库
回归测试样例库
```

---

## 3.2 样本数量比单次结果更重要

单次 paper 盈亏不能说明系统有效。

持续运行要看：

```text
多轮样本是否稳定
胜率是否有结构性意义
亏损是否集中在某类场景
盈利是否来自真实判断还是模型乐观
滑点 / 费用后收益是否仍成立
P09 是否能解释失败
P10 是否能稳定生成受控升级候选
```

---

## 3.3 运行系统必须可暂停

持续运行不是无限运行。  
必须有暂停条件：

```text
数据源异常
trace 断裂
handoff 断裂
acceptance 失败
paper runtime 账本异常
风险事件过多
连续失败过多
P09 复盘失败
P10 升级包异常
检测到 live execution 路径
检测到 wallet signing 路径
```

---

## 3.4 P09 / P10 不能每次都强行升级

持续运行中会产生很多复盘结果，但不能每个样本都升级系统。

必须分层：

```text
单样本问题 → 记录案例
重复样本问题 → 生成升级候选
安全关键问题 → 临时保护性阻断候选
多轮一致问题 → P10 审查升级包
通过回归测试 → 进入受控实现
```

---

# 4. 运行结构

建议建立一个新的 Operational Program 目录，不再放在 Integration Program 下面：

```text
/root/sikk-gmgn/system/operational_program/continuous_paper_operation/
```

运行数据目录：

```text
/root/sikk-gmgn/data/operational_program/continuous_paper_operation/
```

核心结构：

```text
Continuous Paper-only Operation
  ↓
O01 Operation Readiness Gate
  ↓
O02 Scheduled Cycle Runner
  ↓
O03 Paper Runtime Monitor
  ↓
O04 Daily Review Trigger
  ↓
O05 P09/P10 Closed-loop Trigger
  ↓
O06 Operation Health & Risk Monitor
  ↓
O07 Sample Library & Metrics
  ↓
O08 Next Iteration Task Packet
```

注意：这里的 `O01-O08` 是运行子流程，不是新的业务阶段。

---

# 5. 必须建立的核心对象

|对象|作用|
|---|---|
|`Operation Readiness Gate Record`|是否允许进入持续纸面运行|
|`Operation Input Manifest`|每轮运行读取哪些文件|
|`Paper Operation Schedule Record`|定时运行计划|
|`Operation Cycle Record`|每一轮运行主记录|
|`Cycle Candidate Intake Record`|本轮候选进入 P01 情况|
|`Cycle Phase Execution Record`|P01-P08 本轮执行情况|
|`Cycle Paper Runtime Record`|本轮进入 paper runtime 的样本|
|`Paper Position Runtime Cycle Record`|开放仓位更新记录|
|`Operation Dedup Record`|去重、重复 token、重复信号|
|`Operation Pause Record`|暂停原因和恢复条件|
|`Operation Risk Event Record`|运行风险事件|
|`Operation Health Record`|系统健康状态|
|`Operation Data Quality Record`|数据质量状态|
|`Runner Stability Record`|runner 稳定性|
|`Paper Model Drift Record`|纸面模型失真监控|
|`Paper Sample Library Record`|样本库|
|`Daily Paper Review Record`|每日纸面复盘|
|`Cycle Paper Review Record`|周期复盘|
|`Scheduled P09 Review Trigger Record`|P09 触发记录|
|`Scheduled P10 Upgrade Review Trigger Record`|P10 触发记录|
|`Upgrade Throttle Record`|升级节流|
|`Targeted Fix Sprint Trigger Record`|触发修复 sprint|
|`Operation Metrics Record`|运行指标|
|`Operation Broadcast Record`|Telegram / 报告摘要|
|`Operation Archive Record`|归档|
|`Operation Control Decision Record`|继续 / 暂停 / 回退 / 修复决策|
|`Next Operation Task Packet`|下一轮运行任务包|

---

# 6. 系统目录

```text
/root/sikk-gmgn/system/operational_program/continuous_paper_operation/
```

必须创建：

```text
continuous_paper_operation_controller.yaml
continuous_paper_operation_context.md
operation_input_contract.yaml
operation_output_contract.yaml
operation_readiness_gate_schema.yaml
operation_input_manifest_schema.yaml
paper_operation_schedule_schema.yaml
operation_cycle_schema.yaml
cycle_candidate_intake_schema.yaml
cycle_phase_execution_schema.yaml
cycle_paper_runtime_schema.yaml
paper_position_runtime_cycle_schema.yaml
operation_dedup_schema.yaml
operation_pause_schema.yaml
operation_risk_event_schema.yaml
operation_health_schema.yaml
operation_data_quality_schema.yaml
runner_stability_schema.yaml
paper_model_drift_schema.yaml
paper_sample_library_schema.yaml
daily_paper_review_schema.yaml
cycle_paper_review_schema.yaml
scheduled_p09_review_trigger_schema.yaml
scheduled_p10_upgrade_review_trigger_schema.yaml
upgrade_throttle_schema.yaml
targeted_fix_sprint_trigger_schema.yaml
operation_metrics_schema.yaml
operation_broadcast_schema.yaml
operation_archive_schema.yaml
operation_control_decision_schema.yaml
next_operation_task_packet_contract.yaml
continuous_paper_operation_policy.yaml
continuous_paper_operation_hard_negative_rules.yaml
continuous_paper_operation_state_machine.yaml
continuous_paper_operation_trace_requirements.yaml
continuous_paper_operation_acceptance_criteria.md
continuous_paper_operation_storage_constitution.md
continuous_paper_operation_test_matrix.yaml
continuous_paper_operation_report_model.yaml
continuous_paper_operation_review_checklist.md
her_continuous_paper_operation_protocol.md
```

---

# 7. 运行数据目录

```text
/root/sikk-gmgn/data/operational_program/continuous_paper_operation/
  readiness_gate/
  input_manifest/
  schedules/
  cycles/
  candidate_intake/
  phase_execution/
  paper_runtime_cycles/
  position_runtime_cycles/
  dedup/
  pauses/
  risk_events/
  health/
  data_quality/
  runner_stability/
  model_drift/
  sample_library/
  daily_reviews/
  cycle_reviews/
  p09_triggers/
  p10_triggers/
  upgrade_throttle/
  targeted_fix_sprint/
  metrics/
  broadcasts/
  archive/
  control_decisions/
  next_operation_tasks/
  reports/
  audit/
  trace/
  acceptance/
```

继续使用 canonical paper runtime 目录：

```text
/root/sikk-gmgn/data/paper_runtime/
  positions_open/
  positions_closed/
  trades/
  equity_curve/
  runtime_events/
  exit_events/
  risk_events/
  snapshots/
  daily_reports/
  p09_review_inputs/
  trace/
  acceptance/
  handoff/
  reports/
  audit/
```

---

# 8. Operation Readiness Gate

持续运行前必须先过 readiness gate。

```yaml
operation_readiness_gate_record:
  readiness_id: string
  generated_at: datetime

  required_upstream_status:
    i05_status:
      allowed:
        - I05_READY
        - I05_READY_WITH_GAPS
      actual: string

    paper_operation_readiness_status:
      allowed:
        - CONTINUOUS_PAPER_OPERATION_ALLOWED
        - CONTINUOUS_PAPER_OPERATION_ALLOWED_WITH_GAPS
      actual: string

  required_assets:
    p01_to_p08_pipeline_available: boolean
    p08_to_paper_runtime_available: boolean
    paper_runtime_available: boolean
    p09_review_replay_available: boolean
    p10_self_upgrade_available: boolean
    trace_writer_available: boolean
    acceptance_runner_available: boolean
    handoff_writer_available: boolean
    path_guard_available: boolean

  safety_boundary:
    live_execution_allowed: false
    wallet_signing_allowed: false
    auto_order_allowed: false
    auto_deploy_allowed: false

  readiness_result:
    - OPERATION_READY
    - OPERATION_READY_WITH_GAPS
    - OPERATION_REQUIRES_FIX
    - OPERATION_BLOCKED

  allowed_next_mode:
    - SINGLE_CYCLE_PAPER_RUN
    - SCHEDULED_PAPER_RUN
    - PAPER_WITH_MANUAL_REVIEW
    - DRY_RUN_ONLY
    - BLOCKED

  blocking_reasons:
    - reason_id: string
      reason_cn: string
```

---

# 9. Paper Operation Schedule

```yaml
paper_operation_schedule_record:
  schedule_id: string
  generated_at: datetime

  schedule_mode:
    - MANUAL_SINGLE_CYCLE
    - HOURLY_PAPER_CYCLE
    - DAILY_PAPER_CYCLE
    - CUSTOM_INTERVAL
    - PAUSED

  cycle_frequency:
    interval_minutes: integer
    max_cycles_per_day: integer
    allowed_runtime_window:
      start_time: string | null
      end_time: string | null
      timezone: string

  per_cycle_limits:
    max_candidates_per_cycle: integer
    max_new_paper_positions_per_cycle: integer
    max_open_positions_total: integer
    max_same_token_positions: 1
    max_risk_events_per_cycle: integer
    max_runner_failures_per_cycle: integer

  review_schedule:
    p09_review:
      trigger:
        - POSITION_CLOSED
        - RISK_EVENT
        - DAILY_BATCH
        - MANUAL
      min_frequency: DAILY

    p10_upgrade_review:
      trigger:
        - WEEKLY_BATCH
        - HIGH_PRIORITY_SAFETY_CANDIDATE
        - MANUAL
      min_frequency: WEEKLY_OR_ON_SAFETY_EVENT

  safety:
    if_live_execution_detected: HARD_BLOCK
    if_wallet_signing_detected: HARD_BLOCK
    if_trace_chain_breaks: PAUSE_OPERATION
```

---

# 10. Operation Cycle Record

每一次运行都必须有 cycle 主记录。

```yaml
operation_cycle_record:
  cycle_id: string
  generated_at: datetime

  cycle_context:
    schedule_id: string
    cycle_start_time: datetime
    cycle_end_time: datetime | null
    execution_mode:
      - SINGLE_CYCLE_PAPER_RUN
      - SCHEDULED_PAPER_RUN
      - PAPER_WITH_MANUAL_REVIEW
      - DRY_RUN_ONLY

  upstream_assets:
    operation_readiness_id: string
    phase_controller_index_id: string
    runner_binding_index_id: string
    runtime_data_path_index_id: string

  cycle_status:
    - CYCLE_STARTED
    - CYCLE_RUNNING
    - CYCLE_COMPLETED
    - CYCLE_COMPLETED_WITH_GAPS
    - CYCLE_PAUSED
    - CYCLE_FAILED
    - CYCLE_BLOCKED

  cycle_outputs:
    candidate_count_received: integer
    candidates_passed_p08: integer
    paper_positions_opened: integer
    paper_positions_updated: integer
    paper_positions_closed: integer
    p09_reviews_triggered: integer
    p10_reviews_triggered: integer
    risk_events_created: integer

  trace:
    cycle_trace_id: string
    phase_trace_ids: list
```

---

# 11. Cycle Phase Execution

```yaml
cycle_phase_execution_record:
  execution_id: string
  cycle_id: string

  phase_execution:
    - phase_id: P01
      runner_id: string
      started_at: datetime
      ended_at: datetime | null
      status:
        - READY
        - READY_WITH_GAPS
        - REJECTED
        - BLOCKED
        - SKIPPED
        - FAILED
      input_handoff_id: string | null
      output_handoff_id: string | null
      acceptance_result_id: string | null
      trace_id: string | null
      gap_count: integer
      error_count: integer

    - phase_id: P02
    - phase_id: P03
    - phase_id: P04
    - phase_id: P05
    - phase_id: P06
    - phase_id: P07
    - phase_id: P08

  execution_summary:
    all_required_phases_completed: boolean
    blocked_phase_ids: list
    failed_phase_ids: list
    ready_with_gaps_phase_ids: list
    may_enter_paper_runtime: boolean
```

---

# 12. Cycle Paper Runtime Record

```yaml
cycle_paper_runtime_record:
  paper_runtime_cycle_id: string
  cycle_id: string
  generated_at: datetime

  p08_permissions:
    permission_records_received: integer
    runtime_allowed_count: integer
    runtime_allowed_with_limitations_count: integer
    runtime_blocked_count: integer

  paper_runtime_actions:
    new_positions_opened: integer
    existing_positions_updated: integer
    positions_closed: integer
    trades_recorded: integer
    equity_curve_updated: boolean
    risk_events_recorded: integer
    p09_review_inputs_created: integer

  quality:
    slippage_model_applied_count: integer
    cost_model_applied_count: integer
    default_slippage_used_count: integer
    default_cost_used_count: integer
    runtime_trace_complete: boolean

  status:
    - PAPER_RUNTIME_CYCLE_COMPLETED
    - PAPER_RUNTIME_CYCLE_WITH_GAPS
    - PAPER_RUNTIME_CYCLE_PAUSED
    - PAPER_RUNTIME_CYCLE_BLOCKED
```

---

# 13. Paper Sample Library

持续运行的核心资产是样本库。

```yaml
paper_sample_library_record:
  sample_library_id: string
  generated_at: datetime

  sample_index:
    - sample_id: string
      candidate_id: string
      token_address: string
      paper_position_id: string | null
      cycle_id: string
      sample_type:
        - PAPER_WIN
        - PAPER_LOSS
        - BREAKEVEN
        - BLOCKED_CORRECTLY
        - FALSE_POSITIVE
        - FALSE_NEGATIVE
        - RISK_EVENT_CASE
        - INVALIDATION_CASE
        - MODEL_DRIFT_CASE
      strategy_profile: string | null
      scenario_family: string | null
      primary_failure_stage: string | null
      primary_success_stage: string | null
      p09_review_case_id: string | null
      p10_upgrade_candidate_id: string | null

  sample_statistics:
    total_samples: integer
    closed_position_samples: integer
    open_position_samples: integer
    reviewed_samples: integer
    upgrade_candidate_samples: integer
    regression_candidate_samples: integer

  usage:
    used_for_p09_review: boolean
    used_for_p10_review: boolean
    used_for_regression_tests: boolean
    used_for_strategy_calibration: boolean
```

---

# 14. Operation Health Record

```yaml
operation_health_record:
  health_id: string
  cycle_id: string
  generated_at: datetime

  health_dimensions:
    data_source_health:
      status:
        - HEALTHY
        - DEGRADED
        - UNSTABLE
        - DOWN
      issue_count: integer

    runner_health:
      status:
        - HEALTHY
        - DEGRADED
        - UNSTABLE
        - FAILED
      failed_runner_count: integer

    trace_health:
      status:
        - COMPLETE
        - WITH_GAPS
        - BROKEN
        - UNUSABLE
      missing_trace_count: integer

    handoff_health:
      status:
        - COMPLETE
        - WITH_GAPS
        - BROKEN
        - UNUSABLE

    paper_runtime_health:
      status:
        - HEALTHY
        - WITH_GAPS
        - PAUSED
        - BLOCKED

    p09_p10_loop_health:
      status:
        - HEALTHY
        - WITH_GAPS
        - DEGRADED
        - BROKEN

  overall_health:
    - OPERATION_HEALTHY
    - OPERATION_HEALTHY_WITH_GAPS
    - OPERATION_DEGRADED
    - OPERATION_PAUSED
    - OPERATION_BLOCKED
```

---

# 15. Operation Risk Event

```yaml
operation_risk_event_record:
  risk_event_id: string
  cycle_id: string | null
  generated_at: datetime

  risk_event_type:
    - DATA_SOURCE_DOWN
    - DATA_STALE
    - RUNNER_FAILURE
    - TRACE_CHAIN_BROKEN
    - HANDOFF_CHAIN_BROKEN
    - ACCEPTANCE_FAILURE
    - PAPER_RUNTIME_FAILURE
    - P09_REPLAY_FAILURE
    - P10_UPGRADE_REVIEW_FAILURE
    - TOO_MANY_FAILED_CYCLES
    - TOO_MANY_LOSS_POSITIONS
    - MODEL_DRIFT_WARNING
    - LIVE_EXECUTION_ATTEMPT_BLOCKED
    - WALLET_SIGNING_ATTEMPT_BLOCKED
    - AUTO_DEPLOY_ATTEMPT_BLOCKED

  severity:
    - INFO
    - WARNING
    - HIGH
    - CRITICAL

  action_taken:
    - LOG_ONLY
    - MARK_DEGRADED
    - PAUSE_OPERATION
    - BLOCK_OPERATION
    - TRIGGER_P09_REVIEW
    - TRIGGER_FIX_SPRINT

  source_record_ids: list
  trace_id: string
```

---

# 16. Paper Model Drift Record

纸面模型失真必须持续监控。

```yaml
paper_model_drift_record:
  drift_id: string
  generated_at: datetime

  monitored_model:
    - ENTRY_PRICE_MODEL
    - SLIPPAGE_MODEL
    - COST_MODEL
    - EXIT_MODEL
    - LIQUIDITY_MODEL
    - SELLABILITY_MODEL

  drift_checks:
    default_model_used_too_often: boolean
    slippage_cost_underestimated: boolean | null
    exit_price_unrealistic: boolean | null
    cost_model_missing_rate_high: boolean
    liquidity_capacity_ignored: boolean | null

  drift_score:
    score_0_to_100: number
    status:
      - MODEL_STABLE
      - MODEL_DRIFT_WARNING
      - MODEL_DRIFT_HIGH
      - MODEL_UNRELIABLE

  p09_p10_action:
    trigger_p09_review: boolean
    generate_p10_runtime_model_upgrade_candidate: boolean
    block_scheduled_operation_until_fix: boolean
```

---

# 17. Daily Paper Review

```yaml
daily_paper_review_record:
  daily_review_id: string
  review_date: date
  generated_at: datetime

  paper_summary:
    cycles_run: integer
    candidates_processed: integer
    new_positions_opened: integer
    positions_closed: integer
    open_positions_end_of_day: integer
    gross_pnl_usd: number
    net_pnl_usd: number
    win_count: integer
    loss_count: integer
    breakeven_count: integer

  system_summary:
    runner_failures: integer
    trace_gaps: integer
    handoff_gaps: integer
    acceptance_failures: integer
    risk_events: integer
    paused_cycles: integer

  review_summary:
    p09_reviews_triggered: integer
    p09_reviews_completed: integer
    p10_candidates_created: integer
    p10_reviews_completed: integer

  decision:
    next_day_mode:
      - CONTINUE_SCHEDULED_PAPER
      - CONTINUE_WITH_LIMITATIONS
      - SINGLE_CYCLE_ONLY
      - PAUSE_FOR_FIX
      - BLOCKED

  reason_cn: string
```

---

# 18. Scheduled P09 / P10 Trigger

```yaml
scheduled_p09_review_trigger_record:
  trigger_id: string
  generated_at: datetime

  trigger_reason:
    - POSITION_CLOSED
    - LOSS_THRESHOLD_HIT
    - RISK_EVENT_TRIGGERED
    - DAILY_BATCH
    - MODEL_DRIFT_WARNING
    - MANUAL_REQUEST

  target_cases:
    paper_position_ids: list
    candidate_ids: list
    risk_event_ids: list

  trigger_result:
    - P09_TRIGGERED
    - P09_TRIGGERED_WITH_GAPS
    - P09_SKIPPED_NO_REVIEWABLE_CASE
    - P09_BLOCKED

  restrictions:
    p09_review_only: true
    no_rule_mutation: true
```

```yaml
scheduled_p10_upgrade_review_trigger_record:
  trigger_id: string
  generated_at: datetime

  trigger_reason:
    - WEEKLY_BATCH
    - HIGH_PRIORITY_P09_CANDIDATE
    - REPEATED_FAILURE_PATTERN
    - MODEL_DRIFT_CANDIDATE
    - MANUAL_REQUEST

  upgrade_candidates:
    calibration_candidate_ids: list
    missed_negative_rule_ids: list
    runtime_model_upgrade_candidate_ids: list
    test_case_candidate_ids: list

  trigger_result:
    - P10_TRIGGERED
    - P10_TRIGGERED_WITH_GAPS
    - P10_DEFERRED_NEED_MORE_SAMPLES
    - P10_BLOCKED

  restrictions:
    no_auto_deploy: true
    no_live_execution: true
    no_single_case_global_upgrade: true
```

---

# 19. Upgrade Throttle

防止系统过度升级。

```yaml
upgrade_throttle_record:
  throttle_id: string
  generated_at: datetime

  throttle_policy:
    max_p10_upgrade_reviews_per_day: integer
    max_controlled_packages_per_week: integer
    min_samples_for_global_rule_change: integer
    single_case_allowed_actions:
      - TEST_CASE_ONLY
      - MANUAL_REVIEW_ONLY
      - TEMPORARY_SAFETY_BLOCK_CANDIDATE

  current_usage:
    p10_reviews_today: integer
    packages_this_week: integer
    single_case_candidates_waiting: integer

  throttle_result:
    - UPGRADE_REVIEW_ALLOWED
    - UPGRADE_REVIEW_ALLOWED_TEST_ONLY
    - UPGRADE_REVIEW_DEFERRED
    - UPGRADE_REVIEW_BLOCKED
```

---

# 20. Operation Control Decision

```yaml
operation_control_decision_record:
  decision_id: string
  generated_at: datetime

  decision:
    - CONTINUE_SCHEDULED_PAPER
    - CONTINUE_WITH_LIMITATIONS
    - RUN_SINGLE_CYCLE_ONLY
    - PAUSE_FOR_FIX
    - TRIGGER_TARGETED_FIX_SPRINT
    - RETURN_TO_I03
    - RETURN_TO_I04
    - RETURN_TO_P09
    - RETURN_TO_P10
    - OPERATION_BLOCKED

  decision_basis:
    health_record_id: string
    risk_event_ids: list
    daily_review_id: string | null
    maturity_scorecard_id: string | null

  reason_cn: string

  required_next_actions:
    - action_id: string
      action_cn: string
      target:
        - I03
        - I04
        - P09
        - P10
        - PAPER_RUNTIME
        - RUNNER
        - TEST_MATRIX
        - CONTINUE

  restrictions:
    live_execution_allowed: false
    wallet_signing_allowed: false
    auto_deploy_allowed: false
```

---

# 21. Hard Negative Rules

```yaml
continuous_paper_operation_hard_negative_rules:
  - rule_id: CPO_BLOCK_001
    name: I05 未允许持续纸面运行
    condition: i05_permission_not_allowed == true
    result: OPERATION_BLOCKED

  - rule_id: CPO_BLOCK_002
    name: live execution 路径
    condition: live_execution_detected == true
    result: OPERATION_BLOCKED

  - rule_id: CPO_BLOCK_003
    name: 钱包签名路径
    condition: wallet_signing_detected == true
    result: OPERATION_BLOCKED

  - rule_id: CPO_BLOCK_004
    name: 自动下单路径
    condition: auto_order_detected == true
    result: OPERATION_BLOCKED

  - rule_id: CPO_BLOCK_005
    name: P07 绕过 P08
    condition: p07_direct_to_paper_runtime_detected == true
    result: OPERATION_BLOCKED

  - rule_id: CPO_BLOCK_006
    name: P08 handoff 缺失仍进入 Paper Runtime
    condition: paper_runtime_started_without_p08_handoff == true
    result: OPERATION_BLOCKED

  - rule_id: CPO_BLOCK_007
    name: Trace 链断裂
    condition: trace_chain_unusable == true
    result: OPERATION_PAUSED

  - rule_id: CPO_BLOCK_008
    name: Handoff 链断裂
    condition: handoff_chain_unusable == true
    result: OPERATION_PAUSED

  - rule_id: CPO_BLOCK_009
    name: P09 连续复盘失败
    condition: p09_replay_failures_consecutive >= 3
    result: OPERATION_PAUSED

  - rule_id: CPO_BLOCK_010
    name: P10 自动部署
    condition: p10_auto_deploy_detected == true
    result: OPERATION_BLOCKED

  - rule_id: CPO_BLOCK_011
    name: 单样本全局升级
    condition: single_case_global_upgrade_detected == true
    result: OPERATION_BLOCKED

  - rule_id: CPO_BLOCK_012
    name: 未登记路径写入
    condition: unregistered_write_path_detected == true
    result: OPERATION_BLOCKED
```

---

# 22. 状态机

```yaml
continuous_paper_operation_state_machine:
  states:
    - CPO_UNINITIALIZED
    - CPO_CONTEXT_LOADED
    - CPO_I05_PERMISSION_READ
    - CPO_READINESS_GATE_CHECKED
    - CPO_SCHEDULE_CREATED
    - CPO_INPUT_MANIFEST_BUILT
    - CPO_CYCLE_STARTED
    - CPO_PHASE_PIPELINE_EXECUTED
    - CPO_PAPER_RUNTIME_EXECUTED
    - CPO_POSITIONS_UPDATED
    - CPO_RISK_EVENTS_CHECKED
    - CPO_DAILY_REVIEW_BUILT
    - CPO_P09_TRIGGERS_BUILT
    - CPO_P09_REVIEWS_EXECUTED
    - CPO_P10_TRIGGERS_BUILT
    - CPO_P10_REVIEWS_EXECUTED
    - CPO_SAMPLE_LIBRARY_UPDATED
    - CPO_METRICS_UPDATED
    - CPO_HEALTH_CHECKED
    - CPO_OPERATION_DECISION_BUILT
    - CPO_NEXT_TASK_PACKET_BUILT
    - CPO_CONTINUE
    - CPO_CONTINUE_WITH_LIMITATIONS
    - CPO_SINGLE_CYCLE_ONLY
    - CPO_PAUSED
    - CPO_BLOCKED

  critical_transitions:
    - from: CPO_I05_PERMISSION_READ
      to: CPO_READINESS_GATE_CHECKED
      condition: i05_allows_paper_operation == true

    - from: CPO_READINESS_GATE_CHECKED
      to: CPO_SCHEDULE_CREATED
      condition: readiness_result in [OPERATION_READY, OPERATION_READY_WITH_GAPS]

    - from: CPO_SCHEDULE_CREATED
      to: CPO_CYCLE_STARTED
      condition: schedule_active == true

    - from: CPO_CYCLE_STARTED
      to: CPO_PHASE_PIPELINE_EXECUTED
      condition: p01_to_p08_pipeline_executed == true

    - from: CPO_PHASE_PIPELINE_EXECUTED
      to: CPO_PAPER_RUNTIME_EXECUTED
      condition: p08_permission_available == true

    - from: CPO_PAPER_RUNTIME_EXECUTED
      to: CPO_P09_TRIGGERS_BUILT
      condition: p09_review_inputs_created == true

    - from: CPO_P09_TRIGGERS_BUILT
      to: CPO_P09_REVIEWS_EXECUTED
      condition: p09_reviews_completed_or_deferred == true

    - from: CPO_P09_REVIEWS_EXECUTED
      to: CPO_P10_TRIGGERS_BUILT
      condition: p10_candidates_checked == true

    - from: CPO_P10_TRIGGERS_BUILT
      to: CPO_P10_REVIEWS_EXECUTED
      condition: p10_reviews_completed_or_deferred == true

    - from: CPO_P10_REVIEWS_EXECUTED
      to: CPO_SAMPLE_LIBRARY_UPDATED
      condition: sample_library_updated == true

    - from: CPO_SAMPLE_LIBRARY_UPDATED
      to: CPO_OPERATION_DECISION_BUILT
      condition: health_and_metrics_updated == true
```

---

# 23. Acceptance Criteria

```yaml
continuous_paper_operation_acceptance_criteria:
  CPO_READY:
    required:
      - i05_permission_read
      - readiness_gate_passed
      - schedule_created
      - operation_input_manifest_created
      - cycle_record_created
      - p01_to_p08_execution_recorded
      - paper_runtime_cycle_recorded
      - paper_positions_updated
      - risk_events_recorded
      - p09_triggers_created
      - sample_library_updated
      - health_record_created
      - operation_decision_created
      - no_live_execution
      - no_wallet_signing
      - no_auto_order
      - no_auto_deploy

  CPO_READY_WITH_GAPS:
    allowed_when:
      - limited_samples
      - low_confidence_attribution
      - optional_report_missing
      - p10_deferred_due_to_sample_count
    required:
      - safety_boundary_intact
      - trace_usable
      - handoff_usable
      - paper_runtime_usable

  CPO_PAUSED:
    triggered_by:
      - data_source_down
      - runner_failures_high
      - p09_replay_failures_consecutive
      - trace_chain_degraded
      - paper_model_drift_high

  CPO_BLOCKED:
    triggered_by:
      - live_execution_detected
      - wallet_signing_detected
      - p07_bypass_p08
      - paper_runtime_without_p08
      - trace_chain_unusable
      - p10_auto_deploy_detected
      - single_case_global_upgrade_detected
```

---

# 24. 测试矩阵

```yaml
continuous_paper_operation_test_matrix:
  - test_id: CPO_TEST_001
    name: I05_READY 后启动单轮 paper operation
    expected_status: CPO_READY

  - test_id: CPO_TEST_002
    name: I05 未允许持续运行
    expected_status: CPO_BLOCKED

  - test_id: CPO_TEST_003
    name: scheduled cycle 正常执行 P01-P08
    expected_status: CPO_READY

  - test_id: CPO_TEST_004
    name: P08 无 permission 但 runtime 尝试开仓
    expected_status: CPO_BLOCKED

  - test_id: CPO_TEST_005
    name: P07 直接进入 paper runtime
    expected_status: CPO_BLOCKED

  - test_id: CPO_TEST_006
    name: live execution path detected
    expected_status: CPO_BLOCKED

  - test_id: CPO_TEST_007
    name: wallet signing path detected
    expected_status: CPO_BLOCKED

  - test_id: CPO_TEST_008
    name: trace chain degraded but usable
    expected_status: CPO_READY_WITH_GAPS_OR_PAUSED

  - test_id: CPO_TEST_009
    name: trace chain unusable
    expected_status: CPO_BLOCKED

  - test_id: CPO_TEST_010
    name: P09 连续三次复盘失败
    expected_status: CPO_PAUSED

  - test_id: CPO_TEST_011
    name: P10 生成升级候选但样本不足
    expected_status: CPO_READY_WITH_GAPS

  - test_id: CPO_TEST_012
    name: P10 单样本全局升级
    expected_status: CPO_BLOCKED

  - test_id: CPO_TEST_013
    name: paper model drift high
    expected_status: CPO_PAUSED

  - test_id: CPO_TEST_014
    name: 数据源部分缺失但被 gap 传递
    expected_status: CPO_READY_WITH_GAPS

  - test_id: CPO_TEST_015
    name: 每日复盘生成 next_day_mode
    expected_status: CPO_READY

  - test_id: CPO_TEST_016
    name: 风险事件高于阈值
    expected_status: CPO_PAUSED_OR_TRIGGER_FIX_SPRINT

  - test_id: CPO_TEST_017
    name: sample library 正常累计
    expected_status: CPO_READY

  - test_id: CPO_TEST_018
    name: 未登记路径写入
    expected_status: CPO_BLOCKED
```

---

# 25. 报告模型

```yaml
continuous_paper_operation_report:
  report_id: string
  generated_at: datetime

  operation_summary:
    operation_status: string
    current_mode: string
    cycles_run_today: integer
    cycles_run_total: integer
    candidates_processed_today: integer
    candidates_processed_total: integer

  paper_runtime_summary:
    open_positions: integer
    closed_positions_today: integer
    total_closed_positions: integer
    gross_pnl_today: number
    net_pnl_today: number
    cumulative_net_pnl: number
    win_rate_closed: number
    median_return_closed: number
    max_win_pct: number
    max_loss_pct: number

  review_summary:
    p09_reviews_today: integer
    p09_reviews_total: integer
    failure_attribution_count: integer
    success_attribution_count: integer
    calibration_candidates_count: integer
    p10_reviews_today: integer
    controlled_upgrade_packages_count: integer

  system_health:
    overall_health: string
    data_source_health: string
    runner_health: string
    trace_health: string
    handoff_health: string
    paper_runtime_health: string
    p09_p10_loop_health: string

  risk_summary:
    risk_events_today: integer
    critical_events_today: integer
    operation_pauses_today: integer
    live_execution_attempts_blocked: integer
    wallet_signing_attempts_blocked: integer

  sample_library:
    total_samples: integer
    reviewed_samples: integer
    upgrade_candidate_samples: integer
    regression_candidate_samples: integer

  next_decision:
    operation_control_decision: string
    reason_cn: string
    required_next_actions: list
```

---

# 26. HER 正式任务书

```text
任务名称：Continuous Paper-only Operation：持续纸面验证运行任务包

目标：
在 /root/sikk-gmgn/system/operational_program/continuous_paper_operation/ 下建立持续纸面验证运行任务包，并在 /root/sikk-gmgn/data/operational_program/continuous_paper_operation/ 下生成持续运行输出。该任务包不是 P11，也不是 I06，不新增业务判断阶段，不修改 P01-P10 业务逻辑。它的目标是在 I05 Review / Upgrade Closed Loop 达到 I05_READY 或 I05_READY_WITH_GAPS 且允许进入 paper-only operation 后，把 P01-P10 与 I01-I05 闭环转入连续、定时、可审计、可暂停、可复盘、可升级候选审查的纸面运行制度。

核心原则：
1. 只允许 paper-only operation。
2. 不允许 live execution。
3. 不允许 wallet signing。
4. 不允许 auto order。
5. 不允许 auto deploy。
6. 不允许 P07 绕过 P08。
7. 不允许无 P08 permission 进入 Paper Runtime。
8. 不允许 P09 直接修改规则。
9. 不允许 P10 自动部署。
10. 不允许单样本直接全局升级。
11. 必须读取 I05 paper operation readiness。
12. 必须建立 operation readiness gate。
13. 必须建立 paper operation schedule。
14. 必须建立 operation cycle record。
15. 必须记录 P01-P08 每轮执行。
16. 必须记录 Paper Runtime 每轮运行。
17. 必须更新 paper sample library。
18. 必须触发 P09 scheduled review。
19. 必须触发 P10 scheduled upgrade review。
20. 必须建立 operation health / risk / data quality / runner stability 记录。
21. 必须生成 daily paper review。
22. 必须生成 operation control decision。
23. 必须生成 next operation task packet。
24. 必须支持 CONTINUE / CONTINUE_WITH_LIMITATIONS / SINGLE_CYCLE_ONLY / PAUSE / BLOCKED 分流。

需要创建系统目录：
/root/sikk-gmgn/system/operational_program/continuous_paper_operation/

需要创建系统文件：
1. continuous_paper_operation_controller.yaml
2. continuous_paper_operation_context.md
3. operation_input_contract.yaml
4. operation_output_contract.yaml
5. operation_readiness_gate_schema.yaml
6. operation_input_manifest_schema.yaml
7. paper_operation_schedule_schema.yaml
8. operation_cycle_schema.yaml
9. cycle_candidate_intake_schema.yaml
10. cycle_phase_execution_schema.yaml
11. cycle_paper_runtime_schema.yaml
12. paper_position_runtime_cycle_schema.yaml
13. operation_dedup_schema.yaml
14. operation_pause_schema.yaml
15. operation_risk_event_schema.yaml
16. operation_health_schema.yaml
17. operation_data_quality_schema.yaml
18. runner_stability_schema.yaml
19. paper_model_drift_schema.yaml
20. paper_sample_library_schema.yaml
21. daily_paper_review_schema.yaml
22. cycle_paper_review_schema.yaml
23. scheduled_p09_review_trigger_schema.yaml
24. scheduled_p10_upgrade_review_trigger_schema.yaml
25. upgrade_throttle_schema.yaml
26. targeted_fix_sprint_trigger_schema.yaml
27. operation_metrics_schema.yaml
28. operation_broadcast_schema.yaml
29. operation_archive_schema.yaml
30. operation_control_decision_schema.yaml
31. next_operation_task_packet_contract.yaml
32. continuous_paper_operation_policy.yaml
33. continuous_paper_operation_hard_negative_rules.yaml
34. continuous_paper_operation_state_machine.yaml
35. continuous_paper_operation_trace_requirements.yaml
36. continuous_paper_operation_acceptance_criteria.md
37. continuous_paper_operation_storage_constitution.md
38. continuous_paper_operation_test_matrix.yaml
39. continuous_paper_operation_report_model.yaml
40. continuous_paper_operation_review_checklist.md
41. her_continuous_paper_operation_protocol.md

需要创建运行数据目录：
/root/sikk-gmgn/data/operational_program/continuous_paper_operation/
  readiness_gate/
  input_manifest/
  schedules/
  cycles/
  candidate_intake/
  phase_execution/
  paper_runtime_cycles/
  position_runtime_cycles/
  dedup/
  pauses/
  risk_events/
  health/
  data_quality/
  runner_stability/
  model_drift/
  sample_library/
  daily_reviews/
  cycle_reviews/
  p09_triggers/
  p10_triggers/
  upgrade_throttle/
  targeted_fix_sprint/
  metrics/
  broadcasts/
  archive/
  control_decisions/
  next_operation_tasks/
  reports/
  audit/
  trace/
  acceptance/

运行输出要求：
1. operation_readiness_gate_record.yaml
2. operation_input_manifest.yaml
3. paper_operation_schedule_record.yaml
4. operation_cycle_record.yaml
5. cycle_candidate_intake_record.yaml
6. cycle_phase_execution_record.yaml
7. cycle_paper_runtime_record.yaml
8. paper_position_runtime_cycle_record.yaml
9. operation_dedup_record.yaml
10. operation_pause_record.yaml
11. operation_risk_event_record.yaml
12. operation_health_record.yaml
13. operation_data_quality_record.yaml
14. runner_stability_record.yaml
15. paper_model_drift_record.yaml
16. paper_sample_library_record.yaml
17. daily_paper_review_record.yaml
18. cycle_paper_review_record.yaml
19. scheduled_p09_review_trigger_record.yaml
20. scheduled_p10_upgrade_review_trigger_record.yaml
21. upgrade_throttle_record.yaml
22. targeted_fix_sprint_trigger_record.yaml
23. operation_metrics_record.yaml
24. operation_broadcast_record.yaml
25. operation_archive_record.yaml
26. operation_control_decision_record.yaml
27. next_operation_task_packet.yaml
28. continuous_paper_operation_report.md
29. continuous_paper_operation_acceptance_result.yaml

HER 执行顺序：
1. 读取 I05 closed loop acceptance result
2. 读取 paper operation readiness record
3. 读取 P01-P10 phase controller index
4. 读取 I02 directory / schema / contract / handoff index
5. 读取 I03 runner / tool binding
6. 读取 I04 paper runtime outputs
7. 建立 operation readiness gate
8. 建立 operation schedule
9. 建立 operation input manifest
10. 启动 operation cycle
11. 运行 P01-P08 pipeline
12. 读取 P08 paper runtime permission
13. 执行 Paper Runtime cycle
14. 更新 open / closed positions、trades、equity curve、risk events
15. 生成 P09 review input
16. 触发 P09 scheduled review
17. 根据 P09 输出触发 P10 scheduled review
18. 更新 sample library
19. 生成 operation health / risk / metrics
20. 生成 daily paper review
21. 生成 operation control decision
22. 生成 next operation task packet
23. 输出 continuous paper operation report
24. 根据 decision 继续、限制、单轮、暂停或阻断

最终验收标准：
只有当系统具备 readiness gate、schedule、cycle record、P01-P08 execution record、paper runtime cycle、position update、risk event、sample library、daily review、P09 trigger、P10 trigger、upgrade throttle、health monitor、data quality monitor、runner stability monitor、model drift monitor、operation decision、next task packet，并且没有 live execution、没有 wallet signing、没有 auto order、没有 auto deploy、没有 P07 bypass、没有 P10 单样本全局升级时，才允许标记为 CPO_READY。
```

---

# 27. 当前是否达到专业化设计标准

## 判断

这一版 `Continuous Paper-only Operation` 达到：

```text
专业化
轻量机构水准
一次性把持续运行应有数据补全
不是最小版本
不是简单定时脚本
不是自动交易系统
```

它被明确设计为：

```text
持续纸面运行控制层
定时 cycle 层
P01-P08 执行记录层
Paper Runtime 连续账本层
P09 周期复盘触发层
P10 周期升级审查层
样本库积累层
风险事件监控层
系统健康监控层
模型漂移监控层
运行决策层
下一轮任务包生成层
```

---

# 28. 完成后下一步

完成 `Continuous Paper-only Operation` 后，下一步不是实盘，而是：

```text
多轮纸面运行样本积累
  ↓
P09 日复盘
  ↓
P10 周期升级候选审查
  ↓
Targeted Fix Sprint 定向修复
  ↓
Regression Replay 回归回放
  ↓
Scheduled Paper Operation 稳定化
```

只有当多轮纸面运行满足以下条件，才有资格讨论下一层：

```text
连续多周期无 trace / handoff / acceptance 断裂
P09 可稳定复盘
P10 可稳定审查升级候选
paper model drift 可控
滑点 / 费用模型不过度乐观
风险事件可解释
系统不会自动实盘
样本库具备足够统计意义
```

---

# 尚未解决问题

|问题|当前状态|后续处理|
|---|---|---|
|是否有足够 paper 样本|初期通常不足|连续运行积累|
|是否能自动定时稳定运行|需要 runner 实现|HER / cron / tmux / orchestrator|
|P09 是否每天稳定复盘|需要运行验证|Daily Review 触发|
|P10 是否过度频繁升级|已设计 throttle|周期性审查|
|滑点 / 费用模型是否真实|仍需样本校准|P09/P10 修正|
|是否可以进入实盘|不能|当前仍是 paper-only|
|Telegram 面板是否接入|可作为报告输出|不应优先于运行稳定性|
|是否需要 Targeted Fix Sprint|由 operation decision 触发|下一步设计|

---

# 本次认知升级点

1. **持续纸面验证运行不是自动交易，而是连续样本验证系统。**
    
2. **核心资产不是单次收益，而是 paper sample library。**
    
3. **持续运行必须有 readiness gate、schedule、cycle、health、risk、decision。**
    
4. **P09 / P10 必须周期性触发，但不能过度升级。**
    
5. **升级节流是专业系统必需能力。**  
    否则系统会被单样本和短期噪音污染。
    
6. **持续运行必须可暂停、可回退、可进入定向修复。**
    
7. **CPO_READY 只代表可以持续 paper-only，不代表可以实盘。**
    
8. **下一步应进入 Targeted Fix Sprint，而不是实盘执行层。**