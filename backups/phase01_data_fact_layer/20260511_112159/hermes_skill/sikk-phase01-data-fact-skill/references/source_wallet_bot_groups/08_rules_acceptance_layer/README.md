# 规则矩阵 / 字典 / 验收层

## 功能定位

证据等级、钱包角色、GMGN note/watchlist、分发/回收/鲸鱼候选规则、缺失字段报告、验收脚本与扫描报告；负责规则治理与验收闭环。

## 迁移/存放方式

- 方式：copy-only 归档到 skill references，不删除、不移动原项目源文件。
- 目的：让 HER skill 可以按八组单独读取能力文件，降低上下文污染。

## 本组文件

- `evidence_level_matrix.csv`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/evidence_level_matrix.csv`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/08_rules_acceptance_layer/evidence_level_matrix.csv`
- `wallet_role_rule_matrix.csv`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/wallet_role_rule_matrix.csv`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/08_rules_acceptance_layer/wallet_role_rule_matrix.csv`
- `gmgn_note_watchlist_rules.md`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/gmgn_note_watchlist_rules.md`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/08_rules_acceptance_layer/gmgn_note_watchlist_rules.md`
- `evidence_note_rules.md`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/evidence_note_rules.md`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/08_rules_acceptance_layer/evidence_note_rules.md`
- `distribution_recovery_whale_rules.md`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/distribution_recovery_whale_rules.md`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/08_rules_acceptance_layer/distribution_recovery_whale_rules.md`
- `validate_acceptance.py`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/validate_acceptance.py`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/08_rules_acceptance_layer/validate_acceptance.py`
- `missing_fields_report.md`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/missing_fields_report.md`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/08_rules_acceptance_layer/missing_fields_report.md`
- `codebase_inspection_report.md`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/codebase_inspection_report.md`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/08_rules_acceptance_layer/codebase_inspection_report.md`
- `final_module_package.md`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/final_module_package.md`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/08_rules_acceptance_layer/final_module_package.md`
