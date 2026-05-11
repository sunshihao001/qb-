# HER runtime hook quick command usage

## Canonical launcher

```bash
cd /root/sikk-gmgn/hermes_harness && python3 09_scripts/hermes_runtime_hook_launcher.py --dry-run --origin cli --problem '执行任务，全自动完成：把这个问题进入 HER runtime hook。' --json
```

## Recommended trigger mapping

- `/HER_START <problem>` → `hermes_runtime_hook_launcher.py --origin gateway --problem <problem> --json`
- `/HER_SYSTEM_DESIGN <problem>` → `hermes_runtime_hook_launcher.py --origin gateway --problem <problem> --json`
- `/SIKK_START <problem>` → keep SIKK structural workflow; if task is Hermes/HER runtime/control-plane related, route through this launcher.

## Example quick command config shape

> Do not store secrets in quick command definitions.

```yaml
quick_commands:
  HER_START:
    type: exec
    command: "cd /root/sikk-gmgn/hermes_harness && python3 09_scripts/hermes_runtime_hook_launcher.py --origin quick_command --json --problem"
```

If the gateway requires argument interpolation, append the message text after `--problem` according to the active Hermes Agent quick-command syntax.

## Output contract

Launcher prints one JSON object when `--json` is enabled:

```json
{
  "status": "COMPLETED",
  "route": "hermes_runtime_hook_autonomous_problem_loop",
  "dry_run": true,
  "origin": "quick_command",
  "runtime_run_id": "runtime.YYYYMMDD_HHMMSS.slug",
  "run_dir": "/root/sikk-gmgn/hermes_harness/14_runtime_hooks/runtime_runs/...",
  "overall_passed": true
}
```


## V1.5 upstream CLI/Gateway integration (2026-05-09T01:39:46Z)

- `/HER_START <problem>` is now registered in Hermes Agent upstream command registry via canonical `her-start` with alias `her_start`.
- `/HER_SYSTEM_DESIGN <problem>` is now registered via canonical `her-system-design` with alias `her_system_design`.
- CLI origin call: `python3 /root/sikk-gmgn/hermes_harness/09_scripts/hermes_runtime_hook_launcher.py --origin cli --problem <problem> --json`
- Gateway origin call: `python3 /root/sikk-gmgn/hermes_harness/09_scripts/hermes_runtime_hook_launcher.py --origin gateway --problem <problem> --json`
- Verification report: `08_reports/final_reports/HERMES_HARNESS_V1_5_UPSTREAM_HER_COMMANDS_REPORT.md`

## Trigger boundary: normal chat vs runtime hook

普通聊天消息不等同于完整 HER runtime hook。普通消息可能只经过 Hermes persona / memory / skills / tools，不一定生成 runtime run artifacts。

需要强制进入 HER 底层闭环时，使用：

```text
/HER_START <problem>
/HER_SYSTEM_DESIGN <problem>
```

强制 runtime hook 成功后，应至少生成或返回：

```text
runtime_run_id
run_dir
runtime_state.json
tool_ledger.jsonl
problem_passport.md
runtime_completion_audit.md
overall_passed
```

## Dry-run boundary

`--dry-run` 只能证明链路、状态、审计产物可生成；不能证明真实任务已经完成。

## Current canonical index

当前 HER V2.1 本体入口索引：

```text
/root/sikk-gmgn/hermes_harness/HERMES_RUNTIME_SYSTEM_INDEX.md
```

