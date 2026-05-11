# SIKK 专业解释报告

- 生成时间：2026-05-02T23:37:38Z
- live run：data/gmgn_candidates_live_run
- token 数：131
- 安全边界：paper-only；只解释既有结果，不执行真实交易、不签名、不广播。
- 非裁决说明：不重新裁决；缺输入统一标记为 证据缺失/待复查。

## 状态分布

- ACCUMULATING：2
- BLOCKED：15
- DISCOVERED：3
- PAPER_OPEN：2
- PAPER_READY：6
- UNKNOWN：1
- WATCHING：102

## 缺失输入

- 未发现必需输入整体缺失；逐 token 字段仍可能待复查。

## Token 解释

### GRUMP / 21EZ83KVV3YqhXiAuEwsWsUF8C2EkNVZC3ejV29Hpump

- 当前状态：PAPER_READY
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T13:54:08Z｜来源：data/gmgn_candidates_live_run/tokens/21EZ83KVV3YqhXiAuEwsWsUF8C2EkNVZC3ejV29Hpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：GRUMP｜来源：data/gmgn_candidates_live_run/tokens/21EZ83KVV3YqhXiAuEwsWsUF8C2EkNVZC3ejV29Hpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：PAPER_READY｜来源：data/gmgn_candidates_live_run/tokens/21EZ83KVV3YqhXiAuEwsWsUF8C2EkNVZC3ejV29Hpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：PAPER_READY / 吸筹窗口 valid + SIKK S3/S4 + 允许纸面交易 + 仓位大于0｜来源：data/gmgn_candidates_live_run/tokens/21EZ83KVV3YqhXiAuEwsWsUF8C2EkNVZC3ejV29Hpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/21EZ83KVV3YqhXiAuEwsWsUF8C2EkNVZC3ejV29Hpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 有证据：当前状态：PAPER_READY｜来源：data/gmgn_candidates_live_run/tokens/21EZ83KVV3YqhXiAuEwsWsUF8C2EkNVZC3ejV29Hpump/token_status.json｜字段：current_state
- 有证据：钱包结构结论：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/21EZ83KVV3YqhXiAuEwsWsUF8C2EkNVZC3ejV29Hpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：quote/security 权限：由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission

#### 为什么进入paper
- 有证据：当前状态：PAPER_READY｜来源：data/gmgn_candidates_live_run/tokens/21EZ83KVV3YqhXiAuEwsWsUF8C2EkNVZC3ejV29Hpump/token_status.json｜字段：current_state
- 有证据：最新动作：LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/21EZ83KVV3YqhXiAuEwsWsUF8C2EkNVZC3ejV29Hpump/token_status.json｜字段：latest_action
- 有证据：入场依据：吸筹窗口 valid + SIKK S3/S4 + 允许纸面交易 + 仓位大于0｜来源：data/gmgn_candidates_live_run/tokens/21EZ83KVV3YqhXiAuEwsWsUF8C2EkNVZC3ejV29Hpump/token_status.json｜字段：latest_reason

#### 为什么退出
- 有证据：纸面退出原因：钱包结构触发纸面强制退出｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json｜字段：exit_reason
- 有证据：纸面退出时间：2026-05-02T17:22:43Z｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json｜字段：exit_time
- 有证据：当前状态：PAPER_READY｜来源：data/gmgn_candidates_live_run/tokens/21EZ83KVV3YqhXiAuEwsWsUF8C2EkNVZC3ejV29Hpump/token_status.json｜字段：current_state

#### 为什么失败
- 有证据：失败类型：STRUCTURE_WEAKENING｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl｜字段：failure_type
- 有证据：失败原因：钱包结构状态变为 WALLET_BLOCK，纸面阶段直接模拟退出｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl｜字段：failure_reason
- 有证据：当前状态：PAPER_READY｜来源：data/gmgn_candidates_live_run/tokens/21EZ83KVV3YqhXiAuEwsWsUF8C2EkNVZC3ejV29Hpump/token_status.json｜字段：current_state

#### 下一步看什么
- 待复查：复查最新状态/动作：PAPER_READY / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/21EZ83KVV3YqhXiAuEwsWsUF8C2EkNVZC3ejV29Hpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/21EZ83KVV3YqhXiAuEwsWsUF8C2EkNVZC3ejV29Hpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/21EZ83KVV3YqhXiAuEwsWsUF8C2EkNVZC3ejV29Hpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/21EZ83KVV3YqhXiAuEwsWsUF8C2EkNVZC3ejV29Hpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/21EZ83KVV3YqhXiAuEwsWsUF8C2EkNVZC3ejV29Hpump/process_trace.jsonl

### Walter / 2CKp88BFyPzr7gEuQKXMJ9cqa24AFXUNC41FR7udpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/2CKp88BFyPzr7gEuQKXMJ9cqa24AFXUNC41FR7udpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：Walter｜来源：data/gmgn_candidates_live_run/tokens/2CKp88BFyPzr7gEuQKXMJ9cqa24AFXUNC41FR7udpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/2CKp88BFyPzr7gEuQKXMJ9cqa24AFXUNC41FR7udpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/2CKp88BFyPzr7gEuQKXMJ9cqa24AFXUNC41FR7udpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/2CKp88BFyPzr7gEuQKXMJ9cqa24AFXUNC41FR7udpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/2CKp88BFyPzr7gEuQKXMJ9cqa24AFXUNC41FR7udpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/2CKp88BFyPzr7gEuQKXMJ9cqa24AFXUNC41FR7udpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/2CKp88BFyPzr7gEuQKXMJ9cqa24AFXUNC41FR7udpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/2CKp88BFyPzr7gEuQKXMJ9cqa24AFXUNC41FR7udpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/2CKp88BFyPzr7gEuQKXMJ9cqa24AFXUNC41FR7udpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/2CKp88BFyPzr7gEuQKXMJ9cqa24AFXUNC41FR7udpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/2CKp88BFyPzr7gEuQKXMJ9cqa24AFXUNC41FR7udpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/2CKp88BFyPzr7gEuQKXMJ9cqa24AFXUNC41FR7udpump/process_trace.jsonl

### scriblin / 2D7VoRQCHrGr1ZK93XeGAEmbQ6Y5iSa1nzuUSpuppump

- 当前状态：BLOCKED
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T10:15:28Z｜来源：data/gmgn_candidates_live_run/tokens/2D7VoRQCHrGr1ZK93XeGAEmbQ6Y5iSa1nzuUSpuppump/token_status.json｜字段：last_update
- 有证据：发现对象符号：scriblin｜来源：data/gmgn_candidates_live_run/tokens/2D7VoRQCHrGr1ZK93XeGAEmbQ6Y5iSa1nzuUSpuppump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：BLOCKED｜来源：data/gmgn_candidates_live_run/tokens/2D7VoRQCHrGr1ZK93XeGAEmbQ6Y5iSa1nzuUSpuppump/token_status.json｜字段：current_state
- 有证据：最近流程记录：BLOCKED / 风险门禁阻断或 SIKK 信号 SX｜来源：data/gmgn_candidates_live_run/tokens/2D7VoRQCHrGr1ZK93XeGAEmbQ6Y5iSa1nzuUSpuppump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/2D7VoRQCHrGr1ZK93XeGAEmbQ6Y5iSa1nzuUSpuppump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 有证据：当前状态：BLOCKED｜来源：data/gmgn_candidates_live_run/tokens/2D7VoRQCHrGr1ZK93XeGAEmbQ6Y5iSa1nzuUSpuppump/token_status.json｜字段：current_state
- 有证据：钱包结构结论：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/2D7VoRQCHrGr1ZK93XeGAEmbQ6Y5iSa1nzuUSpuppump/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：quote/security 权限：由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/2D7VoRQCHrGr1ZK93XeGAEmbQ6Y5iSa1nzuUSpuppump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：BLOCKED / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/2D7VoRQCHrGr1ZK93XeGAEmbQ6Y5iSa1nzuUSpuppump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/2D7VoRQCHrGr1ZK93XeGAEmbQ6Y5iSa1nzuUSpuppump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/2D7VoRQCHrGr1ZK93XeGAEmbQ6Y5iSa1nzuUSpuppump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/2D7VoRQCHrGr1ZK93XeGAEmbQ6Y5iSa1nzuUSpuppump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/2D7VoRQCHrGr1ZK93XeGAEmbQ6Y5iSa1nzuUSpuppump/process_trace.jsonl

### Dragon / 2p5e3sudKx2LtM8iSefaSszMY9nCiHz6CTEASQ9Xpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T20:43:45Z｜来源：data/gmgn_candidates_live_run/tokens/2p5e3sudKx2LtM8iSefaSszMY9nCiHz6CTEASQ9Xpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：Dragon｜来源：data/gmgn_candidates_live_run/tokens/2p5e3sudKx2LtM8iSefaSszMY9nCiHz6CTEASQ9Xpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/2p5e3sudKx2LtM8iSefaSszMY9nCiHz6CTEASQ9Xpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/2p5e3sudKx2LtM8iSefaSszMY9nCiHz6CTEASQ9Xpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/2p5e3sudKx2LtM8iSefaSszMY9nCiHz6CTEASQ9Xpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/2p5e3sudKx2LtM8iSefaSszMY9nCiHz6CTEASQ9Xpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/2p5e3sudKx2LtM8iSefaSszMY9nCiHz6CTEASQ9Xpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/2p5e3sudKx2LtM8iSefaSszMY9nCiHz6CTEASQ9Xpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/2p5e3sudKx2LtM8iSefaSszMY9nCiHz6CTEASQ9Xpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/2p5e3sudKx2LtM8iSefaSszMY9nCiHz6CTEASQ9Xpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/2p5e3sudKx2LtM8iSefaSszMY9nCiHz6CTEASQ9Xpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/2p5e3sudKx2LtM8iSefaSszMY9nCiHz6CTEASQ9Xpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/2p5e3sudKx2LtM8iSefaSszMY9nCiHz6CTEASQ9Xpump/process_trace.jsonl

### Wish / 2ssMotVbTUfRJev2UnibHzHsoeszPzgwbfsTZPSHpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/2ssMotVbTUfRJev2UnibHzHsoeszPzgwbfsTZPSHpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：Wish｜来源：data/gmgn_candidates_live_run/tokens/2ssMotVbTUfRJev2UnibHzHsoeszPzgwbfsTZPSHpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/2ssMotVbTUfRJev2UnibHzHsoeszPzgwbfsTZPSHpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/2ssMotVbTUfRJev2UnibHzHsoeszPzgwbfsTZPSHpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/2ssMotVbTUfRJev2UnibHzHsoeszPzgwbfsTZPSHpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/2ssMotVbTUfRJev2UnibHzHsoeszPzgwbfsTZPSHpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/2ssMotVbTUfRJev2UnibHzHsoeszPzgwbfsTZPSHpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/2ssMotVbTUfRJev2UnibHzHsoeszPzgwbfsTZPSHpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/2ssMotVbTUfRJev2UnibHzHsoeszPzgwbfsTZPSHpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/2ssMotVbTUfRJev2UnibHzHsoeszPzgwbfsTZPSHpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/2ssMotVbTUfRJev2UnibHzHsoeszPzgwbfsTZPSHpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/2ssMotVbTUfRJev2UnibHzHsoeszPzgwbfsTZPSHpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/2ssMotVbTUfRJev2UnibHzHsoeszPzgwbfsTZPSHpump/process_trace.jsonl

### rice / 2wQq3MrFFHPQnapMt1wnZ2vGkVZDv5ENDCrdLCqFpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T21:36:04Z｜来源：data/gmgn_candidates_live_run/tokens/2wQq3MrFFHPQnapMt1wnZ2vGkVZDv5ENDCrdLCqFpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：rice｜来源：data/gmgn_candidates_live_run/tokens/2wQq3MrFFHPQnapMt1wnZ2vGkVZDv5ENDCrdLCqFpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/2wQq3MrFFHPQnapMt1wnZ2vGkVZDv5ENDCrdLCqFpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/2wQq3MrFFHPQnapMt1wnZ2vGkVZDv5ENDCrdLCqFpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/2wQq3MrFFHPQnapMt1wnZ2vGkVZDv5ENDCrdLCqFpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/2wQq3MrFFHPQnapMt1wnZ2vGkVZDv5ENDCrdLCqFpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/2wQq3MrFFHPQnapMt1wnZ2vGkVZDv5ENDCrdLCqFpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/2wQq3MrFFHPQnapMt1wnZ2vGkVZDv5ENDCrdLCqFpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/2wQq3MrFFHPQnapMt1wnZ2vGkVZDv5ENDCrdLCqFpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/2wQq3MrFFHPQnapMt1wnZ2vGkVZDv5ENDCrdLCqFpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/2wQq3MrFFHPQnapMt1wnZ2vGkVZDv5ENDCrdLCqFpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/2wQq3MrFFHPQnapMt1wnZ2vGkVZDv5ENDCrdLCqFpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/2wQq3MrFFHPQnapMt1wnZ2vGkVZDv5ENDCrdLCqFpump/process_trace.jsonl

### Manfred / 2xbBHYkn6v5PGi19EHp9DiDDTjTB1QHKmwgxdQKx4xff

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T08:39:10Z｜来源：data/gmgn_candidates_live_run/tokens/2xbBHYkn6v5PGi19EHp9DiDDTjTB1QHKmwgxdQKx4xff/token_status.json｜字段：last_update
- 有证据：发现对象符号：Manfred｜来源：data/gmgn_candidates_live_run/tokens/2xbBHYkn6v5PGi19EHp9DiDDTjTB1QHKmwgxdQKx4xff/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/2xbBHYkn6v5PGi19EHp9DiDDTjTB1QHKmwgxdQKx4xff/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/2xbBHYkn6v5PGi19EHp9DiDDTjTB1QHKmwgxdQKx4xff/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/2xbBHYkn6v5PGi19EHp9DiDDTjTB1QHKmwgxdQKx4xff/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/2xbBHYkn6v5PGi19EHp9DiDDTjTB1QHKmwgxdQKx4xff/token_status.json；data/gmgn_candidates_live_run/wallet_structure/2xbBHYkn6v5PGi19EHp9DiDDTjTB1QHKmwgxdQKx4xff/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/2xbBHYkn6v5PGi19EHp9DiDDTjTB1QHKmwgxdQKx4xff/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/2xbBHYkn6v5PGi19EHp9DiDDTjTB1QHKmwgxdQKx4xff/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/2xbBHYkn6v5PGi19EHp9DiDDTjTB1QHKmwgxdQKx4xff/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/2xbBHYkn6v5PGi19EHp9DiDDTjTB1QHKmwgxdQKx4xff/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/2xbBHYkn6v5PGi19EHp9DiDDTjTB1QHKmwgxdQKx4xff/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/2xbBHYkn6v5PGi19EHp9DiDDTjTB1QHKmwgxdQKx4xff/process_trace.jsonl

### Scribblin / 2yoZ6cnXqu5k3EVPH949zwBeXkjhUy2WHWxBXpFXpump

- 当前状态：BLOCKED
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T07:56:36Z｜来源：data/gmgn_candidates_live_run/tokens/2yoZ6cnXqu5k3EVPH949zwBeXkjhUy2WHWxBXpFXpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：Scribblin｜来源：data/gmgn_candidates_live_run/tokens/2yoZ6cnXqu5k3EVPH949zwBeXkjhUy2WHWxBXpFXpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：BLOCKED｜来源：data/gmgn_candidates_live_run/tokens/2yoZ6cnXqu5k3EVPH949zwBeXkjhUy2WHWxBXpFXpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：BLOCKED / 钱包结构门禁阻断：对手盘压力高，接盘/套牢筹码占比偏高｜来源：data/gmgn_candidates_live_run/tokens/2yoZ6cnXqu5k3EVPH949zwBeXkjhUy2WHWxBXpFXpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/2yoZ6cnXqu5k3EVPH949zwBeXkjhUy2WHWxBXpFXpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 有证据：当前状态：BLOCKED｜来源：data/gmgn_candidates_live_run/tokens/2yoZ6cnXqu5k3EVPH949zwBeXkjhUy2WHWxBXpFXpump/token_status.json｜字段：current_state
- 有证据：钱包结构结论：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/2yoZ6cnXqu5k3EVPH949zwBeXkjhUy2WHWxBXpFXpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：钱包结构原因：对手盘压力高，接盘/套牢筹码占比偏高｜来源：data/gmgn_candidates_live_run/wallet_structure/2yoZ6cnXqu5k3EVPH949zwBeXkjhUy2WHWxBXpFXpump/wallet_structure_decision.json｜字段：wallet_structure_reason
- 有证据：quote/security 权限：由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/2yoZ6cnXqu5k3EVPH949zwBeXkjhUy2WHWxBXpFXpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：BLOCKED / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/2yoZ6cnXqu5k3EVPH949zwBeXkjhUy2WHWxBXpFXpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/2yoZ6cnXqu5k3EVPH949zwBeXkjhUy2WHWxBXpFXpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/2yoZ6cnXqu5k3EVPH949zwBeXkjhUy2WHWxBXpFXpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/2yoZ6cnXqu5k3EVPH949zwBeXkjhUy2WHWxBXpFXpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/2yoZ6cnXqu5k3EVPH949zwBeXkjhUy2WHWxBXpFXpump/process_trace.jsonl

### GTAVLOG / 32NJtnoQXoSZPZ8PpUgH3GocZxLf2AoWbaQ7yBRKpump

- 当前状态：BLOCKED
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T09:22:02Z｜来源：data/gmgn_candidates_live_run/tokens/32NJtnoQXoSZPZ8PpUgH3GocZxLf2AoWbaQ7yBRKpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：GTAVLOG｜来源：data/gmgn_candidates_live_run/tokens/32NJtnoQXoSZPZ8PpUgH3GocZxLf2AoWbaQ7yBRKpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：BLOCKED｜来源：data/gmgn_candidates_live_run/tokens/32NJtnoQXoSZPZ8PpUgH3GocZxLf2AoWbaQ7yBRKpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：BLOCKED / 钱包结构门禁阻断：早期钱包集中清仓，筹码控制权疑似向分发/对手盘转移；发现分发侧钱包 6 个；对手盘压力高，接盘/套牢筹码占比偏高｜来源：data/gmgn_candidates_live_run/tokens/32NJtnoQXoSZPZ8PpUgH3GocZxLf2AoWbaQ7yBRKpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/32NJtnoQXoSZPZ8PpUgH3GocZxLf2AoWbaQ7yBRKpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 有证据：当前状态：BLOCKED｜来源：data/gmgn_candidates_live_run/tokens/32NJtnoQXoSZPZ8PpUgH3GocZxLf2AoWbaQ7yBRKpump/token_status.json｜字段：current_state
- 有证据：钱包结构结论：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/32NJtnoQXoSZPZ8PpUgH3GocZxLf2AoWbaQ7yBRKpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：钱包结构原因：早期钱包集中清仓，筹码控制权疑似向分发/对手盘转移；发现分发侧钱包 6 个；对手盘压力高，接盘/套牢筹码占比偏高｜来源：data/gmgn_candidates_live_run/wallet_structure/32NJtnoQXoSZPZ8PpUgH3GocZxLf2AoWbaQ7yBRKpump/wallet_structure_decision.json｜字段：wallet_structure_reason
- 有证据：quote/security 权限：由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/32NJtnoQXoSZPZ8PpUgH3GocZxLf2AoWbaQ7yBRKpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：BLOCKED / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/32NJtnoQXoSZPZ8PpUgH3GocZxLf2AoWbaQ7yBRKpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/32NJtnoQXoSZPZ8PpUgH3GocZxLf2AoWbaQ7yBRKpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/32NJtnoQXoSZPZ8PpUgH3GocZxLf2AoWbaQ7yBRKpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/32NJtnoQXoSZPZ8PpUgH3GocZxLf2AoWbaQ7yBRKpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/32NJtnoQXoSZPZ8PpUgH3GocZxLf2AoWbaQ7yBRKpump/process_trace.jsonl

### SCRIBBLE / 33xDbZM2bUHF841LKJauRZFrDtBJiUKhCH5yVh2KDWH2

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/33xDbZM2bUHF841LKJauRZFrDtBJiUKhCH5yVh2KDWH2/token_status.json｜字段：last_update
- 有证据：发现对象符号：SCRIBBLE｜来源：data/gmgn_candidates_live_run/tokens/33xDbZM2bUHF841LKJauRZFrDtBJiUKhCH5yVh2KDWH2/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/33xDbZM2bUHF841LKJauRZFrDtBJiUKhCH5yVh2KDWH2/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/33xDbZM2bUHF841LKJauRZFrDtBJiUKhCH5yVh2KDWH2/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/33xDbZM2bUHF841LKJauRZFrDtBJiUKhCH5yVh2KDWH2/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/33xDbZM2bUHF841LKJauRZFrDtBJiUKhCH5yVh2KDWH2/token_status.json；data/gmgn_candidates_live_run/wallet_structure/33xDbZM2bUHF841LKJauRZFrDtBJiUKhCH5yVh2KDWH2/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/33xDbZM2bUHF841LKJauRZFrDtBJiUKhCH5yVh2KDWH2/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/33xDbZM2bUHF841LKJauRZFrDtBJiUKhCH5yVh2KDWH2/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/33xDbZM2bUHF841LKJauRZFrDtBJiUKhCH5yVh2KDWH2/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/33xDbZM2bUHF841LKJauRZFrDtBJiUKhCH5yVh2KDWH2/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/33xDbZM2bUHF841LKJauRZFrDtBJiUKhCH5yVh2KDWH2/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/33xDbZM2bUHF841LKJauRZFrDtBJiUKhCH5yVh2KDWH2/process_trace.jsonl

### GOBLIHOUSE / 38CNkUWA8RKHMEAuTGQ5AYUQ5jwKgWLpuKkCsYPLpump

- 当前状态：ACCUMULATING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T08:17:53Z｜来源：data/gmgn_candidates_live_run/tokens/38CNkUWA8RKHMEAuTGQ5AYUQ5jwKgWLpuKkCsYPLpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：GOBLIHOUSE｜来源：data/gmgn_candidates_live_run/tokens/38CNkUWA8RKHMEAuTGQ5AYUQ5jwKgWLpuKkCsYPLpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：ACCUMULATING｜来源：data/gmgn_candidates_live_run/tokens/38CNkUWA8RKHMEAuTGQ5AYUQ5jwKgWLpuKkCsYPLpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：ACCUMULATING / 已出现 T_start，但吸筹窗口仍 pending｜来源：data/gmgn_candidates_live_run/tokens/38CNkUWA8RKHMEAuTGQ5AYUQ5jwKgWLpuKkCsYPLpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/38CNkUWA8RKHMEAuTGQ5AYUQ5jwKgWLpuKkCsYPLpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/38CNkUWA8RKHMEAuTGQ5AYUQ5jwKgWLpuKkCsYPLpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/38CNkUWA8RKHMEAuTGQ5AYUQ5jwKgWLpuKkCsYPLpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/38CNkUWA8RKHMEAuTGQ5AYUQ5jwKgWLpuKkCsYPLpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：ACCUMULATING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/38CNkUWA8RKHMEAuTGQ5AYUQ5jwKgWLpuKkCsYPLpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/38CNkUWA8RKHMEAuTGQ5AYUQ5jwKgWLpuKkCsYPLpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/38CNkUWA8RKHMEAuTGQ5AYUQ5jwKgWLpuKkCsYPLpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/38CNkUWA8RKHMEAuTGQ5AYUQ5jwKgWLpuKkCsYPLpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/38CNkUWA8RKHMEAuTGQ5AYUQ5jwKgWLpuKkCsYPLpump/process_trace.jsonl

### HOTPEPE / 3DCBoC9FcT1RfpabC9Vwqrfeu1th5PBdKRkLF61mzamC

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T11:30:20Z｜来源：data/gmgn_candidates_live_run/tokens/3DCBoC9FcT1RfpabC9Vwqrfeu1th5PBdKRkLF61mzamC/token_status.json｜字段：last_update
- 有证据：发现对象符号：HOTPEPE｜来源：data/gmgn_candidates_live_run/tokens/3DCBoC9FcT1RfpabC9Vwqrfeu1th5PBdKRkLF61mzamC/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/3DCBoC9FcT1RfpabC9Vwqrfeu1th5PBdKRkLF61mzamC/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/3DCBoC9FcT1RfpabC9Vwqrfeu1th5PBdKRkLF61mzamC/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/3DCBoC9FcT1RfpabC9Vwqrfeu1th5PBdKRkLF61mzamC/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/3DCBoC9FcT1RfpabC9Vwqrfeu1th5PBdKRkLF61mzamC/token_status.json；data/gmgn_candidates_live_run/wallet_structure/3DCBoC9FcT1RfpabC9Vwqrfeu1th5PBdKRkLF61mzamC/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/3DCBoC9FcT1RfpabC9Vwqrfeu1th5PBdKRkLF61mzamC/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/3DCBoC9FcT1RfpabC9Vwqrfeu1th5PBdKRkLF61mzamC/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/3DCBoC9FcT1RfpabC9Vwqrfeu1th5PBdKRkLF61mzamC/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/3DCBoC9FcT1RfpabC9Vwqrfeu1th5PBdKRkLF61mzamC/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/3DCBoC9FcT1RfpabC9Vwqrfeu1th5PBdKRkLF61mzamC/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/3DCBoC9FcT1RfpabC9Vwqrfeu1th5PBdKRkLF61mzamC/process_trace.jsonl

### PETS / 3QQQxazHaMb72d7N9iftT26vuk6A4Re31fYmkwA2pump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/3QQQxazHaMb72d7N9iftT26vuk6A4Re31fYmkwA2pump/token_status.json｜字段：last_update
- 有证据：发现对象符号：PETS｜来源：data/gmgn_candidates_live_run/tokens/3QQQxazHaMb72d7N9iftT26vuk6A4Re31fYmkwA2pump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/3QQQxazHaMb72d7N9iftT26vuk6A4Re31fYmkwA2pump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/3QQQxazHaMb72d7N9iftT26vuk6A4Re31fYmkwA2pump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/3QQQxazHaMb72d7N9iftT26vuk6A4Re31fYmkwA2pump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/3QQQxazHaMb72d7N9iftT26vuk6A4Re31fYmkwA2pump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/3QQQxazHaMb72d7N9iftT26vuk6A4Re31fYmkwA2pump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/3QQQxazHaMb72d7N9iftT26vuk6A4Re31fYmkwA2pump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/3QQQxazHaMb72d7N9iftT26vuk6A4Re31fYmkwA2pump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/3QQQxazHaMb72d7N9iftT26vuk6A4Re31fYmkwA2pump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/3QQQxazHaMb72d7N9iftT26vuk6A4Re31fYmkwA2pump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/3QQQxazHaMb72d7N9iftT26vuk6A4Re31fYmkwA2pump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/3QQQxazHaMb72d7N9iftT26vuk6A4Re31fYmkwA2pump/process_trace.jsonl

### LMEOW / 3T3ePWvriBnF82Qp8PA8xD9cacVoqatzfuvFxMfLpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/3T3ePWvriBnF82Qp8PA8xD9cacVoqatzfuvFxMfLpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：LMEOW｜来源：data/gmgn_candidates_live_run/tokens/3T3ePWvriBnF82Qp8PA8xD9cacVoqatzfuvFxMfLpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/3T3ePWvriBnF82Qp8PA8xD9cacVoqatzfuvFxMfLpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/3T3ePWvriBnF82Qp8PA8xD9cacVoqatzfuvFxMfLpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/3T3ePWvriBnF82Qp8PA8xD9cacVoqatzfuvFxMfLpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/3T3ePWvriBnF82Qp8PA8xD9cacVoqatzfuvFxMfLpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/3T3ePWvriBnF82Qp8PA8xD9cacVoqatzfuvFxMfLpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/3T3ePWvriBnF82Qp8PA8xD9cacVoqatzfuvFxMfLpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/3T3ePWvriBnF82Qp8PA8xD9cacVoqatzfuvFxMfLpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/3T3ePWvriBnF82Qp8PA8xD9cacVoqatzfuvFxMfLpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/3T3ePWvriBnF82Qp8PA8xD9cacVoqatzfuvFxMfLpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/3T3ePWvriBnF82Qp8PA8xD9cacVoqatzfuvFxMfLpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/3T3ePWvriBnF82Qp8PA8xD9cacVoqatzfuvFxMfLpump/process_trace.jsonl

### MUSHI / 3es9zL1uMp5MA6FbMGFi9jAhHapoUP7FpFE7njnypump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T10:58:15Z｜来源：data/gmgn_candidates_live_run/tokens/3es9zL1uMp5MA6FbMGFi9jAhHapoUP7FpFE7njnypump/token_status.json｜字段：last_update
- 有证据：发现对象符号：MUSHI｜来源：data/gmgn_candidates_live_run/tokens/3es9zL1uMp5MA6FbMGFi9jAhHapoUP7FpFE7njnypump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/3es9zL1uMp5MA6FbMGFi9jAhHapoUP7FpFE7njnypump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/3es9zL1uMp5MA6FbMGFi9jAhHapoUP7FpFE7njnypump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/3es9zL1uMp5MA6FbMGFi9jAhHapoUP7FpFE7njnypump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/3es9zL1uMp5MA6FbMGFi9jAhHapoUP7FpFE7njnypump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/3es9zL1uMp5MA6FbMGFi9jAhHapoUP7FpFE7njnypump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/3es9zL1uMp5MA6FbMGFi9jAhHapoUP7FpFE7njnypump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/3es9zL1uMp5MA6FbMGFi9jAhHapoUP7FpFE7njnypump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/3es9zL1uMp5MA6FbMGFi9jAhHapoUP7FpFE7njnypump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/3es9zL1uMp5MA6FbMGFi9jAhHapoUP7FpFE7njnypump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/3es9zL1uMp5MA6FbMGFi9jAhHapoUP7FpFE7njnypump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/3es9zL1uMp5MA6FbMGFi9jAhHapoUP7FpFE7njnypump/process_trace.jsonl

### 3 / 3friWWgr5r4RG8VhEcZii8VxHDaWiJaL4vGaw1RQPynq

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T12:19:29Z｜来源：data/gmgn_candidates_live_run/tokens/3friWWgr5r4RG8VhEcZii8VxHDaWiJaL4vGaw1RQPynq/token_status.json｜字段：last_update
- 有证据：发现对象符号：3｜来源：data/gmgn_candidates_live_run/tokens/3friWWgr5r4RG8VhEcZii8VxHDaWiJaL4vGaw1RQPynq/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/3friWWgr5r4RG8VhEcZii8VxHDaWiJaL4vGaw1RQPynq/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/3friWWgr5r4RG8VhEcZii8VxHDaWiJaL4vGaw1RQPynq/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/3friWWgr5r4RG8VhEcZii8VxHDaWiJaL4vGaw1RQPynq/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/3friWWgr5r4RG8VhEcZii8VxHDaWiJaL4vGaw1RQPynq/token_status.json；data/gmgn_candidates_live_run/wallet_structure/3friWWgr5r4RG8VhEcZii8VxHDaWiJaL4vGaw1RQPynq/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/3friWWgr5r4RG8VhEcZii8VxHDaWiJaL4vGaw1RQPynq/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/3friWWgr5r4RG8VhEcZii8VxHDaWiJaL4vGaw1RQPynq/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/3friWWgr5r4RG8VhEcZii8VxHDaWiJaL4vGaw1RQPynq/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/3friWWgr5r4RG8VhEcZii8VxHDaWiJaL4vGaw1RQPynq/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/3friWWgr5r4RG8VhEcZii8VxHDaWiJaL4vGaw1RQPynq/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/3friWWgr5r4RG8VhEcZii8VxHDaWiJaL4vGaw1RQPynq/process_trace.jsonl

### FINE / 3hHZ3QFWKVgUdi64uHJumK9T7hDR2Tr6WZBjUfP5pump

