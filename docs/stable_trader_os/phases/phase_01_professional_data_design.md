下面这一版把 **Phase 01 数据事实层** 从“阶段文档”升级成 **HER 可执行的专业系统数据设计**。

重点不是再写概念，而是明确：

```text
缺什么
为什么缺
补到哪个文件
补成什么格式
给哪个阶段使用
HER 怎么执行
怎么验收
怎么防止只写文档、不落地
```

---

# SIKK Stable Trader OS

# Phase 01 数据事实层专业化补充设计

建议保存为：

```text
/root/sikk-gmgn/docs/stable_trader_os/phases/phase_01_professional_data_design.md
```

---

# 1. 总结论

Phase 01 现在不能只是一份说明文档。

它应该升级成一个完整的 **数据事实层系统包**：

```text
Phase 01 数据事实层
= 数据源接收标准
+ 字段字典
+ 字段来源矩阵
+ 标准化规则
+ 缺失字段规则
+ 数据质量门禁
+ 下游交接合约
+ legacy 旧目录兼容规则
+ mock 样例数据
+ 测试与验收标准
```

也就是说，Phase 01 的专业化目标是：

```text
让 HER 不需要猜字段、不需要猜目录、不需要猜判断边界，
只要读取 Phase 01 系统数据，就知道该抓什么、存哪里、怎么标准化、怎么判断质量、能不能交给 Phase 02。
```

---

# 2. 当前 Phase 01 还缺什么

上一版 `phase_01_data_fact_controller.md` 已经定义了阶段目标、输入输出、目录、字段方向和质量门禁。

但要达到专业系统标准，还需要补齐下面 10 类内容。

|编号|缺口|当前问题|应补成什么|
|---|---|---|---|
|01|字段 Schema 不够机器化|文档里有字段，但 HER 写代码时仍需猜类型和规则|`phase_01_field_schema.json`|
|02|数据源能力矩阵缺失|不清楚哪些字段来自 GMGN、链上、quote、security、历史库|`source_capability_matrix.md/json`|
|03|字段来源优先级缺失|同一字段多个来源冲突时不知道听谁的|`field_source_priority.json`|
|04|缺失字段等级不够细|missing 没有分 fatal / warning / optional|`missing_field_policy.json`|
|05|数据质量门禁需结构化|质量分逻辑还停留在说明层|`quality_gate_rules.json`|
|06|legacy 旧目录桥接缺失|新目录与旧 `gmgn_candidates_live_run` 如何共存不清楚|`legacy_bridge_registry.json`|
|07|下游交接合约不够硬|Phase 02 到底读取哪些文件、哪些字段，需固定|`phase_01_to_phase_02_contract.json`|
|08|mock 数据缺失|HER 无法离线测试 Phase 01|`mock_phase_01_input.json`|
|09|测试标准缺失|不能确认 HER 是否真的做对|`test_phase_01_acceptance.md`|
|10|运行状态记录缺失|每次运行成功/失败原因无法沉淀|`phase_01_runtime_trace.jsonl`|

---

# 3. Phase 01 专业系统数据目录

建议在 `/root/sikk-gmgn` 下新增：

```text
/root/sikk-gmgn/
├── docs/
│   └── stable_trader_os/
│       └── phases/
│           ├── phase_01_data_fact_controller.md
│           ├── phase_01_professional_data_design.md
│           └── phase_01_acceptance_standard.md
│
├── schemas/
│   └── stable_trader_os/
│       └── phase_01_data_fact/
│           ├── phase_01_field_schema.json
│           ├── token_fact_schema.json
│           ├── wallet_fact_table_schema.json
│           ├── trade_fact_table_schema.json
│           ├── holder_fact_table_schema.json
│           ├── transfer_fact_table_schema.json
│           ├── kline_fact_table_schema.json
│           ├── quote_fact_schema.json
│           ├── security_fact_schema.json
│           └── phase_01_quality_gate_schema.json
│
├── contracts/
│   └── stable_trader_os/
│       └── phase_01_data_fact/
│           ├── phase_01_input_contract.json
│           ├── phase_01_output_contract.json
│           ├── phase_01_to_phase_02_contract.json
│           └── phase_01_forbidden_judgement_contract.md
│
├── configs/
│   └── stable_trader_os/
│       └── phase_01_data_fact/
│           ├── source_capability_matrix.json
│           ├── field_source_priority.json
│           ├── missing_field_policy.json
│           ├── quality_gate_rules.json
│           ├── anomaly_detection_rules.json
│           ├── unit_normalization_rules.json
│           ├── time_normalization_rules.json
│           └── legacy_bridge_registry.json
│
├── examples/
│   └── stable_trader_os/
│       └── phase_01_data_fact/
│           ├── mock_phase_01_input.json
│           ├── mock_raw_gmgn_traders.json
│           ├── mock_raw_gmgn_holders.json
│           ├── mock_raw_kline.json
│           ├── expected_token_fact.json
│           ├── expected_wallet_fact_table.csv
│           ├── expected_trade_fact_table.csv
│           └── expected_phase_01_quality_gate.json
│
└── tests/
    └── stable_trader_os/
        └── phase_01_data_fact/
            ├── test_phase_01_schema_validation.py
            ├── test_phase_01_missing_field_policy.py
            ├── test_phase_01_quality_gate.py
            ├── test_phase_01_handoff_contract.py
            └── test_phase_01_forbidden_judgement.py
```

