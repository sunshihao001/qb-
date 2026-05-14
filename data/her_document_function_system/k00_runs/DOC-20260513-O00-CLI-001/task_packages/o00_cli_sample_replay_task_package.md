# Phase Task Execution Package: O00 CLI Sample Replay READY_WITH_GAPS

## Source Material
- material_id: MAT-O00-CLI-SAMPLE-REPLAY-001
- source_path: /root/sikk-gmgn/data/her_document_function_system/k00_runs/DOC-20260513-O00-CLI-001/raw_inputs/功能自动化落实系统0_.md
- title: O00_CLI_SAMPLE_REPLAY_READY_WITH_GAPS

## Purpose
实现并验证 O00 CLI design-level sample replay，最终状态必须是 PIPELINE_READY_WITH_GAPS。

## Required Outputs
- registry/config/sample replay assets
- tools/o00_cli.py validate-config + run-sample
- cli_runs/<cli_run_id> outputs
- o00_runs/<pipeline_run_id> outputs
- tests proving false closure blocked

## Constraints
- safe_mode=true
- no live_runtime/wallet_signing/auto_deploy/production_trading
- no false TESTED/RUNNER_BOUND/POLICY_ACTIVE/PIPELINE_ACCEPTED

## Acceptance Criteria
- validate-config outputs CONFIG_VALIDATED
- run-sample outputs PIPELINE_READY_WITH_GAPS and exits 10
- required trace/audit/gap/acceptance/report files exist
- focused pytest passes

## Handoff
- Next phase: O00 CLI implementation and verification
- Then: V01_real_validation_executor
