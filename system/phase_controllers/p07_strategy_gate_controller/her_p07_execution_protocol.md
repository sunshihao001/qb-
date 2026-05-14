# HER P07 Execution Protocol

生成时间：2026-05-12T04:08:53Z

HER 执行 P07 顺序：
1. 读取 professional_build_order.md。
2. 读取 phase_controller_index.yaml。
3. 读取 P07 controller context。
4. 读取 P06→P07 handoff packet 与 p07_strategy_gate_data_request_packet。
5. 读取 Trace / Acceptance / Handoff 输出。
6. 建立 strategy_gate_input_manifest。
7. 读取 strategy_policy_registry。
8. 执行 hard_negative_evaluation。
9. 执行 scenario/evidence/chip/data/conflict/market/pattern/risk gates。
10. 绑定 invalidation conditions。
11. 生成 observe/pause/block/candidate/human confirmation/decision/usage records。
12. 生成 gap report、P08 request、trace、report、P07→P08 handoff。
13. 执行 acceptance。
14. 只允许 handoff 给 P08。

禁止：无 P06 handoff 启动；无策略注册裁决；忽略 hard negative / conflict / counter evidence；把 PAPER_CANDIDATE 当 PAPER_READY；直接启动 paper runtime；输出 buy_signal；绕过 P08；任何 live execution。
