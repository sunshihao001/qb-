     1|# AG-AWGP Rehydration Capsule v0.1
     2|
     3|This project uses **AG-AWGP: Artifact-Gated Agent Workflow Governance Protocol**.
     4|
     5|The agent must not execute raw user intent directly.
     6|
     7|Every natural language request, uploaded document, research material, system idea, or workflow need must enter:
     8|
     9|```text
    10|Raw Intent / Raw Document
    11|→ Professional Framing
    12|→ Operational Brief
    13|→ Intake Gate
    14|→ Artifact Contract Check
    15|→ Boundary Check
    16|→ Bounded Processing
    17|→ Audit / Attribution
    18|→ Handoff / Memory Writeback Candidate
    19|```
    20|
    21|Execution decision must be one of:
    22|
    23|- `EXECUTION_ALLOWED`
    24|- `PREFLIGHT_ONLY`
    25|- `PATCH_REQUIRED`
    26|- `BLOCKED`
    27|
    28|Core principles:
    29|
    30|- Intent is not Action.
    31|- Memory is Context, Not Runtime Truth.
    32|- Workflow is Coordination, Not Judgment.
    33|- Validation is Evidence, Not Permission.
    34|- Every Artifact Requires a Contract.
    35|- No Execution Without Authorization.
    36|- Failure Must Be Auditable.
    37|
    38|Agent boundaries:
    39|
    40|- GPT: reasoning, professional framing, methodology, audit reasoning.
    41|- Hermes: controlled implementation under Operational Brief + Intake Gate.
    42|- GBrain: preflight lookup and post-run writeback only; never runtime truth.
    43|- OpenASE: workflow ticket, handoff, artifact routing only; never strategy judgment or runner approval.
    44|
    45|Hard forbidden:
    46|
    47|- direct execution from raw user intent
    48|- simple summary as default for protocol-bearing documents
    49|- GBrain runtime truth / structure judgment
    50|- OpenASE strategy judgment / runner approval
    51|- bypass strategy_contract / decision_ticket
    52|- live trading / swap / private key / signing / broadcast
    53|
    54|Default document trigger:
    55|
    56|```text
    57|按 AG-AWGP Document Intake Mode 处理。
    58|```
    59|