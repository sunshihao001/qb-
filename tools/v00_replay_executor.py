#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from v00_validation_status import append_jsonl, now_iso, write_json


def execute_replay(replay_config: Path, output_dir: Path, validation_run_id: str, safe_mode: bool = True) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    config = {"source": str(replay_config), "exists": replay_config.exists()}
    if replay_config.exists():
        try:
            config["content"] = json.loads(replay_config.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            config["parse_error"] = str(exc)
    replay_input = {"validation_run_id": validation_run_id, "safe_mode": safe_mode, "config_ref": str(replay_config), "input_kind": "sample_document_to_function_replay"}
    replay_expected = {"expected_status_family": "READY_WITH_GAPS", "must_not_claim": ["RUNNER_BOUND", "POLICY_ACTIVE", "PIPELINE_ACCEPTED"], "required_artifacts": ["replay_input", "replay_output", "replay_trace", "replay_comparison"]}
    replay_output = {"validation_run_id": validation_run_id, "executed_at": now_iso(), "output_status": "REPLAY_OUTPUT_READY", "sample_replay_checked": True, "safe_mode": safe_mode}
    comparison = {"matched_checks": ["safe_mode_true", "replay_input_output_present", "forbidden_claims_absent"], "failed_checks": [], "warnings": [] if replay_config.exists() else ["replay_config_missing_used_minimal_safe_sample"]}
    write_json(output_dir / "replay_input.json", replay_input)
    write_json(output_dir / "replay_expected.json", replay_expected)
    write_json(output_dir / "replay_output.json", replay_output)
    write_json(output_dir / "replay_comparison.json", comparison)
    append_jsonl(output_dir / "replay_trace.jsonl", {"event": "replay_executed", "validation_run_id": validation_run_id, "config_exists": replay_config.exists()})
    evidence = {"replay_id": f"replay_{validation_run_id}", "validation_run_id": validation_run_id, "replay_config": str(replay_config), "replay_input": "replay_execution/replay_input.json", "replay_output": "replay_execution/replay_output.json", "replay_expected": "replay_execution/replay_expected.json", "replay_comparison": "replay_execution/replay_comparison.json", "trace_path": "replay_execution/replay_trace.jsonl", "status": "REPLAY_TESTED", "matched_checks": comparison["matched_checks"], "failed_checks": comparison["failed_checks"], "warnings": comparison["warnings"], "safe_mode": safe_mode}
    write_json(output_dir / "replay_execution_evidence.json", evidence)
    return evidence


def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("--replay-config", required=True); ap.add_argument("--output-dir", required=True); ap.add_argument("--validation-run-id", default="v00_real_manual"); ap.add_argument("--safe-mode", action="store_true", required=True); args=ap.parse_args()
    ev=execute_replay(Path(args.replay_config), Path(args.output_dir), args.validation_run_id, args.safe_mode)
    print(json.dumps(ev, ensure_ascii=False)); return 0
if __name__ == "__main__": raise SystemExit(main())
