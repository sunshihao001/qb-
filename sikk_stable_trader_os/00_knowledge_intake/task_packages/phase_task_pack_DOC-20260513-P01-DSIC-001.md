# Phase Task Pack — DOC-20260513-P01-DSIC-001

## Source Material
- material_id: `DOC-20260513-P01-DSIC-001`
- source_path: `/root/sikk-gmgn/sikk_stable_trader_os/00_knowledge_intake/raw_inputs/DOC-20260513-P01-DSIC-001_p01_data_source_intelligence_controller_upgrade.md`
- title: P01 数据事实层认知升级版
- type: user_uploaded_markdown

## Purpose
把上传的 P01 认知升级资料转成 HER 可执行任务包；本轮只完成 K00 intake/taskization，不声称 P01 runtime ready。

## System Mapping
- target subsystem: `P01_data_source_intelligence_controller`
- relevant phase: `P01_data_fact_controller`
- expected downstream use: P01 package/code landing, controller contracts, schemas, tests, replay fixtures, downstream permission migration。

## Required Outputs
- K00 raw/registry/passport/corpus index/system mapping/gap/task/handoff/state/acceptance/intake report
- 后续 P01 代码/包落地任务输入
- 明确 runtime/paper/live blocked

## Constraints
- Preserve raw source
- No chat-only inference
- File-backed state required
- `real_execution=false`
- P02/P03/P06 may not read raw directly

## Acceptance Criteria
- K00 expected artifact files exist and parse
- JSONL registry contains `DOC-20260513-P01-DSIC-001`
- Passport status is `PASSPORT_READY`
- Handoff status is `K00_HANDOFF_READY`
- Phase state is `K00_ACCEPTED`
- Runtime permissions remain blocked

## Handoff
- next phase: `P01_DATA_SOURCE_INTELLIGENCE_CONTROLLER_PACKAGE_OR_CODE_LANDING`
- handoff artifacts: see `handoff_packets/handoff_packet_DOC-20260513-P01-DSIC-001.json`
- recovery notes: if any P01 implementation precedes K00 artifacts, route-recover using this package.
