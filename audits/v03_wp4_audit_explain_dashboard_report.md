# v0.3 WP4 审计报告：审计、解释、dashboard/paper review 闭环

## 1. 工作包目标

WP4 的目标不是新增交易执行，而是把 v0.3 已落地的三条核心链路纳入系统治理闭环：

```text
筹码控制权状态机 → 市值上下文 → 主导侧/对手盘生命周期
```

并确保审计层、解释层、dashboard/paper review 能发现缺字段、解释证据链、保留 paper-only 边界。

## 2. 修改文件

- 修改：`sikk_system_audit.py`
- 修改：`sikk_explainability_engine.py`
- 修改：`tests/test_sikk_system_audit.py`
- 修改：`tests/test_sikk_explainability_engine.py`
- 新增：`audits/v03_wp4_audit_explain_dashboard_report.md`

## 3. v0.3 审计闭环

`sikk_system_audit.py` 新增 v0.3 必查字段：

```text
chip_control_state
chip_control_action
market_cap_context
market_cap_context_quality
dominant_side_lifecycle
dominant_side_intent
counterparty_state
```

审计时会把 `market_cap_context`、`chip_control`、`lifecycle` 这些嵌套字段展平检查，避免 dashboard 表面存在 token 行、但 v0.3 关键证据链缺失。

## 4. v0.3 解释闭环

`sikk_explainability_engine.py` 现在会引用：

- `chip_control_state` / `chip_control_action`
- `market_cap_context.paper_entry_market_cap_usd`
- `dominant_side_lifecycle` / `dominant_side_intent` / `counterparty_state`

解释层仍保持原边界：

```text
只解释既有输出；不重新裁决；不生成交易授权；不调用采集、swap、cooking、广播。
```

## 5. 测试结果

指定测试：

```bash
PYTHONPATH=/root/sikk-gmgn pytest -q tests/test_sikk_explainability_engine.py tests/test_sikk_system_audit.py
```

结果：

```text
6 passed in 0.03s
```

全量回归：

```bash
PYTHONPATH=/root/sikk-gmgn pytest -q
```

结果：

```text
133 passed in 9.48s
```

## 6. 安全审计结论

- 本工作包只读/解释/审计，不签名、不广播、不执行真实买卖。
- 未调用 `gmgn_swap`。
- 未调用 `gmgn_cooking`。
- 未引入 `yolo` 或真实交易确认绕过。
- `WALLET_SUPPORT` 仍只代表 paper gate 支持，不能绕过 signal/quote/security。

## 7. 结论

v0.3 的治理闭环已形成：

```text
状态机给出筹码控制权状态
市值上下文记录发现→信号→钱包→paper→当前/退出
生命周期分类把主导侧/对手盘证据回写状态机
审计层检查 v0.3 关键字段是否缺失
解释层把 v0.3 证据链转为可读复盘文本
```
