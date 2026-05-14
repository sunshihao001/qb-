# HER Acceptance Execution Protocol

1. 读取 acceptance_context.md
2. 读取 acceptance_object_registry.yaml
3. 读取目标阶段 trace_handoff_packet
4. 读取 Full Control Plane task_tree
5. 读取目标阶段产物文件列表
6. 读取 contract_trace
7. 读取 state_trace
8. 读取 gap_register
9. 执行 artifact check
10. 执行 semantic check
11. 执行 contract check
12. 执行 traceability check
13. 执行 governance permission check
14. 执行 gap check
15. 执行 downstream readiness check
16. 计算 acceptance_score
17. 检查 blocking rules
18. 输出 acceptance_result_packet
19. 输出 acceptance_report
20. 写入 acceptance_trace
21. 给 Handoff Plane 输出 handoff permission

禁止：未读取 trace_handoff_packet 就验收；只看文件存在；忽略缺口/越权；未生成 result packet 就 handoff；未验收 tool/paper runtime 就运行；任何自动实盘路径通过。
