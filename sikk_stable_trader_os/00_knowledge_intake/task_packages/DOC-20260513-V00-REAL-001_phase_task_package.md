# Phase Task Package — V00 Real Validation Evidence

## Source Material
- material_id: DOC-20260513-V00-REAL-001
- source_path: /root/sikk-gmgn/sikk_stable_trader_os/00_knowledge_intake/raw_inputs/DOC-20260513-V00-REAL-001_v00_real_validation_evidence.md
- title: v00真实证据验证2

## Purpose
建立 V00 real validation executor，将 O00 sample replay 证据推进到真实验证证据层。

## Required Outputs
- V00 validation system files
- tools/v00_*.py
- tests/her_document_function_system/*.py
- validation run output with stdout/stderr/exit_code, replay evidence, bundle, trace/audit, handoff, report

## Constraints
- safe_mode required
- no live/runtime/signing/deploy/trading
- final status READY_WITH_GAPS unless blocking failure

## Acceptance Criteria
- tests written before implementation and RED observed
- executor runs and writes required output files
- final status = V00_REAL_VALIDATION_EVIDENCE_READY_WITH_GAPS
