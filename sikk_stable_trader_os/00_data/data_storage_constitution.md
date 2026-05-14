# Data Storage Constitution

推荐运行数据目录：`/root/sikk-gmgn/data/data_plane/`

- `raw/`：只存原始数据，不允许覆盖，不写推理。
- `normalized/`：存标准化数据，不混入策略结论。
- `entities/`：代币、钱包、池子、群组实体。
- `events/`：买入、卖出、转账、清仓、归集等事件。
- `snapshots/`：发现、钱包判断、市场结构、信号、paper entry/exit、review 快照。
- `quality/`：质量评分、缺失、冲突、新鲜度。
- `lineage/`：字段血缘和 replay manifest。
- `handoff/`：交接给 Evidence Plane 的数据包。
- `reports/`：人类可读报告。

legacy runtime 数据保留，不移动，不作为新写入主路径；后续通过 legacy mapping 只读吸收。
