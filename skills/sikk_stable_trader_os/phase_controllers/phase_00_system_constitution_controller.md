# Phase00 System Constitution Controller

## Role

Phase00 固定系统宪法、全局状态码、硬否决继承、安全边界、目录和合约索引。它不是交易阶段，不读取单个钱包分数，也不输出 token 机会判断。

## Inputs

- `skills/sikk_stable_trader_os/SKILL.md`
- `skills/sikk_stable_trader_os/protocols/*.md`
- `docs/stable_trader_os/04_status_codes/global_status_code_table.md`
- `docs/stable_trader_os/07_contract_index/contract_index.md`
- `docs/stable_trader_os/08_schema_index/schema_index.md`

## Outputs

- 全局状态码可读性检查
- 合约/Schema 索引可读性检查
- hard negative inheritance policy
- paper-only safety boundary

## Forbidden

- 禁止输出买入/卖出/实盘授权。
- 禁止绕过 Phase01-Phase07 直接进入策略门禁。
- 禁止把阶段文件数量当成专业判断质量。

## Handoff

Phase00 只允许交接到 Phase01 数据事实层，或回到总控修复 contracts/schemas/status/audit 缺口。
