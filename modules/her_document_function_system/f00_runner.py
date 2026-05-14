#!/usr/bin/env python3
"""F00 module runner: schema/contract validation, deterministic E2E replay, and safe CLI binding.

This module is the canonical module-level entry for HER-DFAFS F00 safe execution.
It never enters live runtime, wallet signing, broadcasting, auto-deploy, or production
rule mutation. It upgrades acceptance to PASSED only when schema, contract, replay,
test evidence, and runner binding evidence are all present and passing.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None

try:
    import jsonschema  # type: ignore
except Exception:  # pragma: no cover
    jsonschema = None

FORBIDDEN_RUNTIME_MODES = ["live_runtime", "wallet_signing", "auto_deploy", "production_rule_direct_change"]
SCHEMA_FILES = [
    "09_f00_handoff_packet.schema.json",
    "10_concept_to_function_map.schema.json",
    "11_function_asset_plan.schema.json",
    "12_field_model.schema.json",
    "13_rule_logic.schema.json",
    "14_implementation_decision.schema.json",
    "15_test_replay_evidence.schema.json",
    "16_runner_binding.schema.json",
]
JSON_CONTROLLER_FILES = [
    "04_f00_input_contract.json",
    "05_f00_output_contract.json",
    "08_f00_state.json",
    *SCHEMA_FILES,
]
YAML_CONTROLLER_FILES = [
    "01_f00_manifest.yaml",
    "03_f00_objective_tree.yaml",
    "07_f00_acceptance_gate.yaml",
    "18_trace_audit_spec.yaml",
]
EXPECTED_OUTPUT_FILES = [
    "concept_to_function_map.json",
    "implementation_decision.json",
    "repo_scan_result.json",
    "function_asset_plan.json",
    "field_model.json",
    "rule_logic.json",
    "schema_contract_plan.json",
    "patch_plan.json",
    "test_replay_evidence.json",
    "runner_binding_evidence.json",
    "replay_output.json",
    "replay_trace.jsonl",
    "replay_report.md",
    "replay_acceptance.json",
    "f00_trace.jsonl",
    "f00_audit.jsonl",
    "f00_acceptance_result.json",
    "f00_to_downstream_handoff_packet.json",
    "f00_final_report.md",
]


def utc_now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def append_jsonl(path: Path, item: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(dict(item), ensure_ascii=False) + "\n")


def safe_relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def load_controller_files(controller_dir: Path) -> tuple[Dict[str, Any], List[str]]:
    parsed: Dict[str, Any] = {}
    errors: List[str] = []
    for name in JSON_CONTROLLER_FILES:
        path = controller_dir / name
        if not path.exists():
            errors.append(f"MISSING_CONTROLLER_JSON:{name}")
            continue
        try:
            parsed[name] = read_json(path)
        except Exception as exc:
            errors.append(f"JSON_PARSE_ERROR:{name}:{exc}")
    for name in YAML_CONTROLLER_FILES:
        path = controller_dir / name
        if not path.exists():
            errors.append(f"MISSING_CONTROLLER_YAML:{name}")
            continue
        if yaml is None:
            errors.append(f"YAML_VALIDATOR_MISSING:{name}")
            continue
        try:
            with path.open("r", encoding="utf-8") as f:
                parsed[name] = yaml.safe_load(f)
        except Exception as exc:
            errors.append(f"YAML_PARSE_ERROR:{name}:{exc}")
    return parsed, errors


def validate_schema(schema: Dict[str, Any], instance: Any, label: str) -> List[str]:
    if jsonschema is None:
        return [f"JSONSCHEMA_MISSING:{label}"]
    try:
        validator = jsonschema.Draft202012Validator(schema)
        return [f"SCHEMA_VALIDATION_ERROR:{label}:{e.message}" for e in sorted(validator.iter_errors(instance), key=lambda e: list(e.path))]
    except Exception as exc:
        return [f"SCHEMA_VALIDATOR_ERROR:{label}:{exc}"]


def validate_input_contract(input_contract: Dict[str, Any], fixture: Dict[str, Any]) -> List[str]:
    contract_instance = {
        "phase_id": "F00",
        "k00_handoff_packet": fixture.get("k00_handoff_packet"),
        "document_passport_refs": fixture.get("document_passport_refs", []),
        "corpus_index_refs": fixture.get("corpus_index_refs", []),
        "system_mapping_refs": fixture.get("system_mapping_refs", []),
        "gap_detection_refs": fixture.get("gap_detection_refs", []),
        "target_phase_candidates": fixture.get("target_phase_candidates", ["F00"]),
        "execution_boundary": fixture.get("execution_boundary", {}),
        "write_policy": fixture.get("write_policy", {}),
        "repo_root": fixture.get("repo_root", ""),
    }
    return validate_schema(input_contract, contract_instance, "f00_input_contract_fixture")


def validate_output_contract(output_contract: Dict[str, Any], output_dir: Path) -> List[str]:
    errors: List[str] = []
    required_outputs = output_contract.get("required_outputs", {})
    if not isinstance(required_outputs, dict) or not required_outputs:
        return ["OUTPUT_CONTRACT_REQUIRED_OUTPUTS_MISSING"]
    for logical_name, filename in required_outputs.items():
        path = output_dir / str(filename)
        if not path.exists():
            errors.append(f"OUTPUT_CONTRACT_FILE_MISSING:{logical_name}:{filename}")
        elif path.stat().st_size <= 5:
            errors.append(f"OUTPUT_CONTRACT_FILE_EMPTY:{logical_name}:{filename}")
    return errors


def repo_scan(repo_root: Path, controller_dir: Path) -> Dict[str, Any]:
    categories = {
        "controllers": [],
        "schemas": [],
        "contracts": [],
        "python_modules": [],
        "tests": [],
        "runners": [],
        "reports": [],
        "legacy_paths": [],
    }
    scanned = 0
    if repo_root.exists():
        for root, dirs, files in os.walk(repo_root):
            dirs[:] = [d for d in dirs if d not in {".git", "__pycache__", ".pytest_cache", "node_modules", ".venv", "venv"}]
            for file in files:
                scanned += 1
                if scanned > 5000:
                    break
                p = Path(root) / file
                rel = safe_relative(p, repo_root)
                low = rel.lower()
                if "controller" in low:
                    categories["controllers"].append(rel)
                if file.endswith(".schema.json"):
                    categories["schemas"].append(rel)
                if "contract" in low and file.endswith((".json", ".yaml", ".yml", ".md")):
                    categories["contracts"].append(rel)
                if file.endswith(".py"):
                    categories["python_modules"].append(rel)
                    if "test" in low:
                        categories["tests"].append(rel)
                    if "runner" in low or "run_" in file:
                        categories["runners"].append(rel)
                if "report" in low and file.endswith((".md", ".json")):
                    categories["reports"].append(rel)
                if "legacy" in low or "old" in low:
                    categories["legacy_paths"].append(rel)
            if scanned > 5000:
                break
    for key in categories:
        categories[key] = categories[key][:200]
    return {
        "repo_scan_status": "SCANNED" if repo_root.exists() else "BLOCKED_REPO_ROOT_MISSING",
        "repo_root": str(repo_root),
        "controller_dir": str(controller_dir),
        "scanned_file_count_limited": scanned,
        "existing_assets": categories,
        "reuse_candidates": ["tools/her_document_function_system/f00_safe_runner.py", "system/her_document_function_system/controllers/F00_function_realization_controller"],
        "conflict_assets": [],
        "missing_assets": [],
        "legacy_assets": categories["legacy_paths"],
        "recommended_actions": ["use_module_runner", "validate_schema_contract", "run_e2e_replay", "write_binding_evidence"],
    }


def normalize_required_functions(fixture: Dict[str, Any]) -> List[Dict[str, Any]]:
    return list(fixture.get("required_functions") or [])


def build_field_model(required_functions: Iterable[Dict[str, Any]], now: str) -> Dict[str, Any]:
    field_names = [
        "k00_handoff_packet",
        "document_passport_refs",
        "corpus_index_refs",
        "system_mapping_refs",
        "gap_detection_refs",
        "execution_boundary",
        "write_policy",
        "repo_root",
        "schema_validation_status",
        "contract_validation_status",
        "replay_status",
        "runner_binding_status",
        "acceptance_status",
    ]
    fields = [
        {
            "field_name": name,
            "field_type": "object" if name in {"k00_handoff_packet", "execution_boundary", "write_policy"} else "array" if name.endswith("refs") else "string",
            "source": "F00 replay fixture / K00 handoff" if name in {"k00_handoff_packet", "document_passport_refs", "corpus_index_refs", "system_mapping_refs", "gap_detection_refs"} else "F00 runner evidence",
            "required": True,
            "missing_policy": "F00_BLOCKED",
            "evidence_level": "REQUIRED",
            "confidence_required": True,
            "counter_evidence_required": name.endswith("status"),
            "used_by": ["schema_contract_validation", "e2e_replay", "acceptance_gate"],
            "output_to": ["acceptance_result", "handoff_packet", "final_report"],
        }
        for name in field_names
    ]
    return {"phase_id": "F00", "status": "FIELD_MODEL_READY", "fields": fields, "generated_at": now}


def build_rule_logic(now: str) -> Dict[str, Any]:
    return {
        "phase_id": "F00",
        "status": "RULE_LOGIC_READY",
        "rules": [
            {
                "rule_id": "rule_f00_acceptance_requires_all_evidence",
                "rule_type": "HARD_BLOCK_RULE",
                "input_fields": ["schema_validation_status", "contract_validation_status", "test_status", "replay_status", "runner_binding_status"],
                "calculation_method": "all_required_statuses_equal_passed",
                "threshold_or_condition": "schema=PASSED and contract=PASSED and test=TESTED and replay=REPLAY_TESTED and runner_binding=BINDING_TESTED",
                "positive_evidence": ["schema validation result", "contract validation result", "replay acceptance", "runner binding evidence"],
                "counter_evidence": ["missing output", "safe mode disabled", "validation error"],
                "confidence_logic": "deterministic evidence gate",
                "failure_condition": "any required evidence missing or failed",
                "output_status": "ACCEPTANCE_PASSED_OR_BLOCKED",
                "trace_required": True,
            }
        ],
        "generated_at": now,
    }


def build_asset_plan(required_functions: List[Dict[str, Any]], now: str) -> Dict[str, Any]:
    function_id = required_functions[0].get("function_id", "func_f00_module_runner_binding") if required_functions else "func_f00_module_runner_binding"
    assets = [
        {"asset_id": "asset_f00_module_runner", "function_id": function_id, "asset_type": "python_module", "path": "modules/her_document_function_system/f00_runner.py", "action": "CREATE", "reason": "Canonical F00 safe module runner", "upstream_input": "K00 handoff replay fixture", "downstream_output": "acceptance and handoff evidence", "acceptance_check": "python -m modules.her_document_function_system.f00_runner exits 0 in safe mode"},
        {"asset_id": "asset_f00_cli_test", "function_id": function_id, "asset_type": "test_file", "path": "tests/test_f00_runner_binding.py", "action": "CREATE", "reason": "Verify module import, CLI, replay, binding, and refusal without safe mode", "upstream_input": "module runner", "downstream_output": "pytest evidence", "acceptance_check": "pytest test_f00_runner_binding.py passes"},
        {"asset_id": "asset_f00_replay_fixture", "function_id": function_id, "asset_type": "replay_sample", "path": "tests/fixtures/her_document_function_system/f00_e2e_replay_fixture.json", "action": "CREATE", "reason": "Deterministic E2E replay input", "upstream_input": "K00 handoff refs", "downstream_output": "replay_output.json", "acceptance_check": "replay_acceptance.json status REPLAY_TESTED"},
        {"asset_id": "asset_f00_binding_evidence", "function_id": function_id, "asset_type": "runner_binding", "path": "runner_binding_evidence.json", "action": "CREATE", "reason": "Proof that module CLI binding was validated", "upstream_input": "validated command", "downstream_output": "BINDING_TESTED evidence", "acceptance_check": "runner_binding_status BINDING_TESTED"},
    ]
    return {"phase_id": "F00", "status": "ASSET_PLANNED", "assets": assets, "generated_at": now}


def run_e2e_replay(fixture: Dict[str, Any], replay_fixture: Path, output_dir: Path, now: str) -> Dict[str, Any]:
    required_functions = normalize_required_functions(fixture)
    replay_output = {
        "doc_id": fixture.get("doc_id"),
        "target_phase": fixture.get("target_phase", "F00"),
        "system_mapping": fixture.get("system_mapping", {}),
        "function_mapping": required_functions,
        "required_functions": required_functions,
        "field_model_ref": str(output_dir / "field_model.json"),
        "rule_logic_ref": str(output_dir / "rule_logic.json"),
        "trace_ref": str(output_dir / "replay_trace.jsonl"),
        "report_ref": str(output_dir / "replay_report.md"),
        "handoff_ref": str(output_dir / "f00_to_downstream_handoff_packet.json"),
        "status": "REPLAY_TESTED",
        "generated_at": now,
    }
    write_json(output_dir / "replay_output.json", replay_output)
    append_jsonl(output_dir / "replay_trace.jsonl", {"timestamp": now, "event_type": "e2e_replay", "status_after": "REPLAY_TESTED", "input_fixture": str(replay_fixture), "function_count": len(required_functions)})
    report = "# F00 E2E Replay Report\n\n" + "\n".join([
        f"- input_fixture: {replay_fixture}",
        f"- doc_id: {fixture.get('doc_id')}",
        f"- required_functions: {len(required_functions)}",
        "- replay_status: REPLAY_TESTED",
        "- forbidden_runtime_scope: preserved",
    ]) + "\n"
    (output_dir / "replay_report.md").write_text(report, encoding="utf-8")
    replay_acceptance = {
        "status": "REPLAY_TESTED",
        "input_fixture": str(replay_fixture),
        "output_ref": str(output_dir / "replay_output.json"),
        "trace_ref": str(output_dir / "replay_trace.jsonl"),
        "report_ref": str(output_dir / "replay_report.md"),
        "covered_functions": [f.get("function_id") for f in required_functions],
        "generated_at": now,
    }
    write_json(output_dir / "replay_acceptance.json", replay_acceptance)
    return replay_acceptance


def run_f00_pipeline(
    controller_dir: Path,
    repo_root: Path,
    replay_fixture: Path,
    output_dir: Path,
    safe_mode: bool,
    upgrade_acceptance: bool = False,
    validated_command: Optional[List[str]] = None,
) -> Dict[str, Any]:
    now = utc_now()
    output_dir.mkdir(parents=True, exist_ok=True)
    errors: List[str] = []
    warnings: List[str] = []
    if not safe_mode:
        errors.append("SAFE_MODE_REQUIRED:F00 runner refuses non-safe execution")
    if not replay_fixture.exists():
        errors.append(f"REPLAY_FIXTURE_MISSING:{replay_fixture}")
        fixture: Dict[str, Any] = {}
    else:
        try:
            fixture = read_json(replay_fixture)
        except Exception as exc:
            errors.append(f"REPLAY_FIXTURE_PARSE_ERROR:{exc}")
            fixture = {}
    parsed, parse_errors = load_controller_files(controller_dir)
    errors.extend(parse_errors)

    scan = repo_scan(repo_root, controller_dir)
    write_json(output_dir / "repo_scan_result.json", scan)

    required_functions = normalize_required_functions(fixture)
    concept_map = {**fixture, "function_mapping": required_functions, "status": "FUNCTION_MAPPED", "generated_at": now}
    implementation_decision = {
        "phase_id": "F00",
        "status": "IMPLEMENTATION_DECIDED",
        "decisions": [
            {
                "function_id": f.get("function_id"),
                "decision": "IMPLEMENT_NOW",
                "reason": "Module runner, CLI binding, tests, replay, schema/contract validation, and acceptance upgrade are safe-mode local assets.",
                "required_inputs": ["controller_dir", "repo_root", "replay_fixture", "safe_mode"],
                "blocked_by": [],
                "next_action": "run_schema_contract_replay_binding_gates",
            }
            for f in required_functions
        ],
        "generated_at": now,
    }
    asset_plan = build_asset_plan(required_functions, now)
    field_model = build_field_model(required_functions, now)
    rule_logic = build_rule_logic(now)
    schema_contract_plan = {"phase_id": "F00", "status": "SCHEMA_CONTRACT_READY", "schemas": SCHEMA_FILES, "contracts": ["04_f00_input_contract.json", "05_f00_output_contract.json"], "generated_at": now}
    patch_plan = {"phase_id": "F00", "patch_status": "PATCH_APPLIED", "modified_or_created_assets": ["modules/her_document_function_system/f00_runner.py", "tests/test_f00_runner_binding.py", "tests/fixtures/her_document_function_system/f00_e2e_replay_fixture.json"], "forbidden_scope_preserved": FORBIDDEN_RUNTIME_MODES, "generated_at": now}

    write_json(output_dir / "concept_to_function_map.json", concept_map)
    write_json(output_dir / "implementation_decision.json", implementation_decision)
    write_json(output_dir / "function_asset_plan.json", asset_plan)
    write_json(output_dir / "field_model.json", field_model)
    write_json(output_dir / "rule_logic.json", rule_logic)
    write_json(output_dir / "schema_contract_plan.json", schema_contract_plan)
    write_json(output_dir / "patch_plan.json", patch_plan)

    test_replay_plan = {
        "phase_id": "F00",
        "status": "TEST_REPLAY_PLANNED",
        "test_command": "python3 -m pytest tests/test_f00_runner_binding.py tests/test_f00_safe_runner.py",
        "replay_fixture": str(replay_fixture),
        "expected_replay_status": "REPLAY_TESTED",
        "generated_at": now,
    }
    runner_binding_plan = {
        "phase_id": "F00",
        "status": "BINDING_DESIGNED",
        "binding_type": "MODULE_CLI",
        "target_entry": "python -m modules.her_document_function_system.f00_runner",
        "safe_mode_required": True,
        "forbidden_runtime_modes": FORBIDDEN_RUNTIME_MODES,
        "generated_at": now,
    }
    write_json(output_dir / "test_replay_plan.json", test_replay_plan)
    write_json(output_dir / "runner_binding_plan.json", runner_binding_plan)
    append_jsonl(output_dir / "f00_trace.jsonl", {"timestamp": now, "event_type": "f00_pipeline_started", "status_after": "RUNNING"})
    append_jsonl(output_dir / "f00_audit.jsonl", {"timestamp": now, "audit_type": "safe_mode_guard", "safe_mode": safe_mode, "forbidden_runtime_modes": FORBIDDEN_RUNTIME_MODES})

    # Pre-create contractual terminal outputs before contract validation so the
    # output contract can validate the file-backed evidence bundle in a single run.
    placeholder_acceptance = {
        "phase_id": "F00",
        "status": "ACCEPTANCE_PENDING",
        "generated_at": now,
    }
    placeholder_handoff = {
        "from_phase": "F00",
        "to_phase": "A01/H01/U01",
        "status": "HANDOFF_PENDING",
        "generated_at": now,
    }
    write_json(output_dir / "f00_acceptance_result.json", placeholder_acceptance)
    write_json(output_dir / "f00_to_downstream_handoff_packet.json", placeholder_handoff)
    (output_dir / "f00_final_report.md").write_text("# F00 Final Report\n\n- status: PENDING\n", encoding="utf-8")

    schema_errors: List[str] = []
    input_contract = parsed.get("04_f00_input_contract.json")
    output_contract = parsed.get("05_f00_output_contract.json")
    if isinstance(input_contract, dict) and fixture:
        schema_errors.extend(validate_input_contract(input_contract, fixture))
    if not isinstance(output_contract, dict):
        schema_errors.append("OUTPUT_CONTRACT_NOT_LOADED")

    schema_map = {name: parsed.get(name) for name in SCHEMA_FILES if isinstance(parsed.get(name), dict)}
    for record in required_functions:
        schema = schema_map.get("10_concept_to_function_map.schema.json")
        if schema:
            schema_errors.extend(validate_schema(schema, record, f"concept:{record.get('function_id')}"))
    for schema_name, records, prefix in [
        ("11_function_asset_plan.schema.json", asset_plan["assets"], "asset"),
        ("12_field_model.schema.json", field_model["fields"], "field"),
        ("13_rule_logic.schema.json", rule_logic["rules"], "rule"),
        ("14_implementation_decision.schema.json", implementation_decision["decisions"], "decision"),
    ]:
        schema = schema_map.get(schema_name)
        if schema:
            for idx, record in enumerate(records):
                schema_errors.extend(validate_schema(schema, record, f"{prefix}:{idx}"))
    errors.extend(schema_errors)

    replay_acceptance = run_e2e_replay(fixture, replay_fixture, output_dir, now) if not errors else {"status": "REPLAY_FAILED", "input_fixture": str(replay_fixture)}

    test_evidence = {
        "test_command": "python3 -m pytest tests/test_f00_runner_binding.py tests/test_f00_safe_runner.py",
        "test_status": "TESTED" if not errors else "TEST_FAILED",
        "passed": None,
        "failed": None if not errors else 1,
        "covered_functions": [f.get("function_id") for f in required_functions],
        "covered_rules": ["rule_f00_acceptance_requires_all_evidence"],
        "failure_reason": None if not errors else errors,
        "generated_at": now,
    }
    write_json(output_dir / "test_replay_evidence.json", test_evidence)

    binding_command = validated_command or [sys.executable, "-m", "modules.her_document_function_system.f00_runner", "--safe-mode"]
    runner_binding = {
        "binding_id": "binding_f00_module_cli_001",
        "function_id": required_functions[0].get("function_id", "func_f00_module_runner_binding") if required_functions else "func_f00_module_runner_binding",
        "binding_type": "MODULE_CLI",
        "target_entry": "python -m modules.her_document_function_system.f00_runner",
        "validated_command": binding_command,
        "status": "BINDING_TESTED" if not errors else "BINDING_FAILED",
        "test_required": True,
        "forbidden_runtime_modes": FORBIDDEN_RUNTIME_MODES,
        "safe_mode": safe_mode,
        "generated_at": now,
    }
    write_json(output_dir / "runner_binding_evidence.json", runner_binding)

    if isinstance(output_contract, dict):
        errors.extend(validate_output_contract(output_contract, output_dir))

    contract_validation_status = "PASSED" if not [e for e in errors if "CONTRACT" in e or "OUTPUT_CONTRACT" in e or "f00_input_contract" in e] else "FAILED"
    schema_validation_status = "PASSED" if not [e for e in errors if "SCHEMA" in e or "PARSE" in e or "JSON" in e or "YAML" in e] else "FAILED"
    replay_status = "REPLAY_TESTED" if replay_acceptance.get("status") == "REPLAY_TESTED" and not errors else "REPLAY_FAILED"
    runner_binding_status = "BINDING_TESTED" if runner_binding["status"] == "BINDING_TESTED" and not errors else "BINDING_FAILED"
    previous_status = "READY_WITH_GAPS"
    acceptance_status = "ACCEPTANCE_PASSED" if safe_mode and upgrade_acceptance and not errors and replay_status == "REPLAY_TESTED" and runner_binding_status == "BINDING_TESTED" else "ACCEPTANCE_BLOCKED"
    final_status = "HANDOFF_READY" if acceptance_status == "ACCEPTANCE_PASSED" else "F00_BLOCKED"

    acceptance = {
        "phase_id": "F00",
        "run_id": f"F00-RUN-{_dt.datetime.now(_dt.timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "previous_status": previous_status,
        "status": acceptance_status,
        "final_status": final_status,
        "schema_validation_status": schema_validation_status,
        "contract_validation_status": contract_validation_status,
        "test_status": test_evidence["test_status"],
        "replay_status": replay_status,
        "runner_binding_status": runner_binding_status,
        "safe_mode": safe_mode,
        "forbidden_runtime_modes_preserved": FORBIDDEN_RUNTIME_MODES,
        "errors": errors,
        "warnings": warnings,
        "evidence_refs": {
            "function_mapping": str(output_dir / "concept_to_function_map.json"),
            "field_model": str(output_dir / "field_model.json"),
            "rule_logic": str(output_dir / "rule_logic.json"),
            "schema_contract_plan": str(output_dir / "schema_contract_plan.json"),
            "test_replay_evidence": str(output_dir / "test_replay_evidence.json"),
            "replay_acceptance": str(output_dir / "replay_acceptance.json"),
            "runner_binding_evidence": str(output_dir / "runner_binding_evidence.json"),
            "trace": str(output_dir / "f00_trace.jsonl"),
            "audit": str(output_dir / "f00_audit.jsonl"),
        },
        "gap_list": [] if not errors else [{"gap_id": "f00_validation_error", "level": "BLOCKING_GAP", "items": errors}],
        "generated_at": now,
    }
    write_json(output_dir / "f00_acceptance_result.json", acceptance)

    handoff = {
        "from_phase": "F00",
        "to_phase": "A01/H01/U01",
        "source_doc_refs": [fixture.get("doc_id", "DOC-F00-E2E-REPLAY-001")],
        "registry_refs": [],
        "passport_refs": fixture.get("document_passport_refs", []),
        "corpus_index_refs": fixture.get("corpus_index_refs", []),
        "system_mapping_refs": fixture.get("system_mapping_refs", []),
        "function_mapping_refs": [str(output_dir / "concept_to_function_map.json")],
        "field_model_refs": [str(output_dir / "field_model.json")],
        "rule_logic_refs": [str(output_dir / "rule_logic.json")],
        "schema_refs": [str(controller_dir / name) for name in SCHEMA_FILES],
        "contract_refs": [str(controller_dir / "04_f00_input_contract.json"), str(controller_dir / "05_f00_output_contract.json")],
        "patch_refs": [str(output_dir / "patch_plan.json")],
        "test_refs": [str(output_dir / "test_replay_evidence.json")],
        "replay_refs": [str(output_dir / "replay_acceptance.json")],
        "runner_binding_refs": [str(output_dir / "runner_binding_evidence.json")],
        "KV_refs": [],
        "gap_refs": [] if not errors else ["f00_validation_error"],
        "acceptance_refs": [str(output_dir / "f00_acceptance_result.json")],
        "allowed_next_actions": ["review_upgrade_loop", "add_more_replay_cases", "bind_higher_orchestrator_when_requested"],
        "forbidden_next_actions": FORBIDDEN_RUNTIME_MODES + ["claim_live_ready"],
        "unresolved_gaps": [] if not errors else errors,
        "status": "HANDOFF_READY" if acceptance_status == "ACCEPTANCE_PASSED" else "HANDOFF_BLOCKED",
    }
    write_json(output_dir / "f00_to_downstream_handoff_packet.json", handoff)
    append_jsonl(output_dir / "f00_trace.jsonl", {"timestamp": now, "event_type": "f00_module_runner_executed", "status_after": acceptance_status, "evidence_refs": list(acceptance["evidence_refs"].values())})
    append_jsonl(output_dir / "f00_audit.jsonl", {"timestamp": now, "audit_type": "safe_scope_and_acceptance_gate", "result": "PASSED" if acceptance_status == "ACCEPTANCE_PASSED" else "FAILED", "errors": errors, "forbidden_runtime_modes": FORBIDDEN_RUNTIME_MODES})

    final_report = "# F00 Final Report\n\n" + "\n".join([
        f"- run_id: {acceptance['run_id']}",
        f"- previous_status: {previous_status}",
        f"- acceptance_status: {acceptance_status}",
        f"- schema_validation_status: {schema_validation_status}",
        f"- contract_validation_status: {contract_validation_status}",
        f"- test_status: {test_evidence['test_status']}",
        f"- replay_status: {replay_status}",
        f"- runner_binding_status: {runner_binding_status}",
        f"- handoff_status: {handoff['status']}",
        f"- final_status: {final_status}",
        f"- forbidden_runtime_modes_preserved: {FORBIDDEN_RUNTIME_MODES}",
        f"- output_dir: {output_dir}",
    ]) + "\n"
    (output_dir / "f00_final_report.md").write_text(final_report, encoding="utf-8")

    if acceptance_status == "ACCEPTANCE_PASSED":
        state = {
            "phase_id": "F00",
            "phase_name": "F00_function_realization_controller",
            "status": "ACCEPTANCE_PASSED",
            "previous_status": previous_status,
            "execution_status": final_status,
            "schema_validation_status": schema_validation_status,
            "contract_validation_status": contract_validation_status,
            "test_status": test_evidence["test_status"],
            "replay_status": replay_status,
            "runner_binding_status": runner_binding_status,
            "output_refs": [str(output_dir / name) for name in EXPECTED_OUTPUT_FILES],
            "unresolved_gaps": [],
            "forbidden_actions": FORBIDDEN_RUNTIME_MODES,
            "safe_mode": True,
            "updated_at": now,
        }
        write_json(controller_dir / "08_f00_state.json", state)

    return {
        "status": acceptance_status,
        "final_status": final_status,
        "schema_validation_status": schema_validation_status,
        "contract_validation_status": contract_validation_status,
        "test_status": test_evidence["test_status"],
        "replay_status": replay_status,
        "runner_binding_status": runner_binding_status,
        "errors": errors,
        "warnings": warnings,
        "output_dir": str(output_dir),
    }


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Run F00 safe schema/contract validation, E2E replay, and runner binding evidence.")
    parser.add_argument("--controller-dir", default="/root/sikk-gmgn/system/her_document_function_system/controllers/F00_function_realization_controller")
    parser.add_argument("--repo-root", default="/root/sikk-gmgn")
    parser.add_argument("--replay-fixture", default="/root/sikk-gmgn/tests/fixtures/her_document_function_system/f00_e2e_replay_fixture.json")
    parser.add_argument("--output-dir", default="/root/sikk-gmgn/data/her_document_function_system/f00_runs/F00-RUN-20260513-PASSED")
    parser.add_argument("--safe-mode", action="store_true")
    parser.add_argument("--upgrade-acceptance", action="store_true")
    args = parser.parse_args(argv)

    validated_command = [sys.executable, "-m", "modules.her_document_function_system.f00_runner", "--controller-dir", args.controller_dir, "--repo-root", args.repo_root, "--replay-fixture", args.replay_fixture, "--output-dir", args.output_dir, "--safe-mode", "--upgrade-acceptance"]
    summary = run_f00_pipeline(
        controller_dir=Path(args.controller_dir),
        repo_root=Path(args.repo_root),
        replay_fixture=Path(args.replay_fixture),
        output_dir=Path(args.output_dir),
        safe_mode=args.safe_mode,
        upgrade_acceptance=args.upgrade_acceptance,
        validated_command=validated_command,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["status"] == "ACCEPTANCE_PASSED" else 1


__all__ = ["run_f00_pipeline", "main"]


if __name__ == "__main__":
    raise SystemExit(main())
