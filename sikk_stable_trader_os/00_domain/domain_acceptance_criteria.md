# Domain Plane Acceptance Criteria

## DOMAIN_READY
必须同时满足：领域对象、钱包角色、生命周期、场景、证据等级、反证模型、硬否定规则、市值上下文、推理边界、Data Plane 字段需求、handoff 合约、缺口登记、HER context 全部存在；不存在直接买入信号越权。

## DOMAIN_READY_WITH_GAPS
允许进入 P03 Data Plane，但必须保留缺口：阈值待回填、历史样本不足、字段来源待落实、发现市值不稳定、同源归因误差、刷量识别待验证。

## DOMAIN_REJECTED
若写成普通说明文档、直接输出交易信号、缺少证据/反证/推理边界/下游字段需求/验收门/缺口登记，或无法被 HER 调度读取，则驳回。