---

# 4. Phase 01 应补成 8 个专业模块

## 模块 1：字段 Schema 模块

目标：

```text
把所有字段从“文档描述”变成机器可读字段标准。
```

文件：

```text
/root/sikk-gmgn/schemas/stable_trader_os/phase_01_data_fact/phase_01_field_schema.json
```

标准结构：

```json
{
  "schema_version": "phase_01_field_schema_v1.0",
  "phase_id": "phase_01_data_fact_controller",
  "fields": [
    {
      "field_name": "token_address",
      "field_chinese_name": "代币地址",
      "field_group": "token_fact",
      "data_type": "string",
      "required_level": "fatal_required",
      "unit": "none",
      "timezone": "none",
      "allowed_values": null,
      "default_value": null,
      "missing_value": "missing",
      "source_candidates": ["gmgn", "chain", "manual_config"],
      "preferred_source": "manual_config",
      "downstream_used_by": [
        "phase_02_wallet_structure_controller",
        "phase_03_wallet_chip_structure",
        "phase_05_strategy_gate"
      ],
      "description": "Solana 代币 mint 地址，是本次分析对象的唯一标识。"
    }
  ]
}
```

---

## 模块 2：数据源能力矩阵

目标：

```text
让 HER 明确每个字段从哪里来。
```

文件：

```text
/root/sikk-gmgn/configs/stable_trader_os/phase_01_data_fact/source_capability_matrix.json
```

示例：

```json
{
  "gmgn": {
    "can_provide": [
      "token_symbol",
      "current_market_cap_usd",
      "current_liquidity_usd",
      "holder_count",
      "gmgn_tags",
      "first_buy_time",
      "pnl_multiple",
      "realized_profit_usd",
      "unrealized_profit_usd"
    ],
    "cannot_provide_reliably": [
      "complete_funding_source",
      "complete_backflow_path",
      "wallet_first_seen_time"
    ],
    "risk_note": "GMGN 标签只能作为辅助事实，不允许作为最终结构角色判断。"
  },
  "chain": {
    "can_provide": [
      "tx_hash",
      "transfer_time",
      "source_address",
      "counterparty_address",
      "token_transfer",
      "sol_funding",
      "usdc_funding"
    ],
    "cannot_provide_reliably": [
      "gmgn_tags",
      "human_readable_wallet_role"
    ],
    "risk_note": "链上数据能证明交易事实，不能直接证明地址意图。"
  },
  "quote": {
    "can_provide": [
      "current_price_usd",
      "current_market_cap_usd",
      "liquidity_usd",
      "volume_usd"
    ],
    "risk_note": "quote 数据必须记录快照时间，避免后续回测污染。"
  },
  "security": {
    "can_provide": [
      "honeypot_status",
      "mint_authority_status",
      "freeze_authority_status",
      "lp_locked_status",
      "rug_risk_flags"
    ],
    "risk_note": "security 缺失时不得进入强策略门禁。"
  },
  "history_database": {
    "can_provide": [
      "wallet_role_history",
      "appeared_token_count",
      "historical_winrate",
      "historical_roi",
      "known_noise_wallet",
      "known_cex_wallet",
      "known_router_wallet"
    ],
    "risk_note": "历史库只作为复现证据，不得覆盖当前事实。"
  }
}
```

