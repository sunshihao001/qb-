"""Control-plane Orchestrator Skeleton Gate for SIKK.

This module connects Run Isolation and Skill Registry into a minimal invocation
gate. It is deliberately pre-runtime: it builds and validates invocation
envelopes, writes gate results, and never calls GMGN, computes features,
generates structure signals, creates decision tickets, or runs replay/backtest/
paper-only workflows.
"""
from __future__ import annotations

from pathlib import Path
import json
from typing import Any, Dict, Iterable, List, Optional

from .run_isolation import RunContext, append_audit, utc_now
from .skill_registry import SkillRegistry

GATE_STATUSES = ["PASS", "PATCH_REQUIRED", "BLOCKED"]
HARD_FORBIDDEN_TOKENS = [
    "live",
    "swap",
    "private_key",
    "signing",
    "broadcast",
    "wallet_signing",
    "transaction_broadcast",
    "paper_ready",
]
PRE_RUNTIME_FORBIDDEN_ACTIONS = [
    "gmgn_runtime_call",
    "feature_generation",
    "structure_signal_generation",
    "decision_ticket_generation",
    "replay_backtest_paper_only",
    "paper_backtest_live",
]
REQUIRED_ENVELOPE_FIELDS = [
    "run_id",
    "skill_id",
    "expected_backbone_node",
    "allowed_scope",
    "forbidden_scope",
    "input_artifacts",
    "output_artifacts",
    "downstream_consumers",
    "invocation_context",
]
STORAGE_CONTRACT_FILES = {
    "classification": "ARTIFACT_CLASSIFICATION_MATRIX.json",
    "run_directory": "RUN_DIRECTORY_CONTRACT.json",
    "promotion": "CANONICAL_PROMOTION_POLICY.json",
    "index": "ARTIFACT_INDEX_POLICY.json",
    "contamination": "CONTAMINATION_PREVENTION_RULES.json",
}
DEFAULT_STORAGE_CONTRACT_DIR = (
    Path(__file__).resolve().parents[1]
    / "docs/operating_backbone/storage_topology_v0_1"
)


def _as_list(value: Optional[Iterable[str]]) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    return list(value)


def _contains_any(values: Iterable[Any], tokens: Iterable[str]) -> List[str]:
    text = " ".join(str(v).lower() for v in values)
    return [token for token in tokens if token.lower() in text]


