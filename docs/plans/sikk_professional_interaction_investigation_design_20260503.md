# SIKK 专业交互系统探究设计 v20260503T130042Z

## 0. 目标

按 share 方法轮执行：先侦察现状，再把需求拆成可验收 Section Task，最后更新项目认知与运行验证。

本轮不是直接做真实交易功能，而是升级 SIKK 的“认知能力 / 探究设计”：把 `sikk_live_run.py` 单入口产生的 paper/live/site/report 输出，规划为统一索引驱动的 CLI / Web / Telegram / Report / Alert 专业交互系统。

## 1. 固定安全边界

- `sikk_live_run.py` 仍为主入口。
- paper JSON / CSV 同步必须保留。
- wallet daily report 使用新 CSV / 新汇总口径。
- live_state / live_board / live_dashboard / site 必须继续由主入口联动输出。
- `site/dashboard_data.json`、`site/index.html`、`site/app.js`、`site/style.css` 必须保持可生成。
- safety 默认关闭真实交易：不执行真实 swap，不读取私钥，不签名，不广播。
- Telegram / Web / CLI 只做查询、展示、复盘、诊断；不新增交易按钮。

## 2. 当前侦察结论

### 2.1 已存在能力

- 单入口：`sikk_live_run.py` 已存在并能生成 live / paper / site / report 输出。
- 查询层：`sikk_query.py` 已存在，能从 `dashboard_data.json` / live / paper 输出聚合为只读查询索引。
- CLI：`sikkctl.py` 已存在，支持：
  - `board`
  - `token <symbol_or_address>`
- Telegram view 雏形：`sikk_telegram_open.py` 已存在，但目前 callback 使用 `sikk_token:<token_address>`，不是短码索引。
- 项目认知文件已存在：
  - `SIKK_SYSTEM_INDEX.md`
  - `SIKK_PROJECT_STATE.md`
  - `SIKK_CHANGELOG.md`
  - `SIKK_NEXT_TASK.md`
- 知识吸收目录已存在：`knowledge/`。
- 最新 live 输出已存在：
  - `data/gmgn_candidates_live_run/live_run_manifest.json`
  - `data/gmgn_candidates_live_run/live_state.json`
  - `data/gmgn_candidates_live_run/live_board.md`
  - `data/gmgn_candidates_live_run/live_dashboard.html`
  - `data/gmgn_candidates_live_run/site/dashboard_data.json`
  - `data/gmgn_candidates_live_run/site/index.html`
  - `data/gmgn_candidates_live_run/site/app.js`
  - `data/gmgn_candidates_live_run/site/style.css`
  - `data/gmgn_candidates_live_run/paper_live/paper_positions_open.json`
  - `data/gmgn_candidates_live_run/paper_live/paper_positions_open.csv`
  - `data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json`
  - `data/gmgn_candidates_live_run/paper_live/paper_positions_closed.csv`
  - `data/gmgn_candidates_live_run/reports/wallet_structure_daily_report_20260503.md`

### 2.2 当前缺口

- 还没有实体文件：`sikk_unified_view_builder.py`。
- 还没有输出目录：`data/gmgn_candidates_live_run/index/`。
- 还没有持久化统一索引文件：
  - `system_index.json`
  - `token_detail_index.json`
  - `position_index.json`
  - `latest_open_positions.json`
  - `latest_closed_positions.json`
  - `case_file_index.json`
  - `auto_review_index.json`
  - `alert_index.json`
- Telegram 还不是完整中文专业控制台：
  - 缺少 `sikk_telegram_views.py`
  - 缺少 `sikk_telegram_callback_index.py`
  - 缺少短码 callback：`tok:T1` / `pos:P1` / `case:C1` / `menu:main`
  - 缺少分页、详情、多面板、安全审计测试
- Alert 还没有统一索引层；后续应只生成风险提醒，不推交易执行。

## 3. 目标架构

```text
sikk_live_run.py
  ↓
paper JSON / CSV
live_state / live_board / live_dashboard
site/dashboard_data.json / index.html / app.js / style.css
reports/wallet_structure_daily_report_*.csv|json|md
  ↓
sikk_unified_view_builder.py
  ↓
data/gmgn_candidates_live_run/index/
  system_index.json
  token_detail_index.json
  position_index.json
  latest_open_positions.json
  latest_closed_positions.json
  case_file_index.json
  auto_review_index.json
  alert_index.json
  telegram_callback_index.json
  ↓
sikkctl.py / Web / Telegram / Report / Alert
```

## 4. Section Task 拆分

### Section A：统一索引层

- 修改 / 新增文件：
  - 新增：`sikk_unified_view_builder.py`
  - 新增测试：`tests/test_sikk_unified_view_builder.py`
  - 可选修改：`sikk_live_run.py` 在每轮结束调用 builder
- 输入文件：
  - `data/gmgn_candidates_live_run/site/dashboard_data.json`
  - `data/gmgn_candidates_live_run/live_state.json`
  - `data/gmgn_candidates_live_run/paper_live/paper_positions_open.json`
  - `data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json`
  - `data/gmgn_candidates_live_run/paper_live/paper_positions_open.csv`
  - `data/gmgn_candidates_live_run/paper_live/paper_positions_closed.csv`
  - `data/gmgn_candidates_live_run/paper_live/case_files/case_files_manifest.json`
  - `data/gmgn_candidates_live_run/reports/wallet_structure_daily_report_*.csv`
