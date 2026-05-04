# SIKK Phase 0-8 /compress handoff

生成时间：2026-05-03

## 用户给定执行序列

1. `/branch`
2. `/goal`
3. `/codebase_inspection` → Phase 0 侦察
4. `/codex` → Phase 1 中文术语层
5. `/codex` → Phase 2 callback index
6. `/codex` → Phase 3 中文视图函数
7. `/codex` → Phase 4 bot handler
8. `/dogfood` → Phase 5 第一闭环验收
9. `/codex` → Phase 6 全面板补齐
10. `/codex` → Phase 7 runtime 刷新
11. `/codebase_inspection` → Phase 8 安全审计
12. `/compress`

## 当前分支状态

- Git branch: `sikk-paper-audit-20260502`
- 当前工作区存在既有未提交修改与新增文件；本轮遵循“不删除已有模块、不动真实交易逻辑”。

## Phase 0 侦察结论

关键已有/新增落点：

- `sikk_live_run.py`：canonical main entry；每轮输出 runtime/site/paper/report，并已接入统一 index 刷新。
- `sikk_unified_view_builder.py`：统一索引生成器。
- `sikk_telegram_zh.py`：中文术语与自然语言触发层。
- `sikk_telegram_views.py`：中文 Telegram payload 渲染层。
- `sikk_telegram_bot_handler.py`：只读 bot handler 适配层。
- `data/gmgn_candidates_live_run/index/telegram_callback_index.json`：callback 短码索引。
- `reports/sikk_phase_4_7_telegram_readonly_acceptance_20260503.md`：阶段验收报告。

代码体量粗略扫描（排除 data/.git/cache/venv）：

- Markdown: 80 files / 62911 lines
- Python: 103 files / 25057 lines
- JSON: 34 files / 4361 lines
- CSV: 62 files / 1229 lines
- Shell: 10 files / 727 lines
- Total: 289 files / 94285 lines

注：`pygount` 在当前 Hermes venv 缺 pip，无法安装；已用 Python 文件扫描替代。

## Phase 1 中文术语层

文件：`sikk_telegram_zh.py`

已支持：

- 状态中文化：`HOLD_WITH_DATA_RISK`、`WALLET_BLOCK`、`UNKNOWN` 等。
- 固定触发：`系统总览`、`开放仓位`、`风险提醒` 等。
- 自然语言触发：
  - `查看 LITH` → `tok:T*`
  - `代币 LITH` → `tok:T*`
  - `仓位 P1` → `pos:P1`

## Phase 2 callback index

文件：`sikk_unified_view_builder.py`

已输出：

- `telegram_callback_index.json`
- callback 短码包括：
  - `menu:main`
  - `list:open:0`
  - `tok:T*`
  - `pos:P*`
  - `case:C*`
  - `review:P*`
  - `alert:A*`

当前样例：`callback_count=330`，且无 forbidden callback。

## Phase 3 中文视图函数

文件：`sikk_telegram_views.py`

已支持：

- 主菜单：`render_main_menu()`
- 开放仓位列表：`render_open_positions()`
- 仓位详情：`render_position_detail()`
- 风险提醒：`render_alerts()`
- 代币详情：`render_token_detail()`
- Case File 详情：`render_case_detail()`
- 自动复盘详情：`render_review_detail()`
- 统一入口：`render_by_callback()`

## Phase 4 bot handler

文件：`sikk_telegram_bot_handler.py`

已提供：

- `handle_text_message(text, index_dir=...)`
- `handle_callback_query(callback_data, index_dir=...)`

边界：只读 payload 层，不直接连接 Telegram，不发送消息，不交易，不签名，不广播。

## Phase 5 第一闭环验收

测试：`tests/test_sikk_telegram_bot_handler_phase_4_7.py`

样例：

```text
查看 LITH -> 【LITH 代币详情】 callback=tok:T4 buttons=[pos:P1, case:C1, review:P1, menu:main]
仓位 P1 -> 【LITH 纸面仓位详情】 callback=pos:P1 buttons=[entry:P1, review:P1, list:open:0, menu:main]
case:C1 -> 【Case File 详情 C1】
review:P1 -> 【自动复盘 P1】
```

## Phase 6 全面板补齐

已补齐最小全链路面板：

- token detail
- position detail
- case detail
- review detail
- alerts
- main menu

保留项：`entry:P*` 目前仍是预留入口，可后续补“入场证据详情”。

## Phase 7 runtime 刷新

文件：`sikk_live_run.py`

每轮结束后自动：

```python
unified_result = build_unified_indexes(root)
```

返回路径新增：

- `unified_index_dir`
- `telegram_callback_index_json`
- `system_index_json`

## Phase 8 安全审计

已跑命令：

```bash
PYTHONPATH=. pytest -q tests/test_sikk_telegram_bot_handler_phase_4_7.py tests/test_sikk_telegram_views.py tests/test_sikk_unified_view_builder.py tests/test_sikk_live_run.py tests/test_sikk_system_audit.py -q
# PASS: 28 passed
```

Manifest safety：

```json
{
  "broadcast_allowed": false,
  "confirmation_enabled": false,
  "dashboard_enabled": true,
  "notification_enabled": false,
  "real_swap_enabled": false,
  "telegram_broadcast_enabled": false,
  "telegram_target": "",
  "trace_enabled": true
}
```

安全结论：PASS。

- 无真实交易按钮。
- 无自动 swap。
- 无私钥读取。
- 无签名。
- 无 broadcast。
- callback 短码无 BUY/SELL/SWAP/EXECUTE/APPROVE/BROADCAST。

## 验收命令历史

```bash
python3 -m py_compile sikk_telegram_bot_handler.py sikk_telegram_zh.py sikk_telegram_views.py sikk_unified_view_builder.py sikk_live_run.py
# PASS

PYTHONPATH=. pytest -q tests/test_sikk_telegram_bot_handler_phase_4_7.py tests/test_sikk_telegram_views.py tests/test_sikk_unified_view_builder.py tests/test_sikk_live_run.py -q
# PASS: 24 passed

PYTHONPATH=. pytest -q tests/test_sikk_query.py tests/test_sikk_dashboard_site_builder.py tests/test_sikk_wallet_structure_daily_report.py -q
# PASS: 21 passed

PYTHONPATH=. pytest -q tests/test_sikk_telegram_bot_handler_phase_4_7.py tests/test_sikk_telegram_views.py tests/test_sikk_unified_view_builder.py tests/test_sikk_live_run.py tests/test_sikk_system_audit.py -q
# PASS: 28 passed
```

## 下一步建议

如果继续推进，建议下一轮做：

1. 补 `entry:P*` 入场证据详情页。
2. 把只读 bot handler 接入真实 Telegram gateway adapter，但仍保持 no-trade/no-sign/no-broadcast。
3. 对 `site/` 静态控制台做 dogfood 浏览器 QA。
4. 如果要提交代码，先整理 git diff，避免把历史 data 大文件误提交。
