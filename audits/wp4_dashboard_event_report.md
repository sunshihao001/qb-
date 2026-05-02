# WP4 Dashboard 事件级字段升级审计报告

## 范围
- 工作包：WP4 dashboard 事件级字段升级 + paper runner / 状态机接入检查。
- 主要模块：`sikk_dashboard_builder.py`。
- 只读检查/轻量接入补强：`sikk_live_run.py`。
- 安全边界：paper-only；未启用、未新增真实交易、gmgn_swap/gmgn_cooking、交易广播或 yolo 路径。

## 已完成修改
1. `sikk_dashboard_builder.py`
   - 将 dashboard token 表从基础状态表升级为“Token 状态 / 事件链路”表。
   - 新增读取/合并来源：
     - `live_state.json` 中的 token_status 字段；
     - `paper_live/paper_positions_open.json`；
     - `paper_live/paper_positions_closed.json` 或 `paper_positions_closed.csv` fallback；
     - `paper_live/failure_attribution.jsonl`。
   - 新增展示字段：
     - `discovered_at`
     - `discovery_market_cap_usd`
     - `discovery_liquidity_usd`
     - `first_signal_at`
     - `first_signal_type`
     - `signal_market_cap_usd`
     - `wallet_decision_at`
     - `wallet_decision_market_cap_usd`
     - `wallet_structure_status`
     - `paper_entry_at`
     - `paper_entry_market_cap_usd`
     - `paper_entry_price`
     - `paper_entry_amount_sol`
     - `paper_entry_amount_usd`
     - `paper_token_amount`
     - `current_market_cap_usd`
     - `current_price`
     - `unrealized_pnl_sol`
     - `unrealized_pnl_pct`
     - `exit_monitor_at`
     - `paper_exit_at`
     - `exit_reason`
     - `failure_attribution_type`
   - 缺失字段统一显示 `待补`，避免空白和崩溃。
   - 表格增加横向滚动容器，适配事件级长字段。

2. `sikk_live_run.py`
   - 检查主流程发现：`run_live_once()` 已通过 `paper_runner` 输出、`build_enriched_runtime_statuses()`、`_write_live_state()`、`write_dashboard()` 串起状态机 → paper live → live_state → dashboard。
   - 轻量补强 `build_enriched_runtime_statuses()`：从 open/closed paper positions 与 failure_attribution 合并 paper event 字段到 token status，供 dashboard 与 token_status 消费。
   - 保持真实交易相关配置默认关闭：`confirmation_enabled=False`、`real_swap_enabled=False`、`broadcast_allowed=False`。

3. 测试
   - `tests/test_sikk_runtime_v02.py`
     - 扩展 dashboard builder 测试，覆盖事件级字段、paper open position、failure attribution、`待补` 缺失字段显示。
   - `tests/test_sikk_live_run.py`
     - 扩展 fake paper runner 输出入场价/当前价/PnL 等字段。
     - 验证 `live_state.json` 与 `live_dashboard.html` 能承载 paper event 字段。
     - 验证 failure attribution 的 `EXIT_MONITOR` 与 `failure_type` 合并到 runtime status。

## 接入检查结论
- 状态机接入：`sikk_live_run.build_enriched_runtime_statuses()` 从 `state_machine/candidate_states.json` 构建 runtime token status，保留状态机当前状态并合并 quote/security 与 paper 输出。
- Paper runner 接入：`run_live_once()` 将 `paper_runner()` 输出目录固定为 `paper_live/`，dashboard builder 直接读取同一目录的 open/closed/failure 文件。
- Dashboard 输出：`write_dashboard()` 继续输出升级版 `live_dashboard.html`，现在不再只显示 token/state/score，可展示发现 → 判断 → 入场 → 持仓 → 退出/失败归因链路。
- 缺字段行为：新增 `_display()` / formatter，缺失值统一显示 `待补`。

## 测试结果
- 指定测试：
  - 命令：`PYTHONPATH=/root/sikk-gmgn pytest -q tests/test_sikk_runtime_v02.py tests/test_sikk_live_run.py`
  - 首次结果：`11 passed in 0.11s`
  - 写报告后复验：`11 passed in 0.07s`
- 全量测试：
  - 命令：`PYTHONPATH=/root/sikk-gmgn pytest -q`
  - 首次结果：`124 passed in 9.44s`
  - 写报告后复验：`124 passed in 9.39s`

## 修改文件
- `sikk_dashboard_builder.py`
- `sikk_live_run.py`
- `tests/test_sikk_runtime_v02.py`
- `tests/test_sikk_live_run.py`
- `audits/wp4_dashboard_event_report.md`

## 真实交易触碰说明
- 未触碰真实交易。
- 未新增或调用 `gmgn_swap` / `gmgn_cooking` / 交易广播 / yolo。
- 本次变更仅做 dashboard 展示、runtime status 合并与测试覆盖，保持 paper-only 安全边界。
