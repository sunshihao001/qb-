# 工作包 2：sikk_system_audit.py 系统审计层报告

- 时间：2026-05-02
- 分支：sikk-paper-audit-20260502
- 项目路径：/root/sikk-gmgn
- 安全边界：paper-only；本工作包新增模块为只读审计层，不采集、不交易、不调用 gmgn_swap/gmgn_cooking、不广播、不 yolo。

## 完成内容

- 新增 `sikk_system_audit.py`。
  - 输入：live run 根目录及其中 candidate outputs、state machine、wallet decision、paper runner、dashboard 文件。
  - 输出：`system_audit.json`、`system_audit.md`。
  - 只读取本地 JSON/JSONL/CSV/HTML 状态文件并写审计结果，不调用采集器、quote 命令或交易相关命令。
- 新增 `tests/test_sikk_system_audit.py`。
  - 覆盖空目录。
  - 覆盖部分缺失目录。
  - 覆盖正常 fake outputs，并断言候选数、模块成功/失败/跳过、卡住 token、钱包结构降级、状态冲突、dashboard 缺字段、复盘不可用字段。
- 对当前 live run 执行审计，生成：
  - `/root/sikk-gmgn/data/gmgn_candidates_live_run/system_audit.json`
  - `/root/sikk-gmgn/data/gmgn_candidates_live_run/system_audit.md`

## 当前 live run 审计摘要

- 当前候选数：50。
- 模块统计：
  - candidates：success=0 failed=0 skipped=0。
  - kline：success=0 failed=0 skipped=0。
  - signals：success=0 failed=0 skipped=0。
  - quote_security：success=4 failed=0 skipped=0。
  - state_machine：success=49 failed=1 skipped=0。
  - wallet_structure：success=4 failed=0 skipped=0。
  - paper_runner：读取候选数=50，新增纸面入场数=2，纸面退出数=2，当前开放仓位数=3，累计关闭仓位数=93。
- 缺失文件：
  - `/root/sikk-gmgn/data/gmgn_candidates_live_run/candidate_pool/token_candidates.json`
  - `/root/sikk-gmgn/data/gmgn_candidates_live_run/kline/candidate_kline_pipeline_summary.json`
  - `/root/sikk-gmgn/data/gmgn_candidates_live_run/signals/candidate_signal_summary.json`
- 缺失字段：wallet_structure 当前 4 条决策缺标准字段，包括 `token_address`、`wallet_gate_result`、`paper_gate_effect`、`reason_codes`、`data_quality_status`。
- 卡住 token：审计输出识别多条 WATCHING/PAPER_READY/ACCUMULATING token，其中 PAPER_READY 示例包括 NYAN、AALIEN、UNITED、MSTRUMP。
- 钱包结构旁路/降级：大量 state row 为 `未接入 / NO_WALLET_INPUT`，提示 wallet decision 未覆盖所有候选。
- 状态机冲突：`ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1` 同时出现在 open/closed paper positions。
- Dashboard 缺字段：50 条 live_state token 均缺事件级字段，如 `discovered_at`、`discovery_market_cap_usd`、`wallet_decision_at`、`paper_entry_at`、`paper_entry_market_cap_usd`、`current_market_cap_usd`、`current_price`、`paper_exit_at`、`failure_attribution_type` 等。
- 复盘不可用字段：主要缺 `paper_entry_market_cap_usd`、`current_market_cap_usd`、部分关闭仓位缺 `exit_time/exit_price/exit_reason`，部分事件缺 `failure_type/failure_reason`。

## 下一步建议

- 补齐 live run 标准输出目录与文件布局，避免候选池/K线/信号摘要只能从下游状态反推。
- 继续沿用 WP1 标准合约，确保 wallet_structure_decision 输出 `reason_codes`、`data_quality_status` 与 gate/effect 字段。
- 优先排查 PAPER_READY 卡住但未稳定入场/复盘的 token，确认 paper runner 与 quote/security 是否存在缺输入或重复仓位问题。
- 处理 open/closed paper positions 重复 token 的状态冲突。
- 后续 WP4 应升级 dashboard 事件级字段，覆盖发现→判断→入场→持仓→退出。
- 补齐复盘字段，尤其市值上下文与 failure attribution 字段。

## 测试结果

- 指定测试：`PYTHONPATH=/root/sikk-gmgn pytest -q tests/test_sikk_system_audit.py`
  - 结果：3 passed。
- 全量测试：`PYTHONPATH=/root/sikk-gmgn pytest -q`
  - 结果：121 passed。

## 触碰真实交易确认

- 未触碰真实交易。
- 未调用 gmgn_swap/gmgn_cooking。
- 未执行交易广播、签名或 yolo。
- 新增审计模块仅读取本地文件并写审计报告。
