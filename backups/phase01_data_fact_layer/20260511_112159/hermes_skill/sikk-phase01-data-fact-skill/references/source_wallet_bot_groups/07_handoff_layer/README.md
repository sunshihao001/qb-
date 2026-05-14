# Handoff 层

## 功能定位

Phase 01 → Phase 02 / Bot2 / behavior inference 的交接导出、交接契约、交接 schema 与补充协议；确保下游只读标准事实。

## 迁移/存放方式

- 方式：copy-only 归档到 skill references，不删除、不移动原项目源文件。
- 目的：让 HER skill 可以按八组单独读取能力文件，降低上下文污染。

## 本组文件

- `handoff_exporter.py`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/handoff_exporter.py`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/07_handoff_layer/handoff_exporter.py`
- `bot2_handoff_contract.md`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/bot2_handoff_contract.md`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/07_handoff_layer/bot2_handoff_contract.md`
- `bot2_handoff_packet_schema.json`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/bot2_handoff_packet_schema.json`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/07_handoff_layer/bot2_handoff_packet_schema.json`
- `wallet_intel_behavior_handoff_addendum.md`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/wallet_intel_behavior_handoff_addendum.md`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/07_handoff_layer/wallet_intel_behavior_handoff_addendum.md`