---

## 模块 3：字段来源优先级

目标：

```text
同一个字段多个来源冲突时，HER 必须知道优先级。
```

文件：

```text
/root/sikk-gmgn/configs/stable_trader_os/phase_01_data_fact/field_source_priority.json
```

示例：

```json
{
  "token_address": ["manual_config", "chain", "gmgn"],
  "token_symbol": ["gmgn", "chain", "manual_config"],
  "token_create_time": ["chain", "gmgn"],
  "current_price_usd": ["quote", "gmgn"],
  "current_market_cap_usd": ["quote", "gmgn"],
  "first_buy_time": ["chain", "gmgn"],
  "first_buy_amount_sol": ["chain", "gmgn"],
  "pnl_multiple": ["gmgn", "calculated"],
  "wallet_first_seen_time": ["history_database", "chain", "gmgn"],
  "gmgn_tags": ["gmgn"],
  "source_address": ["chain"],
  "security_flags": ["security"]
}
```

规则：

```text
1. 地址类字段优先 manual_config / chain。
2. 时间类字段优先 chain。
3. 标签类字段只能来自 GMGN 或内部历史库。
4. quote 类字段必须记录快照时间。
5. 如果来源冲突，必须写入 anomaly_fields_report.csv。
```

---

## 模块 4：缺失字段策略

目标：

```text
不是所有 missing 都一样，要分清楚 fatal、warning、optional。
```

文件：

```text
/root/sikk-gmgn/configs/stable_trader_os/phase_01_data_fact/missing_field_policy.json
```

示例：

```json
{
  "fatal_required": [
    "token_address",
    "chain",
    "run_id",
    "data_snapshot_time"
  ],
  "phase_02_required": [
    "token_create_time",
    "current_market_cap_usd",
    "current_liquidity_usd",
    "kline_fact_table",
    "trade_fact_table"
  ],
  "phase_03_required": [
    "wallet_address",
    "first_buy_time",
    "current_token_balance",
    "transfer_fact_table",
    "source_address"
  ],
  "phase_05_required": [
    "security_fact",
    "quote_fact",
    "liquidity_usd",
    "slippage_estimate"
  ],
  "warning_allowed": [
    "wallet_first_seen_time",
    "historical_winrate",
    "historical_roi",
    "gmgn_tags"
  ],
  "optional": [
    "token_name",
    "social_links",
    "website",
    "twitter"
  ],
  "policy": {
    "fatal_required_missing": "BLOCK",
    "phase_02_required_missing": "PAUSE_OR_PASS_WITH_WARNING",
    "warning_allowed_missing": "PASS_WITH_WARNING",
    "optional_missing": "PASS"
  }
}
```

---

## 模块 5：质量门禁规则

目标：

```text
让 Phase 01 自动输出 PASS / PASS_WITH_WARNING / PAUSE / BLOCK。
```

文件：

```text
/root/sikk-gmgn/configs/stable_trader_os/phase_01_data_fact/quality_gate_rules.json
```

示例：

```json
{
  "quality_score_components": {
    "config_completeness": 15,
    "token_fact_completeness": 15,
    "wallet_fact_completeness": 15,
    "trade_fact_completeness": 20,
    "holder_fact_completeness": 10,
    "transfer_fact_completeness": 10,
    "market_fact_completeness": 10,
    "consistency_validation": 5
  },
  "gate_rules": [
    {
      "condition": "fatal_missing_count > 0",
      "gate_status": "BLOCK",
      "reason": "存在致命字段缺失"
    },
    {
      "condition": "quality_score >= 90",
      "gate_status": "PASS",
      "reason": "数据质量良好"
    },
    {
      "condition": "quality_score >= 75 and quality_score < 90",
      "gate_status": "PASS_WITH_WARNING",
      "reason": "数据可用，但存在警告"
    },
    {
      "condition": "quality_score >= 40 and quality_score < 75",
      "gate_status": "PAUSE",
      "reason": "数据不完整，不建议进入强判断"
    },
    {
      "condition": "quality_score < 40",
      "gate_status": "BLOCK",
      "reason": "数据质量过低"
    }
  ],
  "forbidden_downstream_when_missing": {
    "security_fact": [
      "phase_05_strategy_gate",
      "real_trade_gate"
    ],
    "transfer_fact_table": [
      "same_source_group_strong_judgement",
      "fund_backflow_judgement"
    ],
    "kline_fact_table": [
      "phase_02_scene_recognition"
    ]
  }
}
```

