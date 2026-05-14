# 数据适配层

## 功能定位

GMGN/OKX/read-only runtime 数据源适配、source registry、source reliability、gap scanner；负责把外部数据源接入标准事实层。

## 迁移/存放方式

- 方式：copy-only 归档到 skill references，不删除、不移动原项目源文件。
- 目的：让 HER skill 可以按八组单独读取能力文件，降低上下文污染。

## 本组文件

- `gmgn_live_adapter.py`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/gmgn_live_adapter.py`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/04_data_adapter_layer/gmgn_live_adapter.py`
- `gmgn_okx_readonly_adapter.py`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/gmgn_okx_readonly_adapter.py`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/04_data_adapter_layer/gmgn_okx_readonly_adapter.py`
- `runtime_adapter_registry.py`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/runtime_adapter_registry.py`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/04_data_adapter_layer/runtime_adapter_registry.py`
- `system_gap_runtime_adapters.py`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/system_gap_runtime_adapters.py`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/04_data_adapter_layer/system_gap_runtime_adapters.py`
- `system_gap_scanner.py`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/system_gap_scanner.py`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/04_data_adapter_layer/system_gap_scanner.py`
- `source_registry.md`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/source_registry.md`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/04_data_adapter_layer/source_registry.md`
- `source_registry_schema.json`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/source_registry_schema.json`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/04_data_adapter_layer/source_registry_schema.json`
- `source_reliability_matrix.csv`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/source_reliability_matrix.csv`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/04_data_adapter_layer/source_reliability_matrix.csv`