- 当前状态：PAPER_READY
- 最新动作：OPEN_PAPER_POSITION
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T20:01:44Z｜来源：data/gmgn_candidates_live_run/tokens/3hHZ3QFWKVgUdi64uHJumK9T7hDR2Tr6WZBjUfP5pump/token_status.json｜字段：last_update
- 有证据：发现对象符号：FINE｜来源：data/gmgn_candidates_live_run/tokens/3hHZ3QFWKVgUdi64uHJumK9T7hDR2Tr6WZBjUfP5pump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：PAPER_READY｜来源：data/gmgn_candidates_live_run/tokens/3hHZ3QFWKVgUdi64uHJumK9T7hDR2Tr6WZBjUfP5pump/token_status.json｜字段：current_state
- 有证据：最近流程记录：PAPER_READY / 吸筹窗口 valid + SIKK S3/S4 + 允许纸面交易 + 仓位大于0｜来源：data/gmgn_candidates_live_run/tokens/3hHZ3QFWKVgUdi64uHJumK9T7hDR2Tr6WZBjUfP5pump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 有证据：钱包结构结论：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/3hHZ3QFWKVgUdi64uHJumK9T7hDR2Tr6WZBjUfP5pump/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：quote/security 权限：ALLOW_CONFIRMATION_LAYER｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 有证据：当前状态：PAPER_READY｜来源：data/gmgn_candidates_live_run/tokens/3hHZ3QFWKVgUdi64uHJumK9T7hDR2Tr6WZBjUfP5pump/token_status.json｜字段：current_state
- 有证据：钱包结构结论：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/3hHZ3QFWKVgUdi64uHJumK9T7hDR2Tr6WZBjUfP5pump/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：钱包结构原因：发现分发侧钱包 6 个；对手盘压力高，接盘/套牢筹码占比偏高｜来源：data/gmgn_candidates_live_run/wallet_structure/3hHZ3QFWKVgUdi64uHJumK9T7hDR2Tr6WZBjUfP5pump/wallet_structure_decision.json｜字段：wallet_structure_reason
- 有证据：quote/security 权限：ALLOW_CONFIRMATION_LAYER｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission

#### 为什么进入paper
- 有证据：当前状态：PAPER_READY｜来源：data/gmgn_candidates_live_run/tokens/3hHZ3QFWKVgUdi64uHJumK9T7hDR2Tr6WZBjUfP5pump/token_status.json｜字段：current_state
- 有证据：最新动作：OPEN_PAPER_POSITION｜来源：data/gmgn_candidates_live_run/tokens/3hHZ3QFWKVgUdi64uHJumK9T7hDR2Tr6WZBjUfP5pump/token_status.json｜字段：latest_action
- 有证据：入场依据：吸筹窗口 valid + SIKK S3/S4 + 允许纸面交易 + 仓位大于0｜来源：data/gmgn_candidates_live_run/tokens/3hHZ3QFWKVgUdi64uHJumK9T7hDR2Tr6WZBjUfP5pump/token_status.json｜字段：latest_reason

#### 为什么退出
- 有证据：纸面退出原因：命中纸面止损｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json｜字段：exit_reason
- 有证据：纸面退出时间：2026-05-02T20:02:21Z｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json｜字段：exit_time
- 有证据：当前状态：PAPER_READY｜来源：data/gmgn_candidates_live_run/tokens/3hHZ3QFWKVgUdi64uHJumK9T7hDR2Tr6WZBjUfP5pump/token_status.json｜字段：current_state

#### 为什么失败
- 有证据：失败类型：STRUCTURE_WEAKENING｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl｜字段：failure_type
- 有证据：失败原因：钱包结构状态变为 WALLET_BLOCK，纸面阶段直接模拟退出｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl｜字段：failure_reason
- 有证据：当前状态：PAPER_READY｜来源：data/gmgn_candidates_live_run/tokens/3hHZ3QFWKVgUdi64uHJumK9T7hDR2Tr6WZBjUfP5pump/token_status.json｜字段：current_state

#### 下一步看什么
- 待复查：复查最新状态/动作：PAPER_READY / OPEN_PAPER_POSITION｜来源：data/gmgn_candidates_live_run/tokens/3hHZ3QFWKVgUdi64uHJumK9T7hDR2Tr6WZBjUfP5pump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/3hHZ3QFWKVgUdi64uHJumK9T7hDR2Tr6WZBjUfP5pump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：ALLOW_CONFIRMATION_LAYER / READY_FOR_CONFIRMATION｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/3hHZ3QFWKVgUdi64uHJumK9T7hDR2Tr6WZBjUfP5pump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/3hHZ3QFWKVgUdi64uHJumK9T7hDR2Tr6WZBjUfP5pump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/3hHZ3QFWKVgUdi64uHJumK9T7hDR2Tr6WZBjUfP5pump/process_trace.jsonl

### Faglon / 3kJYnVAhCWyLLkoEC2WdGZKwjFu77oXeayvuhbrupump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T21:36:04Z｜来源：data/gmgn_candidates_live_run/tokens/3kJYnVAhCWyLLkoEC2WdGZKwjFu77oXeayvuhbrupump/token_status.json｜字段：last_update
- 有证据：发现对象符号：Faglon｜来源：data/gmgn_candidates_live_run/tokens/3kJYnVAhCWyLLkoEC2WdGZKwjFu77oXeayvuhbrupump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/3kJYnVAhCWyLLkoEC2WdGZKwjFu77oXeayvuhbrupump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/3kJYnVAhCWyLLkoEC2WdGZKwjFu77oXeayvuhbrupump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/3kJYnVAhCWyLLkoEC2WdGZKwjFu77oXeayvuhbrupump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/3kJYnVAhCWyLLkoEC2WdGZKwjFu77oXeayvuhbrupump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/3kJYnVAhCWyLLkoEC2WdGZKwjFu77oXeayvuhbrupump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/3kJYnVAhCWyLLkoEC2WdGZKwjFu77oXeayvuhbrupump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/3kJYnVAhCWyLLkoEC2WdGZKwjFu77oXeayvuhbrupump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/3kJYnVAhCWyLLkoEC2WdGZKwjFu77oXeayvuhbrupump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/3kJYnVAhCWyLLkoEC2WdGZKwjFu77oXeayvuhbrupump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/3kJYnVAhCWyLLkoEC2WdGZKwjFu77oXeayvuhbrupump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/3kJYnVAhCWyLLkoEC2WdGZKwjFu77oXeayvuhbrupump/process_trace.jsonl

### GOP / 3pCyU31quPpsVYaC5TxtXpe6sR1KXSLzk5TkZgXGpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/3pCyU31quPpsVYaC5TxtXpe6sR1KXSLzk5TkZgXGpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：GOP｜来源：data/gmgn_candidates_live_run/tokens/3pCyU31quPpsVYaC5TxtXpe6sR1KXSLzk5TkZgXGpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/3pCyU31quPpsVYaC5TxtXpe6sR1KXSLzk5TkZgXGpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/3pCyU31quPpsVYaC5TxtXpe6sR1KXSLzk5TkZgXGpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/3pCyU31quPpsVYaC5TxtXpe6sR1KXSLzk5TkZgXGpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/3pCyU31quPpsVYaC5TxtXpe6sR1KXSLzk5TkZgXGpump/token_status.json｜字段：current_state
- 有证据：钱包结构结论：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/3pCyU31quPpsVYaC5TxtXpe6sR1KXSLzk5TkZgXGpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：钱包结构原因：发现分发侧钱包 57 个｜来源：data/gmgn_candidates_live_run/wallet_structure/3pCyU31quPpsVYaC5TxtXpe6sR1KXSLzk5TkZgXGpump/wallet_structure_decision.json｜字段：wallet_structure_reason
- 有证据：quote/security 权限：MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/3pCyU31quPpsVYaC5TxtXpe6sR1KXSLzk5TkZgXGpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/3pCyU31quPpsVYaC5TxtXpe6sR1KXSLzk5TkZgXGpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/3pCyU31quPpsVYaC5TxtXpe6sR1KXSLzk5TkZgXGpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/3pCyU31quPpsVYaC5TxtXpe6sR1KXSLzk5TkZgXGpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/3pCyU31quPpsVYaC5TxtXpe6sR1KXSLzk5TkZgXGpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/3pCyU31quPpsVYaC5TxtXpe6sR1KXSLzk5TkZgXGpump/process_trace.jsonl

### AGI / 3qwtMkiBc4uFSPmZeK7TMq8dVzmB4kCqnARXxAkmpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T10:36:52Z｜来源：data/gmgn_candidates_live_run/tokens/3qwtMkiBc4uFSPmZeK7TMq8dVzmB4kCqnARXxAkmpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：AGI｜来源：data/gmgn_candidates_live_run/tokens/3qwtMkiBc4uFSPmZeK7TMq8dVzmB4kCqnARXxAkmpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/3qwtMkiBc4uFSPmZeK7TMq8dVzmB4kCqnARXxAkmpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/3qwtMkiBc4uFSPmZeK7TMq8dVzmB4kCqnARXxAkmpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/3qwtMkiBc4uFSPmZeK7TMq8dVzmB4kCqnARXxAkmpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/3qwtMkiBc4uFSPmZeK7TMq8dVzmB4kCqnARXxAkmpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/3qwtMkiBc4uFSPmZeK7TMq8dVzmB4kCqnARXxAkmpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/3qwtMkiBc4uFSPmZeK7TMq8dVzmB4kCqnARXxAkmpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/3qwtMkiBc4uFSPmZeK7TMq8dVzmB4kCqnARXxAkmpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/3qwtMkiBc4uFSPmZeK7TMq8dVzmB4kCqnARXxAkmpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/3qwtMkiBc4uFSPmZeK7TMq8dVzmB4kCqnARXxAkmpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/3qwtMkiBc4uFSPmZeK7TMq8dVzmB4kCqnARXxAkmpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/3qwtMkiBc4uFSPmZeK7TMq8dVzmB4kCqnARXxAkmpump/process_trace.jsonl

### HODLERS / 42ieLgTvKFwecrnYRNpTSBwWYgHLjCkfKKLecX9Tpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T18:15:51Z｜来源：data/gmgn_candidates_live_run/tokens/42ieLgTvKFwecrnYRNpTSBwWYgHLjCkfKKLecX9Tpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：HODLERS｜来源：data/gmgn_candidates_live_run/tokens/42ieLgTvKFwecrnYRNpTSBwWYgHLjCkfKKLecX9Tpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/42ieLgTvKFwecrnYRNpTSBwWYgHLjCkfKKLecX9Tpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/42ieLgTvKFwecrnYRNpTSBwWYgHLjCkfKKLecX9Tpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/42ieLgTvKFwecrnYRNpTSBwWYgHLjCkfKKLecX9Tpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/42ieLgTvKFwecrnYRNpTSBwWYgHLjCkfKKLecX9Tpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/42ieLgTvKFwecrnYRNpTSBwWYgHLjCkfKKLecX9Tpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/42ieLgTvKFwecrnYRNpTSBwWYgHLjCkfKKLecX9Tpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/42ieLgTvKFwecrnYRNpTSBwWYgHLjCkfKKLecX9Tpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/42ieLgTvKFwecrnYRNpTSBwWYgHLjCkfKKLecX9Tpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/42ieLgTvKFwecrnYRNpTSBwWYgHLjCkfKKLecX9Tpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/42ieLgTvKFwecrnYRNpTSBwWYgHLjCkfKKLecX9Tpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/42ieLgTvKFwecrnYRNpTSBwWYgHLjCkfKKLecX9Tpump/process_trace.jsonl

### TICK  / 4EKxurxAC4Tt7NrBR164vPZ9v7jwAhSeQ3ynFbANpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T21:46:26Z｜来源：data/gmgn_candidates_live_run/tokens/4EKxurxAC4Tt7NrBR164vPZ9v7jwAhSeQ3ynFbANpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：TICK ｜来源：data/gmgn_candidates_live_run/tokens/4EKxurxAC4Tt7NrBR164vPZ9v7jwAhSeQ3ynFbANpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/4EKxurxAC4Tt7NrBR164vPZ9v7jwAhSeQ3ynFbANpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/4EKxurxAC4Tt7NrBR164vPZ9v7jwAhSeQ3ynFbANpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/4EKxurxAC4Tt7NrBR164vPZ9v7jwAhSeQ3ynFbANpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/4EKxurxAC4Tt7NrBR164vPZ9v7jwAhSeQ3ynFbANpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/4EKxurxAC4Tt7NrBR164vPZ9v7jwAhSeQ3ynFbANpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/4EKxurxAC4Tt7NrBR164vPZ9v7jwAhSeQ3ynFbANpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/4EKxurxAC4Tt7NrBR164vPZ9v7jwAhSeQ3ynFbANpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/4EKxurxAC4Tt7NrBR164vPZ9v7jwAhSeQ3ynFbANpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/4EKxurxAC4Tt7NrBR164vPZ9v7jwAhSeQ3ynFbANpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/4EKxurxAC4Tt7NrBR164vPZ9v7jwAhSeQ3ynFbANpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/4EKxurxAC4Tt7NrBR164vPZ9v7jwAhSeQ3ynFbANpump/process_trace.jsonl

### Lana / 4PV3vCzAAU7K7oeh3j8MnXh52LUqdn3voo2yN7Stvyp2

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T11:41:02Z｜来源：data/gmgn_candidates_live_run/tokens/4PV3vCzAAU7K7oeh3j8MnXh52LUqdn3voo2yN7Stvyp2/token_status.json｜字段：last_update
- 有证据：发现对象符号：Lana｜来源：data/gmgn_candidates_live_run/tokens/4PV3vCzAAU7K7oeh3j8MnXh52LUqdn3voo2yN7Stvyp2/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/4PV3vCzAAU7K7oeh3j8MnXh52LUqdn3voo2yN7Stvyp2/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/4PV3vCzAAU7K7oeh3j8MnXh52LUqdn3voo2yN7Stvyp2/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/4PV3vCzAAU7K7oeh3j8MnXh52LUqdn3voo2yN7Stvyp2/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/4PV3vCzAAU7K7oeh3j8MnXh52LUqdn3voo2yN7Stvyp2/token_status.json；data/gmgn_candidates_live_run/wallet_structure/4PV3vCzAAU7K7oeh3j8MnXh52LUqdn3voo2yN7Stvyp2/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/4PV3vCzAAU7K7oeh3j8MnXh52LUqdn3voo2yN7Stvyp2/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/4PV3vCzAAU7K7oeh3j8MnXh52LUqdn3voo2yN7Stvyp2/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/4PV3vCzAAU7K7oeh3j8MnXh52LUqdn3voo2yN7Stvyp2/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/4PV3vCzAAU7K7oeh3j8MnXh52LUqdn3voo2yN7Stvyp2/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/4PV3vCzAAU7K7oeh3j8MnXh52LUqdn3voo2yN7Stvyp2/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/4PV3vCzAAU7K7oeh3j8MnXh52LUqdn3voo2yN7Stvyp2/process_trace.jsonl

### GOBLIEN / 4bNNLxMjDmoQz1QxfbhiMJJpe3m2LDQUUW5edfnMpump

- 当前状态：PAPER_READY
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T13:54:08Z｜来源：data/gmgn_candidates_live_run/tokens/4bNNLxMjDmoQz1QxfbhiMJJpe3m2LDQUUW5edfnMpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：GOBLIEN｜来源：data/gmgn_candidates_live_run/tokens/4bNNLxMjDmoQz1QxfbhiMJJpe3m2LDQUUW5edfnMpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：PAPER_READY｜来源：data/gmgn_candidates_live_run/tokens/4bNNLxMjDmoQz1QxfbhiMJJpe3m2LDQUUW5edfnMpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：PAPER_READY / 吸筹窗口 valid + SIKK S3/S4 + 允许纸面交易 + 仓位大于0｜来源：data/gmgn_candidates_live_run/tokens/4bNNLxMjDmoQz1QxfbhiMJJpe3m2LDQUUW5edfnMpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/4bNNLxMjDmoQz1QxfbhiMJJpe3m2LDQUUW5edfnMpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 有证据：当前状态：PAPER_READY｜来源：data/gmgn_candidates_live_run/tokens/4bNNLxMjDmoQz1QxfbhiMJJpe3m2LDQUUW5edfnMpump/token_status.json｜字段：current_state
- 有证据：钱包结构结论：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/4bNNLxMjDmoQz1QxfbhiMJJpe3m2LDQUUW5edfnMpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：钱包结构原因：发现分发侧钱包 2 个；对手盘压力高，接盘/套牢筹码占比偏高｜来源：data/gmgn_candidates_live_run/wallet_structure/4bNNLxMjDmoQz1QxfbhiMJJpe3m2LDQUUW5edfnMpump/wallet_structure_decision.json｜字段：wallet_structure_reason
- 有证据：quote/security 权限：由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission

#### 为什么进入paper
- 有证据：当前状态：PAPER_READY｜来源：data/gmgn_candidates_live_run/tokens/4bNNLxMjDmoQz1QxfbhiMJJpe3m2LDQUUW5edfnMpump/token_status.json｜字段：current_state
- 有证据：最新动作：LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/4bNNLxMjDmoQz1QxfbhiMJJpe3m2LDQUUW5edfnMpump/token_status.json｜字段：latest_action
- 有证据：入场依据：吸筹窗口 valid + SIKK S3/S4 + 允许纸面交易 + 仓位大于0｜来源：data/gmgn_candidates_live_run/tokens/4bNNLxMjDmoQz1QxfbhiMJJpe3m2LDQUUW5edfnMpump/token_status.json｜字段：latest_reason

#### 为什么退出
- 有证据：纸面退出原因：钱包结构触发纸面强制退出｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json｜字段：exit_reason
- 有证据：纸面退出时间：2026-05-02T17:33:17Z｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json｜字段：exit_time
- 有证据：当前状态：PAPER_READY｜来源：data/gmgn_candidates_live_run/tokens/4bNNLxMjDmoQz1QxfbhiMJJpe3m2LDQUUW5edfnMpump/token_status.json｜字段：current_state

#### 为什么失败
- 有证据：失败类型：STRUCTURE_WEAKENING｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl｜字段：failure_type
- 有证据：失败原因：钱包结构状态变为 WALLET_BLOCK，纸面阶段直接模拟退出｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl｜字段：failure_reason
- 有证据：当前状态：PAPER_READY｜来源：data/gmgn_candidates_live_run/tokens/4bNNLxMjDmoQz1QxfbhiMJJpe3m2LDQUUW5edfnMpump/token_status.json｜字段：current_state

#### 下一步看什么
- 待复查：复查最新状态/动作：PAPER_READY / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/4bNNLxMjDmoQz1QxfbhiMJJpe3m2LDQUUW5edfnMpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/4bNNLxMjDmoQz1QxfbhiMJJpe3m2LDQUUW5edfnMpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/4bNNLxMjDmoQz1QxfbhiMJJpe3m2LDQUUW5edfnMpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/4bNNLxMjDmoQz1QxfbhiMJJpe3m2LDQUUW5edfnMpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/4bNNLxMjDmoQz1QxfbhiMJJpe3m2LDQUUW5edfnMpump/process_trace.jsonl

### MSPEPE / 4kCZp6rLBNSrjHEYXbE54MYbFb5dpMuptBtZHnMvpump

- 当前状态：BLOCKED
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T12:19:29Z｜来源：data/gmgn_candidates_live_run/tokens/4kCZp6rLBNSrjHEYXbE54MYbFb5dpMuptBtZHnMvpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：MSPEPE｜来源：data/gmgn_candidates_live_run/tokens/4kCZp6rLBNSrjHEYXbE54MYbFb5dpMuptBtZHnMvpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：BLOCKED｜来源：data/gmgn_candidates_live_run/tokens/4kCZp6rLBNSrjHEYXbE54MYbFb5dpMuptBtZHnMvpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：BLOCKED / 钱包结构门禁阻断：发现分发侧钱包 2 个；对手盘压力高，接盘/套牢筹码占比偏高｜来源：data/gmgn_candidates_live_run/tokens/4kCZp6rLBNSrjHEYXbE54MYbFb5dpMuptBtZHnMvpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/4kCZp6rLBNSrjHEYXbE54MYbFb5dpMuptBtZHnMvpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 有证据：当前状态：BLOCKED｜来源：data/gmgn_candidates_live_run/tokens/4kCZp6rLBNSrjHEYXbE54MYbFb5dpMuptBtZHnMvpump/token_status.json｜字段：current_state
- 有证据：钱包结构结论：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/4kCZp6rLBNSrjHEYXbE54MYbFb5dpMuptBtZHnMvpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：钱包结构原因：发现分发侧钱包 2 个；对手盘压力高，接盘/套牢筹码占比偏高｜来源：data/gmgn_candidates_live_run/wallet_structure/4kCZp6rLBNSrjHEYXbE54MYbFb5dpMuptBtZHnMvpump/wallet_structure_decision.json｜字段：wallet_structure_reason
- 有证据：quote/security 权限：由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/4kCZp6rLBNSrjHEYXbE54MYbFb5dpMuptBtZHnMvpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：BLOCKED / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/4kCZp6rLBNSrjHEYXbE54MYbFb5dpMuptBtZHnMvpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/4kCZp6rLBNSrjHEYXbE54MYbFb5dpMuptBtZHnMvpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/4kCZp6rLBNSrjHEYXbE54MYbFb5dpMuptBtZHnMvpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/4kCZp6rLBNSrjHEYXbE54MYbFb5dpMuptBtZHnMvpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/4kCZp6rLBNSrjHEYXbE54MYbFb5dpMuptBtZHnMvpump/process_trace.jsonl

### WCINU / 4mLUpStfvutSZP27m397WmArEbS8xt5HKTzFL8Depump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T21:15:08Z｜来源：data/gmgn_candidates_live_run/tokens/4mLUpStfvutSZP27m397WmArEbS8xt5HKTzFL8Depump/token_status.json｜字段：last_update
- 有证据：发现对象符号：WCINU｜来源：data/gmgn_candidates_live_run/tokens/4mLUpStfvutSZP27m397WmArEbS8xt5HKTzFL8Depump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/4mLUpStfvutSZP27m397WmArEbS8xt5HKTzFL8Depump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/4mLUpStfvutSZP27m397WmArEbS8xt5HKTzFL8Depump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/4mLUpStfvutSZP27m397WmArEbS8xt5HKTzFL8Depump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/4mLUpStfvutSZP27m397WmArEbS8xt5HKTzFL8Depump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/4mLUpStfvutSZP27m397WmArEbS8xt5HKTzFL8Depump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/4mLUpStfvutSZP27m397WmArEbS8xt5HKTzFL8Depump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/4mLUpStfvutSZP27m397WmArEbS8xt5HKTzFL8Depump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/4mLUpStfvutSZP27m397WmArEbS8xt5HKTzFL8Depump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/4mLUpStfvutSZP27m397WmArEbS8xt5HKTzFL8Depump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/4mLUpStfvutSZP27m397WmArEbS8xt5HKTzFL8Depump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/4mLUpStfvutSZP27m397WmArEbS8xt5HKTzFL8Depump/process_trace.jsonl

### ROAF / 4ne9SgdsLE2P2FJEjxDxUnpwS3fLGCPpHFzYeuDCpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/4ne9SgdsLE2P2FJEjxDxUnpwS3fLGCPpHFzYeuDCpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：ROAF｜来源：data/gmgn_candidates_live_run/tokens/4ne9SgdsLE2P2FJEjxDxUnpwS3fLGCPpHFzYeuDCpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/4ne9SgdsLE2P2FJEjxDxUnpwS3fLGCPpHFzYeuDCpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/4ne9SgdsLE2P2FJEjxDxUnpwS3fLGCPpHFzYeuDCpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/4ne9SgdsLE2P2FJEjxDxUnpwS3fLGCPpHFzYeuDCpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/4ne9SgdsLE2P2FJEjxDxUnpwS3fLGCPpHFzYeuDCpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/4ne9SgdsLE2P2FJEjxDxUnpwS3fLGCPpHFzYeuDCpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/4ne9SgdsLE2P2FJEjxDxUnpwS3fLGCPpHFzYeuDCpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/4ne9SgdsLE2P2FJEjxDxUnpwS3fLGCPpHFzYeuDCpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/4ne9SgdsLE2P2FJEjxDxUnpwS3fLGCPpHFzYeuDCpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/4ne9SgdsLE2P2FJEjxDxUnpwS3fLGCPpHFzYeuDCpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/4ne9SgdsLE2P2FJEjxDxUnpwS3fLGCPpHFzYeuDCpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/4ne9SgdsLE2P2FJEjxDxUnpwS3fLGCPpHFzYeuDCpump/process_trace.jsonl

### CREATURES / 4y1gkKzCb4qAiH8pH8ft2xvezf6sazurmYDajWXwpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T10:47:33Z｜来源：data/gmgn_candidates_live_run/tokens/4y1gkKzCb4qAiH8pH8ft2xvezf6sazurmYDajWXwpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：CREATURES｜来源：data/gmgn_candidates_live_run/tokens/4y1gkKzCb4qAiH8pH8ft2xvezf6sazurmYDajWXwpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/4y1gkKzCb4qAiH8pH8ft2xvezf6sazurmYDajWXwpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/4y1gkKzCb4qAiH8pH8ft2xvezf6sazurmYDajWXwpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/4y1gkKzCb4qAiH8pH8ft2xvezf6sazurmYDajWXwpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/4y1gkKzCb4qAiH8pH8ft2xvezf6sazurmYDajWXwpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/4y1gkKzCb4qAiH8pH8ft2xvezf6sazurmYDajWXwpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/4y1gkKzCb4qAiH8pH8ft2xvezf6sazurmYDajWXwpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/4y1gkKzCb4qAiH8pH8ft2xvezf6sazurmYDajWXwpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/4y1gkKzCb4qAiH8pH8ft2xvezf6sazurmYDajWXwpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/4y1gkKzCb4qAiH8pH8ft2xvezf6sazurmYDajWXwpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/4y1gkKzCb4qAiH8pH8ft2xvezf6sazurmYDajWXwpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/4y1gkKzCb4qAiH8pH8ft2xvezf6sazurmYDajWXwpump/process_trace.jsonl

### NORMIE / 4y874got9bZ2sR42qHYdnfoL6UcdfMaa1SjcP7Ucpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/4y874got9bZ2sR42qHYdnfoL6UcdfMaa1SjcP7Ucpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：NORMIE｜来源：data/gmgn_candidates_live_run/tokens/4y874got9bZ2sR42qHYdnfoL6UcdfMaa1SjcP7Ucpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/4y874got9bZ2sR42qHYdnfoL6UcdfMaa1SjcP7Ucpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/4y874got9bZ2sR42qHYdnfoL6UcdfMaa1SjcP7Ucpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/4y874got9bZ2sR42qHYdnfoL6UcdfMaa1SjcP7Ucpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/4y874got9bZ2sR42qHYdnfoL6UcdfMaa1SjcP7Ucpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/4y874got9bZ2sR42qHYdnfoL6UcdfMaa1SjcP7Ucpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/4y874got9bZ2sR42qHYdnfoL6UcdfMaa1SjcP7Ucpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/4y874got9bZ2sR42qHYdnfoL6UcdfMaa1SjcP7Ucpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/4y874got9bZ2sR42qHYdnfoL6UcdfMaa1SjcP7Ucpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/4y874got9bZ2sR42qHYdnfoL6UcdfMaa1SjcP7Ucpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/4y874got9bZ2sR42qHYdnfoL6UcdfMaa1SjcP7Ucpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/4y874got9bZ2sR42qHYdnfoL6UcdfMaa1SjcP7Ucpump/process_trace.jsonl

### Life / 533wS5wLqdr9JtnLfRW5WKv5cFdKHLKMnjwidJSgpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T21:04:41Z｜来源：data/gmgn_candidates_live_run/tokens/533wS5wLqdr9JtnLfRW5WKv5cFdKHLKMnjwidJSgpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：Life｜来源：data/gmgn_candidates_live_run/tokens/533wS5wLqdr9JtnLfRW5WKv5cFdKHLKMnjwidJSgpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/533wS5wLqdr9JtnLfRW5WKv5cFdKHLKMnjwidJSgpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/533wS5wLqdr9JtnLfRW5WKv5cFdKHLKMnjwidJSgpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/533wS5wLqdr9JtnLfRW5WKv5cFdKHLKMnjwidJSgpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/533wS5wLqdr9JtnLfRW5WKv5cFdKHLKMnjwidJSgpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/533wS5wLqdr9JtnLfRW5WKv5cFdKHLKMnjwidJSgpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/533wS5wLqdr9JtnLfRW5WKv5cFdKHLKMnjwidJSgpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/533wS5wLqdr9JtnLfRW5WKv5cFdKHLKMnjwidJSgpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/533wS5wLqdr9JtnLfRW5WKv5cFdKHLKMnjwidJSgpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/533wS5wLqdr9JtnLfRW5WKv5cFdKHLKMnjwidJSgpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/533wS5wLqdr9JtnLfRW5WKv5cFdKHLKMnjwidJSgpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/533wS5wLqdr9JtnLfRW5WKv5cFdKHLKMnjwidJSgpump/process_trace.jsonl

### ROAF / 5ByEYVGSKtTzcQRhY8QkWRqKdhweXMHvHnacRznYnhUY

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/5ByEYVGSKtTzcQRhY8QkWRqKdhweXMHvHnacRznYnhUY/token_status.json｜字段：last_update
- 有证据：发现对象符号：ROAF｜来源：data/gmgn_candidates_live_run/tokens/5ByEYVGSKtTzcQRhY8QkWRqKdhweXMHvHnacRznYnhUY/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/5ByEYVGSKtTzcQRhY8QkWRqKdhweXMHvHnacRznYnhUY/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/5ByEYVGSKtTzcQRhY8QkWRqKdhweXMHvHnacRznYnhUY/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/5ByEYVGSKtTzcQRhY8QkWRqKdhweXMHvHnacRznYnhUY/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/5ByEYVGSKtTzcQRhY8QkWRqKdhweXMHvHnacRznYnhUY/token_status.json；data/gmgn_candidates_live_run/wallet_structure/5ByEYVGSKtTzcQRhY8QkWRqKdhweXMHvHnacRznYnhUY/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/5ByEYVGSKtTzcQRhY8QkWRqKdhweXMHvHnacRznYnhUY/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/5ByEYVGSKtTzcQRhY8QkWRqKdhweXMHvHnacRznYnhUY/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/5ByEYVGSKtTzcQRhY8QkWRqKdhweXMHvHnacRznYnhUY/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/5ByEYVGSKtTzcQRhY8QkWRqKdhweXMHvHnacRznYnhUY/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/5ByEYVGSKtTzcQRhY8QkWRqKdhweXMHvHnacRznYnhUY/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/5ByEYVGSKtTzcQRhY8QkWRqKdhweXMHvHnacRznYnhUY/process_trace.jsonl

### MUSK / 5C71ySmA8Jd9NhyFHiNRsmZwrX26fRp7nknB7bzGpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:17:29Z｜来源：data/gmgn_candidates_live_run/tokens/5C71ySmA8Jd9NhyFHiNRsmZwrX26fRp7nknB7bzGpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：MUSK｜来源：data/gmgn_candidates_live_run/tokens/5C71ySmA8Jd9NhyFHiNRsmZwrX26fRp7nknB7bzGpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/5C71ySmA8Jd9NhyFHiNRsmZwrX26fRp7nknB7bzGpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/5C71ySmA8Jd9NhyFHiNRsmZwrX26fRp7nknB7bzGpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/5C71ySmA8Jd9NhyFHiNRsmZwrX26fRp7nknB7bzGpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/5C71ySmA8Jd9NhyFHiNRsmZwrX26fRp7nknB7bzGpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/5C71ySmA8Jd9NhyFHiNRsmZwrX26fRp7nknB7bzGpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/5C71ySmA8Jd9NhyFHiNRsmZwrX26fRp7nknB7bzGpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/5C71ySmA8Jd9NhyFHiNRsmZwrX26fRp7nknB7bzGpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/5C71ySmA8Jd9NhyFHiNRsmZwrX26fRp7nknB7bzGpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/5C71ySmA8Jd9NhyFHiNRsmZwrX26fRp7nknB7bzGpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/5C71ySmA8Jd9NhyFHiNRsmZwrX26fRp7nknB7bzGpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/5C71ySmA8Jd9NhyFHiNRsmZwrX26fRp7nknB7bzGpump/process_trace.jsonl

