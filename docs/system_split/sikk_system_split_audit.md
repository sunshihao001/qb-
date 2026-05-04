# SIKK 系统拆分阶段 0：边界审计报告

## 0. 审计边界

本次只做归属审计与拆分方案：不移动文件、不删除文件、不修改状态机、不修改 paper runner、不修改钱包结构评分、不修改实盘逻辑、不改 Telegram Bot 配置、不读取私钥、不签名、不广播、不真实 swap。

## 一、当前目录结构概览

- `ai_context/`
- `audits/`
- `config/`
- `data/`
- `docs/`
- `knowledge/`
- `logs/`
- `outputs/`
- `reports/`
- `research_loop/`
- `scripts/`
- `tasks/`
- `tests/`
- `.hermes_long_task_prompt_20260503_chatgpt_share_sikk.txt`
- `AGENTS.md`
- `SIKK_AUDIT_REPORT.md`
- `SIKK_CHANGELOG.md`
- `SIKK_LESSONS_LEARNED.md`
- `SIKK_NEXT_TASK.md`
- `SIKK_PROJECT_STATE.md`
- `SIKK_SYSTEM_INDEX.md`
- `SIKK_TASK_PLAN.md`
- `SIKK_VERIFY_REPORT.md`
- `SIKK_交易系统固定命令.md`
- `run_sikk_gmgn_pipeline.py`
- `sikk_accumulation_window_detector.py`
- `sikk_auto_exit_planner.py`
- `sikk_auto_position_sizer.py`
- `sikk_auto_readiness_runner.py`
- `sikk_auto_risk_gate.py`
- `sikk_auto_signal_engine.py`
- `sikk_auto_trade_types.py`
- `sikk_automation_workflow.py`
- `sikk_candidate_kline_pipeline.py`
- `sikk_candidate_quote_security_pipeline.py`
- `sikk_candidate_signal_pipeline.py`
- `sikk_candidate_state_machine.py`
- `sikk_candidate_wallet_structure_pipeline.py`
- `sikk_case_field_source_map.py`
- `sikk_chip_control_state_machine.py`
- `sikk_control_chip_window_detector.py`
- `sikk_dashboard_builder.py`
- `sikk_dashboard_site_builder.py`
- `sikk_document_ingestor.py`
- `sikk_document_passport_builder.py`
- `sikk_dominant_lifecycle_classifier.py`
- `sikk_execution_adapter_base.py`
- `sikk_execution_state_machine.py`
- `sikk_explainability_engine.py`
- `sikk_full_auto_orchestrator.py`
- `sikk_gap_detector.py`
- `sikk_gmgn_new_token_filter.py`
- `sikk_gmgn_quote_adapter.py`
- `sikk_gmgn_token_report.py`
- `sikk_her_task_router.py`
- `sikk_knowledge_absorption.py`
- `sikk_live_orchestrator.py`
- `sikk_live_quote_security_collector.py`
- `sikk_live_run.py`
- `sikk_loop_review_ingestor.py`
- `sikk_loop_state_manager.py`
- `sikk_market_cap_context.py`
- `sikk_method_lens_router.py`
- `sikk_module_runner.py`
- `sikk_notifier.py`
- `sikk_okx_cluster_delta.py`
- `sikk_okx_cluster_holding_analyzer.py`
- `sikk_okx_quote_adapter.py`
- `sikk_operator_psychology_engine.py`
- `sikk_paper_explanation_builder.py`
- `sikk_paper_live_runner.py`
- `sikk_paper_trading_engine.py`
- `sikk_pre_trade_security_checker.py`
- `sikk_query.py`
- `sikk_quote_security_review.py`
- `sikk_real_trade_guard.py`
- `sikk_repomix_context_planner.py`
- `sikk_research_loop_controller.py`
- `sikk_same_source_grouping.py`
- `sikk_system_audit.py`
- `sikk_system_mapper.py`
- `sikk_task_package_builder.py`
- `sikk_telegram_bot_handler.py`
- `sikk_telegram_gateway_adapter.py`
- `sikk_telegram_open.py`
- `sikk_telegram_views.py`
- `sikk_telegram_zh.py`
- `sikk_time_context_gate.py`
- `sikk_token_skip_policy.py`
- `sikk_topic_map_builder.py`
- `sikk_trace_logger.py`
- `sikk_trade_confirmation_ticket.py`
- `sikk_trade_journal.py`
- `sikk_transaction_broadcast_guard.py`
- `sikk_unified_view_builder.py`
- `sikk_wallet_structure_daily_report.py`
- `sikk_wallet_structure_gate.py`
- `sikk_wallet_structure_snapshot.py`
- `sikk_wallet_trade_adapter.py`
- `sikkctl.py`
- `strategy_sikk_b_control_box_retest.md`
- `单轮检查交易系统.sh`
- `启动SIKK专业会话.sh`
- `启动交易系统.sh`
- `查看交易系统状态.sh`
- `查看交易系统进程.sh`
- `查看交易证据面板.sh`
- `查询代币明细.sh`

## 二、文件归属分类

本次纳入 inventory 的主要文件/目录共 `219` 项。分类统计：`{'UNKNOWN': 18, 'OPS_PANEL': 101, 'WALLET_INTEL': 24, 'TRADE_ENGINE': 64, 'SHARED_CONTRACT': 7, 'DEPRECATED_CANDIDATE': 5}`。完整机器可读清单见 `data/gmgn_candidates_live_run/system_split/module_ownership_inventory.json`。

### `.hermes_long_task_prompt_20260503_chatgpt_share_sikk.txt`
- 归属标签：`UNKNOWN`
- 当前作用：暂未确认用途。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：保留原位，下一轮人工复核后再定归属。
- 风险等级：`HIGH`

### `AGENTS.md`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `SIKK_AUDIT_REPORT.md`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `SIKK_CHANGELOG.md`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `SIKK_LESSONS_LEARNED.md`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`MEDIUM`

### `SIKK_NEXT_TASK.md`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `SIKK_PROJECT_STATE.md`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `SIKK_SYSTEM_INDEX.md`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `SIKK_TASK_PLAN.md`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`MEDIUM`

### `SIKK_VERIFY_REPORT.md`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `SIKK_交易系统固定命令.md`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `audits`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`LOW`

### `audits/chatgpt_share_69f6a19a_okx_cluster_summary.md`
- 归属标签：`WALLET_INTEL`
- 当前作用：钱包采集/画像/同源/集群/资金路径/结构评分/GMGN note 或 wallet_structure_decision 相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险
- 迁移建议：未来迁入 /root/sikk/wallet-intel；只生产钱包事实、画像与 shared/decisions/wallet_structure/wallet_structure_decision.json。
- 风险等级：`HIGH`

