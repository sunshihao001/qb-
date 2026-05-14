# P00 Full Control Plane 控制上下文

来源文档：DOC-20260511-024 Full Control Plane：完整控制面专业化设计  
生成时间：2026-05-11T16:50:12Z  
主目录：`/root/sikk-gmgn/sikk_stable_trader_os/00_control/full_control_plane`

## 定位
Full Control Plane 是 SIKK Stable Trader OS 的最高级运行控制面，负责阶段选择、任务树编译、合约路由、验收、状态回写、缺口登记、失败恢复、审计与 handoff。

## 边界
- 不做交易判断。
- 不采集原始数据。
- 不生成买入信号。
- 不执行真实交易。
- 不绕过 Governance / Domain / Data / Evidence / Scenario / Strategy Gate。
- 不把文件创建等同于验收通过。

## HER 执行顺序
1. 读取本文件。
2. 读取 `global_plane_registry.yaml`。
3. 读取 `phase_controller_registry.yaml`。
4. 读取 `phase_dependency_graph.yaml` 与 `contract_router.yaml`。
5. 校验当前目标 Plane 的上游依赖、输入合约、权限矩阵。
6. 编译任务树。
7. 执行目标阶段文件/合约/验证任务。
8. 运行 acceptance gate。
9. 写回 `00_control/current_system_state.json`。
10. 写入 audit / gap / handoff。

## 当前裁决
- Full Control Plane 文件/合约/控制面就绪度：`CONTROL_READY_WITH_GAPS`。
- 系统生产就绪度：`BLOCKED`。
- P01 runtime connection：禁止。
- paper_only：true。
- real_trade_enabled：false。
- auto_order_allowed：false。

## 下一阶段原则
Full Control Plane 完成后，不自动进入业务运行；先进行 Governance / Domain / Data 反向审计，然后才允许推进 `P04_EVIDENCE_PLANE_DESIGN`。
