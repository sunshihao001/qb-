#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from v00_contract_validator import validate_contracts_dir
from v00_evidence_bundle_builder import build_bundle
from v00_field_model_validator import validate_field_model
from v00_replay_executor import execute_replay
from v00_rule_logic_validator import validate_rule_logic
from v00_schema_validator import validate_schema_dir
from v00_test_runner import run_tests
from v00_validation_status import FINAL_STATUS, append_jsonl, ensure_dirs, now_iso, read_json, status_from_failures, write_json


def _failure(failure_id: str, failure_type: str, source_step: str, affected_asset: str, reason: str, refs: list[str], can_continue: bool = False) -> dict:
    return {"failure_id": failure_id, "failure_type": failure_type, "source_step": source_step, "affected_asset": affected_asset, "gap_level": "BLOCKING_GAP" if not can_continue else "NON_BLOCKING_GAP", "failure_reason": reason, "evidence_refs": refs, "required_fix": "Fix failing validation input or implementation and rerun V00 real validation", "can_continue": can_continue}


def build_report(output_dir: Path, validation_run_id: str, source_pipeline_run_id: str, final_status: str, bundle: dict) -> None:
    report = f"""# V00 Real Validation Evidence Report

## 1. Run Info
- validation_run_id: {validation_run_id}
- source_pipeline_run_id: {source_pipeline_run_id}
- safe_mode: true
- final_status: {final_status}

## 2. Evidence Bundle
- bundle_path: evidence_bundle/validation_evidence_bundle.json
- schema_status: {bundle['summary'].get('schema_status')}
- contract_status: {bundle['summary'].get('contract_status')}
- field_model_status: {bundle['summary'].get('field_model_status')}
- rule_logic_status: {bundle['summary'].get('rule_logic_status')}
- test_status: {bundle['summary'].get('test_status')}
- replay_status: {bundle['summary'].get('replay_status')}

## 3. Gap Summary
- blocking_gaps: {len(bundle.get('blocking_gaps', []))}
- open_gaps: {len(bundle.get('open_gaps', []))}

## 4. Allowed Next Actions
- A00 acceptance evidence review
- R00 safe dry-run binding design/implementation only after explicit downstream handoff

## 5. Forbidden Next Actions
- RUNNER_BOUND claim
- POLICY_ACTIVE claim
- PIPELINE_ACCEPTED claim
- live_runtime / wallet_signing / auto_deploy / production_trading

## 6. Final Decision
{final_status}
"""
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "reports/v00_real_validation_report.md").write_text(report, encoding="utf-8")


