# Phase Controller Index

阶段是系统流程边界，不是孤立 Skill。每个 Controller 负责读取合约、调用候选 Atomic Skill/runtime module、输出标准状态、handoff 和 audit。

## Controller Map

- `P00` 系统宪法层: `phase_00_system_constitution_controller.md` — missing；system constitution / global rules / safety boundary
- `P01` 数据事实层: `phase_01_data_fact_controller.md` — present；fact normalization / field quality / freshness
- `P02` 结构地址层: `phase_02_wallet_structure_controller.md` — present；wallet roles / same-source / distribution / backflow / infra exclusion
- `P03` 筹码控制层: `phase_03_chip_control_controller.md` — present；retention / transfer / distribution pressure / dominant side
- `P04` 场景盘型层: `phase_04_scenario_recognition_controller.md` — present；risk-first scenario / counter-evidence / pattern classification
- `P05` 结构位置层: `phase_05_structure_position_controller.md` — present；POC / AVWAP / failure / fatigue / overextension
- `P06` 策略门禁层: `phase_06_strategy_gate_controller.md` — present；hard-negative inheritance / A+P1 / evidence chain
- `P07` 执行风控层: `phase_07_execution_risk_controller.md` — present；quote / security / liquidity / slippage / paper-only
- `P08` 复盘学习层: `phase_08_review_learning_controller.md` — present；failure attribution / case library / rule candidates
- `P09` 系统升级层: `phase_09_system_upgrade_controller.md` — present；review-only upgrade packages / regression / rollback / shadow

## Non-Negotiable Rules

- Controller 不自定义状态码；只引用全局状态表。
- Controller 不直接给实盘授权。
- Controller 必须写 `positive_evidence`、`counter_evidence`、`missing`、`hard_negatives`、`handoff_packet`、`audit`。
- 上游 hard negative 必须继承到下游。
