# Hermes Harness V1.4 Runtime Hooks

Created: 2026-05-09T01:03:33Z

本目录把 V1.3 APUR Loop 接入 Hermes/HER 任务运行时。

## 子目录
- `runtime_templates/`：runtime state 与 tool ledger 模板。
- `runtime_runs/`：每次复杂任务的 hook 运行产物。

## 主脚本
- `../09_scripts/hermes_runtime_hook_run.py`

## 主 route
- `hermes_runtime_hook_autonomous_problem_loop`

## 完成标准
必须通过独立验证报告：`../06_verification/verification_reports/HERMES_HARNESS_V1_4_RUNTIME_HOOK_VERIFICATION.md`
