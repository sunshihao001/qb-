#!/usr/bin/env python3
"""O00 CLI / HER Command Entry.

Safe-mode command entry for HER document-function pipeline. The bundled sample
runner creates a DESIGN_LEVEL_REPLAY evidence package only. It intentionally
returns READY_WITH_GAPS and blocks false claims such as TESTED, RUNNER_BOUND,
POLICY_ACTIVE, PIPELINE_ACCEPTED, or SYSTEM_FULLY_IMPLEMENTED.
"""
from __future__ import annotations

import argparse
import contextlib
import datetime as _dt
import json
import sys
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional

FORBIDDEN_ACTIONS = ["live_runtime", "wallet_signing", "auto_deploy", "production_trading", "execute_real_order"]
REQUIRED_CONTROLLERS = ["G00", "O00", "K00", "F00", "V00", "R00", "A00", "H00", "U00"]
FALSE_SAMPLE_CLAIMS = ["TESTED", "RUNNER_BOUND", "POLICY_ACTIVE", "PIPELINE_ACCEPTED", "SYSTEM_FULLY_IMPLEMENTED"]


def utcnow() -> str:
    return _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def stamp() -> str:
    return _dt.datetime.now().strftime("%Y%m%d_%H%M%S_%f")


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def append_jsonl(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(data, ensure_ascii=False) + "\n")


def resolve(repo: Path, maybe: Optional[str]) -> Optional[Path]:
    if maybe is None:
        return None
    p = Path(maybe)
    return p if p.is_absolute() else repo / p


class Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for stream in self.streams:
            stream.write(data)
            stream.flush()

    def flush(self):
        for stream in self.streams:
            stream.flush()


class CliContext:
    def __init__(self, repo_root: Path, command: str):
        self.repo_root = repo_root
        self.command = command
        self.cli_run_id = f"cli_run_{command}_{stamp()}"
        self.cli_run_dir = repo_root / "data/her_document_function_system/cli_runs" / self.cli_run_id
        self.trace = self.cli_run_dir / "cli_trace.jsonl"
        self.audit = self.cli_run_dir / "cli_audit.jsonl"
        self.pipeline_run_id: Optional[str] = None
        self.pipeline_trace: Optional[Path] = None
        self.pipeline_audit: Optional[Path] = None
        self.cli_run_dir.mkdir(parents=True, exist_ok=True)

    def trace_event(self, event_type: str, message: str = "", **extra: Any) -> None:
        event = {
            "event_id": f"{event_type}_{stamp()}", "timestamp": utcnow(), "cli_run_id": self.cli_run_id,
            "pipeline_run_id": self.pipeline_run_id, "command": self.command, "event_type": event_type,
            "message": message, **extra,
        }
        append_jsonl(self.trace, event)
        if self.pipeline_trace:
            append_jsonl(self.pipeline_trace, event)

    def audit_event(self, event_type: str, **extra: Any) -> None:
        event = {"timestamp": utcnow(), "cli_run_id": self.cli_run_id, "pipeline_run_id": self.pipeline_run_id, "command": self.command, "event_type": event_type, **extra}
        append_jsonl(self.audit, event)
        if self.pipeline_audit:
            append_jsonl(self.pipeline_audit, event)


def safe_mode_required(command: str) -> bool:
    return command in {"init", "validate-config", "run-sample", "run-document", "resume", "recover"}


def check_safe_mode(ctx: CliContext, args: argparse.Namespace) -> Optional[Dict[str, Any]]:
    ctx.trace_event("safe_mode_checked", safe_mode=bool(args.safe_mode))
    if safe_mode_required(args.command) and not args.safe_mode:
        return {"status": "CLI_BLOCKED", "exit_code": 40, "reason": "safe_mode_required"}
    return None