### `audits/initial_codebase_audit.md`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `audits/module_inventory.json`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `audits/module_inventory.md`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `audits/phase_1_3_time_context_acceptance.md`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；候选文件多写入/多解释风险；消费层时间字段反推风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `audits/phase_1_3c_upstream_time_anchor_report.md`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：消费层时间字段反推风险
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `audits/v03_initial_audit.json`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；消费层时间字段反推风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `audits/v03_initial_audit.md`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `audits/v03_work_packages.md`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `audits/v03_wp1_chip_control_state_machine_report.md`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `audits/v03_wp2_market_cap_context_report.md`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`MEDIUM`

### `audits/v03_wp3_lifecycle_closed_loop_report.md`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`MEDIUM`

### `audits/v03_wp4_audit_explain_dashboard_report.md`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `audits/v04_initial_audit.json`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；消费层时间字段反推风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `audits/v04_initial_audit.md`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；消费层时间字段反推风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `audits/v04_work_packages.md`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `audits/v04_wp1_okx_cluster_report.md`
- 归属标签：`WALLET_INTEL`
- 当前作用：钱包采集/画像/同源/集群/资金路径/结构评分/GMGN note 或 wallet_structure_decision 相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/wallet-intel；只生产钱包事实、画像与 shared/decisions/wallet_structure/wallet_structure_decision.json。
- 风险等级：`HIGH`

### `audits/v04_wp2_chip_state_cluster_report.md`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`MEDIUM`

### `audits/v04_wp3_governance_cluster_report.md`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`MEDIUM`

### `audits/v04_wp4_cluster_delta_failure_attribution_report.md`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `audits/work_packages.md`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：消费层时间字段反推风险
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `audits/wp1_wallet_contract_report.md`
- 归属标签：`WALLET_INTEL`
- 当前作用：钱包采集/画像/同源/集群/资金路径/结构评分/GMGN note 或 wallet_structure_decision 相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/wallet-intel；只生产钱包事实、画像与 shared/decisions/wallet_structure/wallet_structure_decision.json。
- 风险等级：`HIGH`

### `audits/wp2_system_audit_report.md`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；候选文件多写入/多解释风险；消费层时间字段反推风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `audits/wp3_explainability_report.md`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `audits/wp4_dashboard_event_report.md`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；消费层时间字段反推风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `config`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`LOW`

### `config/token_filter_config.json`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `data/gmgn_candidates_live_run`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`LOW`

### `data/gmgn_candidates_live_run/events`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`LOW`

### `data/gmgn_candidates_live_run/explainability_report.json`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`LOW`

### `data/gmgn_candidates_live_run/explainability_report.md`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`LOW`

### `data/gmgn_candidates_live_run/index`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`LOW`

### `data/gmgn_candidates_live_run/live_board.md`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `data/gmgn_candidates_live_run/live_dashboard.html`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `data/gmgn_candidates_live_run/live_run_manifest.json`
- 归属标签：`SHARED_CONTRACT`
- 当前作用：共享 schema、标准快照、registry、manifest、跨系统审计清单或标准交接产物。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：候选文件多写入/多解释风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/shared；保留 normalized/decisions/registry/schemas/archive 标准交接。
- 风险等级：`HIGH`

### `data/gmgn_candidates_live_run/live_state.json`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `data/gmgn_candidates_live_run/paper_live`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`MEDIUM`

### `data/gmgn_candidates_live_run/reports`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`LOW`

### `data/gmgn_candidates_live_run/site`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`LOW`

### `data/gmgn_candidates_live_run/system_audit.json`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；候选文件多写入/多解释风险；消费层时间字段反推风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `data/gmgn_candidates_live_run/system_audit.md`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；候选文件多写入/多解释风险；消费层时间字段反推风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `data/gmgn_candidates_live_run/system_split`
- 归属标签：`SHARED_CONTRACT`
- 当前作用：共享 schema、标准快照、registry、manifest、跨系统审计清单或标准交接产物。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/shared；保留 normalized/decisions/registry/schemas/archive 标准交接。
- 风险等级：`LOW`

### `data/gmgn_candidates_live_run/time_context`
- 归属标签：`SHARED_CONTRACT`
- 当前作用：共享 schema、标准快照、registry、manifest、跨系统审计清单或标准交接产物。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/shared；保留 normalized/decisions/registry/schemas/archive 标准交接。
- 风险等级：`LOW`

### `data/gmgn_candidates_live_run/tokens`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`LOW`

### `docs`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`LOW`

### `docs/SIKK_CASE_FIELD_SOURCE_MAP.md`
- 归属标签：`DEPRECATED_CANDIDATE`
- 当前作用：旧兼容/反推字段/混合事实来源候选，后续应隔离或替换。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；候选文件多写入/多解释风险；消费层时间字段反推风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：暂不删除不移动；阶段 1 后加审计隔离，替换反推事实或旧桥接逻辑。
- 风险等级：`HIGH`

### `docs/hindsight_sikk_integration_plan.md`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `docs/imported`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`LOW`

### `docs/plans`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`LOW`

### `docs/sikk_time_context_schema.md`
- 归属标签：`SHARED_CONTRACT`
- 当前作用：共享 schema、标准快照、registry、manifest、跨系统审计清单或标准交接产物。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：消费层时间字段反推风险
- 迁移建议：未来迁入 /root/sikk/shared；保留 normalized/decisions/registry/schemas/archive 标准交接。
- 风险等级：`MEDIUM`

### `docs/sikk_wallet_normalized_contract.md`
- 归属标签：`SHARED_CONTRACT`
- 当前作用：共享 schema、标准快照、registry、manifest、跨系统审计清单或标准交接产物。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；消费层时间字段反推风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/shared；保留 normalized/decisions/registry/schemas/archive 标准交接。
- 风险等级：`HIGH`

### `docs/sikk_wallet_structure_integration_v2.md`
- 归属标签：`SHARED_CONTRACT`
- 当前作用：共享 schema、标准快照、registry、manifest、跨系统审计清单或标准交接产物。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；消费层时间字段反推风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/shared；保留 normalized/decisions/registry/schemas/archive 标准交接。
- 风险等级：`HIGH`

### `docs/system_split`
- 归属标签：`SHARED_CONTRACT`
- 当前作用：共享 schema、标准快照、registry、manifest、跨系统审计清单或标准交接产物。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/shared；保留 normalized/decisions/registry/schemas/archive 标准交接。
- 风险等级：`LOW`

### `run_sikk_gmgn_pipeline.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：旧一键管道：串联候选发现、K线、信号、状态机、钱包结构与 quote/security，当前是混合编排层。
- 是否被 runtime 调用：DIRECT_ENTRY
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；同一编排层串联 wallet_structure 与 state_machine；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `scripts`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`LOW`

