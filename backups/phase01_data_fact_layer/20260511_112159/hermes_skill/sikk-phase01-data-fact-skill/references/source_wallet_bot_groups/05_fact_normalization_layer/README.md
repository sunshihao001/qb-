# 事实标准化层

## 功能定位

交易、钱包画像、wallet_fact 聚合、同源候选、角色候选分类、字段映射和 GMGN 标签字典；负责 raw → normalized facts。

## 迁移/存放方式

- 方式：copy-only 归档到 skill references，不删除、不移动原项目源文件。
- 目的：让 HER skill 可以按八组单独读取能力文件，降低上下文污染。

## 本组文件

- `wallet_trade_normalizer.py`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/wallet_trade_normalizer.py`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/05_fact_normalization_layer/wallet_trade_normalizer.py`
- `wallet_profile_normalizer.py`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/wallet_profile_normalizer.py`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/05_fact_normalization_layer/wallet_profile_normalizer.py`
- `wallet_fact_builder.py`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/wallet_fact_builder.py`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/05_fact_normalization_layer/wallet_fact_builder.py`
- `source_group_engine.py`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/source_group_engine.py`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/05_fact_normalization_layer/source_group_engine.py`
- `role_classifier.py`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/role_classifier.py`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/05_fact_normalization_layer/role_classifier.py`
- `gmgn_to_sikk_field_mapping.csv`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/gmgn_to_sikk_field_mapping.csv`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/05_fact_normalization_layer/gmgn_to_sikk_field_mapping.csv`
- `field_dictionary.csv`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/field_dictionary.csv`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/05_fact_normalization_layer/field_dictionary.csv`
- `gmgn_note_dictionary.csv`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/gmgn_note_dictionary.csv`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/05_fact_normalization_layer/gmgn_note_dictionary.csv`