### SHARKYPEPE / 5Rc8u7maeVVJNGTWzr1rTdQi88UuvXUM1mAYzVSxtEyo

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T12:19:29Z｜来源：data/gmgn_candidates_live_run/tokens/5Rc8u7maeVVJNGTWzr1rTdQi88UuvXUM1mAYzVSxtEyo/token_status.json｜字段：last_update
- 有证据：发现对象符号：SHARKYPEPE｜来源：data/gmgn_candidates_live_run/tokens/5Rc8u7maeVVJNGTWzr1rTdQi88UuvXUM1mAYzVSxtEyo/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/5Rc8u7maeVVJNGTWzr1rTdQi88UuvXUM1mAYzVSxtEyo/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/5Rc8u7maeVVJNGTWzr1rTdQi88UuvXUM1mAYzVSxtEyo/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/5Rc8u7maeVVJNGTWzr1rTdQi88UuvXUM1mAYzVSxtEyo/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/5Rc8u7maeVVJNGTWzr1rTdQi88UuvXUM1mAYzVSxtEyo/token_status.json；data/gmgn_candidates_live_run/wallet_structure/5Rc8u7maeVVJNGTWzr1rTdQi88UuvXUM1mAYzVSxtEyo/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/5Rc8u7maeVVJNGTWzr1rTdQi88UuvXUM1mAYzVSxtEyo/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/5Rc8u7maeVVJNGTWzr1rTdQi88UuvXUM1mAYzVSxtEyo/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/5Rc8u7maeVVJNGTWzr1rTdQi88UuvXUM1mAYzVSxtEyo/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/5Rc8u7maeVVJNGTWzr1rTdQi88UuvXUM1mAYzVSxtEyo/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/5Rc8u7maeVVJNGTWzr1rTdQi88UuvXUM1mAYzVSxtEyo/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/5Rc8u7maeVVJNGTWzr1rTdQi88UuvXUM1mAYzVSxtEyo/process_trace.jsonl

### USDC / 5RtpfXg8x574bpNUQpAaoVNtEBfQg7c5h1u4tG41Y2jd

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T21:36:04Z｜来源：data/gmgn_candidates_live_run/tokens/5RtpfXg8x574bpNUQpAaoVNtEBfQg7c5h1u4tG41Y2jd/token_status.json｜字段：last_update
- 有证据：发现对象符号：USDC｜来源：data/gmgn_candidates_live_run/tokens/5RtpfXg8x574bpNUQpAaoVNtEBfQg7c5h1u4tG41Y2jd/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/5RtpfXg8x574bpNUQpAaoVNtEBfQg7c5h1u4tG41Y2jd/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/5RtpfXg8x574bpNUQpAaoVNtEBfQg7c5h1u4tG41Y2jd/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/5RtpfXg8x574bpNUQpAaoVNtEBfQg7c5h1u4tG41Y2jd/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/5RtpfXg8x574bpNUQpAaoVNtEBfQg7c5h1u4tG41Y2jd/token_status.json；data/gmgn_candidates_live_run/wallet_structure/5RtpfXg8x574bpNUQpAaoVNtEBfQg7c5h1u4tG41Y2jd/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/5RtpfXg8x574bpNUQpAaoVNtEBfQg7c5h1u4tG41Y2jd/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/5RtpfXg8x574bpNUQpAaoVNtEBfQg7c5h1u4tG41Y2jd/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/5RtpfXg8x574bpNUQpAaoVNtEBfQg7c5h1u4tG41Y2jd/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/5RtpfXg8x574bpNUQpAaoVNtEBfQg7c5h1u4tG41Y2jd/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/5RtpfXg8x574bpNUQpAaoVNtEBfQg7c5h1u4tG41Y2jd/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/5RtpfXg8x574bpNUQpAaoVNtEBfQg7c5h1u4tG41Y2jd/process_trace.jsonl

### TRUMPPEPE / 5UKrpr9Xmdkge8UFfRiboiMbA9vwPxW5ARKbQ3Q6tcXS

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T09:43:30Z｜来源：data/gmgn_candidates_live_run/tokens/5UKrpr9Xmdkge8UFfRiboiMbA9vwPxW5ARKbQ3Q6tcXS/token_status.json｜字段：last_update
- 有证据：发现对象符号：TRUMPPEPE｜来源：data/gmgn_candidates_live_run/tokens/5UKrpr9Xmdkge8UFfRiboiMbA9vwPxW5ARKbQ3Q6tcXS/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/5UKrpr9Xmdkge8UFfRiboiMbA9vwPxW5ARKbQ3Q6tcXS/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/5UKrpr9Xmdkge8UFfRiboiMbA9vwPxW5ARKbQ3Q6tcXS/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/5UKrpr9Xmdkge8UFfRiboiMbA9vwPxW5ARKbQ3Q6tcXS/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/5UKrpr9Xmdkge8UFfRiboiMbA9vwPxW5ARKbQ3Q6tcXS/token_status.json；data/gmgn_candidates_live_run/wallet_structure/5UKrpr9Xmdkge8UFfRiboiMbA9vwPxW5ARKbQ3Q6tcXS/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/5UKrpr9Xmdkge8UFfRiboiMbA9vwPxW5ARKbQ3Q6tcXS/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/5UKrpr9Xmdkge8UFfRiboiMbA9vwPxW5ARKbQ3Q6tcXS/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/5UKrpr9Xmdkge8UFfRiboiMbA9vwPxW5ARKbQ3Q6tcXS/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/5UKrpr9Xmdkge8UFfRiboiMbA9vwPxW5ARKbQ3Q6tcXS/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/5UKrpr9Xmdkge8UFfRiboiMbA9vwPxW5ARKbQ3Q6tcXS/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/5UKrpr9Xmdkge8UFfRiboiMbA9vwPxW5ARKbQ3Q6tcXS/process_trace.jsonl

### RETARDPEPE / 5XXAtxZbxFqhLUe6Ho7VKwBDNdKy6VtWpGvKxvYhv2FK

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T21:36:04Z｜来源：data/gmgn_candidates_live_run/tokens/5XXAtxZbxFqhLUe6Ho7VKwBDNdKy6VtWpGvKxvYhv2FK/token_status.json｜字段：last_update
- 有证据：发现对象符号：RETARDPEPE｜来源：data/gmgn_candidates_live_run/tokens/5XXAtxZbxFqhLUe6Ho7VKwBDNdKy6VtWpGvKxvYhv2FK/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/5XXAtxZbxFqhLUe6Ho7VKwBDNdKy6VtWpGvKxvYhv2FK/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/5XXAtxZbxFqhLUe6Ho7VKwBDNdKy6VtWpGvKxvYhv2FK/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/5XXAtxZbxFqhLUe6Ho7VKwBDNdKy6VtWpGvKxvYhv2FK/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/5XXAtxZbxFqhLUe6Ho7VKwBDNdKy6VtWpGvKxvYhv2FK/token_status.json；data/gmgn_candidates_live_run/wallet_structure/5XXAtxZbxFqhLUe6Ho7VKwBDNdKy6VtWpGvKxvYhv2FK/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/5XXAtxZbxFqhLUe6Ho7VKwBDNdKy6VtWpGvKxvYhv2FK/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/5XXAtxZbxFqhLUe6Ho7VKwBDNdKy6VtWpGvKxvYhv2FK/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/5XXAtxZbxFqhLUe6Ho7VKwBDNdKy6VtWpGvKxvYhv2FK/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/5XXAtxZbxFqhLUe6Ho7VKwBDNdKy6VtWpGvKxvYhv2FK/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/5XXAtxZbxFqhLUe6Ho7VKwBDNdKy6VtWpGvKxvYhv2FK/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/5XXAtxZbxFqhLUe6Ho7VKwBDNdKy6VtWpGvKxvYhv2FK/process_trace.jsonl

### CHARITYDROP / 5oNQP9NSRspWy2qrpJexuvkX8DqZUW6TLNTZbHKypump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T19:30:17Z｜来源：data/gmgn_candidates_live_run/tokens/5oNQP9NSRspWy2qrpJexuvkX8DqZUW6TLNTZbHKypump/token_status.json｜字段：last_update
- 有证据：发现对象符号：CHARITYDROP｜来源：data/gmgn_candidates_live_run/tokens/5oNQP9NSRspWy2qrpJexuvkX8DqZUW6TLNTZbHKypump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/5oNQP9NSRspWy2qrpJexuvkX8DqZUW6TLNTZbHKypump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/5oNQP9NSRspWy2qrpJexuvkX8DqZUW6TLNTZbHKypump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/5oNQP9NSRspWy2qrpJexuvkX8DqZUW6TLNTZbHKypump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/5oNQP9NSRspWy2qrpJexuvkX8DqZUW6TLNTZbHKypump/token_status.json｜字段：current_state
- 有证据：钱包结构结论：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/5oNQP9NSRspWy2qrpJexuvkX8DqZUW6TLNTZbHKypump/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：钱包结构原因：早期钱包集中清仓，筹码控制权疑似向分发/对手盘转移；发现分发侧钱包 9 个；对手盘压力高，接盘/套牢筹码占比偏高｜来源：data/gmgn_candidates_live_run/wallet_structure/5oNQP9NSRspWy2qrpJexuvkX8DqZUW6TLNTZbHKypump/wallet_structure_decision.json｜字段：wallet_structure_reason
- 有证据：quote/security 权限：MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/5oNQP9NSRspWy2qrpJexuvkX8DqZUW6TLNTZbHKypump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 有证据：纸面退出原因：钱包结构触发纸面强制退出｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json｜字段：exit_reason
- 有证据：纸面退出时间：2026-05-02T18:48:46Z｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json｜字段：exit_time
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/5oNQP9NSRspWy2qrpJexuvkX8DqZUW6TLNTZbHKypump/token_status.json｜字段：current_state

#### 为什么失败
- 有证据：失败类型：STRUCTURE_WEAKENING｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl｜字段：failure_type
- 有证据：失败原因：钱包结构状态变为 WALLET_BLOCK，纸面阶段直接模拟退出｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl｜字段：failure_reason
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/5oNQP9NSRspWy2qrpJexuvkX8DqZUW6TLNTZbHKypump/token_status.json｜字段：current_state

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/5oNQP9NSRspWy2qrpJexuvkX8DqZUW6TLNTZbHKypump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/5oNQP9NSRspWy2qrpJexuvkX8DqZUW6TLNTZbHKypump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/5oNQP9NSRspWy2qrpJexuvkX8DqZUW6TLNTZbHKypump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/5oNQP9NSRspWy2qrpJexuvkX8DqZUW6TLNTZbHKypump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/5oNQP9NSRspWy2qrpJexuvkX8DqZUW6TLNTZbHKypump/process_trace.jsonl

### MOGRUMP / 619pqYDbUcNpCuobgg2Ed8sxeocfmGzwfHWsTCe2pump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/619pqYDbUcNpCuobgg2Ed8sxeocfmGzwfHWsTCe2pump/token_status.json｜字段：last_update
- 有证据：发现对象符号：MOGRUMP｜来源：data/gmgn_candidates_live_run/tokens/619pqYDbUcNpCuobgg2Ed8sxeocfmGzwfHWsTCe2pump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/619pqYDbUcNpCuobgg2Ed8sxeocfmGzwfHWsTCe2pump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / SIKK 信号仍为观察/预备层｜来源：data/gmgn_candidates_live_run/tokens/619pqYDbUcNpCuobgg2Ed8sxeocfmGzwfHWsTCe2pump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/619pqYDbUcNpCuobgg2Ed8sxeocfmGzwfHWsTCe2pump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/619pqYDbUcNpCuobgg2Ed8sxeocfmGzwfHWsTCe2pump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/619pqYDbUcNpCuobgg2Ed8sxeocfmGzwfHWsTCe2pump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/619pqYDbUcNpCuobgg2Ed8sxeocfmGzwfHWsTCe2pump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/619pqYDbUcNpCuobgg2Ed8sxeocfmGzwfHWsTCe2pump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/619pqYDbUcNpCuobgg2Ed8sxeocfmGzwfHWsTCe2pump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/619pqYDbUcNpCuobgg2Ed8sxeocfmGzwfHWsTCe2pump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/619pqYDbUcNpCuobgg2Ed8sxeocfmGzwfHWsTCe2pump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/619pqYDbUcNpCuobgg2Ed8sxeocfmGzwfHWsTCe2pump/process_trace.jsonl

### HORNY / 69HZnSz3XDHyTeBrrsn5NFbjpiryhHbYJZUGDx3QXH69

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T11:51:43Z｜来源：data/gmgn_candidates_live_run/tokens/69HZnSz3XDHyTeBrrsn5NFbjpiryhHbYJZUGDx3QXH69/token_status.json｜字段：last_update
- 有证据：发现对象符号：HORNY｜来源：data/gmgn_candidates_live_run/tokens/69HZnSz3XDHyTeBrrsn5NFbjpiryhHbYJZUGDx3QXH69/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/69HZnSz3XDHyTeBrrsn5NFbjpiryhHbYJZUGDx3QXH69/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/69HZnSz3XDHyTeBrrsn5NFbjpiryhHbYJZUGDx3QXH69/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/69HZnSz3XDHyTeBrrsn5NFbjpiryhHbYJZUGDx3QXH69/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/69HZnSz3XDHyTeBrrsn5NFbjpiryhHbYJZUGDx3QXH69/token_status.json；data/gmgn_candidates_live_run/wallet_structure/69HZnSz3XDHyTeBrrsn5NFbjpiryhHbYJZUGDx3QXH69/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/69HZnSz3XDHyTeBrrsn5NFbjpiryhHbYJZUGDx3QXH69/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/69HZnSz3XDHyTeBrrsn5NFbjpiryhHbYJZUGDx3QXH69/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/69HZnSz3XDHyTeBrrsn5NFbjpiryhHbYJZUGDx3QXH69/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/69HZnSz3XDHyTeBrrsn5NFbjpiryhHbYJZUGDx3QXH69/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/69HZnSz3XDHyTeBrrsn5NFbjpiryhHbYJZUGDx3QXH69/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/69HZnSz3XDHyTeBrrsn5NFbjpiryhHbYJZUGDx3QXH69/process_trace.jsonl

### SCAM / 6AVAUKa9uxQpruHZUinFECpXEh1usRVtzQWK8N2wpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T20:22:50Z｜来源：data/gmgn_candidates_live_run/tokens/6AVAUKa9uxQpruHZUinFECpXEh1usRVtzQWK8N2wpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：SCAM｜来源：data/gmgn_candidates_live_run/tokens/6AVAUKa9uxQpruHZUinFECpXEh1usRVtzQWK8N2wpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/6AVAUKa9uxQpruHZUinFECpXEh1usRVtzQWK8N2wpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/6AVAUKa9uxQpruHZUinFECpXEh1usRVtzQWK8N2wpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/6AVAUKa9uxQpruHZUinFECpXEh1usRVtzQWK8N2wpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/6AVAUKa9uxQpruHZUinFECpXEh1usRVtzQWK8N2wpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/6AVAUKa9uxQpruHZUinFECpXEh1usRVtzQWK8N2wpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/6AVAUKa9uxQpruHZUinFECpXEh1usRVtzQWK8N2wpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/6AVAUKa9uxQpruHZUinFECpXEh1usRVtzQWK8N2wpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/6AVAUKa9uxQpruHZUinFECpXEh1usRVtzQWK8N2wpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/6AVAUKa9uxQpruHZUinFECpXEh1usRVtzQWK8N2wpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/6AVAUKa9uxQpruHZUinFECpXEh1usRVtzQWK8N2wpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/6AVAUKa9uxQpruHZUinFECpXEh1usRVtzQWK8N2wpump/process_trace.jsonl

### HODLERS / 6P18kpmUZbm3YKeq7PqVyrxz1eEUmAUjqqMqrdWoTQjT

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T18:26:44Z｜来源：data/gmgn_candidates_live_run/tokens/6P18kpmUZbm3YKeq7PqVyrxz1eEUmAUjqqMqrdWoTQjT/token_status.json｜字段：last_update
- 有证据：发现对象符号：HODLERS｜来源：data/gmgn_candidates_live_run/tokens/6P18kpmUZbm3YKeq7PqVyrxz1eEUmAUjqqMqrdWoTQjT/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/6P18kpmUZbm3YKeq7PqVyrxz1eEUmAUjqqMqrdWoTQjT/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/6P18kpmUZbm3YKeq7PqVyrxz1eEUmAUjqqMqrdWoTQjT/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/6P18kpmUZbm3YKeq7PqVyrxz1eEUmAUjqqMqrdWoTQjT/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/6P18kpmUZbm3YKeq7PqVyrxz1eEUmAUjqqMqrdWoTQjT/token_status.json；data/gmgn_candidates_live_run/wallet_structure/6P18kpmUZbm3YKeq7PqVyrxz1eEUmAUjqqMqrdWoTQjT/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/6P18kpmUZbm3YKeq7PqVyrxz1eEUmAUjqqMqrdWoTQjT/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/6P18kpmUZbm3YKeq7PqVyrxz1eEUmAUjqqMqrdWoTQjT/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/6P18kpmUZbm3YKeq7PqVyrxz1eEUmAUjqqMqrdWoTQjT/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/6P18kpmUZbm3YKeq7PqVyrxz1eEUmAUjqqMqrdWoTQjT/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/6P18kpmUZbm3YKeq7PqVyrxz1eEUmAUjqqMqrdWoTQjT/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/6P18kpmUZbm3YKeq7PqVyrxz1eEUmAUjqqMqrdWoTQjT/process_trace.jsonl

### JPPEPE / 6SB6cyoYWQ31fcVHNFbZzbW8GZ4vJqLwrba4cicY6xai

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T17:22:17Z｜来源：data/gmgn_candidates_live_run/tokens/6SB6cyoYWQ31fcVHNFbZzbW8GZ4vJqLwrba4cicY6xai/token_status.json｜字段：last_update
- 有证据：发现对象符号：JPPEPE｜来源：data/gmgn_candidates_live_run/tokens/6SB6cyoYWQ31fcVHNFbZzbW8GZ4vJqLwrba4cicY6xai/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/6SB6cyoYWQ31fcVHNFbZzbW8GZ4vJqLwrba4cicY6xai/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/6SB6cyoYWQ31fcVHNFbZzbW8GZ4vJqLwrba4cicY6xai/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/6SB6cyoYWQ31fcVHNFbZzbW8GZ4vJqLwrba4cicY6xai/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/6SB6cyoYWQ31fcVHNFbZzbW8GZ4vJqLwrba4cicY6xai/token_status.json；data/gmgn_candidates_live_run/wallet_structure/6SB6cyoYWQ31fcVHNFbZzbW8GZ4vJqLwrba4cicY6xai/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/6SB6cyoYWQ31fcVHNFbZzbW8GZ4vJqLwrba4cicY6xai/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/6SB6cyoYWQ31fcVHNFbZzbW8GZ4vJqLwrba4cicY6xai/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/6SB6cyoYWQ31fcVHNFbZzbW8GZ4vJqLwrba4cicY6xai/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/6SB6cyoYWQ31fcVHNFbZzbW8GZ4vJqLwrba4cicY6xai/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/6SB6cyoYWQ31fcVHNFbZzbW8GZ4vJqLwrba4cicY6xai/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/6SB6cyoYWQ31fcVHNFbZzbW8GZ4vJqLwrba4cicY6xai/process_trace.jsonl

### Shrek / 6ixv7h9LQ8Vz4S9F4Ta8BWM7USaDapihZroDWSRBpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/6ixv7h9LQ8Vz4S9F4Ta8BWM7USaDapihZroDWSRBpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：Shrek｜来源：data/gmgn_candidates_live_run/tokens/6ixv7h9LQ8Vz4S9F4Ta8BWM7USaDapihZroDWSRBpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/6ixv7h9LQ8Vz4S9F4Ta8BWM7USaDapihZroDWSRBpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/6ixv7h9LQ8Vz4S9F4Ta8BWM7USaDapihZroDWSRBpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/6ixv7h9LQ8Vz4S9F4Ta8BWM7USaDapihZroDWSRBpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/6ixv7h9LQ8Vz4S9F4Ta8BWM7USaDapihZroDWSRBpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/6ixv7h9LQ8Vz4S9F4Ta8BWM7USaDapihZroDWSRBpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/6ixv7h9LQ8Vz4S9F4Ta8BWM7USaDapihZroDWSRBpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/6ixv7h9LQ8Vz4S9F4Ta8BWM7USaDapihZroDWSRBpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/6ixv7h9LQ8Vz4S9F4Ta8BWM7USaDapihZroDWSRBpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/6ixv7h9LQ8Vz4S9F4Ta8BWM7USaDapihZroDWSRBpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/6ixv7h9LQ8Vz4S9F4Ta8BWM7USaDapihZroDWSRBpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/6ixv7h9LQ8Vz4S9F4Ta8BWM7USaDapihZroDWSRBpump/process_trace.jsonl

### ROME / 6r9CBT6kYgC49CwcnsX4NNtZmdixxhbjBGAfnXhqpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T11:09:01Z｜来源：data/gmgn_candidates_live_run/tokens/6r9CBT6kYgC49CwcnsX4NNtZmdixxhbjBGAfnXhqpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：ROME｜来源：data/gmgn_candidates_live_run/tokens/6r9CBT6kYgC49CwcnsX4NNtZmdixxhbjBGAfnXhqpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/6r9CBT6kYgC49CwcnsX4NNtZmdixxhbjBGAfnXhqpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/6r9CBT6kYgC49CwcnsX4NNtZmdixxhbjBGAfnXhqpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/6r9CBT6kYgC49CwcnsX4NNtZmdixxhbjBGAfnXhqpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/6r9CBT6kYgC49CwcnsX4NNtZmdixxhbjBGAfnXhqpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/6r9CBT6kYgC49CwcnsX4NNtZmdixxhbjBGAfnXhqpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/6r9CBT6kYgC49CwcnsX4NNtZmdixxhbjBGAfnXhqpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/6r9CBT6kYgC49CwcnsX4NNtZmdixxhbjBGAfnXhqpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/6r9CBT6kYgC49CwcnsX4NNtZmdixxhbjBGAfnXhqpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/6r9CBT6kYgC49CwcnsX4NNtZmdixxhbjBGAfnXhqpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/6r9CBT6kYgC49CwcnsX4NNtZmdixxhbjBGAfnXhqpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/6r9CBT6kYgC49CwcnsX4NNtZmdixxhbjBGAfnXhqpump/process_trace.jsonl

### CLUTCH / 74CQjPmRd5A7MGc7Dnp1kgUNdPsYtB8FNbtak2Padpce

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/74CQjPmRd5A7MGc7Dnp1kgUNdPsYtB8FNbtak2Padpce/token_status.json｜字段：last_update
- 有证据：发现对象符号：CLUTCH｜来源：data/gmgn_candidates_live_run/tokens/74CQjPmRd5A7MGc7Dnp1kgUNdPsYtB8FNbtak2Padpce/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/74CQjPmRd5A7MGc7Dnp1kgUNdPsYtB8FNbtak2Padpce/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/74CQjPmRd5A7MGc7Dnp1kgUNdPsYtB8FNbtak2Padpce/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/74CQjPmRd5A7MGc7Dnp1kgUNdPsYtB8FNbtak2Padpce/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/74CQjPmRd5A7MGc7Dnp1kgUNdPsYtB8FNbtak2Padpce/token_status.json；data/gmgn_candidates_live_run/wallet_structure/74CQjPmRd5A7MGc7Dnp1kgUNdPsYtB8FNbtak2Padpce/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/74CQjPmRd5A7MGc7Dnp1kgUNdPsYtB8FNbtak2Padpce/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/74CQjPmRd5A7MGc7Dnp1kgUNdPsYtB8FNbtak2Padpce/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/74CQjPmRd5A7MGc7Dnp1kgUNdPsYtB8FNbtak2Padpce/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/74CQjPmRd5A7MGc7Dnp1kgUNdPsYtB8FNbtak2Padpce/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/74CQjPmRd5A7MGc7Dnp1kgUNdPsYtB8FNbtak2Padpce/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/74CQjPmRd5A7MGc7Dnp1kgUNdPsYtB8FNbtak2Padpce/process_trace.jsonl

### EVERYTHING / 773epH9k9PkjWxQt8NVwHPzti1ohchEmoC4JzdsYExbo

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T11:41:02Z｜来源：data/gmgn_candidates_live_run/tokens/773epH9k9PkjWxQt8NVwHPzti1ohchEmoC4JzdsYExbo/token_status.json｜字段：last_update
- 有证据：发现对象符号：EVERYTHING｜来源：data/gmgn_candidates_live_run/tokens/773epH9k9PkjWxQt8NVwHPzti1ohchEmoC4JzdsYExbo/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/773epH9k9PkjWxQt8NVwHPzti1ohchEmoC4JzdsYExbo/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/773epH9k9PkjWxQt8NVwHPzti1ohchEmoC4JzdsYExbo/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/773epH9k9PkjWxQt8NVwHPzti1ohchEmoC4JzdsYExbo/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/773epH9k9PkjWxQt8NVwHPzti1ohchEmoC4JzdsYExbo/token_status.json；data/gmgn_candidates_live_run/wallet_structure/773epH9k9PkjWxQt8NVwHPzti1ohchEmoC4JzdsYExbo/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/773epH9k9PkjWxQt8NVwHPzti1ohchEmoC4JzdsYExbo/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/773epH9k9PkjWxQt8NVwHPzti1ohchEmoC4JzdsYExbo/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/773epH9k9PkjWxQt8NVwHPzti1ohchEmoC4JzdsYExbo/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/773epH9k9PkjWxQt8NVwHPzti1ohchEmoC4JzdsYExbo/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/773epH9k9PkjWxQt8NVwHPzti1ohchEmoC4JzdsYExbo/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/773epH9k9PkjWxQt8NVwHPzti1ohchEmoC4JzdsYExbo/process_trace.jsonl

### RC / 79ogrGd2bhRS455phmsJo8iHYzBusqgLeyxF9Tf5pump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/79ogrGd2bhRS455phmsJo8iHYzBusqgLeyxF9Tf5pump/token_status.json｜字段：last_update
- 有证据：发现对象符号：RC｜来源：data/gmgn_candidates_live_run/tokens/79ogrGd2bhRS455phmsJo8iHYzBusqgLeyxF9Tf5pump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/79ogrGd2bhRS455phmsJo8iHYzBusqgLeyxF9Tf5pump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/79ogrGd2bhRS455phmsJo8iHYzBusqgLeyxF9Tf5pump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/79ogrGd2bhRS455phmsJo8iHYzBusqgLeyxF9Tf5pump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/79ogrGd2bhRS455phmsJo8iHYzBusqgLeyxF9Tf5pump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/79ogrGd2bhRS455phmsJo8iHYzBusqgLeyxF9Tf5pump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/79ogrGd2bhRS455phmsJo8iHYzBusqgLeyxF9Tf5pump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/79ogrGd2bhRS455phmsJo8iHYzBusqgLeyxF9Tf5pump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/79ogrGd2bhRS455phmsJo8iHYzBusqgLeyxF9Tf5pump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/79ogrGd2bhRS455phmsJo8iHYzBusqgLeyxF9Tf5pump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/79ogrGd2bhRS455phmsJo8iHYzBusqgLeyxF9Tf5pump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/79ogrGd2bhRS455phmsJo8iHYzBusqgLeyxF9Tf5pump/process_trace.jsonl

### PEPTA / 7WddhpM5mLMTyS16Dqeru1mUcoHetVVkh92zU8Tppump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/7WddhpM5mLMTyS16Dqeru1mUcoHetVVkh92zU8Tppump/token_status.json｜字段：last_update
- 有证据：发现对象符号：PEPTA｜来源：data/gmgn_candidates_live_run/tokens/7WddhpM5mLMTyS16Dqeru1mUcoHetVVkh92zU8Tppump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/7WddhpM5mLMTyS16Dqeru1mUcoHetVVkh92zU8Tppump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/7WddhpM5mLMTyS16Dqeru1mUcoHetVVkh92zU8Tppump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/7WddhpM5mLMTyS16Dqeru1mUcoHetVVkh92zU8Tppump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/7WddhpM5mLMTyS16Dqeru1mUcoHetVVkh92zU8Tppump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/7WddhpM5mLMTyS16Dqeru1mUcoHetVVkh92zU8Tppump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/7WddhpM5mLMTyS16Dqeru1mUcoHetVVkh92zU8Tppump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/7WddhpM5mLMTyS16Dqeru1mUcoHetVVkh92zU8Tppump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/7WddhpM5mLMTyS16Dqeru1mUcoHetVVkh92zU8Tppump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/7WddhpM5mLMTyS16Dqeru1mUcoHetVVkh92zU8Tppump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/7WddhpM5mLMTyS16Dqeru1mUcoHetVVkh92zU8Tppump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/7WddhpM5mLMTyS16Dqeru1mUcoHetVVkh92zU8Tppump/process_trace.jsonl

### WOLVERINE / 7soYuSPe1LaJ9V37W7ZGDB5Xwxi41LUWjRT3AEQGpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/7soYuSPe1LaJ9V37W7ZGDB5Xwxi41LUWjRT3AEQGpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：WOLVERINE｜来源：data/gmgn_candidates_live_run/tokens/7soYuSPe1LaJ9V37W7ZGDB5Xwxi41LUWjRT3AEQGpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/7soYuSPe1LaJ9V37W7ZGDB5Xwxi41LUWjRT3AEQGpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/7soYuSPe1LaJ9V37W7ZGDB5Xwxi41LUWjRT3AEQGpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/7soYuSPe1LaJ9V37W7ZGDB5Xwxi41LUWjRT3AEQGpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/7soYuSPe1LaJ9V37W7ZGDB5Xwxi41LUWjRT3AEQGpump/token_status.json｜字段：current_state
- 有证据：钱包结构结论：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/7soYuSPe1LaJ9V37W7ZGDB5Xwxi41LUWjRT3AEQGpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：钱包结构原因：发现分发侧钱包 10 个；对手盘压力高，接盘/套牢筹码占比偏高｜来源：data/gmgn_candidates_live_run/wallet_structure/7soYuSPe1LaJ9V37W7ZGDB5Xwxi41LUWjRT3AEQGpump/wallet_structure_decision.json｜字段：wallet_structure_reason
- 有证据：quote/security 权限：MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/7soYuSPe1LaJ9V37W7ZGDB5Xwxi41LUWjRT3AEQGpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 有证据：纸面退出原因：钱包结构触发纸面强制退出｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json｜字段：exit_reason
- 有证据：纸面退出时间：2026-05-02T21:26:03Z｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json｜字段：exit_time
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/7soYuSPe1LaJ9V37W7ZGDB5Xwxi41LUWjRT3AEQGpump/token_status.json｜字段：current_state

#### 为什么失败
- 有证据：失败类型：STRUCTURE_WEAKENING｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl｜字段：failure_type
- 有证据：失败原因：钱包结构状态变为 WALLET_BLOCK，纸面阶段直接模拟退出｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl｜字段：failure_reason
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/7soYuSPe1LaJ9V37W7ZGDB5Xwxi41LUWjRT3AEQGpump/token_status.json｜字段：current_state

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/7soYuSPe1LaJ9V37W7ZGDB5Xwxi41LUWjRT3AEQGpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/7soYuSPe1LaJ9V37W7ZGDB5Xwxi41LUWjRT3AEQGpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/7soYuSPe1LaJ9V37W7ZGDB5Xwxi41LUWjRT3AEQGpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/7soYuSPe1LaJ9V37W7ZGDB5Xwxi41LUWjRT3AEQGpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/7soYuSPe1LaJ9V37W7ZGDB5Xwxi41LUWjRT3AEQGpump/process_trace.jsonl