### `scripts/__pycache__`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`LOW`

### `scripts/configure_hindsight_llm_key.sh`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`LOW`

### `scripts/hindsight_recall_sikk.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`LOW`

### `scripts/hindsight_reflect_sikk.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `scripts/hindsight_retain_sikk.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `scripts/hindsight_smoke_sikk.sh`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`MEDIUM`

### `scripts/start_hindsight_docker.sh`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`LOW`

### `sikk_accumulation_window_detector.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`LOW`

### `sikk_auto_exit_planner.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `sikk_auto_position_sizer.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`LOW`

### `sikk_auto_readiness_runner.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`LOW`

### `sikk_auto_risk_gate.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`LOW`

### `sikk_auto_signal_engine.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`LOW`

### `sikk_auto_trade_types.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `sikk_automation_workflow.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；候选文件多写入/多解释风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `sikk_candidate_kline_pipeline.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：候选文件多写入/多解释风险
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `sikk_candidate_quote_security_pipeline.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `sikk_candidate_signal_pipeline.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `sikk_candidate_state_machine.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选状态机；当前可读取钱包结构 summary 并 apply_wallet_gate，属于污染重点。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；候选文件多写入/多解释风险；状态机直接 apply_wallet_gate 消费 wallet_structure_summary；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `sikk_candidate_wallet_structure_pipeline.py`
- 归属标签：`WALLET_INTEL`
- 当前作用：候选状态到钱包结构门禁的旧 pipeline，当前更像 trade→wallet 的桥。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/wallet-intel；只生产钱包事实、画像与 shared/decisions/wallet_structure/wallet_structure_decision.json。
- 风险等级：`HIGH`

### `sikk_case_field_source_map.py`
- 归属标签：`DEPRECATED_CANDIDATE`
- 当前作用：旧兼容/反推字段/混合事实来源候选，后续应隔离或替换。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：case file 字段来源映射，易让 report/case 变成事实来源；provider 原始/混合数据进入状态机风险；候选文件多写入/多解释风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：暂不删除不移动；阶段 1 后加审计隔离，替换反推事实或旧桥接逻辑。
- 风险等级：`HIGH`

### `sikk_chip_control_state_machine.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `sikk_control_chip_window_detector.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`LOW`

### `sikk_dashboard_builder.py`
- 归属标签：`OPS_PANEL`
- 当前作用：dashboard_data 构建器。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：消费层时间字段反推风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `sikk_dashboard_site_builder.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：候选文件多写入/多解释风险；消费层时间字段反推风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `sikk_document_ingestor.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`LOW`

### `sikk_document_passport_builder.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `sikk_dominant_lifecycle_classifier.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `sikk_execution_adapter_base.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `sikk_execution_state_machine.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `sikk_explainability_engine.py`
- 归属标签：`UNKNOWN`
- 当前作用：暂未确认用途。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：消费层时间字段反推风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：保留原位，下一轮人工复核后再定归属。
- 风险等级：`HIGH`

### `sikk_full_auto_orchestrator.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：DIRECT_ENTRY
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；候选文件多写入/多解释风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `sikk_gap_detector.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `sikk_gmgn_new_token_filter.py`
- 归属标签：`UNKNOWN`
- 当前作用：暂未确认用途。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：候选文件多写入/多解释风险
- 迁移建议：保留原位，下一轮人工复核后再定归属。
- 风险等级：`HIGH`

### `sikk_gmgn_quote_adapter.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `sikk_gmgn_token_report.py`
- 归属标签：`WALLET_INTEL`
- 当前作用：钱包采集/画像/同源/集群/资金路径/结构评分/GMGN note 或 wallet_structure_decision 相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/wallet-intel；只生产钱包事实、画像与 shared/decisions/wallet_structure/wallet_structure_decision.json。
- 风险等级：`LOW`

### `sikk_her_task_router.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `sikk_knowledge_absorption.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `sikk_live_orchestrator.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：候选文件多写入/多解释风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `sikk_live_quote_security_collector.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `sikk_live_run.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：canonical runtime 主入口：候选、状态、paper、dashboard、审计产物的单入口编排。
- 是否被 runtime 调用：DIRECT_ENTRY
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；候选文件多写入/多解释风险；消费层时间字段反推风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `sikk_loop_review_ingestor.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`LOW`

### `sikk_loop_state_manager.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`LOW`

### `sikk_market_cap_context.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`LOW`

### `sikk_method_lens_router.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`LOW`

### `sikk_module_runner.py`
- 归属标签：`UNKNOWN`
- 当前作用：暂未确认用途。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：保留原位，下一轮人工复核后再定归属。
- 风险等级：`HIGH`

### `sikk_notifier.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`MEDIUM`

### `sikk_okx_cluster_delta.py`
- 归属标签：`WALLET_INTEL`
- 当前作用：钱包采集/画像/同源/集群/资金路径/结构评分/GMGN note 或 wallet_structure_decision 相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/wallet-intel；只生产钱包事实、画像与 shared/decisions/wallet_structure/wallet_structure_decision.json。
- 风险等级：`MEDIUM`

### `sikk_okx_cluster_holding_analyzer.py`
- 归属标签：`WALLET_INTEL`
- 当前作用：钱包采集/画像/同源/集群/资金路径/结构评分/GMGN note 或 wallet_structure_decision 相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/wallet-intel；只生产钱包事实、画像与 shared/decisions/wallet_structure/wallet_structure_decision.json。
- 风险等级：`LOW`

### `sikk_okx_quote_adapter.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `sikk_operator_psychology_engine.py`
- 归属标签：`UNKNOWN`
- 当前作用：暂未确认用途。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：保留原位，下一轮人工复核后再定归属。
- 风险等级：`HIGH`

### `sikk_paper_explanation_builder.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：消费层时间字段反推风险
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `sikk_paper_live_runner.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：paper 持仓运行器。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：消费层时间字段反推风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `sikk_paper_trading_engine.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `sikk_pre_trade_security_checker.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`LOW`

### `sikk_query.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `sikk_quote_security_review.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：消费层时间字段反推风险
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `sikk_real_trade_guard.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `sikk_repomix_context_planner.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `sikk_research_loop_controller.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `sikk_same_source_grouping.py`
- 归属标签：`WALLET_INTEL`
- 当前作用：钱包采集/画像/同源/集群/资金路径/结构评分/GMGN note 或 wallet_structure_decision 相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/wallet-intel；只生产钱包事实、画像与 shared/decisions/wallet_structure/wallet_structure_decision.json。
- 风险等级：`LOW`

