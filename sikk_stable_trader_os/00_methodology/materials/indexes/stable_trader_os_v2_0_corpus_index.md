# Corpus Index — Stable Trader OS v2.0 Design

## Anchors

- 总定位: 控制系统，不是预测器；目标是少犯错与可验证判断链。
- 方法论: 控制论 / OODA / V-Model / STAMP-STPA / 数据血缘 / DDD / 状态机 / 决策情报 / 闭环学习。
- 九大平面: 治理、领域、数据、控制、决策、风险、执行、验证、学习。
- P00-P09: system_boundary, data_fact, market_scene, wallet_structure, chip_control, strategy_gate, risk_control, execution, review, self_upgrade。
- 状态体系: SYSTEM / PHASE / WALLET / CHIP / STRATEGY_GATE / EXECUTION。
- 硬否定: 全局硬否定、交易判断硬否定、执行层硬否定。
- 流程: data_flow, decision_flow, risk_flow, handoff_flow, replay/review/upgrade。
- Atomic Skill: 跨阶段复用、I/O 稳定、可测试、不可直接授权交易。
- HER 协议: 读治理→读状态→读控制→读领域→读数据→读风险→读决策→执行→验证→handoff→学习。

## Downstream Task Mapping

1. `system_methodology_blueprint.md` — 本次优先生成。
2. `system_planes/*.md` — 下一阶段生成九大平面细化文件。
3. `01_domain_model/*.yaml|md` — 第三阶段领域对象与状态字典。
4. `02_control_plane/*.yaml|md` — 第四阶段阶段注册与转换。
5. `03_flow_maps/*.md` — 第六阶段四流图谱。
6. `07_atomic_skills/*.yaml|md` — 第七阶段候选 Skill 规格。
7. `08_execution_plane/*.md` — HER 执行/恢复/验证协议。