def execute(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root)
    output_dir = Path(args.output_dir)
    validation_run_id = output_dir.name or f"v00_real_{now_iso()}"
    ensure_dirs(output_dir)
    trace = output_dir / "trace/v00_real_validation_trace.jsonl"
    audit = output_dir / "audit/v00_real_validation_audit.jsonl"
    failures: list[dict] = []
    started_at = now_iso()

    append_jsonl(trace, {"event": "v00_started", "validation_run_id": validation_run_id})
    append_jsonl(audit, {"event": "safe_mode_asserted", "safe_mode": bool(args.safe_mode)})
    if not args.safe_mode:
        failures.append(_failure("failure_safe_mode", "FORBIDDEN_ACTION_DETECTED", "V00_REAL.0", "safe_mode", "safe_mode must be true", [], False))

    pipeline_path = repo_root / args.pipeline_run if not Path(args.pipeline_run).is_absolute() else Path(args.pipeline_run)
    f00_path = None
    if args.f00_handoff:
        f00_path = repo_root / args.f00_handoff if not Path(args.f00_handoff).is_absolute() else Path(args.f00_handoff)

    pipeline = read_json(pipeline_path) if pipeline_path.exists() else {}
    source_pipeline_run_id = pipeline.get("pipeline_run_id", "UNKNOWN_PIPELINE_RUN")
    f00 = read_json(f00_path) if f00_path and f00_path.exists() else {}
    preflight_blockers = []
    if not pipeline_path.exists(): preflight_blockers.append("o00_pipeline_run_missing")
    if f00_path and not f00_path.exists(): preflight_blockers.append("f00_handoff_missing")
    if pipeline.get("system_status_code") != "O00_CLI_SAMPLE_REPLAY_READY_WITH_GAPS":
        preflight_blockers.append("upstream_status_not_o00_cli_sample_replay_ready_with_gaps")
    preflight = {"preflight_status": "PASSED" if not preflight_blockers and args.safe_mode else "BLOCKED", "safe_mode": bool(args.safe_mode), "loaded_inputs": ["o00_pipeline_run", "f00_handoff", "function_mapping", "field_model", "rule_logic", "schema_refs", "contract_refs", "test_plan", "replay_plan"], "forbidden_actions_checked": ["live_runtime", "wallet_signing", "auto_deploy", "production_trading"], "blocking_gaps": preflight_blockers, "pipeline_run_ref": str(pipeline_path), "f00_handoff_ref": str(f00_path) if f00_path else None, "f00_handoff_status": f00.get("status")}
    write_json(output_dir / "preflight/v00_real_validation_preflight.json", preflight)
    write_json(output_dir / "input/o00_pipeline_run_ref.json", {"path": str(pipeline_path), "loaded": bool(pipeline)})
    write_json(output_dir / "input/f00_handoff_ref.json", {"path": str(f00_path) if f00_path else None, "loaded": bool(f00)})
    if preflight["preflight_status"] == "BLOCKED":
        failures.append(_failure("failure_preflight", "CONTRACT_INVALID", "V00_REAL.0", str(pipeline_path), ", ".join(preflight_blockers), ["preflight/v00_real_validation_preflight.json"], False))

    schema = validate_schema_dir(repo_root / "system/her_document_function_system", output_dir / "schema_validation", True)
    append_jsonl(trace, {"event": "schema_validation_done", "status": schema["status"]})
    contract = validate_contracts_dir(repo_root / "system/her_document_function_system", output_dir / "contract_validation", True)
    append_jsonl(trace, {"event": "contract_validation_done", "status": contract["status"]})
    field = validate_field_model(repo_root / "data/her_document_function_system/o00_runs" / source_pipeline_run_id / "evidence/field_model.json", output_dir / "field_model_validation", True)
    rule = validate_rule_logic(repo_root / "data/her_document_function_system/o00_runs" / source_pipeline_run_id / "evidence/rule_logic.json", output_dir / "rule_logic_validation", True)

    test = run_tests(repo_root / "tests/her_document_function_system", output_dir / "test_execution", repo_root, validation_run_id, True)
    append_jsonl(trace, {"event": "test_command_executed", "exit_code": test["exit_code"], "status": test["status"]})
    if test["exit_code"] != 0:
        failures.append(_failure("failure_test_execution", "TEST_FAILED", "V00_REAL.6", "tests/her_document_function_system", "pytest exit_code != 0", ["test_execution/test_stdout.log", "test_execution/test_stderr.log"], False))

    replay_config = repo_root / "system/her_document_function_system/replay/sample_cases/sample_001_document_to_function/run/replay_run_config.json"
    replay = execute_replay(replay_config, output_dir / "replay_execution", validation_run_id, True)
    append_jsonl(trace, {"event": "replay_tested", "status": replay["status"]})

    failure_evidence = {"failure_evidence_id": f"failure_{validation_run_id}", "validation_run_id": validation_run_id, "failures": failures}
    write_json(output_dir / "failure_evidence/failure_evidence.json", failure_evidence)
    append_jsonl(audit, {"event": "failure_evidence_written", "failure_count": len(failures)})

    bundle = build_bundle(output_dir, validation_run_id, source_pipeline_run_id, failures)
    append_jsonl(trace, {"event": "bundle_built", "final_status": bundle["summary"]["final_validation_status"]})
    final_status = status_from_failures(FINAL_STATUS, failures)
    acceptance = {"validation_run_id": validation_run_id, "accepted_for_a00_review": not failures, "final_status": final_status, "ready_for_a00": not failures, "ready_for_r00": False, "forbidden_claims_blocked": ["RUNNER_BOUND", "POLICY_ACTIVE", "PIPELINE_ACCEPTED"]}
    write_json(output_dir / "acceptance/v00_real_validation_acceptance.json", acceptance)
    handoff = {"validation_run_id": validation_run_id, "from_phase": "V00_REAL_VALIDATION", "to_phase": "A00", "status": final_status, "evidence_bundle_ref": "evidence_bundle/validation_evidence_bundle.json", "failure_evidence_ref": "failure_evidence/failure_evidence.json", "ready_for_r00": False}
    write_json(output_dir / "handoff/v00_real_validation_to_a00_handoff.json", handoff)
    build_report(output_dir, validation_run_id, source_pipeline_run_id, final_status, bundle)
    append_jsonl(audit, {"event": "v00_completed", "started_at": started_at, "completed_at": now_iso(), "final_status": final_status})
    print(json.dumps({"validation_run_id": validation_run_id, "final_status": final_status, "output_dir": str(output_dir)}, ensure_ascii=False))
    return 2 if failures else 10


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pipeline-run", required=True)
    ap.add_argument("--f00-handoff", default=None)
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--safe-mode", action="store_true", required=True)
    return execute(ap.parse_args())

if __name__ == "__main__":
    raise SystemExit(main())