---

## 模块 6：异常检测规则

文件：

```text
/root/sikk-gmgn/configs/stable_trader_os/phase_01_data_fact/anomaly_detection_rules.json
```

示例：

```json
{
  "rules": [
    {
      "rule_id": "ADDR_001",
      "field": "wallet_address",
      "anomaly_type": "invalid_address",
      "condition": "not_valid_solana_address",
      "severity": "high",
      "action": "exclude_from_downstream"
    },
    {
      "rule_id": "TIME_001",
      "field": "first_buy_time",
      "anomaly_type": "future_time",
      "condition": "first_buy_time > data_snapshot_time",
      "severity": "high",
      "action": "write_anomaly_and_pause"
    },
    {
      "rule_id": "TIME_002",
      "field": "first_buy_time",
      "anomaly_type": "time_order_conflict",
      "condition": "first_buy_time < token_create_time",
      "severity": "high",
      "action": "write_anomaly_and_pause"
    },
    {
      "rule_id": "AMOUNT_001",
      "field": "total_buy_amount_usd",
      "anomaly_type": "negative_amount",
      "condition": "value < 0",
      "severity": "high",
      "action": "write_anomaly_and_exclude"
    },
    {
      "rule_id": "DUP_001",
      "field": "wallet_address",
      "anomaly_type": "duplicate_record",
      "condition": "duplicate_wallet_same_token",
      "severity": "medium",
      "action": "deduplicate_and_log"
    }
  ]
}
```

---

## 模块 7：旧目录桥接规则

目标：

```text
保留旧数据，不移动、不删除，但允许 Phase 01 读取旧目录作为 legacy 参考。
```

文件：

```text
/root/sikk-gmgn/configs/stable_trader_os/phase_01_data_fact/legacy_bridge_registry.json
```

示例：

```json
{
  "legacy_root": "/root/sikk-gmgn/data/gmgn_candidates_live_run",
  "policy": "read_only_keep_in_place",
  "do_not_move": true,
  "do_not_delete": true,
  "allowed_reference_paths": {
    "old_candidate_states": "state_machine/candidate_states.json",
    "old_signal_summary": "candidate_signal_outputs/candidate_signal_summary.json",
    "old_wallet_structure_summary": "wallet_structure/candidate_wallet_structure_summary.json",
    "old_quote_security_summary": "quote_security/candidate_quote_security_summary.json",
    "old_paper_live": "paper_live/"
  },
  "new_write_root": "/root/sikk-gmgn/data/stable_trader_os/runs",
  "bridge_outputs": [
    "legacy_source_reference.json",
    "legacy_field_mapping_report.md"
  ],
  "rule": "旧目录只作为历史参考和字段迁移来源，新 Phase 01 输出必须写入 data/stable_trader_os/runs/<run_id>/01_data_fact/"
}
```

---

## 模块 8：下游交接合约

目标：

```text
Phase 02 不再猜 Phase 01 输出，直接按合约读取。
```

文件：

```text
/root/sikk-gmgn/contracts/stable_trader_os/phase_01_data_fact/phase_01_to_phase_02_contract.json
```

示例：

```json
{
  "contract_name": "phase_01_to_phase_02_contract",
  "version": "v1.0",
  "from_phase": "phase_01_data_fact_controller",
  "to_phase": "phase_02_wallet_structure_controller",
  "required_files": [
    "01_data_fact/normalized/token_fact.json",
    "01_data_fact/normalized/kline_fact_table.csv",
    "01_data_fact/normalized/trade_fact_table.csv",
    "01_data_fact/normalized/holder_fact_table.csv",
    "01_data_fact/normalized/quote_fact.json",
    "01_data_fact/audit/phase_01_quality_gate.json"
  ],
  "optional_files": [
    "01_data_fact/normalized/security_fact.json",
    "01_data_fact/normalized/transfer_fact_table.csv",
    "01_data_fact/audit/field_quality_report.json"
  ],
  "minimum_gate_status": [
    "PASS",
    "PASS_WITH_WARNING"
  ],
  "phase_02_must_carry_forward": [
    "quality_score",
    "phase_01_gate_status",
    "missing_fields",
    "restricted_models",
    "data_snapshot_time"
  ],
  "forbidden": [
    "Phase 02 不得忽略 Phase 01 的 missing 字段",
    "Phase 02 不得把缺失 security 的样本判定为强通过",
    "Phase 02 不得使用 Phase 01 未输出的字段进行判断"
  ]
}
```