### `sikk_system_audit.py`
- 归属标签：`UNKNOWN`
- 当前作用：暂未确认用途。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；候选文件多写入/多解释风险；消费层时间字段反推风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：保留原位，下一轮人工复核后再定归属。
- 风险等级：`HIGH`

### `sikk_system_mapper.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `sikk_task_package_builder.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `sikk_telegram_bot_handler.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：DIRECT_ENTRY
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`LOW`

### `sikk_telegram_gateway_adapter.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`LOW`

### `sikk_telegram_open.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `sikk_telegram_views.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `sikk_telegram_zh.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `sikk_time_context_gate.py`
- 归属标签：`DEPRECATED_CANDIDATE`
- 当前作用：时间上下文门禁；当前会扫描 dashboard/paper/report/case 等消费层产物，属于反推风险候选。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；候选文件多写入/多解释风险；扫描 dashboard/paper/report/case file 的时间字段，存在消费层反推事实风险；消费层时间字段反推风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：暂不删除不移动；阶段 1 后加审计隔离，替换反推事实或旧桥接逻辑。
- 风险等级：`HIGH`

### `sikk_token_skip_policy.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`MEDIUM`

### `sikk_topic_map_builder.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`LOW`

### `sikk_trace_logger.py`
- 归属标签：`UNKNOWN`
- 当前作用：暂未确认用途。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：保留原位，下一轮人工复核后再定归属。
- 风险等级：`LOW`

### `sikk_trade_confirmation_ticket.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `sikk_trade_journal.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `sikk_transaction_broadcast_guard.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `sikk_unified_view_builder.py`
- 归属标签：`UNKNOWN`
- 当前作用：暂未确认用途。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：保留原位，下一轮人工复核后再定归属。
- 风险等级：`HIGH`

### `sikk_wallet_structure_daily_report.py`
- 归属标签：`WALLET_INTEL`
- 当前作用：钱包采集/画像/同源/集群/资金路径/结构评分/GMGN note 或 wallet_structure_decision 相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/wallet-intel；只生产钱包事实、画像与 shared/decisions/wallet_structure/wallet_structure_decision.json。
- 风险等级：`HIGH`

### `sikk_wallet_structure_gate.py`
- 归属标签：`WALLET_INTEL`
- 当前作用：钱包结构评分与 wallet_structure_decision 生成核心。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/wallet-intel；只生产钱包事实、画像与 shared/decisions/wallet_structure/wallet_structure_decision.json。
- 风险等级：`HIGH`

### `sikk_wallet_structure_snapshot.py`
- 归属标签：`WALLET_INTEL`
- 当前作用：钱包采集/画像/同源/集群/资金路径/结构评分/GMGN note 或 wallet_structure_decision 相关。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/wallet-intel；只生产钱包事实、画像与 shared/decisions/wallet_structure/wallet_structure_decision.json。
- 风险等级：`HIGH`

### `sikk_wallet_trade_adapter.py`
- 归属标签：`WALLET_INTEL`
- 当前作用：钱包门禁到交易状态的 adapter；当前是边界污染/未来 final_trade_gate 替代重点。
- 是否被 runtime 调用：YES_STATIC_IMPORT_OR_RUNTIME_OUTPUT
- 是否可能跨系统污染：wallet gate 到交易状态 adapter，未来应由 final_trade_gate 替代；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/wallet-intel；只生产钱包事实、画像与 shared/decisions/wallet_structure/wallet_structure_decision.json。
- 风险等级：`HIGH`

### `sikkctl.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：DIRECT_ENTRY
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`MEDIUM`

### `strategy_sikk_b_control_box_retest.md`
- 归属标签：`UNKNOWN`
- 当前作用：暂未确认用途。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：保留原位，下一轮人工复核后再定归属。
- 风险等级：`LOW`

### `tests`
- 归属标签：`UNKNOWN`
- 当前作用：暂未确认用途。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：保留原位，下一轮人工复核后再定归属。
- 风险等级：`LOW`

### `tests/__pycache__`
- 归属标签：`UNKNOWN`
- 当前作用：暂未确认用途。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：保留原位，下一轮人工复核后再定归属。
- 风险等级：`LOW`

### `tests/test_run_sikk_gmgn_pipeline.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：同一编排层串联 wallet_structure 与 state_machine
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `tests/test_sikk_auto_framework.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `tests/test_sikk_automation_workflow.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `tests/test_sikk_candidate_kline_pipeline.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：候选文件多写入/多解释风险
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `tests/test_sikk_candidate_quote_security_pipeline.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `tests/test_sikk_candidate_signal_pipeline.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `tests/test_sikk_candidate_state_machine.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；候选文件多写入/多解释风险；状态机直接 apply_wallet_gate 消费 wallet_structure_summary
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `tests/test_sikk_candidate_wallet_structure_pipeline.py`
- 归属标签：`WALLET_INTEL`
- 当前作用：钱包采集/画像/同源/集群/资金路径/结构评分/GMGN note 或 wallet_structure_decision 相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/wallet-intel；只生产钱包事实、画像与 shared/decisions/wallet_structure/wallet_structure_decision.json。
- 风险等级：`MEDIUM`

### `tests/test_sikk_case_field_source_map.py`
- 归属标签：`DEPRECATED_CANDIDATE`
- 当前作用：旧兼容/反推字段/混合事实来源候选，后续应隔离或替换。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：case file 字段来源映射，易让 report/case 变成事实来源；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：暂不删除不移动；阶段 1 后加审计隔离，替换反推事实或旧桥接逻辑。
- 风险等级：`HIGH`

### `tests/test_sikk_chip_control_state_machine.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`MEDIUM`

### `tests/test_sikk_dashboard_site_builder.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `tests/test_sikk_document_ingestor.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`LOW`

### `tests/test_sikk_document_passport_builder.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`LOW`

### `tests/test_sikk_dominant_lifecycle_classifier.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`MEDIUM`

### `tests/test_sikk_execution_adapters.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `tests/test_sikk_execution_state_machine.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `tests/test_sikk_explainability_engine.py`
- 归属标签：`UNKNOWN`
- 当前作用：暂未确认用途。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：保留原位，下一轮人工复核后再定归属。
- 风险等级：`MEDIUM`

### `tests/test_sikk_full_auto_orchestrator.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `tests/test_sikk_gap_detector.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `tests/test_sikk_gmgn_new_token_filter.py`
- 归属标签：`UNKNOWN`
- 当前作用：暂未确认用途。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：保留原位，下一轮人工复核后再定归属。
- 风险等级：`HIGH`

### `tests/test_sikk_her_task_router.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `tests/test_sikk_knowledge_absorption.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `tests/test_sikk_live_collectors.py`
- 归属标签：`UNKNOWN`
- 当前作用：暂未确认用途。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：保留原位，下一轮人工复核后再定归属。
- 风险等级：`HIGH`

