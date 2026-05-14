# Phase 02 Wallet Structure Controller

## 1. 阶段定位

`phase_02_wallet_structure_controller` 是 SIKK Stable Trader OS 的第 2 阶段控制器，负责把 Phase 01 数据事实层输出的标准化钱包/交易/holder/top trader/transfer/token context 事实，转化为可审计的结构地址证据包。

本阶段不是庄家识别器，不输出买卖结论，不允许输出绝对定性。所有角色均使用“疑似结构角色 + 字段证据 + 规则依据 + 证据等级 + 风险等级 + 反证/硬否决”。

## 2. 阶段目标

1. 校验 Phase 01 handoff 与钱包事实输入是否可用。
2. 清洗地址，剔除或隔离 CEX、LP、router、program、可疑 hub 等基础设施地址。
3. 生成钱包基础画像。
4. 生成当前 token 行为画像。
5. 判断 Token 来源、资金路径、同源执行组、分发接收、卖出/回流路径。
6. 查询/承接地址历史复现证据。
7. 对钱包输出 21 类固定结构角色之一。
8. 生成证据等级、风险等级、GMGN 备注。
9. 执行反证与硬否决规则。
10. 写入 Phase02 decision、handoff、audit，并交接给 Phase03 筹码控制层。

## 3. 上游输入

主入口：

- `phase_01_handoff_packet.json`

推荐事实文件：

- `data_quality_summary.json`
- `wallet_trade_normalized.csv`
- `holder_normalized.csv`
- `top_trader_normalized.csv`
- `transfer_normalized.csv`
- `token_market_context.json`

机器合约：

- `/root/sikk-gmgn/contracts/stable_trader_os/phase_02_wallet_structure/phase_02_input_contract.json`

## 4. 输入状态

- `PHASE_02_INPUT_READY`：handoff 合法，钱包主事实存在，无上游硬否决。
- `PHASE_02_INPUT_DEGRADED`：存在可降级 missing 或弱字段，但可继续结构归因。
- `PHASE_02_INPUT_BLOCKED`：上游硬否决、关键钱包事实缺失、或 Phase01 数据无效。

## 5. 必需字段

handoff 必需字段：

- `phase`
- `token_address`
- `snapshot_id`
- `phase_status`
- `allow_next_stage`
- `next_stage`
- `required_files_for_next_stage`
- `missing_fields`
- `hard_negative_triggered`

钱包事实至少需要以下任一入口：

- `wallet_trade_source_json`
- `gmgn_traders`
- `trade_fact_table`
- `wallet_trade_normalized`
- `wallet_fact_table`

## 6. Missing 处理

1. 所有缺失字段必须写入 `missing_fields`。
2. 所有缺失字段必须写入 `audit/missing_fields_report.md`。
3. 不得用 `0`、空字符串或 AI 猜测替代 missing。
4. optional missing 只降级；critical missing 阻断。
5. 钱包主事实缺失且无可替代输入时输出 `WALLET_DATA_WEAK` 或 `WALLET_BLOCK`。

## 7. 调用 Atomic Skill / Runtime Module

本阶段 Controller 通过 runtime module 统一调用结构地址能力：

- `modules.wallet_structure.decision_builder.build_bundle_from_request`

其内部能力对应：

1. `wallet_entity_profiler_skill`
2. `current_token_behavior_skill`
3. `token_source_classifier_skill`
4. `fund_flow_detector_skill`
5. `same_source_group_detector_skill`
6. `backflow_path_detector_skill`
7. `address_history_lookup_skill`
8. `address_role_classifier_skill`
9. `evidence_level_scorer_skill`
10. `gmgn_note_generator_skill`

## 8. 结构判断分层（2.1–2.16）

本阶段必须覆盖以下层次：

1. Phase01 handoff 输入门禁。
2. 钱包地址清洗与基础设施隔离。
3. 钱包基础画像。
4. 当前 token 行为画像。
5. Token 来源分类。
6. 资金来源/资金边。
7. 同源组识别。
8. 分发接收路径。
9. 卖出/利润回流路径。
10. 地址历史复现。
11. 固定角色分类。
12. 证据等级评分。
13. 风险等级评分。
14. GMGN 备注生成。
15. 硬否决与反证。
16. Phase03 handoff 与审计。

## 9. 输出文件

标准输出目录：`<run_output>/02_wallet_structure/`

必需输出：

