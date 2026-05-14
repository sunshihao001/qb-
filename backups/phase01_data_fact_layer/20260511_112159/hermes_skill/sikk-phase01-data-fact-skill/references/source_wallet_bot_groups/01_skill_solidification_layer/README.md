# Skill 固化层

## 功能定位

HER skill 自身的能力入口、数据资产矩阵、运行检查清单；用于把 Phase 01 数据事实层固定成可调用、可审计、可复用的子能力。

## 迁移/存放方式

- 方式：copy-only 归档到 skill references，不删除、不移动原项目源文件。
- 目的：让 HER skill 可以按八组单独读取能力文件，降低上下文污染。

## 本组文件

- `SKILL.md`
  - source: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/SKILL.md`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/01_skill_solidification_layer/SKILL.md`
- `data_asset_matrix.md`
  - source: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/data_asset_matrix.md`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/01_skill_solidification_layer/data_asset_matrix.md`
- `run_checklist.md`
  - source: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/run_checklist.md`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/01_skill_solidification_layer/run_checklist.md`
