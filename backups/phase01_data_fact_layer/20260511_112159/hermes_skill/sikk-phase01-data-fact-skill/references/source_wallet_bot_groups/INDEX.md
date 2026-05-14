# Source Wallet Bot Eight Functional Groups
本索引把 `/root/sikk-gmgn/modules/source_wallet_bot/` 中可复用的功能文件，按八个 HER 功能组 copy-only 固化到当前 skill 目录。
## 固定原则
- 只复制到 skill references，不删除、不移动原始项目文件。
- skill 目录中的副本用于能力理解、离线参考和上下文隔离；实际运行仍以 `/root/sikk-gmgn/` 项目源文件为准。
- 八组分别单独建目录，避免 schema、contract、runtime、handoff、规则矩阵混在一起。
- Phase 01 仍只做事实采集、标准化、质量门禁与 handoff，不做交易判断或确定性庄家/内幕结论。

## 八组目录

### 01_skill_solidification_layer — Skill 固化层
- 功能：HER skill 自身的能力入口、数据资产矩阵、运行检查清单；用于把 Phase 01 数据事实层固定成可调用、可审计、可复用的子能力。
- 目录：`references/source_wallet_bot_groups/01_skill_solidification_layer/`
- 文件数：3
- 文件：
  - `SKILL.md`
  - `data_asset_matrix.md`
  - `run_checklist.md`

### 02_runtime_orchestration_layer — 运行入口层
- 功能：Source Wallet Bot 的执行入口、配置、数据模型、IO、错误处理和任务状态文件；负责把多个事实处理步骤串成一次稳定运行。
- 目录：`references/source_wallet_bot_groups/02_runtime_orchestration_layer/`
- 文件数：7
- 文件：
  - `runner.py`
  - `config.py`
  - `models.py`
  - `io_utils.py`
  - `errors.py`
  - `__init__.py`
  - `kanban_task_board.md`

### 03_directory_governance_layer — 目录治理层
- 功能：路径解析、目录宪法执行、文件归属和 legacy 映射；确保新增事实/报告/契约/运行产物不污染根目录或错误工作区。
- 目录：`references/source_wallet_bot_groups/03_directory_governance_layer/`
- 文件数：6
- 文件：
  - `path_resolver.py`
  - `directory_governance.py`
  - `package_file_passport.md`
  - `package_file_passport.json`
  - `legacy_mapping.md`
  - `old_system_inventory.json`

### 04_data_adapter_layer — 数据适配层
- 功能：GMGN/OKX/read-only runtime 数据源适配、source registry、source reliability、gap scanner；负责把外部数据源接入标准事实层。
- 目录：`references/source_wallet_bot_groups/04_data_adapter_layer/`
- 文件数：8
- 文件：
  - `gmgn_live_adapter.py`
  - `gmgn_okx_readonly_adapter.py`
  - `runtime_adapter_registry.py`
  - `system_gap_runtime_adapters.py`
  - `system_gap_scanner.py`
  - `source_registry.md`
  - `source_registry_schema.json`
  - `source_reliability_matrix.csv`

### 05_fact_normalization_layer — 事实标准化层
- 功能：交易、钱包画像、wallet_fact 聚合、同源候选、角色候选分类、字段映射和 GMGN 标签字典；负责 raw → normalized facts。
- 目录：`references/source_wallet_bot_groups/05_fact_normalization_layer/`
- 文件数：8
- 文件：
  - `wallet_trade_normalizer.py`
  - `wallet_profile_normalizer.py`
  - `wallet_fact_builder.py`
  - `source_group_engine.py`
  - `role_classifier.py`
  - `gmgn_to_sikk_field_mapping.csv`
  - `field_dictionary.csv`
  - `gmgn_note_dictionary.csv`

### 06_schema_contract_layer — Schema / Contract 层
- 功能：schema 校验器、各类 JSON schema、wallet/source/group/manifest 合同和架构文档；负责约束输入输出形状和边界。
- 目录：`references/source_wallet_bot_groups/06_schema_contract_layer/`
- 文件数：16
- 文件：
  - `schema_validator.py`
  - `wallet_fact_schema_index.json`
  - `wallet_raw_normalized_schema.json`
  - `wallet_entity_profile_schema.json`
  - `same_source_group_schema.json`
  - `wallet_intelligence_decision_schema.json`
  - `current_token_behavior_schema.json`
  - `wallet_fact_architecture.md`
  - `wallet_fact_output_contract.md`
  - `wallet_trade_contract.md`
  - `wallet_intelligence_contracts.md`
  - `source_group_contract.md`
  - `source_and_group_models.md`
  - `source_manifest_contract.md`
  - `field_mapping_dictionary.md`
  - `quantitative_structure_field_addendum.md`

### 07_handoff_layer — Handoff 层
- 功能：Phase 01 → Phase 02 / Bot2 / behavior inference 的交接导出、交接契约、交接 schema 与补充协议；确保下游只读标准事实。
- 目录：`references/source_wallet_bot_groups/07_handoff_layer/`
- 文件数：4
- 文件：
  - `handoff_exporter.py`
  - `bot2_handoff_contract.md`
  - `bot2_handoff_packet_schema.json`
  - `wallet_intel_behavior_handoff_addendum.md`

### 08_rules_acceptance_layer — 规则矩阵 / 字典 / 验收层
- 功能：证据等级、钱包角色、GMGN note/watchlist、分发/回收/鲸鱼候选规则、缺失字段报告、验收脚本与扫描报告；负责规则治理与验收闭环。
- 目录：`references/source_wallet_bot_groups/08_rules_acceptance_layer/`
- 文件数：9
- 文件：
  - `evidence_level_matrix.csv`
  - `wallet_role_rule_matrix.csv`
  - `gmgn_note_watchlist_rules.md`
  - `evidence_note_rules.md`
  - `distribution_recovery_whale_rules.md`
  - `validate_acceptance.py`
  - `missing_fields_report.md`
  - `codebase_inspection_report.md`
  - `final_module_package.md`

## 调用建议
当后续任务只涉及某一组能力时，优先读取对应组 README 和文件，不要一次性加载全部 8 组，避免上下文污染。

## 八组执行链路
```text
Skill 固化层
→ 运行入口层
→ 目录治理层
→ 数据适配层
→ 事实标准化层
→ Schema / Contract 层
→ Handoff 层
→ 规则矩阵 / 字典 / 验收层
```
