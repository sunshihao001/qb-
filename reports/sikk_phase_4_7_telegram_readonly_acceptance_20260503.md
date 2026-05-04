# SIKK Phase 4-7 验收报告：只读 Telegram 专业交互闭环

生成时间：2026-05-03

## 阶段范围

- Phase 4：接入只读 Telegram bot handler。
- Phase 5：支持 `查看 LITH` / `代币 LITH` / `仓位 P1` 中文自然语言触发。
- Phase 6：接入 Case File / Auto Review 详情按钮。
- Phase 7：`sikk_live_run.py` 每轮结束自动刷新统一 index 与 TG callback index。

## 修改文件

- `sikk_telegram_bot_handler.py`：新增只读 handler，暴露 `handle_text_message()` / `handle_callback_query()`。
- `sikk_telegram_zh.py`：扩展中文自然语言触发解析，支持代币 symbol 与仓位短码。
- `sikk_telegram_views.py`：新增 token/case/review 详情渲染，保留短码 callback。
- `sikk_unified_view_builder.py`：`telegram_callback_index.json` 增加 `review:P*` 与更完整 Case 引用。
- `sikk_live_run.py`：每轮结束自动调用 `build_unified_indexes()`，返回并写入 `unified_index_dir`、`telegram_callback_index_json`、`system_index_json`。
- `tests/test_sikk_telegram_bot_handler_phase_4_7.py`：新增 Phase 4-7 TDD 验收测试。
- `tests/test_sikk_unified_view_builder.py`：允许 callback index 的 `review` 类型。

## 输入文件

- `data/gmgn_candidates_live_run/site/dashboard_data.json`
- `data/gmgn_candidates_live_run/paper_live/paper_positions_open.json`
- `data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json`
- `data/gmgn_candidates_live_run/paper_live/case_files/case_files_manifest.json`
- `data/gmgn_candidates_live_run/live_run_manifest.json`

## 输出文件

- `data/gmgn_candidates_live_run/index/system_index.json`
- `data/gmgn_candidates_live_run/index/token_detail_index.json`
- `data/gmgn_candidates_live_run/index/position_index.json`
- `data/gmgn_candidates_live_run/index/case_file_index.json`
- `data/gmgn_candidates_live_run/index/auto_review_index.json`
- `data/gmgn_candidates_live_run/index/alert_index.json`
- `data/gmgn_candidates_live_run/index/telegram_callback_index.json`

## 验收命令与结果

```bash
python3 -m py_compile sikk_telegram_bot_handler.py sikk_telegram_zh.py sikk_telegram_views.py sikk_unified_view_builder.py sikk_live_run.py
# PASS

PYTHONPATH=. pytest -q tests/test_sikk_telegram_bot_handler_phase_4_7.py tests/test_sikk_telegram_views.py tests/test_sikk_unified_view_builder.py tests/test_sikk_live_run.py -q
# PASS: 24 passed

PYTHONPATH=. pytest -q tests/test_sikk_query.py tests/test_sikk_dashboard_site_builder.py tests/test_sikk_wallet_structure_daily_report.py -q
# PASS: 21 passed

PYTHONPATH=. python3 sikk_unified_view_builder.py --base-dir data/gmgn_candidates_live_run
# PASS: 写出 9 个 index JSON
```

## 真实样例输出

```text
查看 LITH -> 【LITH 代币详情】 callback=tok:T4 buttons=[pos:P1, case:C1, review:P1, menu:main]
仓位 P1 -> 【LITH 纸面仓位详情】 callback=pos:P1 buttons=[entry:P1, review:P1, list:open:0, menu:main]
case:C1 -> 【Case File 详情 C1】
review:P1 -> 【自动复盘 P1】
telegram_callback_index callback_count=330, has_review=True
```

## 安全审计

`live_run_manifest.json` 当前配置：

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

- 未新增 BUY / SELL / SWAP / EXECUTE / APPROVE / BROADCAST 按钮。
- Telegram handler 只返回 payload，不发送网络消息。
- 不读取私钥、不签名、不广播、不执行真实交易。
- callback_data 保持短码：`tok:T*`、`pos:P*`、`case:C*`、`review:P*`、`menu:main`。

## 完成结论

Phase 4-7 已形成最小可用只读闭环：统一索引 → 中文自然语言触发 → 只读 bot handler → Token/Position/Case/Review 详情 → live_run 每轮刷新 TG callback index。
