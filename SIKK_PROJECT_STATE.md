# SIKK Project State

更新时间：2026-05-03T13:00:42Z

## 当前阶段

Phase B-0.5：连续运行 + 纸面验证 + 本地静态专业可视化控制台。

## 当前系统定位

SIKK-GMGN / SIKK-SOL 当前是 Solana 结构智能、候选发现、钱包结构门禁、quote/security、状态机、纸面交易、日报复盘和可视化观测系统。

当前阶段保持：

- 纸面验证 / readiness / observability only。
- 不执行真实 swap。
- 不读取、写入或保存私钥。
- 不自动签名或自动 broadcast。
- 不把 dashboard 做成交易执行后台。

## Canonical 主入口

```bash
cd /root/sikk-gmgn
python3 sikk_live_run.py   --output-root data/gmgn_candidates_live_run   --limit 50   --quote-sources okx   --default-quote-amount-sol 0.01   --mode once
```

连续运行命令：

```bash
cd /root/sikk-gmgn
python3 sikk_live_run.py   --output-root data/gmgn_candidates_live_run   --limit 50   --quote-sources okx   --default-quote-amount-sol 0.01   --mode loop   --interval-sec 600
```

## 入口边界

- `sikk_live_run.py` 是唯一 canonical main entrypoint。
- `sikk_live_orchestrator.py` 只作为 observability / professional live_board / token-status 组件复用。
- 禁止同时对同一个 `data/gmgn_candidates_live_run` 启动 `sikk_live_run.py --mode loop` 与 `sikk_live_orchestrator.py --mode loop`。

## 已实现/保留模块

- `sikk_live_run.py`
- `sikk_live_orchestrator.py`
- `sikk_dashboard_builder.py`
- `sikk_dashboard_site_builder.py`
- `sikk_query.py`（只读统一查询层早期版）
- `sikkctl.py`（移动端友好 CLI 早期版）
- `sikk_telegram_open.py`（Telegram 只读 view 雏形，后续需短码 callback 化）
- `sikk_paper_live_runner.py`
- `sikk_wallet_structure_gate.py`
- `sikk_candidate_wallet_structure_pipeline.py`
- `sikk_candidate_state_machine.py`
- `sikk_candidate_quote_security_pipeline.py`
- `sikk_wallet_structure_daily_report.py`
- `sikk_notifier.py`（可选，默认关闭/凭证外置）
- `live_board.md`
- `live_dashboard.html`
- paper daily report / wallet structure daily report

## 当前新增目标

从本地静态专业可视化控制台继续升级为统一索引驱动的专业交互系统：

```text
sikk_live_run.py
  -> paper JSON/CSV
  -> live_state / live_board / live_dashboard
  -> site/dashboard_data.json / index.html / app.js / style.css
  -> wallet daily report
  -> data/gmgn_candidates_live_run/index/*.json
  -> CLI / Web / Telegram / Report / Alert
```

探究设计文档：

```text
docs/plans/sikk_professional_interaction_investigation_design_20260503.md
```

后续首个代码落点：

```text
sikk_unified_view_builder.py
tests/test_sikk_unified_view_builder.py
data/gmgn_candidates_live_run/index/system_index.json
```

## 当前已知状态

- `sikk_dashboard_site_builder.py`：已存在并生成 `site/` 静态控制台。
- `data/gmgn_candidates_live_run/site/`：已存在。
- `sikk_query.py` / `sikkctl.py`：已存在，只读查询层早期版。
- `sikk_telegram_open.py`：已存在 Telegram view 早期版，保留作兼容查询雏形。
- `sikk_telegram_bot_handler.py`：已存在 Phase 4-7 只读 Telegram handler，支持中文自然语言触发与 callback payload。
- `sikk_telegram_views.py` / `sikk_telegram_zh.py`：已支持 `查看 LITH`、`代币 LITH`、`仓位 P1`、`tok:T*`、`pos:P*`、`entry:P*`、`case:C*`、`review:P*` 只读详情。
- `sikk_telegram_gateway_adapter.py`：已存在 Phase 9 只读 Telegram update 适配器，只返回 `sendMessage`/`editMessageText` payload shape，不联网发送、不交易、不签名、不广播。
- `sikk_unified_view_builder.py`：已存在，Section A + Phase 4-7 + Phase 9 已实现，生成 `data/gmgn_candidates_live_run/index/*.json` 与 `telegram_callback_index.json`，callback index 已包含 `entry:P*`。
- `sikk_live_run.py`：每轮结束自动刷新统一 index 与 Telegram callback index。
- `data/gmgn_candidates_live_run/index/`：已存在，包含 system/token/position/case/auto_review/alert/telegram_callback 统一索引。
- `data/gmgn_candidates_live_run/live_state.json`：存在，含 token 汇总。
- `data/gmgn_candidates_live_run/tokens/*/token_status.json`：存在。
- `data/gmgn_candidates_live_run/paper_live/*`：存在，JSON/CSV 同步输出已存在。
- `data/gmgn_candidates_live_run/events/live_events.jsonl`：存在。
- `data/gmgn_candidates_live_run/state_machine/candidate_states.json`：存在。
- `data/gmgn_candidates_live_run/wallet_structure/*/wallet_structure_decision.json`：存在。

## 严格禁止

- 不删除已有 Runtime / dashboard / notifier / paper runner / confirmation 相关模块。
- 不新增真实交易按钮。
- 不新增实盘 swap、私钥、签名、自动 broadcast。
- 不新增 FastAPI 后端、数据库、登录系统、React 大项目。
- 不新增 Telegram/Discord 功能扩张。
- 不把 `priority_level` 当作买入信号；它只用于 dashboard 排序。
