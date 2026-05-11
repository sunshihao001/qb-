#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

REQUIRED_DIRS = [
    "00_startup",
    "01_control_plane",
    "02_task_intake",
    "03_task_runtime",
    "03_task_runtime/checkpoints",
    "03_task_runtime/compact_snapshots",
    "04_memory",
    "05_templates",
    "06_verification",
    "07_recovery",
    "07_recovery/recovery_reports",
    "07_recovery/interrupt_reports",
    "07_recovery/blocked_tasks",
    "08_reports",
    "09_scripts",
    "10_audit",
    "11_workflows",
]

REQUIRED_FILES = [
    "01_control_plane/prompt_layer_policy.md",
    "01_control_plane/runtime_state_policy.md",
    "01_control_plane/input_governance_policy.md",
    "01_control_plane/context_budget_policy.md",
    "01_control_plane/bash_risk_policy.md",
    "01_control_plane/recovery_circuit_breaker_policy.md",
    "01_control_plane/interrupt_policy.md",
    "01_control_plane/tool_ledger_policy.md",
    "01_control_plane/execution_narrative_policy.md",
    "03_task_runtime/active_task_state.json",
    "03_task_runtime/active_task_context.md",
    "03_task_runtime/input_governance_queue.jsonl",
    "03_task_runtime/context_budget.json",
    "03_task_runtime/tool_ledger.jsonl",
    "03_task_runtime/recovery_counter.json",
    "03_task_runtime/execution_narrative.md",
    "03_task_runtime/execution_loop_log.jsonl",
    "03_task_runtime/command_log.jsonl",
    "04_memory/memory_verification_log.jsonl",
    "04_memory/stale_memory.jsonl",
    "04_memory/superseded_memory.jsonl",
    "04_memory/verified_memory.jsonl",
    "09_scripts/hermes_input_governance.py",
    "09_scripts/hermes_context_budget_check.py",
    "09_scripts/hermes_bash_classifier.py",
    "09_scripts/hermes_tool_ledger_check.py",
    "09_scripts/hermes_compact_rebuild.py",
    "09_scripts/hermes_narrative_check.py",
    "09_scripts/hermes_memory_revalidate.py",
    "09_scripts/hermes_recovery_circuit_check.py",
    "11_workflows/method_wheel.workflow.md",
    "11_workflows/directory_governance.workflow.md",
    "11_workflows/code_change.workflow.md",
    "11_workflows/recovery.workflow.md",
    "11_workflows/verification.workflow.md",
]


def parser():
    p = argparse.ArgumentParser(description="Verify Hermes Harness V1.2 target architecture")
    p.add_argument("--base", default=str(BASE), help="Hermes harness root")
    p.add_argument("--dry-run", action="store_true")
    return p


def check_json(path, findings):
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        findings.append({"severity": "error", "reason": "invalid_json", "path": str(path), "detail": str(exc)})


def main():
    args = parser().parse_args()
    base = Path(args.base)
    findings = []

    for rel in REQUIRED_DIRS:
        p = base / rel
        if not p.is_dir():
            findings.append({"severity": "error", "reason": "missing_dir", "path": rel})

    for rel in REQUIRED_FILES:
        p = base / rel
        if not p.exists():
            findings.append({"severity": "error", "reason": "missing_file", "path": rel})
        elif rel.endswith(".json"):
            check_json(p, findings)

    workflow_sections = ["适用条件", "输入", "允许工具", "禁止工具", "执行阶段", "输出物", "验证标准", "失败处理"]
    for rel in [r for r in REQUIRED_FILES if r.startswith("11_workflows/")]:
        p = base / rel
        if p.exists():
            text = p.read_text(encoding="utf-8")
            missing = [s for s in workflow_sections if s not in text]
            if missing:
                findings.append({"severity": "error", "reason": "workflow_missing_sections", "path": rel, "missing": missing})

    status = "PASSED" if not findings else "FAILED"
    out = {
        "harness_architecture": "V1.2",
        "base": str(base),
        "status": status,
        "required_dir_count": len(REQUIRED_DIRS),
        "required_file_count": len(REQUIRED_FILES),
        "findings": findings,
        "dry_run": args.dry_run,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    raise SystemExit(0 if status == "PASSED" else 2)


if __name__ == "__main__":
    main()
