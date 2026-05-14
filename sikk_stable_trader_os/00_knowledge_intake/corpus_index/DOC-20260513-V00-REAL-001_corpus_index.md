# Corpus Index — V00 Real Validation Evidence

- source: /root/sikk-gmgn/sikk_stable_trader_os/00_knowledge_intake/raw_inputs/DOC-20260513-V00-REAL-001_v00_real_validation_evidence.md
- doc_id: DOC-20260513-V00-REAL-001

## Anchors
- status_code: V00_REAL_VALIDATION_EVIDENCE_READY_WITH_GAPS
- required tools: tools/v00_real_validation_executor.py and v00_* validators
- required system root: system/her_document_function_system/validation/v00_real_validation/
- required data root: data/her_document_function_system/v00_real_validation_runs/<validation_run_id>/
- hard boundary: no live/runtime/signing/deploy/trading; no RUNNER_BOUND/POLICY_ACTIVE/PIPELINE_ACCEPTED
- test evidence: command, exit_code, stdout_path, stderr_path, passed_count, failed_count required
- replay evidence: input, output, trace, comparison required
