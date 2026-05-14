# HER Handoff Execution Protocol

1. 读取 current_system_state.json。
2. 读取 acceptance_result_packet。
3. 读取 trace_handoff_packet。
4. 如果 acceptance 未允许 handoff，阻断。
5. 如果存在阻断缺口，阻断。
6. 继承 limitation_tags / forbidden_actions。
7. 生成 handoff_packet、downstream_read_instruction、gap_propagation_packet、limitation_transfer_packet、field_usage_permission。
8. 回写状态与 audit。
9. 保持 paper_only=true、real_trade_enabled=false。

当前 doc_id: DOC-20260511-027