def build_invocation_envelope(
    *,
    run_id: str,
    skill_id: str,
    expected_backbone_node: str,
    allowed_scope: Optional[Iterable[str]] = None,
    forbidden_scope: Optional[Iterable[str]] = None,
    input_artifacts: Optional[Iterable[str]] = None,
    output_artifacts: Optional[Iterable[str]] = None,
    downstream_consumers: Optional[Iterable[str]] = None,
    invocation_context: str = "preflight_gate",
    artifact_class: Optional[str] = None,
    target_paths: Optional[Iterable[str]] = None,
    read_paths: Optional[Iterable[str]] = None,
    promotion_requested: bool = False,
    canonical_write_requested: bool = False,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Build a machine-checkable invocation envelope.

    The envelope is evidence for a gate decision. It is not permission to execute
    the target skill.
    """
    return {
        "artifact_type": "sikk_invocation_envelope",
        "version": "0.1",
        "created_at_utc": utc_now(),
        "run_id": run_id,
        "skill_id": skill_id,
        "expected_backbone_node": expected_backbone_node,
        "allowed_scope": _as_list(allowed_scope),
        "forbidden_scope": _as_list(forbidden_scope),
        "input_artifacts": _as_list(input_artifacts),
        "output_artifacts": _as_list(output_artifacts),
        "downstream_consumers": _as_list(downstream_consumers),
        "invocation_context": invocation_context,
        "artifact_class": artifact_class,
        "target_paths": _as_list(target_paths),
        "read_paths": _as_list(read_paths),
        "promotion_requested": promotion_requested,
        "canonical_write_requested": canonical_write_requested,
        "metadata": metadata or {},
        "execution_requested": False,
        "runtime_action_allowed": False,
    }


def validate_invocation_envelope(envelope: Dict[str, Any]) -> Dict[str, Any]:
    missing = [field for field in REQUIRED_ENVELOPE_FIELDS if field not in envelope]
    empty_required = [
        field
        for field in ["input_artifacts", "output_artifacts", "downstream_consumers"]
        if field in envelope and not envelope.get(field)
    ]
    scope_values = []
    # Hard forbidden tokens are blocking only when they appear in requested/allowed
    # behavior or artifacts. Listing them inside forbidden_scope is expected and
    # should not block the gate.
    for key in ["allowed_scope", "input_artifacts", "output_artifacts", "downstream_consumers", "invocation_context"]:
        value = envelope.get(key, [])
        scope_values.extend(value if isinstance(value, list) else [value])
    hard_forbidden_hits = _contains_any(scope_values, HARD_FORBIDDEN_TOKENS)
    pre_runtime_hits = _contains_any(envelope.get("allowed_scope", []), PRE_RUNTIME_FORBIDDEN_ACTIONS)
    errors = missing + [f"empty:{field}" for field in empty_required]
    status = "PASS"
    if errors or pre_runtime_hits:
        status = "PATCH_REQUIRED"
    if hard_forbidden_hits:
        status = "BLOCKED"
    return {
        "status": status,
        "missing_fields": missing,
        "empty_required_fields": empty_required,
        "hard_forbidden_hits": hard_forbidden_hits,
        "pre_runtime_forbidden_allowed_scope_hits": pre_runtime_hits,
        "errors": errors,
    }


def load_storage_policy_contracts(contract_dir: Path | str = DEFAULT_STORAGE_CONTRACT_DIR) -> Dict[str, Any]:
    """Load Storage Topology Contract v0.1 files for gate evaluation."""
    root = Path(contract_dir)
    contracts: Dict[str, Any] = {"contract_dir": str(root), "missing": []}
    for key, filename in STORAGE_CONTRACT_FILES.items():
        path = root / filename
        if not path.exists():
            contracts["missing"].append(filename)
            contracts[key] = None
            continue
        contracts[key] = json.loads(path.read_text(encoding="utf-8"))
    return contracts


def _artifact_class_map(storage_contracts: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    classification = storage_contracts.get("classification") or {}
    return {item.get("class"): item for item in classification.get("artifact_classes", [])}


def _path_allowed(path: str, allowed_subpaths: Iterable[str]) -> bool:
    normalized = path.replace("\\", "/")
    # Paths may be run-relative (e.g. evidence/raw/x.json) or absolute under a run.
    return any(sub in normalized or normalized.startswith(sub) for sub in allowed_subpaths)


def evaluate_storage_policy_gate(envelope: Dict[str, Any], storage_contracts: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate artifact class, storage path, consumer, promotion, and read policy.

    This is a pre-runtime policy check only. It never reads artifact payloads and
    never promotes artifacts.
    """
    missing_contracts = list(storage_contracts.get("missing", []))
    patch_reasons: List[str] = []
    block_reasons: List[str] = []
    warnings: List[str] = []
    if missing_contracts:
        patch_reasons.append("storage_policy_contract_files_missing")

    artifact_class = envelope.get("artifact_class")
    target_paths = _as_list(envelope.get("target_paths", []))
    read_paths = _as_list(envelope.get("read_paths", []))
    downstream_consumers = _as_list(envelope.get("downstream_consumers", []))
    output_artifacts = _as_list(envelope.get("output_artifacts", []))
    allowed_scope = _as_list(envelope.get("allowed_scope", []))

    classes = _artifact_class_map(storage_contracts)
    class_record = classes.get(artifact_class) if artifact_class else None
    if not artifact_class:
        patch_reasons.append("artifact_class_missing")
    elif class_record is None:
        block_reasons.append("artifact_class_not_registered")

    if class_record:
        allowed_subpaths = class_record.get("allowed_run_subpaths", [])
        allowed_consumers = class_record.get("allowed_consumers", [])
        forbidden_outputs = class_record.get("forbidden_outputs", [])
        if not target_paths:
            patch_reasons.append("target_paths_missing")
        else:
            bad_paths = [path for path in target_paths if not _path_allowed(path, allowed_subpaths)]
            if bad_paths:
                block_reasons.append("target_path_not_allowed_for_artifact_class")
        bad_consumers = [c for c in downstream_consumers if c not in allowed_consumers]
        if bad_consumers:
            block_reasons.append("downstream_consumer_not_allowed_for_artifact_class")
        forbidden_output_hits = _contains_any(output_artifacts + allowed_scope, forbidden_outputs)
        if forbidden_output_hits:
            block_reasons.append("forbidden_output_for_artifact_class")
    else:
        bad_paths = []
        bad_consumers = []
        forbidden_output_hits = []

    if envelope.get("promotion_requested") or envelope.get("canonical_write_requested"):
        # Promotion/canonical write is never allowed from ordinary invocation gate.
        block_reasons.append("promotion_or_canonical_write_requested_without_promotion_gate")

    forbidden_read_patterns = []
    index_policy = storage_contracts.get("index") or {}
    if read_paths:
        for path in read_paths:
            normalized = path.replace("\\", "/")
            if "runs/*" in normalized or "/runs/*" in normalized or "**" in normalized:
                forbidden_read_patterns.append(path)
            if "latest" in normalized.lower() and "latest_approved_pointers" not in normalized:
                forbidden_read_patterns.append(path)
            if "blocked" in normalized.lower() or "PATCH_REQUIRED" in normalized:
                forbidden_read_patterns.append(path)
    if forbidden_read_patterns:
        block_reasons.append("forbidden_read_pattern_detected")
    if not read_paths and artifact_class not in (None, "control_plane", "raw_evidence"):
        warnings.append("read_paths_not_declared_for_non_source_artifact")

    status = "PASS"
    if patch_reasons:
        status = "PATCH_REQUIRED"
    if block_reasons:
        status = "BLOCKED"
    return {
        "status": status,
        "artifact_class": artifact_class,
        "class_registered": class_record is not None,
        "missing_contracts": missing_contracts,
        "bad_target_paths": bad_paths,
        "bad_consumers": bad_consumers,
        "forbidden_output_hits": forbidden_output_hits,
        "forbidden_read_patterns": sorted(set(forbidden_read_patterns)),
        "patch_reasons": patch_reasons,
        "block_reasons": block_reasons,
        "warnings": warnings,
        "read_policy_ref": index_policy.get("artifact_id"),
    }


def evaluate_orchestrator_gate(
    *,
    ctx: RunContext,
    registry: SkillRegistry,
    envelope: Dict[str, Any],
    require_run_manifest: bool = True,
    storage_contracts: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Evaluate whether a skill invocation envelope may proceed past the gate.

    PASS means the envelope is admissible for a future controlled handoff. It does
    not invoke the skill and does not grant runtime trading authority.
    """
    envelope_check = validate_invocation_envelope(envelope)
    storage_policy_check = evaluate_storage_policy_gate(
        envelope, storage_contracts or load_storage_policy_contracts()
    )
    registry_check = registry.validate()
    invocation_check = registry.invocation_allowed(
        envelope.get("skill_id", ""),
        envelope.get("expected_backbone_node", ""),
    )
    run_missing = []
    if require_run_manifest:
        for name in ["run_manifest.yaml", "audit_log.jsonl"]:
            if not (ctx.run_dir / name).exists():
                run_missing.append(name)
    record = registry.by_id.get(envelope.get("skill_id", ""))
    registry_forbidden_scope = record.raw.get("forbidden_scope", []) if record else []
    allowed_scope = envelope.get("allowed_scope", [])
    allowed_forbidden_hits = _contains_any(allowed_scope, registry_forbidden_scope)
    hard_hits = list(envelope_check["hard_forbidden_hits"])
    hard_hits.extend(_contains_any(envelope.get("allowed_scope", []), HARD_FORBIDDEN_TOKENS))

    patch_reasons: List[str] = []
    block_reasons: List[str] = []
    if registry_check["status"] != "PASS":
        patch_reasons.append("skill_registry_invalid")
    if envelope_check["status"] == "PATCH_REQUIRED":
        patch_reasons.append("invocation_envelope_incomplete_or_pre_runtime_scope_violation")
    if run_missing:
        patch_reasons.append("run_isolation_artifacts_missing")
    if allowed_forbidden_hits:
        patch_reasons.append("allowed_scope_conflicts_with_skill_forbidden_scope")
    if storage_policy_check["status"] == "PATCH_REQUIRED":
        patch_reasons.append("storage_policy_patch_required")
    if storage_policy_check["status"] == "BLOCKED":
        block_reasons.append("storage_policy_blocked")
    if not invocation_check.get("allowed"):
        block_reasons.append(invocation_check.get("reason", "invocation_not_allowed"))
    if hard_hits:
        block_reasons.append("hard_forbidden_scope_detected")

    status = "PASS"
    if patch_reasons:
        status = "PATCH_REQUIRED"
    if block_reasons:
        status = "BLOCKED"

    result = {
        "artifact_type": "sikk_orchestrator_gate_result",
        "version": "0.1",
        "created_at_utc": utc_now(),
        "run_id": ctx.run_id,
        "skill_id": envelope.get("skill_id"),
        "expected_backbone_node": envelope.get("expected_backbone_node"),
        "status": status,
        "reason": "; ".join(block_reasons or patch_reasons or ["registered_and_control_scope_valid"]),
        "registry_check": registry_check,
        "invocation_check": invocation_check,
        "envelope_check": envelope_check,
        "storage_policy_check": storage_policy_check,
        "run_missing": run_missing,
        "allowed_forbidden_hits": allowed_forbidden_hits,
        "hard_forbidden_hits": sorted(set(hard_hits)),
        "patch_reasons": patch_reasons,
        "block_reasons": block_reasons,
        "runtime_action_executed": False,
        "gmgn_called": False,
        "feature_generated": False,
        "structure_signal_generated": False,
        "decision_ticket_generated": False,
        "paper_validation_executed": False,
        "canonical_promoted": False,
        "storage_policy_enforced": True,
        "next_allowed_action": "write_handoff_or_patch_missing_contracts" if status == "PASS" else "repair_or_block_before_invocation",
    }
    append_audit(ctx, "orchestrator_gate_evaluated", {"skill_id": result["skill_id"], "status": status})
    return result


def write_gate_artifacts(ctx: RunContext, envelope: Dict[str, Any], gate_result: Dict[str, Any], subdir: str = "control_layer") -> Dict[str, str]:
    out_dir = ctx.run_dir / subdir
    out_dir.mkdir(parents=True, exist_ok=True)
    envelope_path = out_dir / "invocation_envelope.json"
    gate_path = out_dir / "orchestrator_gate_result.json"
    envelope_path.write_text(json.dumps(envelope, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    gate_path.write_text(json.dumps(gate_result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    append_audit(ctx, "orchestrator_gate_artifacts_written", {"paths": [str(envelope_path), str(gate_path)]})
    return {"invocation_envelope": str(envelope_path), "orchestrator_gate_result": str(gate_path)}