### LOKN / 7thaUtsPjcef9hd5p34PEkvr8wTuF63LhmPY7a3Vpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/7thaUtsPjcef9hd5p34PEkvr8wTuF63LhmPY7a3Vpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：LOKN｜来源：data/gmgn_candidates_live_run/tokens/7thaUtsPjcef9hd5p34PEkvr8wTuF63LhmPY7a3Vpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/7thaUtsPjcef9hd5p34PEkvr8wTuF63LhmPY7a3Vpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/7thaUtsPjcef9hd5p34PEkvr8wTuF63LhmPY7a3Vpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/7thaUtsPjcef9hd5p34PEkvr8wTuF63LhmPY7a3Vpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/7thaUtsPjcef9hd5p34PEkvr8wTuF63LhmPY7a3Vpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/7thaUtsPjcef9hd5p34PEkvr8wTuF63LhmPY7a3Vpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/7thaUtsPjcef9hd5p34PEkvr8wTuF63LhmPY7a3Vpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/7thaUtsPjcef9hd5p34PEkvr8wTuF63LhmPY7a3Vpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/7thaUtsPjcef9hd5p34PEkvr8wTuF63LhmPY7a3Vpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/7thaUtsPjcef9hd5p34PEkvr8wTuF63LhmPY7a3Vpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/7thaUtsPjcef9hd5p34PEkvr8wTuF63LhmPY7a3Vpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/7thaUtsPjcef9hd5p34PEkvr8wTuF63LhmPY7a3Vpump/process_trace.jsonl

### May4th / 7wC7z6FbueVpDhb724xg7VHvsLwMPuQgwvHUfMbq5Z89

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T19:51:09Z｜来源：data/gmgn_candidates_live_run/tokens/7wC7z6FbueVpDhb724xg7VHvsLwMPuQgwvHUfMbq5Z89/token_status.json｜字段：last_update
- 有证据：发现对象符号：May4th｜来源：data/gmgn_candidates_live_run/tokens/7wC7z6FbueVpDhb724xg7VHvsLwMPuQgwvHUfMbq5Z89/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/7wC7z6FbueVpDhb724xg7VHvsLwMPuQgwvHUfMbq5Z89/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/7wC7z6FbueVpDhb724xg7VHvsLwMPuQgwvHUfMbq5Z89/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/7wC7z6FbueVpDhb724xg7VHvsLwMPuQgwvHUfMbq5Z89/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/7wC7z6FbueVpDhb724xg7VHvsLwMPuQgwvHUfMbq5Z89/token_status.json；data/gmgn_candidates_live_run/wallet_structure/7wC7z6FbueVpDhb724xg7VHvsLwMPuQgwvHUfMbq5Z89/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/7wC7z6FbueVpDhb724xg7VHvsLwMPuQgwvHUfMbq5Z89/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/7wC7z6FbueVpDhb724xg7VHvsLwMPuQgwvHUfMbq5Z89/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/7wC7z6FbueVpDhb724xg7VHvsLwMPuQgwvHUfMbq5Z89/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/7wC7z6FbueVpDhb724xg7VHvsLwMPuQgwvHUfMbq5Z89/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/7wC7z6FbueVpDhb724xg7VHvsLwMPuQgwvHUfMbq5Z89/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/7wC7z6FbueVpDhb724xg7VHvsLwMPuQgwvHUfMbq5Z89/process_trace.jsonl

### TrumpPepe / 7xHxokqd3T9qNhZRYDWRBQTThyYUkLxEDkYegdFQaTT7

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:07:09Z｜来源：data/gmgn_candidates_live_run/tokens/7xHxokqd3T9qNhZRYDWRBQTThyYUkLxEDkYegdFQaTT7/token_status.json｜字段：last_update
- 有证据：发现对象符号：TrumpPepe｜来源：data/gmgn_candidates_live_run/tokens/7xHxokqd3T9qNhZRYDWRBQTThyYUkLxEDkYegdFQaTT7/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/7xHxokqd3T9qNhZRYDWRBQTThyYUkLxEDkYegdFQaTT7/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/7xHxokqd3T9qNhZRYDWRBQTThyYUkLxEDkYegdFQaTT7/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/7xHxokqd3T9qNhZRYDWRBQTThyYUkLxEDkYegdFQaTT7/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/7xHxokqd3T9qNhZRYDWRBQTThyYUkLxEDkYegdFQaTT7/token_status.json；data/gmgn_candidates_live_run/wallet_structure/7xHxokqd3T9qNhZRYDWRBQTThyYUkLxEDkYegdFQaTT7/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/7xHxokqd3T9qNhZRYDWRBQTThyYUkLxEDkYegdFQaTT7/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/7xHxokqd3T9qNhZRYDWRBQTThyYUkLxEDkYegdFQaTT7/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/7xHxokqd3T9qNhZRYDWRBQTThyYUkLxEDkYegdFQaTT7/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/7xHxokqd3T9qNhZRYDWRBQTThyYUkLxEDkYegdFQaTT7/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/7xHxokqd3T9qNhZRYDWRBQTThyYUkLxEDkYegdFQaTT7/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/7xHxokqd3T9qNhZRYDWRBQTThyYUkLxEDkYegdFQaTT7/process_trace.jsonl

### PEPEAIR / 7xbzewm84HyvJR22hzfQe2sbJYH7ZR7hw4LRiUUsywTb

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/7xbzewm84HyvJR22hzfQe2sbJYH7ZR7hw4LRiUUsywTb/token_status.json｜字段：last_update
- 有证据：发现对象符号：PEPEAIR｜来源：data/gmgn_candidates_live_run/tokens/7xbzewm84HyvJR22hzfQe2sbJYH7ZR7hw4LRiUUsywTb/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/7xbzewm84HyvJR22hzfQe2sbJYH7ZR7hw4LRiUUsywTb/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/7xbzewm84HyvJR22hzfQe2sbJYH7ZR7hw4LRiUUsywTb/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/7xbzewm84HyvJR22hzfQe2sbJYH7ZR7hw4LRiUUsywTb/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/7xbzewm84HyvJR22hzfQe2sbJYH7ZR7hw4LRiUUsywTb/token_status.json；data/gmgn_candidates_live_run/wallet_structure/7xbzewm84HyvJR22hzfQe2sbJYH7ZR7hw4LRiUUsywTb/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/7xbzewm84HyvJR22hzfQe2sbJYH7ZR7hw4LRiUUsywTb/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/7xbzewm84HyvJR22hzfQe2sbJYH7ZR7hw4LRiUUsywTb/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/7xbzewm84HyvJR22hzfQe2sbJYH7ZR7hw4LRiUUsywTb/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/7xbzewm84HyvJR22hzfQe2sbJYH7ZR7hw4LRiUUsywTb/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/7xbzewm84HyvJR22hzfQe2sbJYH7ZR7hw4LRiUUsywTb/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/7xbzewm84HyvJR22hzfQe2sbJYH7ZR7hw4LRiUUsywTb/process_trace.jsonl

### Mogman / 87i4TeZvP2Z4xM1KJpfSutQy34mkHnwgnR5bt8Q2pump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T21:04:41Z｜来源：data/gmgn_candidates_live_run/tokens/87i4TeZvP2Z4xM1KJpfSutQy34mkHnwgnR5bt8Q2pump/token_status.json｜字段：last_update
- 有证据：发现对象符号：Mogman｜来源：data/gmgn_candidates_live_run/tokens/87i4TeZvP2Z4xM1KJpfSutQy34mkHnwgnR5bt8Q2pump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/87i4TeZvP2Z4xM1KJpfSutQy34mkHnwgnR5bt8Q2pump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/87i4TeZvP2Z4xM1KJpfSutQy34mkHnwgnR5bt8Q2pump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/87i4TeZvP2Z4xM1KJpfSutQy34mkHnwgnR5bt8Q2pump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/87i4TeZvP2Z4xM1KJpfSutQy34mkHnwgnR5bt8Q2pump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/87i4TeZvP2Z4xM1KJpfSutQy34mkHnwgnR5bt8Q2pump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/87i4TeZvP2Z4xM1KJpfSutQy34mkHnwgnR5bt8Q2pump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/87i4TeZvP2Z4xM1KJpfSutQy34mkHnwgnR5bt8Q2pump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/87i4TeZvP2Z4xM1KJpfSutQy34mkHnwgnR5bt8Q2pump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/87i4TeZvP2Z4xM1KJpfSutQy34mkHnwgnR5bt8Q2pump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/87i4TeZvP2Z4xM1KJpfSutQy34mkHnwgnR5bt8Q2pump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/87i4TeZvP2Z4xM1KJpfSutQy34mkHnwgnR5bt8Q2pump/process_trace.jsonl

### OMOGGLE / 8MjmLaX4q7xJqHSqLrt2v6sXBgJe97muaXmi7qdepump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/8MjmLaX4q7xJqHSqLrt2v6sXBgJe97muaXmi7qdepump/token_status.json｜字段：last_update
- 有证据：发现对象符号：OMOGGLE｜来源：data/gmgn_candidates_live_run/tokens/8MjmLaX4q7xJqHSqLrt2v6sXBgJe97muaXmi7qdepump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/8MjmLaX4q7xJqHSqLrt2v6sXBgJe97muaXmi7qdepump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/8MjmLaX4q7xJqHSqLrt2v6sXBgJe97muaXmi7qdepump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/8MjmLaX4q7xJqHSqLrt2v6sXBgJe97muaXmi7qdepump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/8MjmLaX4q7xJqHSqLrt2v6sXBgJe97muaXmi7qdepump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/8MjmLaX4q7xJqHSqLrt2v6sXBgJe97muaXmi7qdepump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/8MjmLaX4q7xJqHSqLrt2v6sXBgJe97muaXmi7qdepump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/8MjmLaX4q7xJqHSqLrt2v6sXBgJe97muaXmi7qdepump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/8MjmLaX4q7xJqHSqLrt2v6sXBgJe97muaXmi7qdepump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/8MjmLaX4q7xJqHSqLrt2v6sXBgJe97muaXmi7qdepump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/8MjmLaX4q7xJqHSqLrt2v6sXBgJe97muaXmi7qdepump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/8MjmLaX4q7xJqHSqLrt2v6sXBgJe97muaXmi7qdepump/process_trace.jsonl

### Scribbli / 8c3JdTcEqy9XdUJ36NAns7XVDfh356nWxvwcMYKNpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/8c3JdTcEqy9XdUJ36NAns7XVDfh356nWxvwcMYKNpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：Scribbli｜来源：data/gmgn_candidates_live_run/tokens/8c3JdTcEqy9XdUJ36NAns7XVDfh356nWxvwcMYKNpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/8c3JdTcEqy9XdUJ36NAns7XVDfh356nWxvwcMYKNpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/8c3JdTcEqy9XdUJ36NAns7XVDfh356nWxvwcMYKNpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/8c3JdTcEqy9XdUJ36NAns7XVDfh356nWxvwcMYKNpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/8c3JdTcEqy9XdUJ36NAns7XVDfh356nWxvwcMYKNpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/8c3JdTcEqy9XdUJ36NAns7XVDfh356nWxvwcMYKNpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/8c3JdTcEqy9XdUJ36NAns7XVDfh356nWxvwcMYKNpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/8c3JdTcEqy9XdUJ36NAns7XVDfh356nWxvwcMYKNpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/8c3JdTcEqy9XdUJ36NAns7XVDfh356nWxvwcMYKNpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/8c3JdTcEqy9XdUJ36NAns7XVDfh356nWxvwcMYKNpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/8c3JdTcEqy9XdUJ36NAns7XVDfh356nWxvwcMYKNpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/8c3JdTcEqy9XdUJ36NAns7XVDfh356nWxvwcMYKNpump/process_trace.jsonl

### GMEBAY / 8n58q3pUr7VK3jhCXfx75rPLiygRWLuSSiyxP7aapump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T08:49:50Z｜来源：data/gmgn_candidates_live_run/tokens/8n58q3pUr7VK3jhCXfx75rPLiygRWLuSSiyxP7aapump/token_status.json｜字段：last_update
- 有证据：发现对象符号：GMEBAY｜来源：data/gmgn_candidates_live_run/tokens/8n58q3pUr7VK3jhCXfx75rPLiygRWLuSSiyxP7aapump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/8n58q3pUr7VK3jhCXfx75rPLiygRWLuSSiyxP7aapump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/8n58q3pUr7VK3jhCXfx75rPLiygRWLuSSiyxP7aapump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/8n58q3pUr7VK3jhCXfx75rPLiygRWLuSSiyxP7aapump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/8n58q3pUr7VK3jhCXfx75rPLiygRWLuSSiyxP7aapump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/8n58q3pUr7VK3jhCXfx75rPLiygRWLuSSiyxP7aapump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/8n58q3pUr7VK3jhCXfx75rPLiygRWLuSSiyxP7aapump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/8n58q3pUr7VK3jhCXfx75rPLiygRWLuSSiyxP7aapump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/8n58q3pUr7VK3jhCXfx75rPLiygRWLuSSiyxP7aapump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/8n58q3pUr7VK3jhCXfx75rPLiygRWLuSSiyxP7aapump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/8n58q3pUr7VK3jhCXfx75rPLiygRWLuSSiyxP7aapump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/8n58q3pUr7VK3jhCXfx75rPLiygRWLuSSiyxP7aapump/process_trace.jsonl

### MINTY / 8r6gy6Cu1tEksgduBtrR3jDXVFPszQcwoYBB8ha6tbBL

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T07:18:10Z｜来源：data/gmgn_candidates_live_run/tokens/8r6gy6Cu1tEksgduBtrR3jDXVFPszQcwoYBB8ha6tbBL/token_status.json｜字段：last_update
- 有证据：发现对象符号：MINTY｜来源：data/gmgn_candidates_live_run/tokens/8r6gy6Cu1tEksgduBtrR3jDXVFPszQcwoYBB8ha6tbBL/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/8r6gy6Cu1tEksgduBtrR3jDXVFPszQcwoYBB8ha6tbBL/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/8r6gy6Cu1tEksgduBtrR3jDXVFPszQcwoYBB8ha6tbBL/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/8r6gy6Cu1tEksgduBtrR3jDXVFPszQcwoYBB8ha6tbBL/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/8r6gy6Cu1tEksgduBtrR3jDXVFPszQcwoYBB8ha6tbBL/token_status.json；data/gmgn_candidates_live_run/wallet_structure/8r6gy6Cu1tEksgduBtrR3jDXVFPszQcwoYBB8ha6tbBL/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/8r6gy6Cu1tEksgduBtrR3jDXVFPszQcwoYBB8ha6tbBL/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/8r6gy6Cu1tEksgduBtrR3jDXVFPszQcwoYBB8ha6tbBL/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/8r6gy6Cu1tEksgduBtrR3jDXVFPszQcwoYBB8ha6tbBL/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/8r6gy6Cu1tEksgduBtrR3jDXVFPszQcwoYBB8ha6tbBL/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/8r6gy6Cu1tEksgduBtrR3jDXVFPszQcwoYBB8ha6tbBL/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/8r6gy6Cu1tEksgduBtrR3jDXVFPszQcwoYBB8ha6tbBL/process_trace.jsonl

### WCUP / 8uyt2M978pnk1D78ixtvyERq73aGHWDP7HYx7W1qpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T13:54:08Z｜来源：data/gmgn_candidates_live_run/tokens/8uyt2M978pnk1D78ixtvyERq73aGHWDP7HYx7W1qpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：WCUP｜来源：data/gmgn_candidates_live_run/tokens/8uyt2M978pnk1D78ixtvyERq73aGHWDP7HYx7W1qpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/8uyt2M978pnk1D78ixtvyERq73aGHWDP7HYx7W1qpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/8uyt2M978pnk1D78ixtvyERq73aGHWDP7HYx7W1qpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/8uyt2M978pnk1D78ixtvyERq73aGHWDP7HYx7W1qpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/8uyt2M978pnk1D78ixtvyERq73aGHWDP7HYx7W1qpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/8uyt2M978pnk1D78ixtvyERq73aGHWDP7HYx7W1qpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/8uyt2M978pnk1D78ixtvyERq73aGHWDP7HYx7W1qpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/8uyt2M978pnk1D78ixtvyERq73aGHWDP7HYx7W1qpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/8uyt2M978pnk1D78ixtvyERq73aGHWDP7HYx7W1qpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/8uyt2M978pnk1D78ixtvyERq73aGHWDP7HYx7W1qpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/8uyt2M978pnk1D78ixtvyERq73aGHWDP7HYx7W1qpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/8uyt2M978pnk1D78ixtvyERq73aGHWDP7HYx7W1qpump/process_trace.jsonl

### Points / 8vvjTTH1SDqYXhZJ6axBoc5NT8LBNfaNa9tmRqtXpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T13:54:08Z｜来源：data/gmgn_candidates_live_run/tokens/8vvjTTH1SDqYXhZJ6axBoc5NT8LBNfaNa9tmRqtXpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：Points｜来源：data/gmgn_candidates_live_run/tokens/8vvjTTH1SDqYXhZJ6axBoc5NT8LBNfaNa9tmRqtXpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/8vvjTTH1SDqYXhZJ6axBoc5NT8LBNfaNa9tmRqtXpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/8vvjTTH1SDqYXhZJ6axBoc5NT8LBNfaNa9tmRqtXpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/8vvjTTH1SDqYXhZJ6axBoc5NT8LBNfaNa9tmRqtXpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/8vvjTTH1SDqYXhZJ6axBoc5NT8LBNfaNa9tmRqtXpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/8vvjTTH1SDqYXhZJ6axBoc5NT8LBNfaNa9tmRqtXpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/8vvjTTH1SDqYXhZJ6axBoc5NT8LBNfaNa9tmRqtXpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/8vvjTTH1SDqYXhZJ6axBoc5NT8LBNfaNa9tmRqtXpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/8vvjTTH1SDqYXhZJ6axBoc5NT8LBNfaNa9tmRqtXpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/8vvjTTH1SDqYXhZJ6axBoc5NT8LBNfaNa9tmRqtXpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/8vvjTTH1SDqYXhZJ6axBoc5NT8LBNfaNa9tmRqtXpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/8vvjTTH1SDqYXhZJ6axBoc5NT8LBNfaNa9tmRqtXpump/process_trace.jsonl

### Codex / 93uoNYX96BvG9RSSwvD6k9w6sXF4wsgTx1Rc84YSpump

- 当前状态：BLOCKED
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/93uoNYX96BvG9RSSwvD6k9w6sXF4wsgTx1Rc84YSpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：Codex｜来源：data/gmgn_candidates_live_run/tokens/93uoNYX96BvG9RSSwvD6k9w6sXF4wsgTx1Rc84YSpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：BLOCKED｜来源：data/gmgn_candidates_live_run/tokens/93uoNYX96BvG9RSSwvD6k9w6sXF4wsgTx1Rc84YSpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：BLOCKED / 吸筹窗口 invalid，进入风险阻断观察｜来源：data/gmgn_candidates_live_run/tokens/93uoNYX96BvG9RSSwvD6k9w6sXF4wsgTx1Rc84YSpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/93uoNYX96BvG9RSSwvD6k9w6sXF4wsgTx1Rc84YSpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 有证据：当前状态：BLOCKED｜来源：data/gmgn_candidates_live_run/tokens/93uoNYX96BvG9RSSwvD6k9w6sXF4wsgTx1Rc84YSpump/token_status.json｜字段：current_state
- 有证据：钱包结构结论：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/93uoNYX96BvG9RSSwvD6k9w6sXF4wsgTx1Rc84YSpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：quote/security 权限：MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/93uoNYX96BvG9RSSwvD6k9w6sXF4wsgTx1Rc84YSpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：BLOCKED / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/93uoNYX96BvG9RSSwvD6k9w6sXF4wsgTx1Rc84YSpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/93uoNYX96BvG9RSSwvD6k9w6sXF4wsgTx1Rc84YSpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/93uoNYX96BvG9RSSwvD6k9w6sXF4wsgTx1Rc84YSpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/93uoNYX96BvG9RSSwvD6k9w6sXF4wsgTx1Rc84YSpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/93uoNYX96BvG9RSSwvD6k9w6sXF4wsgTx1Rc84YSpump/process_trace.jsonl

### APE  / 95QtdngA6rmai8N5pVrj92JVvK9si6mPTiZ1zTFwbrrr

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T21:46:26Z｜来源：data/gmgn_candidates_live_run/tokens/95QtdngA6rmai8N5pVrj92JVvK9si6mPTiZ1zTFwbrrr/token_status.json｜字段：last_update
- 有证据：发现对象符号：APE ｜来源：data/gmgn_candidates_live_run/tokens/95QtdngA6rmai8N5pVrj92JVvK9si6mPTiZ1zTFwbrrr/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/95QtdngA6rmai8N5pVrj92JVvK9si6mPTiZ1zTFwbrrr/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/95QtdngA6rmai8N5pVrj92JVvK9si6mPTiZ1zTFwbrrr/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/95QtdngA6rmai8N5pVrj92JVvK9si6mPTiZ1zTFwbrrr/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/95QtdngA6rmai8N5pVrj92JVvK9si6mPTiZ1zTFwbrrr/token_status.json；data/gmgn_candidates_live_run/wallet_structure/95QtdngA6rmai8N5pVrj92JVvK9si6mPTiZ1zTFwbrrr/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/95QtdngA6rmai8N5pVrj92JVvK9si6mPTiZ1zTFwbrrr/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/95QtdngA6rmai8N5pVrj92JVvK9si6mPTiZ1zTFwbrrr/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/95QtdngA6rmai8N5pVrj92JVvK9si6mPTiZ1zTFwbrrr/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/95QtdngA6rmai8N5pVrj92JVvK9si6mPTiZ1zTFwbrrr/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/95QtdngA6rmai8N5pVrj92JVvK9si6mPTiZ1zTFwbrrr/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/95QtdngA6rmai8N5pVrj92JVvK9si6mPTiZ1zTFwbrrr/process_trace.jsonl

### USDBC / 96HTFKXidMzhT39bpsD3ogf6GXhwyvXctDMMtpqBpump

- 当前状态：DISCOVERED
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T07:07:39Z｜来源：data/gmgn_candidates_live_run/tokens/96HTFKXidMzhT39bpsD3ogf6GXhwyvXctDMMtpqBpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：USDBC｜来源：data/gmgn_candidates_live_run/tokens/96HTFKXidMzhT39bpsD3ogf6GXhwyvXctDMMtpqBpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：DISCOVERED｜来源：data/gmgn_candidates_live_run/tokens/96HTFKXidMzhT39bpsD3ogf6GXhwyvXctDMMtpqBpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：DISCOVERED / GMGN 新币筛选进入候选池｜来源：data/gmgn_candidates_live_run/tokens/96HTFKXidMzhT39bpsD3ogf6GXhwyvXctDMMtpqBpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/96HTFKXidMzhT39bpsD3ogf6GXhwyvXctDMMtpqBpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/96HTFKXidMzhT39bpsD3ogf6GXhwyvXctDMMtpqBpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/96HTFKXidMzhT39bpsD3ogf6GXhwyvXctDMMtpqBpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/96HTFKXidMzhT39bpsD3ogf6GXhwyvXctDMMtpqBpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：DISCOVERED / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/96HTFKXidMzhT39bpsD3ogf6GXhwyvXctDMMtpqBpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/96HTFKXidMzhT39bpsD3ogf6GXhwyvXctDMMtpqBpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/96HTFKXidMzhT39bpsD3ogf6GXhwyvXctDMMtpqBpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/96HTFKXidMzhT39bpsD3ogf6GXhwyvXctDMMtpqBpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/96HTFKXidMzhT39bpsD3ogf6GXhwyvXctDMMtpqBpump/process_trace.jsonl

### UNIPUMP / 9KrdYnHHrsWYpWMxyzbmmrjcXRr7ERWpB3byNeb1pump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/9KrdYnHHrsWYpWMxyzbmmrjcXRr7ERWpB3byNeb1pump/token_status.json｜字段：last_update
- 有证据：发现对象符号：UNIPUMP｜来源：data/gmgn_candidates_live_run/tokens/9KrdYnHHrsWYpWMxyzbmmrjcXRr7ERWpB3byNeb1pump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/9KrdYnHHrsWYpWMxyzbmmrjcXRr7ERWpB3byNeb1pump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/9KrdYnHHrsWYpWMxyzbmmrjcXRr7ERWpB3byNeb1pump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/9KrdYnHHrsWYpWMxyzbmmrjcXRr7ERWpB3byNeb1pump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/9KrdYnHHrsWYpWMxyzbmmrjcXRr7ERWpB3byNeb1pump/token_status.json｜字段：current_state
- 有证据：钱包结构结论：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/9KrdYnHHrsWYpWMxyzbmmrjcXRr7ERWpB3byNeb1pump/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：钱包结构原因：发现分发侧钱包 4 个；对手盘压力高，接盘/套牢筹码占比偏高｜来源：data/gmgn_candidates_live_run/wallet_structure/9KrdYnHHrsWYpWMxyzbmmrjcXRr7ERWpB3byNeb1pump/wallet_structure_decision.json｜字段：wallet_structure_reason
- 有证据：quote/security 权限：MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/9KrdYnHHrsWYpWMxyzbmmrjcXRr7ERWpB3byNeb1pump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 有证据：纸面退出原因：钱包结构触发纸面强制退出｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json｜字段：exit_reason
- 有证据：纸面退出时间：2026-05-02T18:38:16Z｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json｜字段：exit_time
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/9KrdYnHHrsWYpWMxyzbmmrjcXRr7ERWpB3byNeb1pump/token_status.json｜字段：current_state

#### 为什么失败
- 有证据：失败类型：STRUCTURE_WEAKENING｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl｜字段：failure_type
- 有证据：失败原因：钱包结构状态变为 WALLET_BLOCK，纸面阶段直接模拟退出｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl｜字段：failure_reason
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/9KrdYnHHrsWYpWMxyzbmmrjcXRr7ERWpB3byNeb1pump/token_status.json｜字段：current_state

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/9KrdYnHHrsWYpWMxyzbmmrjcXRr7ERWpB3byNeb1pump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/9KrdYnHHrsWYpWMxyzbmmrjcXRr7ERWpB3byNeb1pump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/9KrdYnHHrsWYpWMxyzbmmrjcXRr7ERWpB3byNeb1pump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/9KrdYnHHrsWYpWMxyzbmmrjcXRr7ERWpB3byNeb1pump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/9KrdYnHHrsWYpWMxyzbmmrjcXRr7ERWpB3byNeb1pump/process_trace.jsonl

### CHUDMAN / 9RZUk7Yf767NZiLjz4ZsatdBe4Ai8KBv4HhVFJaBDzWC

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:07:09Z｜来源：data/gmgn_candidates_live_run/tokens/9RZUk7Yf767NZiLjz4ZsatdBe4Ai8KBv4HhVFJaBDzWC/token_status.json｜字段：last_update
- 有证据：发现对象符号：CHUDMAN｜来源：data/gmgn_candidates_live_run/tokens/9RZUk7Yf767NZiLjz4ZsatdBe4Ai8KBv4HhVFJaBDzWC/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/9RZUk7Yf767NZiLjz4ZsatdBe4Ai8KBv4HhVFJaBDzWC/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/9RZUk7Yf767NZiLjz4ZsatdBe4Ai8KBv4HhVFJaBDzWC/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/9RZUk7Yf767NZiLjz4ZsatdBe4Ai8KBv4HhVFJaBDzWC/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/9RZUk7Yf767NZiLjz4ZsatdBe4Ai8KBv4HhVFJaBDzWC/token_status.json；data/gmgn_candidates_live_run/wallet_structure/9RZUk7Yf767NZiLjz4ZsatdBe4Ai8KBv4HhVFJaBDzWC/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/9RZUk7Yf767NZiLjz4ZsatdBe4Ai8KBv4HhVFJaBDzWC/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/9RZUk7Yf767NZiLjz4ZsatdBe4Ai8KBv4HhVFJaBDzWC/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/9RZUk7Yf767NZiLjz4ZsatdBe4Ai8KBv4HhVFJaBDzWC/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/9RZUk7Yf767NZiLjz4ZsatdBe4Ai8KBv4HhVFJaBDzWC/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/9RZUk7Yf767NZiLjz4ZsatdBe4Ai8KBv4HhVFJaBDzWC/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/9RZUk7Yf767NZiLjz4ZsatdBe4Ai8KBv4HhVFJaBDzWC/process_trace.jsonl

### DARIO / 9SqUgFAC6td5oXUTJbpBxE4HDQnrGLa9JxcSbBpjpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T13:54:08Z｜来源：data/gmgn_candidates_live_run/tokens/9SqUgFAC6td5oXUTJbpBxE4HDQnrGLa9JxcSbBpjpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：DARIO｜来源：data/gmgn_candidates_live_run/tokens/9SqUgFAC6td5oXUTJbpBxE4HDQnrGLa9JxcSbBpjpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/9SqUgFAC6td5oXUTJbpBxE4HDQnrGLa9JxcSbBpjpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/9SqUgFAC6td5oXUTJbpBxE4HDQnrGLa9JxcSbBpjpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/9SqUgFAC6td5oXUTJbpBxE4HDQnrGLa9JxcSbBpjpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/9SqUgFAC6td5oXUTJbpBxE4HDQnrGLa9JxcSbBpjpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/9SqUgFAC6td5oXUTJbpBxE4HDQnrGLa9JxcSbBpjpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/9SqUgFAC6td5oXUTJbpBxE4HDQnrGLa9JxcSbBpjpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/9SqUgFAC6td5oXUTJbpBxE4HDQnrGLa9JxcSbBpjpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/9SqUgFAC6td5oXUTJbpBxE4HDQnrGLa9JxcSbBpjpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/9SqUgFAC6td5oXUTJbpBxE4HDQnrGLa9JxcSbBpjpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/9SqUgFAC6td5oXUTJbpBxE4HDQnrGLa9JxcSbBpjpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/9SqUgFAC6td5oXUTJbpBxE4HDQnrGLa9JxcSbBpjpump/process_trace.jsonl

### MOGMAN / 9gBzMZ1oJ9wDTvzVrhaA7tKMmtWqg9SEmc1UuBPbpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/9gBzMZ1oJ9wDTvzVrhaA7tKMmtWqg9SEmc1UuBPbpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：MOGMAN｜来源：data/gmgn_candidates_live_run/tokens/9gBzMZ1oJ9wDTvzVrhaA7tKMmtWqg9SEmc1UuBPbpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/9gBzMZ1oJ9wDTvzVrhaA7tKMmtWqg9SEmc1UuBPbpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/9gBzMZ1oJ9wDTvzVrhaA7tKMmtWqg9SEmc1UuBPbpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/9gBzMZ1oJ9wDTvzVrhaA7tKMmtWqg9SEmc1UuBPbpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/9gBzMZ1oJ9wDTvzVrhaA7tKMmtWqg9SEmc1UuBPbpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/9gBzMZ1oJ9wDTvzVrhaA7tKMmtWqg9SEmc1UuBPbpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/9gBzMZ1oJ9wDTvzVrhaA7tKMmtWqg9SEmc1UuBPbpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/9gBzMZ1oJ9wDTvzVrhaA7tKMmtWqg9SEmc1UuBPbpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/9gBzMZ1oJ9wDTvzVrhaA7tKMmtWqg9SEmc1UuBPbpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/9gBzMZ1oJ9wDTvzVrhaA7tKMmtWqg9SEmc1UuBPbpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/9gBzMZ1oJ9wDTvzVrhaA7tKMmtWqg9SEmc1UuBPbpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/9gBzMZ1oJ9wDTvzVrhaA7tKMmtWqg9SEmc1UuBPbpump/process_trace.jsonl

### PEPX / 9qy89gnSE6HkPPFigfJPWppuLsL3hTpE7HR3YE4Qpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/9qy89gnSE6HkPPFigfJPWppuLsL3hTpE7HR3YE4Qpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：PEPX｜来源：data/gmgn_candidates_live_run/tokens/9qy89gnSE6HkPPFigfJPWppuLsL3hTpE7HR3YE4Qpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/9qy89gnSE6HkPPFigfJPWppuLsL3hTpE7HR3YE4Qpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/9qy89gnSE6HkPPFigfJPWppuLsL3hTpE7HR3YE4Qpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/9qy89gnSE6HkPPFigfJPWppuLsL3hTpE7HR3YE4Qpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/9qy89gnSE6HkPPFigfJPWppuLsL3hTpE7HR3YE4Qpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/9qy89gnSE6HkPPFigfJPWppuLsL3hTpE7HR3YE4Qpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/9qy89gnSE6HkPPFigfJPWppuLsL3hTpE7HR3YE4Qpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/9qy89gnSE6HkPPFigfJPWppuLsL3hTpE7HR3YE4Qpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/9qy89gnSE6HkPPFigfJPWppuLsL3hTpE7HR3YE4Qpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/9qy89gnSE6HkPPFigfJPWppuLsL3hTpE7HR3YE4Qpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/9qy89gnSE6HkPPFigfJPWppuLsL3hTpE7HR3YE4Qpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/9qy89gnSE6HkPPFigfJPWppuLsL3hTpE7HR3YE4Qpump/process_trace.jsonl

