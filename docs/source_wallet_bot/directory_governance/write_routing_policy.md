# Source Wallet Bot 写入路由策略

## 目的

Hermes 收到不同任务时，必须先按任务类型路由，再决定写入目录。

## 路由原则

- 方法轮 / 自动思考 / 长任务：`/root/sikk-gmgn/research_loop/source_wallet_bot/`
- 架构文档 / 说明 / ADR / 验收：`/root/sikk-gmgn/docs/source_wallet_bot/`
- 字段合约 / schema / output contract / handoff contract：`/root/sikk-gmgn/contracts/source_wallet_bot/`
- 数据依赖地图 / 字段映射 / 判断目标合同：`/root/sikk-gmgn/docs/source_wallet_bot/directory_governance/`
- 正式代码：`/root/sikk-gmgn/modules/source_wallet_bot/`
- token 运行数据：`/root/sikk-gmgn/data/source_wallet_bot/<mode>/<token_address>/`
- 历史地址库：`/root/sikk-gmgn/data/source_wallet_bot/history/`
- 外部导入包：`/root/sikk-gmgn/data/source_wallet_bot/imports/`
- 测试：`/root/sikk-gmgn/tests/source_wallet_bot/`
- 日志：`/root/sikk-gmgn/logs/source_wallet_bot/`

## 禁止写入

- `/root/sikk`
- `/root/sikk-gmgn/data/gmgn_candidates_live_run`
- `/root/sikk-gmgn/outputs`
- `/root/sikk-gmgn/data/paper_live_*`
- `/root/sikk-gmgn/data/gmgn_candidates_live_run_*`

除非任务明确是兼容读取或归档审计。

## 任务类型到写入根目录

- directory_governance → docs/source_wallet_bot/directory_governance/
- method_loop → research_loop/source_wallet_bot/
- long_running_workflow → research_loop/source_wallet_bot/
- field_contract → contracts/source_wallet_bot/
- schema_design → contracts/source_wallet_bot/ 或 schemas/shared/
- code_module → modules/source_wallet_bot/
- token_live_output → data/source_wallet_bot/<mode>/<token_address>/
- token_structure_analysis → data/source_wallet_bot/<mode>/<token_address>/structure_analysis/
- wallet_fact_output → data/source_wallet_bot/<mode>/<token_address>/wallet_data/
- behavior_inference_output → data/source_wallet_bot/<mode>/<token_address>/structure_analysis/intelligence/
- historical_address_db → data/source_wallet_bot/history/
- import_package → data/source_wallet_bot/imports/
- compatibility_audit → legacy_compat/
- test → tests/source_wallet_bot/
- log → logs/source_wallet_bot/

## 强制要求

若写文件前无法确认任务类型、资产类型、token/run/import/case/task id 和主写路径，必须先写 plan，不得直接写运行文件。
