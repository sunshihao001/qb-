# Hermes Harness V1.4 usable entrypoint audit

## 审计结论

V1.4 runtime hook 已经在 harness 层完成 router/state/tool-ledger/verification/recovery/writeback/completion-audit 绑定，但“可用层”缺口是：

1. **CLI 可调用入口**：已有 `hermes_runtime_hook_run.py`，但它更像内部 runner；缺少稳定 launcher contract。
2. **Gateway / quick command 可调用入口**：Hermes Agent 支持配置型 quick command / exec command 模式；需要一个固定脚本入口输出 JSON，便于 Gateway/Telegram/CLI 表层调用。
3. **项目脚本索引**：README 只索引 runner，没有给出 `/HER_START` / `/HER_SYSTEM_DESIGN` 类触发如何映射。
4. **端到端验证**：V1.4 已有 dry-run 验证，但没有覆盖 launcher/quick-command 形态。

## 接入策略

本轮不直接 patch Hermes Agent upstream 主循环；先建立稳定可验证的 local launcher：

- launcher: `09_scripts/hermes_runtime_hook_launcher.py`
- wrapped runner: `09_scripts/hermes_runtime_hook_run.py`
- route: `hermes_runtime_hook_autonomous_problem_loop`
- supported surfaces: `cli`, `gateway`, `quick_command`, `script`, `local`
- output contract: compact JSON with `status`, `route`, `runtime_run_id`, `run_dir`, `overall_passed`, `contract`。

## 下一阶段边界

若继续进入 V1.5，才应把 launcher 接入 Hermes Agent upstream CLI/Gateway 主循环；当前 V1.4 usable entrypoint 已满足本地命令、项目脚本、quick command 配置可调用。