### HIIE / AKKAPZBnJnzfE83DspsBSoqGSMwa2haFvoEJj1qzdrmk

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/AKKAPZBnJnzfE83DspsBSoqGSMwa2haFvoEJj1qzdrmk/token_status.json｜字段：last_update
- 有证据：发现对象符号：HIIE｜来源：data/gmgn_candidates_live_run/tokens/AKKAPZBnJnzfE83DspsBSoqGSMwa2haFvoEJj1qzdrmk/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/AKKAPZBnJnzfE83DspsBSoqGSMwa2haFvoEJj1qzdrmk/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/AKKAPZBnJnzfE83DspsBSoqGSMwa2haFvoEJj1qzdrmk/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/AKKAPZBnJnzfE83DspsBSoqGSMwa2haFvoEJj1qzdrmk/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/AKKAPZBnJnzfE83DspsBSoqGSMwa2haFvoEJj1qzdrmk/token_status.json；data/gmgn_candidates_live_run/wallet_structure/AKKAPZBnJnzfE83DspsBSoqGSMwa2haFvoEJj1qzdrmk/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/AKKAPZBnJnzfE83DspsBSoqGSMwa2haFvoEJj1qzdrmk/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/AKKAPZBnJnzfE83DspsBSoqGSMwa2haFvoEJj1qzdrmk/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/AKKAPZBnJnzfE83DspsBSoqGSMwa2haFvoEJj1qzdrmk/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/AKKAPZBnJnzfE83DspsBSoqGSMwa2haFvoEJj1qzdrmk/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/AKKAPZBnJnzfE83DspsBSoqGSMwa2haFvoEJj1qzdrmk/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/AKKAPZBnJnzfE83DspsBSoqGSMwa2haFvoEJj1qzdrmk/process_trace.jsonl

### GTRUMP / ANba8pCGnaPvtu483BwMvHKxy31Zod4pGMfDBcmqpump

- 当前状态：DISCOVERED
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T11:41:02Z｜来源：data/gmgn_candidates_live_run/tokens/ANba8pCGnaPvtu483BwMvHKxy31Zod4pGMfDBcmqpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：GTRUMP｜来源：data/gmgn_candidates_live_run/tokens/ANba8pCGnaPvtu483BwMvHKxy31Zod4pGMfDBcmqpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：DISCOVERED｜来源：data/gmgn_candidates_live_run/tokens/ANba8pCGnaPvtu483BwMvHKxy31Zod4pGMfDBcmqpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：DISCOVERED / GMGN 新币筛选进入候选池｜来源：data/gmgn_candidates_live_run/tokens/ANba8pCGnaPvtu483BwMvHKxy31Zod4pGMfDBcmqpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/ANba8pCGnaPvtu483BwMvHKxy31Zod4pGMfDBcmqpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/ANba8pCGnaPvtu483BwMvHKxy31Zod4pGMfDBcmqpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/ANba8pCGnaPvtu483BwMvHKxy31Zod4pGMfDBcmqpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/ANba8pCGnaPvtu483BwMvHKxy31Zod4pGMfDBcmqpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：DISCOVERED / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/ANba8pCGnaPvtu483BwMvHKxy31Zod4pGMfDBcmqpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/ANba8pCGnaPvtu483BwMvHKxy31Zod4pGMfDBcmqpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/ANba8pCGnaPvtu483BwMvHKxy31Zod4pGMfDBcmqpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/ANba8pCGnaPvtu483BwMvHKxy31Zod4pGMfDBcmqpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/ANba8pCGnaPvtu483BwMvHKxy31Zod4pGMfDBcmqpump/process_trace.jsonl

### AALIEN / ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1

- 当前状态：PAPER_OPEN
- 最新动作：HOLD
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1/token_status.json｜字段：last_update
- 有证据：发现对象符号：AALIEN｜来源：data/gmgn_candidates_live_run/tokens/ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：PAPER_OPEN｜来源：data/gmgn_candidates_live_run/tokens/ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1/token_status.json｜字段：current_state
- 有证据：最近流程记录：PAPER_OPEN / 吸筹窗口 valid + SIKK S3/S4 + 允许纸面交易 + 仓位大于0｜来源：data/gmgn_candidates_live_run/tokens/ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 有证据：钱包结构结论：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：quote/security 权限：ALLOW_CONFIRMATION_LAYER｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission
- 有证据：quote/security 原因：报价与安全扫描未触发硬阻断，可进入人工确认层｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：原因

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 有证据：当前状态：PAPER_OPEN｜来源：data/gmgn_candidates_live_run/tokens/ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1/token_status.json｜字段：current_state
- 有证据：钱包结构结论：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：钱包结构原因：发现分发侧钱包 15 个；对手盘压力高，接盘/套牢筹码占比偏高｜来源：data/gmgn_candidates_live_run/wallet_structure/ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1/wallet_structure_decision.json｜字段：wallet_structure_reason
- 有证据：quote/security 权限：ALLOW_CONFIRMATION_LAYER｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission

#### 为什么进入paper
- 有证据：当前状态：PAPER_OPEN｜来源：data/gmgn_candidates_live_run/tokens/ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1/token_status.json｜字段：current_state
- 有证据：最新动作：HOLD｜来源：data/gmgn_candidates_live_run/tokens/ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1/token_status.json｜字段：latest_action
- 有证据：入场依据：吸筹窗口 valid + SIKK S3/S4 + 允许纸面交易 + 仓位大于0｜来源：data/gmgn_candidates_live_run/tokens/ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1/token_status.json｜字段：latest_reason
- 有证据：纸面入场时间：2026-04-30 16:34:00 UTC｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json｜字段：entry_time

#### 为什么退出
- 有证据：纸面退出原因：钱包结构触发纸面强制退出｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json｜字段：exit_reason
- 有证据：纸面退出时间：2026-05-02T22:28:31Z｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json｜字段：exit_time
- 有证据：当前状态：PAPER_OPEN｜来源：data/gmgn_candidates_live_run/tokens/ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1/token_status.json｜字段：current_state

#### 为什么失败
- 有证据：失败类型：STRUCTURE_WEAKENING｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl｜字段：failure_type
- 有证据：失败原因：钱包结构状态变为 WALLET_BLOCK，纸面阶段直接模拟退出｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl｜字段：failure_reason
- 有证据：当前状态：PAPER_OPEN｜来源：data/gmgn_candidates_live_run/tokens/ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1/token_status.json｜字段：current_state

#### 下一步看什么
- 待复查：复查最新状态/动作：PAPER_OPEN / HOLD｜来源：data/gmgn_candidates_live_run/tokens/ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：ALLOW_CONFIRMATION_LAYER / READY_FOR_CONFIRMATION｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1/process_trace.jsonl

### GOBLINPOOP / ASz8X7JaWqp4P4pf5zRfEzD5x5WXeautdHFmLEk7pump

- 当前状态：ACCUMULATING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T11:51:43Z｜来源：data/gmgn_candidates_live_run/tokens/ASz8X7JaWqp4P4pf5zRfEzD5x5WXeautdHFmLEk7pump/token_status.json｜字段：last_update
- 有证据：发现对象符号：GOBLINPOOP｜来源：data/gmgn_candidates_live_run/tokens/ASz8X7JaWqp4P4pf5zRfEzD5x5WXeautdHFmLEk7pump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：ACCUMULATING｜来源：data/gmgn_candidates_live_run/tokens/ASz8X7JaWqp4P4pf5zRfEzD5x5WXeautdHFmLEk7pump/token_status.json｜字段：current_state
- 有证据：最近流程记录：ACCUMULATING / 已出现 T_start，但吸筹窗口仍 pending｜来源：data/gmgn_candidates_live_run/tokens/ASz8X7JaWqp4P4pf5zRfEzD5x5WXeautdHFmLEk7pump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/ASz8X7JaWqp4P4pf5zRfEzD5x5WXeautdHFmLEk7pump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/ASz8X7JaWqp4P4pf5zRfEzD5x5WXeautdHFmLEk7pump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/ASz8X7JaWqp4P4pf5zRfEzD5x5WXeautdHFmLEk7pump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/ASz8X7JaWqp4P4pf5zRfEzD5x5WXeautdHFmLEk7pump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：ACCUMULATING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/ASz8X7JaWqp4P4pf5zRfEzD5x5WXeautdHFmLEk7pump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/ASz8X7JaWqp4P4pf5zRfEzD5x5WXeautdHFmLEk7pump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/ASz8X7JaWqp4P4pf5zRfEzD5x5WXeautdHFmLEk7pump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/ASz8X7JaWqp4P4pf5zRfEzD5x5WXeautdHFmLEk7pump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/ASz8X7JaWqp4P4pf5zRfEzD5x5WXeautdHFmLEk7pump/process_trace.jsonl

### PIRATENALD / AhXUJZTAtU7nYiPB552jhuNfKEvYBErCzbBTj8F1st3g

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T21:15:08Z｜来源：data/gmgn_candidates_live_run/tokens/AhXUJZTAtU7nYiPB552jhuNfKEvYBErCzbBTj8F1st3g/token_status.json｜字段：last_update
- 有证据：发现对象符号：PIRATENALD｜来源：data/gmgn_candidates_live_run/tokens/AhXUJZTAtU7nYiPB552jhuNfKEvYBErCzbBTj8F1st3g/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/AhXUJZTAtU7nYiPB552jhuNfKEvYBErCzbBTj8F1st3g/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/AhXUJZTAtU7nYiPB552jhuNfKEvYBErCzbBTj8F1st3g/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/AhXUJZTAtU7nYiPB552jhuNfKEvYBErCzbBTj8F1st3g/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/AhXUJZTAtU7nYiPB552jhuNfKEvYBErCzbBTj8F1st3g/token_status.json；data/gmgn_candidates_live_run/wallet_structure/AhXUJZTAtU7nYiPB552jhuNfKEvYBErCzbBTj8F1st3g/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/AhXUJZTAtU7nYiPB552jhuNfKEvYBErCzbBTj8F1st3g/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/AhXUJZTAtU7nYiPB552jhuNfKEvYBErCzbBTj8F1st3g/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/AhXUJZTAtU7nYiPB552jhuNfKEvYBErCzbBTj8F1st3g/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/AhXUJZTAtU7nYiPB552jhuNfKEvYBErCzbBTj8F1st3g/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/AhXUJZTAtU7nYiPB552jhuNfKEvYBErCzbBTj8F1st3g/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/AhXUJZTAtU7nYiPB552jhuNfKEvYBErCzbBTj8F1st3g/process_trace.jsonl

### FERVUSAI / AtEvKAGgLD3YZn7y1o5Yf5LfDypwWgRcH5TzdZcepump

- 当前状态：BLOCKED
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T21:25:36Z｜来源：data/gmgn_candidates_live_run/tokens/AtEvKAGgLD3YZn7y1o5Yf5LfDypwWgRcH5TzdZcepump/token_status.json｜字段：last_update
- 有证据：发现对象符号：FERVUSAI｜来源：data/gmgn_candidates_live_run/tokens/AtEvKAGgLD3YZn7y1o5Yf5LfDypwWgRcH5TzdZcepump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：BLOCKED｜来源：data/gmgn_candidates_live_run/tokens/AtEvKAGgLD3YZn7y1o5Yf5LfDypwWgRcH5TzdZcepump/token_status.json｜字段：current_state
- 有证据：最近流程记录：BLOCKED / 吸筹窗口 invalid，进入风险阻断观察｜来源：data/gmgn_candidates_live_run/tokens/AtEvKAGgLD3YZn7y1o5Yf5LfDypwWgRcH5TzdZcepump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/AtEvKAGgLD3YZn7y1o5Yf5LfDypwWgRcH5TzdZcepump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 有证据：当前状态：BLOCKED｜来源：data/gmgn_candidates_live_run/tokens/AtEvKAGgLD3YZn7y1o5Yf5LfDypwWgRcH5TzdZcepump/token_status.json｜字段：current_state
- 有证据：钱包结构结论：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/AtEvKAGgLD3YZn7y1o5Yf5LfDypwWgRcH5TzdZcepump/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：quote/security 权限：MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/AtEvKAGgLD3YZn7y1o5Yf5LfDypwWgRcH5TzdZcepump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：BLOCKED / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/AtEvKAGgLD3YZn7y1o5Yf5LfDypwWgRcH5TzdZcepump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/AtEvKAGgLD3YZn7y1o5Yf5LfDypwWgRcH5TzdZcepump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/AtEvKAGgLD3YZn7y1o5Yf5LfDypwWgRcH5TzdZcepump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/AtEvKAGgLD3YZn7y1o5Yf5LfDypwWgRcH5TzdZcepump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/AtEvKAGgLD3YZn7y1o5Yf5LfDypwWgRcH5TzdZcepump/process_trace.jsonl

### JPPEPE / B167Yu1K7XRm6iut2P7g6gsFfwhVvAWvS2xGYjc7BFrD

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T21:46:26Z｜来源：data/gmgn_candidates_live_run/tokens/B167Yu1K7XRm6iut2P7g6gsFfwhVvAWvS2xGYjc7BFrD/token_status.json｜字段：last_update
- 有证据：发现对象符号：JPPEPE｜来源：data/gmgn_candidates_live_run/tokens/B167Yu1K7XRm6iut2P7g6gsFfwhVvAWvS2xGYjc7BFrD/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/B167Yu1K7XRm6iut2P7g6gsFfwhVvAWvS2xGYjc7BFrD/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/B167Yu1K7XRm6iut2P7g6gsFfwhVvAWvS2xGYjc7BFrD/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/B167Yu1K7XRm6iut2P7g6gsFfwhVvAWvS2xGYjc7BFrD/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/B167Yu1K7XRm6iut2P7g6gsFfwhVvAWvS2xGYjc7BFrD/token_status.json；data/gmgn_candidates_live_run/wallet_structure/B167Yu1K7XRm6iut2P7g6gsFfwhVvAWvS2xGYjc7BFrD/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/B167Yu1K7XRm6iut2P7g6gsFfwhVvAWvS2xGYjc7BFrD/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/B167Yu1K7XRm6iut2P7g6gsFfwhVvAWvS2xGYjc7BFrD/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/B167Yu1K7XRm6iut2P7g6gsFfwhVvAWvS2xGYjc7BFrD/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/B167Yu1K7XRm6iut2P7g6gsFfwhVvAWvS2xGYjc7BFrD/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/B167Yu1K7XRm6iut2P7g6gsFfwhVvAWvS2xGYjc7BFrD/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/B167Yu1K7XRm6iut2P7g6gsFfwhVvAWvS2xGYjc7BFrD/process_trace.jsonl

### AMC / B85ta9Qp7EgoVXaMka9BQYrFogSmC3PRjsxNM6HaHF41

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/B85ta9Qp7EgoVXaMka9BQYrFogSmC3PRjsxNM6HaHF41/token_status.json｜字段：last_update
- 有证据：发现对象符号：AMC｜来源：data/gmgn_candidates_live_run/tokens/B85ta9Qp7EgoVXaMka9BQYrFogSmC3PRjsxNM6HaHF41/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/B85ta9Qp7EgoVXaMka9BQYrFogSmC3PRjsxNM6HaHF41/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/B85ta9Qp7EgoVXaMka9BQYrFogSmC3PRjsxNM6HaHF41/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/B85ta9Qp7EgoVXaMka9BQYrFogSmC3PRjsxNM6HaHF41/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/B85ta9Qp7EgoVXaMka9BQYrFogSmC3PRjsxNM6HaHF41/token_status.json；data/gmgn_candidates_live_run/wallet_structure/B85ta9Qp7EgoVXaMka9BQYrFogSmC3PRjsxNM6HaHF41/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/B85ta9Qp7EgoVXaMka9BQYrFogSmC3PRjsxNM6HaHF41/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/B85ta9Qp7EgoVXaMka9BQYrFogSmC3PRjsxNM6HaHF41/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/B85ta9Qp7EgoVXaMka9BQYrFogSmC3PRjsxNM6HaHF41/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/B85ta9Qp7EgoVXaMka9BQYrFogSmC3PRjsxNM6HaHF41/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/B85ta9Qp7EgoVXaMka9BQYrFogSmC3PRjsxNM6HaHF41/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/B85ta9Qp7EgoVXaMka9BQYrFogSmC3PRjsxNM6HaHF41/process_trace.jsonl

### Nigslop / BA8Pe9vy7GnybMLofZW5c8XAezJF4XGt94siHB7bpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T13:54:08Z｜来源：data/gmgn_candidates_live_run/tokens/BA8Pe9vy7GnybMLofZW5c8XAezJF4XGt94siHB7bpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：Nigslop｜来源：data/gmgn_candidates_live_run/tokens/BA8Pe9vy7GnybMLofZW5c8XAezJF4XGt94siHB7bpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/BA8Pe9vy7GnybMLofZW5c8XAezJF4XGt94siHB7bpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/BA8Pe9vy7GnybMLofZW5c8XAezJF4XGt94siHB7bpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/BA8Pe9vy7GnybMLofZW5c8XAezJF4XGt94siHB7bpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/BA8Pe9vy7GnybMLofZW5c8XAezJF4XGt94siHB7bpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/BA8Pe9vy7GnybMLofZW5c8XAezJF4XGt94siHB7bpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/BA8Pe9vy7GnybMLofZW5c8XAezJF4XGt94siHB7bpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/BA8Pe9vy7GnybMLofZW5c8XAezJF4XGt94siHB7bpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/BA8Pe9vy7GnybMLofZW5c8XAezJF4XGt94siHB7bpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/BA8Pe9vy7GnybMLofZW5c8XAezJF4XGt94siHB7bpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/BA8Pe9vy7GnybMLofZW5c8XAezJF4XGt94siHB7bpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/BA8Pe9vy7GnybMLofZW5c8XAezJF4XGt94siHB7bpump/process_trace.jsonl

### memegotchi / BaCSr6omaLf113LfDDv9Wgb2dfGmJzKWvQhJB2QNpump

- 当前状态：BLOCKED
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T17:32:44Z｜来源：data/gmgn_candidates_live_run/tokens/BaCSr6omaLf113LfDDv9Wgb2dfGmJzKWvQhJB2QNpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：memegotchi｜来源：data/gmgn_candidates_live_run/tokens/BaCSr6omaLf113LfDDv9Wgb2dfGmJzKWvQhJB2QNpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：BLOCKED｜来源：data/gmgn_candidates_live_run/tokens/BaCSr6omaLf113LfDDv9Wgb2dfGmJzKWvQhJB2QNpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：BLOCKED / 风险门禁阻断或 SIKK 信号 SX｜来源：data/gmgn_candidates_live_run/tokens/BaCSr6omaLf113LfDDv9Wgb2dfGmJzKWvQhJB2QNpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/BaCSr6omaLf113LfDDv9Wgb2dfGmJzKWvQhJB2QNpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 有证据：当前状态：BLOCKED｜来源：data/gmgn_candidates_live_run/tokens/BaCSr6omaLf113LfDDv9Wgb2dfGmJzKWvQhJB2QNpump/token_status.json｜字段：current_state
- 有证据：钱包结构结论：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/BaCSr6omaLf113LfDDv9Wgb2dfGmJzKWvQhJB2QNpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：quote/security 权限：MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/BaCSr6omaLf113LfDDv9Wgb2dfGmJzKWvQhJB2QNpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：BLOCKED / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/BaCSr6omaLf113LfDDv9Wgb2dfGmJzKWvQhJB2QNpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/BaCSr6omaLf113LfDDv9Wgb2dfGmJzKWvQhJB2QNpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/BaCSr6omaLf113LfDDv9Wgb2dfGmJzKWvQhJB2QNpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/BaCSr6omaLf113LfDDv9Wgb2dfGmJzKWvQhJB2QNpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/BaCSr6omaLf113LfDDv9Wgb2dfGmJzKWvQhJB2QNpump/process_trace.jsonl

### GA / BhCuLLN38Ru7qBkXBmGzNeG6ipiAcqvywpvNjQW7pump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/BhCuLLN38Ru7qBkXBmGzNeG6ipiAcqvywpvNjQW7pump/token_status.json｜字段：last_update
- 有证据：发现对象符号：GA｜来源：data/gmgn_candidates_live_run/tokens/BhCuLLN38Ru7qBkXBmGzNeG6ipiAcqvywpvNjQW7pump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/BhCuLLN38Ru7qBkXBmGzNeG6ipiAcqvywpvNjQW7pump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/BhCuLLN38Ru7qBkXBmGzNeG6ipiAcqvywpvNjQW7pump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/BhCuLLN38Ru7qBkXBmGzNeG6ipiAcqvywpvNjQW7pump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/BhCuLLN38Ru7qBkXBmGzNeG6ipiAcqvywpvNjQW7pump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/BhCuLLN38Ru7qBkXBmGzNeG6ipiAcqvywpvNjQW7pump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/BhCuLLN38Ru7qBkXBmGzNeG6ipiAcqvywpvNjQW7pump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/BhCuLLN38Ru7qBkXBmGzNeG6ipiAcqvywpvNjQW7pump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/BhCuLLN38Ru7qBkXBmGzNeG6ipiAcqvywpvNjQW7pump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/BhCuLLN38Ru7qBkXBmGzNeG6ipiAcqvywpvNjQW7pump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/BhCuLLN38Ru7qBkXBmGzNeG6ipiAcqvywpvNjQW7pump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/BhCuLLN38Ru7qBkXBmGzNeG6ipiAcqvywpvNjQW7pump/process_trace.jsonl

### CHUDBOB / Bvh8xqP2nkzZBBEywAFqNAc7Mek7QiUofeTmTbKRpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/Bvh8xqP2nkzZBBEywAFqNAc7Mek7QiUofeTmTbKRpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：CHUDBOB｜来源：data/gmgn_candidates_live_run/tokens/Bvh8xqP2nkzZBBEywAFqNAc7Mek7QiUofeTmTbKRpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/Bvh8xqP2nkzZBBEywAFqNAc7Mek7QiUofeTmTbKRpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/Bvh8xqP2nkzZBBEywAFqNAc7Mek7QiUofeTmTbKRpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/Bvh8xqP2nkzZBBEywAFqNAc7Mek7QiUofeTmTbKRpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/Bvh8xqP2nkzZBBEywAFqNAc7Mek7QiUofeTmTbKRpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/Bvh8xqP2nkzZBBEywAFqNAc7Mek7QiUofeTmTbKRpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/Bvh8xqP2nkzZBBEywAFqNAc7Mek7QiUofeTmTbKRpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/Bvh8xqP2nkzZBBEywAFqNAc7Mek7QiUofeTmTbKRpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/Bvh8xqP2nkzZBBEywAFqNAc7Mek7QiUofeTmTbKRpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/Bvh8xqP2nkzZBBEywAFqNAc7Mek7QiUofeTmTbKRpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/Bvh8xqP2nkzZBBEywAFqNAc7Mek7QiUofeTmTbKRpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/Bvh8xqP2nkzZBBEywAFqNAc7Mek7QiUofeTmTbKRpump/process_trace.jsonl

### SIGHT  / ByqipPbSHxzLi6ga5LNrnE229vsLuSrCfHMaDbe1TRND

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/ByqipPbSHxzLi6ga5LNrnE229vsLuSrCfHMaDbe1TRND/token_status.json｜字段：last_update
- 有证据：发现对象符号：SIGHT ｜来源：data/gmgn_candidates_live_run/tokens/ByqipPbSHxzLi6ga5LNrnE229vsLuSrCfHMaDbe1TRND/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/ByqipPbSHxzLi6ga5LNrnE229vsLuSrCfHMaDbe1TRND/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/ByqipPbSHxzLi6ga5LNrnE229vsLuSrCfHMaDbe1TRND/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/ByqipPbSHxzLi6ga5LNrnE229vsLuSrCfHMaDbe1TRND/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/ByqipPbSHxzLi6ga5LNrnE229vsLuSrCfHMaDbe1TRND/token_status.json；data/gmgn_candidates_live_run/wallet_structure/ByqipPbSHxzLi6ga5LNrnE229vsLuSrCfHMaDbe1TRND/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/ByqipPbSHxzLi6ga5LNrnE229vsLuSrCfHMaDbe1TRND/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/ByqipPbSHxzLi6ga5LNrnE229vsLuSrCfHMaDbe1TRND/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/ByqipPbSHxzLi6ga5LNrnE229vsLuSrCfHMaDbe1TRND/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/ByqipPbSHxzLi6ga5LNrnE229vsLuSrCfHMaDbe1TRND/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/ByqipPbSHxzLi6ga5LNrnE229vsLuSrCfHMaDbe1TRND/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/ByqipPbSHxzLi6ga5LNrnE229vsLuSrCfHMaDbe1TRND/process_trace.jsonl

### 1000x / C1FjBybKVyatJcJ8JDd7VunSjVkmsb3m1p6q3qvHpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/C1FjBybKVyatJcJ8JDd7VunSjVkmsb3m1p6q3qvHpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：1000x｜来源：data/gmgn_candidates_live_run/tokens/C1FjBybKVyatJcJ8JDd7VunSjVkmsb3m1p6q3qvHpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/C1FjBybKVyatJcJ8JDd7VunSjVkmsb3m1p6q3qvHpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/C1FjBybKVyatJcJ8JDd7VunSjVkmsb3m1p6q3qvHpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/C1FjBybKVyatJcJ8JDd7VunSjVkmsb3m1p6q3qvHpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/C1FjBybKVyatJcJ8JDd7VunSjVkmsb3m1p6q3qvHpump/token_status.json｜字段：current_state
- 有证据：钱包结构结论：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/C1FjBybKVyatJcJ8JDd7VunSjVkmsb3m1p6q3qvHpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：钱包结构原因：发现分发侧钱包 10 个；对手盘压力高，接盘/套牢筹码占比偏高｜来源：data/gmgn_candidates_live_run/wallet_structure/C1FjBybKVyatJcJ8JDd7VunSjVkmsb3m1p6q3qvHpump/wallet_structure_decision.json｜字段：wallet_structure_reason
- 有证据：quote/security 权限：MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/C1FjBybKVyatJcJ8JDd7VunSjVkmsb3m1p6q3qvHpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 有证据：纸面退出原因：钱包结构触发纸面强制退出｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json｜字段：exit_reason
- 有证据：纸面退出时间：2026-05-02T12:20:12Z｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json｜字段：exit_time
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/C1FjBybKVyatJcJ8JDd7VunSjVkmsb3m1p6q3qvHpump/token_status.json｜字段：current_state

#### 为什么失败
- 有证据：失败类型：STRUCTURE_WEAKENING｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl｜字段：failure_type
- 有证据：失败原因：钱包结构状态变为 WALLET_BLOCK，纸面阶段直接模拟退出｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl｜字段：failure_reason
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/C1FjBybKVyatJcJ8JDd7VunSjVkmsb3m1p6q3qvHpump/token_status.json｜字段：current_state

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/C1FjBybKVyatJcJ8JDd7VunSjVkmsb3m1p6q3qvHpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/C1FjBybKVyatJcJ8JDd7VunSjVkmsb3m1p6q3qvHpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/C1FjBybKVyatJcJ8JDd7VunSjVkmsb3m1p6q3qvHpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/C1FjBybKVyatJcJ8JDd7VunSjVkmsb3m1p6q3qvHpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/C1FjBybKVyatJcJ8JDd7VunSjVkmsb3m1p6q3qvHpump/process_trace.jsonl

### NPC / CEqaq1pe8TZUFyiTSy8MAz7wzoBu5xWExqW99BBVpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T21:56:47Z｜来源：data/gmgn_candidates_live_run/tokens/CEqaq1pe8TZUFyiTSy8MAz7wzoBu5xWExqW99BBVpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：NPC｜来源：data/gmgn_candidates_live_run/tokens/CEqaq1pe8TZUFyiTSy8MAz7wzoBu5xWExqW99BBVpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/CEqaq1pe8TZUFyiTSy8MAz7wzoBu5xWExqW99BBVpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/CEqaq1pe8TZUFyiTSy8MAz7wzoBu5xWExqW99BBVpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/CEqaq1pe8TZUFyiTSy8MAz7wzoBu5xWExqW99BBVpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/CEqaq1pe8TZUFyiTSy8MAz7wzoBu5xWExqW99BBVpump/token_status.json｜字段：current_state
- 有证据：钱包结构结论：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/CEqaq1pe8TZUFyiTSy8MAz7wzoBu5xWExqW99BBVpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：钱包结构原因：发现分发侧钱包 9 个；对手盘压力高，接盘/套牢筹码占比偏高｜来源：data/gmgn_candidates_live_run/wallet_structure/CEqaq1pe8TZUFyiTSy8MAz7wzoBu5xWExqW99BBVpump/wallet_structure_decision.json｜字段：wallet_structure_reason
- 有证据：quote/security 权限：MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/CEqaq1pe8TZUFyiTSy8MAz7wzoBu5xWExqW99BBVpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 有证据：纸面退出原因：钱包结构触发纸面强制退出｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json｜字段：exit_reason
- 有证据：纸面退出时间：2026-05-02T18:38:16Z｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json｜字段：exit_time
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/CEqaq1pe8TZUFyiTSy8MAz7wzoBu5xWExqW99BBVpump/token_status.json｜字段：current_state

#### 为什么失败
- 有证据：失败类型：STRUCTURE_WEAKENING｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl｜字段：failure_type
- 有证据：失败原因：钱包结构状态变为 WALLET_BLOCK，纸面阶段直接模拟退出｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl｜字段：failure_reason
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/CEqaq1pe8TZUFyiTSy8MAz7wzoBu5xWExqW99BBVpump/token_status.json｜字段：current_state

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/CEqaq1pe8TZUFyiTSy8MAz7wzoBu5xWExqW99BBVpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/CEqaq1pe8TZUFyiTSy8MAz7wzoBu5xWExqW99BBVpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/CEqaq1pe8TZUFyiTSy8MAz7wzoBu5xWExqW99BBVpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/CEqaq1pe8TZUFyiTSy8MAz7wzoBu5xWExqW99BBVpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/CEqaq1pe8TZUFyiTSy8MAz7wzoBu5xWExqW99BBVpump/process_trace.jsonl

### FIT / CFRX4w9w2mvhwZAxCPnyTY3PhHTJ9vQgninuXZfH5Wwn

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/CFRX4w9w2mvhwZAxCPnyTY3PhHTJ9vQgninuXZfH5Wwn/token_status.json｜字段：last_update
- 有证据：发现对象符号：FIT｜来源：data/gmgn_candidates_live_run/tokens/CFRX4w9w2mvhwZAxCPnyTY3PhHTJ9vQgninuXZfH5Wwn/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/CFRX4w9w2mvhwZAxCPnyTY3PhHTJ9vQgninuXZfH5Wwn/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/CFRX4w9w2mvhwZAxCPnyTY3PhHTJ9vQgninuXZfH5Wwn/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/CFRX4w9w2mvhwZAxCPnyTY3PhHTJ9vQgninuXZfH5Wwn/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/CFRX4w9w2mvhwZAxCPnyTY3PhHTJ9vQgninuXZfH5Wwn/token_status.json；data/gmgn_candidates_live_run/wallet_structure/CFRX4w9w2mvhwZAxCPnyTY3PhHTJ9vQgninuXZfH5Wwn/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/CFRX4w9w2mvhwZAxCPnyTY3PhHTJ9vQgninuXZfH5Wwn/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/CFRX4w9w2mvhwZAxCPnyTY3PhHTJ9vQgninuXZfH5Wwn/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/CFRX4w9w2mvhwZAxCPnyTY3PhHTJ9vQgninuXZfH5Wwn/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/CFRX4w9w2mvhwZAxCPnyTY3PhHTJ9vQgninuXZfH5Wwn/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/CFRX4w9w2mvhwZAxCPnyTY3PhHTJ9vQgninuXZfH5Wwn/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/CFRX4w9w2mvhwZAxCPnyTY3PhHTJ9vQgninuXZfH5Wwn/process_trace.jsonl