---

# 5. Phase 01 专业化后的系统数据包

最终 Phase 01 应该形成 5 类系统数据。

## 5.1 规则类数据

```text
configs/stable_trader_os/phase_01_data_fact/
├── source_capability_matrix.json
├── field_source_priority.json
├── missing_field_policy.json
├── quality_gate_rules.json
├── anomaly_detection_rules.json
├── unit_normalization_rules.json
├── time_normalization_rules.json
└── legacy_bridge_registry.json
```

作用：

```text
告诉 HER：
数据从哪里来
哪个来源优先
缺失怎么处理
异常怎么处理
质量怎么判断
旧目录怎么兼容
```

---

## 5.2 Schema 类数据

```text
schemas/stable_trader_os/phase_01_data_fact/
├── phase_01_field_schema.json
├── token_fact_schema.json
├── wallet_fact_table_schema.json
├── trade_fact_table_schema.json
├── holder_fact_table_schema.json
├── transfer_fact_table_schema.json
├── kline_fact_table_schema.json
├── quote_fact_schema.json
├── security_fact_schema.json
└── phase_01_quality_gate_schema.json
```

作用：

```text
告诉 HER：
每个输出文件有哪些字段
字段类型是什么
是否必填
单位是什么
缺失值怎么写
下游谁会用
```

---

## 5.3 Contract 类数据

```text
contracts/stable_trader_os/phase_01_data_fact/
├── phase_01_input_contract.json
├── phase_01_output_contract.json
├── phase_01_to_phase_02_contract.json
└── phase_01_forbidden_judgement_contract.md
```

作用：

```text
告诉 HER：
Phase 01 接收什么
必须输出什么
输出给谁
禁止判断什么
```

---

## 5.4 Example 类数据

```text
examples/stable_trader_os/phase_01_data_fact/
├── mock_phase_01_input.json
├── mock_raw_gmgn_traders.json
├── mock_raw_gmgn_holders.json
├── mock_raw_kline.json
├── expected_token_fact.json
├── expected_wallet_fact_table.csv
├── expected_trade_fact_table.csv
└── expected_phase_01_quality_gate.json
```

作用：

```text
让 HER 可以离线测试，不依赖真实 GMGN 接口。
```

---

## 5.5 Test 类数据

```text
tests/stable_trader_os/phase_01_data_fact/
├── test_phase_01_schema_validation.py
├── test_phase_01_missing_field_policy.py
├── test_phase_01_quality_gate.py
├── test_phase_01_handoff_contract.py
└── test_phase_01_forbidden_judgement.py
```

作用：

```text
防止 HER 只写文档，不验证系统是否真的可运行。
```

---

# 6. HER 底层逻辑执行顺序

按照 HER 的工作方式，不要让它直接“自由发挥写系统”。

应该给它固定执行顺序：

```text
第 1 步：读取 Phase 01 阶段文档
第 2 步：建立专业系统目录
第 3 步：创建 Schema 文件
第 4 步：创建 Config 规则文件
第 5 步：创建 Contract 合约文件
第 6 步：创建 Mock 样例数据
第 7 步：创建测试文件
第 8 步：检查旧目录是否只读引用
第 9 步：生成 Phase 01 专业化报告
第 10 步：输出是否允许进入 Phase 02
```

HER 不能先写代码。

正确顺序是：

```text
系统数据标准
→ 文件合约
→ 样例数据
→ 测试标准
→ 再写控制器代码
```

---

# 7. 给 HER 的完整任务书

下面可以直接复制给 HER。

