# Section A 验收报告：统一索引层

时间：2026-05-03T13:00Z

## 1. 本节目标

实现 `sikk_unified_view_builder.py`，把 `sikk_live_run.py` 已生成的 paper/live/site/report 输出统一收敛到：

```text
data/gmgn_candidates_live_run/index/*.json
```

供后续 CLI / Web / Telegram / Report / Alert 共用。

## 2. 修改 / 新增文件

新增：

```text
sikk_unified_view_builder.py
tests/test_sikk_unified_view_builder.py
```

生成输出：

```text
data/gmgn_candidates_live_run/index/system_index.json
data/gmgn_candidates_live_run/index/token_detail_index.json
data/gmgn_candidates_live_run/index/position_index.json
data/gmgn_candidates_live_run/index/latest_open_positions.json
data/gmgn_candidates_live_run/index/latest_closed_positions.json
data/gmgn_candidates_live_run/index/case_file_index.json
data/gmgn_candidates_live_run/index/auto_review_index.json
data/gmgn_candidates_live_run/index/alert_index.json
data/gmgn_candidates_live_run/index/telegram_callback_index.json
```

## 3. 输入文件

```text
data/gmgn_candidates_live_run/live_run_manifest.json
data/gmgn_candidates_live_run/live_state.json
data/gmgn_candidates_live_run/live_board.md
data/gmgn_candidates_live_run/live_dashboard.html
data/gmgn_candidates_live_run/site/dashboard_data.json
data/gmgn_candidates_live_run/site/index.html
data/gmgn_candidates_live_run/site/app.js
data/gmgn_candidates_live_run/site/style.css
data/gmgn_candidates_live_run/paper_live/paper_positions_open.json
data/gmgn_candidates_live_run/paper_live/paper_positions_open.csv
data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json
data/gmgn_candidates_live_run/paper_live/paper_positions_closed.csv
data/gmgn_candidates_live_run/paper_live/case_files/case_files_manifest.json
data/gmgn_candidates_live_run/reports/wallet_structure_daily_report_20260503.csv/json/md
```

## 4. TDD 验收过程

RED：先写测试并确认失败：

```text
ModuleNotFoundError: No module named 'sikk_unified_view_builder'
```

GREEN：实现模块后运行：

```bash
PYTHONPATH=. pytest -q tests/test_sikk_unified_view_builder.py -q
```

结果：

```text
..... [100%]
```

全链路相关测试：

```bash
PYTHONPATH=. pytest -q tests/test_sikk_unified_view_builder.py tests/test_sikk_query.py tests/test_sikk_dashboard_site_builder.py -q
```

结果：

```text
........................ [100%]
```

## 5. 真实运行命令

```bash
python3 sikk_unified_view_builder.py --base-dir data/gmgn_candidates_live_run
```

结果：成功写入 `data/gmgn_candidates_live_run/index/` 下 9 个 JSON 索引文件。

## 6. 真实样例输出

### system_index 摘要

```json
{
  "entrypoint": {"canonical": "sikk_live_run.py", "mode": "paper_runtime_once"},
  "counts": {"token_count": 156, "open_position_count": 5, "closed_position_count": 178, "opportunity_count": 26},
  "paper_sync": {"open_json_count": 5, "closed_json_count": 178, "open_csv_count": 5, "closed_csv_count": 178, "open_csv_exists": true, "closed_csv_exists": true},
  "safety": {"real_swap_enabled": false, "broadcast_allowed": false, "private_key_required": false, "confirmation_enabled": false, "telegram_broadcast_enabled": false}
}
```

### Telegram callback 摘要

```json
{
  "callback_count": 250,
  "sample": {
    "menu:main": {"type": "menu", "view": "main"},
    "list:open:0": {"type": "list", "view": "open_positions", "page": 0},
    "tok:T1": {"type": "token", "token_id": "T1", "token_symbol": "AALIEN"}
  }
}
```

### Alert 摘要

```json
{
  "alert_count": 6,
  "alerts": [
    {"alert_id": "A1", "type": "DATA_SYNC_FAIL", "severity": "HIGH", "title": "钱包结构覆盖缺口较高", "action": "数据补全"},
    {"alert_id": "A2", "type": "PAPER_DRAWDOWN", "severity": "MEDIUM", "title": "开放纸面仓位浮亏", "action": "观察"},
    {"alert_id": "A3", "type": "WALLET_BLOCK", "severity": "HIGH", "title": "开放纸面仓位钱包结构阻断", "action": "退出监控"}
  ]
}
```

## 7. 安全审计

已确认：

```text
real_swap_enabled=False
broadcast_allowed=False
private_key_required=False
confirmation_enabled=False
telegram_broadcast_enabled=False
```

统一索引层只读取本地文件并写入 JSON；不采集、不报价、不交易、不签名、不广播。

Alert 只输出中文提醒动作：

```text
记录 / 观察 / 复查 / 暂停纸面入场 / 退出监控 / 数据补全
```

不输出 BUY / SELL / SWAP / EXECUTE / APPROVE / BROADCAST 交易动作。

## 8. 是否允许进入下一节

PASS。允许进入 Section B：让 `sikk_query.py` / `sikkctl.py` 优先读取 `data/gmgn_candidates_live_run/index/*.json`。
