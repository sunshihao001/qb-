# SIKK-SOL 审计后工作包拆分

生成时间: 2026-05-02T23:21Z
项目路径: /root/sikk-gmgn
当前分支: sikk-paper-audit-20260502
基线提交: 428536b

## 全局安全边界

- 模式: paper-only。
- 禁止: 真实买入、真实卖出、gmgn_swap、gmgn_cooking、交易广播、yolo。
- 原则: 兼容现有模块，不重复造新体系；每包只做一个模块；每包必须有测试与审计输出。
- 基线测试: `PYTHONPATH=/root/sikk-gmgn pytest -q` 当前通过 118 个测试。

## 初始审计结论

- `/root/sikk-gmgn` 原本不是 git 仓库，已初始化为 `sikk-paper-audit-20260502` 分支并做基线提交。
- 已有钱包结构核心模块: `sikk_wallet_structure_gate.py`、`sikk_candidate_wallet_structure_pipeline.py`、`sikk_wallet_structure_snapshot.py`、`sikk_wallet_trade_adapter.py`。
- 已有 paper/live 模块: `sikk_paper_live_runner.py`、`sikk_live_run.py`、`sikk_live_orchestrator.py`、`sikk_dashboard_builder.py`。
- 明确缺口:
  - 缺 `sikk_system_audit.py` 系统审计层。
  - 缺 `sikk_explainability_engine.py` 专业解释引擎。
  - `wallet_structure_decision.json` 已存在但需要标准合约与字段完整性检查。
  - dashboard 当前偏状态摘要，缺发现→判断→入场→持仓→退出事件级字段。
  - 市值上下文字段如 `paper_entry_market_cap`、`current_market_cap` 命中很少，需要贯穿。

## 工作包 1：wallet_structure_decision.json 标准合约 + 钱包门控接入

- 单模块范围: `sikk_wallet_structure_gate.py`；必要时只补测试 `tests/test_sikk_wallet_structure_gate.py`。
- 输入: 早期钱包分类 JSON/CSV、候选状态、可选 snapshot/delta。
- 输出: 标准 `wallet_structure_decision.json`、`wallet_structure_decision.csv`。
- 必填字段建议:
  - `token_address`, `symbol`, `decision_at`, `wallet_structure_status`, `wallet_structure_score`, `evidence_level`, `action_code`
  - `wallet_gate_result`, `paper_gate_effect`, `risk_level`, `reason_codes`, `降级原因`
  - `discovery_market_cap_usd`, `signal_market_cap_usd`, `wallet_decision_market_cap_usd`, `current_market_cap_usd`
  - `valid_until`, `source_files`, `missing_fields`, `data_quality_status`
- 验收标准:
  - 缺字段不崩溃，输出 `data_quality_status=DEGRADED/MISSING`。
  - `WALLET_SUPPORT` 不绕过 signal/quote/security。
  - 测试覆盖标准 JSON 字段、缺字段降级、paper-only 说明。
- 测试命令: `PYTHONPATH=/root/sikk-gmgn pytest -q tests/test_sikk_wallet_structure_gate.py tests/test_sikk_wallet_trade_adapter.py`
- 报告路径: `audits/wp1_wallet_contract_report.md`

## 工作包 2：sikk_system_audit.py 系统审计层

- 单模块范围: 新增 `sikk_system_audit.py`；新增 `tests/test_sikk_system_audit.py`。
- 输入: live run 根目录、candidate outputs、state machine、wallet decision、paper runner、dashboard 文件。
- 输出: `system_audit.json`、`system_audit.md`。
- 必查项:
  - 当前候选数、各模块成功/失败/跳过数量。
  - 缺失文件与缺失字段。
  - 卡住 token 列表。
  - 钱包结构旁路/降级原因。
  - 状态机冲突。
  - dashboard 缺字段。
  - 复盘不可用字段。
  - 下一步修复建议。
- 验收标准:
  - 对空目录、部分缺失目录、正常 fake outputs 均可运行。
  - 不执行采集、不交易，只读审计。
- 测试命令: `PYTHONPATH=/root/sikk-gmgn pytest -q tests/test_sikk_system_audit.py`
- 报告路径: `audits/wp2_system_audit_report.md`

## 工作包 3：sikk_explainability_engine.py 专业解释引擎

- 单模块范围: 新增 `sikk_explainability_engine.py`；新增 `tests/test_sikk_explainability_engine.py`。
- 输入: token_status.json、wallet_structure_decision.json、dominant lifecycle、quote/security、paper positions、failure attribution、process_trace。
- 输出: `explainability_report.json`、`explainability_report.md`。
- 必答问题:
  - 为什么发现？为什么观察？为什么支持？为什么暂停？为什么阻断？为什么进入 paper？为什么退出？为什么失败？下一步看什么？主要失效条件/替代假设是什么？
- 验收标准:
  - 不重新裁决，只解释已有结果。
  - 缺输入时显示 `证据缺失/待复查`，不编造。
  - 输出中文证据链，保留原始文件引用。
- 测试命令: `PYTHONPATH=/root/sikk-gmgn pytest -q tests/test_sikk_explainability_engine.py`
- 报告路径: `audits/wp3_explainability_report.md`

## 工作包 4：dashboard 事件级字段升级 + paper runner / 状态机接入检查

- 单模块范围: `sikk_dashboard_builder.py`；只在必要时读取但不重构 `sikk_live_run.py` / `sikk_paper_live_runner.py`。
- 输入: `live_state.json`、token_status、paper live outputs、failure attribution。
- 输出: 升级版 `live_dashboard.html`。
- 事件级字段:
  - `discovered_at`, `discovery_market_cap_usd`, `discovery_liquidity_usd`
  - `first_signal_at`, `first_signal_type`, `signal_market_cap_usd`
  - `wallet_decision_at`, `wallet_decision_market_cap_usd`, `wallet_structure_status`
  - `paper_entry_at`, `paper_entry_market_cap_usd`, `paper_entry_price`, `paper_entry_amount_sol/usd`, `paper_token_amount`
  - `current_market_cap_usd`, `current_price`, `unrealized_pnl_sol`, `unrealized_pnl_pct`
  - `exit_monitor_at`, `paper_exit_at`, `exit_reason`, `failure_attribution_type`
- 验收标准:
  - dashboard 不再只显示 token/state/score；能看到发现→判断→入场→持仓→退出。
  - 缺字段显示 `待补`，不空白、不崩溃。
- 测试命令: `PYTHONPATH=/root/sikk-gmgn pytest -q tests/test_sikk_runtime_v02.py tests/test_sikk_live_run.py`
- 报告路径: `audits/wp4_dashboard_event_report.md`