### `tests/test_sikk_live_run.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；候选文件多写入/多解释风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `tests/test_sikk_loop_review_ingestor.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`LOW`

### `tests/test_sikk_loop_state_manager.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`LOW`

### `tests/test_sikk_market_cap_context.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`LOW`

### `tests/test_sikk_method_lens_router.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`LOW`

### `tests/test_sikk_okx_cluster_delta.py`
- 归属标签：`WALLET_INTEL`
- 当前作用：钱包采集/画像/同源/集群/资金路径/结构评分/GMGN note 或 wallet_structure_decision 相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/wallet-intel；只生产钱包事实、画像与 shared/decisions/wallet_structure/wallet_structure_decision.json。
- 风险等级：`LOW`

### `tests/test_sikk_okx_cluster_holding_analyzer.py`
- 归属标签：`WALLET_INTEL`
- 当前作用：钱包采集/画像/同源/集群/资金路径/结构评分/GMGN note 或 wallet_structure_decision 相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/wallet-intel；只生产钱包事实、画像与 shared/decisions/wallet_structure/wallet_structure_decision.json。
- 风险等级：`LOW`

### `tests/test_sikk_operator_psychology_engine.py`
- 归属标签：`UNKNOWN`
- 当前作用：暂未确认用途。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：保留原位，下一轮人工复核后再定归属。
- 风险等级：`HIGH`

### `tests/test_sikk_orchestrator_wallet_structure_integration.py`
- 归属标签：`WALLET_INTEL`
- 当前作用：钱包采集/画像/同源/集群/资金路径/结构评分/GMGN note 或 wallet_structure_decision 相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/wallet-intel；只生产钱包事实、画像与 shared/decisions/wallet_structure/wallet_structure_decision.json。
- 风险等级：`MEDIUM`

### `tests/test_sikk_paper_explanation_builder.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：消费层时间字段反推风险
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `tests/test_sikk_paper_live_runner.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；消费层时间字段反推风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `tests/test_sikk_paper_wallet_structure_integration.py`
- 归属标签：`WALLET_INTEL`
- 当前作用：钱包采集/画像/同源/集群/资金路径/结构评分/GMGN note 或 wallet_structure_decision 相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/wallet-intel；只生产钱包事实、画像与 shared/decisions/wallet_structure/wallet_structure_decision.json。
- 风险等级：`MEDIUM`

### `tests/test_sikk_pipeline_wallet_structure_mode.py`
- 归属标签：`WALLET_INTEL`
- 当前作用：钱包采集/画像/同源/集群/资金路径/结构评分/GMGN note 或 wallet_structure_decision 相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/wallet-intel；只生产钱包事实、画像与 shared/decisions/wallet_structure/wallet_structure_decision.json。
- 风险等级：`HIGH`

### `tests/test_sikk_query.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `tests/test_sikk_quote_security_outputs.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：消费层时间字段反推风险
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `tests/test_sikk_repomix_context_planner.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `tests/test_sikk_research_loop_controller.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`LOW`

### `tests/test_sikk_research_loop_controller_status.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `tests/test_sikk_research_loop_final_reports.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `tests/test_sikk_runtime_v02.py`
- 归属标签：`UNKNOWN`
- 当前作用：暂未确认用途。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：消费层时间字段反推风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：保留原位，下一轮人工复核后再定归属。
- 风险等级：`MEDIUM`

### `tests/test_sikk_same_source_grouping.py`
- 归属标签：`WALLET_INTEL`
- 当前作用：钱包采集/画像/同源/集群/资金路径/结构评分/GMGN note 或 wallet_structure_decision 相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/wallet-intel；只生产钱包事实、画像与 shared/decisions/wallet_structure/wallet_structure_decision.json。
- 风险等级：`LOW`

### `tests/test_sikk_state_wallet_structure_integration.py`
- 归属标签：`WALLET_INTEL`
- 当前作用：钱包采集/画像/同源/集群/资金路径/结构评分/GMGN note 或 wallet_structure_decision 相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/wallet-intel；只生产钱包事实、画像与 shared/decisions/wallet_structure/wallet_structure_decision.json。
- 风险等级：`HIGH`

### `tests/test_sikk_system_audit.py`
- 归属标签：`UNKNOWN`
- 当前作用：暂未确认用途。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：候选文件多写入/多解释风险；消费层时间字段反推风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：保留原位，下一轮人工复核后再定归属。
- 风险等级：`HIGH`

### `tests/test_sikk_system_mapper.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`MEDIUM`

### `tests/test_sikk_task_package_builder.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `tests/test_sikk_telegram_bot_handler_phase_4_7.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `tests/test_sikk_telegram_entry_gateway.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `tests/test_sikk_telegram_views.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `tests/test_sikk_time_context_gate.py`
- 归属标签：`DEPRECATED_CANDIDATE`
- 当前作用：旧兼容/反推字段/混合事实来源候选，后续应隔离或替换。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：扫描 dashboard/paper/report/case file 的时间字段，存在消费层反推事实风险；消费层时间字段反推风险
- 迁移建议：暂不删除不移动；阶段 1 后加审计隔离，替换反推事实或旧桥接逻辑。
- 风险等级：`HIGH`

### `tests/test_sikk_topic_map_builder.py`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`LOW`

### `tests/test_sikk_trade_confirmation_ticket.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `tests/test_sikk_transaction_broadcast_guard.py`
- 归属标签：`TRADE_ENGINE`
- 当前作用：候选发现、K线、盘型、时间门禁、quote/security、状态机、paper、失败归因或交易安全验证相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/trade-engine；只读取 shared 标准决策，不读钱包原始采集，不从 dashboard/paper/report 取事实。
- 风险等级：`HIGH`

### `tests/test_sikk_unified_view_builder.py`
- 归属标签：`UNKNOWN`
- 当前作用：暂未确认用途。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：保留原位，下一轮人工复核后再定归属。
- 风险等级：`HIGH`

### `tests/test_sikk_wallet_structure_daily_report.py`
- 归属标签：`WALLET_INTEL`
- 当前作用：钱包采集/画像/同源/集群/资金路径/结构评分/GMGN note 或 wallet_structure_decision 相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/wallet-intel；只生产钱包事实、画像与 shared/decisions/wallet_structure/wallet_structure_decision.json。
- 风险等级：`HIGH`

### `tests/test_sikk_wallet_structure_gate.py`
- 归属标签：`WALLET_INTEL`
- 当前作用：钱包采集/画像/同源/集群/资金路径/结构评分/GMGN note 或 wallet_structure_decision 相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/wallet-intel；只生产钱包事实、画像与 shared/decisions/wallet_structure/wallet_structure_decision.json。
- 风险等级：`LOW`

