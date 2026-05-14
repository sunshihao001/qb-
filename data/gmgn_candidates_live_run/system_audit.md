# SIKK 系统审计报告

- 审计时间：2026-05-14T05:36:03Z
- live run 根目录：`/root/sikk-gmgn/data/gmgn_candidates_live_run`
- 安全边界：只读审计；不采集、不交易、不签名、不广播。
- 当前候选数：5

## 模块统计
- candidates：success=0 failed=0 skipped=0
- kline：success=0 failed=0 skipped=0
- signals：success=0 failed=0 skipped=0
- quote_security：success=1 failed=0 skipped=0
- state_machine：success=3 failed=2 skipped=0
- wallet_structure：success=0 failed=0 skipped=0
- paper_runner：success=0 failed=0 skipped=0

## 缺失文件
- `/root/sikk-gmgn/data/gmgn_candidates_live_run/candidate_pool/token_candidates.json`
- `/root/sikk-gmgn/data/gmgn_candidates_live_run/kline/candidate_kline_pipeline_summary.json`
- `/root/sikk-gmgn/data/gmgn_candidates_live_run/signals/candidate_signal_summary.json`
- `/root/sikk-gmgn/data/gmgn_candidates_live_run/wallet_structure/candidate_wallet_structure_summary.json`

## 缺失字段
- 无

## 卡住 token
- TROLLIEN `ECgweD7xkMj4bm8CcM9rusxKjyQGgdosCvVmhGUupump` state=PAPER_READY reason=吸筹窗口 valid + SIKK S3/S4 + 允许纸面交易 + 仓位大于0
- trolls `7CR3CBpivSMzBEet3cvUckjeSLdbCKaxRB1yNNm6pump` state=WATCHING reason=SIKK 信号仍为观察/预备层
- jestin  `D5GpuB8FAWAc6Qex1p3B1vT9DJKvjPNuBzQgX5y3bonk` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据

## 钱包结构旁路/降级
- `Y4vtfnvGSTe2exSm94SXUq3684MGWwWEhXzASkupump` status=未接入 effect=NO_WALLET_INPUT reason=
- `ziffq43QSCC95DUjVc7cULKYttEHyA1pops25gDpump` status=未接入 effect=NO_WALLET_INPUT reason=
- `7CR3CBpivSMzBEet3cvUckjeSLdbCKaxRB1yNNm6pump` status=未接入 effect=NO_WALLET_INPUT reason=
- `D5GpuB8FAWAc6Qex1p3B1vT9DJKvjPNuBzQgX5y3bonk` status=未接入 effect=NO_WALLET_INPUT reason=

## 状态机冲突
- `3pCyU31quPpsVYaC5TxtXpe6sR1KXSLzk5TkZgXGpump` token_in_open_and_closed_positions  
- `7soYuSPe1LaJ9V37W7ZGDB5Xwxi41LUWjRT3AEQGpump` token_in_open_and_closed_positions  
- `ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1` token_in_open_and_closed_positions  

## Dashboard 缺字段
- token_count：5
- chip_control_action：5
- chip_control_state：5
- cluster_holding_pct_delta：5
- counterparty_state：5
- current_market_cap_usd：5
- current_price：5
- discovered_at：5
- discovery_market_cap_usd：5
- dominant_side_intent：5
- dominant_side_lifecycle：5
- exit_monitor_at：5
- exit_reason：5
- failure_attribution_type：5
- first_signal_at：5
- largest_cluster_holding_pct：5
- largest_cluster_holding_pct_delta：5
- okx_cluster_control_retention_score：5
- okx_cluster_distribution_score：5
- okx_cluster_risk_score：5
- okx_cluster_score：5
- okx_cluster_status：5
- paper_entry_at：5
- paper_entry_market_cap_usd：5
- paper_exit_at：5
- top300_total_holding_pct：5
- wallet_decision_at：5

## 复盘不可用字段
- current_market_cap_usd：206
- exit_price：5
- exit_reason：5
- exit_time：5
- failure_reason：48
- failure_type：48
- paper_entry_market_cap_usd：206

## 缺口优先级
- P0｜钱包结构大面积未接入：覆盖率 20.0%，缺失 4/5；修复：先修 wallet_structure 输出与 token join，再刷新 live_state/dashboard。
- P1｜live_state/dashboard 事件级字段缺失：discovered_at=5, discovery_market_cap_usd=5, first_signal_at=5, wallet_decision_at=5, paper_entry_at=5；修复：补齐 discovery/signal/wallet/paper/market_cap/chip_control 字段并同步 site/dashboard_data.json。
- P1｜paper/case file 复盘字段缺失：paper_entry_market_cap_usd=206, current_market_cap_usd=206, failure_type=48, failure_reason=48, exit_time=5；修复：补 Paper Entry Snapshot、退出证据、failure_type/failure_reason、case file 质量等级。
- P2｜状态机与纸面仓位冲突：冲突 3 条；修复：统一 open/closed 索引，开放仓位不得同时处于终态。
- SAFETY｜真实交易默认关闭：只读系统审计；不采集、不交易、不调用 gmgn_swap/gmgn_cooking、不广播、不 yolo。；修复：不新增 swap/签名/broadcast/私钥读取路径。

## 钱包结构覆盖诊断
- 等级：P0_CRITICAL
- 覆盖：1/5（20.0%）
- 缺失：4（80.0%）
- 缺失原因 NO_WALLET_INPUT：4
- 修复步骤：检查 wallet_structure/candidate_wallet_structure_summary.json 是否由 sikk_live_run.py 单入口生成，禁止用空 summary 覆盖旧结果。
- 修复步骤：逐 token 核对 wallet_structure/<token>/wallet_structure_decision.json、early_wallet_raw.csv、wallet_classification.csv、candidate_groups.csv 是否存在。
- 修复步骤：缺数据时显式写 data_quality_status=MISSING/DEGRADED、reason_codes、missing_fields，不允许空白绕过。
- 修复步骤：MISSING 只进入 OBSERVE/FIX_DATA_SOURCE，不放宽纸面入场或真实交易确认。

## 下一步建议
- 补齐 live run 标准输出目录：候选池、K线、信号、状态机、钱包结构、quote/security、paper_live、live_state/dashboard。
- 优先排查卡住 token：确认其 K线/信号/quote/security/wallet 决策是否缺失或被跳过。
- 修复钱包结构旁路/降级：标准化 wallet_structure_decision.json 并保留 reason_codes/data_quality_status。
- 处理状态机冲突：开放纸面仓位不得同时处于 BLOCKED/FAILED/EXITED，关闭与开放仓位索引需去重。
- 升级 dashboard live_state 事件级字段，覆盖发现→判断→入场→持仓→退出，并接入 chip_control / market_cap_context / lifecycle v0.3 与 OKX cluster v0.4 字段。
- 补齐复盘字段：市值、入场/退出时间价格、failure_type/failure_reason。
- 保持 paper-only：审计层不得调用采集、gmgn_swap/gmgn_cooking、交易广播或 yolo。
