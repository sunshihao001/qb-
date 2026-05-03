# SIKK-SOL v0.3 工作包拆分

## 总目标

把当前 v0.2 paper-only 可复盘骨架升级为 v0.3：

```text
筹码控制权状态机独立化 + 市值上下文全链路贯穿 + 主导侧/对手盘生命周期闭环
```

## 全局安全边界

- paper-only。
- 禁止真实买入。
- 禁止真实卖出。
- 禁止调用 `gmgn_swap`。
- 禁止调用 `gmgn_cooking`。
- 禁止交易广播 / send transaction。
- 禁止 `yolo`。
- 任何 `WALLET_SUPPORT` / `CONTROL_RETAINED_BY_STRUCTURE_SIDE` 仅允许进入 paper/观察条件，不等于买入授权。

## 测试命令

统一使用：

```bash
PYTHONPATH=/root/sikk-gmgn pytest -q
```

## WP1：独立筹码控制权状态机

### 目标

新增 `sikk_chip_control_state_machine.py`，把当前散落在 `sikk_wallet_structure_gate.py` 中的筹码控制逻辑抽离为独立、可测试、可解释的状态机。

### 输入

- wallet structure decision / summary
- dominant lifecycle row（可选）
- market context row（可选）
- paper position row（可选）

### 输出

- `chip_control_state`
- `chip_control_confidence`
- `chip_control_action`
- `chip_control_reason_codes`
- `chip_control_evidence_refs`
- `chip_control_invalidators`

### 文件

- 新增：`sikk_chip_control_state_machine.py`
- 新增：`tests/test_sikk_chip_control_state_machine.py`
- 修改：`sikk_wallet_structure_gate.py` 只做轻量接入，不扩大职责
- 报告：`audits/v03_wp1_chip_control_state_machine_report.md`

### 验收

- 缺输入不崩溃，输出 `CONTROL_UNCLEAR` 或 `DATA_QUALITY_FAIL`。
- `CONTROL_RETAINED_BY_STRUCTURE_SIDE` 不绕过 signal/quote/security。
- 对手盘压力、同源卖出、集中清仓优先触发迁移/丢失/阻断。
- 单测覆盖保留、迁移、派发丢失、不清晰、数据质量失败。

## WP2：市值上下文全链路贯穿

### 目标

建立统一 `market_cap_context` 合约，让市值从发现、信号、钱包判断、paper 入场、当前、退出可复盘。

### 输出字段

```text
discovery_market_cap_usd
signal_market_cap_usd
wallet_decision_market_cap_usd
paper_entry_market_cap_usd
current_market_cap_usd
exit_market_cap_usd
market_cap_change_from_discovery_pct
market_cap_change_from_signal_pct
market_cap_change_from_wallet_decision_pct
market_cap_context_quality
market_cap_missing_fields
```

### 文件

- 新增或增强：`sikk_market_cap_context.py`
- 修改：`sikk_live_run.py`
- 修改：`sikk_dashboard_builder.py`
- 新增：`tests/test_sikk_market_cap_context.py`
- 报告：`audits/v03_wp2_market_cap_context_report.md`

### 验收

- 支持中英文字段读取。
- 缺市值字段显示 `待补` / `MISSING`，不能编造。
- dashboard 与 token_status 显示发现→信号→钱包→paper→当前→退出市值。

## WP3：主导侧/对手盘生命周期闭环

### 目标

让 `sikk_dominant_lifecycle_classifier.py` 与 WP1 状态机形成闭环：生命周期不只是旁路分类，而是成为筹码控制权状态与 paper 行动的证据输入。

### 文件

- 修改：`sikk_dominant_lifecycle_classifier.py`
- 修改/接入：`sikk_chip_control_state_machine.py`
- 新增或修改测试：`tests/test_sikk_dominant_lifecycle_classifier.py`
- 报告：`audits/v03_wp3_lifecycle_closed_loop_report.md`

### 验收

- ACTIVE_DISTRIBUTION / FINAL_DISTRIBUTION / STRUCTURE_COLLAPSE 能驱动 CONTROL_LOST 或 CONTROL_MIGRATING。
- SECOND_STAGE_EXPANSION / REACTIVATION 只能增强观察或 paper candidate，不直接交易。
- 输出主导侧意图、对手盘状态、失效条件、替代假设。

## WP4：v0.3 审计、解释、dashboard/paper review 闭环

### 目标

让审计层、解释层、dashboard、live_state、paper review 全部读取 v0.3 输出。

### 文件

- 修改：`sikk_system_audit.py`
- 修改：`sikk_explainability_engine.py`
- 修改：`sikk_dashboard_builder.py`
- 修改：`sikk_live_run.py`
- 报告：`audits/v03_final_audit_report.md`

### 验收

- 全量测试通过。
- 审计报告能指出 chip_control / market_cap_context / lifecycle 缺口。
- 解释引擎能回答为什么保留控制、为什么迁移、为什么丢失、为什么暂停或阻断。
- dashboard 不只显示裸状态，而显示事件级证据链。
- 最终 git 提交。
