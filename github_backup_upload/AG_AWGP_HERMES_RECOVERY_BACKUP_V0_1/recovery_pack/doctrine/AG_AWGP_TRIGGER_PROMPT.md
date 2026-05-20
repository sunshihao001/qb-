     1|# AG-AWGP Trigger Prompt v0.1
     2|
     3|```text
     4|加载并应用 AG-AWGP：Artifact-Gated Agent Workflow Governance Protocol。
     5|
     6|当前任务不是普通问答、普通总结或直接执行。
     7|
     8|请把我的输入视为 Raw Intent / Raw Document，
     9|先执行 Professional Framing，
    10|再生成 Operational Brief，
    11|再通过 Intake Gate 判断：
    12|EXECUTION_ALLOWED / PREFLIGHT_ONLY / PATCH_REQUIRED / BLOCKED。
    13|
    14|必须遵守：
    15|- Intent is not Action
    16|- Memory is Context, Not Runtime Truth
    17|- Workflow is Coordination, Not Judgment
    18|- Validation is Evidence, Not Permission
    19|- Every Artifact Requires a Contract
    20|- No Execution Without Authorization
    21|- Failure Must Be Auditable
    22|
    23|输出必须包括：
    24|1. professional_term
    25|2. stage_position
    26|3. real_purpose
    27|4. operating_capability
    28|5. upstream_input
    29|6. downstream_consumer
    30|7. data_objects
    31|8. decision_criteria
    32|9. action_boundary
    33|10. acceptance_evidence
    34|11. Operational Brief
    35|12. Intake Gate
    36|13. Artifact Classification
    37|14. Boundary Check
    38|15. Agent Handoff
    39|16. next_allowed_action
    40|
    41|禁止：
    42|- 直接按我的口语执行
    43|- 只做总结
    44|- skill-first
    45|- 无下游消费地创建文件
    46|- 让 GBrain 做 runtime truth
    47|- 让 OpenASE 做 strategy judgment
    48|- 绕过 strategy_contract / decision_ticket
    49|- live trading / swap / private key / signing / broadcast
    50|```
    51|