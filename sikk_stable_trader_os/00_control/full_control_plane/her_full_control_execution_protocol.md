# HER Full Control Execution Protocol

1. 先读取 `00_control/full_control_plane/control_context.md`。
2. 再读取 `global_plane_registry.yaml`。
3. 再读取 `phase_controller_registry.yaml`。
4. 根据用户目标选择目标 Plane。
5. 检查目标 Plane 的上游依赖是否完成。
6. 检查输入合约是否存在。
7. 编译阶段任务树。
8. 按任务树创建或更新阶段文件。
9. 运行验收门。
10. 写入状态码。
11. 登记缺口。
12. 生成 handoff packet。
13. 输出下一阶段建议。

禁止：跳过 Full Control、跳过验收、无 handoff 交接、Data Plane 输出策略判断、Strategy Gate 输出执行订单、删除 legacy runtime 数据、真实交易或自动下单。
