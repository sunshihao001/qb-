# Data Plane Acceptance Criteria

## DATA_READY
必须具备数据源注册、字段字典、Domain 字段需求映射、raw 模型、normalized 模型、实体模型、事件模型、快照模型、质量模型、新鲜度模型、缺失处理、冲突处理、血缘模型、目录宪法、handoff 合约，且不存在交易信号或主导侧意图越权逻辑。

## DATA_READY_WITH_GAPS
文件/合约/语义结构齐全，但真实 API 稳定性、字段覆盖率、阈值校准、replay 样本、安全扫描覆盖或质量权重仍需后续验证。允许交接给 Evidence Plane 做证据对象设计，但不允许解除 P01 runtime 阻断。

## DATA_REJECTED
缺少字段字典、raw/normalized 模型、质量评分、新鲜度、缺失处理、冲突处理、血缘、快照或 handoff 合约；或 Data Plane 直接输出买入信号 / 主导侧意图。
