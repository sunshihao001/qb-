# HER Document Function System under /root/sikk-gmgn

Canonical system root for HER-DFAFS inside SIKK:

- Controllers: `/root/sikk-gmgn/system/her_document_function_system/controllers/`
- Runtime data: `/root/sikk-gmgn/data/her_document_function_system/`
- Self-audit: `/root/sikk-gmgn/system/her_document_function_system/system_audit/`

Legacy standalone root `/root/her_document_function_system/` is retained only as reference/bootstrap material. New controller assets should be written under `/root/sikk-gmgn/system/her_document_function_system/` to avoid directory fragmentation.

## Controller chain

- G00 Governance Boundary Controller: `/root/sikk-gmgn/system/her_document_function_system/controllers/G00_governance_boundary_controller/`
- K00 Knowledge Intake Controller: `/root/sikk-gmgn/system/her_document_function_system/controllers/K00_knowledge_intake_controller/`
- F00 Function Realization Controller: `/root/sikk-gmgn/system/her_document_function_system/controllers/F00_function_realization_controller/`
- V00 Validation Evidence Controller: `/root/sikk-gmgn/system/her_document_function_system/controllers/V00_validation_evidence_controller/`
- R00 Runner / Tool Binding Controller: `/root/sikk-gmgn/system/her_document_function_system/controllers/R00_runner_tool_binding_controller/`
- A00 Acceptance Evidence Controller: `/root/sikk-gmgn/system/her_document_function_system/controllers/A00_acceptance_evidence_controller/`
- H00 Handoff Downstream Queue Controller: `/root/sikk-gmgn/system/her_document_function_system/controllers/H00_handoff_downstream_queue_controller/`
- U00 Review / Upgrade Controller: `/root/sikk-gmgn/system/her_document_function_system/controllers/U00_review_upgrade_controller/`
- O00 Full Pipeline Orchestrator: `/root/sikk-gmgn/system/her_document_function_system/controllers/O00_full_pipeline_orchestrator/`

## Fixed command entries

- `HER_DOC_PIPELINE` — run the document-to-function automation pipeline in safe governed mode.
- `HER_DOC_SYSTEM_AUDIT` — audit HER-DFAFS itself: stage docs, contracts, system data, gaps, readiness.
- `HER_DOC_SYSTEM_REVIEW` — design/review first, then decide whether execution is allowed.

## Current self-audit conclusion

Latest structural self-audit result:

- Status: `HER_DFAFS_SYSTEM_READY`
- Evidence: `/root/sikk-gmgn/system/her_document_function_system/system_audit/audit_result_auto.json`
- Runner: `/root/sikk-gmgn/tools/her_doc_system_audit.py --write`

Important boundary:

- `HER_DFAFS_SYSTEM_READY` means the system structure and controller assets are complete.
- It does **not** mean a specific document task is ready.
- Every concrete task must still begin with K00 handoff.
- F00 must not directly read chat context as source input.

## Mobile-safe audit command

```bash
cd /root/sikk-gmgn && python3 tools/her_doc_system_audit.py --write
```