- 输出文件：
  - `data/gmgn_candidates_live_run/index/system_index.json`
  - `data/gmgn_candidates_live_run/index/token_detail_index.json`
  - `data/gmgn_candidates_live_run/index/position_index.json`
  - `data/gmgn_candidates_live_run/index/latest_open_positions.json`
  - `data/gmgn_candidates_live_run/index/latest_closed_positions.json`
  - `data/gmgn_candidates_live_run/index/case_file_index.json`
  - `data/gmgn_candidates_live_run/index/auto_review_index.json`
  - `data/gmgn_candidates_live_run/index/alert_index.json`
- 核心字段：
  - `schema_version`
  - `generated_at`
  - `boundary`
  - `source_files`
  - `safety`
  - `system_health`
  - `paper_sync`
  - `token_count`
  - `open_position_count`
  - `closed_position_count`
  - `wallet_daily_report_ref`
  - `top_alerts`
- 验收命令：
  - `PYTHONPATH=. pytest -q tests/test_sikk_unified_view_builder.py -q`
  - `python3 sikk_unified_view_builder.py --base-dir data/gmgn_candidates_live_run`

### Section B：CLI 读取统一索引

- 修改文件：
  - `sikk_query.py`
  - `sikkctl.py`
  - `tests/test_sikk_query.py`
- 输入文件：`data/gmgn_candidates_live_run/index/*.json`
- 输出：中文 CLI 总览与单币 / 单仓位详情。
- 验收命令：
  - `PYTHONPATH=. pytest -q tests/test_sikk_query.py -q`
  - `python3 sikkctl.py board --base-dir data/gmgn_candidates_live_run`
  - `python3 sikkctl.py token <symbol_or_address> --base-dir data/gmgn_candidates_live_run`

### Section C：Telegram 中文专业控制台视图层

- 新增文件：
  - `sikk_telegram_views.py`
  - `sikk_telegram_callback_index.py`
  - `tests/test_sikk_telegram_views.py`
  - `tests/test_sikk_telegram_callback_index.py`
- 输入文件：`data/gmgn_candidates_live_run/index/*.json`
- 输出：只读 Telegram payload：
  - M0 系统总览
  - M1 开放仓位
  - M2 已关闭仓位
  - M3 单代币详情
  - M4 单仓位详情
  - M5 入场证据
  - M6 钱包结构
  - M7 持仓过程
  - M8 自动复盘
  - M9 系统健康
  - M10 风险提醒
- callback_data 规则：
  - `menu:main`
  - `list:open:0`
  - `list:closed:0`
  - `tok:T1`
  - `pos:P1`
  - `case:C1`
  - `alert:A1`
  - `refresh:main`
- 禁止：
  - 中文 callback_data
  - 长地址直接进入 callback_data
  - BUY / SELL / SWAP / EXECUTE / APPROVE / BROADCAST 按钮
- 验收命令：
  - `PYTHONPATH=. pytest -q tests/test_sikk_telegram_views.py tests/test_sikk_telegram_callback_index.py -q`

### Section D：Web 点击详情层

- 修改文件：
  - `sikk_dashboard_site_builder.py`
  - `tests/test_sikk_dashboard_site_builder.py`
- 输入文件：`data/gmgn_candidates_live_run/index/*.json`
- 输出：`site/index.html` / `app.js` 中单币、仓位、case、alert 的详情视图。
- 验收命令：
  - `PYTHONPATH=. pytest -q tests/test_sikk_dashboard_site_builder.py -q`

### Section E：Alert System 只读提醒层

- 新增 / 修改文件：
  - `sikk_alert_index_builder.py` 或并入 `sikk_unified_view_builder.py`
  - `tests/test_sikk_alert_index.py`
- 输入：open positions、wallet structure、failure attribution、risk events、strategy panel。
- 输出：`index/alert_index.json`
- 提醒类型：
  - `WALLET_BLOCK`
  - `HIGH_COUNTERPARTY_PRESSURE`
  - `PAPER_DRAWDOWN`
  - `QUOTE_STALE`
  - `SECURITY_SCAN_MISSING`
  - `DATA_SYNC_FAIL`
- 安全边界：Alert 只提醒，不交易。

### Section F：主入口联动与全链路验收

- 修改文件：`sikk_live_run.py`
- 要求：每轮结束后刷新统一索引；如果 builder 失败，写事件与健康状态，不影响 safety 默认关闭。
- 验收命令：
  - `python3 sikk_live_run.py --output-root data/gmgn_candidates_live_run --limit 50 --quote-sources okx --default-quote-amount-sol 0.01 --mode once`
  - `python3 -m json.tool data/gmgn_candidates_live_run/index/system_index.json >/dev/null`
  - `python3 -m json.tool data/gmgn_candidates_live_run/index/alert_index.json >/dev/null`

## 5. 本轮已完成 / 后续执行顺序

本轮完成：

1. 侦察已有能力和缺口。
2. 生成本文档作为专业交互系统探究设计。
3. 下一步更新项目认知文档。
4. 最后运行当前可用测试和安全验收。

后续实际代码实现顺序：

1. Section A：统一索引层。
2. Section B：CLI 改为优先读统一索引。
3. Section C：Telegram 中文专业控制台视图层。
4. Section D：Web 点击详情层。
5. Section E：Alert 只读提醒层。
6. Section F：`sikk_live_run.py` 每轮结束刷新 index。

## 6. 验收口径

任一 Section 必须同时满足：

- 有代码落点。
- 有输入文件。
- 有输出文件。
- 有字段 schema。
- 有测试命令。
- 有运行命令。
- 有真实样例输出。
- 有 safety 审计：真实交易默认关闭。