```text
任务名称：
SIKK Stable Trader OS Phase 01 数据事实层专业化系统数据补全

总目标：
把 Phase 01 数据事实层从普通阶段文档升级为专业系统数据包，使 HER 可以根据固定 Schema、Config、Contract、Example、Test 自动执行数据接收、字段标准化、数据质量审计、缺失字段处理、旧目录兼容和 Phase 02 交接。

工作根目录：
/root/sikk-gmgn

重要边界：
1. 不允许删除旧目录。
2. 不允许移动旧目录。
3. 旧目录 /root/sikk-gmgn/data/gmgn_candidates_live_run/ 只能作为 legacy_runtime_keep_in_place 读取参考。
4. 新系统输出统一写入 /root/sikk-gmgn/data/stable_trader_os/runs/<run_id>/。
5. Phase 01 只做数据事实层，不允许输出吸筹、派发、二段扩张、买点、卖点、庄家判断、主导侧心理判断、策略通过等结论。
6. 所有字段说明必须使用中文。
7. 不允许使用 TSV，优先 CSV、JSON、MD。
8. 所有 missing 必须显式标记，不允许编造字段。

第一部分：创建文档目录

请创建或更新：

/root/sikk-gmgn/docs/stable_trader_os/phases/phase_01_data_fact_controller.md
/root/sikk-gmgn/docs/stable_trader_os/phases/phase_01_professional_data_design.md
/root/sikk-gmgn/docs/stable_trader_os/phases/phase_01_acceptance_standard.md

phase_01_acceptance_standard.md 必须包括：
- 必须生成的目录
- 必须生成的 Schema
- 必须生成的 Config
- 必须生成的 Contract
- 必须生成的 Example
- 必须生成的 Test
- 禁止判断清单
- 验收命令
- 验收失败处理方式

第二部分：创建 Schema 目录和文件

请创建：

/root/sikk-gmgn/schemas/stable_trader_os/phase_01_data_fact/

并创建以下文件：

1. phase_01_field_schema.json
2. token_fact_schema.json
3. wallet_fact_table_schema.json
4. trade_fact_table_schema.json
5. holder_fact_table_schema.json
6. transfer_fact_table_schema.json
7. kline_fact_table_schema.json
8. quote_fact_schema.json
9. security_fact_schema.json
10. phase_01_quality_gate_schema.json

每个 Schema 必须包含：
- field_name
- field_chinese_name
- data_type
- required_level
- unit
- timezone
- missing_value
- source_candidates
- preferred_source
- downstream_used_by
- description

第三部分：创建 Config 规则目录和文件

请创建：

/root/sikk-gmgn/configs/stable_trader_os/phase_01_data_fact/

并创建以下文件：

1. source_capability_matrix.json
2. field_source_priority.json
3. missing_field_policy.json
4. quality_gate_rules.json
5. anomaly_detection_rules.json
6. unit_normalization_rules.json
7. time_normalization_rules.json
8. legacy_bridge_registry.json

要求：
- source_capability_matrix.json 必须区分 GMGN、chain、quote、security、history_database。
- field_source_priority.json 必须定义同字段多来源冲突时的优先级。
- missing_field_policy.json 必须区分 fatal_required、phase_02_required、phase_03_required、phase_05_required、warning_allowed、optional。
- quality_gate_rules.json 必须能输出 PASS、PASS_WITH_WARNING、PAUSE、BLOCK。
- anomaly_detection_rules.json 必须覆盖 invalid_address、future_time、time_order_conflict、negative_amount、duplicate_record、source_conflict。
- legacy_bridge_registry.json 必须声明旧目录只读，不移动、不删除。

第四部分：创建 Contract 合约目录和文件

请创建：

/root/sikk-gmgn/contracts/stable_trader_os/phase_01_data_fact/

并创建以下文件：

1. phase_01_input_contract.json
2. phase_01_output_contract.json
3. phase_01_to_phase_02_contract.json
4. phase_01_forbidden_judgement_contract.md

要求：
- phase_01_input_contract.json 定义 Phase 01 必须接收的 config 和可选数据源。
- phase_01_output_contract.json 定义 raw、normalized、audit、handoff、report 必须输出的文件。
- phase_01_to_phase_02_contract.json 定义 Phase 02 必须读取哪些文件，哪些字段必须携带 warning。
- phase_01_forbidden_judgement_contract.md 明确禁止 Phase 01 输出任何市场解释、机会判断、交易信号、主导侧意图判断。

第五部分：创建 Example 样例数据

请创建：

/root/sikk-gmgn/examples/stable_trader_os/phase_01_data_fact/

并创建：

1. mock_phase_01_input.json
2. mock_raw_gmgn_traders.json
3. mock_raw_gmgn_holders.json
4. mock_raw_kline.json
5. expected_token_fact.json
6. expected_wallet_fact_table.csv
7. expected_trade_fact_table.csv
8. expected_phase_01_quality_gate.json

要求：
- mock 数据必须覆盖正常字段、缺失字段、异常字段。
- expected 输出必须能用于测试。
- 样例钱包地址可以使用模拟地址，但必须标记为 mock。
- 不允许混入真实私钥、真实敏感信息。

第六部分：创建测试目录和测试说明

请创建：

/root/sikk-gmgn/tests/stable_trader_os/phase_01_data_fact/

并创建：

1. test_phase_01_schema_validation.py
2. test_phase_01_missing_field_policy.py
3. test_phase_01_quality_gate.py
4. test_phase_01_handoff_contract.py
5. test_phase_01_forbidden_judgement.py

测试必须覆盖：
- Schema 是否包含中文字段说明
- fatal_required 缺失时是否 BLOCK
- warning_allowed 缺失时是否 PASS_WITH_WARNING
- quality_score 是否正确计算
- handoff 是否包含 Phase 02 必需文件
- Phase 01 输出中是否禁止出现“吸筹”“派发”“可以买”“庄家”“主力控盘”“二段扩张概率高”等越级判断词

第七部分：生成运行状态记录标准

请设计运行状态文件：

/root/sikk-gmgn/data/stable_trader_os/runs/<run_id>/01_data_fact/audit/phase_01_runtime_trace.jsonl

每一行必须包含：
- timestamp
- run_id
- phase_id
- step_name
- status
- input_path
- output_path
- error
- warning
- next_action

第八部分：生成最终报告

请生成：

/root/sikk-gmgn/docs/stable_trader_os/phases/phase_01_professional_data_design_report.md

报告必须包括：
1. 新增文件列表
2. 新增目录列表
3. 每个文件的用途
4. Phase 01 当前专业化完成度
5. 尚未实现的代码部分
6. 尚未接入的数据源
7. 与旧目录的兼容方式
8. 是否允许进入 Phase 02
9. 下一步建议

验收标准：
1. 所有目录存在。
2. 所有 Schema 文件存在。
3. 所有 Config 文件存在。
4. 所有 Contract 文件存在。
5. 所有 Example 文件存在。
6. 所有 Test 文件存在。
7. forbidden judgement contract 存在。
8. legacy_bridge_registry.json 明确旧目录只读。
9. phase_01_to_phase_02_contract.json 明确 Phase 02 输入。
10. phase_01_quality_gate_schema.json 明确 PASS / PASS_WITH_WARNING / PAUSE / BLOCK。
11. 所有字段说明必须中文化。
12. 不得出现“确定庄家”“可以买”“强烈建议买入”等交易判断。
13. 输出最终报告。
```