### `tests/test_sikk_wallet_structure_snapshot.py`
- 归属标签：`WALLET_INTEL`
- 当前作用：钱包采集/画像/同源/集群/资金路径/结构评分/GMGN note 或 wallet_structure_decision 相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/wallet-intel；只生产钱包事实、画像与 shared/decisions/wallet_structure/wallet_structure_decision.json。
- 风险等级：`LOW`

### `tests/test_sikk_wallet_trade_adapter.py`
- 归属标签：`WALLET_INTEL`
- 当前作用：钱包采集/画像/同源/集群/资金路径/结构评分/GMGN note 或 wallet_structure_decision 相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：wallet gate 到交易状态 adapter，未来应由 final_trade_gate 替代；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/wallet-intel；只生产钱包事实、画像与 shared/decisions/wallet_structure/wallet_structure_decision.json。
- 风险等级：`HIGH`

### `单轮检查交易系统.sh`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`LOW`

### `启动SIKK专业会话.sh`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `启动交易系统.sh`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`LOW`

### `查看交易系统状态.sh`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`MEDIUM`

### `查看交易系统进程.sh`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：否
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`LOW`

### `查看交易证据面板.sh`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：provider 原始/混合数据进入状态机风险；候选文件多写入/多解释风险；消费层时间字段反推风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

### `查询代币明细.sh`
- 归属标签：`OPS_PANEL`
- 当前作用：Telegram/查询/看板/报告/日志/知识吸收/审计展示/运维命令相关。
- 是否被 runtime 调用：NO_OR_UNKNOWN
- 是否可能跨系统污染：候选文件多写入/多解释风险；钱包结构与状态机/PAPER_READY/BLOCKED 耦合
- 迁移建议：未来迁入 /root/sikk/ops-panel；只读 shared 与各系统 reports/logs，负责展示与命令，不反向写事实。
- 风险等级：`HIGH`

## 三、WALLET_INTEL 文件列表

- `audits/chatgpt_share_69f6a19a_okx_cluster_summary.md`
- `audits/v04_wp1_okx_cluster_report.md`
- `audits/wp1_wallet_contract_report.md`
- `sikk_candidate_wallet_structure_pipeline.py`
- `sikk_gmgn_token_report.py`
- `sikk_okx_cluster_delta.py`
- `sikk_okx_cluster_holding_analyzer.py`
- `sikk_same_source_grouping.py`
- `sikk_wallet_structure_daily_report.py`
- `sikk_wallet_structure_gate.py`
- `sikk_wallet_structure_snapshot.py`
- `sikk_wallet_trade_adapter.py`
- `tests/test_sikk_candidate_wallet_structure_pipeline.py`
- `tests/test_sikk_okx_cluster_delta.py`
- `tests/test_sikk_okx_cluster_holding_analyzer.py`
- `tests/test_sikk_orchestrator_wallet_structure_integration.py`
- `tests/test_sikk_paper_wallet_structure_integration.py`
- `tests/test_sikk_pipeline_wallet_structure_mode.py`
- `tests/test_sikk_same_source_grouping.py`
- `tests/test_sikk_state_wallet_structure_integration.py`
- `tests/test_sikk_wallet_structure_daily_report.py`
- `tests/test_sikk_wallet_structure_gate.py`
- `tests/test_sikk_wallet_structure_snapshot.py`
- `tests/test_sikk_wallet_trade_adapter.py`

## 四、TRADE_ENGINE 文件列表

- `audits/phase_1_3_time_context_acceptance.md`
- `audits/v03_wp1_chip_control_state_machine_report.md`
- `audits/v03_wp2_market_cap_context_report.md`
- `config`
- `config/token_filter_config.json`
- `data/gmgn_candidates_live_run`
- `data/gmgn_candidates_live_run/explainability_report.json`
- `data/gmgn_candidates_live_run/explainability_report.md`
- `data/gmgn_candidates_live_run/paper_live`
- `data/gmgn_candidates_live_run/system_audit.json`
- `data/gmgn_candidates_live_run/system_audit.md`
- `data/gmgn_candidates_live_run/tokens`
- `run_sikk_gmgn_pipeline.py`
- `sikk_accumulation_window_detector.py`
- `sikk_auto_exit_planner.py`
- `sikk_auto_position_sizer.py`
- `sikk_auto_readiness_runner.py`
- `sikk_auto_risk_gate.py`
- `sikk_auto_signal_engine.py`
- `sikk_auto_trade_types.py`
- `sikk_candidate_kline_pipeline.py`
- `sikk_candidate_quote_security_pipeline.py`
- `sikk_candidate_signal_pipeline.py`
- `sikk_candidate_state_machine.py`
- `sikk_chip_control_state_machine.py`
- `sikk_control_chip_window_detector.py`
- `sikk_dominant_lifecycle_classifier.py`
- `sikk_execution_adapter_base.py`
- `sikk_execution_state_machine.py`
- `sikk_full_auto_orchestrator.py`
- `sikk_gmgn_quote_adapter.py`
- `sikk_live_orchestrator.py`
- `sikk_live_quote_security_collector.py`
- `sikk_live_run.py`
- `sikk_market_cap_context.py`
- `sikk_okx_quote_adapter.py`
- `sikk_paper_explanation_builder.py`
- `sikk_paper_live_runner.py`
- `sikk_paper_trading_engine.py`
- `sikk_pre_trade_security_checker.py`
- `sikk_quote_security_review.py`
- `sikk_real_trade_guard.py`
- `sikk_token_skip_policy.py`
- `sikk_trade_confirmation_ticket.py`
- `sikk_trade_journal.py`
- `sikk_transaction_broadcast_guard.py`
- `tests/test_run_sikk_gmgn_pipeline.py`
- `tests/test_sikk_auto_framework.py`
- `tests/test_sikk_candidate_kline_pipeline.py`
- `tests/test_sikk_candidate_quote_security_pipeline.py`
- `tests/test_sikk_candidate_signal_pipeline.py`
- `tests/test_sikk_candidate_state_machine.py`
- `tests/test_sikk_chip_control_state_machine.py`
- `tests/test_sikk_dominant_lifecycle_classifier.py`
- `tests/test_sikk_execution_adapters.py`
- `tests/test_sikk_execution_state_machine.py`
- `tests/test_sikk_full_auto_orchestrator.py`
- `tests/test_sikk_live_run.py`
- `tests/test_sikk_market_cap_context.py`
- `tests/test_sikk_paper_explanation_builder.py`
- `tests/test_sikk_paper_live_runner.py`
- `tests/test_sikk_quote_security_outputs.py`
- `tests/test_sikk_trade_confirmation_ticket.py`
- `tests/test_sikk_transaction_broadcast_guard.py`

