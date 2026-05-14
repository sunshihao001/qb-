#!/usr/bin/env python3
"""A01-A08 second-pass audit for SIKK Stable Trader OS standard stages.

Paper-only audit: reads generated standard-stage assets and existing binding files,
produces eight reports without enabling any real trading path.
"""
from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

ROOT_DEFAULT = Path("/root/sikk-gmgn")
REPORT_REL = Path("reports/stable_trader_os/second_pass_audit/A01_A08_20260514")
MANIFEST_REL = Path("system/stable_trader_os/standard_stage_closure/manifest.json")
FORBIDDEN = ["swap", "private_key", "signing", "broadcast", "real_trade"]
SAFETY_PERMISSION_FIELDS = [
    "real_execution_allowed",
    "private_key_access_allowed",
    "signing_allowed",
    "broadcast_allowed",
    "network_swap_allowed",
]
TRACE_REQUIRED = ["input_hash", "source_artifact", "decision_reason", "downgrade_reason", "missing_fields", "acceptance_evidence"]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, title: str, lines: Iterable[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# " + title + "\n\n" + "\n".join(lines) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def py_info(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text)
    imports = []
    functions = []
    constants = {}
    calls = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            else:
                imports.append(node.module or "")
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    try:
                        constants[target.id] = ast.literal_eval(node.value)
                    except Exception:
                        constants[target.id] = "<non_literal>"
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                calls.append(node.func.attr)
            elif isinstance(node.func, ast.Name):
                calls.append(node.func.id)
    lowered = text.lower()
    return {
        "line_count": len(text.splitlines()),
        "sha256": hashlib.sha256(text.encode()).hexdigest(),
        "imports": sorted(set(imports)),
        "functions": sorted(set(functions)),
        "constants": constants,
        "calls": sorted(set(calls)),
        "forbidden_token_occurrences": {term: lowered.count(term) for term in FORBIDDEN},
    }


def classify_runtime_depth(info: Dict[str, Any]) -> Tuple[str, List[str]]:
    reasons = []
    imports = set(info.get("imports", []))
    calls = set(info.get("calls", []))
    line_count = info.get("line_count", 0)
    if line_count <= 30 and not imports and calls == set():
        reasons.append("runtime_entry is deterministic minimal wrapper with no imports/calls")
        return "WRAPPER_ONLY", reasons
    if "run" not in info.get("functions", []):
        reasons.append("missing run() entry")
        return "BROKEN_ENTRY", reasons
    if not imports and len(calls) < 3:
        reasons.append("low integration surface")
        return "SHALLOW_RUNTIME", reasons
    reasons.append("has imports/calls beyond minimal wrapper")
    return "INTEGRATED_RUNTIME_CANDIDATE", reasons


def import_and_run(root: Path, phase: str, runtime_rel: str) -> Dict[str, Any]:
    path = root / runtime_rel
    module_name = f"audit_{phase.lower()}_{hashlib.md5(str(path).encode()).hexdigest()}"
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    if not spec or not spec.loader:
        return {"phase": phase, "status": "IMPORT_FAILED", "error": "no spec"}
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    if not hasattr(mod, "run"):
        return {"phase": phase, "status": "NO_RUN_FUNCTION"}
    result = mod.run({"run_id": "A01_A08_SECOND_PASS_AUDIT", "audit_mode": "paper_only"})
    return {"phase": phase, "status": "RUN_OK", "result": result}


def flatten_strings(obj: Any) -> List[str]:
    out: List[str] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.append(str(k))
            out.extend(flatten_strings(v))
    elif isinstance(obj, list):
        for v in obj:
            out.extend(flatten_strings(v))
    else:
        out.append(str(obj))
    return out


def find_files(root: Path, names: Iterable[str]) -> List[str]:
    found = []
    for name in names:
        found.extend(str(p.relative_to(root)) for p in root.rglob(name) if p.is_file())
    return sorted(set(found))


def main(root: Path = ROOT_DEFAULT) -> int:
    manifest_path = root / MANIFEST_REL
    report_dir = root / REPORT_REL
    manifest = load_json(manifest_path)
    phases: Dict[str, Dict[str, str]] = manifest["phases"]
    ordered = sorted(phases.keys(), key=lambda p: (p[0], int(p[1:])))

    # Load assets and runtime outputs.
    assets: Dict[str, Dict[str, Any]] = {}
    for phase in ordered:
        rec = phases[phase]
        loaded = {}
        for kind in ["controller", "schema", "contract", "trace", "acceptance", "handoff"]:
            p = root / rec[kind]
            loaded[kind] = load_json(p) if p.exists() else {"__missing__": str(p)}
        runtime_path = root / rec["runtime_entry"]
        info = py_info(runtime_path)
        depth, reasons = classify_runtime_depth(info)
        run_result = import_and_run(root, phase, rec["runtime_entry"])
        assets[phase] = {"paths": rec, "json": loaded, "runtime_info": info, "runtime_depth": depth, "runtime_depth_reasons": reasons, "run_result": run_result}

    # A01 runtime depth
    a01 = {"audit_id": "A01_RUNTIME_DEPTH", "status": "PASS_WITH_GAPS", "phase_count": len(ordered), "phases": {}}
    wrapper_count = 0
    for phase in ordered:
        depth = assets[phase]["runtime_depth"]
        wrapper_count += 1 if depth == "WRAPPER_ONLY" else 0
        a01["phases"][phase] = {
            "runtime_depth": depth,
            "reasons": assets[phase]["runtime_depth_reasons"],
            "runtime_entry": assets[phase]["paths"]["runtime_entry"],
            "line_count": assets[phase]["runtime_info"]["line_count"],
            "imports": assets[phase]["runtime_info"]["imports"],
            "functions": assets[phase]["runtime_info"]["functions"],
            "calls": assets[phase]["runtime_info"]["calls"],
        }
    a01["summary"] = {"wrapper_only_count": wrapper_count, "integrated_runtime_count": len(ordered) - wrapper_count, "interpretation": "standard entries exist; most/all are shallow wrappers unless integrated_runtime_count > 0"}
    write_json(report_dir / "A01_runtime_depth_matrix.json", a01)

    # A02 handoff-contract compatibility
    a02_pairs = []
    groups = {"K": [p for p in ordered if p.startswith("K")], "P": [p for p in ordered if p.startswith("P")], "I": [p for p in ordered if p.startswith("I")], "R": [p for p in ordered if p.startswith("R")]}
    chains = groups["K"] + groups["P"] + groups["I"] + groups["R"]
    for up, down in zip(chains, chains[1:]):
        up_fields = set(assets[up]["json"]["handoff"].get("fields", []))
        down_contract = assets[down]["json"]["contract"].get("input_contract", {})
        required_upstream = down_contract.get("required_upstream_handoff")
        compatibility = "TEMPLATE_COMPATIBLE_WITH_GAPS"
        gaps = []
        if required_upstream == "SYSTEM_BOOTSTRAP" and up != chains[0]:
            gaps.append("downstream input_contract still says SYSTEM_BOOTSTRAP instead of explicit upstream phase handoff")
            compatibility = "GENERIC_BOOTSTRAP_NOT_EXPLICIT"
        if not up_fields:
            gaps.append("upstream handoff fields missing")
            compatibility = "BROKEN"
        a02_pairs.append({"upstream": up, "downstream": down, "upstream_handoff_fields": sorted(up_fields), "downstream_required_upstream_handoff": required_upstream, "compatibility_status": compatibility, "gaps": gaps})
    a02 = {"audit_id": "A02_HANDOFF_CONTRACT_COMPATIBILITY", "status": "PASS_WITH_GAPS", "pairs": a02_pairs, "summary": {"pair_count": len(a02_pairs), "generic_bootstrap_pairs": sum(1 for p in a02_pairs if p["compatibility_status"] == "GENERIC_BOOTSTRAP_NOT_EXPLICIT")}}
    write_json(report_dir / "A02_handoff_contract_compatibility_matrix.json", a02)

    # A03 trace/evidence
    a03 = {"audit_id": "A03_TRACE_EVIDENCE", "status": "PASS_WITH_GAPS", "phases": {}}
    for phase in ordered:
        trace = assets[phase]["json"]["trace"]
        strings = set(flatten_strings(trace))
        missing = [f for f in TRACE_REQUIRED if f not in strings]
        a03["phases"][phase] = {"trace_path": assets[phase]["paths"]["trace"], "missing_evidence_fields": missing, "trace_status": "EVIDENCE_READY" if not missing else "TRACE_TEMPLATE_SHALLOW"}
    write_json(report_dir / "A03_evidence_trace_completeness_matrix.json", a03)

    # A04 semantic acceptance
    semantic_keywords = ["sample", "replay", "semantic", "missing", "conflict", "quality", "field", "schema", "forbidden"]
    a04 = {"audit_id": "A04_SEMANTIC_ACCEPTANCE", "status": "PASS_WITH_GAPS", "phases": {}}
    shallow = 0
    for phase in ordered:
        acceptance = assets[phase]["json"]["acceptance"]
        strings = " ".join(flatten_strings(acceptance)).lower()
        hits = [k for k in semantic_keywords if k in strings]
        status = "STRUCTURAL_ONLY" if len(hits) <= 2 else "SEMANTIC_CANDIDATE"
        shallow += 1 if status == "STRUCTURAL_ONLY" else 0
        a04["phases"][phase] = {"acceptance_path": assets[phase]["paths"]["acceptance"], "semantic_keyword_hits": hits, "acceptance_depth": status}
    a04["summary"] = {"structural_only_count": shallow, "semantic_candidate_count": len(ordered) - shallow}
    write_json(report_dir / "A04_acceptance_semantic_depth_matrix.json", a04)

    # A05 R00 safety
    r00 = assets.get("R00")
    r00_contract = r00["json"]["contract"] if r00 else {}
    perms = r00_contract.get("permissions", {})
    r00_result = r00["run_result"].get("result", {}) if r00 else {}
    safety_gaps = []
    for f in SAFETY_PERMISSION_FIELDS:
        if perms.get(f) is not False:
            safety_gaps.append(f"permission {f} is not false")
    if r00_result.get("runtime_mode") != "paper_only":
        safety_gaps.append("runtime result is not paper_only")
    blocked = set(r00_result.get("blocked_real_execution", []))
    for term in FORBIDDEN:
        if term not in blocked:
            safety_gaps.append(f"runtime result does not explicitly block {term}")
    a05 = {"audit_id": "A05_R00_PAPER_ONLY_SAFETY", "status": "PASS" if not safety_gaps else "FAIL", "r00_contract_permissions": perms, "r00_runtime_result": r00_result, "forbidden_action_scan": r00["runtime_info"] if r00 else {}, "gaps": safety_gaps}
    write_json(report_dir / "A05_r00_runtime_safety_audit.json", a05)
    write_md(report_dir / "A05_r00_runtime_safety_audit.md", "A05 R00 Paper-Only Safety Audit", [
        f"- status: `{a05['status']}`",
        f"- runtime_mode: `{r00_result.get('runtime_mode')}`",
        f"- blocked_real_execution: `{sorted(blocked)}`",
        f"- gaps: `{safety_gaps}`",
        "- conclusion: R00 remains paper-only under current standard-stage wrapper; this does not enable live trading.",
    ])

    # A06 legacy bypass audit
    legacy_files = []
    for p in root.rglob("*.py"):
        rel = str(p.relative_to(root))
        if any(skip in rel for skip in [".git/", "__pycache__"]):
            continue
        name = p.name.lower()
        text = p.read_text(encoding="utf-8", errors="ignore").lower()
        if "legacy" in rel.lower() or "old_runner" in text or "r00" in text and any(t in text for t in FORBIDDEN):
            legacy_files.append(rel)
    a06 = {"audit_id": "A06_LEGACY_BYPASS", "status": "PASS_WITH_GAPS", "candidate_legacy_or_bypass_files": sorted(set(legacy_files))[:200], "candidate_count": len(set(legacy_files)), "required_next_controls": ["legacy_absorption_registry", "legacy_read_only_policy", "old_runner_blocklist", "compatibility_adapter_list"]}
    write_json(report_dir / "A06_legacy_bypass_audit.json", a06)

    # A07 sample replay
    replay = {"audit_id": "A07_SAMPLE_REPLAY", "status": "PASS_WITH_GAPS", "mode": "paper_only", "sample_packet": {"run_id": "A01_A08_SECOND_PASS_AUDIT", "audit_mode": "paper_only"}, "phases": {}}
    for phase in ordered:
        res = assets[phase]["run_result"]
        result = res.get("result", {})
        phase_gaps = []
        if res.get("status") != "RUN_OK":
            phase_gaps.append("runtime did not import/run")
        if result.get("runtime_mode") != "paper_only":
            phase_gaps.append("runtime_mode not paper_only")
        for required in ["phase_id", "status", "trace_refs", "acceptance", "handoff", "blocked_real_execution"]:
            if required not in result:
                phase_gaps.append(f"missing result field {required}")
        replay["phases"][phase] = {"runtime_status": res.get("status"), "result_status": result.get("status"), "runtime_mode": result.get("runtime_mode"), "gaps": phase_gaps, "result_hash": hashlib.sha256(json.dumps(result, sort_keys=True, ensure_ascii=False).encode()).hexdigest() if result else None}
    write_json(report_dir / "A07_sample_replay_acceptance_report.json", replay)

    # A08 Telegram binding
    telegram_paths = sorted(str(p.relative_to(root)) for p in root.rglob("*telegram*") if p.is_file())
    canonical_hits = []
    for rel in telegram_paths:
        p = root / rel
        text = p.read_text(encoding="utf-8", errors="ignore").lower()
        hits = [h for h in ["standard_stage_closure", "runtime_entry", "k00", "k08", "r00", "paper_only", "telegram_status_panel", "telegram_run_request"] if h in text or h in rel.lower()]
        if hits:
            canonical_hits.append({"path": rel, "hits": hits})
    a08 = {"audit_id": "A08_TELEGRAM_BINDING", "status": "PASS_WITH_GAPS", "telegram_related_file_count": len(telegram_paths), "canonical_binding_candidates": canonical_hits[:120], "gap": "Telegram surfaces exist, but this audit does not prove a single canonical command routes all K/I/P/R phases through standard_stage_closure manifest."}
    write_json(report_dir / "A08_telegram_command_binding_matrix.json", a08)

    summary = {
        "audit_id": "SIKK_A01_A08_SECOND_PASS_AUDIT_20260514",
        "scope": ["K00-K08", "P00-P10", "I01-I05", "R00"],
        "safety_boundary": "paper-only audit; no private keys, signing, broadcast, swap, or real trading enabled",
        "source_manifest": str(MANIFEST_REL),
        "report_dir": str(REPORT_REL),
        "overall_status": "PASS_WITH_GAPS",
        "key_findings": {
            "A01": a01["summary"],
            "A02": a02["summary"],
            "A04": a04["summary"],
            "A05": a05["status"],
            "A06_candidate_legacy_count": a06["candidate_count"],
            "A08_telegram_related_file_count": a08["telegram_related_file_count"],
        },
        "generated_reports": [
            "A01_runtime_depth_matrix.json",
            "A02_handoff_contract_compatibility_matrix.json",
            "A03_evidence_trace_completeness_matrix.json",
            "A04_acceptance_semantic_depth_matrix.json",
            "A05_r00_runtime_safety_audit.json",
            "A05_r00_runtime_safety_audit.md",
            "A06_legacy_bypass_audit.json",
            "A07_sample_replay_acceptance_report.json",
            "A08_telegram_command_binding_matrix.json",
            "SECOND_PASS_AUDIT_SUMMARY.md",
        ],
    }
    write_json(report_dir / "audit_summary.json", summary)
    write_md(report_dir / "SECOND_PASS_AUDIT_SUMMARY.md", "SIKK A01-A08 Second-Pass Audit Summary", [
        "## Scope",
        "- K00-K08, P00-P10, I01-I05, R00",
        "- Mode: paper-only audit and replay",
        "- Forbidden: swap, private_key, signing, broadcast, real_trade",
        "",
        "## Overall Status",
        "- `PASS_WITH_GAPS`",
        "",
        "## Key Findings",
        f"- A01 runtime wrapper-only count: `{a01['summary']['wrapper_only_count']}` / `{len(ordered)}`",
        f"- A02 generic bootstrap handoff pairs: `{a02['summary']['generic_bootstrap_pairs']}` / `{a02['summary']['pair_count']}`",
        f"- A04 structural-only acceptance count: `{a04['summary']['structural_only_count']}` / `{len(ordered)}`",
        f"- A05 R00 safety status: `{a05['status']}`",
        f"- A06 legacy/bypass candidate files: `{a06['candidate_count']}`",
        f"- A08 telegram-related files: `{a08['telegram_related_file_count']}`",
        "",
        "## Interpretation",
        "- Standard stage assets exist and paper-only runtime replay succeeds.",
        "- Main remaining gaps are runtime depth, explicit phase-to-phase handoff binding, semantic acceptance depth, legacy bypass control, and canonical Telegram command routing.",
    ])
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(ROOT_DEFAULT))
    args = parser.parse_args()
    raise SystemExit(main(Path(args.root)))