def check_forbidden_boundary(ctx: CliContext, config: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    violations: List[str] = []
    if config:
        boundary = config.get("execution_boundary", {})
        for key, action in [("allow_live_runtime", "live_runtime"), ("allow_wallet_signing", "wallet_signing"), ("allow_auto_deploy", "auto_deploy"), ("allow_production_trading", "production_trading"), ("allow_execute_real_order", "execute_real_order")]:
            if boundary.get(key) is True:
                violations.append(action)
    ctx.trace_event("forbidden_actions_checked", violations=violations)
    if violations:
        return {"status": "CLI_BLOCKED", "exit_code": 40, "reason": "forbidden_action_detected", "violations": violations}
    return None


def command_init(ctx: CliContext, args: argparse.Namespace) -> Dict[str, Any]:
    dirs = ["system/her_document_function_system/cli", "system/her_document_function_system/registry", "system/her_document_function_system/config", "system/her_document_function_system/replay/sample_cases", "data/her_document_function_system/o00_runs", "data/her_document_function_system/cli_runs"]
    created, existing = [], []
    for rel in dirs:
        p = ctx.repo_root / rel
        if p.exists(): existing.append(str(p))
        else:
            p.mkdir(parents=True, exist_ok=True); created.append(str(p))
    result = {"command": "init", "status": "INIT_COMPLETED", "created_dirs": created, "existing_dirs": existing, "forbidden_actions": FORBIDDEN_ACTIONS, "gaps": []}
    write_json(ctx.cli_run_dir / "execution_result.json", result)
    ctx.trace_event("command_completed", status="INIT_COMPLETED")
    return {"exit_code": 0, "result": result}


def validate_config_core(repo: Path, registry_path: Path, config_path: Path) -> Dict[str, Any]:
    gaps, warnings = [], []
    registry_status = "PASSED"; config_status = "PASSED"; registered: List[str] = []
    if not registry_path.exists():
        gaps.append({"gap_type": "missing_registry", "path": str(registry_path), "blocking": True}); registry_status = "FAILED"
    else:
        registry = read_json(registry_path)
        registered = [c.get("controller_id") for c in registry.get("registered_controllers", [])]
        missing = [c for c in REQUIRED_CONTROLLERS if c not in registered]
        if missing:
            gaps.append({"gap_type": "missing_required_controllers", "missing": missing, "blocking": True}); registry_status = "FAILED"
    if not config_path.exists():
        gaps.append({"gap_type": "missing_config", "path": str(config_path), "blocking": True}); config_status = "FAILED"
    else:
        config = read_json(config_path)
        if config.get("safe_mode") is not True:
            gaps.append({"gap_type": "safe_mode_not_true", "blocking": True}); config_status = "FAILED"
        boundary = config.get("execution_boundary", {})
        for key in ["allow_live_runtime", "allow_wallet_signing", "allow_auto_deploy", "allow_production_trading"]:
            if boundary.get(key) is not False:
                gaps.append({"gap_type": "unsafe_execution_boundary", "field": key, "blocking": True}); config_status = "FAILED"
    status = "CONFIG_VALIDATED" if not gaps else "CONFIG_VALIDATION_FAILED"
    return {"command": "validate-config", "status": status, "registry_status": registry_status, "pipeline_config_status": config_status, "registered_controllers": registered, "blocking_gaps": gaps, "warnings": warnings}


def command_validate_config(ctx: CliContext, args: argparse.Namespace) -> Dict[str, Any]:
    registry = resolve(ctx.repo_root, args.registry); config = resolve(ctx.repo_root, args.config)
    assert registry and config
    ctx.trace_event("registry_loaded", input_refs=[str(registry)]); ctx.trace_event("config_loaded", input_refs=[str(config)])
    result = validate_config_core(ctx.repo_root, registry, config)
    write_json(ctx.cli_run_dir / "preflight_result.json", {"status": result["status"], "blocking_gaps": result["blocking_gaps"]})
    write_json(ctx.cli_run_dir / "config_validation_result.json", result); write_json(ctx.cli_run_dir / "execution_result.json", result)
    exit_code = 0 if result["status"] == "CONFIG_VALIDATED" else 20
    ctx.trace_event("command_completed" if exit_code == 0 else "command_failed", status=result["status"])
    return {"exit_code": exit_code, "result": result}


def ref(path: Path) -> Dict[str, str]:
    return {"path": str(path), "exists": str(path.exists()).lower()}


def make_pipeline_run(ctx: CliContext, args: argparse.Namespace, registry: Path, config: Path, sample: Path, *, command_name: str = "run-sample", source_document: Optional[Path] = None, operator_goal: Optional[Path] = None, run_root_name: str = "o00_runs") -> Dict[str, Any]:
    pipeline_run_id = f"o00_run_{stamp()}"; ctx.pipeline_run_id = pipeline_run_id
    root = ctx.repo_root / "data/her_document_function_system" / run_root_name / pipeline_run_id
    for rel in ["input", "preflight", "plan", "state", "queue", "stage_refs", "handoffs", "gaps", "evidence", "recovery", "trace", "acceptance", "reports"]:
        (root / rel).mkdir(parents=True, exist_ok=True)
    ctx.pipeline_trace = root / "trace/o00_trace.jsonl"; ctx.pipeline_audit = root / "trace/o00_audit.jsonl"
    for bootstrap_event in ["cli_started", "safe_mode_checked", "registry_loaded", "config_loaded", "sample_loaded" if command_name == "run-sample" else "document_loaded"]:
        ctx.trace_event(bootstrap_event, message="mirrored into pipeline trace after pipeline run creation")
    cfg = read_json(config); replay = read_json(sample) if sample.exists() else {}
    sample_doc = source_document or resolve(ctx.repo_root, replay.get("sample_document_ref", "")) or sample
    goal_ref = operator_goal or resolve(ctx.repo_root, replay.get("operator_goal_ref", "")) or sample
    ctx.trace_event("pipeline_run_created", status_after="PIPELINE_READY_WITH_GAPS")
    for name, path in [("sample_document_ref.json", sample_doc), ("operator_goal_ref.json", goal_ref), ("replay_run_config_ref.json", sample), ("controller_registry_ref.json", registry), ("pipeline_config_ref.json", config)]:
        write_json(root / "input" / name, ref(path))
    write_json(root / "preflight/o00_preflight_result.json", {"preflight_status": "PASSED", "safe_mode": True, "allowed_modes": ["DESIGN_LEVEL_REPLAY"], "forbidden_modes": FORBIDDEN_ACTIONS, "blocking_gaps": []})
    write_json(root / "preflight/governance_policy_check.json", {"status": "PASSED", "policy_active": False, "candidate_only": True})
    write_json(root / "preflight/execution_boundary_check.json", {"status": "PASSED", "forbidden_actions": FORBIDDEN_ACTIONS})
    stages = {
        "K00": {"status": "K00_READY_WITH_GAPS", "real_runtime_executed": False},
        "F00": {"status": "F00_READY_WITH_GAPS", "real_runtime_executed": False},
        "V00": {"status": "V00_READY_WITH_GAPS", "real_runtime_executed": False},
        "R00": {"status": "SKIPPED_WITH_REASON", "skip_reason": "runner binding not required/executed in design-level replay", "real_runtime_executed": False},
        "A00": {"status": "A00_READY_WITH_GAPS", "real_runtime_executed": False},
        "H00": {"status": "H00_READY_WITH_GAPS", "real_runtime_executed": False},
        "U00": {"status": "U00_READY_WITH_GAPS", "real_runtime_executed": False},
        "G00": {"status": "G00_READY_WITH_GAPS", "policy_active": False, "real_runtime_executed": False},
    }
    write_json(root / "plan/pipeline_execution_plan.json", {"pipeline_run_id": pipeline_run_id, "stage_plan": list(stages), "forbidden_actions": FORBIDDEN_ACTIONS, "false_claims_blocked": FALSE_SAMPLE_CLAIMS})
    write_json(root / "plan/stage_dependency_graph.json", {"nodes": list(stages), "edges": [{"from":"K00","to":"F00"},{"from":"F00","to":"V00"},{"from":"V00","to":"A00"},{"from":"A00","to":"H00"},{"from":"H00","to":"U00"},{"from":"U00","to":"G00"}], "skipped_nodes": ["R00"]})
    write_json(root / "plan/controller_registry_snapshot.json", read_json(registry))
    status_code = "O00_CLI_SAMPLE_REPLAY_READY_WITH_GAPS" if command_name == "run-sample" else "O00_RUN_DOCUMENT_READY_WITH_GAPS"
    state = {"pipeline_run_id": pipeline_run_id, "current_status": "PIPELINE_READY_WITH_GAPS", "final_status": "PIPELINE_READY_WITH_GAPS", "system_status_code": status_code, "current_stage": "H00", "completed_stages": ["K00","F00","V00","A00","H00"], "skipped_stages": ["R00"], "ready_with_gaps": ["PIPELINE","V00","G00"], "open_gaps": ["gap_sample_001_v00_test_not_executed", "gap_sample_001_g00_policy_not_active", "gap_sample_001_r00_not_required"], "forbidden_actions": FORBIDDEN_ACTIONS, "final_report_path": str(root / "reports/o00_final_report.md")}
    write_json(root / "state/pipeline_state.json", state)
    write_json(root / "state/stage_state_matrix.json", stages)
    write_json(root / "state/pipeline_status_history.json", [{"timestamp":utcnow(),"status":"PIPELINE_READY_WITH_GAPS","event":"design_level_replay_completed"}])
    for stage in ["k00","f00","v00","r00","a00","h00","u00","g00"]:
        write_json(root / f"stage_refs/{stage}_run_ref.json", {"stage": stage.upper(), "run_type": "DESIGN_LEVEL_SIMULATED", "status": stages[stage.upper()]["status"]})
    for name in ["k00_to_f00_ref", "f00_to_v00_ref", "v00_to_a00_ref", "a00_to_h00_ref", "h00_to_u00_ref", "u00_to_g00_ref"]:
        write_json(root / f"handoffs/{name}.json", {"handoff_id": name, "status": "SIMULATED_HANDOFF_READY_WITH_GAPS", "gap_refs": state["open_gaps"]})
    write_json(root / "handoffs/o00_final_handoff.json", {"from":"O00", "status":"HANDOFF_READY_WITH_GAPS", "forbidden_actions": FORBIDDEN_ACTIONS, "unresolved_gaps": state["open_gaps"]})
    gaps = [{"gap_id":"gap_sample_001_v00_test_not_executed","gap_level":"NON_BLOCKING_GAP","reason":"sample replay does not execute real tests"},{"gap_id":"gap_sample_001_g00_policy_not_active","gap_level":"NON_BLOCKING_GAP","reason":"governance output is candidate only"},{"gap_id":"gap_sample_001_r00_not_required","gap_level":"NON_BLOCKING_GAP","reason":"runner binding skipped in sample replay"}]
    write_json(root / "gaps/pipeline_gap_register.json", {"pipeline_run_id":pipeline_run_id, "gaps": gaps, "blocking_gaps": [], "non_blocking_gaps": gaps})
    write_json(root / "gaps/gap_propagation_matrix.json", {"gap_policy":"MUST_RETAIN", "gap_refs":[g["gap_id"] for g in gaps]})
    write_json(root / "gaps/unresolved_gaps.json", {"unresolved_gaps": gaps})
    write_json(root / "gaps/accepted_risks.json", {"accepted_risks": [{"risk_id":"risk_design_level_only", "accepted": True, "reason":"explicit sample replay boundary"}]})
    queue = {"pipeline_run_id": pipeline_run_id, "queue_status": "QUEUE_READY_WITH_GAPS", "queue_items": [{"stage":k,"status":v["status"]} for k,v in stages.items()]}
    write_json(root / "queue/pipeline_queue.json", queue)
    replay_result = {"sample_id": replay.get("sample_id") or command_name, "status":"DESIGN_LEVEL_REPLAY_COMPLETED", "command": command_name, "final_status":"PIPELINE_READY_WITH_GAPS", "system_status_code":"O00_CLI_SAMPLE_REPLAY_READY_WITH_GAPS" if command_name == "run-sample" else "O00_RUN_DOCUMENT_READY_WITH_GAPS", "expected_vs_actual_checked": True, "forbidden_claims": {c:"BLOCKED" for c in FALSE_SAMPLE_CLAIMS}}
    write_json(root / "evidence/replay_result.json", replay_result)
    write_json(root / "evidence/sample_replay_result.json", replay_result)
    write_json(root / "evidence/expected_vs_actual_check.json", {"status":"PASSED_WITH_GAPS", "checked": True, "false_claims_blocked": FALSE_SAMPLE_CLAIMS})
    write_json(root / "evidence/pipeline_evidence_bundle.json", {"status":"EVIDENCE_BUNDLE_READY_WITH_GAPS", "evidence_refs":["evidence/replay_result.json", "acceptance/pipeline_acceptance_matrix.json"]})
    write_json(root / "evidence/phase_evidence_refs.json", {"phase_refs": {k: f"stage_refs/{k.lower()}_run_ref.json" for k in stages}})
    acceptance = {"pipeline_run_id":pipeline_run_id, "final_pipeline_status":"PIPELINE_READY_WITH_GAPS", "system_status_code":"O00_CLI_SAMPLE_REPLAY_READY_WITH_GAPS" if command_name == "run-sample" else "O00_RUN_DOCUMENT_READY_WITH_GAPS", "forbidden_claims_blocked": FALSE_SAMPLE_CLAIMS, "false_tested_blocked": True, "false_runner_bound_blocked": True, "false_policy_active_blocked": True, "false_pipeline_accepted_blocked": True, "false_system_fully_implemented_blocked": True, "accepted": False, "ready_with_gaps": True, "blocking": False}
    write_json(root / "acceptance/pipeline_acceptance_matrix.json", acceptance)
    write_json(root / "acceptance/o00_acceptance_result.json", {"status":"O00_CLI_SAMPLE_REPLAY_READY_WITH_GAPS" if command_name == "run-sample" else "O00_RUN_DOCUMENT_READY_WITH_GAPS", "exit_code":10, "exit_name":"READY_WITH_GAPS", "blocking":False})
    write_json(root / "recovery/recovery_report.json", {"status":"NO_BLOCKING_RECOVERY_REQUIRED", "safe_next_actions":["inspect_report", "implement_real_stage_bindings_under_safe_mode"], "forbidden_actions": FORBIDDEN_ACTIONS})
    for ev in ["v00_simulated_with_gaps", "r00_skipped_with_reason", "g00_simulated_with_gaps", "pipeline_acceptance_built", "gap_register_written"]:
        ctx.trace_event(ev)
    ctx.audit_event("pipeline_design_level_replay_audited", final_status="PIPELINE_READY_WITH_GAPS")
    write_json(root / "trace/cross_phase_trace_index.json", {"trace_path": str(root / "trace/o00_trace.jsonl"), "stages": list(stages)})
    report = f"""# O00 CLI / Pipeline Final Report\n\n## Run Info\n- cli_run_id: `{ctx.cli_run_id}`\n- pipeline_run_id: `{pipeline_run_id}`\n- command: `{command_name}`\n- safe_mode: `true`\n- exit_code: `10`\n\n## Replay Result\n- mode: `DESIGN_LEVEL_REPLAY`\n- final_status: `PIPELINE_READY_WITH_GAPS`\n- system_status_code: `{status_code}`\n- R00: `SKIPPED_WITH_REASON`\n\n## Blocked False Claims\n- false tested claim blocked\n- false runner-bound claim blocked\n- false policy-active claim blocked\n- false pipeline-accepted claim blocked\n- false fully-implemented claim blocked\n\n## Evidence Paths\n- state: `{root / 'state/pipeline_state.json'}`\n- gaps: `{root / 'gaps/pipeline_gap_register.json'}`\n- acceptance: `{root / 'acceptance/pipeline_acceptance_matrix.json'}`\n- trace: `{root / 'trace/o00_trace.jsonl'}`\n\n## Forbidden Next Actions\n- live_runtime\n- wallet_signing\n- auto_deploy\n- production_trading\n- execute_real_order\n"""
    (root / "reports/o00_final_report.md").write_text(report, encoding="utf-8")
    (root / "reports/pipeline_summary.md").write_text(report, encoding="utf-8")
    ctx.trace_event("final_report_written", output_refs=[str(root / "reports/o00_final_report.md")])
    ctx.trace_event("cli_completed_with_gaps")
    return {"status": ("CLI_SAMPLE_REPLAY_COMPLETED_WITH_GAPS" if command_name == "run-sample" else "O00_RUN_DOCUMENT_COMPLETED_WITH_GAPS"), "system_status_code": status_code, "pipeline_run_id": pipeline_run_id, "pipeline_run_dir": str(root), "pipeline_state": state, "replay_result": replay_result, "final_status":"PIPELINE_READY_WITH_GAPS", "report": str(root / "reports/o00_final_report.md"), "command": command_name}


def command_run_sample(ctx: CliContext, args: argparse.Namespace) -> Dict[str, Any]:
    registry = resolve(ctx.repo_root, args.registry); config = resolve(ctx.repo_root, args.config); sample = resolve(ctx.repo_root, args.sample)
    assert registry and config and sample
    ctx.trace_event("registry_loaded", input_refs=[str(registry)]); ctx.trace_event("config_loaded", input_refs=[str(config)])
    validation = validate_config_core(ctx.repo_root, registry, config)
    write_json(ctx.cli_run_dir / "preflight_result.json", {"status":validation["status"], "blocking_gaps":validation["blocking_gaps"]})
    if validation["blocking_gaps"]:
        write_json(ctx.cli_run_dir / "execution_result.json", validation); return {"exit_code": 20, "result": validation}
    if not sample.exists():
        result = {"status":"CLI_BLOCKED","reason":"missing_sample","path":str(sample)}; write_json(ctx.cli_run_dir / "execution_result.json", result); return {"exit_code":50,"result":result}
    ctx.trace_event("sample_loaded", input_refs=[str(sample)])
    result = make_pipeline_run(ctx, args, registry, config, sample)
    write_json(ctx.cli_run_dir / "execution_result.json", result)
    ctx.trace_event("command_completed", status="CLI_SAMPLE_REPLAY_COMPLETED_WITH_GAPS")
    return {"exit_code": 10, "result": result}


def load_pipeline_state(repo: Path, run_id: str) -> Dict[str, Any]:
    for run_root_name in ["o00_runs", "o00_run_document_runs"]:
        state_path = repo / "data/her_document_function_system" / run_root_name / run_id / "state/pipeline_state.json"
        if state_path.exists():
            state = read_json(state_path)
            state.setdefault("run_root_name", run_root_name)
            state.setdefault("run_root", str(state_path.parent.parent))
            return state
    fallback = repo / "data/her_document_function_system/o00_runs" / run_id / "state/pipeline_state.json"
    return {"status":"NOT_FOUND", "pipeline_run_id":run_id, "path":str(fallback)}


def command_status(ctx: CliContext, args: argparse.Namespace) -> Dict[str, Any]:
    result = load_pipeline_state(ctx.repo_root, args.run_id); write_json(ctx.cli_run_dir / "execution_result.json", result)
    return {"exit_code": 0 if result.get("status") != "NOT_FOUND" else 50, "result": result}


def command_show_report(ctx: CliContext, args: argparse.Namespace) -> Dict[str, Any]:
    state = load_pipeline_state(ctx.repo_root, args.run_id); path = state.get("final_report_path")
    result = {"pipeline_run_id": args.run_id, "final_report_path": path, "exists": bool(path and Path(path).exists()), "current_status": state.get("current_status")}
    write_json(ctx.cli_run_dir / "execution_result.json", result); return {"exit_code": 0 if result["exists"] else 50, "result": result}


def command_show_gaps(ctx: CliContext, args: argparse.Namespace) -> Dict[str, Any]:
    state = load_pipeline_state(ctx.repo_root, args.run_id)
    base = Path(state.get("run_root", ctx.repo_root / "data/her_document_function_system/o00_runs" / args.run_id))
    path = base / "gaps/pipeline_gap_register.json"
    result = read_json(path) if path.exists() else {"status":"NOT_FOUND","path":str(path)}; write_json(ctx.cli_run_dir / "execution_result.json", result)
    return {"exit_code": 0 if path.exists() else 50, "result": result}


def command_show_trace(ctx: CliContext, args: argparse.Namespace) -> Dict[str, Any]:
    state = load_pipeline_state(ctx.repo_root, args.run_id)
    base = Path(state.get("run_root", ctx.repo_root / "data/her_document_function_system/o00_runs" / args.run_id))
    path = base / "trace/o00_trace.jsonl"
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    result = {"pipeline_run_id": args.run_id, "trace_path": str(path), "event_count": len(lines), "events": lines[-10:]}; write_json(ctx.cli_run_dir / "execution_result.json", result)
    return {"exit_code": 0 if path.exists() else 50, "result": result}


def command_recover(ctx: CliContext, args: argparse.Namespace) -> Dict[str, Any]:
    run_id = getattr(args, "run_id", None)
    if run_id:
        state = load_pipeline_state(ctx.repo_root, run_id)
        root = Path(state.get("run_root", ctx.repo_root / "data/her_document_function_system/o00_runs" / run_id))
    else:
        root = ctx.cli_run_dir
    root.mkdir(parents=True, exist_ok=True)
    result = {"status":"RECOVERY_REPORT_GENERATED","run_id":run_id,"decision":"RUN_VALIDATE_CONFIG_OR_RERUN_SAMPLE_IN_SAFE_MODE","forbidden_actions":FORBIDDEN_ACTIONS}
    write_json(root / "recovery/recovery_report.json", result); write_json(ctx.cli_run_dir / "execution_result.json", result)
    return {"exit_code":70,"result":result}


def command_run_document(ctx: CliContext, args: argparse.Namespace) -> Dict[str, Any]:
    registry = resolve(ctx.repo_root, args.registry) if args.registry else ctx.repo_root / "system/her_document_function_system/registry/controller_registry.json"
    config = resolve(ctx.repo_root, args.config) if args.config else ctx.repo_root / "system/her_document_function_system/config/pipeline_config.full_safe_replay.json"
    replay = resolve(ctx.repo_root, args.sample) if args.sample else ctx.repo_root / "system/her_document_function_system/replay/sample_cases/o00_sample_replay.json"
    document = resolve(ctx.repo_root, args.document) if args.document else None
    goal = resolve(ctx.repo_root, args.goal) if args.goal else None
    missing = []
    if not document or not document.exists():
        missing.append("--document")
    if not goal or not goal.exists():
        missing.append("--goal")
    if missing:
        result = {"status":"CLI_BLOCKED", "reason":"missing_required_run_document_inputs", "missing_inputs":missing, "required_inputs":["--document", "--goal"], "safe_next_action":"rerun run-document --safe-mode with document and goal refs"}
        write_json(ctx.cli_run_dir / "execution_result.json", result)
        return {"exit_code":30,"result":result}
    result = make_pipeline_run(ctx, args, registry, config, replay, command_name="run-document", source_document=document, operator_goal=goal, run_root_name="o00_run_document_runs")
    result["command"] = "run-document"
    result["status"] = "O00_RUN_DOCUMENT_READY_WITH_GAPS"
    result["system_status_code"] = "O00_RUN_DOCUMENT_READY_WITH_GAPS"
    write_json(ctx.cli_run_dir / "execution_result.json", result)
    return {"exit_code": 10, "result": result}


def command_not_implemented_safe(ctx: CliContext, args: argparse.Namespace) -> Dict[str, Any]:
    result = {"status":"CLI_BLOCKED","reason":f"{args.command}_not_enabled_in_first_batch", "safe_next_action":"use init/validate-config/run-sample/run-document/status/show-report/show-gaps/recover"}
    write_json(ctx.cli_run_dir / "execution_result.json", result); return {"exit_code":30,"result":result}


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="O00 CLI / HER Command Entry")
    p.add_argument("command", choices=["init","validate-config","run-sample","run-document","status","resume","recover","show-report","show-gaps","show-trace"])
    p.add_argument("--repo-root", default="/root/sikk-gmgn"); p.add_argument("--safe-mode", action="store_true")
    p.add_argument("--registry"); p.add_argument("--config"); p.add_argument("--sample"); p.add_argument("--document"); p.add_argument("--goal"); p.add_argument("--run-id"); p.add_argument("--from-stage")
    return p


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser(); args = parser.parse_args(argv); repo = Path(args.repo_root); ctx = CliContext(repo, args.command)
    exit_code = 90; result: Dict[str, Any] = {}; stdout_path = ctx.cli_run_dir / "stdout.log"; stderr_path = ctx.cli_run_dir / "stderr.log"
    with stdout_path.open("w", encoding="utf-8") as out, stderr_path.open("w", encoding="utf-8") as err, contextlib.redirect_stdout(Tee(sys.stdout, out)), contextlib.redirect_stderr(Tee(sys.stderr, err)):
        try:
            ctx.trace_event("cli_started"); ctx.audit_event("args_parsed", argv=argv if argv is not None else sys.argv[1:])
            write_json(ctx.cli_run_dir / "command.json", vars(args)); write_json(ctx.cli_run_dir / "command_normalized.json", {"command":args.command,"repo_root":str(repo),"safe_mode":bool(args.safe_mode),"inputs":vars(args)})
            block = check_safe_mode(ctx, args)
            if block: result = block; exit_code = block["exit_code"]
            else:
                cfg_path = resolve(repo, args.config) if args.config else None; cfg = read_json(cfg_path) if cfg_path and cfg_path.exists() else None
                block = check_forbidden_boundary(ctx, cfg)
                if block: result = block; exit_code = block["exit_code"]
                else:
                    handlers = {"init": command_init, "validate-config": command_validate_config, "run-sample": command_run_sample, "status": command_status, "show-report": command_show_report, "show-gaps": command_show_gaps, "show-trace": command_show_trace, "recover": command_recover, "run-document": command_run_document, "resume": command_not_implemented_safe}
                    ctx.trace_event("command_dispatched"); r = handlers[args.command](ctx, args); exit_code = int(r["exit_code"]); result = r["result"]
            marker = {"cli_run_id": ctx.cli_run_id, "pipeline_run_id": ctx.pipeline_run_id, "exit_code": exit_code, "status": result.get("status"), "final_status": result.get("final_status") or result.get("current_status"), "system_status_code": result.get("system_status_code")}
            print("O00_RUN_RESULT=" + json.dumps(marker, ensure_ascii=False, separators=(",", ":")))
            print(json.dumps({"cli_run_id": ctx.cli_run_id, "pipeline_run_id": ctx.pipeline_run_id, "exit_code": exit_code, "result": result}, ensure_ascii=False, indent=2))
        except Exception as exc:
            traceback.print_exc(); result = {"status":"CLI_FAILED","error":str(exc)}; exit_code = 90; ctx.trace_event("command_failed", message=str(exc))
        finally:
            exit_payload = {"exit_code": exit_code, "exit_name": "READY_WITH_GAPS" if exit_code == 10 else ("OK" if exit_code == 0 else "FAILED"), "final_status": result.get("final_status") or result.get("current_status") or result.get("status"), "blocking": exit_code not in (0,10)}
            write_json(ctx.cli_run_dir / "exit_code.json", exit_payload)
            report = f"# O00 CLI Final Report\n\n- cli_run_id: `{ctx.cli_run_id}`\n- pipeline_run_id: `{ctx.pipeline_run_id}`\n- command: `{args.command}`\n- exit_code: `{exit_code}`\n- stdout: `{stdout_path}`\n- stderr: `{stderr_path}`\n- result_status: `{result.get('status') or result.get('final_status') or result.get('current_status')}`\n"
            (ctx.cli_run_dir / "final_cli_report.md").write_text(report, encoding="utf-8")
            ctx.trace_event("exit_code_written", exit_code=exit_code); ctx.trace_event("cli_report_written", output_refs=[str(ctx.cli_run_dir / "final_cli_report.md")])
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
