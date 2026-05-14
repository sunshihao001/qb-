from __future__ import annotations

import csv
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping

from modules.wallet_structure.decision_builder import build_bundle_from_request

PHASE_ID = "phase_02_wallet_structure_controller"
NEXT_STAGE = "phase_03_chip_control_controller"
VALID_STATUS = {
    "WALLET_SUPPORT",
    "WALLET_PAUSE",
    "WALLET_BLOCK",
    "WALLET_UNKNOWN",
    "WALLET_DATA_WEAK",
    "WALLET_SAME_SOURCE_DETECTED",
    "WALLET_DISTRIBUTION_DETECTED",
    "WALLET_BACKFLOW_DETECTED",
    "WALLET_COUNTERPARTY_PRESSURE",
}
BLOCKING_STATUS = {"WALLET_BLOCK", "WALLET_DISTRIBUTION_DETECTED", "WALLET_BACKFLOW_DETECTED"}
PAUSE_STATUS = {"WALLET_PAUSE", "WALLET_UNKNOWN", "WALLET_DATA_WEAK", "WALLET_COUNTERPARTY_PRESSURE"}


class Phase02WalletStructureController:
    """HER wrapper for wallet_structure atomic runtime.

    Controller owns contract validation, hard-negative propagation, standard
    output layout, status transition, handoff and audit. The underlying
    wallet_structure bundle remains an Atomic Skill / module capability.
    """

    def run(self, *, phase01_handoff_file: str | Path, output_dir: str | Path) -> Dict[str, Any]:
        handoff_file = Path(phase01_handoff_file)
        out = Path(output_dir)
        phase_dir = out / "02_wallet_structure"
        dirs = self._ensure_dirs(phase_dir)

        phase01 = json.loads(handoff_file.read_text(encoding="utf-8"))
        validation = self._validate_phase01_handoff(phase01, handoff_file.parent)
        if not validation["allowed"]:
            status = "WALLET_BLOCK" if validation["hard_negative_triggered"] else "WALLET_DATA_WEAK"
            artifacts = self._write_blocked_outputs(phase_dir, dirs, handoff_file, phase01, status, validation)
            return {"phase": PHASE_ID, "phase_status": status, "artifacts": artifacts}

        request = {
            "token_address": phase01.get("token_address", "missing"),
            "token_symbol": phase01.get("token_symbol", ""),
            "chain": phase01.get("chain", "sol"),
            "analysis_time": self._now(),
            "analysis_window": "PHASE02_FROM_PHASE01_HANDOFF",
            "max_wallets": 500,
        }
        collector = self._collector_from_handoff(phase01, handoff_file.parent)
        bundle = build_bundle_from_request(request, collector=collector, output_dir=dirs["atomic"])
        std_files = self._standardize_bundle_outputs(bundle, dirs)

        decision_path = Path(std_files["wallet_structure_decision"])
        decision = json.loads(decision_path.read_text(encoding="utf-8"))
        decision = self._normalize_decision(decision, phase01)
        status = self._apply_hard_negative_status(self._map_status(decision.get("wallet_structure_status")), decision)
        decision["wallet_structure_status"] = status
        decision["hard_negative_triggered"] = status in BLOCKING_STATUS or bool(decision.get("hard_negative_triggered"))
        decision["allowed_next_stage"] = status in {"WALLET_SUPPORT", "WALLET_SAME_SOURCE_DETECTED"} and not decision["hard_negative_triggered"]
        decision["blocked_next_stage_reason"] = "; ".join(decision.get("hard_negative_reasons", [])) if not decision["allowed_next_stage"] else ""
        decision_path.write_text(json.dumps(decision, ensure_ascii=False, indent=2), encoding="utf-8")

        handoff_packet = self._build_handoff_packet(phase01, decision, status, std_files, dirs)
        hp = dirs["handoff"] / "phase_02_handoff_packet.json"
        hp.write_text(json.dumps(handoff_packet, ensure_ascii=False, indent=2), encoding="utf-8")

        output_validation = self._write_output_validation(dirs, std_files, hp)
        handoff_validation = self._write_handoff_validation(dirs, handoff_packet)
        missing_report = self._write_missing_report(dirs, handoff_packet, validation)
        gaps = dirs["audit"] / "gaps.md"
        gaps.write_text(self._gaps(handoff_packet, std_files), encoding="utf-8")
        audit = dirs["audit"] / "audit_report.md"
        audit.write_text(self._audit_report(handoff_file, std_files, handoff_packet, validation), encoding="utf-8")

        artifacts = {
            **std_files,
            "handoff_packet": str(hp),
            "audit_report": str(audit),
            "output_validation_report": str(output_validation),
            "handoff_validation_report": str(handoff_validation),
            "missing_fields_report": str(missing_report),
            "gaps": str(gaps),
        }
        manifest = phase_dir / "run_manifest.json"
        manifest.write_text(json.dumps({"phase": PHASE_ID, "phase_status": status, "artifacts": artifacts}, ensure_ascii=False, indent=2), encoding="utf-8")
        artifacts["run_manifest"] = str(manifest)
        return {"phase": PHASE_ID, "phase_status": status, "artifacts": artifacts}

    def _ensure_dirs(self, phase_dir: Path) -> Dict[str, Path]:
        dirs = {
            "phase": phase_dir,
            "atomic": phase_dir / "atomic_wallet_structure",
            "audit": phase_dir / "audit",
            "handoff": phase_dir / "handoff",
            "normalized": phase_dir / "normalized",
            "wallet_fact": phase_dir / "wallet_fact",
            "reports": phase_dir / "reports",
        }
        for d in dirs.values():
            d.mkdir(parents=True, exist_ok=True)
        return dirs

    def _standardize_bundle_outputs(self, bundle: Mapping[str, str], dirs: Mapping[str, Path]) -> Dict[str, str]:
        mapping = {
            "wallet_raw_snapshot_csv": dirs["wallet_fact"] / "wallet_cleaning_result.csv",
            "wallet_normalized_csv": dirs["normalized"] / "wallet_entity_profile.csv",
            "wallet_role_classification_csv": dirs["normalized"] / "wallet_classification.csv",
            "wallet_funding_edges_csv": dirs["normalized"] / "fund_flow_edges.csv",
            "same_source_groups_csv": dirs["normalized"] / "same_source_groups.csv",
            "distribution_paths_csv": dirs["normalized"] / "distribution_paths.csv",
            "backflow_paths_csv": dirs["normalized"] / "backflow_paths.csv",
            "gmgn_note_table_csv": dirs["normalized"] / "gmgn_note_table.csv",
            "wallet_structure_report_md": dirs["reports"] / "wallet_structure_report.md",
            "wallet_structure_decision_json": dirs["phase"] / "wallet_structure_decision.json",
        }
        out: Dict[str, str] = {}
        for src_key, dst in mapping.items():
            src = bundle.get(src_key)
            if src and Path(src).exists():
                shutil.copyfile(src, dst)
                if dst.suffix == ".csv":
                    self._strip_utf8_bom(dst)
            else:
                self._write_empty_file(dst)
            out[self._artifact_key(dst)] = str(dst)
        token_flow_src = bundle.get("wallet_token_flow_edges_csv")
        current_behavior = dirs["normalized"] / "current_token_behavior.csv"
        if token_flow_src and Path(token_flow_src).exists():
            shutil.copyfile(token_flow_src, current_behavior)
        else:
            self._write_empty_file(current_behavior)
        out["current_token_behavior"] = str(current_behavior)

        excluded = dirs["wallet_fact"] / "excluded_address_list.csv"
        self._write_excluded_address_list(excluded, Path(out["wallet_classification"]))
        out["excluded_address_list"] = str(excluded)
        return out

    def _artifact_key(self, dst: Path) -> str:
        name = dst.name
        if name == "wallet_cleaning_result.csv":
            return "wallet_cleaning_result"
        if name == "wallet_entity_profile.csv":
            return "wallet_entity_profile"
        if name == "fund_flow_edges.csv":
            return "fund_flow_edges"
        if name == "wallet_structure_report.md":
            return "wallet_structure_report"
        if name == "wallet_structure_decision.json":
            return "wallet_structure_decision"
        return name.rsplit(".", 1)[0]

    def _strip_utf8_bom(self, path: Path) -> None:
        raw = path.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            path.write_bytes(raw[3:])

    def _write_empty_file(self, path: Path) -> None:
        if path.suffix == ".csv":
            path.write_text("status\nmissing\n", encoding="utf-8")
        elif path.suffix == ".md":
            path.write_text("# missing\n\n- status: missing\n", encoding="utf-8")
        else:
            path.write_text("{}\n", encoding="utf-8")

    def _write_excluded_address_list(self, path: Path, classification_path: Path) -> None:
        infra_keywords = ("CEX", "LP", "router", "aggregator", "program", "hub", "系统", "池")
        rows = []
        if classification_path.exists():
            with classification_path.open(newline="", encoding="utf-8-sig") as f:
                for row in csv.DictReader(f):
                    text = " ".join(str(v) for v in row.values())
                    if any(k.lower() in text.lower() for k in infra_keywords):
                        rows.append({"wallet_address": row.get("wallet_address") or row.get("address") or "missing", "exclusion_reason": "infra_or_system_address", "keep_edges": "true"})
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["wallet_address", "exclusion_reason", "keep_edges"])
            writer.writeheader()
            writer.writerows(rows)

    def _normalize_decision(self, decision: Mapping[str, Any], phase01: Mapping[str, Any]) -> Dict[str, Any]:
        d = dict(decision)
        status = self._map_status(d.get("wallet_structure_status"))
        supporting = list(d.get("supporting_reasons") or [])
        pause = list(d.get("pause_reasons") or [])
        block = list(d.get("blocking_reasons") or [])
        evidence_chain = list(d.get("evidence_chain") or [])
        d.setdefault("positive_evidence", supporting or evidence_chain[:5])
        d.setdefault("negative_evidence", pause or block)
        d.setdefault("counter_evidence", block or pause)
        d.setdefault("hard_negative_reasons", block)
        d.setdefault("missing_fields", phase01.get("missing_fields", []))
        d.setdefault("confidence_level", d.get("data_quality_status") or "UNKNOWN")
        d.setdefault("risk_level", self._risk_level(d))
        d.setdefault("evidence_level", d.get("wallet_evidence_level") or "E0")
        d.setdefault("wallet_structure_status", status)
        d.setdefault("allowed_next_stage", status in {"WALLET_SUPPORT", "WALLET_SAME_SOURCE_DETECTED"})
        d.setdefault("blocked_next_stage_reason", "")
        return d

    def _risk_level(self, decision: Mapping[str, Any]) -> str:
        try:
            score = float(decision.get("wallet_risk_score", 0) or 0)
        except (TypeError, ValueError):
            score = 0
        if score >= 70:
            return "R3"
        if score >= 35:
            return "R2"
        return "R1"

    def _apply_hard_negative_status(self, status: str, decision: Mapping[str, Any]) -> str:
        if decision.get("backflow_detected"):
            return "WALLET_BACKFLOW_DETECTED"
        if decision.get("distribution_risk_level") == "HIGH" and status == "WALLET_BLOCK":
            return "WALLET_DISTRIBUTION_DETECTED"
        if float(decision.get("counterparty_pressure_score", 0) or 0) >= 70 and status != "WALLET_BLOCK":
            return "WALLET_COUNTERPARTY_PRESSURE"
        return status

    def _build_handoff_packet(self, phase01: Mapping[str, Any], decision: Mapping[str, Any], status: str, files: Mapping[str, str], dirs: Mapping[str, Path]) -> Dict[str, Any]:
        hard_negative = status in BLOCKING_STATUS or bool(decision.get("hard_negative_triggered"))
        allow = status in {"WALLET_SUPPORT", "WALLET_SAME_SOURCE_DETECTED"} and not hard_negative
        return {
            "phase": PHASE_ID,
            "token_address": phase01.get("token_address", "missing"),
            "snapshot_id": phase01.get("snapshot_id", "missing"),
            "phase_status": status,
            "allow_next_stage": allow,
            "next_stage": NEXT_STAGE,
            "required_files_for_next_stage": {
                "wallet_structure_decision": files.get("wallet_structure_decision", "missing"),
                "wallet_classification": files.get("wallet_classification", "missing"),
                "same_source_groups": files.get("same_source_groups", "missing"),
                "distribution_paths": files.get("distribution_paths", "missing"),
                "backflow_paths": files.get("backflow_paths", "missing"),
                "gmgn_note_table": files.get("gmgn_note_table", "missing"),
            },
            "positive_evidence": decision.get("positive_evidence", []),
            "negative_evidence": decision.get("negative_evidence", []),
            "counter_evidence": decision.get("counter_evidence", []),
            "hard_negative_triggered": hard_negative,
            "hard_negative_reasons": decision.get("hard_negative_reasons", []) if hard_negative else [],
            "block_reason": "; ".join(decision.get("hard_negative_reasons", [])) if hard_negative else "",
            "degrade_reason": "; ".join(decision.get("negative_evidence", [])) if status in PAUSE_STATUS else "",
            "missing_fields": decision.get("missing_fields", []),
            "audit_file": str(dirs["audit"] / "audit_report.md"),
        }

    def _validate_phase01_handoff(self, packet: Mapping[str, Any], base: Path) -> Dict[str, Any]:
        errors = []
        required_fields = ["phase", "token_address", "snapshot_id", "phase_status", "allow_next_stage", "next_stage", "required_files_for_next_stage", "missing_fields", "hard_negative_triggered"]
        missing_fields = [f for f in required_fields if f not in packet]
        if missing_fields:
            errors.append("missing_handoff_fields:" + ",".join(missing_fields))
        if packet.get("next_stage") != PHASE_ID:
            errors.append("next_stage_not_phase02_wallet_structure_controller")
        if packet.get("phase_status") in {"DATA_INVALID", "DATA_SOURCE_CONFLICT", "HANDOFF_BLOCKED", "BLOCK"}:
            errors.append("upstream_data_invalid")
        if packet.get("hard_negative_triggered"):
            errors.append("upstream_hard_negative_triggered")
        if packet.get("allow_next_stage") is False:
            errors.append("upstream_disallows_next_stage")
        required = packet.get("required_files_for_next_stage", {}) or {}
        missing_file_names = []
        for name, ref in required.items():
            p = Path(ref)
            if not p.is_absolute():
                p = base / p
            if not p.exists():
                missing_file_names.append(name)
        if missing_file_names:
            errors.append("missing_required_files:" + ",".join(sorted(missing_file_names)))
        source_keys = {"gmgn_traders", "wallet_trade_source_json", "trade_fact_table", "wallet_trade_normalized", "wallet_fact_table"}
        if not any(k in required for k in source_keys):
            errors.append("missing_wallet_trade_fact_entry")
        hard = any("hard_negative" in e or "disallows" in e or "invalid" in e for e in errors)
        return {"allowed": not errors, "errors": errors, "missing_files": missing_file_names, "missing_fields": missing_fields, "hard_negative_triggered": hard}

    def _collector_from_handoff(self, packet: Mapping[str, Any], base: Path):
        refs = packet.get("required_files_for_next_stage", {}) or {}
        selected = refs.get("gmgn_traders") or refs.get("wallet_trade_source_json") or refs.get("trade_fact_table") or refs.get("wallet_trade_normalized") or refs.get("wallet_fact_table")
        if not selected:
            raise ValueError("phase02 controller requires wallet trade facts in handoff")
        selected_path = Path(selected)
        if not selected_path.is_absolute():
            selected_path = base / selected_path

        def collector(token_address: str, token_symbol: str = ""):
            if selected_path.suffix.lower() == ".csv":
                with selected_path.open(newline="", encoding="utf-8-sig") as f:
                    return [dict(r) for r in csv.DictReader(f)]
            data = json.loads(selected_path.read_text(encoding="utf-8"))
            rows = data.get("records", data.get("traders", data.get("data", data if isinstance(data, list) else []))) if isinstance(data, dict) else data
            out = []
            for row in rows if isinstance(rows, list) else []:
                r = dict(row)
                if "address" not in r:
                    r["address"] = r.get("wallet_address") or r.get("wallet") or "missing"
                r.setdefault("token_address", token_address)
                r.setdefault("token_symbol", token_symbol)
                out.append(r)
            return out
        return collector

    def _map_status(self, status: Any) -> str:
        s = str(status or "WALLET_UNKNOWN")
        return s if s in VALID_STATUS else "WALLET_UNKNOWN"

    def _write_output_validation(self, dirs: Mapping[str, Path], files: Mapping[str, str], hp: Path) -> Path:
        required = list(files.values()) + [str(hp)]
        missing = [p for p in required if not Path(p).exists()]
        payload = {"status": "PASS" if not missing else "FAIL", "checked_files": required, "missing_files": missing}
        path = dirs["audit"] / "output_validation_report.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def _write_handoff_validation(self, dirs: Mapping[str, Path], handoff: Mapping[str, Any]) -> Path:
        req = handoff.get("required_files_for_next_stage", {}) or {}
        missing = [k for k, v in req.items() if not v or v == "missing" or not Path(v).exists()]
        ok = handoff.get("phase_status") in VALID_STATUS and handoff.get("next_stage") == NEXT_STAGE and not missing
        payload = {"status": "PASS" if ok else "FAIL", "phase_status": handoff.get("phase_status"), "next_stage": handoff.get("next_stage"), "missing_required_files_for_next_stage": missing}
        path = dirs["audit"] / "handoff_validation_report.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def _write_missing_report(self, dirs: Mapping[str, Path], handoff: Mapping[str, Any], validation: Mapping[str, Any]) -> Path:
        fields = list(handoff.get("missing_fields", []) or []) + list(validation.get("missing_fields", []) or [])
        lines = ["# Phase 02 Missing Fields Report", ""]
        if fields:
            lines += [f"- {x}" for x in sorted(set(map(str, fields)))]
        else:
            lines.append("- none")
        path = dirs["audit"] / "missing_fields_report.md"
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    def _write_blocked_outputs(self, phase_dir: Path, dirs: Mapping[str, Path], handoff_file: Path, phase01: Mapping[str, Any], status: str, validation: Mapping[str, Any]) -> Dict[str, str]:
        decision = {
            "token_address": phase01.get("token_address", "missing"),
            "wallet_structure_status": status,
            "positive_evidence": [],
            "negative_evidence": validation.get("errors", []),
            "counter_evidence": validation.get("errors", []),
            "hard_negative_triggered": status == "WALLET_BLOCK",
            "hard_negative_reasons": validation.get("errors", []) if status == "WALLET_BLOCK" else [],
            "missing_fields": phase01.get("missing_fields", []) + validation.get("missing_fields", []),
            "confidence_level": "LOW",
            "risk_level": "R3" if status == "WALLET_BLOCK" else "R2",
            "evidence_level": "E0",
            "allowed_next_stage": False,
            "blocked_next_stage_reason": "; ".join(validation.get("errors", [])),
        }
        decision_path = phase_dir / "wallet_structure_decision.json"
        decision_path.write_text(json.dumps(decision, ensure_ascii=False, indent=2), encoding="utf-8")
        handoff = self._build_handoff_packet(phase01, decision, status, {"wallet_structure_decision": str(decision_path)}, dirs)
        hp = dirs["handoff"] / "phase_02_handoff_packet.json"
        hp.write_text(json.dumps(handoff, ensure_ascii=False, indent=2), encoding="utf-8")
        missing = self._write_missing_report(dirs, handoff, validation)
        hv = self._write_handoff_validation(dirs, handoff)
        ov = self._write_output_validation(dirs, {"wallet_structure_decision": str(decision_path)}, hp)
        gaps = dirs["audit"] / "gaps.md"
        gaps.write_text(self._gaps(handoff, {"wallet_structure_decision": str(decision_path)}), encoding="utf-8")
        audit = dirs["audit"] / "audit_report.md"
        audit.write_text(self._audit_report(handoff_file, {"wallet_structure_decision": str(decision_path)}, handoff, validation), encoding="utf-8")
        return {"wallet_structure_decision": str(decision_path), "handoff_packet": str(hp), "audit_report": str(audit), "output_validation_report": str(ov), "handoff_validation_report": str(hv), "missing_fields_report": str(missing), "gaps": str(gaps)}

    def _audit_report(self, handoff_file: Path, files: Mapping[str, str], handoff: Mapping[str, Any], validation: Mapping[str, Any]) -> str:
        lines = [
            "# Phase 02 Wallet Structure Controller Audit",
            "",
            f"- phase: {PHASE_ID}",
            f"- input_handoff: {handoff_file}",
            f"- phase_status: {handoff.get('phase_status')}",
            f"- allow_next_stage: {handoff.get('allow_next_stage')}",
            f"- hard negative: {handoff.get('hard_negative_triggered')}",
            f"- validation_errors: {validation.get('errors', [])}",
            "- Atomic Skill: modules.wallet_structure.decision_builder.build_bundle_from_request",
            "- contract_validation: enabled",
            "- handoff_written: enabled",
            "",
            "## 读取文件",
            f"- {handoff_file}",
            "",
            "## Missing 字段",
        ]
        missing = handoff.get("missing_fields") or []
        lines += [f"- {m}" for m in missing] if missing else ["- none"]
        lines += ["", "## 输出文件"]
        for k, v in files.items():
            lines.append(f"- {k}: {v}")
        lines += [
            "",
            "## 反证 / 硬否决",
            f"- negative_evidence: {handoff.get('negative_evidence', [])}",
            f"- counter_evidence: {handoff.get('counter_evidence', [])}",
            f"- hard_negative_reasons: {handoff.get('hard_negative_reasons', [])}",
            "",
            "## 下游交接",
            f"- next_stage: {handoff.get('next_stage')}",
            f"- required_files_for_next_stage: {handoff.get('required_files_for_next_stage')}",
        ]
        return "\n".join(lines) + "\n"

    def _gaps(self, handoff: Mapping[str, Any], files: Mapping[str, str]) -> str:
        gaps = []
        if handoff.get("missing_fields"):
            gaps.append("upstream_or_phase02_missing_fields_carried_forward")
        if handoff.get("phase_status") not in {"WALLET_SUPPORT", "WALLET_SAME_SOURCE_DETECTED"}:
            gaps.append("phase02_not_support_status_requires_review")
        missing_files = [k for k, v in files.items() if not v or v == "missing" or not Path(v).exists()]
        if missing_files:
            gaps.append("missing_output_files:" + ",".join(missing_files))
        if not gaps:
            gaps.append("none")
        return "# gaps\n\n" + "\n".join(f"- {g}" for g in gaps) + "\n"

    def _now(self) -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