## 五、OPS_PANEL 文件列表

- `AGENTS.md`
- `SIKK_AUDIT_REPORT.md`
- `SIKK_CHANGELOG.md`
- `SIKK_LESSONS_LEARNED.md`
- `SIKK_NEXT_TASK.md`
- `SIKK_PROJECT_STATE.md`
- `SIKK_SYSTEM_INDEX.md`
- `SIKK_TASK_PLAN.md`
- `SIKK_VERIFY_REPORT.md`
- `SIKK_交易系统固定命令.md`
- `audits`
- `audits/initial_codebase_audit.md`
- `audits/module_inventory.json`
- `audits/module_inventory.md`
- `audits/phase_1_3c_upstream_time_anchor_report.md`
- `audits/v03_initial_audit.json`
- `audits/v03_initial_audit.md`
- `audits/v03_work_packages.md`
- `audits/v03_wp3_lifecycle_closed_loop_report.md`
- `audits/v03_wp4_audit_explain_dashboard_report.md`
- `audits/v04_initial_audit.json`
- `audits/v04_initial_audit.md`
- `audits/v04_work_packages.md`
- `audits/v04_wp2_chip_state_cluster_report.md`
- `audits/v04_wp3_governance_cluster_report.md`
- `audits/v04_wp4_cluster_delta_failure_attribution_report.md`
- `audits/work_packages.md`
- `audits/wp2_system_audit_report.md`
- `audits/wp3_explainability_report.md`
- `audits/wp4_dashboard_event_report.md`
- `data/gmgn_candidates_live_run/events`
- `data/gmgn_candidates_live_run/index`
- `data/gmgn_candidates_live_run/live_board.md`
- `data/gmgn_candidates_live_run/live_dashboard.html`
- `data/gmgn_candidates_live_run/live_state.json`
- `data/gmgn_candidates_live_run/reports`
- `data/gmgn_candidates_live_run/site`
- `docs`
- `docs/hindsight_sikk_integration_plan.md`
- `docs/imported`
- `docs/plans`
- `scripts`
- `scripts/__pycache__`
- `scripts/configure_hindsight_llm_key.sh`
- `scripts/hindsight_recall_sikk.py`
- `scripts/hindsight_reflect_sikk.py`
- `scripts/hindsight_retain_sikk.py`
- `scripts/hindsight_smoke_sikk.sh`
- `scripts/start_hindsight_docker.sh`
- `sikk_automation_workflow.py`
- `sikk_dashboard_builder.py`
- `sikk_dashboard_site_builder.py`
- `sikk_document_ingestor.py`
- `sikk_document_passport_builder.py`
- `sikk_gap_detector.py`
- `sikk_her_task_router.py`
- `sikk_knowledge_absorption.py`
- `sikk_loop_review_ingestor.py`
- `sikk_loop_state_manager.py`
- `sikk_method_lens_router.py`
- `sikk_notifier.py`
- `sikk_query.py`
- `sikk_repomix_context_planner.py`
- `sikk_research_loop_controller.py`
- `sikk_system_mapper.py`
- `sikk_task_package_builder.py`
- `sikk_telegram_bot_handler.py`
- `sikk_telegram_gateway_adapter.py`
- `sikk_telegram_open.py`
- `sikk_telegram_views.py`
- `sikk_telegram_zh.py`
- `sikk_topic_map_builder.py`
- `sikkctl.py`
- `tests/test_sikk_automation_workflow.py`
- `tests/test_sikk_dashboard_site_builder.py`
- `tests/test_sikk_document_ingestor.py`
- `tests/test_sikk_document_passport_builder.py`
- `tests/test_sikk_gap_detector.py`
- `tests/test_sikk_her_task_router.py`
- `tests/test_sikk_knowledge_absorption.py`
- `tests/test_sikk_loop_review_ingestor.py`
- `tests/test_sikk_loop_state_manager.py`
- `tests/test_sikk_method_lens_router.py`
- `tests/test_sikk_query.py`
- `tests/test_sikk_repomix_context_planner.py`
- `tests/test_sikk_research_loop_controller.py`
- `tests/test_sikk_research_loop_controller_status.py`
- `tests/test_sikk_research_loop_final_reports.py`
- `tests/test_sikk_system_mapper.py`
- `tests/test_sikk_task_package_builder.py`
- `tests/test_sikk_telegram_bot_handler_phase_4_7.py`
- `tests/test_sikk_telegram_entry_gateway.py`
- `tests/test_sikk_telegram_views.py`
- `tests/test_sikk_topic_map_builder.py`
- `单轮检查交易系统.sh`
- `启动SIKK专业会话.sh`
- `启动交易系统.sh`
- `查看交易系统状态.sh`
- `查看交易系统进程.sh`
- `查看交易证据面板.sh`
- `查询代币明细.sh`

## 六、SHARED_CONTRACT 文件列表

- `data/gmgn_candidates_live_run/live_run_manifest.json`
- `data/gmgn_candidates_live_run/system_split`
- `data/gmgn_candidates_live_run/time_context`
- `docs/sikk_time_context_schema.md`
- `docs/sikk_wallet_normalized_contract.md`
- `docs/sikk_wallet_structure_integration_v2.md`
- `docs/system_split`

## 七、DEPRECATED_CANDIDATE 文件列表

- `docs/SIKK_CASE_FIELD_SOURCE_MAP.md`
- `sikk_case_field_source_map.py`
- `sikk_time_context_gate.py`
- `tests/test_sikk_case_field_source_map.py`
- `tests/test_sikk_time_context_gate.py`

## 八、UNKNOWN 文件列表

- `.hermes_long_task_prompt_20260503_chatgpt_share_sikk.txt`
- `sikk_explainability_engine.py`
- `sikk_gmgn_new_token_filter.py`
- `sikk_module_runner.py`
- `sikk_operator_psychology_engine.py`
- `sikk_system_audit.py`
- `sikk_trace_logger.py`
- `sikk_unified_view_builder.py`
- `strategy_sikk_b_control_box_retest.md`
- `tests`
- `tests/__pycache__`
- `tests/test_sikk_explainability_engine.py`
- `tests/test_sikk_gmgn_new_token_filter.py`
- `tests/test_sikk_live_collectors.py`
- `tests/test_sikk_operator_psychology_engine.py`
- `tests/test_sikk_runtime_v02.py`
- `tests/test_sikk_system_audit.py`
- `tests/test_sikk_unified_view_builder.py`

## 九、跨系统污染点

