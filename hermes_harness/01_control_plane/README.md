     1|# 01_control_plane
     2|
     3|Core policy and governance files.
     4|
     5|## Hermes Harness V1.6

- `judgment_governance_policy_v1_6.md`：Judgment Governance 控制面；将闭环执行升级为判断质量治理，强制 problem triage、evidence sufficiency、abstention gate、complexity brake、meta verification、anti self-deception、memory lifecycle 与 human override。

## Hermes Harness V1.4
     6|
     7|- `runtime_hook_policy_v1_4.md`：Runtime Hook 控制面；将复杂执行请求路由到 `hermes_runtime_hook_autonomous_problem_loop`，强制记录 runtime state、tool ledger、verification hook、recovery hook、learning writeback 与 completion audit。
     8|
     9|## Hermes Harness V1.3
    10|
    11|- `problem_understanding_closed_loop_policy_v1_3.md`：全自动问题理解与闭环解决控制面；用于将复杂问题路由到 `problem_understanding_closed_loop_resolution`，强制经过问题接收、自动理解、证据收集、假设生成、根因定位、方案生成、执行、验证、失败恢复与复盘写回。
    12|
    13|## Wallet-Intel Harness V2.0
    14|
    15|- `wallet_intel_harness_v2_policy.md`：Wallet-Intel 钱包数据语义整合控制面；用于识别钱包数据采集分析、钱包结构分析、旧目录导入、数据护照、字段字典、handoff、导入后验证等任务，并路由到 `wallet_intel_semantic_integration` workflow。
    16|
    17|## APUR 自动问题理解与闭环解决策略
    18|
    19|- `auto_problem_solving_policy.md` — V1.3 APUR control policy. Forces complex problems through problem_passport → understanding_report → evidence_plan → hypothesis_set → root_cause_report → solution_design → verification → failure_attribution/learning_writeback before CLOSED.
    20|