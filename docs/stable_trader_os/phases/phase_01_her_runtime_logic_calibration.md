# Phase 01 HER 本体底层逻辑专业化理解与校准

生成时间：2026-05-09

## 1. 核心判断

Phase 01 数据事实层不能被理解为“数据说明文档”或“采集脚本前置层”。

在 HER 本体底层逻辑中，Phase 01 是 Stable Trader OS 的第一个运行时状态边界：

```text
Phase 01 = 事实接收边界 + 字段解释权边界 + 数据质量裁决边界 + 时间有效性边界 + Phase 02 交接边界
```

它的任务不是分析 token，不是解释钱包，不是判断场景，也不是生成交易结论。

它只回答一个问题：

```text
当前 token 的事实数据，是否已经被保全、标准化、标记 missing、完成质量裁决，并可被 Phase 02 结构地址层安全读取？
```

因此 Phase 01 在 HER 中的身份是：

- 不是普通 Skill。
- 不是交易分析器。
- 不是钱包角色分类器。
- 不是场景识别器。
- 是 Phase Controller 驱动的 runtime gate。

## 2. HER 分层校准

### 2.1 Phase

Phase 01 作为 Phase，只定义边界与状态：

```text
输入：原始 token / wallet / holder / trader / transfer / kline / quote / security 数据
处理：保全、映射、标准化、missing、质量、时间、审计
输出：normalized facts + quality gate + handoff + audit
下游：phase_02_wallet_structure_controller
```

### 2.2 Phase Controller

`phase_01_data_fact_controller` 是编排层，负责：

1. 读取 input contract。
2. 检查 required config。
3. 检查 forbidden judgement leakage。
4. 写 raw source manifest。
5. 调度 raw -> normalized。
6. 执行 missing policy。
7. 执行 quality gate。
8. 生成 status / state。
9. 写 Phase 01 -> Phase 02 handoff。
10. 写 audit / trace / validation reports。

Controller 不应该把字段标准化逻辑、数据源适配逻辑、钱包解释逻辑混成一个大函数。

### 2.3 Atomic Skill / Module

Phase 01 内部可复用能力应作为 Atomic Skill 或 runtime module：

- raw_snapshot_writer
- gmgn_field_mapping
- token_basic_normalizer
- wallet_trade_normalizer
- holder_trader_normalizer
- transfer_normalizer
- kline_normalizer
- quote_security_normalizer
- missing_field_checker
- time_validity_checker
- data_quality_scorer
- phase_handoff_writer

这些能力只能输出事实、状态、证据、missing、gaps，不得输出钱包角色、主导侧、场景、买卖点。

## 3. 状态机校准

Phase 01 的运行时状态链应固定为：

```text
P01_INIT
→ P01_INPUT_LOADED
→ P01_RAW_SNAPSHOT_WRITTEN
→ P01_FIELDS_MAPPED
→ P01_NORMALIZED
→ P01_MISSING_CHECKED
→ P01_QUALITY_SCORED
→ P01_HANDOFF_READY
→ P01_AUDITED
→ P01_COMPLETE
```

阻断或暂停状态：

```text
P01_PAUSED
P01_BLOCKED
```

状态含义：

- `P01_COMPLETE`：只表示 Phase 01 完成事实层交接，不表示 token 可交易。
- `P01_PAUSED`：数据需要刷新、补充或人工复查。
- `P01_BLOCKED`：关键事实缺失、数据冲突、无效输入或出现越级判断字段。

## 4. DATA 状态与 runtime gate 映射

用户文档中的全局数据状态应映射到 runtime gate，而不是单独漂浮：

```text
DATA_OK                 -> PASS
DATA_PARTIAL            -> PASS_WITH_WARNING
DATA_WEAK               -> PAUSE 或 PASS_WITH_WARNING，取决于关键字段是否缺失
DATA_STALE              -> PAUSE
DATA_SOURCE_CONFLICT    -> PAUSE 或 BLOCK，取决于冲突字段是否为 critical/fatal
DATA_INVALID            -> BLOCK
TIME_OK                 -> 可进入 P01_QUALITY_SCORED
TIME_REFRESH_REQUIRED   -> PAUSE
HANDOFF_READY           -> P01_HANDOFF_READY
HANDOFF_BLOCKED         -> P01_BLOCKED
```

禁止出现：

```text
DATA_INVALID 但 allow_next_stage=true
HANDOFF_BLOCKED 但 next_stage=phase_02_wallet_structure_controller
P01_COMPLETE 但缺 handoff packet 或 audit report
```

## 5. Phase 01 的硬边界

Phase 01 输出必须保留事实，不得提前解释。

### 允许输出

- token basic fact
- wallet fact table
- trade fact table
- holder fact table
- transfer fact table
- kline fact table
- quote fact
- security fact
- raw source manifest
- missing fields report
- anomaly fields report
- quality gate
- handoff packet
- runtime trace
- audit report

### 禁止输出