### Cancer / CJxdacDnC9CZXrtGSntJVFcuaVjkqH5Rigde6Y1Fpump

- 当前状态：BLOCKED
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T13:54:08Z｜来源：data/gmgn_candidates_live_run/tokens/CJxdacDnC9CZXrtGSntJVFcuaVjkqH5Rigde6Y1Fpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：Cancer｜来源：data/gmgn_candidates_live_run/tokens/CJxdacDnC9CZXrtGSntJVFcuaVjkqH5Rigde6Y1Fpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：BLOCKED｜来源：data/gmgn_candidates_live_run/tokens/CJxdacDnC9CZXrtGSntJVFcuaVjkqH5Rigde6Y1Fpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：BLOCKED / 风险门禁阻断或 SIKK 信号 SX｜来源：data/gmgn_candidates_live_run/tokens/CJxdacDnC9CZXrtGSntJVFcuaVjkqH5Rigde6Y1Fpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/CJxdacDnC9CZXrtGSntJVFcuaVjkqH5Rigde6Y1Fpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 有证据：当前状态：BLOCKED｜来源：data/gmgn_candidates_live_run/tokens/CJxdacDnC9CZXrtGSntJVFcuaVjkqH5Rigde6Y1Fpump/token_status.json｜字段：current_state
- 有证据：钱包结构结论：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/CJxdacDnC9CZXrtGSntJVFcuaVjkqH5Rigde6Y1Fpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：quote/security 权限：由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/CJxdacDnC9CZXrtGSntJVFcuaVjkqH5Rigde6Y1Fpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：BLOCKED / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/CJxdacDnC9CZXrtGSntJVFcuaVjkqH5Rigde6Y1Fpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/CJxdacDnC9CZXrtGSntJVFcuaVjkqH5Rigde6Y1Fpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/CJxdacDnC9CZXrtGSntJVFcuaVjkqH5Rigde6Y1Fpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/CJxdacDnC9CZXrtGSntJVFcuaVjkqH5Rigde6Y1Fpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/CJxdacDnC9CZXrtGSntJVFcuaVjkqH5Rigde6Y1Fpump/process_trace.jsonl

### HANK / CegXaVAwRpXw9P9CXHyuPTuyTHveKH5GHeRVWJwtpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T10:04:43Z｜来源：data/gmgn_candidates_live_run/tokens/CegXaVAwRpXw9P9CXHyuPTuyTHveKH5GHeRVWJwtpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：HANK｜来源：data/gmgn_candidates_live_run/tokens/CegXaVAwRpXw9P9CXHyuPTuyTHveKH5GHeRVWJwtpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/CegXaVAwRpXw9P9CXHyuPTuyTHveKH5GHeRVWJwtpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/CegXaVAwRpXw9P9CXHyuPTuyTHveKH5GHeRVWJwtpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/CegXaVAwRpXw9P9CXHyuPTuyTHveKH5GHeRVWJwtpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/CegXaVAwRpXw9P9CXHyuPTuyTHveKH5GHeRVWJwtpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/CegXaVAwRpXw9P9CXHyuPTuyTHveKH5GHeRVWJwtpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/CegXaVAwRpXw9P9CXHyuPTuyTHveKH5GHeRVWJwtpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/CegXaVAwRpXw9P9CXHyuPTuyTHveKH5GHeRVWJwtpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/CegXaVAwRpXw9P9CXHyuPTuyTHveKH5GHeRVWJwtpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/CegXaVAwRpXw9P9CXHyuPTuyTHveKH5GHeRVWJwtpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/CegXaVAwRpXw9P9CXHyuPTuyTHveKH5GHeRVWJwtpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/CegXaVAwRpXw9P9CXHyuPTuyTHveKH5GHeRVWJwtpump/process_trace.jsonl

### CHEEMS / Ck4UWKNw4v86j6Z6AkCf22z7XwQJrH6tBeiA9BKBpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T12:19:29Z｜来源：data/gmgn_candidates_live_run/tokens/Ck4UWKNw4v86j6Z6AkCf22z7XwQJrH6tBeiA9BKBpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：CHEEMS｜来源：data/gmgn_candidates_live_run/tokens/Ck4UWKNw4v86j6Z6AkCf22z7XwQJrH6tBeiA9BKBpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/Ck4UWKNw4v86j6Z6AkCf22z7XwQJrH6tBeiA9BKBpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/Ck4UWKNw4v86j6Z6AkCf22z7XwQJrH6tBeiA9BKBpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/Ck4UWKNw4v86j6Z6AkCf22z7XwQJrH6tBeiA9BKBpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/Ck4UWKNw4v86j6Z6AkCf22z7XwQJrH6tBeiA9BKBpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/Ck4UWKNw4v86j6Z6AkCf22z7XwQJrH6tBeiA9BKBpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/Ck4UWKNw4v86j6Z6AkCf22z7XwQJrH6tBeiA9BKBpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/Ck4UWKNw4v86j6Z6AkCf22z7XwQJrH6tBeiA9BKBpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/Ck4UWKNw4v86j6Z6AkCf22z7XwQJrH6tBeiA9BKBpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/Ck4UWKNw4v86j6Z6AkCf22z7XwQJrH6tBeiA9BKBpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/Ck4UWKNw4v86j6Z6AkCf22z7XwQJrH6tBeiA9BKBpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/Ck4UWKNw4v86j6Z6AkCf22z7XwQJrH6tBeiA9BKBpump/process_trace.jsonl

### MOG / D9dDZ7sbPGzjBu2MD49E66Eo1VDKGLPCzWGxMF7Dfac2

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T21:25:36Z｜来源：data/gmgn_candidates_live_run/tokens/D9dDZ7sbPGzjBu2MD49E66Eo1VDKGLPCzWGxMF7Dfac2/token_status.json｜字段：last_update
- 有证据：发现对象符号：MOG｜来源：data/gmgn_candidates_live_run/tokens/D9dDZ7sbPGzjBu2MD49E66Eo1VDKGLPCzWGxMF7Dfac2/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/D9dDZ7sbPGzjBu2MD49E66Eo1VDKGLPCzWGxMF7Dfac2/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/D9dDZ7sbPGzjBu2MD49E66Eo1VDKGLPCzWGxMF7Dfac2/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/D9dDZ7sbPGzjBu2MD49E66Eo1VDKGLPCzWGxMF7Dfac2/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/D9dDZ7sbPGzjBu2MD49E66Eo1VDKGLPCzWGxMF7Dfac2/token_status.json；data/gmgn_candidates_live_run/wallet_structure/D9dDZ7sbPGzjBu2MD49E66Eo1VDKGLPCzWGxMF7Dfac2/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/D9dDZ7sbPGzjBu2MD49E66Eo1VDKGLPCzWGxMF7Dfac2/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/D9dDZ7sbPGzjBu2MD49E66Eo1VDKGLPCzWGxMF7Dfac2/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/D9dDZ7sbPGzjBu2MD49E66Eo1VDKGLPCzWGxMF7Dfac2/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/D9dDZ7sbPGzjBu2MD49E66Eo1VDKGLPCzWGxMF7Dfac2/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/D9dDZ7sbPGzjBu2MD49E66Eo1VDKGLPCzWGxMF7Dfac2/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/D9dDZ7sbPGzjBu2MD49E66Eo1VDKGLPCzWGxMF7Dfac2/process_trace.jsonl

### ELUENT / DQa4mxFws6WsXMwn8gpEBXqMsGfDn4Uopi8W2Zvopump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/DQa4mxFws6WsXMwn8gpEBXqMsGfDn4Uopi8W2Zvopump/token_status.json｜字段：last_update
- 有证据：发现对象符号：ELUENT｜来源：data/gmgn_candidates_live_run/tokens/DQa4mxFws6WsXMwn8gpEBXqMsGfDn4Uopi8W2Zvopump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/DQa4mxFws6WsXMwn8gpEBXqMsGfDn4Uopi8W2Zvopump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/DQa4mxFws6WsXMwn8gpEBXqMsGfDn4Uopi8W2Zvopump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/DQa4mxFws6WsXMwn8gpEBXqMsGfDn4Uopi8W2Zvopump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/DQa4mxFws6WsXMwn8gpEBXqMsGfDn4Uopi8W2Zvopump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/DQa4mxFws6WsXMwn8gpEBXqMsGfDn4Uopi8W2Zvopump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/DQa4mxFws6WsXMwn8gpEBXqMsGfDn4Uopi8W2Zvopump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/DQa4mxFws6WsXMwn8gpEBXqMsGfDn4Uopi8W2Zvopump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/DQa4mxFws6WsXMwn8gpEBXqMsGfDn4Uopi8W2Zvopump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/DQa4mxFws6WsXMwn8gpEBXqMsGfDn4Uopi8W2Zvopump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/DQa4mxFws6WsXMwn8gpEBXqMsGfDn4Uopi8W2Zvopump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/DQa4mxFws6WsXMwn8gpEBXqMsGfDn4Uopi8W2Zvopump/process_trace.jsonl

### ML / DyhgWtTeAE2UYEfLwpAZ4441eaCWFedRMoxUYM9ypump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/DyhgWtTeAE2UYEfLwpAZ4441eaCWFedRMoxUYM9ypump/token_status.json｜字段：last_update
- 有证据：发现对象符号：ML｜来源：data/gmgn_candidates_live_run/tokens/DyhgWtTeAE2UYEfLwpAZ4441eaCWFedRMoxUYM9ypump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/DyhgWtTeAE2UYEfLwpAZ4441eaCWFedRMoxUYM9ypump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/DyhgWtTeAE2UYEfLwpAZ4441eaCWFedRMoxUYM9ypump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/DyhgWtTeAE2UYEfLwpAZ4441eaCWFedRMoxUYM9ypump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/DyhgWtTeAE2UYEfLwpAZ4441eaCWFedRMoxUYM9ypump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/DyhgWtTeAE2UYEfLwpAZ4441eaCWFedRMoxUYM9ypump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/DyhgWtTeAE2UYEfLwpAZ4441eaCWFedRMoxUYM9ypump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/DyhgWtTeAE2UYEfLwpAZ4441eaCWFedRMoxUYM9ypump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/DyhgWtTeAE2UYEfLwpAZ4441eaCWFedRMoxUYM9ypump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/DyhgWtTeAE2UYEfLwpAZ4441eaCWFedRMoxUYM9ypump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/DyhgWtTeAE2UYEfLwpAZ4441eaCWFedRMoxUYM9ypump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/DyhgWtTeAE2UYEfLwpAZ4441eaCWFedRMoxUYM9ypump/process_trace.jsonl

### Shekel / DzZ25zeRccJ7uZw47DE9mZEjWa19bAKZerePfGRApump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/DzZ25zeRccJ7uZw47DE9mZEjWa19bAKZerePfGRApump/token_status.json｜字段：last_update
- 有证据：发现对象符号：Shekel｜来源：data/gmgn_candidates_live_run/tokens/DzZ25zeRccJ7uZw47DE9mZEjWa19bAKZerePfGRApump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/DzZ25zeRccJ7uZw47DE9mZEjWa19bAKZerePfGRApump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/DzZ25zeRccJ7uZw47DE9mZEjWa19bAKZerePfGRApump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/DzZ25zeRccJ7uZw47DE9mZEjWa19bAKZerePfGRApump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/DzZ25zeRccJ7uZw47DE9mZEjWa19bAKZerePfGRApump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/DzZ25zeRccJ7uZw47DE9mZEjWa19bAKZerePfGRApump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/DzZ25zeRccJ7uZw47DE9mZEjWa19bAKZerePfGRApump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/DzZ25zeRccJ7uZw47DE9mZEjWa19bAKZerePfGRApump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/DzZ25zeRccJ7uZw47DE9mZEjWa19bAKZerePfGRApump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/DzZ25zeRccJ7uZw47DE9mZEjWa19bAKZerePfGRApump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/DzZ25zeRccJ7uZw47DE9mZEjWa19bAKZerePfGRApump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/DzZ25zeRccJ7uZw47DE9mZEjWa19bAKZerePfGRApump/process_trace.jsonl

### DOGE / E4tPSmY1EtFKfeDaqBfAgbauBpFtvPwS4iQMDfpSpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T17:32:44Z｜来源：data/gmgn_candidates_live_run/tokens/E4tPSmY1EtFKfeDaqBfAgbauBpFtvPwS4iQMDfpSpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：DOGE｜来源：data/gmgn_candidates_live_run/tokens/E4tPSmY1EtFKfeDaqBfAgbauBpFtvPwS4iQMDfpSpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/E4tPSmY1EtFKfeDaqBfAgbauBpFtvPwS4iQMDfpSpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/E4tPSmY1EtFKfeDaqBfAgbauBpFtvPwS4iQMDfpSpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/E4tPSmY1EtFKfeDaqBfAgbauBpFtvPwS4iQMDfpSpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/E4tPSmY1EtFKfeDaqBfAgbauBpFtvPwS4iQMDfpSpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/E4tPSmY1EtFKfeDaqBfAgbauBpFtvPwS4iQMDfpSpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/E4tPSmY1EtFKfeDaqBfAgbauBpFtvPwS4iQMDfpSpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/E4tPSmY1EtFKfeDaqBfAgbauBpFtvPwS4iQMDfpSpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/E4tPSmY1EtFKfeDaqBfAgbauBpFtvPwS4iQMDfpSpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/E4tPSmY1EtFKfeDaqBfAgbauBpFtvPwS4iQMDfpSpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/E4tPSmY1EtFKfeDaqBfAgbauBpFtvPwS4iQMDfpSpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/E4tPSmY1EtFKfeDaqBfAgbauBpFtvPwS4iQMDfpSpump/process_trace.jsonl

### STJUDE / E8syR4zsgQG2zo9YyiyfX4ujubByR4z6qj9stjASpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/E8syR4zsgQG2zo9YyiyfX4ujubByR4z6qj9stjASpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：STJUDE｜来源：data/gmgn_candidates_live_run/tokens/E8syR4zsgQG2zo9YyiyfX4ujubByR4z6qj9stjASpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/E8syR4zsgQG2zo9YyiyfX4ujubByR4z6qj9stjASpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/E8syR4zsgQG2zo9YyiyfX4ujubByR4z6qj9stjASpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/E8syR4zsgQG2zo9YyiyfX4ujubByR4z6qj9stjASpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/E8syR4zsgQG2zo9YyiyfX4ujubByR4z6qj9stjASpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/E8syR4zsgQG2zo9YyiyfX4ujubByR4z6qj9stjASpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/E8syR4zsgQG2zo9YyiyfX4ujubByR4z6qj9stjASpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/E8syR4zsgQG2zo9YyiyfX4ujubByR4z6qj9stjASpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/E8syR4zsgQG2zo9YyiyfX4ujubByR4z6qj9stjASpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/E8syR4zsgQG2zo9YyiyfX4ujubByR4z6qj9stjASpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/E8syR4zsgQG2zo9YyiyfX4ujubByR4z6qj9stjASpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/E8syR4zsgQG2zo9YyiyfX4ujubByR4z6qj9stjASpump/process_trace.jsonl

### ROBO / EC1TMMg4shn1XrYNy5Y5a98LT6kjNcFtgnav11jSpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T11:51:43Z｜来源：data/gmgn_candidates_live_run/tokens/EC1TMMg4shn1XrYNy5Y5a98LT6kjNcFtgnav11jSpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：ROBO｜来源：data/gmgn_candidates_live_run/tokens/EC1TMMg4shn1XrYNy5Y5a98LT6kjNcFtgnav11jSpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/EC1TMMg4shn1XrYNy5Y5a98LT6kjNcFtgnav11jSpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/EC1TMMg4shn1XrYNy5Y5a98LT6kjNcFtgnav11jSpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/EC1TMMg4shn1XrYNy5Y5a98LT6kjNcFtgnav11jSpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/EC1TMMg4shn1XrYNy5Y5a98LT6kjNcFtgnav11jSpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/EC1TMMg4shn1XrYNy5Y5a98LT6kjNcFtgnav11jSpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/EC1TMMg4shn1XrYNy5Y5a98LT6kjNcFtgnav11jSpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/EC1TMMg4shn1XrYNy5Y5a98LT6kjNcFtgnav11jSpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/EC1TMMg4shn1XrYNy5Y5a98LT6kjNcFtgnav11jSpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/EC1TMMg4shn1XrYNy5Y5a98LT6kjNcFtgnav11jSpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/EC1TMMg4shn1XrYNy5Y5a98LT6kjNcFtgnav11jSpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/EC1TMMg4shn1XrYNy5Y5a98LT6kjNcFtgnav11jSpump/process_trace.jsonl

### CHUNGUS / EMuNS94pVJUKVk1uHCp52K4wPyP8wsF7bDnGP6e1iQ92

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T12:19:29Z｜来源：data/gmgn_candidates_live_run/tokens/EMuNS94pVJUKVk1uHCp52K4wPyP8wsF7bDnGP6e1iQ92/token_status.json｜字段：last_update
- 有证据：发现对象符号：CHUNGUS｜来源：data/gmgn_candidates_live_run/tokens/EMuNS94pVJUKVk1uHCp52K4wPyP8wsF7bDnGP6e1iQ92/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/EMuNS94pVJUKVk1uHCp52K4wPyP8wsF7bDnGP6e1iQ92/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/EMuNS94pVJUKVk1uHCp52K4wPyP8wsF7bDnGP6e1iQ92/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/EMuNS94pVJUKVk1uHCp52K4wPyP8wsF7bDnGP6e1iQ92/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/EMuNS94pVJUKVk1uHCp52K4wPyP8wsF7bDnGP6e1iQ92/token_status.json；data/gmgn_candidates_live_run/wallet_structure/EMuNS94pVJUKVk1uHCp52K4wPyP8wsF7bDnGP6e1iQ92/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/EMuNS94pVJUKVk1uHCp52K4wPyP8wsF7bDnGP6e1iQ92/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/EMuNS94pVJUKVk1uHCp52K4wPyP8wsF7bDnGP6e1iQ92/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/EMuNS94pVJUKVk1uHCp52K4wPyP8wsF7bDnGP6e1iQ92/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/EMuNS94pVJUKVk1uHCp52K4wPyP8wsF7bDnGP6e1iQ92/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/EMuNS94pVJUKVk1uHCp52K4wPyP8wsF7bDnGP6e1iQ92/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/EMuNS94pVJUKVk1uHCp52K4wPyP8wsF7bDnGP6e1iQ92/process_trace.jsonl

### SMW / EVrfnKXnX1XCT5ESvp6VJUwLFDU1Ajq1dpUrG5qUpump

- 当前状态：PAPER_READY
- 最新动作：OPEN_PAPER_POSITION
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T19:19:47Z｜来源：data/gmgn_candidates_live_run/tokens/EVrfnKXnX1XCT5ESvp6VJUwLFDU1Ajq1dpUrG5qUpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：SMW｜来源：data/gmgn_candidates_live_run/tokens/EVrfnKXnX1XCT5ESvp6VJUwLFDU1Ajq1dpUrG5qUpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：PAPER_READY｜来源：data/gmgn_candidates_live_run/tokens/EVrfnKXnX1XCT5ESvp6VJUwLFDU1Ajq1dpUrG5qUpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：PAPER_READY / 吸筹窗口 valid + SIKK S3/S4 + 允许纸面交易 + 仓位大于0｜来源：data/gmgn_candidates_live_run/tokens/EVrfnKXnX1XCT5ESvp6VJUwLFDU1Ajq1dpUrG5qUpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 有证据：钱包结构结论：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/EVrfnKXnX1XCT5ESvp6VJUwLFDU1Ajq1dpUrG5qUpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：quote/security 权限：ALLOW_CONFIRMATION_LAYER｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 有证据：当前状态：PAPER_READY｜来源：data/gmgn_candidates_live_run/tokens/EVrfnKXnX1XCT5ESvp6VJUwLFDU1Ajq1dpUrG5qUpump/token_status.json｜字段：current_state
- 有证据：钱包结构结论：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/EVrfnKXnX1XCT5ESvp6VJUwLFDU1Ajq1dpUrG5qUpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：钱包结构原因：对手盘压力高，接盘/套牢筹码占比偏高｜来源：data/gmgn_candidates_live_run/wallet_structure/EVrfnKXnX1XCT5ESvp6VJUwLFDU1Ajq1dpUrG5qUpump/wallet_structure_decision.json｜字段：wallet_structure_reason
- 有证据：quote/security 权限：ALLOW_CONFIRMATION_LAYER｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission

#### 为什么进入paper
- 有证据：当前状态：PAPER_READY｜来源：data/gmgn_candidates_live_run/tokens/EVrfnKXnX1XCT5ESvp6VJUwLFDU1Ajq1dpUrG5qUpump/token_status.json｜字段：current_state
- 有证据：最新动作：OPEN_PAPER_POSITION｜来源：data/gmgn_candidates_live_run/tokens/EVrfnKXnX1XCT5ESvp6VJUwLFDU1Ajq1dpUrG5qUpump/token_status.json｜字段：latest_action
- 有证据：入场依据：吸筹窗口 valid + SIKK S3/S4 + 允许纸面交易 + 仓位大于0｜来源：data/gmgn_candidates_live_run/tokens/EVrfnKXnX1XCT5ESvp6VJUwLFDU1Ajq1dpUrG5qUpump/token_status.json｜字段：latest_reason

#### 为什么退出
- 有证据：纸面退出原因：命中纸面止损｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json｜字段：exit_reason
- 有证据：纸面退出时间：2026-05-02T19:09:45Z｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json｜字段：exit_time
- 有证据：当前状态：PAPER_READY｜来源：data/gmgn_candidates_live_run/tokens/EVrfnKXnX1XCT5ESvp6VJUwLFDU1Ajq1dpUrG5qUpump/token_status.json｜字段：current_state

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：PAPER_READY / OPEN_PAPER_POSITION｜来源：data/gmgn_candidates_live_run/tokens/EVrfnKXnX1XCT5ESvp6VJUwLFDU1Ajq1dpUrG5qUpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/EVrfnKXnX1XCT5ESvp6VJUwLFDU1Ajq1dpUrG5qUpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：ALLOW_CONFIRMATION_LAYER / READY_FOR_CONFIRMATION｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/EVrfnKXnX1XCT5ESvp6VJUwLFDU1Ajq1dpUrG5qUpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/EVrfnKXnX1XCT5ESvp6VJUwLFDU1Ajq1dpUrG5qUpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/EVrfnKXnX1XCT5ESvp6VJUwLFDU1Ajq1dpUrG5qUpump/process_trace.jsonl

### VIGIL / F3iV4HCdr4rBCHmLZPEEFiLxBwznSVwPYx2AoQy5pump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/F3iV4HCdr4rBCHmLZPEEFiLxBwznSVwPYx2AoQy5pump/token_status.json｜字段：last_update
- 有证据：发现对象符号：VIGIL｜来源：data/gmgn_candidates_live_run/tokens/F3iV4HCdr4rBCHmLZPEEFiLxBwznSVwPYx2AoQy5pump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/F3iV4HCdr4rBCHmLZPEEFiLxBwznSVwPYx2AoQy5pump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / SIKK 信号仍为观察/预备层｜来源：data/gmgn_candidates_live_run/tokens/F3iV4HCdr4rBCHmLZPEEFiLxBwznSVwPYx2AoQy5pump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/F3iV4HCdr4rBCHmLZPEEFiLxBwznSVwPYx2AoQy5pump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/F3iV4HCdr4rBCHmLZPEEFiLxBwznSVwPYx2AoQy5pump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/F3iV4HCdr4rBCHmLZPEEFiLxBwznSVwPYx2AoQy5pump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/F3iV4HCdr4rBCHmLZPEEFiLxBwznSVwPYx2AoQy5pump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/F3iV4HCdr4rBCHmLZPEEFiLxBwznSVwPYx2AoQy5pump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/F3iV4HCdr4rBCHmLZPEEFiLxBwznSVwPYx2AoQy5pump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/F3iV4HCdr4rBCHmLZPEEFiLxBwznSVwPYx2AoQy5pump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/F3iV4HCdr4rBCHmLZPEEFiLxBwznSVwPYx2AoQy5pump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/F3iV4HCdr4rBCHmLZPEEFiLxBwznSVwPYx2AoQy5pump/process_trace.jsonl

### NYAN / F7ySj1p4f83fLXzdN8Dgf9UySr4MrkPVgZ1usFMzpump

- 当前状态：PAPER_OPEN
- 最新动作：HOLD
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/F7ySj1p4f83fLXzdN8Dgf9UySr4MrkPVgZ1usFMzpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：NYAN｜来源：data/gmgn_candidates_live_run/tokens/F7ySj1p4f83fLXzdN8Dgf9UySr4MrkPVgZ1usFMzpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：PAPER_OPEN｜来源：data/gmgn_candidates_live_run/tokens/F7ySj1p4f83fLXzdN8Dgf9UySr4MrkPVgZ1usFMzpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：PAPER_OPEN / 吸筹窗口 valid + SIKK S3/S4 + 允许纸面交易 + 仓位大于0｜来源：data/gmgn_candidates_live_run/tokens/F7ySj1p4f83fLXzdN8Dgf9UySr4MrkPVgZ1usFMzpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 有证据：钱包结构结论：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/F7ySj1p4f83fLXzdN8Dgf9UySr4MrkPVgZ1usFMzpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：quote/security 权限：ALLOW_CONFIRMATION_LAYER｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission
- 有证据：quote/security 原因：报价与安全扫描未触发硬阻断，可进入人工确认层｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：原因

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 有证据：当前状态：PAPER_OPEN｜来源：data/gmgn_candidates_live_run/tokens/F7ySj1p4f83fLXzdN8Dgf9UySr4MrkPVgZ1usFMzpump/token_status.json｜字段：current_state
- 有证据：钱包结构结论：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/F7ySj1p4f83fLXzdN8Dgf9UySr4MrkPVgZ1usFMzpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：钱包结构原因：发现分发侧钱包 3 个；对手盘压力高，接盘/套牢筹码占比偏高｜来源：data/gmgn_candidates_live_run/wallet_structure/F7ySj1p4f83fLXzdN8Dgf9UySr4MrkPVgZ1usFMzpump/wallet_structure_decision.json｜字段：wallet_structure_reason
- 有证据：quote/security 权限：ALLOW_CONFIRMATION_LAYER｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission

#### 为什么进入paper
- 有证据：当前状态：PAPER_OPEN｜来源：data/gmgn_candidates_live_run/tokens/F7ySj1p4f83fLXzdN8Dgf9UySr4MrkPVgZ1usFMzpump/token_status.json｜字段：current_state
- 有证据：最新动作：HOLD｜来源：data/gmgn_candidates_live_run/tokens/F7ySj1p4f83fLXzdN8Dgf9UySr4MrkPVgZ1usFMzpump/token_status.json｜字段：latest_action
- 有证据：入场依据：吸筹窗口 valid + SIKK S3/S4 + 允许纸面交易 + 仓位大于0｜来源：data/gmgn_candidates_live_run/tokens/F7ySj1p4f83fLXzdN8Dgf9UySr4MrkPVgZ1usFMzpump/token_status.json｜字段：latest_reason
- 有证据：纸面入场时间：2026-05-02 21:37:00 UTC｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json｜字段：entry_time

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：PAPER_OPEN / HOLD｜来源：data/gmgn_candidates_live_run/tokens/F7ySj1p4f83fLXzdN8Dgf9UySr4MrkPVgZ1usFMzpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/F7ySj1p4f83fLXzdN8Dgf9UySr4MrkPVgZ1usFMzpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：ALLOW_CONFIRMATION_LAYER / READY_FOR_CONFIRMATION｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/F7ySj1p4f83fLXzdN8Dgf9UySr4MrkPVgZ1usFMzpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/F7ySj1p4f83fLXzdN8Dgf9UySr4MrkPVgZ1usFMzpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/F7ySj1p4f83fLXzdN8Dgf9UySr4MrkPVgZ1usFMzpump/process_trace.jsonl

### lolcat / F8R8VWgiKHvpEh13DFtKsk5PSN7vMzzvP5mmLLUspump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/F8R8VWgiKHvpEh13DFtKsk5PSN7vMzzvP5mmLLUspump/token_status.json｜字段：last_update
- 有证据：发现对象符号：lolcat｜来源：data/gmgn_candidates_live_run/tokens/F8R8VWgiKHvpEh13DFtKsk5PSN7vMzzvP5mmLLUspump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/F8R8VWgiKHvpEh13DFtKsk5PSN7vMzzvP5mmLLUspump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/F8R8VWgiKHvpEh13DFtKsk5PSN7vMzzvP5mmLLUspump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/F8R8VWgiKHvpEh13DFtKsk5PSN7vMzzvP5mmLLUspump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/F8R8VWgiKHvpEh13DFtKsk5PSN7vMzzvP5mmLLUspump/token_status.json｜字段：current_state
- 有证据：钱包结构结论：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/F8R8VWgiKHvpEh13DFtKsk5PSN7vMzzvP5mmLLUspump/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：钱包结构原因：发现分发侧钱包 8 个；对手盘压力高，接盘/套牢筹码占比偏高｜来源：data/gmgn_candidates_live_run/wallet_structure/F8R8VWgiKHvpEh13DFtKsk5PSN7vMzzvP5mmLLUspump/wallet_structure_decision.json｜字段：wallet_structure_reason
- 有证据：quote/security 权限：MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/F8R8VWgiKHvpEh13DFtKsk5PSN7vMzzvP5mmLLUspump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 有证据：纸面退出原因：钱包结构触发纸面强制退出｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json｜字段：exit_reason
- 有证据：纸面退出时间：2026-05-02T18:48:46Z｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json｜字段：exit_time
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/F8R8VWgiKHvpEh13DFtKsk5PSN7vMzzvP5mmLLUspump/token_status.json｜字段：current_state

#### 为什么失败
- 有证据：失败类型：STRUCTURE_WEAKENING｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl｜字段：failure_type
- 有证据：失败原因：钱包结构状态变为 WALLET_BLOCK，纸面阶段直接模拟退出｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl｜字段：failure_reason
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/F8R8VWgiKHvpEh13DFtKsk5PSN7vMzzvP5mmLLUspump/token_status.json｜字段：current_state

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/F8R8VWgiKHvpEh13DFtKsk5PSN7vMzzvP5mmLLUspump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/F8R8VWgiKHvpEh13DFtKsk5PSN7vMzzvP5mmLLUspump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/F8R8VWgiKHvpEh13DFtKsk5PSN7vMzzvP5mmLLUspump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/F8R8VWgiKHvpEh13DFtKsk5PSN7vMzzvP5mmLLUspump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/F8R8VWgiKHvpEh13DFtKsk5PSN7vMzzvP5mmLLUspump/process_trace.jsonl

### DUKE / F9gvdBs5kmTuPAw8oyPkohRBvXLbtfGwUiFvgsjhpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T19:51:09Z｜来源：data/gmgn_candidates_live_run/tokens/F9gvdBs5kmTuPAw8oyPkohRBvXLbtfGwUiFvgsjhpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：DUKE｜来源：data/gmgn_candidates_live_run/tokens/F9gvdBs5kmTuPAw8oyPkohRBvXLbtfGwUiFvgsjhpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/F9gvdBs5kmTuPAw8oyPkohRBvXLbtfGwUiFvgsjhpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/F9gvdBs5kmTuPAw8oyPkohRBvXLbtfGwUiFvgsjhpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/F9gvdBs5kmTuPAw8oyPkohRBvXLbtfGwUiFvgsjhpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/F9gvdBs5kmTuPAw8oyPkohRBvXLbtfGwUiFvgsjhpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/F9gvdBs5kmTuPAw8oyPkohRBvXLbtfGwUiFvgsjhpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/F9gvdBs5kmTuPAw8oyPkohRBvXLbtfGwUiFvgsjhpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/F9gvdBs5kmTuPAw8oyPkohRBvXLbtfGwUiFvgsjhpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/F9gvdBs5kmTuPAw8oyPkohRBvXLbtfGwUiFvgsjhpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/F9gvdBs5kmTuPAw8oyPkohRBvXLbtfGwUiFvgsjhpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/F9gvdBs5kmTuPAw8oyPkohRBvXLbtfGwUiFvgsjhpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/F9gvdBs5kmTuPAw8oyPkohRBvXLbtfGwUiFvgsjhpump/process_trace.jsonl

