# O00 CLI Command Help

Commands: init, validate-config, run-sample, run-document, status, resume, recover, show-report, show-gaps, show-trace.

All runtime-capable commands require `--safe-mode`. The CLI forbids live_runtime, wallet_signing, auto_deploy, production_trading, and execute_real_order.

`run-sample` is DESIGN_LEVEL_REPLAY only and must not claim TESTED, RUNNER_BOUND, POLICY_ACTIVE, or PIPELINE_ACCEPTED.
