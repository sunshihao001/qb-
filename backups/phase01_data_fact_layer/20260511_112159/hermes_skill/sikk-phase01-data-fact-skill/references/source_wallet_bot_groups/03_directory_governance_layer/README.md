# 目录治理层

## 功能定位

路径解析、目录宪法执行、文件归属和 legacy 映射；确保新增事实/报告/契约/运行产物不污染根目录或错误工作区。

## 迁移/存放方式

- 方式：copy-only 归档到 skill references，不删除、不移动原项目源文件。
- 目的：让 HER skill 可以按八组单独读取能力文件，降低上下文污染。

## 本组文件

- `path_resolver.py`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/path_resolver.py`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/03_directory_governance_layer/path_resolver.py`
- `directory_governance.py`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/directory_governance.py`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/03_directory_governance_layer/directory_governance.py`
- `package_file_passport.md`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/package_file_passport.md`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/03_directory_governance_layer/package_file_passport.md`
- `package_file_passport.json`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/package_file_passport.json`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/03_directory_governance_layer/package_file_passport.json`
- `legacy_mapping.md`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/legacy_mapping.md`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/03_directory_governance_layer/legacy_mapping.md`
- `old_system_inventory.json`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/old_system_inventory.json`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/03_directory_governance_layer/old_system_inventory.json`
