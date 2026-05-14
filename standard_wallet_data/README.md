# standard_wallet_data

SIKK 钱包分析标准数据骨架：用于把分散的钱包/结构/GMGN 导入数据统一映射到 7 层模型。

## 七层目录

- `00_ingest/`：原始导入、批次、来源清单。
- `01_facts/`：钱包、Token、交易、对手方等可复核事实。
- `02_evidence/`：时间窗口、资金边、Token 转移边、交易边、来源链接。
- `03_inference/`：钱包角色、候选组、风险标记、置信说明。
- `04_handoff/`：GMGN 备注、跟踪名单、复查队列。
- `05_reports/`：Token/钱包/日复盘报告。
- `06_index/`：地址、Token、来源、迁移映射索引。

## 约束

- 当前只创建空目录骨架，不迁移、不删除旧数据。
- 后续迁移应先 scan → classify → map → spec → migration-plan。
- 旧目录数据进入本目录前必须保留来源路径和证据链。