- buy_signal
- sell_signal
- trade_allowed
- execute_now
- certain_dealer_judgement
- 疑似庄家结论
- 疑似同源组结论
- 主导侧判断
- 控盘判断
- 吸筹/拉升/派发等场景判断
- A+P1 判断

这些判断分别属于 Phase 02、Phase 03、Phase 04、Phase 05、Phase 06，不属于 Phase 01。

## 6. 字段治理理解

Phase 01 字段不是普通字段列表，而是 HER 对事实解释权的机器契约。

每个字段至少应具备：

```text
field_name
field_chinese_name / 中文解释
source_candidates / 来源
preferred_source / 来源优先级
unit / 单位
required_level / 是否必须
missing_allowed / 是否可缺失
judgement_allowed / 是否可用于判断
```

关键规则：

- 缺失必须写 `missing`。
- 不得用 `0` 替代 missing。
- 不得用空字符串替代 missing。
- 不得 AI 猜字段。
- optional missing 可以降级，不一定阻断。
- fatal/critical missing 必须 PAUSE 或 BLOCK。

## 7. Handoff 校准

Phase 01 的唯一合法下游是：

```text
phase_02_wallet_structure_controller
```

handoff packet 必须携带：

- phase
- token_address
- snapshot_id / run_id
- phase_status / gate_status
- allow_next_stage
- next_stage
- required_files_for_next_stage
- positive_evidence
- negative_evidence
- counter_evidence
- missing_fields
- hard_negative_triggered
- block_reason
- degrade_reason
- audit_file

Phase 02 必须读取 Phase 01 的：

- `phase_01_to_phase_02_handoff_packet.json`
- `token_fact.json`
- `wallet_fact_table.csv`
- `trade_fact_table.csv`
- `holder_fact_table.csv`
- `transfer_fact_table.csv`（如存在）
- `kline_fact_table.csv`
- `quote_fact.json`
- `security_fact.json`（如存在）
- `phase_01_quality_gate.json`
- `missing_fields_report.md`

Phase 02 不得忽略 Phase 01 missing / warning / block。

## 8. 与当前仓库资产的覆盖关系

当前仓库已经覆盖的 Phase 01 HER 资产：

- Controller 文档：`docs/stable_trader_os/phases/phase_01_data_fact_controller.md`
- 系统数据设计：`docs/stable_trader_os/phases/phase_01_professional_data_design.md`
- 目标对齐：`docs/stable_trader_os/phases/phase_01_system_goal_alignment.md`
- Runtime 资产索引：`docs/stable_trader_os/phases/phase_01_runtime_asset_index.md`
- Input/Output/Handoff/Forbidden contracts
- Field schemas / fact schemas / quality gate schema
- Source capability / source priority / missing policy / quality rules / time rules / legacy bridge
- Runtime module：`modules/stable_trader_os/phase_01_data_fact/`
- Tests：`tests/stable_trader_os/phase_01_data_fact/`
- Mock examples：`examples/stable_trader_os/phase_01_data_fact/`
- Smoke run output：`data/stable_trader_os/runs/mock_phase_01_runtime_professional/01_data_fact/`

当前仍应保留为 gaps 或后续增强的部分：

- 真实 GMGN / chain / quote / security adapter 尚未接入。
- runner 对 schema 的逐行严格验证还可增强。
- time_validity_report 可从当前 quality gate 中独立拆成专门 artifact。
- field mapping registry 可继续细化为每个 raw source 的字段级映射表。
- snapshot append-only 策略可进一步强化，避免覆盖历史快照。
- DATA_* 状态码可在 output 中显式并行写出，避免只有 PASS/PASS_WITH_WARNING/PAUSE/BLOCK。

## 9. 专业级验收定义

Phase 01 只有同时满足以下条件，才可视为 HER 专业级完成：

1. 阶段目录存在。
2. input contract 存在。
3. output contract 存在。
4. handoff contract 存在。
5. field schema 存在。
6. missing policy 存在。
7. quality gate rules 存在。
8. forbidden judgement contract 存在。
9. runner/validator/CLI 可执行。
10. mock input 可跑出完整 `01_data_fact/`。
11. quality gate 状态合法。
12. handoff next_stage 固定为 `phase_02_wallet_structure_controller`。
13. output validation report 通过。
14. handoff validation report 通过。
15. audit / trace / gaps 已写入。
16. 测试通过。

不满足则输出：

```text
STAGE_INCOMPLETE
```

并写明缺口。

## 10. 结论

Phase 01 的 HER 本体理解应固定为：

```text
它不是分析层；
它是事实层 runtime gate；
它用 contracts 固定输入输出；
它用 schemas 固定字段解释权；
它用 validator 阻断越级判断；
它用 quality gate 裁决数据可用性；
它用 handoff 把状态交给 Phase 02；
它用 audit/trace 让每一步可回放、可审计、可恢复。
```

下一阶段只能进入：

```text
Phase 02：结构地址层
```

不得把多模型场景识别放回 Phase 02；多模型场景识别属于 Phase 04。
