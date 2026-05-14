# Package File Passport

- Package: `SIKK-GMGN 保留数据包：截止 2026-04-30 10:22`
- Package ID: `sikk_import_20260505_131832`
- Source archive: `/root/sikk-gmgn/data/gmgn_candidates_live_run/orchestrator/sikk_gmgn_live_run_summary_package.zip`
- Import dir: `imports/staging/sikk_import_20260505_131832`
- File count: `16`

## 分类规则
- `FACT_SOURCE`：事实源或标准事实层，仅限可验证来源。
- `HISTORY_SAMPLE`：历史钱包情报样本，可用于复盘或归档。
- `REVIEW_ONLY`：复盘 / 审计 / 展示用途，不能反向生成事实字段。
- `STATE_OUTPUT`：状态产物，不作为新事实源。
- `DISPLAY_ONLY`：仅展示，不参与事实推导。
- `UNKNOWN`：未知文件，需要人工补查。

## 文件清单
- `orchestrator/pipeline_manifest.json` → **REVIEW_ONLY**：只能作为复盘 / 审计 / 展示参考，不能反向生成事实字段。
- `orchestrator/pipeline_report.md` → **REVIEW_ONLY**：只能作为复盘 / 审计 / 展示参考，不能反向生成事实字段。
- `gmgn_new_token_filter/token_candidates.json` → **HISTORY_SAMPLE**：历史钱包情报样本，可用于复盘、归档、模式参考，不可反推当前实时事实。
- `gmgn_new_token_filter/token_candidates.csv` → **HISTORY_SAMPLE**：历史钱包情报样本，可用于复盘、归档、模式参考，不可反推当前实时事实。
- `kline_pipeline/candidate_kline_pipeline_summary.json` → **FACT_SOURCE**：可作为事实源或事实来源记录，但仍需与实时源分离验证。
- `candidate_signal_outputs/candidate_signal_summary.json` → **REVIEW_ONLY**：只能作为复盘 / 审计 / 展示参考，不能反向生成事实字段。
- `candidate_signal_outputs/candidate_signal_summary.csv` → **REVIEW_ONLY**：只能作为复盘 / 审计 / 展示参考，不能反向生成事实字段。
- `state_machine/candidate_states.json` → **STATE_OUTPUT**：状态产物，不作为新事实源。
- `state_machine/candidate_states.csv` → **STATE_OUTPUT**：状态产物，不作为新事实源。
- `state_machine/state_summary.md` → **STATE_OUTPUT**：状态产物，不作为新事实源。
- `wallet_structure/candidate_wallet_structure_summary.json` → **HISTORY_SAMPLE**：历史钱包情报样本，可用于复盘、归档、模式参考，不可反推当前实时事实。
- `wallet_structure/candidate_wallet_structure_summary.csv` → **HISTORY_SAMPLE**：历史钱包情报样本，可用于复盘、归档、模式参考，不可反推当前实时事实。
- `wallet_structure/candidate_wallet_structure_summary.md` → **HISTORY_SAMPLE**：历史钱包情报样本，可用于复盘、归档、模式参考，不可反推当前实时事实。
- `quote_security/candidate_quote_security_summary.json` → **HISTORY_SAMPLE**：历史钱包情报样本，可用于复盘、归档、模式参考，不可反推当前实时事实。
- `quote_security/candidate_quote_security_summary.csv` → **HISTORY_SAMPLE**：历史钱包情报样本，可用于复盘、归档、模式参考，不可反推当前实时事实。
- `quote_security/candidate_quote_security_summary.md` → **HISTORY_SAMPLE**：历史钱包情报样本，可用于复盘、归档、模式参考，不可反推当前实时事实。

## 必须写入规则
- state_machine/candidate_states.json 不作为新事实源
- dashboard/paper/report 不反向生成事实字段
- wallet_structure summary 可作为历史钱包情报样本
- token_candidates 可作为历史候选样本
- quote_security summary 只能作为历史参考
- pipeline_manifest 可作为审计来源
- pipeline_report 可作为复盘来源
- 不得伪造 discovered_at
- 不得伪造 wallet_snapshot_time

## 安全边界
- 不写状态机
- 不覆盖实时事实源
- 不伪造 discovered_at
- 不伪造 wallet_snapshot_time
- 不修改 paper runner
- 不修改 state machine
- 不把展示/复盘文件当成事实源
