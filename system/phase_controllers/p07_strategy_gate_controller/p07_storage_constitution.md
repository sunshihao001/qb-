# P07 Storage Constitution

生成时间：2026-05-12T04:08:53Z

系统目录：`/root/sikk-gmgn/system/phase_controllers/p07_strategy_gate_controller/`

运行数据目录：`/root/sikk-gmgn/data/phase_controllers/p07_strategy_gate/`

系统文件只存放控制器身份、上下文、合约、schema、policy、状态机、trace、验收、报告模型和 HER 执行协议。

运行数据目录按对象分区：input_manifest、policy_registry、hard_negative_evaluations、scenario_gate、evidence_gate、chip_gate、data_quality_gate、scenario_conflict_gate、market_position_context、strategy_pattern_fit、risk_flags、invalidation_bindings、observe_conditions、pause_conditions、block_reasons、strategy_candidates、human_confirmation、decisions、usage_permissions、quality、gaps、p08_data_requests、rejected_candidates、blocked_candidates、trace、acceptance、handoff、reports、audit。

禁止将 P07 运行输出写入旧目录或 paper runtime 目录。
