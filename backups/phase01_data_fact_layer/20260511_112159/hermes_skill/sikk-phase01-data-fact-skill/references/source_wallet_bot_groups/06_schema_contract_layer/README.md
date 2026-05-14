# Schema / Contract 层

## 功能定位

schema 校验器、各类 JSON schema、wallet/source/group/manifest 合同和架构文档；负责约束输入输出形状和边界。

## 迁移/存放方式

- 方式：copy-only 归档到 skill references，不删除、不移动原项目源文件。
- 目的：让 HER skill 可以按八组单独读取能力文件，降低上下文污染。

## 本组文件

- `schema_validator.py`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/schema_validator.py`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/06_schema_contract_layer/schema_validator.py`
- `wallet_fact_schema_index.json`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/wallet_fact_schema_index.json`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/06_schema_contract_layer/wallet_fact_schema_index.json`
- `wallet_raw_normalized_schema.json`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/wallet_raw_normalized_schema.json`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/06_schema_contract_layer/wallet_raw_normalized_schema.json`
- `wallet_entity_profile_schema.json`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/wallet_entity_profile_schema.json`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/06_schema_contract_layer/wallet_entity_profile_schema.json`
- `same_source_group_schema.json`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/same_source_group_schema.json`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/06_schema_contract_layer/same_source_group_schema.json`
- `wallet_intelligence_decision_schema.json`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/wallet_intelligence_decision_schema.json`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/06_schema_contract_layer/wallet_intelligence_decision_schema.json`
- `current_token_behavior_schema.json`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/current_token_behavior_schema.json`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/06_schema_contract_layer/current_token_behavior_schema.json`
- `wallet_fact_architecture.md`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/wallet_fact_architecture.md`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/06_schema_contract_layer/wallet_fact_architecture.md`
- `wallet_fact_output_contract.md`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/wallet_fact_output_contract.md`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/06_schema_contract_layer/wallet_fact_output_contract.md`
- `wallet_trade_contract.md`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/wallet_trade_contract.md`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/06_schema_contract_layer/wallet_trade_contract.md`
- `wallet_intelligence_contracts.md`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/wallet_intelligence_contracts.md`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/06_schema_contract_layer/wallet_intelligence_contracts.md`
- `source_group_contract.md`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/source_group_contract.md`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/06_schema_contract_layer/source_group_contract.md`
- `source_and_group_models.md`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/source_and_group_models.md`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/06_schema_contract_layer/source_and_group_models.md`
- `source_manifest_contract.md`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/source_manifest_contract.md`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/06_schema_contract_layer/source_manifest_contract.md`
- `field_mapping_dictionary.md`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/field_mapping_dictionary.md`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/06_schema_contract_layer/field_mapping_dictionary.md`
- `quantitative_structure_field_addendum.md`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/quantitative_structure_field_addendum.md`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/06_schema_contract_layer/quantitative_structure_field_addendum.md`