### 钱包系统是否直接改状态机
- 结论：存在边界污染：sikk_candidate_state_machine.py 从 sikk_wallet_trade_adapter import apply_wallet_gate/normalize_wallet_decision，并根据 wallet_structure_summary_path 写入钱包门禁字段；run_sikk_gmgn_pipeline.py 在钱包结构生成后重跑状态机。当前默认 observe 较安全，但架构上应改为 final_trade_gate 消费。
- 风险等级：`HIGH`
- 相关文件：`sikk_candidate_state_machine.py`、`sikk_wallet_trade_adapter.py`、`run_sikk_gmgn_pipeline.py`

### 交易系统是否直接读取钱包原始采集文件
- 结论：未发现状态机直接读取 GMGN holder/wallet/trade/cluster 原始文件；但交易 pipeline 读取 wallet_structure_summary 而非唯一标准 wallet_structure_decision，且候选状态直接混入钱包评分字段。
- 风险等级：`MEDIUM`
- 相关文件：`sikk_candidate_state_machine.py`、`sikk_candidate_wallet_structure_pipeline.py`

### dashboard 是否反向提供事实字段
- 结论：dashboard_builder/site 当前主要是展示层；但 time_context_gate 扫描 dashboard_data/site/case_files 等消费层产物时，存在把展示产物纳入时间事实 universe 的风险。
- 风险等级：`HIGH`
- 相关文件：`sikk_time_context_gate.py`、`sikk_dashboard_builder.py`、`data/gmgn_candidates_live_run/site`

### paper 是否反向提供 token_open_time / discovered_at
- 结论：paper_live/case_files 是 paper 复盘产物；time_context_gate 当前会收集 paper/case/report 输入，虽然多数为审计用途，但不应作为 token_open_time/discovered_at/quote_time/wallet_snapshot_time 的事实来源。
- 风险等级：`HIGH`
- 相关文件：`sikk_time_context_gate.py`、`data/gmgn_candidates_live_run/paper_live`

### report / case file 是否被当作事实源
- 结论：存在 sikk_case_field_source_map.py 与 time_context_gate 对 case/report 路径的扫描风险；应标记 DEPRECATED_CANDIDATE，不应反推钱包或 token 事实。
- 风险等级：`HIGH`
- 相关文件：`sikk_case_field_source_map.py`、`sikk_time_context_gate.py`、`data/gmgn_candidates_live_run/site/case_files`

### 多个模块是否各自写 candidates.json
- 结论：候选发现、runtime、orchestrator、state/pipeline 共同读写 token_candidates/candidates 语义文件，建议阶段 1 统一为 shared registry + trade-engine candidate snapshot。
- 风险等级：`MEDIUM`
- 相关文件：`sikk_gmgn_new_token_filter.py`、`run_sikk_gmgn_pipeline.py`、`sikk_live_run.py`、`sikk_time_context_gate.py`

### 多个模块是否各自解释 token/quote/wallet 时间
- 结论：候选发现、quote/security、wallet_structure、time_context_gate、paper/case/report 都存在时间字段；阶段 1.3C 已补上游锚点，但消费层仍需禁止作为事实来源。
- 风险等级：`HIGH`
- 相关文件：`sikk_gmgn_new_token_filter.py`、`sikk_quote_security_review.py`、`sikk_wallet_structure_gate.py`、`sikk_time_context_gate.py`

## 十、建议的新目录结构

只提出建议，不执行移动。

```text
/root/sikk/
  wallet-intel/
    code/
    data/
    logs/
    reports/

  trade-engine/
    code/
    data/
    logs/
    reports/

  ops-panel/
    code/
    data/
    logs/

  shared/
    normalized/
    decisions/
    registry/
    schemas/
    archive/
```

## 十一、共享交接规则

- `wallet-intel` 只能写 `shared/decisions/wallet_structure/`，标准产物是 `wallet_structure_decision.json`。
- `trade-engine` 只能读 `shared/decisions/wallet_structure/`，不得读取 GMGN 原始 wallet/holder/trade/cluster 文件。
- `ops-panel` 只能读 `shared`、各系统 `reports/` 与 `logs/`，不得把 dashboard/paper/report/case file 反向写成事实字段。
- `dashboard` / `paper` / `report` 不能反向提供 `token_open_time`、`discovered_at`、`quote_time`、`wallet_snapshot_time`、钱包事实、资金事实。
- `final_trade_gate` 是交易系统消费 wallet decision 的唯一综合点；状态机只读 final gate。

## 十二、是否建议分多个 Telegram Bot

### 只分一个 Bot 的风险
- 命令、展示、paper 操作、钱包情报查询混在一起，容易把 ops 面板误当事实源。
- 权限边界不清，未来如果接入更多自动化命令，误触发风险上升。

### 分两个 Bot 的方案
- Bot A：`sikk-ops-panel`，负责系统状态、dashboard、日报、审计报告。
- Bot B：`sikk-trade-control`，负责 paper-only 交易验证命令、final gate 查询、状态机只读/纸面命令。
- 钱包情报仍通过 ops 查询或只读命令展示。

### 分三个 Bot 的方案
- Bot A：`sikk-wallet-intel-bot`，只查钱包情报、同源、历史画像、wallet decision。
- Bot B：`sikk-trade-engine-bot`，只查候选、final gate、状态机、paper。
- Bot C：`sikk-ops-panel-bot`，只做 dashboard、日报、日志、审计和系统状态。

### 当前最推荐方案
当前阶段推荐：暂不拆 Bot 配置；先进入阶段 1 建立 shared 合约目录与 schema。等 wallet decision 与 final gate 连接稳定后，优先升级为两个 Bot；三个 Bot 适合系统稳定、权限和命令量明显增加后再拆。

## 十三、下一阶段建议

- 建议进入：**阶段 1：建立 shared 合约目录与 schema**。
- 暂不建议直接移动文件。
- 阶段 2：钱包系统输出迁移到 `shared/decisions/wallet_structure/`。
- 阶段 3：交易系统只读 `wallet_structure_decision.json`，由 `final_trade_gate` 综合后状态机再消费。
- 阶段 4：再拆 Telegram Bot。

### 阶段 1 可做事项
- 建立 `shared/schemas/wallet_structure_decision.schema.json`。
- 建立 `shared/schemas/final_trade_gate.schema.json`。
- 建立 `shared/schemas/time_context.schema.json`。
- 建立 `shared/registry/source_registry.json`。
- 只新增合约与空目录/示例，不改变 runtime 行为。

## 验收结论

- 未修改核心代码。
- 未移动文件。
- 未删除文件。
- 未改变 runtime 行为。
- 未改变 paper runner。
- 未改变状态机。
- 已输出 system split audit 文档。
- 已输出 module ownership inventory JSON。
- 已明确跨系统污染点。
- 下一阶段可以建立 shared 合约，但不应直接移动文件。
