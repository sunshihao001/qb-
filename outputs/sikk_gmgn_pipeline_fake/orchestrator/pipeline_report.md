# SIKK-GMGN 一键管道运行报告

- 运行时间：2026-04-30T11:47:46Z
- 模式：paper/readiness
- 执行边界：只做候选发现、K线吸筹识别、纸面信号与状态机，不执行真实 swap。

## 阶段统计

- 新币筛选：{"总扫描数": 1, "进入候选池": 1, "排除数量": 0, "S3数量": 1, "S2数量": 0, "S1数量": 0, "S0数量": 0}
- K线吸筹管道：{"读取候选数": 1, "处理候选数": 1, "成功数量": 1, "失败数量": 0}
- 信号管道：{"读取候选数": 1, "成功数量": 1, "跳过数量": 0, "失败数量": 0}
- 状态机：{"DISCOVERED": 0, "WATCHING": 0, "ACCUMULATING": 0, "READY_TO_BUY": 0, "PAPER_READY": 1, "BLOCKED": 0, "FAILED": 0, "EXITED": 0, "候选数量": 1}

## 输出文件

- 候选池JSON：outputs/sikk_gmgn_pipeline_fake/gmgn_new_token_filter/token_candidates.json
- 候选池CSV：outputs/sikk_gmgn_pipeline_fake/gmgn_new_token_filter/token_candidates.csv
- 原始GMGN响应：outputs/sikk_gmgn_pipeline_fake/gmgn_new_token_filter/gmgn_trenches_raw.json
- K线管道汇总：outputs/sikk_gmgn_pipeline_fake/kline_pipeline/candidate_kline_pipeline_summary.json
- 信号汇总JSON：outputs/sikk_gmgn_pipeline_fake/candidate_signal_outputs/candidate_signal_summary.json
- 信号汇总CSV：outputs/sikk_gmgn_pipeline_fake/candidate_signal_outputs/candidate_signal_summary.csv
- 状态机JSON：outputs/sikk_gmgn_pipeline_fake/state_machine/candidate_states.json
- 状态机CSV：outputs/sikk_gmgn_pipeline_fake/state_machine/candidate_states.csv
- 状态事件JSONL：outputs/sikk_gmgn_pipeline_fake/state_machine/state_events.jsonl
- 状态报告MD：outputs/sikk_gmgn_pipeline_fake/state_machine/state_summary.md
- 运行报告MD：outputs/sikk_gmgn_pipeline_fake/orchestrator/pipeline_report.md
- 运行ManifestJSON：outputs/sikk_gmgn_pipeline_fake/orchestrator/pipeline_manifest.json

## 下一步

- 若状态机出现 PAPER_READY，可进入报价 + 安全扫描 + 确认层。
- 若状态为 ACCUMULATING，继续刷新 K线与吸筹窗口。
- 若 BLOCKED / FAILED，进入风险复查或数据修复。