### Chatex / FHohWwWG5gVK2RvGZPM8UhRcL1zRK3EZGTWTi9SD7fFP

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T10:58:15Z｜来源：data/gmgn_candidates_live_run/tokens/FHohWwWG5gVK2RvGZPM8UhRcL1zRK3EZGTWTi9SD7fFP/token_status.json｜字段：last_update
- 有证据：发现对象符号：Chatex｜来源：data/gmgn_candidates_live_run/tokens/FHohWwWG5gVK2RvGZPM8UhRcL1zRK3EZGTWTi9SD7fFP/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/FHohWwWG5gVK2RvGZPM8UhRcL1zRK3EZGTWTi9SD7fFP/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/FHohWwWG5gVK2RvGZPM8UhRcL1zRK3EZGTWTi9SD7fFP/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/FHohWwWG5gVK2RvGZPM8UhRcL1zRK3EZGTWTi9SD7fFP/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/FHohWwWG5gVK2RvGZPM8UhRcL1zRK3EZGTWTi9SD7fFP/token_status.json；data/gmgn_candidates_live_run/wallet_structure/FHohWwWG5gVK2RvGZPM8UhRcL1zRK3EZGTWTi9SD7fFP/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/FHohWwWG5gVK2RvGZPM8UhRcL1zRK3EZGTWTi9SD7fFP/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/FHohWwWG5gVK2RvGZPM8UhRcL1zRK3EZGTWTi9SD7fFP/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/FHohWwWG5gVK2RvGZPM8UhRcL1zRK3EZGTWTi9SD7fFP/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/FHohWwWG5gVK2RvGZPM8UhRcL1zRK3EZGTWTi9SD7fFP/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/FHohWwWG5gVK2RvGZPM8UhRcL1zRK3EZGTWTi9SD7fFP/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/FHohWwWG5gVK2RvGZPM8UhRcL1zRK3EZGTWTi9SD7fFP/process_trace.jsonl

### CLIPLIN / FVC2ExyVRMEd65nAcmiLTEeXrG9Y41LC53AWyw3Rpump

- 当前状态：BLOCKED
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T12:19:29Z｜来源：data/gmgn_candidates_live_run/tokens/FVC2ExyVRMEd65nAcmiLTEeXrG9Y41LC53AWyw3Rpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：CLIPLIN｜来源：data/gmgn_candidates_live_run/tokens/FVC2ExyVRMEd65nAcmiLTEeXrG9Y41LC53AWyw3Rpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：BLOCKED｜来源：data/gmgn_candidates_live_run/tokens/FVC2ExyVRMEd65nAcmiLTEeXrG9Y41LC53AWyw3Rpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：BLOCKED / 钱包结构门禁阻断：对手盘压力高，接盘/套牢筹码占比偏高｜来源：data/gmgn_candidates_live_run/tokens/FVC2ExyVRMEd65nAcmiLTEeXrG9Y41LC53AWyw3Rpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/FVC2ExyVRMEd65nAcmiLTEeXrG9Y41LC53AWyw3Rpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 有证据：当前状态：BLOCKED｜来源：data/gmgn_candidates_live_run/tokens/FVC2ExyVRMEd65nAcmiLTEeXrG9Y41LC53AWyw3Rpump/token_status.json｜字段：current_state
- 有证据：钱包结构结论：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/FVC2ExyVRMEd65nAcmiLTEeXrG9Y41LC53AWyw3Rpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：钱包结构原因：对手盘压力高，接盘/套牢筹码占比偏高｜来源：data/gmgn_candidates_live_run/wallet_structure/FVC2ExyVRMEd65nAcmiLTEeXrG9Y41LC53AWyw3Rpump/wallet_structure_decision.json｜字段：wallet_structure_reason
- 有证据：quote/security 权限：由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/FVC2ExyVRMEd65nAcmiLTEeXrG9Y41LC53AWyw3Rpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：BLOCKED / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/FVC2ExyVRMEd65nAcmiLTEeXrG9Y41LC53AWyw3Rpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/FVC2ExyVRMEd65nAcmiLTEeXrG9Y41LC53AWyw3Rpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/FVC2ExyVRMEd65nAcmiLTEeXrG9Y41LC53AWyw3Rpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/FVC2ExyVRMEd65nAcmiLTEeXrG9Y41LC53AWyw3Rpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/FVC2ExyVRMEd65nAcmiLTEeXrG9Y41LC53AWyw3Rpump/process_trace.jsonl

### three / FeMbDoX7R1Psc4GEcvJdsbNbZA3bfztcyDCatJVJpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/FeMbDoX7R1Psc4GEcvJdsbNbZA3bfztcyDCatJVJpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：three｜来源：data/gmgn_candidates_live_run/tokens/FeMbDoX7R1Psc4GEcvJdsbNbZA3bfztcyDCatJVJpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/FeMbDoX7R1Psc4GEcvJdsbNbZA3bfztcyDCatJVJpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/FeMbDoX7R1Psc4GEcvJdsbNbZA3bfztcyDCatJVJpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/FeMbDoX7R1Psc4GEcvJdsbNbZA3bfztcyDCatJVJpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/FeMbDoX7R1Psc4GEcvJdsbNbZA3bfztcyDCatJVJpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/FeMbDoX7R1Psc4GEcvJdsbNbZA3bfztcyDCatJVJpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/FeMbDoX7R1Psc4GEcvJdsbNbZA3bfztcyDCatJVJpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/FeMbDoX7R1Psc4GEcvJdsbNbZA3bfztcyDCatJVJpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/FeMbDoX7R1Psc4GEcvJdsbNbZA3bfztcyDCatJVJpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/FeMbDoX7R1Psc4GEcvJdsbNbZA3bfztcyDCatJVJpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/FeMbDoX7R1Psc4GEcvJdsbNbZA3bfztcyDCatJVJpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/FeMbDoX7R1Psc4GEcvJdsbNbZA3bfztcyDCatJVJpump/process_trace.jsonl

### RETArd / G7Tg9KsfQce1HZvBjXfv5ZcdKpuKzPTajhMf51nRpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/G7Tg9KsfQce1HZvBjXfv5ZcdKpuKzPTajhMf51nRpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：RETArd｜来源：data/gmgn_candidates_live_run/tokens/G7Tg9KsfQce1HZvBjXfv5ZcdKpuKzPTajhMf51nRpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/G7Tg9KsfQce1HZvBjXfv5ZcdKpuKzPTajhMf51nRpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/G7Tg9KsfQce1HZvBjXfv5ZcdKpuKzPTajhMf51nRpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/G7Tg9KsfQce1HZvBjXfv5ZcdKpuKzPTajhMf51nRpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/G7Tg9KsfQce1HZvBjXfv5ZcdKpuKzPTajhMf51nRpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/G7Tg9KsfQce1HZvBjXfv5ZcdKpuKzPTajhMf51nRpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/G7Tg9KsfQce1HZvBjXfv5ZcdKpuKzPTajhMf51nRpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/G7Tg9KsfQce1HZvBjXfv5ZcdKpuKzPTajhMf51nRpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/G7Tg9KsfQce1HZvBjXfv5ZcdKpuKzPTajhMf51nRpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/G7Tg9KsfQce1HZvBjXfv5ZcdKpuKzPTajhMf51nRpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/G7Tg9KsfQce1HZvBjXfv5ZcdKpuKzPTajhMf51nRpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/G7Tg9KsfQce1HZvBjXfv5ZcdKpuKzPTajhMf51nRpump/process_trace.jsonl

### LITH / GC3T8XboCofhBPs5U48DJgp6cxxMeu1CBZXgB2dopump

- 当前状态：UNKNOWN
- 最新动作：证据缺失/待复查
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 证据缺失/待复查：为什么发现：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/GC3T8XboCofhBPs5U48DJgp6cxxMeu1CBZXgB2dopump/token_status.json

#### 为什么观察
- 证据缺失/待复查：为什么观察：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/GC3T8XboCofhBPs5U48DJgp6cxxMeu1CBZXgB2dopump/process_trace.jsonl

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/GC3T8XboCofhBPs5U48DJgp6cxxMeu1CBZXgB2dopump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/GC3T8XboCofhBPs5U48DJgp6cxxMeu1CBZXgB2dopump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/GC3T8XboCofhBPs5U48DJgp6cxxMeu1CBZXgB2dopump/wallet_structure_decision.json

#### 为什么进入paper
- 有证据：当前状态：UNKNOWN｜来源：data/gmgn_candidates_live_run/tokens/GC3T8XboCofhBPs5U48DJgp6cxxMeu1CBZXgB2dopump/token_status.json｜字段：current_state
- 有证据：纸面入场时间：2026-04-28 17:46:00 UTC｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json｜字段：entry_time

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：UNKNOWN / 证据缺失｜来源：data/gmgn_candidates_live_run/tokens/GC3T8XboCofhBPs5U48DJgp6cxxMeu1CBZXgB2dopump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：证据缺失｜来源：data/gmgn_candidates_live_run/wallet_structure/GC3T8XboCofhBPs5U48DJgp6cxxMeu1CBZXgB2dopump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：证据缺失 / 证据缺失｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/GC3T8XboCofhBPs5U48DJgp6cxxMeu1CBZXgB2dopump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/GC3T8XboCofhBPs5U48DJgp6cxxMeu1CBZXgB2dopump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/GC3T8XboCofhBPs5U48DJgp6cxxMeu1CBZXgB2dopump/process_trace.jsonl

### monk  / GH6MV3UVLjSbY2WaMUZqEECkDFnt7W4Z7Jrij43gpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:17:29Z｜来源：data/gmgn_candidates_live_run/tokens/GH6MV3UVLjSbY2WaMUZqEECkDFnt7W4Z7Jrij43gpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：monk ｜来源：data/gmgn_candidates_live_run/tokens/GH6MV3UVLjSbY2WaMUZqEECkDFnt7W4Z7Jrij43gpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/GH6MV3UVLjSbY2WaMUZqEECkDFnt7W4Z7Jrij43gpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/GH6MV3UVLjSbY2WaMUZqEECkDFnt7W4Z7Jrij43gpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/GH6MV3UVLjSbY2WaMUZqEECkDFnt7W4Z7Jrij43gpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/GH6MV3UVLjSbY2WaMUZqEECkDFnt7W4Z7Jrij43gpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/GH6MV3UVLjSbY2WaMUZqEECkDFnt7W4Z7Jrij43gpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/GH6MV3UVLjSbY2WaMUZqEECkDFnt7W4Z7Jrij43gpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/GH6MV3UVLjSbY2WaMUZqEECkDFnt7W4Z7Jrij43gpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/GH6MV3UVLjSbY2WaMUZqEECkDFnt7W4Z7Jrij43gpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/GH6MV3UVLjSbY2WaMUZqEECkDFnt7W4Z7Jrij43gpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/GH6MV3UVLjSbY2WaMUZqEECkDFnt7W4Z7Jrij43gpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/GH6MV3UVLjSbY2WaMUZqEECkDFnt7W4Z7Jrij43gpump/process_trace.jsonl

### eBay / GKy3ZrAj7n1n47WSNMPdqH3VxEHazcsoyvhRyoKfxM3u

- 当前状态：BLOCKED
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T07:07:39Z｜来源：data/gmgn_candidates_live_run/tokens/GKy3ZrAj7n1n47WSNMPdqH3VxEHazcsoyvhRyoKfxM3u/token_status.json｜字段：last_update
- 有证据：发现对象符号：eBay｜来源：data/gmgn_candidates_live_run/tokens/GKy3ZrAj7n1n47WSNMPdqH3VxEHazcsoyvhRyoKfxM3u/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：BLOCKED｜来源：data/gmgn_candidates_live_run/tokens/GKy3ZrAj7n1n47WSNMPdqH3VxEHazcsoyvhRyoKfxM3u/token_status.json｜字段：current_state
- 有证据：最近流程记录：BLOCKED / 风险门禁阻断或 SIKK 信号 SX｜来源：data/gmgn_candidates_live_run/tokens/GKy3ZrAj7n1n47WSNMPdqH3VxEHazcsoyvhRyoKfxM3u/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/GKy3ZrAj7n1n47WSNMPdqH3VxEHazcsoyvhRyoKfxM3u/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 有证据：当前状态：BLOCKED｜来源：data/gmgn_candidates_live_run/tokens/GKy3ZrAj7n1n47WSNMPdqH3VxEHazcsoyvhRyoKfxM3u/token_status.json｜字段：current_state
- 有证据：钱包结构结论：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/GKy3ZrAj7n1n47WSNMPdqH3VxEHazcsoyvhRyoKfxM3u/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：quote/security 权限：由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/GKy3ZrAj7n1n47WSNMPdqH3VxEHazcsoyvhRyoKfxM3u/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：BLOCKED / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/GKy3ZrAj7n1n47WSNMPdqH3VxEHazcsoyvhRyoKfxM3u/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/GKy3ZrAj7n1n47WSNMPdqH3VxEHazcsoyvhRyoKfxM3u/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/GKy3ZrAj7n1n47WSNMPdqH3VxEHazcsoyvhRyoKfxM3u/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/GKy3ZrAj7n1n47WSNMPdqH3VxEHazcsoyvhRyoKfxM3u/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/GKy3ZrAj7n1n47WSNMPdqH3VxEHazcsoyvhRyoKfxM3u/process_trace.jsonl

### LUCY / GNL7MQSzzksbfuquHTJuiDPVXvXpfxBfHfu1mQGhpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T20:54:13Z｜来源：data/gmgn_candidates_live_run/tokens/GNL7MQSzzksbfuquHTJuiDPVXvXpfxBfHfu1mQGhpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：LUCY｜来源：data/gmgn_candidates_live_run/tokens/GNL7MQSzzksbfuquHTJuiDPVXvXpfxBfHfu1mQGhpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/GNL7MQSzzksbfuquHTJuiDPVXvXpfxBfHfu1mQGhpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/GNL7MQSzzksbfuquHTJuiDPVXvXpfxBfHfu1mQGhpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/GNL7MQSzzksbfuquHTJuiDPVXvXpfxBfHfu1mQGhpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/GNL7MQSzzksbfuquHTJuiDPVXvXpfxBfHfu1mQGhpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/GNL7MQSzzksbfuquHTJuiDPVXvXpfxBfHfu1mQGhpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/GNL7MQSzzksbfuquHTJuiDPVXvXpfxBfHfu1mQGhpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/GNL7MQSzzksbfuquHTJuiDPVXvXpfxBfHfu1mQGhpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/GNL7MQSzzksbfuquHTJuiDPVXvXpfxBfHfu1mQGhpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/GNL7MQSzzksbfuquHTJuiDPVXvXpfxBfHfu1mQGhpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/GNL7MQSzzksbfuquHTJuiDPVXvXpfxBfHfu1mQGhpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/GNL7MQSzzksbfuquHTJuiDPVXvXpfxBfHfu1mQGhpump/process_trace.jsonl

### musk / GUfyGEF62BUUqj5f5PveZknhBQMWWFSXm2jqAdikpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T09:32:48Z｜来源：data/gmgn_candidates_live_run/tokens/GUfyGEF62BUUqj5f5PveZknhBQMWWFSXm2jqAdikpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：musk｜来源：data/gmgn_candidates_live_run/tokens/GUfyGEF62BUUqj5f5PveZknhBQMWWFSXm2jqAdikpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/GUfyGEF62BUUqj5f5PveZknhBQMWWFSXm2jqAdikpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/GUfyGEF62BUUqj5f5PveZknhBQMWWFSXm2jqAdikpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/GUfyGEF62BUUqj5f5PveZknhBQMWWFSXm2jqAdikpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/GUfyGEF62BUUqj5f5PveZknhBQMWWFSXm2jqAdikpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/GUfyGEF62BUUqj5f5PveZknhBQMWWFSXm2jqAdikpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/GUfyGEF62BUUqj5f5PveZknhBQMWWFSXm2jqAdikpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/GUfyGEF62BUUqj5f5PveZknhBQMWWFSXm2jqAdikpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/GUfyGEF62BUUqj5f5PveZknhBQMWWFSXm2jqAdikpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/GUfyGEF62BUUqj5f5PveZknhBQMWWFSXm2jqAdikpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/GUfyGEF62BUUqj5f5PveZknhBQMWWFSXm2jqAdikpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/GUfyGEF62BUUqj5f5PveZknhBQMWWFSXm2jqAdikpump/process_trace.jsonl

### SHUSH / GVa4jr163EaBG1fv5hKFQbePKPojsoawuxdozcMSpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T21:46:26Z｜来源：data/gmgn_candidates_live_run/tokens/GVa4jr163EaBG1fv5hKFQbePKPojsoawuxdozcMSpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：SHUSH｜来源：data/gmgn_candidates_live_run/tokens/GVa4jr163EaBG1fv5hKFQbePKPojsoawuxdozcMSpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/GVa4jr163EaBG1fv5hKFQbePKPojsoawuxdozcMSpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/GVa4jr163EaBG1fv5hKFQbePKPojsoawuxdozcMSpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/GVa4jr163EaBG1fv5hKFQbePKPojsoawuxdozcMSpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/GVa4jr163EaBG1fv5hKFQbePKPojsoawuxdozcMSpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/GVa4jr163EaBG1fv5hKFQbePKPojsoawuxdozcMSpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/GVa4jr163EaBG1fv5hKFQbePKPojsoawuxdozcMSpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/GVa4jr163EaBG1fv5hKFQbePKPojsoawuxdozcMSpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/GVa4jr163EaBG1fv5hKFQbePKPojsoawuxdozcMSpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/GVa4jr163EaBG1fv5hKFQbePKPojsoawuxdozcMSpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/GVa4jr163EaBG1fv5hKFQbePKPojsoawuxdozcMSpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/GVa4jr163EaBG1fv5hKFQbePKPojsoawuxdozcMSpump/process_trace.jsonl

### GOBLIPIN / Gf94BoxxfMJMqCyvuKwnrK5pUYVNjH7KRXggEEzZpump

- 当前状态：DISCOVERED
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T10:04:43Z｜来源：data/gmgn_candidates_live_run/tokens/Gf94BoxxfMJMqCyvuKwnrK5pUYVNjH7KRXggEEzZpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：GOBLIPIN｜来源：data/gmgn_candidates_live_run/tokens/Gf94BoxxfMJMqCyvuKwnrK5pUYVNjH7KRXggEEzZpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：DISCOVERED｜来源：data/gmgn_candidates_live_run/tokens/Gf94BoxxfMJMqCyvuKwnrK5pUYVNjH7KRXggEEzZpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：DISCOVERED / GMGN 新币筛选进入候选池｜来源：data/gmgn_candidates_live_run/tokens/Gf94BoxxfMJMqCyvuKwnrK5pUYVNjH7KRXggEEzZpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/Gf94BoxxfMJMqCyvuKwnrK5pUYVNjH7KRXggEEzZpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/Gf94BoxxfMJMqCyvuKwnrK5pUYVNjH7KRXggEEzZpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/Gf94BoxxfMJMqCyvuKwnrK5pUYVNjH7KRXggEEzZpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/Gf94BoxxfMJMqCyvuKwnrK5pUYVNjH7KRXggEEzZpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：DISCOVERED / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/Gf94BoxxfMJMqCyvuKwnrK5pUYVNjH7KRXggEEzZpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/Gf94BoxxfMJMqCyvuKwnrK5pUYVNjH7KRXggEEzZpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/Gf94BoxxfMJMqCyvuKwnrK5pUYVNjH7KRXggEEzZpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/Gf94BoxxfMJMqCyvuKwnrK5pUYVNjH7KRXggEEzZpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/Gf94BoxxfMJMqCyvuKwnrK5pUYVNjH7KRXggEEzZpump/process_trace.jsonl

### RunPepe / GjTFrUsow3gcaC9m4EVRg6twauzbF4CPiwt9rtbioJK

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T11:19:44Z｜来源：data/gmgn_candidates_live_run/tokens/GjTFrUsow3gcaC9m4EVRg6twauzbF4CPiwt9rtbioJK/token_status.json｜字段：last_update
- 有证据：发现对象符号：RunPepe｜来源：data/gmgn_candidates_live_run/tokens/GjTFrUsow3gcaC9m4EVRg6twauzbF4CPiwt9rtbioJK/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/GjTFrUsow3gcaC9m4EVRg6twauzbF4CPiwt9rtbioJK/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/GjTFrUsow3gcaC9m4EVRg6twauzbF4CPiwt9rtbioJK/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/GjTFrUsow3gcaC9m4EVRg6twauzbF4CPiwt9rtbioJK/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/GjTFrUsow3gcaC9m4EVRg6twauzbF4CPiwt9rtbioJK/token_status.json；data/gmgn_candidates_live_run/wallet_structure/GjTFrUsow3gcaC9m4EVRg6twauzbF4CPiwt9rtbioJK/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/GjTFrUsow3gcaC9m4EVRg6twauzbF4CPiwt9rtbioJK/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/GjTFrUsow3gcaC9m4EVRg6twauzbF4CPiwt9rtbioJK/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/GjTFrUsow3gcaC9m4EVRg6twauzbF4CPiwt9rtbioJK/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/GjTFrUsow3gcaC9m4EVRg6twauzbF4CPiwt9rtbioJK/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/GjTFrUsow3gcaC9m4EVRg6twauzbF4CPiwt9rtbioJK/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/GjTFrUsow3gcaC9m4EVRg6twauzbF4CPiwt9rtbioJK/process_trace.jsonl

### MSTRUMP / GnqRKyQfcna6XbkoJMKkvUZUBQdtMb8oy5rH2ocpump

- 当前状态：PAPER_READY
- 最新动作：OPEN_PAPER_POSITION
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/GnqRKyQfcna6XbkoJMKkvUZUBQdtMb8oy5rH2ocpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：MSTRUMP｜来源：data/gmgn_candidates_live_run/tokens/GnqRKyQfcna6XbkoJMKkvUZUBQdtMb8oy5rH2ocpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：PAPER_READY｜来源：data/gmgn_candidates_live_run/tokens/GnqRKyQfcna6XbkoJMKkvUZUBQdtMb8oy5rH2ocpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：PAPER_READY / 吸筹窗口 valid + SIKK S3/S4 + 允许纸面交易 + 仓位大于0｜来源：data/gmgn_candidates_live_run/tokens/GnqRKyQfcna6XbkoJMKkvUZUBQdtMb8oy5rH2ocpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 有证据：钱包结构结论：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/GnqRKyQfcna6XbkoJMKkvUZUBQdtMb8oy5rH2ocpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：quote/security 权限：ALLOW_CONFIRMATION_LAYER｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission
- 有证据：quote/security 原因：报价与安全扫描未触发硬阻断，可进入人工确认层｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：原因

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 有证据：当前状态：PAPER_READY｜来源：data/gmgn_candidates_live_run/tokens/GnqRKyQfcna6XbkoJMKkvUZUBQdtMb8oy5rH2ocpump/token_status.json｜字段：current_state
- 有证据：钱包结构结论：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/GnqRKyQfcna6XbkoJMKkvUZUBQdtMb8oy5rH2ocpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：钱包结构原因：发现分发侧钱包 1 个；对手盘压力高，接盘/套牢筹码占比偏高｜来源：data/gmgn_candidates_live_run/wallet_structure/GnqRKyQfcna6XbkoJMKkvUZUBQdtMb8oy5rH2ocpump/wallet_structure_decision.json｜字段：wallet_structure_reason
- 有证据：quote/security 权限：ALLOW_CONFIRMATION_LAYER｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission

#### 为什么进入paper
- 有证据：当前状态：PAPER_READY｜来源：data/gmgn_candidates_live_run/tokens/GnqRKyQfcna6XbkoJMKkvUZUBQdtMb8oy5rH2ocpump/token_status.json｜字段：current_state
- 有证据：最新动作：OPEN_PAPER_POSITION｜来源：data/gmgn_candidates_live_run/tokens/GnqRKyQfcna6XbkoJMKkvUZUBQdtMb8oy5rH2ocpump/token_status.json｜字段：latest_action
- 有证据：入场依据：吸筹窗口 valid + SIKK S3/S4 + 允许纸面交易 + 仓位大于0｜来源：data/gmgn_candidates_live_run/tokens/GnqRKyQfcna6XbkoJMKkvUZUBQdtMb8oy5rH2ocpump/token_status.json｜字段：latest_reason

#### 为什么退出
- 有证据：纸面退出原因：钱包结构触发纸面强制退出｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json｜字段：exit_reason
- 有证据：纸面退出时间：2026-05-02T22:28:31Z｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json｜字段：exit_time
- 有证据：当前状态：PAPER_READY｜来源：data/gmgn_candidates_live_run/tokens/GnqRKyQfcna6XbkoJMKkvUZUBQdtMb8oy5rH2ocpump/token_status.json｜字段：current_state

#### 为什么失败
- 有证据：失败类型：STRUCTURE_WEAKENING｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl｜字段：failure_type
- 有证据：失败原因：钱包结构状态变为 WALLET_BLOCK，纸面阶段直接模拟退出｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl｜字段：failure_reason
- 有证据：当前状态：PAPER_READY｜来源：data/gmgn_candidates_live_run/tokens/GnqRKyQfcna6XbkoJMKkvUZUBQdtMb8oy5rH2ocpump/token_status.json｜字段：current_state

#### 下一步看什么
- 待复查：复查最新状态/动作：PAPER_READY / OPEN_PAPER_POSITION｜来源：data/gmgn_candidates_live_run/tokens/GnqRKyQfcna6XbkoJMKkvUZUBQdtMb8oy5rH2ocpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/GnqRKyQfcna6XbkoJMKkvUZUBQdtMb8oy5rH2ocpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：ALLOW_CONFIRMATION_LAYER / READY_FOR_CONFIRMATION｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/GnqRKyQfcna6XbkoJMKkvUZUBQdtMb8oy5rH2ocpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/GnqRKyQfcna6XbkoJMKkvUZUBQdtMb8oy5rH2ocpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/GnqRKyQfcna6XbkoJMKkvUZUBQdtMb8oy5rH2ocpump/process_trace.jsonl

### ROSE / Gr5N2EecbtP4156TWvKaHH4fy2rn8TH2M7cAaTpdpump

- 当前状态：BLOCKED
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T11:09:01Z｜来源：data/gmgn_candidates_live_run/tokens/Gr5N2EecbtP4156TWvKaHH4fy2rn8TH2M7cAaTpdpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：ROSE｜来源：data/gmgn_candidates_live_run/tokens/Gr5N2EecbtP4156TWvKaHH4fy2rn8TH2M7cAaTpdpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：BLOCKED｜来源：data/gmgn_candidates_live_run/tokens/Gr5N2EecbtP4156TWvKaHH4fy2rn8TH2M7cAaTpdpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：BLOCKED / 钱包结构门禁阻断：发现分发侧钱包 2 个；对手盘压力高，接盘/套牢筹码占比偏高｜来源：data/gmgn_candidates_live_run/tokens/Gr5N2EecbtP4156TWvKaHH4fy2rn8TH2M7cAaTpdpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/Gr5N2EecbtP4156TWvKaHH4fy2rn8TH2M7cAaTpdpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 有证据：当前状态：BLOCKED｜来源：data/gmgn_candidates_live_run/tokens/Gr5N2EecbtP4156TWvKaHH4fy2rn8TH2M7cAaTpdpump/token_status.json｜字段：current_state
- 有证据：钱包结构结论：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/Gr5N2EecbtP4156TWvKaHH4fy2rn8TH2M7cAaTpdpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：钱包结构原因：发现分发侧钱包 2 个；对手盘压力高，接盘/套牢筹码占比偏高｜来源：data/gmgn_candidates_live_run/wallet_structure/Gr5N2EecbtP4156TWvKaHH4fy2rn8TH2M7cAaTpdpump/wallet_structure_decision.json｜字段：wallet_structure_reason
- 有证据：quote/security 权限：由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/Gr5N2EecbtP4156TWvKaHH4fy2rn8TH2M7cAaTpdpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：BLOCKED / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/Gr5N2EecbtP4156TWvKaHH4fy2rn8TH2M7cAaTpdpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/Gr5N2EecbtP4156TWvKaHH4fy2rn8TH2M7cAaTpdpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/Gr5N2EecbtP4156TWvKaHH4fy2rn8TH2M7cAaTpdpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/Gr5N2EecbtP4156TWvKaHH4fy2rn8TH2M7cAaTpdpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/Gr5N2EecbtP4156TWvKaHH4fy2rn8TH2M7cAaTpdpump/process_trace.jsonl

### Octopus / HDG8Ng6YLpiYXzBASD1Zd5Wh7T8DHRYFcbf4YGuvpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/HDG8Ng6YLpiYXzBASD1Zd5Wh7T8DHRYFcbf4YGuvpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：Octopus｜来源：data/gmgn_candidates_live_run/tokens/HDG8Ng6YLpiYXzBASD1Zd5Wh7T8DHRYFcbf4YGuvpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/HDG8Ng6YLpiYXzBASD1Zd5Wh7T8DHRYFcbf4YGuvpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/HDG8Ng6YLpiYXzBASD1Zd5Wh7T8DHRYFcbf4YGuvpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/HDG8Ng6YLpiYXzBASD1Zd5Wh7T8DHRYFcbf4YGuvpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/HDG8Ng6YLpiYXzBASD1Zd5Wh7T8DHRYFcbf4YGuvpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/HDG8Ng6YLpiYXzBASD1Zd5Wh7T8DHRYFcbf4YGuvpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/HDG8Ng6YLpiYXzBASD1Zd5Wh7T8DHRYFcbf4YGuvpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/HDG8Ng6YLpiYXzBASD1Zd5Wh7T8DHRYFcbf4YGuvpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/HDG8Ng6YLpiYXzBASD1Zd5Wh7T8DHRYFcbf4YGuvpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/HDG8Ng6YLpiYXzBASD1Zd5Wh7T8DHRYFcbf4YGuvpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/HDG8Ng6YLpiYXzBASD1Zd5Wh7T8DHRYFcbf4YGuvpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/HDG8Ng6YLpiYXzBASD1Zd5Wh7T8DHRYFcbf4YGuvpump/process_trace.jsonl

### MSPAINTIFY / HDmojpFZvf1F421Gev2hh2p1ThaVbWsW5qh9C5Bipump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/HDmojpFZvf1F421Gev2hh2p1ThaVbWsW5qh9C5Bipump/token_status.json｜字段：last_update
- 有证据：发现对象符号：MSPAINTIFY｜来源：data/gmgn_candidates_live_run/tokens/HDmojpFZvf1F421Gev2hh2p1ThaVbWsW5qh9C5Bipump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/HDmojpFZvf1F421Gev2hh2p1ThaVbWsW5qh9C5Bipump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/HDmojpFZvf1F421Gev2hh2p1ThaVbWsW5qh9C5Bipump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/HDmojpFZvf1F421Gev2hh2p1ThaVbWsW5qh9C5Bipump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/HDmojpFZvf1F421Gev2hh2p1ThaVbWsW5qh9C5Bipump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/HDmojpFZvf1F421Gev2hh2p1ThaVbWsW5qh9C5Bipump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/HDmojpFZvf1F421Gev2hh2p1ThaVbWsW5qh9C5Bipump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/HDmojpFZvf1F421Gev2hh2p1ThaVbWsW5qh9C5Bipump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/HDmojpFZvf1F421Gev2hh2p1ThaVbWsW5qh9C5Bipump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/HDmojpFZvf1F421Gev2hh2p1ThaVbWsW5qh9C5Bipump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/HDmojpFZvf1F421Gev2hh2p1ThaVbWsW5qh9C5Bipump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/HDmojpFZvf1F421Gev2hh2p1ThaVbWsW5qh9C5Bipump/process_trace.jsonl

### 67GOBLIN / HLqP7mJPtTtRedrepL3nza8uiTPvGv1BYDQnVYbcpump

