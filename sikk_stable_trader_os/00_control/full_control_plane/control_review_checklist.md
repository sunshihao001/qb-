# Control Review Checklist

- [ ] Governance Plane 反向审计：权限矩阵与 hard negative 是否被 Full Control 引用。
- [ ] Domain Plane 反向审计：领域对象/场景/证据语义是否都有下游字段需求。
- [ ] Data Plane 反向审计：字段来源、质量、缺失策略、handoff 是否能进入 Evidence Plane。
- [ ] Legacy 路径审计：旧路径只读映射，不作为新写入主路径。
- [ ] Tool 审计：注册工具是否真实可运行。
- [ ] Handoff 联调：控制面 handoff 是否被目标阶段消费并记录。
- [ ] Safety 审计：paper_only=true、real_trade_enabled=false、auto_order_allowed=false。
