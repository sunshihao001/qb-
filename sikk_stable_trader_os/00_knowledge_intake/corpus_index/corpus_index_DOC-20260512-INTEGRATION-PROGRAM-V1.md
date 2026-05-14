# Corpus Index — DOC-20260512-INTEGRATION-PROGRAM-V1

## Anchors
- conclusion: 分别开来完善，但作为连续流程执行。
- architecture_boundary: P01-P10 = 业务阶段控制器体系；Integration Program = 系统集成与运行落地流程。
- sequence: I01 → I02 → I03 → I04 → I05。
- current_next_step: I01_full_phase_consistency_audit。
- no_new_business_phase: I01-I05 不是 P11-P15。
- no_runner_before_audit: 一致性没审计就做 Runner 会绑定错误字段。
- no_code_before_index: 目录与合约没统一就写代码会造成路径混乱。

## Required I01 Outputs
- full_phase_consistency_audit_report.md
- phase_io_alignment_matrix.yaml
- handoff_chain_integrity_report.yaml
- status_code_consistency_report.yaml
- forbidden_use_inheritance_report.yaml
- gap_propagation_report.yaml
- phase_boundary_violation_report.yaml
- fix_priority_list.yaml
- i01_to_i02_handoff_packet.yaml

## Key Claims
1. 当前不应新增 P11/P12/P13 业务阶段。
2. 系统集成任务必须拆成连续任务包而非混成一个大任务。
3. I01/I02 是 Runner/Tool Binding 的前置条件。
4. Paper Runtime 与 P08 权限边界不同：P08 只允许进入纸面运行；Paper Runtime 才记录纸面仓位与结果。
5. I05 用真实 paper runtime 输出验证 P09/P10 闭环。