- 当前状态：BLOCKED
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T10:04:43Z｜来源：data/gmgn_candidates_live_run/tokens/HLqP7mJPtTtRedrepL3nza8uiTPvGv1BYDQnVYbcpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：67GOBLIN｜来源：data/gmgn_candidates_live_run/tokens/HLqP7mJPtTtRedrepL3nza8uiTPvGv1BYDQnVYbcpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：BLOCKED｜来源：data/gmgn_candidates_live_run/tokens/HLqP7mJPtTtRedrepL3nza8uiTPvGv1BYDQnVYbcpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：BLOCKED / 吸筹窗口 invalid，进入风险阻断观察｜来源：data/gmgn_candidates_live_run/tokens/HLqP7mJPtTtRedrepL3nza8uiTPvGv1BYDQnVYbcpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/HLqP7mJPtTtRedrepL3nza8uiTPvGv1BYDQnVYbcpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 有证据：当前状态：BLOCKED｜来源：data/gmgn_candidates_live_run/tokens/HLqP7mJPtTtRedrepL3nza8uiTPvGv1BYDQnVYbcpump/token_status.json｜字段：current_state
- 有证据：钱包结构结论：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/HLqP7mJPtTtRedrepL3nza8uiTPvGv1BYDQnVYbcpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：quote/security 权限：由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/HLqP7mJPtTtRedrepL3nza8uiTPvGv1BYDQnVYbcpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：BLOCKED / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/HLqP7mJPtTtRedrepL3nza8uiTPvGv1BYDQnVYbcpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/HLqP7mJPtTtRedrepL3nza8uiTPvGv1BYDQnVYbcpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/HLqP7mJPtTtRedrepL3nza8uiTPvGv1BYDQnVYbcpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/HLqP7mJPtTtRedrepL3nza8uiTPvGv1BYDQnVYbcpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/HLqP7mJPtTtRedrepL3nza8uiTPvGv1BYDQnVYbcpump/process_trace.jsonl

### Spirit / HXzqEEUjQ6JevbrJiMBAwoiCVikZb93XHmYtde4iCA3G

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/HXzqEEUjQ6JevbrJiMBAwoiCVikZb93XHmYtde4iCA3G/token_status.json｜字段：last_update
- 有证据：发现对象符号：Spirit｜来源：data/gmgn_candidates_live_run/tokens/HXzqEEUjQ6JevbrJiMBAwoiCVikZb93XHmYtde4iCA3G/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/HXzqEEUjQ6JevbrJiMBAwoiCVikZb93XHmYtde4iCA3G/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/HXzqEEUjQ6JevbrJiMBAwoiCVikZb93XHmYtde4iCA3G/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/HXzqEEUjQ6JevbrJiMBAwoiCVikZb93XHmYtde4iCA3G/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/HXzqEEUjQ6JevbrJiMBAwoiCVikZb93XHmYtde4iCA3G/token_status.json；data/gmgn_candidates_live_run/wallet_structure/HXzqEEUjQ6JevbrJiMBAwoiCVikZb93XHmYtde4iCA3G/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/HXzqEEUjQ6JevbrJiMBAwoiCVikZb93XHmYtde4iCA3G/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/HXzqEEUjQ6JevbrJiMBAwoiCVikZb93XHmYtde4iCA3G/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/HXzqEEUjQ6JevbrJiMBAwoiCVikZb93XHmYtde4iCA3G/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/HXzqEEUjQ6JevbrJiMBAwoiCVikZb93XHmYtde4iCA3G/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/HXzqEEUjQ6JevbrJiMBAwoiCVikZb93XHmYtde4iCA3G/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/HXzqEEUjQ6JevbrJiMBAwoiCVikZb93XHmYtde4iCA3G/process_trace.jsonl

### FOFAR / Ha5Z2DfRv6Ar2nAeBLCGWHqzwXKL3of4DqKwzzwpump

- 当前状态：BLOCKED
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T09:54:07Z｜来源：data/gmgn_candidates_live_run/tokens/Ha5Z2DfRv6Ar2nAeBLCGWHqzwXKL3of4DqKwzzwpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：FOFAR｜来源：data/gmgn_candidates_live_run/tokens/Ha5Z2DfRv6Ar2nAeBLCGWHqzwXKL3of4DqKwzzwpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：BLOCKED｜来源：data/gmgn_candidates_live_run/tokens/Ha5Z2DfRv6Ar2nAeBLCGWHqzwXKL3of4DqKwzzwpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：BLOCKED / 吸筹窗口 invalid，进入风险阻断观察｜来源：data/gmgn_candidates_live_run/tokens/Ha5Z2DfRv6Ar2nAeBLCGWHqzwXKL3of4DqKwzzwpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/Ha5Z2DfRv6Ar2nAeBLCGWHqzwXKL3of4DqKwzzwpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 有证据：当前状态：BLOCKED｜来源：data/gmgn_candidates_live_run/tokens/Ha5Z2DfRv6Ar2nAeBLCGWHqzwXKL3of4DqKwzzwpump/token_status.json｜字段：current_state
- 有证据：钱包结构结论：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/Ha5Z2DfRv6Ar2nAeBLCGWHqzwXKL3of4DqKwzzwpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：quote/security 权限：由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/Ha5Z2DfRv6Ar2nAeBLCGWHqzwXKL3of4DqKwzzwpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：BLOCKED / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/Ha5Z2DfRv6Ar2nAeBLCGWHqzwXKL3of4DqKwzzwpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/Ha5Z2DfRv6Ar2nAeBLCGWHqzwXKL3of4DqKwzzwpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/Ha5Z2DfRv6Ar2nAeBLCGWHqzwXKL3of4DqKwzzwpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/Ha5Z2DfRv6Ar2nAeBLCGWHqzwXKL3of4DqKwzzwpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/Ha5Z2DfRv6Ar2nAeBLCGWHqzwXKL3of4DqKwzzwpump/process_trace.jsonl

### CRACKROCK / HdRFFy6Sm42rDAPLGRAZ1YymtpLukziwBrE9QGs4pump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T21:46:26Z｜来源：data/gmgn_candidates_live_run/tokens/HdRFFy6Sm42rDAPLGRAZ1YymtpLukziwBrE9QGs4pump/token_status.json｜字段：last_update
- 有证据：发现对象符号：CRACKROCK｜来源：data/gmgn_candidates_live_run/tokens/HdRFFy6Sm42rDAPLGRAZ1YymtpLukziwBrE9QGs4pump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/HdRFFy6Sm42rDAPLGRAZ1YymtpLukziwBrE9QGs4pump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/HdRFFy6Sm42rDAPLGRAZ1YymtpLukziwBrE9QGs4pump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/HdRFFy6Sm42rDAPLGRAZ1YymtpLukziwBrE9QGs4pump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/HdRFFy6Sm42rDAPLGRAZ1YymtpLukziwBrE9QGs4pump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/HdRFFy6Sm42rDAPLGRAZ1YymtpLukziwBrE9QGs4pump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/HdRFFy6Sm42rDAPLGRAZ1YymtpLukziwBrE9QGs4pump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/HdRFFy6Sm42rDAPLGRAZ1YymtpLukziwBrE9QGs4pump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/HdRFFy6Sm42rDAPLGRAZ1YymtpLukziwBrE9QGs4pump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/HdRFFy6Sm42rDAPLGRAZ1YymtpLukziwBrE9QGs4pump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/HdRFFy6Sm42rDAPLGRAZ1YymtpLukziwBrE9QGs4pump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/HdRFFy6Sm42rDAPLGRAZ1YymtpLukziwBrE9QGs4pump/process_trace.jsonl

### ODAI / HxFSWTJE3SeUCgsKJUcuGQYAiH4S4BFEnSoktfKLpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T13:54:08Z｜来源：data/gmgn_candidates_live_run/tokens/HxFSWTJE3SeUCgsKJUcuGQYAiH4S4BFEnSoktfKLpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：ODAI｜来源：data/gmgn_candidates_live_run/tokens/HxFSWTJE3SeUCgsKJUcuGQYAiH4S4BFEnSoktfKLpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/HxFSWTJE3SeUCgsKJUcuGQYAiH4S4BFEnSoktfKLpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/HxFSWTJE3SeUCgsKJUcuGQYAiH4S4BFEnSoktfKLpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/HxFSWTJE3SeUCgsKJUcuGQYAiH4S4BFEnSoktfKLpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/HxFSWTJE3SeUCgsKJUcuGQYAiH4S4BFEnSoktfKLpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/HxFSWTJE3SeUCgsKJUcuGQYAiH4S4BFEnSoktfKLpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/HxFSWTJE3SeUCgsKJUcuGQYAiH4S4BFEnSoktfKLpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/HxFSWTJE3SeUCgsKJUcuGQYAiH4S4BFEnSoktfKLpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/HxFSWTJE3SeUCgsKJUcuGQYAiH4S4BFEnSoktfKLpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/HxFSWTJE3SeUCgsKJUcuGQYAiH4S4BFEnSoktfKLpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/HxFSWTJE3SeUCgsKJUcuGQYAiH4S4BFEnSoktfKLpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/HxFSWTJE3SeUCgsKJUcuGQYAiH4S4BFEnSoktfKLpump/process_trace.jsonl

### 小丫头 / J1UpPrMTEv2sNPFtB8ecyc4YScvrYoZJ7iriWJnwpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/J1UpPrMTEv2sNPFtB8ecyc4YScvrYoZJ7iriWJnwpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：小丫头｜来源：data/gmgn_candidates_live_run/tokens/J1UpPrMTEv2sNPFtB8ecyc4YScvrYoZJ7iriWJnwpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/J1UpPrMTEv2sNPFtB8ecyc4YScvrYoZJ7iriWJnwpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/J1UpPrMTEv2sNPFtB8ecyc4YScvrYoZJ7iriWJnwpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/J1UpPrMTEv2sNPFtB8ecyc4YScvrYoZJ7iriWJnwpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/J1UpPrMTEv2sNPFtB8ecyc4YScvrYoZJ7iriWJnwpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/J1UpPrMTEv2sNPFtB8ecyc4YScvrYoZJ7iriWJnwpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/J1UpPrMTEv2sNPFtB8ecyc4YScvrYoZJ7iriWJnwpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/J1UpPrMTEv2sNPFtB8ecyc4YScvrYoZJ7iriWJnwpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/J1UpPrMTEv2sNPFtB8ecyc4YScvrYoZJ7iriWJnwpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/J1UpPrMTEv2sNPFtB8ecyc4YScvrYoZJ7iriWJnwpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/J1UpPrMTEv2sNPFtB8ecyc4YScvrYoZJ7iriWJnwpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/J1UpPrMTEv2sNPFtB8ecyc4YScvrYoZJ7iriWJnwpump/process_trace.jsonl

### WINNING / JAxMg5ErnK6ji37TnUh89yA2mouDkFVpiKGaEi1mpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/JAxMg5ErnK6ji37TnUh89yA2mouDkFVpiKGaEi1mpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：WINNING｜来源：data/gmgn_candidates_live_run/tokens/JAxMg5ErnK6ji37TnUh89yA2mouDkFVpiKGaEi1mpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/JAxMg5ErnK6ji37TnUh89yA2mouDkFVpiKGaEi1mpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/JAxMg5ErnK6ji37TnUh89yA2mouDkFVpiKGaEi1mpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/JAxMg5ErnK6ji37TnUh89yA2mouDkFVpiKGaEi1mpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/JAxMg5ErnK6ji37TnUh89yA2mouDkFVpiKGaEi1mpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/JAxMg5ErnK6ji37TnUh89yA2mouDkFVpiKGaEi1mpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/JAxMg5ErnK6ji37TnUh89yA2mouDkFVpiKGaEi1mpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/JAxMg5ErnK6ji37TnUh89yA2mouDkFVpiKGaEi1mpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/JAxMg5ErnK6ji37TnUh89yA2mouDkFVpiKGaEi1mpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/JAxMg5ErnK6ji37TnUh89yA2mouDkFVpiKGaEi1mpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/JAxMg5ErnK6ji37TnUh89yA2mouDkFVpiKGaEi1mpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/JAxMg5ErnK6ji37TnUh89yA2mouDkFVpiKGaEi1mpump/process_trace.jsonl

### UNITED / LzxN1DNn3qNdLw7VKYvxBqvWMY45rhTeq4KoytyLUSA

- 当前状态：PAPER_READY
- 最新动作：WAIT_QUOTE
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/LzxN1DNn3qNdLw7VKYvxBqvWMY45rhTeq4KoytyLUSA/token_status.json｜字段：last_update
- 有证据：发现对象符号：UNITED｜来源：data/gmgn_candidates_live_run/tokens/LzxN1DNn3qNdLw7VKYvxBqvWMY45rhTeq4KoytyLUSA/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：PAPER_READY｜来源：data/gmgn_candidates_live_run/tokens/LzxN1DNn3qNdLw7VKYvxBqvWMY45rhTeq4KoytyLUSA/token_status.json｜字段：current_state
- 有证据：最近流程记录：PAPER_READY / 吸筹窗口 valid + SIKK S3/S4 + 允许纸面交易 + 仓位大于0｜来源：data/gmgn_candidates_live_run/tokens/LzxN1DNn3qNdLw7VKYvxBqvWMY45rhTeq4KoytyLUSA/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/LzxN1DNn3qNdLw7VKYvxBqvWMY45rhTeq4KoytyLUSA/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 有证据：quote/security 权限：PAUSE_NEED_CONFIRM｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission
- 有证据：安全层状态：PAUSE｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：交易前状态
- 有证据：暂停原因：OKX 中等风险：无标签明细｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：原因

#### 为什么阻断
- 有证据：当前状态：PAPER_READY｜来源：data/gmgn_candidates_live_run/tokens/LzxN1DNn3qNdLw7VKYvxBqvWMY45rhTeq4KoytyLUSA/token_status.json｜字段：current_state
- 有证据：钱包结构结论：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/LzxN1DNn3qNdLw7VKYvxBqvWMY45rhTeq4KoytyLUSA/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：钱包结构原因：发现分发侧钱包 15 个；对手盘压力高，接盘/套牢筹码占比偏高｜来源：data/gmgn_candidates_live_run/wallet_structure/LzxN1DNn3qNdLw7VKYvxBqvWMY45rhTeq4KoytyLUSA/wallet_structure_decision.json｜字段：wallet_structure_reason
- 有证据：quote/security 权限：PAUSE_NEED_CONFIRM｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission

#### 为什么进入paper
- 有证据：当前状态：PAPER_READY｜来源：data/gmgn_candidates_live_run/tokens/LzxN1DNn3qNdLw7VKYvxBqvWMY45rhTeq4KoytyLUSA/token_status.json｜字段：current_state
- 有证据：最新动作：WAIT_QUOTE｜来源：data/gmgn_candidates_live_run/tokens/LzxN1DNn3qNdLw7VKYvxBqvWMY45rhTeq4KoytyLUSA/token_status.json｜字段：latest_action
- 有证据：入场依据：吸筹窗口 valid + SIKK S3/S4 + 允许纸面交易 + 仓位大于0｜来源：data/gmgn_candidates_live_run/tokens/LzxN1DNn3qNdLw7VKYvxBqvWMY45rhTeq4KoytyLUSA/token_status.json｜字段：latest_reason

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：PAPER_READY / WAIT_QUOTE｜来源：data/gmgn_candidates_live_run/tokens/LzxN1DNn3qNdLw7VKYvxBqvWMY45rhTeq4KoytyLUSA/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/LzxN1DNn3qNdLw7VKYvxBqvWMY45rhTeq4KoytyLUSA/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：PAUSE_NEED_CONFIRM / PAUSE｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/LzxN1DNn3qNdLw7VKYvxBqvWMY45rhTeq4KoytyLUSA/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/LzxN1DNn3qNdLw7VKYvxBqvWMY45rhTeq4KoytyLUSA/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/LzxN1DNn3qNdLw7VKYvxBqvWMY45rhTeq4KoytyLUSA/process_trace.jsonl

### PXC / PXCgWpfDv6hnNE9rac8qTk6Z1zWKJrRUcfjkVQWpXm7

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T11:41:02Z｜来源：data/gmgn_candidates_live_run/tokens/PXCgWpfDv6hnNE9rac8qTk6Z1zWKJrRUcfjkVQWpXm7/token_status.json｜字段：last_update
- 有证据：发现对象符号：PXC｜来源：data/gmgn_candidates_live_run/tokens/PXCgWpfDv6hnNE9rac8qTk6Z1zWKJrRUcfjkVQWpXm7/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/PXCgWpfDv6hnNE9rac8qTk6Z1zWKJrRUcfjkVQWpXm7/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/PXCgWpfDv6hnNE9rac8qTk6Z1zWKJrRUcfjkVQWpXm7/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/PXCgWpfDv6hnNE9rac8qTk6Z1zWKJrRUcfjkVQWpXm7/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/PXCgWpfDv6hnNE9rac8qTk6Z1zWKJrRUcfjkVQWpXm7/token_status.json；data/gmgn_candidates_live_run/wallet_structure/PXCgWpfDv6hnNE9rac8qTk6Z1zWKJrRUcfjkVQWpXm7/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/PXCgWpfDv6hnNE9rac8qTk6Z1zWKJrRUcfjkVQWpXm7/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/PXCgWpfDv6hnNE9rac8qTk6Z1zWKJrRUcfjkVQWpXm7/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/PXCgWpfDv6hnNE9rac8qTk6Z1zWKJrRUcfjkVQWpXm7/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/PXCgWpfDv6hnNE9rac8qTk6Z1zWKJrRUcfjkVQWpXm7/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/PXCgWpfDv6hnNE9rac8qTk6Z1zWKJrRUcfjkVQWpXm7/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/PXCgWpfDv6hnNE9rac8qTk6Z1zWKJrRUcfjkVQWpXm7/process_trace.jsonl

### WINNING / W1NqGUNfaxJpiKeeu9p8yxZNomPaC1ugLHeZ5ZvKC4m

- 当前状态：BLOCKED
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T19:19:47Z｜来源：data/gmgn_candidates_live_run/tokens/W1NqGUNfaxJpiKeeu9p8yxZNomPaC1ugLHeZ5ZvKC4m/token_status.json｜字段：last_update
- 有证据：发现对象符号：WINNING｜来源：data/gmgn_candidates_live_run/tokens/W1NqGUNfaxJpiKeeu9p8yxZNomPaC1ugLHeZ5ZvKC4m/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：BLOCKED｜来源：data/gmgn_candidates_live_run/tokens/W1NqGUNfaxJpiKeeu9p8yxZNomPaC1ugLHeZ5ZvKC4m/token_status.json｜字段：current_state
- 有证据：最近流程记录：BLOCKED / 吸筹窗口 invalid，进入风险阻断观察｜来源：data/gmgn_candidates_live_run/tokens/W1NqGUNfaxJpiKeeu9p8yxZNomPaC1ugLHeZ5ZvKC4m/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/W1NqGUNfaxJpiKeeu9p8yxZNomPaC1ugLHeZ5ZvKC4m/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 有证据：当前状态：BLOCKED｜来源：data/gmgn_candidates_live_run/tokens/W1NqGUNfaxJpiKeeu9p8yxZNomPaC1ugLHeZ5ZvKC4m/token_status.json｜字段：current_state
- 有证据：钱包结构结论：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/W1NqGUNfaxJpiKeeu9p8yxZNomPaC1ugLHeZ5ZvKC4m/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：钱包结构原因：发现分发侧钱包 30 个；对手盘压力高，接盘/套牢筹码占比偏高｜来源：data/gmgn_candidates_live_run/wallet_structure/W1NqGUNfaxJpiKeeu9p8yxZNomPaC1ugLHeZ5ZvKC4m/wallet_structure_decision.json｜字段：wallet_structure_reason
- 有证据：quote/security 权限：MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/W1NqGUNfaxJpiKeeu9p8yxZNomPaC1ugLHeZ5ZvKC4m/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 有证据：纸面退出原因：命中纸面止损｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json｜字段：exit_reason
- 有证据：纸面退出时间：2026-05-02T18:38:16Z｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json｜字段：exit_time
- 有证据：当前状态：BLOCKED｜来源：data/gmgn_candidates_live_run/tokens/W1NqGUNfaxJpiKeeu9p8yxZNomPaC1ugLHeZ5ZvKC4m/token_status.json｜字段：current_state

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：BLOCKED / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/W1NqGUNfaxJpiKeeu9p8yxZNomPaC1ugLHeZ5ZvKC4m/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/W1NqGUNfaxJpiKeeu9p8yxZNomPaC1ugLHeZ5ZvKC4m/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/W1NqGUNfaxJpiKeeu9p8yxZNomPaC1ugLHeZ5ZvKC4m/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/W1NqGUNfaxJpiKeeu9p8yxZNomPaC1ugLHeZ5ZvKC4m/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/W1NqGUNfaxJpiKeeu9p8yxZNomPaC1ugLHeZ5ZvKC4m/process_trace.jsonl

### CHADLON / hLokvfUnqYUztoVdA4gwZnpvTKsPNefkdn2DyxGpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/hLokvfUnqYUztoVdA4gwZnpvTKsPNefkdn2DyxGpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：CHADLON｜来源：data/gmgn_candidates_live_run/tokens/hLokvfUnqYUztoVdA4gwZnpvTKsPNefkdn2DyxGpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/hLokvfUnqYUztoVdA4gwZnpvTKsPNefkdn2DyxGpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/hLokvfUnqYUztoVdA4gwZnpvTKsPNefkdn2DyxGpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/hLokvfUnqYUztoVdA4gwZnpvTKsPNefkdn2DyxGpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/hLokvfUnqYUztoVdA4gwZnpvTKsPNefkdn2DyxGpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/hLokvfUnqYUztoVdA4gwZnpvTKsPNefkdn2DyxGpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/hLokvfUnqYUztoVdA4gwZnpvTKsPNefkdn2DyxGpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/hLokvfUnqYUztoVdA4gwZnpvTKsPNefkdn2DyxGpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/hLokvfUnqYUztoVdA4gwZnpvTKsPNefkdn2DyxGpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/hLokvfUnqYUztoVdA4gwZnpvTKsPNefkdn2DyxGpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/hLokvfUnqYUztoVdA4gwZnpvTKsPNefkdn2DyxGpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/hLokvfUnqYUztoVdA4gwZnpvTKsPNefkdn2DyxGpump/process_trace.jsonl

### RJGN / hpvoUYjKkvy2hyqC7444mU6eXFD3ETZW4tLd6Dapump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/hpvoUYjKkvy2hyqC7444mU6eXFD3ETZW4tLd6Dapump/token_status.json｜字段：last_update
- 有证据：发现对象符号：RJGN｜来源：data/gmgn_candidates_live_run/tokens/hpvoUYjKkvy2hyqC7444mU6eXFD3ETZW4tLd6Dapump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/hpvoUYjKkvy2hyqC7444mU6eXFD3ETZW4tLd6Dapump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/hpvoUYjKkvy2hyqC7444mU6eXFD3ETZW4tLd6Dapump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/hpvoUYjKkvy2hyqC7444mU6eXFD3ETZW4tLd6Dapump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/hpvoUYjKkvy2hyqC7444mU6eXFD3ETZW4tLd6Dapump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/hpvoUYjKkvy2hyqC7444mU6eXFD3ETZW4tLd6Dapump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/hpvoUYjKkvy2hyqC7444mU6eXFD3ETZW4tLd6Dapump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/hpvoUYjKkvy2hyqC7444mU6eXFD3ETZW4tLd6Dapump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/hpvoUYjKkvy2hyqC7444mU6eXFD3ETZW4tLd6Dapump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/hpvoUYjKkvy2hyqC7444mU6eXFD3ETZW4tLd6Dapump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/hpvoUYjKkvy2hyqC7444mU6eXFD3ETZW4tLd6Dapump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/hpvoUYjKkvy2hyqC7444mU6eXFD3ETZW4tLd6Dapump/process_trace.jsonl

### NKT / iBcavzgHdvaHHEM6Tdm9UsRqEJu2iQRac3cjinbpump

- 当前状态：BLOCKED
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T11:51:43Z｜来源：data/gmgn_candidates_live_run/tokens/iBcavzgHdvaHHEM6Tdm9UsRqEJu2iQRac3cjinbpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：NKT｜来源：data/gmgn_candidates_live_run/tokens/iBcavzgHdvaHHEM6Tdm9UsRqEJu2iQRac3cjinbpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：BLOCKED｜来源：data/gmgn_candidates_live_run/tokens/iBcavzgHdvaHHEM6Tdm9UsRqEJu2iQRac3cjinbpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：BLOCKED / 钱包结构门禁阻断：发现分发侧钱包 2 个；对手盘压力高，接盘/套牢筹码占比偏高｜来源：data/gmgn_candidates_live_run/tokens/iBcavzgHdvaHHEM6Tdm9UsRqEJu2iQRac3cjinbpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/iBcavzgHdvaHHEM6Tdm9UsRqEJu2iQRac3cjinbpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 有证据：当前状态：BLOCKED｜来源：data/gmgn_candidates_live_run/tokens/iBcavzgHdvaHHEM6Tdm9UsRqEJu2iQRac3cjinbpump/token_status.json｜字段：current_state
- 有证据：钱包结构结论：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/iBcavzgHdvaHHEM6Tdm9UsRqEJu2iQRac3cjinbpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 有证据：钱包结构原因：发现分发侧钱包 2 个；对手盘压力高，接盘/套牢筹码占比偏高｜来源：data/gmgn_candidates_live_run/wallet_structure/iBcavzgHdvaHHEM6Tdm9UsRqEJu2iQRac3cjinbpump/wallet_structure_decision.json｜字段：wallet_structure_reason
- 有证据：quote/security 权限：由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/iBcavzgHdvaHHEM6Tdm9UsRqEJu2iQRac3cjinbpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：BLOCKED / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/iBcavzgHdvaHHEM6Tdm9UsRqEJu2iQRac3cjinbpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：WALLET_BLOCK｜来源：data/gmgn_candidates_live_run/wallet_structure/iBcavzgHdvaHHEM6Tdm9UsRqEJu2iQRac3cjinbpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：由 quote_security/candidate_quote_security_summary.json 提供 / 由 quote_security/candidate_quote_security_summary.json 提供｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/iBcavzgHdvaHHEM6Tdm9UsRqEJu2iQRac3cjinbpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/iBcavzgHdvaHHEM6Tdm9UsRqEJu2iQRac3cjinbpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/iBcavzgHdvaHHEM6Tdm9UsRqEJu2iQRac3cjinbpump/process_trace.jsonl

### GETTER / uEBgmzYWX8RnJVPkkg7eoEtPSUQoxMPWBjyGqCipump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T20:33:17Z｜来源：data/gmgn_candidates_live_run/tokens/uEBgmzYWX8RnJVPkkg7eoEtPSUQoxMPWBjyGqCipump/token_status.json｜字段：last_update
- 有证据：发现对象符号：GETTER｜来源：data/gmgn_candidates_live_run/tokens/uEBgmzYWX8RnJVPkkg7eoEtPSUQoxMPWBjyGqCipump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/uEBgmzYWX8RnJVPkkg7eoEtPSUQoxMPWBjyGqCipump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/uEBgmzYWX8RnJVPkkg7eoEtPSUQoxMPWBjyGqCipump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/uEBgmzYWX8RnJVPkkg7eoEtPSUQoxMPWBjyGqCipump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/uEBgmzYWX8RnJVPkkg7eoEtPSUQoxMPWBjyGqCipump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/uEBgmzYWX8RnJVPkkg7eoEtPSUQoxMPWBjyGqCipump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/uEBgmzYWX8RnJVPkkg7eoEtPSUQoxMPWBjyGqCipump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/uEBgmzYWX8RnJVPkkg7eoEtPSUQoxMPWBjyGqCipump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/uEBgmzYWX8RnJVPkkg7eoEtPSUQoxMPWBjyGqCipump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/uEBgmzYWX8RnJVPkkg7eoEtPSUQoxMPWBjyGqCipump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/uEBgmzYWX8RnJVPkkg7eoEtPSUQoxMPWBjyGqCipump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/uEBgmzYWX8RnJVPkkg7eoEtPSUQoxMPWBjyGqCipump/process_trace.jsonl

### ELIENUS / yrKmZe5x2YBp1P6ufKLUCNifPbqxwHiwsbfDRWBpump

- 当前状态：WATCHING
- 最新动作：LIVE_RUN_SYNC
- 说明：只解释已有结果，不重新裁决。

#### 为什么发现
- 有证据：token_status 出现/更新时间：2026-05-02T22:27:58Z｜来源：data/gmgn_candidates_live_run/tokens/yrKmZe5x2YBp1P6ufKLUCNifPbqxwHiwsbfDRWBpump/token_status.json｜字段：last_update
- 有证据：发现对象符号：ELIENUS｜来源：data/gmgn_candidates_live_run/tokens/yrKmZe5x2YBp1P6ufKLUCNifPbqxwHiwsbfDRWBpump/token_status.json｜字段：token_symbol

#### 为什么观察
- 有证据：当前状态：WATCHING｜来源：data/gmgn_candidates_live_run/tokens/yrKmZe5x2YBp1P6ufKLUCNifPbqxwHiwsbfDRWBpump/token_status.json｜字段：current_state
- 有证据：最近流程记录：WATCHING / 候选筛选等级为观察层，等待更多 K线/结构证据｜来源：data/gmgn_candidates_live_run/tokens/yrKmZe5x2YBp1P6ufKLUCNifPbqxwHiwsbfDRWBpump/process_trace.jsonl｜字段：current_state/latest_reason

#### 为什么支持
- 证据缺失/待复查：为什么支持：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/wallet_structure/yrKmZe5x2YBp1P6ufKLUCNifPbqxwHiwsbfDRWBpump/wallet_structure_decision.json；data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么暂停
- 证据缺失/待复查：为什么暂停：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

#### 为什么阻断
- 证据缺失/待复查：为什么阻断：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/yrKmZe5x2YBp1P6ufKLUCNifPbqxwHiwsbfDRWBpump/token_status.json；data/gmgn_candidates_live_run/wallet_structure/yrKmZe5x2YBp1P6ufKLUCNifPbqxwHiwsbfDRWBpump/wallet_structure_decision.json

#### 为什么进入paper
- 证据缺失/待复查：为什么进入paper：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/tokens/yrKmZe5x2YBp1P6ufKLUCNifPbqxwHiwsbfDRWBpump/token_status.json；data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

#### 为什么退出
- 证据缺失/待复查：为什么退出：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json

#### 为什么失败
- 证据缺失/待复查：为什么失败：未在输入中找到可引用字段，待复查；不据此新增结论。｜来源：data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 下一步看什么
- 待复查：复查最新状态/动作：WATCHING / LIVE_RUN_SYNC｜来源：data/gmgn_candidates_live_run/tokens/yrKmZe5x2YBp1P6ufKLUCNifPbqxwHiwsbfDRWBpump/token_status.json｜字段：current_state/latest_action
- 待复查：复查钱包结构是否变化：未接入｜来源：data/gmgn_candidates_live_run/wallet_structure/yrKmZe5x2YBp1P6ufKLUCNifPbqxwHiwsbfDRWBpump/wallet_structure_decision.json｜字段：wallet_structure_status
- 待复查：复查 quote/security：MISSING / MISSING｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 待复查：如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_open.json；data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 主要失效条件
- 条件：wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化｜来源：data/gmgn_candidates_live_run/wallet_structure/yrKmZe5x2YBp1P6ufKLUCNifPbqxwHiwsbfDRWBpump/wallet_structure_decision.json｜字段：wallet_structure_status/wallet_risk_score/counterparty_pressure_score
- 条件：quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json｜字段：quote_security_permission/交易前状态
- 条件：paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败｜来源：data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json；data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl

#### 替代假设
- 待验证：若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。｜来源：data/gmgn_candidates_live_run/wallet_structure/yrKmZe5x2YBp1P6ufKLUCNifPbqxwHiwsbfDRWBpump/wallet_structure_decision.json
- 待验证：若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。｜来源：data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
- 待验证：若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。｜来源：data/gmgn_candidates_live_run/tokens/yrKmZe5x2YBp1P6ufKLUCNifPbqxwHiwsbfDRWBpump/process_trace.jsonl
