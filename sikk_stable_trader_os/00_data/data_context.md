# P03 Data Plane HER Context Pack

Data Plane 不是抓数据脚本层，而是数据事实生产层。HER 执行 P03 前必须读取本文件，确认：字段来源、含义、质量、新鲜度、缺失、冲突、血缘、快照与 Evidence Plane 交接都已文件化。

## 本阶段做什么
- 承接 Domain Plane 字段需求。
- 建立数据源注册、字段字典、raw/normalized/entity/event/snapshot 模型。
- 建立质量、新鲜度、缺失、冲突、血缘规则。
- 输出给 Evidence Plane 的 data_handoff_packet 合约。

## 本阶段不做什么
- 不生成买入信号。
- 不判断主导侧意图。
- 不把缺失字段补脑成确定事实。
- 不覆盖 raw 原始数据。
- 不静默合并多源冲突。

当前验收状态：DATA_READY_WITH_GAPS。P01 runtime 仍保持 BLOCKED_BY_DATA_PLANE，直到后续 Data Audit / runtime 接入验收通过。