---

# 8. Phase 01 专业化后，HER 应该能自动判断什么

Phase 01 完成后，HER 应该能自动回答：

```text
1. 当前 token 数据是否齐全？
2. 当前缺哪些关键字段？
3. 缺失字段影响哪个阶段？
4. 当前是否能进入 Phase 02？
5. 当前是否只能低置信度分析？
6. 哪些模型必须禁用？
7. 哪些判断必须降级？
8. 哪些旧数据可以读取？
9. 哪些目录不能写入？
10. 哪些字段必须继续传给下游？
```

---

# 9. 关键认知修正

Phase 01 的专业化不是“多写字段”。

真正要补的是：

```text
数据控制权
字段解释权
来源优先权
缺失处理权
质量门禁权
下游交接权
```

如果没有这些，后面 Phase 02 会出现：

```text
看到一点 K 线就说吸筹
看到 GMGN 标签就说结构钱包
看到新钱包就说主控地址
看到上涨就说二段扩张
看到清仓就说派发完成
```

这就是判断污染。

Phase 01 的作用就是在源头阻断这种污染。

---

# 10. 下一步建议

当前最合理的顺序是：

```text
第一步：让 HER 按上面任务书补齐 Phase 01 系统数据包
第二步：检查 Schema / Config / Contract 是否真的生成
第三步：让 HER 用 mock 数据跑一轮 Phase 01 验收
第四步：确认 phase_01_quality_gate.json 是否能正确输出
第五步：再设计 Phase 02 结构地址体系
```

不要现在直接进入 Phase 02。

否则 Phase 02 会建立在不稳定事实层上。