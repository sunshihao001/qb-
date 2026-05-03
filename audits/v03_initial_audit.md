# SIKK-SOL v0.3 初始审计报告

- 生成时间：2026-05-03T01:18:52.271080Z
- 阶段目标：v0.3 = 筹码控制权状态机独立化 + 市值上下文全链路贯穿 + 主导侧/对手盘生命周期闭环。
- 安全边界：paper-only；禁止真实买入/卖出；禁止 `gmgn_swap` / `gmgn_cooking` / 交易广播 / `yolo`。
- 测试基线：`PYTHONPATH=/root/sikk-gmgn pytest -q` 已通过，结果 `124 passed in 10.26s`。

## 1. Git 状态

```text
sikk-paper-audit-20260502
40ef1a6
?? config/
?? data/
?? reports/
```

## 2. v0.3 相关模块行数

```text
653 sikk_wallet_structure_gate.py
   246 sikk_wallet_trade_adapter.py
   456 sikk_system_audit.py
   428 sikk_explainability_engine.py
   273 sikk_dashboard_builder.py
   590 sikk_live_run.py
   544 sikk_dominant_lifecycle_classifier.py
  3190 total
```

## 3. 关键词命中概览

- 筹码控制权：19 条样例命中。
- 市值上下文：57 条样例命中。
- 主导侧/对手盘生命周期：80 条样例命中。
- paper/dashboard/失败归因：80 条样例命中。
- 交易安全风险关键词：80 条样例命中；需逐项确认均为说明/禁止/边界，而非真实执行入口。

## 4. 审计结论

1. `sikk_wallet_structure_gate.py` 已包含 `chip_control_state` 与 `CONTROL_RETAINED_BY_STRUCTURE_SIDE` / `CONTROL_MIGRATING_TO_COUNTERPARTY` / `CONTROL_LOST_TO_DISTRIBUTION` / `CONTROL_UNCLEAR`，但逻辑仍嵌在钱包门禁内，v0.3 需要独立成 `sikk_chip_control_state_machine.py`，让状态、证据、降级、失效条件可单测、可复盘。
2. 市值字段已散落在 K线、候选、dashboard、paper 字段位中，但尚未形成统一 `market_cap_context` 合约；v0.3 需要从发现、信号、钱包判断、paper 入场、当前、退出全链路保存。
3. `sikk_dominant_lifecycle_classifier.py` 已有主导侧生命周期评分、意图、对手盘状态，但与筹码控制权状态尚未形成统一闭环；v0.3 应让生命周期输出成为筹码控制状态机的输入之一。
4. `sikk_live_run.py` 已能合并状态机、quote/security、paper、failure attribution；v0.3 需补充 `chip_control` 与 `market_cap_context` 到 token_status/live_state/dashboard。
5. 未跟踪 `config/`、`data/`、`reports/` 继续视为运行数据，暂不纳入代码提交。

## 5. v0.3 工作包建议

- WP1：新增 `sikk_chip_control_state_machine.py`，抽离筹码控制权状态机，并接入 `sikk_wallet_structure_gate.py`。
- WP2：新增/增强市场上下文标准化模块，贯穿 `discovery_market_cap_usd` → `signal_market_cap_usd` → `wallet_decision_market_cap_usd` → `paper_entry_market_cap_usd` → `current_market_cap_usd` → `exit_market_cap_usd`。
- WP3：增强主导侧/对手盘生命周期闭环，使 `sikk_dominant_lifecycle_classifier.py` 输出能进入筹码控制状态机、审计与解释层。
- WP4：系统审计、解释引擎、dashboard/live/paper review 读取 v0.3 输出；全量测试；生成最终审计报告并提交。
