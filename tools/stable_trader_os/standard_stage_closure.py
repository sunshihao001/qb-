#!/usr/bin/env python3
"""Standard stage closure generator/validator for SIKK Stable Trader OS.

Creates additive paper-only standard assets for K00-K08, P00-P10, I01-I05 and R00:
controller + schema + contract + trace + acceptance + handoff + runtime entry.

Safety: this tool never performs swap, signing, broadcast, private-key access, or real trading.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List

PHASES: List[str] = [f"K{i:02d}" for i in range(0, 9)] + [f"P{i:02d}" for i in range(0, 11)] + [f"I{i:02d}" for i in range(1, 6)] + ["R00"]
FORBIDDEN_REAL_EXECUTION = ["swap", "private_key", "signing", "broadcast", "real_trade"]

PHASE_NAMES: Dict[str, str] = {
    "K00": "knowledge_intake_entry",
    "K01": "knowledge_source_passport",
    "K02": "knowledge_field_mapping",
    "K03": "knowledge_candidate_extraction",
    "K04": "knowledge_gap_detection",
    "K05": "knowledge_governance_queue",
    "K06": "knowledge_contract_projection",
    "K07": "knowledge_acceptance_review",
    "K08": "knowledge_system_upgrade_candidate",
    "P00": "bootstrap_control_plane",
    "P01": "candidate_intake",
    "P02": "source_data_fact",
    "P03": "wallet_entity",
    "P04": "chip_structure",
    "P05": "evidence",
    "P06": "scenario_recognition",
    "P07": "strategy_gate",
    "P08": "execution_risk",
    "P09": "review_replay",
    "P10": "self_upgrade",
    "I01": "intake_manifest",
    "I02": "task_packet",
    "I03": "runner_binding",
    "I04": "phase_state_acceptance",
    "I05": "review_upgrade",
    "R00": "paper_only_runtime_entry",
}


def slug(phase_id: str) -> str:
    return f"{phase_id.lower()}_standard_stage"


def rel(path: Path, root: Path) -> str:
    return str(path.relative_to(root))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_phase_assets(root: Path, phase_id: str, generated_at: str) -> Dict[str, str]:
    name = PHASE_NAMES[phase_id]
    phase_slug = slug(phase_id)
    controller_dir = root / "system" / "phase_controllers" / phase_slug
    schema_dir = root / "schemas" / "stable_trader_os" / phase_slug
    contract_dir = root / "contracts" / "stable_trader_os" / phase_slug
    runtime_dir = root / "modules" / "stable_trader_os" / phase_slug
    trace_dir = root / "system" / "trace_plane" / phase_slug
    acceptance_dir = root / "system" / "acceptance_plane" / phase_slug
    handoff_dir = root / "system" / "handoff_plane" / phase_slug

    upstream = "SYSTEM_BOOTSTRAP" if phase_id in {"K00", "P00", "I01", "R00"} else "PREVIOUS_STANDARD_STAGE_HANDOFF"
    downstream = "STANDARD_STAGE_HANDOFF_CONSUMER"

    controller = {
        "controller_id": f"{phase_id}_STANDARD_STAGE_CONTROLLER",
        "phase_id": phase_id,
        "phase_name": name,
        "status": "STANDARD_STAGE_CLOSED_PAPER_ONLY",
        "runtime_mode": "paper_only",
        "generated_at": generated_at,
        "purpose": "Provide standard controller/schema/contract/trace/acceptance/handoff closure without enabling real execution.",
        "required_assets": ["schema", "contract", "trace", "acceptance", "handoff", "runtime_entry"],
        "forbidden_actions": FORBIDDEN_REAL_EXECUTION,
        "upstream": upstream,
        "downstream": downstream,
    }
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": f"{phase_id} Standard Stage Packet",
        "type": "object",
        "required": ["phase_id", "status", "runtime_mode", "trace_refs", "acceptance", "handoff"],
        "properties": {
            "phase_id": {"const": phase_id},
            "status": {"type": "string"},
            "runtime_mode": {"const": "paper_only"},
            "trace_refs": {"type": "array", "items": {"type": "string"}},
            "acceptance": {"type": "object"},
            "handoff": {"type": "object"},
        },
        "additionalProperties": True,
    }
    contract = {
        "contract_id": f"{phase_id}_STANDARD_STAGE_CONTRACT",
        "phase_id": phase_id,
        "phase_name": name,
        "runtime_mode": "paper_only",
        "input_contract": {"required_upstream_handoff": upstream, "missing_policy": "downgrade_or_block_never_fabricate"},
        "output_contract": {"required_outputs": ["trace_packet", "acceptance_result", "handoff_packet"]},
        "permissions": {
            "real_execution_allowed": False,
            "private_key_access_allowed": False,
            "signing_allowed": False,
            "broadcast_allowed": False,
            "network_swap_allowed": False,
        },
        "allowed_outputs": ["PAPER_ONLY_RUNTIME_STAGE", "TRACE_PACKET", "ACCEPTANCE_RESULT", "HANDOFF_PACKET"],
        "forbidden_actions": FORBIDDEN_REAL_EXECUTION,
    }
    trace = {
        "trace_id": f"{phase_id}_STANDARD_STAGE_TRACE",
        "phase_id": phase_id,
        "status": "TRACE_TEMPLATE_READY",
        "required_trace_fields": ["run_id", "phase_id", "input_refs", "output_refs", "downgrade_reasons", "forbidden_action_check"],
        "forbidden_action_check": {key: False for key in FORBIDDEN_REAL_EXECUTION},
    }
    acceptance = {
        "acceptance_id": f"{phase_id}_STANDARD_STAGE_ACCEPTANCE",
        "phase_id": phase_id,
        "status": "ACCEPTANCE_TEMPLATE_READY",
        "pass_status": "STANDARD_STAGE_CLOSED_PAPER_ONLY",
        "checks": [
            "controller_exists",
            "schema_exists",
            "contract_exists",
            "trace_exists",
            "handoff_exists",
            "runtime_entry_exists",
            "paper_only_permissions_enforced",
            "no_real_execution_fields_enabled",
        ],
    }
    handoff = {
        "handoff_id": f"{phase_id}_STANDARD_STAGE_HANDOFF",
        "phase_id": phase_id,
        "status": "HANDOFF_TEMPLATE_READY",
        "handoff_status": "READY_FOR_DOWNSTREAM_READ_WITH_PAPER_ONLY_BOUNDARY",
        "required_downstream_policy": "read_standard_handoff_only; do_not_infer_from_legacy_or_chat",
        "fields": ["phase_id", "status", "runtime_mode", "trace_refs", "acceptance_result_path", "next_phase_refs", "blocked_real_execution"],
    }
    runtime_py = f'''"""Paper-only runtime entry for {phase_id} standard stage."""

PHASE_ID = "{phase_id}"
RUNTIME_MODE = "paper_only"
FORBIDDEN_REAL_EXECUTION = {FORBIDDEN_REAL_EXECUTION!r}


def run(input_packet=None):
    """Return a deterministic paper-only standard stage packet; performs no real execution."""
    return {{
        "phase_id": PHASE_ID,
        "status": "STANDARD_STAGE_CLOSED_PAPER_ONLY",
        "runtime_mode": RUNTIME_MODE,
        "input_packet": input_packet or {{}},
        "trace_refs": [f"{{PHASE_ID}}_STANDARD_STAGE_TRACE"],
        "acceptance": {{"status": "ACCEPTANCE_TEMPLATE_READY", "paper_only": True}},
        "handoff": {{"status": "READY_FOR_DOWNSTREAM_READ_WITH_PAPER_ONLY_BOUNDARY"}},
        "blocked_real_execution": FORBIDDEN_REAL_EXECUTION,
    }}
'''

    controller_path = controller_dir / "controller.json"
    schema_path = schema_dir / "schema.json"
    contract_path = contract_dir / "contract.json"
    trace_path = trace_dir / "trace_packet_template.json"
    acceptance_path = acceptance_dir / "acceptance_gate.json"
    handoff_path = handoff_dir / "handoff_contract.json"
    runtime_path = runtime_dir / "runtime_entry.py"
    init_path = runtime_dir / "__init__.py"
    readme_path = controller_dir / "README.md"

    write_json(controller_path, controller)
    write_json(schema_path, schema)
    write_json(contract_path, contract)
    write_json(trace_path, trace)
    write_json(acceptance_path, acceptance)
    write_json(handoff_path, handoff)
    write_text(runtime_path, runtime_py)
    write_text(init_path, f"from .runtime_entry import run\n\n__all__ = ['run']\n")
    write_text(readme_path, f"# {phase_id} Standard Stage Controller\n\nStatus: STANDARD_STAGE_CLOSED_PAPER_ONLY.\n\nThis additive wrapper closes controller/schema/contract/trace/acceptance/handoff assets and forbids swap, private key access, signing, broadcast, and real trading.\n")

    return {
        "controller": rel(controller_path, root),
        "schema": rel(schema_path, root),
        "contract": rel(contract_path, root),
        "trace": rel(trace_path, root),
        "acceptance": rel(acceptance_path, root),
        "handoff": rel(handoff_path, root),
        "runtime_entry": rel(runtime_path, root),
        "status": "STANDARD_STAGE_CLOSED_PAPER_ONLY",
    }


def generate(root: Path) -> dict:
    generated_at = datetime.now(timezone.utc).isoformat()
    phases = {phase_id: build_phase_assets(root, phase_id, generated_at) for phase_id in PHASES}
    manifest = {
        "manifest_id": "SIKK_STANDARD_STAGE_CLOSURE_MANIFEST",
        "generated_at": generated_at,
        "scope": PHASES,
        "status": "STANDARD_STAGE_CLOSURE_GENERATED",
        "safety": {"paper_only": True, "forbidden_real_execution": FORBIDDEN_REAL_EXECUTION},
        "phases": phases,
    }
    manifest_path = root / "system" / "stable_trader_os" / "standard_stage_closure" / "manifest.json"
    write_json(manifest_path, manifest)
    report = root / "reports" / "stable_trader_os" / "standard_stage_closure" / "STANDARD_STAGE_CLOSURE_REPORT.md"
    lines = ["# Standard Stage Closure Report", "", f"Generated: {generated_at}", "", "Safety: paper-only; no swap/private-key/signing/broadcast/real trade.", "", "## Closed phases"]
    for phase_id in PHASES:
        lines.append(f"- {phase_id}: STANDARD_STAGE_CLOSED_PAPER_ONLY")
    write_text(report, "\n".join(lines) + "\n")
    return manifest


def validate(root: Path) -> List[str]:
    manifest_path = root / "system" / "stable_trader_os" / "standard_stage_closure" / "manifest.json"
    errors: List[str] = []
    if not manifest_path.exists():
        return [f"missing manifest: {manifest_path}"]
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover
        return [f"manifest parse error: {exc}"]
    if manifest.get("safety", {}).get("paper_only") is not True:
        errors.append("manifest safety.paper_only is not true")
    if manifest.get("safety", {}).get("forbidden_real_execution") != FORBIDDEN_REAL_EXECUTION:
        errors.append("manifest forbidden_real_execution mismatch")
    phases = manifest.get("phases", {})
    for phase_id in PHASES:
        record = phases.get(phase_id)
        if not isinstance(record, dict):
            errors.append(f"missing phase record {phase_id}")
            continue
        allowed_status = {
            "STANDARD_STAGE_CLOSED_PAPER_ONLY",
            "BUSINESS_BOUND_STAGE_READY_PAPER_ONLY",
        }
        if record.get("status") not in allowed_status:
            errors.append(f"bad status for {phase_id}: {record.get('status')}")
        for key in ["controller", "schema", "contract", "trace", "acceptance", "handoff", "runtime_entry"]:
            rel_path = record.get(key)
            if not rel_path or not (root / rel_path).exists():
                errors.append(f"missing {phase_id} {key}: {rel_path}")
        contract_path = root / record.get("contract", "")
        if contract_path.exists():
            contract = json.loads(contract_path.read_text(encoding="utf-8"))
            perms = contract.get("permissions", {})
            if contract.get("runtime_mode") != "paper_only":
                errors.append(f"{phase_id} contract not paper_only")
            for perm in ["real_execution_allowed", "private_key_access_allowed", "signing_allowed", "broadcast_allowed", "network_swap_allowed"]:
                if perms.get(perm) is not False:
                    errors.append(f"{phase_id} {perm} not false")
    return errors


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    for cmd in ["generate", "validate", "generate-and-validate"]:
        p = sub.add_parser(cmd)
        p.add_argument("--root", default="/root/sikk-gmgn")
    args = parser.parse_args(list(argv) if argv is not None else None)
    root = Path(args.root)
    if args.command in {"generate", "generate-and-validate"}:
        manifest = generate(root)
        print(f"STANDARD_STAGE_CLOSURE_GENERATED phases={len(manifest['phases'])}")
    if args.command in {"validate", "generate-and-validate"}:
        errors = validate(root)
        if errors:
            print("STANDARD_STAGE_CLOSURE_VALIDATION_FAIL")
            for err in errors:
                print(f"- {err}")
            return 1
        print("STANDARD_STAGE_CLOSURE_VALIDATION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
