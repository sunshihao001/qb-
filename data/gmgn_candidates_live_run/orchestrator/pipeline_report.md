# SIKK-GMGN 一键管道运行报告

- 运行时间：2026-05-04T12:40:24Z
- 模式：paper/readiness
- 执行边界：只做候选发现、K线吸筹识别、纸面信号、状态机，可选进入报价 + 安全扫描 + 确认层；不执行真实 swap。

## 阶段统计

- 新币筛选：{"总扫描数": 5, "进入候选池": 5, "排除数量": 0, "S3数量": 4, "S2数量": 0, "S1数量": 1, "S0数量": 0}
- K线吸筹管道：{"读取候选数": 4, "处理候选数": 4, "成功数量": 4, "失败数量": 0}
- 信号管道：{"读取候选数": 4, "成功数量": 4, "跳过数量": 0, "失败数量": 0}
- 状态机：{"DISCOVERED": 0, "WATCHING": 2, "ACCUMULATING": 0, "READY_TO_BUY": 0, "PAPER_READY": 1, "BLOCKED": 2, "FAILED": 0, "EXITED": 0, "候选数量": 5}
- 钱包结构门禁：{"处理数量": 1, "WALLET_BLOCK": 1}
- 报价安全确认层：{"读取状态数": 5, "PAPER_READY数量": 1, "成功数量": 1, "跳过数量": 4, "失败数量": 0, "READY_FOR_CONFIRMATION": 1, "PAUSE": 0, "BLOCK": 0}

## 输出文件

- 候选池JSON：data/gmgn_candidates_live_run/gmgn_new_token_filter/token_candidates.json
- 候选池CSV：data/gmgn_candidates_live_run/gmgn_new_token_filter/token_candidates.csv
- 原始GMGN响应：data/gmgn_candidates_live_run/gmgn_new_token_filter/gmgn_trenches_raw.json
- K线管道汇总：data/gmgn_candidates_live_run/kline_pipeline/candidate_kline_pipeline_summary.json
- 信号汇总JSON：data/gmgn_candidates_live_run/candidate_signal_outputs/candidate_signal_summary.json
- 信号汇总CSV：data/gmgn_candidates_live_run/candidate_signal_outputs/candidate_signal_summary.csv
- 状态机JSON：data/gmgn_candidates_live_run/state_machine/candidate_states.json
- 状态机CSV：data/gmgn_candidates_live_run/state_machine/candidate_states.csv
- 状态事件JSONL：data/gmgn_candidates_live_run/state_machine/state_events.jsonl
- 状态报告MD：data/gmgn_candidates_live_run/state_machine/state_summary.md
- 钱包结构汇总JSON：data/gmgn_candidates_live_run/wallet_structure/candidate_wallet_structure_summary.json
- 钱包结构汇总CSV：data/gmgn_candidates_live_run/wallet_structure/candidate_wallet_structure_summary.csv
- 钱包结构报告MD：data/gmgn_candidates_live_run/wallet_structure/candidate_wallet_structure_summary.md
- 报价安全汇总JSON：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 报价安全汇总CSV：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.csv
- 报价安全报告MD：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.md
- 运行报告MD：data/gmgn_candidates_live_run/orchestrator/pipeline_report.md
- 运行ManifestJSON：data/gmgn_candidates_live_run/orchestrator/pipeline_manifest.json

## 下一步

- 若已启用报价 + 安全扫描 + 确认层，只能得到 READY_FOR_CONFIRMATION / PAUSE / BLOCK，不代表真实执行授权。
- 若状态机出现 PAPER_READY 但未启用确认层，可再运行 `--run-quote-security`。
- 若状态为 ACCUMULATING，继续刷新 K线与吸筹窗口。
- 若 BLOCKED / FAILED，进入风险复查或数据修复。
