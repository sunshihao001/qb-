# 运行入口层

## 功能定位

Source Wallet Bot 的执行入口、配置、数据模型、IO、错误处理和任务状态文件；负责把多个事实处理步骤串成一次稳定运行。

## 迁移/存放方式

- 方式：copy-only 归档到 skill references，不删除、不移动原项目源文件。
- 目的：让 HER skill 可以按八组单独读取能力文件，降低上下文污染。

## 本组文件

- `runner.py`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/runner.py`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/02_runtime_orchestration_layer/runner.py`
- `config.py`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/config.py`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/02_runtime_orchestration_layer/config.py`
- `models.py`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/models.py`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/02_runtime_orchestration_layer/models.py`
- `io_utils.py`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/io_utils.py`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/02_runtime_orchestration_layer/io_utils.py`
- `errors.py`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/errors.py`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/02_runtime_orchestration_layer/errors.py`
- `__init__.py`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/__init__.py`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/02_runtime_orchestration_layer/__init__.py`
- `kanban_task_board.md`
  - source: `/root/sikk-gmgn/modules/source_wallet_bot/kanban_task_board.md`
  - copy: `/root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/references/source_wallet_bot_groups/02_runtime_orchestration_layer/kanban_task_board.md`
