# Phase Task Pack — DOC-20260513-P01-DATA-FACT-CONTROLLER-002

## Source Material
- material_id: DOC-20260513-P01-DATA-FACT-CONTROLLER-002
- source_path: `/root/sikk-gmgn/sikk_stable_trader_os/00_knowledge_intake/raw_inputs/DOC-20260513-P01-DATA-FACT-CONTROLLER-002_phase_01_data_fact_controller_v1.md`
- canonical_doc_path: `/root/sikk-gmgn/docs/stable_trader_os/phases/phase_01_data_fact_controller.md`
- title: Phase 01 数据事实层控制器 v1.0
- type: user_uploaded_markdown / phase controller spec

## Purpose
把上传资料作为 P01 数据事实层控制器权威阶段说明进入 HER/SIKK，而不是当普通总结处理。

## System Mapping
- Target subsystem: SIKK Stable Trader OS / Data Plane / P01
- Relevant phase: P01_data_fact_controller
- Expected downstream use: P02 只能通过 P01 handoff 读取事实包。

## Required Outputs
- P01 controller doc and field schema split
- raw / normalized / audit / handoff / report output contract
- quality gate and handoff schema
- mock fixture and pytest coverage

## Constraints
- Preserve raw source
- No chat-only inference
- No trading advice / no P02 scene interpretation
- File-backed state required

## Acceptance Criteria
- K00 artifacts exist and parse
- P01 runtime remains blocked until actual controller/tests/replay pass
- P01 implementation must emit explicit missing/degrade statuses

## Handoff
- Next phase: P01_DATA_FACT_CONTROLLER_PACKAGE_OR_CODE_LANDING
- Handoff artifacts: `handoff_packet_DOC-20260513-P01-DATA-FACT-CONTROLLER-002.json`, `task_execution_package_DOC-20260513-P01-DATA-FACT-CONTROLLER-002.json`
- Recovery notes: If implementation bypasses K00 or reads raw GMGN directly in P02, classify as route failure and recover through P01 handoff.
