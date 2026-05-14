# HER 执行任务书：Phase 01 数据事实层落地

## 任务名称
SIKK Stable Trader OS `phase_01_data_fact` 合约/schema/runtime/审计接入。

## 任务目标
把 Phase 01 从文档基线推进为可执行、可验证、可交接、可阻断、可降级、可审计的系统模块。

## 总系统目标
只生成事实层与数据质量裁决，不输出买卖点、不输出确定庄家、不执行交易；下游只能通过 handoff 读取已审计事实。

## 当前阶段
`phase_01_data_fact_controller`。

## 禁止事项
- 禁止用 `0`、空字符串或推测值伪装 missing。
- 禁止输出 `buy_signal`、`sell_signal`、`trade_allowed`、`execute_now`、确定庄家结论。
- 禁止绕过 `data/shared_handoff/` 进入下游。
- 禁止删除原始事实、snapshot、历史 audit chain。

## 多步骤实现
1. 读取总控基线状态：仅 `BASELINE_ACCEPTED` / `BASELINE_ACCEPTED_WITH_GAPS` 可继续；gap 必须登记。
2. 补齐 phase_01 合约：`required_fields.md`、`handoff_rules.md`，对齐旧 `contracts/stable_trader_os/phase_01_data_fact/` 与 canonical `contracts/phase_01_data_fact/`。
3. 补齐 canonical schema：`schemas/data_fact/*` 与 `schemas/shared_handoff/phase_handoff_packet.schema.json`。
4. 改造 runtime runner：写入 canonical 输出、质量摘要、阶段 handoff、shared handoff。
5. 接入测试：schema/contract/runtime/handoff/禁用交易字段。
6. 运行 pytest 与一次 mock runtime。
7. 写入 audit、validation、missing gap update。

## 输入文件
- `examples/stable_trader_os/phase_01_data_fact/mock_phase_01_input.json`
- `contracts/phase_01_data_fact/input_contract.json`
- `contracts/phase_01_data_fact/output_contract.json`
- `contracts/stable_trader_os/phase_01_data_fact/*.json`

## 输出文件
- `contracts/phase_01_data_fact/required_fields.md`
- `contracts/phase_01_data_fact/handoff_rules.md`
- `schemas/data_fact/*.schema.json`
- `schemas/shared_handoff/phase_handoff_packet.schema.json`
- Runtime outputs under `data/stable_trader_os/runs/<run_id>/01_data_fact/`
- Shared handoff under `data/stable_trader_os/runs/<run_id>/shared_handoff/<token>/phase_01_handoff_packet.json`
- Audit under `reports/system_audit/phase_01_data_fact_landing_audit.md`

## Phase Controller
`phase_01_data_fact_controller`。

## Atomic Skill
`raw_snapshot_writer_skill`、`gmgn_field_mapping_skill`、`token_basic_normalizer_skill`、`wallet_trade_normalizer_skill`、`holder_trader_normalizer_skill`、`kline_normalizer_skill`、`quote_security_normalizer_skill`、`missing_field_checker_skill`、`time_validity_checker_skill`、`data_quality_scorer_skill`、`phase_handoff_writer_skill`。

## 状态码
`DATA_OK`、`DATA_PARTIAL`、`DATA_WEAK`、`DATA_INVALID`、`HANDOFF_READY`、`HANDOFF_DEGRADED`、`HANDOFF_BLOCKED`。

## 反证规则
必须输出 `negative_evidence` 与 `counter_evidence`；mock/source missing/field missing 必须进入反证或降级。

## 硬否决规则
输入 JSON 无效、required config 严重缺失、出现交易执行字段或确定性判断字段时阻断。

## 验收标准
- 目标文件存在。
- Runtime 可生成 canonical 输出和 shared handoff。
- pytest 通过。
- audit 报告记录输出、缺口、阻断/降级、下游交接。

## 下一阶段交接
下游阶段：`phase_02_wallet_structure_controller`。
读取文件：`token_basic_normalized.json`、`token_market_context.json`、`wallet_trade_normalized.csv`、`holder_normalized.csv`、`kline_normalized.csv`、`quote_security_normalized.json`、`data_quality_summary.json`、`phase_01_handoff_packet.json`。
