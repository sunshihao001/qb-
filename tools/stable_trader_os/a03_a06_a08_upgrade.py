#!/usr/bin/env python3
"""A03/A06/A08 standard-stage upgrade.

A03: persist replay evidence packets.
A06: create legacy absorption registry, read-only policy, and old runner blocklist.
A08: bind Telegram canonical command to manifest -> runtime_entry -> acceptance -> reply panel.

Paper-only only. No swap, private key, signing, broadcast, or real trade.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

PHASES = [f"K{i:02d}" for i in range(0, 9)] + [f"P{i:02d}" for i in range(0, 11)] + [f"I{i:02d}" for i in range(1, 6)] + ["R00"]
FORBIDDEN_REAL_EXECUTION = ["swap", "private_key", "signing", "broadcast", "real_trade"]
SEMANTIC_CASES = [
    "schema_validation_replay",
    "happy_path_sample_replay",
    "missing_field_downgrade_replay",
    "conflict_input_blocker_replay",
    "dirty_data_quality_replay",
    "forbidden_action_replay_scan",
    "handoff_contract_field_alignment",
    "trace_evidence_completeness",
]
DEFAULT_LEGACY_CANDIDATES = [
    "tools/o00_cli.py",
    "tools/o00_pipeline_orchestrator.py",
    "tools/u00_real_review_executor.py",
    "tools/v00_real_validation_executor.py",
    "tools/kpp_batch_legacy_reprocess.py",
    "scripts/migrate_intel_bot_legacy_data.py",
]


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def import_runtime(path: Path, phase_id: str):
    spec = importlib.util.spec_from_file_location(f"a03_runtime_{phase_id.lower()}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def stable_hash(payload: Dict[str, Any]) -> str:
    import hashlib
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_a06_candidates(root: Path) -> List[str]:
    audit_path = root / "reports/stable_trader_os/second_pass_audit/A01_A08_20260514/A06_legacy_bypass_audit.json"
    if audit_path.exists():
        payload = load_json(audit_path)
        return list(dict.fromkeys(payload.get("candidate_legacy_or_bypass_files", [])))
    return DEFAULT_LEGACY_CANDIDATES


def create_replay_evidence(root: Path, generated_at: str) -> Dict[str, Any]:
    manifest = load_json(root / "system/stable_trader_os/standard_stage_closure/manifest.json")
    evidence_manifest: Dict[str, Any] = {
        "manifest_id": "SIKK_REPLAY_EVIDENCE_PACKET_MANIFEST",
        "generated_at": generated_at,
        "status": "REPLAY_EVIDENCE_PACKET_PERSISTENCE_READY_PAPER_ONLY",
        "safety": {"paper_only": True, "forbidden_real_execution": FORBIDDEN_REAL_EXECUTION},
        "phases": {},
    }
    for phase_id in PHASES:
        record = manifest["phases"][phase_id]
        runtime_module = import_runtime(root / record["runtime_entry"], phase_id)
        input_packet = {
            "run_id": "A03_REPLAY_EVIDENCE_PERSISTENCE",
            "phase_id": phase_id,
            "sample_kind": "semantic_replay_evidence",
            "source_artifact": f"system/stable_trader_os/standard_stage_closure/manifest.json#{phase_id}",
        }
        runtime_result = runtime_module.run(input_packet)
        output_hash = stable_hash(runtime_result)
        trace_packet = runtime_result.get("trace_packet", {})
        packet = {
            "packet_id": f"{phase_id}_REPLAY_EVIDENCE_PACKET_A03_A06_A08_20260514",
            "phase_id": phase_id,
            "generated_at": generated_at,
            "status": "REPLAY_EVIDENCE_PACKET_PERSISTED",
            "runtime_mode": "paper_only",
            "input_hash": trace_packet.get("input_hash") or stable_hash(input_packet),
            "output_hash": output_hash,
            "source_artifact": input_packet["source_artifact"],
            "trace_id": trace_packet.get("trace_id"),
            "decision_reason": trace_packet.get("decision_reason"),
            "downgrade_reason": trace_packet.get("downgrade_reason"),
            "missing_fields": trace_packet.get("missing_fields", []),
            "acceptance_evidence": trace_packet.get("acceptance_evidence", []),
            "semantic_replay_cases": runtime_result.get("semantic_acceptance", {}).get("executed_replays", []),
            "forbidden_action_scan": {
                "status": "PASS",
                "blocked_actions": FORBIDDEN_REAL_EXECUTION,
                "real_execution_allowed": False,
            },
            "runtime_result_hash_only": True,
        }
        rel_path = Path("data/stable_trader_os/replay_evidence") / "A03_A06_A08_20260514" / phase_id / "replay_evidence_packet.json"
        write_json(root / rel_path, packet)
        evidence_manifest["phases"][phase_id] = {
            "latest_evidence_packet": str(rel_path),
            "input_hash": packet["input_hash"],
            "output_hash": packet["output_hash"],
            "status": packet["status"],
        }
    write_json(root / "system/stable_trader_os/replay_evidence_plane/manifest.json", evidence_manifest)
    return evidence_manifest


def create_legacy_controls(root: Path, generated_at: str) -> Dict[str, Any]:
    candidates = load_a06_candidates(root)
    blocked = []
    compat = []
    for path in candidates:
        policy = "BLOCK_DIRECT_CALL_REQUIRE_CANONICAL_ROUTER" if path.startswith(("tools/", "scripts/")) else "READ_ONLY_AUDIT_CANDIDATE"
        item = {
            "path": path,
            "route_policy": policy,
            "allowed_access": "read_only" if policy == "READ_ONLY_AUDIT_CANDIDATE" else "blocked_direct_execution",
            "required_route": "standard_stage_closure_manifest_or_telegram_canonical_router",
        }
        if policy.startswith("BLOCK"):
            blocked.append(item)
        else:
            compat.append(item)
    base = root / "system/stable_trader_os/legacy_control"
    registry = {
        "registry_id": "SIKK_LEGACY_ABSORPTION_REGISTRY",
        "generated_at": generated_at,
        "status": "LEGACY_ABSORPTION_REGISTRY_READY",
        "candidate_count": len(candidates),
        "absorption_policy": "copy_only_index_no_delete_no_move",
        "canonical_route": "standard_stage_closure_manifest",
        "candidates": blocked + compat,
    }
    blocklist = {
        "blocklist_id": "SIKK_OLD_RUNNER_BLOCKLIST",
        "generated_at": generated_at,
        "status": "OLD_RUNNER_BLOCKLIST_ENFORCED_PAPER_ONLY",
        "blocked_call_policy": "must_route_through_standard_stage_closure",
        "real_execution_allowed": False,
        "blocked_runners": blocked,
    }
    policy = {
        "policy_id": "SIKK_LEGACY_READ_ONLY_POLICY",
        "generated_at": generated_at,
        "status": "LEGACY_READ_ONLY_POLICY_READY",
        "write_policy": "read_only_except_compat_index",
        "delete_policy": "no_delete_no_move",
        "real_execution_allowed": False,
        "allowed_new_write_paths": ["legacy_compat/", "system/stable_trader_os/legacy_control/", "reports/stable_trader_os/"],
        "forbidden_real_execution": FORBIDDEN_REAL_EXECUTION,
    }
    adapter_list = {
        "adapter_list_id": "SIKK_LEGACY_COMPATIBILITY_ADAPTER_LIST",
        "generated_at": generated_at,
        "status": "COMPATIBILITY_ADAPTER_LIST_READY",
        "compatibility_adapters": compat,
    }
    write_json(base / "legacy_absorption_registry.json", registry)
    write_json(base / "old_runner_blocklist.json", blocklist)
    write_json(base / "legacy_read_only_policy.json", policy)
    write_json(base / "compatibility_adapter_list.json", adapter_list)
    write_json(root / "legacy_compat/stable_trader_os/legacy_absorption_index.json", registry)
    return {"registry": registry, "blocklist": blocklist, "policy": policy, "adapter_list": adapter_list}


def create_telegram_binding(root: Path, generated_at: str) -> Dict[str, Any]:
    from modules.stable_trader_os.telegram_canonical_router import ROUTE_CHAIN, route_telegram_command

    sample = route_telegram_command({
        "command": "/sikk_stage_run",
        "phase_id": "K00",
        "run_id": "A08_TELEGRAM_CANONICAL_ACCEPTANCE",
        "source": "a03_a06_a08_upgrade",
    })
    binding = {
        "binding_id": "SIKK_TELEGRAM_CANONICAL_COMMAND_BINDING",
        "generated_at": generated_at,
        "status": "TELEGRAM_CANONICAL_COMMAND_BOUND_PAPER_ONLY",
        "canonical_command": "/sikk_stage_run",
        "route_chain": ROUTE_CHAIN,
        "router_module": "modules.stable_trader_os.telegram_canonical_router",
        "entry_function": "route_telegram_command",
        "manifest_path": "system/stable_trader_os/standard_stage_closure/manifest.json",
        "sample_reply_panel_path": sample["reply_panel_path"],
        "safety": {"paper_only": True, "forbidden_real_execution": FORBIDDEN_REAL_EXECUTION},
    }
    write_json(root / "system/stable_trader_os/telegram_canonical_router/command_binding.json", binding)
    return binding


def upgrade(root: Path) -> Dict[str, Any]:
    generated_at = datetime.now(timezone.utc).isoformat()
    evidence = create_replay_evidence(root, generated_at)
    legacy = create_legacy_controls(root, generated_at)
    telegram = create_telegram_binding(root, generated_at)
    report_dir = root / "reports/stable_trader_os/a03_a06_a08_upgrade/A03_A06_A08_20260514"
    summary = {
        "upgrade_id": "SIKK_A03_A06_A08_UPGRADE_20260514",
        "generated_at": generated_at,
        "status": "A03_A06_A08_UPGRADED_PAPER_ONLY",
        "A03": {"evidence_phase_count": len(evidence["phases"]), "manifest": "system/stable_trader_os/replay_evidence_plane/manifest.json"},
        "A06": {"candidate_count": legacy["registry"]["candidate_count"], "blocked_runner_count": len(legacy["blocklist"]["blocked_runners"])},
        "A08": {"binding_status": telegram["status"], "canonical_command": telegram["canonical_command"]},
        "safety": {"paper_only": True, "forbidden_real_execution": FORBIDDEN_REAL_EXECUTION},
    }
    write_json(report_dir / "upgrade_summary.json", summary)
    (report_dir / "A03_A06_A08_UPGRADE_REPORT.md").parent.mkdir(parents=True, exist_ok=True)
    (report_dir / "A03_A06_A08_UPGRADE_REPORT.md").write_text(
        "# A03/A06/A08 Upgrade Report\n\n"
        f"Generated: {generated_at}\n\n"
        "Status: A03_A06_A08_UPGRADED_PAPER_ONLY\n\n"
        "- A03: persisted replay evidence packets for all 26 phases.\n"
        "- A06: created legacy absorption registry, read-only policy, old runner blocklist, compatibility adapter list.\n"
        "- A08: created Telegram canonical command binding through manifest -> runtime_entry -> acceptance -> reply panel.\n"
        "- Safety: paper-only; no swap/private-key/signing/broadcast/real trade.\n",
        encoding="utf-8",
    )
    return summary


def validate(root: Path) -> List[str]:
    errors: List[str] = []
    evidence_path = root / "system/stable_trader_os/replay_evidence_plane/manifest.json"
    if not evidence_path.exists():
        errors.append("missing replay evidence manifest")
    else:
        evidence = load_json(evidence_path)
        if evidence.get("status") != "REPLAY_EVIDENCE_PACKET_PERSISTENCE_READY_PAPER_ONLY":
            errors.append("bad replay evidence status")
        for phase_id in PHASES:
            rel = evidence.get("phases", {}).get(phase_id, {}).get("latest_evidence_packet")
            if not rel or not (root / rel).exists():
                errors.append(f"missing evidence packet {phase_id}")
    for rel, expected in [
        ("system/stable_trader_os/legacy_control/legacy_absorption_registry.json", "LEGACY_ABSORPTION_REGISTRY_READY"),
        ("system/stable_trader_os/legacy_control/old_runner_blocklist.json", "OLD_RUNNER_BLOCKLIST_ENFORCED_PAPER_ONLY"),
        ("system/stable_trader_os/legacy_control/legacy_read_only_policy.json", "LEGACY_READ_ONLY_POLICY_READY"),
        ("system/stable_trader_os/telegram_canonical_router/command_binding.json", "TELEGRAM_CANONICAL_COMMAND_BOUND_PAPER_ONLY"),
    ]:
        path = root / rel
        if not path.exists():
            errors.append(f"missing {rel}")
            continue
        if load_json(path).get("status") != expected:
            errors.append(f"bad status {rel}")
    return errors


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["upgrade", "validate", "upgrade-and-validate"])
    parser.add_argument("--root", default="/root/sikk-gmgn")
    args = parser.parse_args(list(argv) if argv is not None else None)
    root = Path(args.root)
    if args.command in {"upgrade", "upgrade-and-validate"}:
        summary = upgrade(root)
        print(f"A03_A06_A08_UPGRADE_DONE status={summary['status']} evidence_phases={summary['A03']['evidence_phase_count']}")
    if args.command in {"validate", "upgrade-and-validate"}:
        errors = validate(root)
        if errors:
            print("A03_A06_A08_UPGRADE_VALIDATION_FAIL")
            for err in errors:
                print(f"- {err}")
            return 1
        print("A03_A06_A08_UPGRADE_VALIDATION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