- `wallet_fact/wallet_cleaning_result.csv`
- `wallet_fact/excluded_address_list.csv`
- `normalized/wallet_entity_profile.csv`
- `normalized/current_token_behavior.csv`
- `normalized/fund_flow_edges.csv`
- `normalized/same_source_groups.csv`
- `normalized/distribution_paths.csv`
- `normalized/backflow_paths.csv`
- `normalized/wallet_classification.csv`
- `normalized/gmgn_note_table.csv`
- `wallet_structure_decision.json`
- `handoff/phase_02_handoff_packet.json`
- `audit/audit_report.md`
- `audit/output_validation_report.json`
- `audit/handoff_validation_report.json`
- `audit/missing_fields_report.md`
- `audit/gaps.md`
- `reports/wallet_structure_report.md`

机器合约：

- `/root/sikk-gmgn/contracts/stable_trader_os/phase_02_wallet_structure/phase_02_output_contract.json`

## 10. 状态码

Phase02 决策状态：

- `WALLET_SUPPORT`
- `WALLET_PAUSE`
- `WALLET_BLOCK`
- `WALLET_UNKNOWN`
- `WALLET_DATA_WEAK`
- `WALLET_SAME_SOURCE_DETECTED`
- `WALLET_DISTRIBUTION_DETECTED`
- `WALLET_BACKFLOW_DETECTED`
- `WALLET_COUNTERPARTY_PRESSURE`

Handoff 状态：

- `HANDOFF_READY`
- `HANDOFF_BLOCKED`

状态码配置：

- `/root/sikk-gmgn/configs/stable_trader_os/phase_02_wallet_structure/phase_02_status_codes.json`
- `/root/sikk-gmgn/configs/stable_trader_os/status_transition_matrix.json`

## 11. 反证规则

必须输出并保留：

- `positive_evidence`
- `negative_evidence`
- `counter_evidence`
- `hard_negative_triggered`
- `hard_negative_reasons`
- `missing_fields`
- `confidence_level`
- `risk_level`
- `evidence_level`
- `allowed_next_stage`
- `blocked_next_stage_reason`

禁止只输出正向证据。

## 12. 硬否决规则

硬否决高于所有正向解释：

1. 同源组核心成员大比例同步卖出。
2. 早期结构钱包集中清仓。
3. 多个 Token 分发接收地址卖出或清仓。
4. 卖后资金集中回流到同一核心节点。
5. 高位接盘鲸鱼成为主要承接方。
6. 钱包结构证据显示结构侧已经撤退。
7. Phase01 数据无效或上游硬否决。
8. 钱包数据缺失且无法降级处理。

机器规则：

- `/root/sikk-gmgn/configs/stable_trader_os/phase_02_wallet_structure/hard_negative_rules.json`

## 13. Handoff 规则

下游：`phase_03_chip_control_controller`

handoff packet 必须包含：

- `phase`
- `token_address`
- `snapshot_id`
- `phase_status`
- `allow_next_stage`
- `next_stage`
- `required_files_for_next_stage`
- `positive_evidence`
- `negative_evidence`
- `counter_evidence`
- `hard_negative_triggered`
- `hard_negative_reasons`
- `block_reason`
- `degrade_reason`
- `missing_fields`
- `audit_file`

机器 schema：

- `/root/sikk-gmgn/schemas/stable_trader_os/phase_02_wallet_structure/phase_02_handoff_packet.schema.json`

交接合约：

- `/root/sikk-gmgn/contracts/stable_trader_os/phase_02_wallet_structure/phase_02_to_phase_03_contract.json`

## 14. 审计标准

每次执行必须写入：

- `audit_report.md`
- `output_validation_report.json`
- `handoff_validation_report.json`
- `missing_fields_report.md`
- `gaps.md`

审计报告必须回答：

1. 本阶段读取了什么文件？
2. 哪些输入缺失？
3. 哪些字段 missing？
4. 哪些 Atomic Skill / Runtime Module 被调用？
5. 哪些输出文件已生成？
6. 是否触发反证？
7. 是否触发硬否决？
8. 是否允许进入下一阶段？
9. 如果不允许，阻断原因是什么？
10. 是否存在未实现模块？

## 15. 禁止事项

- 禁止输出“确定庄家”。
- 禁止把 GMGN 单标签作为地址角色唯一依据。
- 禁止跳过 Phase01 数据事实层。
- 禁止用缺失字段做强判断。
- 禁止直接输出买点、卖点或实盘执行。
- 禁止策略层覆盖 Phase02 硬否决。
- 禁止无 handoff packet 宣称完成。
- 禁止无 audit report 宣称完成。

## 16. 完成定义

满足以下条件才可标记 Phase02 完成：

1. 合约存在。
2. schema 存在。
3. 状态码合法。
4. 主要输出文件存在。
5. handoff packet 存在。
6. audit report 存在。
7. missing 字段已标记。
8. 反证已检查。
9. 硬否决已检查。
10. 下游读取文件明确。
11. pytest 验收通过。

不满足时输出：`STAGE_INCOMPLETE`。
