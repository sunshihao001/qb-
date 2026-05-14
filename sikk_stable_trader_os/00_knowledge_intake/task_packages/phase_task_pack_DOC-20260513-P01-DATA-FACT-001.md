# Phase Task Execution Package｜TASK-P01-DATA-FACT-CONTROLLER-LANDING-20260513

## Source Material
- material_id: `DOC-20260513-P01-DATA-FACT-001`
- source_path: `/root/sikk-gmgn/sikk_stable_trader_os/00_knowledge_intake/raw_inputs/DOC-20260513-P01-DATA-FACT-001_p01_data_fact_controller_professional_phase_pack.md`
- title: P01 数据事实层专业版阶段包
- type: user_uploaded_markdown

## Purpose
将 P01 专业版阶段包转为 HER 可调度、可验收、可交接的 P01 data fact controller 建设任务。此资料不是普通总结材料，而是 P01 系统控制器规范。

## System Mapping
- Target subsystem: SIKK Stable Trader OS / P01 data fact controller
- Relevant phase: K00 -> P01
- Expected downstream use: P01 package/code landing, contracts/schemas/tests/replay/handoff/audit

## Required Outputs
- P01 phase identity and context files
- Source registry and capability matrix
- GMGN/OKX connectivity classified reports
- Raw snapshot persistence and manifest
- Normalized token/market/wallet/quote facts
- Coverage/freshness/provenance/schema/cross-source quality reports
- `data_quality_decision.json`
- `data_fact_handoff_packet.json`
- Replay fixture and audit reports

## Constraints
- Preserve raw source
- No chat-only inference
- File-backed state required
- No synthetic data
- P01 `real_execution` must remain false
- Downstream cannot read raw external payload directly

## Acceptance Criteria
- K00 raw / registry / passport / corpus index / mapping / gap / task package / handoff all exist
- P01 implementation/package landing must pass contracts + tests before runtime readiness
- Missing source fields must have explicit `missing_reason`
- Key fields must have provenance and freshness checks

## Handoff
- Next phase: `P01_data_fact_controller_package_or_code_landing`
- Handoff artifacts: passport, corpus index, system mapping, gap detection, task package
- Recovery notes: if existing repo state conflicts, run audit first and preserve old paths as fallback; do not unblock paper/live.
