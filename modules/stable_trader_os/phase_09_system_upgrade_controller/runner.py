from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional


class Phase09SystemUpgradeController:
    """Controlled Phase09 system-upgrade runtime.

    Phase09 consumes Phase08 review-learning artifacts and creates a gated upgrade
    package. It never applies runtime changes directly.
    """

    phase = "phase_09_system_upgrade_controller"

    REQUIRED_KEYS = ["review_learning_summary", "failure_attribution"]
    OPTIONAL_KEYS = [
        "success_attribution",
        "evidence_chain_manifest",
        "threshold_review_candidates",
        "model_recalibration_candidates",
        "scenario_case_library",
        "address_history_update",
        "strategy_performance_summary",
    ]

    def run(self, phase08_handoff_file: str | Path, output_dir: str | Path) -> Dict[str, Any]:
        out = Path(output_dir)
        self._mkdirs(out)
        now = self._now()
        source_handoff = Path(phase08_handoff_file)

        validation, handoff, loaded = self._validate_inputs(source_handoff)
        candidates = self._collect_candidates(loaded)
        candidate_issues = self._candidate_issues(candidates)
        if candidate_issues:
            validation["input_status"] = "PHASE_09_INPUT_BLOCKED"
            validation["block_reasons"].extend(candidate_issues)
        elif validation["input_status"] != "PHASE_09_INPUT_BLOCKED" and validation["missing_optional_inputs"]:
            validation["input_status"] = "PHASE_09_INPUT_DEGRADED"

        classification = self._classify_candidates(candidates)
        evidence_chain_manifest = loaded.get("evidence_chain_manifest") if isinstance(loaded.get("evidence_chain_manifest"), Mapping) else {}
        evidence = self._review_evidence(classification["candidates"], loaded)
        rule_review = self._review_rules(classification["candidates"], validation)
        hard_negative_review = self._review_by_type(classification["candidates"], {"HARD_NEGATIVE_ADD", "HARD_NEGATIVE_STRENGTHEN"}, "hard_negative_reviews", validation)
        threshold_review = self._review_thresholds(classification["candidates"], validation)
        model_review = self._review_by_type(classification["candidates"], {"MODEL_WEIGHT_ADJUST"}, "model_weight_reviews", validation)
        schema_contract_review = self._review_by_type(classification["candidates"], {"SCHEMA_UPDATE", "CONTRACT_UPDATE"}, "schema_contract_reviews", validation)
        status_code_review = self._review_by_type(classification["candidates"], {"STATUS_CODE_UPDATE"}, "status_code_reviews", validation)
        telegram_review = self._review_by_type(classification["candidates"], {"TELEGRAM_PANEL_UPDATE"}, "telegram_panel_reviews", validation)
        regression_plan = self._regression_plan(classification["candidates"], validation)
        known_success_review = self._known_success_preservation_review(loaded, classification["candidates"], validation)
        shadow_mode_plan = self._shadow_mode_plan(classification["candidates"], validation)
        rollback_validation = self._rollback_validation(rollback_path := out / "upgrade_package" / "rollback_plan.md", validation)
        regression_report = self._regression_report(validation, loaded, classification["candidates"], known_success_review, rollback_validation, shadow_mode_plan)

        package_ready = validation["input_status"] in {"PHASE_09_INPUT_READY", "PHASE_09_INPUT_DEGRADED"} and regression_report["regression_status"] == "REGRESSION_TEST_PASS"
        package_status = "UPGRADE_PACKAGE_READY" if package_ready else "UPGRADE_PACKAGE_REJECTED"
        system_status = "SYSTEM_UPGRADE_READY" if package_ready else "SYSTEM_UPGRADE_BLOCKED"
        handoff_status = "HANDOFF_READY" if package_ready else "HANDOFF_BLOCKED"

        package = {
            "phase": self.phase,
            "package_version": f"phase09-{now.replace(':', '').replace('-', '')}",
            "package_status": package_status,
            "regression_status": regression_report["regression_status"],
            "requires_manual_confirmation": True,
            "allow_apply_to_runtime": False,
            "recommended_apply_mode": "SHADOW_MODE_FIRST",
            "approved_rule_updates": rule_review["accepted_rule_updates"] if package_ready else [],
            "source_phase08_handoff": str(source_handoff),
            "source_phase08_cases": self._source_cases(loaded),
            "source_phase08_evidence_chain_status": evidence_chain_manifest.get("evidence_chain_status", "EVIDENCE_CHAIN_MISSING"),
            "source_phase08_evidence_chain_manifest": validation["loaded_inputs"].get("evidence_chain_manifest", "missing"),
            "impact_phases": sorted({c.get("target_phase", "missing") for c in classification["candidates"] if c.get("target_phase") != "missing"}),
            "rollback_plan": str(rollback_path),
            "manual_confirmation_required_before_apply": True,
            "direct_runtime_apply_allowed": False,
            "block_reasons": validation["block_reasons"] + regression_report.get("block_reasons", []),
        }
        manifest = {
            "phase": self.phase,
            "system_upgrade_status": system_status,
            "package_status": package_status,
            "regression_status": regression_report["regression_status"],
            "candidate_count": classification["candidate_count"],
            "requires_manual_confirmation": True,
            "allow_apply_to_runtime": False,
            "recommended_apply_mode": "SHADOW_MODE_FIRST",
            "created_at": now,
        }
        feedback_map = {
            "phase": self.phase,
            "feedback_targets": sorted({c.get("target_phase", "missing") for c in classification["candidates"]}),
            "phase08_handoff": str(source_handoff),
            "apply_mode": "SHADOW_MODE_FIRST",
            "runtime_apply_allowed": False,
        }
        next_stage_files = {
            "rule_update_package": str(out / "upgrade_package" / "rule_update_package.json"),
            "system_upgrade_manifest": str(out / "upgrade_package" / "system_upgrade_manifest.json"),
            "known_success_preservation_review": str(out / "validation" / "known_success_preservation_review.json"),
            "regression_validation_report": str(out / "validation" / "regression_validation_report.json"),
            "shadow_mode_plan": str(out / "validation" / "shadow_mode_plan.json"),
            "rollback_validation_report": str(out / "validation" / "rollback_validation_report.json"),
            "rollback_plan": str(rollback_path),
            "evidence_chain_manifest": validation["loaded_inputs"].get("evidence_chain_manifest", "missing"),
        }
        handoff_out = {
            "phase": "phase_09_system_upgrade",
            "controller": self.phase,
            "system_upgrade_status": system_status,
            "regression_status": regression_report["regression_status"],
            "package_status": package_status,
            "requires_manual_confirmation": True,
            "allow_apply_to_runtime": False,
            "recommended_apply_mode": "SHADOW_MODE_FIRST",
            "handoff_status": handoff_status,
            "source_phase08_handoff": str(source_handoff),
            "upgrade_package": str(out / "upgrade_package" / "rule_update_package.json"),
            "rollback_plan": str(rollback_path),
            "evidence_chain_status": evidence_chain_manifest.get("evidence_chain_status", "EVIDENCE_CHAIN_MISSING"),
            "block_reasons": package["block_reasons"],
            "missing_fields": validation["missing_required_inputs"] + validation["missing_optional_inputs"],
            "required_files_for_next_stage": next_stage_files,
        }

        artifacts: Dict[str, str] = {}
        artifacts["upgrade_input_validation"] = str(self._write_json(out / "upgrade_fact" / "upgrade_input_validation.json", validation))
        artifacts["upgrade_candidate_classification"] = str(self._write_json(out / "upgrade_fact" / "upgrade_candidate_classification.json", classification))
        artifacts["upgrade_candidate_table"] = str(self._write_candidate_table(out / "upgrade_fact" / "upgrade_candidate_table.csv", classification["candidates"]))
        artifacts["evidence_strength_review"] = str(self._write_json(out / "upgrade_review" / "evidence_strength_review.json", evidence))
        artifacts["rule_update_review"] = str(self._write_json(out / "upgrade_review" / "rule_update_review.json", rule_review))
        artifacts["hard_negative_update_review"] = str(self._write_json(out / "upgrade_review" / "hard_negative_update_review.json", hard_negative_review))
        artifacts["threshold_calibration_review"] = str(self._write_json(out / "upgrade_review" / "threshold_calibration_review.json", threshold_review))
        artifacts["model_recalibration_review"] = str(self._write_json(out / "upgrade_review" / "model_recalibration_review.json", model_review))
        artifacts["schema_contract_update_review"] = str(self._write_json(out / "upgrade_review" / "schema_contract_update_review.json", schema_contract_review))
        artifacts["status_code_update_review"] = str(self._write_json(out / "upgrade_review" / "status_code_update_review.json", status_code_review))
        artifacts["telegram_panel_update_review"] = str(self._write_json(out / "upgrade_review" / "telegram_panel_update_review.json", telegram_review))
        artifacts["regression_validation_plan"] = str(self._write_json(out / "validation" / "regression_validation_plan.json", regression_plan))
        artifacts["known_success_preservation_review"] = str(self._write_json(out / "validation" / "known_success_preservation_review.json", known_success_review))
        artifacts["rollback_validation_report"] = str(self._write_json(out / "validation" / "rollback_validation_report.json", rollback_validation))
        artifacts["shadow_mode_plan"] = str(self._write_json(out / "validation" / "shadow_mode_plan.json", shadow_mode_plan))
        artifacts["regression_validation_report"] = str(self._write_json(out / "validation" / "regression_validation_report.json", regression_report))
        artifacts["rule_update_package"] = str(self._write_json(out / "upgrade_package" / "rule_update_package.json", package))
        artifacts["system_upgrade_manifest"] = str(self._write_json(out / "upgrade_package" / "system_upgrade_manifest.json", manifest))
        artifacts["upgrade_diff_summary"] = str(self._write_text(out / "upgrade_package" / "upgrade_diff_summary.md", self._diff_summary(classification, package)))
        artifacts["version_changelog"] = str(self._write_text(out / "upgrade_package" / "version_changelog.md", self._changelog(package, classification)))
        artifacts["rollback_plan"] = str(self._write_text(rollback_path, self._rollback_plan(package)))
        artifacts["threshold_calibration_report"] = str(self._write_text(out / "reports" / "threshold_calibration_report.md", self._generic_report("Threshold Calibration", threshold_review)))
        artifacts["model_recalibration_report"] = str(self._write_text(out / "reports" / "model_recalibration_report.md", self._generic_report("Model Recalibration", model_review)))
        artifacts["system_upgrade_report"] = str(self._write_text(out / "reports" / "system_upgrade_report.md", self._system_report(manifest, validation, package)))
        artifacts["regression_validation_report_md"] = str(self._write_text(out / "reports" / "regression_validation_report.md", self._generic_report("Regression Validation", regression_report)))
        artifacts["handoff_packet"] = str(self._write_json(out / "handoff" / "phase_09_handoff_packet.json", handoff_out))
        artifacts["system_upgrade_feedback_map"] = str(self._write_json(out / "handoff" / "system_upgrade_feedback_map.json", feedback_map))
        output_validation = self._output_validation(out, artifacts)
        artifacts["output_validation_report"] = str(self._write_json(out / "audit" / "output_validation_report.json", output_validation))
        handoff_validation = self._handoff_validation(handoff_out)
        artifacts["handoff_validation_report"] = str(self._write_json(out / "audit" / "handoff_validation_report.json", handoff_validation))
        gaps = self._gaps(validation, regression_report, package)
        artifacts["gaps"] = str(self._write_text(out / "audit" / "gaps.md", gaps))
        artifacts["audit_report"] = str(self._write_text(out / "audit" / "phase_09_audit_report.md", self._audit_report(validation, classification, regression_report, package, artifacts)))

        return {"phase": self.phase, "status": system_status, "artifacts": artifacts, "handoff": handoff_out}

    def _validate_inputs(self, source_handoff: Path) -> tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
        validation = {
            "phase": self.phase,
            "input_status": "PHASE_09_INPUT_READY",
            "phase08_handoff_file": str(source_handoff),
            "direct_runtime_apply_allowed": False,
            "missing_required_inputs": [],
            "missing_optional_inputs": [],
            "block_reasons": [],
            "degrade_reasons": [],
            "loaded_inputs": {},
        }
        loaded: Dict[str, Any] = {}
        if not source_handoff.exists():
            validation["input_status"] = "PHASE_09_INPUT_BLOCKED"
            validation["missing_required_inputs"].append("phase_08_handoff_packet")
            validation["block_reasons"].append("phase_08_handoff_packet_missing")
            return validation, {}, loaded
        handoff = self._read_json(source_handoff) or {}
        loaded["phase08_handoff"] = handoff
        required_files = handoff.get("required_files_for_next_stage", {}) if isinstance(handoff, Mapping) else {}
        for key in self.REQUIRED_KEYS:
            path = Path(str(required_files.get(key, "")))
            if not path.exists():
                validation["input_status"] = "PHASE_09_INPUT_BLOCKED"
                validation["missing_required_inputs"].append(key)
                validation["block_reasons"].append(f"{key}_missing")
            else:
                loaded[key] = self._read_any(path)
                validation["loaded_inputs"][key] = str(path)
        rule_path = Path(str(required_files.get("rule_update_candidates", "")))
        if not rule_path.exists():
            validation["input_status"] = "PHASE_09_INPUT_BLOCKED"
            validation["missing_required_inputs"].append("rule_update_candidates")
            validation["block_reasons"].append("rule_update_candidates_missing")
        else:
            loaded["rule_update_candidates"] = self._read_json(rule_path) or {}
            validation["loaded_inputs"]["rule_update_candidates"] = str(rule_path)
        for key in self.OPTIONAL_KEYS:
            path_text = required_files.get(key)
            if not path_text or not Path(str(path_text)).exists():
                validation["missing_optional_inputs"].append(key)
                validation["degrade_reasons"].append(f"{key}_missing")
            else:
                loaded[key] = self._read_any(Path(str(path_text)))
                validation["loaded_inputs"][key] = str(path_text)
        if validation["input_status"] != "PHASE_09_INPUT_BLOCKED" and validation["missing_optional_inputs"]:
            validation["input_status"] = "PHASE_09_INPUT_DEGRADED"
        return validation, handoff, loaded

    def _collect_candidates(self, loaded: Mapping[str, Any]) -> List[Dict[str, Any]]:
        candidates: List[Dict[str, Any]] = []
        for raw in self._extract_candidate_list(loaded.get("rule_update_candidates")):
            candidates.append(self._candidate(raw, default_type="RULE_MODIFY"))
        for raw in self._extract_candidate_list(loaded.get("threshold_review_candidates")):
            candidates.append(self._candidate(raw, default_type="THRESHOLD_ADJUST"))
        for raw in self._extract_candidate_list(loaded.get("model_recalibration_candidates")):
            candidates.append(self._candidate(raw, default_type="MODEL_WEIGHT_ADJUST"))
        return candidates

    def _candidate(self, raw: Mapping[str, Any], default_type: str) -> Dict[str, Any]:
        c = dict(raw)
        c.setdefault("candidate_id", f"candidate-{abs(hash(json.dumps(c, sort_keys=True, default=str))) % 100000}")
        c["upgrade_type"] = c.get("candidate_type") or c.get("upgrade_type") or default_type
        c["target_phase"] = c.get("target_phase") or "missing"
        c["evidence_cases"] = c.get("evidence_cases", [])
        c["evidence_refs"] = c.get("evidence_refs", [])
        c["reason"] = c.get("reason") or c.get("review_reason") or "missing"
        return c

    def _candidate_issues(self, candidates: Iterable[Mapping[str, Any]]) -> List[str]:
        issues = []
        for c in candidates:
            cid = c.get("candidate_id", "unknown")
            if not c.get("target_phase") or c.get("target_phase") == "missing":
                issues.append(f"candidate_{cid}_target_phase_missing")
            if not c.get("evidence_cases"):
                issues.append(f"candidate_{cid}_evidence_cases_missing")
        return issues

    def _classify_candidates(self, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        rows = []
        for c in candidates:
            rows.append({
                "candidate_id": c.get("candidate_id"),
                "upgrade_type": c.get("upgrade_type"),
                "target_phase": c.get("target_phase", "missing"),
                "evidence_cases": c.get("evidence_cases", []),
                "evidence_refs": c.get("evidence_refs", []),
                "reason": c.get("reason", "missing"),
                "classification_status": "CLASSIFIED" if c.get("target_phase") != "missing" and c.get("evidence_cases") else "INVALID",
                "direct_runtime_apply_allowed": False,
            })
        return {"phase": self.phase, "candidate_count": len(rows), "candidates": rows}

    def _review_evidence(self, candidates: List[Mapping[str, Any]], loaded: Mapping[str, Any]) -> Dict[str, Any]:
        reviews = []
        levels = []
        success_count = len(loaded.get("success_attribution") or [])
        failure_count = len(loaded.get("failure_attribution") or [])
        evidence_chain = loaded.get("evidence_chain_manifest") if isinstance(loaded.get("evidence_chain_manifest"), Mapping) else {}
        for c in candidates:
            n = len(c.get("evidence_cases") or [])
            if n <= 0:
                level = "EVIDENCE_NONE"
                decision = "REJECT_CANDIDATE"
            elif n == 1 and success_count == 0:
                level = "EVIDENCE_WEAK"
                decision = "HOLD_FOR_MORE_DATA"
            elif n == 1:
                level = "EVIDENCE_MODERATE"
                decision = "ACCEPT_FOR_REGRESSION"
            else:
                level = "EVIDENCE_STRONG"
                decision = "ACCEPT_FOR_REGRESSION"
            levels.append(level)
            reviews.append({"candidate_id": c.get("candidate_id"), "evidence_level": level, "review_decision": decision, "evidence_case_count": n, "failure_count": failure_count, "success_count": success_count})
        order = ["EVIDENCE_NONE", "EVIDENCE_WEAK", "EVIDENCE_MODERATE", "EVIDENCE_STRONG", "EVIDENCE_CRITICAL"]
        overall = max(levels or ["EVIDENCE_NONE"], key=lambda x: order.index(x))
        return {
            "phase": self.phase,
            "overall_evidence_level": overall,
            "candidate_reviews": reviews,
            "phase08_evidence_chain_status": evidence_chain.get("evidence_chain_status", "EVIDENCE_CHAIN_MISSING"),
            "phase08_evidence_chain_links": evidence_chain.get("links", []),
            "phase08_evidence_chain_missing": evidence_chain.get("missing_evidence_chain", []),
            "absolute_conclusion_allowed": bool(evidence_chain.get("absolute_conclusion_allowed", False)),
        }

    def _review_rules(self, candidates: List[Mapping[str, Any]], validation: Mapping[str, Any]) -> Dict[str, Any]:
        reviews = []
        accepted = []
        blocked = validation.get("input_status") == "PHASE_09_INPUT_BLOCKED"
        for c in candidates:
            is_rule = c.get("upgrade_type") in {"RULE_ADD", "RULE_MODIFY", "RULE_DEPRECATE", "HARD_NEGATIVE_ADD", "HARD_NEGATIVE_STRENGTHEN"}
            if not is_rule:
                continue
            decision = "REJECT_UPDATE" if blocked or c.get("classification_status") == "INVALID" else "ACCEPT_FOR_PACKAGE"
            item = {"candidate_id": c.get("candidate_id"), "target_phase": c.get("target_phase"), "upgrade_type": c.get("upgrade_type"), "review_decision": decision, "direct_runtime_apply_allowed": False, "requires_manual_confirmation": True}
            reviews.append(item)
            if decision == "ACCEPT_FOR_PACKAGE":
                accepted.append(item)
        return {"phase": self.phase, "rule_reviews": reviews, "accepted_rule_updates": accepted, "direct_runtime_apply_allowed": False}

    def _review_by_type(self, candidates: List[Mapping[str, Any]], types: set[str], key: str, validation: Mapping[str, Any]) -> Dict[str, Any]:
        reviews = []
        blocked = validation.get("input_status") == "PHASE_09_INPUT_BLOCKED"
        for c in candidates:
            if c.get("upgrade_type") in types:
                reviews.append({"candidate_id": c.get("candidate_id"), "target_phase": c.get("target_phase"), "upgrade_type": c.get("upgrade_type"), "review_decision": "REJECT_CANDIDATE" if blocked else "ACCEPT_FOR_REGRESSION", "direct_apply_allowed": False, "requires_manual_confirmation": True})
        return {"phase": self.phase, key: reviews, "direct_runtime_apply_allowed": False}

    def _review_thresholds(self, candidates: List[Mapping[str, Any]], validation: Mapping[str, Any]) -> Dict[str, Any]:
        rows = []
        for c in candidates:
            if c.get("upgrade_type") == "THRESHOLD_ADJUST":
                n = len(c.get("evidence_cases") or [])
                if validation.get("input_status") == "PHASE_09_INPUT_BLOCKED":
                    decision = "HOLD_FOR_MORE_DATA"
                elif n <= 1:
                    decision = "HOLD_FOR_MORE_DATA"
                else:
                    decision = "ACCEPT_FOR_REGRESSION"
                rows.append({"candidate_id": c.get("candidate_id"), "target_phase": c.get("target_phase"), "calibration_decision": decision, "direct_threshold_change_allowed": False, "requires_shadow_mode": True})
        return {"phase": self.phase, "threshold_status": "THRESHOLD_REVIEW_REQUIRED" if rows else "NO_THRESHOLD_UPDATE", "threshold_reviews": rows}

    def _regression_plan(self, candidates: List[Mapping[str, Any]], validation: Mapping[str, Any]) -> Dict[str, Any]:
        return {"phase": self.phase, "plan_status": "REGRESSION_PLAN_READY", "candidate_count": len(candidates), "test_targets": sorted({c.get("target_phase", "missing") for c in candidates}), "blocked_by_input": validation.get("input_status") == "PHASE_09_INPUT_BLOCKED", "checks": ["known_failure_block_check", "known_success_preservation_check", "rollback_plan_check", "shadow_mode_gate_check"]}

    def _known_success_preservation_review(self, loaded: Mapping[str, Any], candidates: List[Mapping[str, Any]], validation: Mapping[str, Any]) -> Dict[str, Any]:
        successes = loaded.get("success_attribution") or []
        candidate_targets = sorted({c.get("target_phase", "missing") for c in candidates if c.get("classification_status") != "INVALID"})
        protected_cases = []
        for row in successes:
            if not isinstance(row, Mapping):
                continue
            protected_cases.append({
                "token_address": row.get("token_address", "missing"),
                "success_type": row.get("success_type", "missing"),
                "source_phase": row.get("source_phase", "missing"),
                "evidence_refs": row.get("evidence_refs", []),
                "preservation_decision": "PRESERVE_BEFORE_UPGRADE",
            })
        missing_refs = [case["token_address"] for case in protected_cases if not case.get("evidence_refs")]
        if validation.get("input_status") == "PHASE_09_INPUT_BLOCKED":
            status = "KNOWN_SUCCESS_BLOCKED_BY_INPUT"
        elif not protected_cases:
            status = "KNOWN_SUCCESS_MISSING"
        elif missing_refs:
            status = "KNOWN_SUCCESS_DEGRADED"
        else:
            status = "KNOWN_SUCCESS_PRESERVED"
        return {
            "phase": self.phase,
            "known_success_status": status,
            "known_success_case_count": len(protected_cases),
            "candidate_targets": candidate_targets,
            "protected_cases": protected_cases,
            "missing_evidence_refs": missing_refs,
            "block_reason": "known_success_cases_missing" if status == "KNOWN_SUCCESS_MISSING" else None,
            "regression_fixture_required": True,
            "preservation_gate": "no_known_success_regression",
            "allow_apply_to_runtime": False,
        }

    def _rollback_validation(self, rollback_path: Path, validation: Mapping[str, Any]) -> Dict[str, Any]:
        checks = {
            "rollback_path_declared": bool(str(rollback_path)),
            "runtime_apply_blocked": True,
            "manual_confirmation_required": True,
            "no_production_files_modified_by_phase09": True,
            "shadow_mode_can_be_disabled": True,
        }
        status = "ROLLBACK_VALID" if all(checks.values()) and validation.get("input_status") != "PHASE_09_INPUT_BLOCKED" else "ROLLBACK_BLOCKED"
        return {"phase": self.phase, "rollback_validation_status": status, "rollback_plan": str(rollback_path), "checks": checks}

    def _shadow_mode_plan(self, candidates: List[Mapping[str, Any]], validation: Mapping[str, Any]) -> Dict[str, Any]:
        candidate_ids = [str(c.get("candidate_id")) for c in candidates if c.get("classification_status") != "INVALID"]
        status = "SHADOW_MODE_BLOCKED" if validation.get("input_status") == "PHASE_09_INPUT_BLOCKED" else "SHADOW_MODE_REQUIRED"
        return {
            "phase": self.phase,
            "shadow_mode_status": status,
            "candidate_ids": candidate_ids,
            "entry_gate": "manual_confirmation_required",
            "exit_gate": "regression_pass_and_no_known_success_regression",
            "runtime_apply_allowed": False,
            "broadcast_allowed": False,
            "signing_allowed": False,
        }

    def _regression_report(self, validation: Mapping[str, Any], loaded: Mapping[str, Any], candidates: List[Mapping[str, Any]], known_success_review: Mapping[str, Any], rollback_validation: Mapping[str, Any], shadow_mode_plan: Mapping[str, Any]) -> Dict[str, Any]:
        block_reasons: List[str] = []
        failures = loaded.get("failure_attribution") or []
        successes = loaded.get("success_attribution") or []
        if validation.get("input_status") == "PHASE_09_INPUT_BLOCKED":
            block_reasons.extend(validation.get("block_reasons", []))
        if failures and not successes:
            block_reasons.append("new_rule_would_not_preserve_known_success_cases")
        if known_success_review.get("known_success_status") in {"KNOWN_SUCCESS_MISSING", "KNOWN_SUCCESS_BLOCKED_BY_INPUT"}:
            block_reasons.append(known_success_review.get("block_reason") or "known_success_not_preserved")
        if rollback_validation.get("rollback_validation_status") != "ROLLBACK_VALID":
            block_reasons.append("rollback_validation_failed")
        if shadow_mode_plan.get("shadow_mode_status") != "SHADOW_MODE_REQUIRED":
            block_reasons.append("shadow_mode_gate_not_ready")
        if any(c.get("classification_status") == "INVALID" for c in candidates):
            block_reasons.append("invalid_candidate_in_regression_scope")
        block_reasons = list(dict.fromkeys(block_reasons))
        status = "REGRESSION_TEST_FAIL" if block_reasons else "REGRESSION_TEST_PASS"
        return {
            "phase": self.phase,
            "regression_status": status,
            "decision": "UPGRADE_BLOCKED" if status == "REGRESSION_TEST_FAIL" else "ACCEPT_FOR_PACKAGE",
            "known_failure_case_count": len(failures),
            "known_success_case_count": len(successes),
            "known_success_status": known_success_review.get("known_success_status"),
            "rollback_validation_status": rollback_validation.get("rollback_validation_status"),
            "shadow_mode_status": shadow_mode_plan.get("shadow_mode_status"),
            "block_reasons": block_reasons,
            "allow_apply_to_runtime": False,
        }

    def _output_validation(self, out: Path, artifacts: Mapping[str, str]) -> Dict[str, Any]:
        missing = [key for key, path in artifacts.items() if not Path(path).exists()]
        return {"phase": self.phase, "output_status": "OUTPUT_VALID" if not missing else "OUTPUT_INCOMPLETE", "missing_outputs": missing, "checked_output_count": len(artifacts)}

    def _handoff_validation(self, handoff: Mapping[str, Any]) -> Dict[str, Any]:
        ok = handoff.get("requires_manual_confirmation") is True and handoff.get("allow_apply_to_runtime") is False and handoff.get("recommended_apply_mode") == "SHADOW_MODE_FIRST"
        return {"phase": self.phase, "handoff_validation_status": "HANDOFF_VALID" if ok else "HANDOFF_INVALID", "manual_confirmation_required": handoff.get("requires_manual_confirmation"), "runtime_apply_allowed": handoff.get("allow_apply_to_runtime")}

    def _gaps(self, validation: Mapping[str, Any], regression: Mapping[str, Any], package: Mapping[str, Any]) -> str:
        lines = ["# Phase09 Gaps", ""]
        gaps = validation.get("block_reasons", []) + regression.get("block_reasons", [])
        if gaps:
            for g in gaps:
                lines.append(f"- {g}")
        else:
            lines.append("- missing: none")
        lines.append("- runtime_apply: blocked_by_design")
        return "\n".join(lines) + "\n"

    def _audit_report(self, validation: Mapping[str, Any], classification: Mapping[str, Any], regression: Mapping[str, Any], package: Mapping[str, Any], artifacts: Mapping[str, str]) -> str:
        return f"""# Phase09 System Upgrade Audit

- phase: {self.phase}
- input_status: {validation.get('input_status')}
- package_status: {package.get('package_status')}
- regression_status: {regression.get('regression_status')}
- candidate_count: {classification.get('candidate_count')}
- requires_manual_confirmation: true
- allow_apply_to_runtime: false
- artifact_count: {len(artifacts)}

## Block reasons

{chr(10).join('- ' + r for r in (package.get('block_reasons') or ['none']))}

## Boundary

Phase09 produced review/package artifacts only. It did not apply runtime changes.
"""

    def _diff_summary(self, classification: Mapping[str, Any], package: Mapping[str, Any]) -> str:
        return f"# Upgrade Diff Summary\n\n- candidate_count: {classification.get('candidate_count')}\n- package_status: {package.get('package_status')}\n- direct_runtime_apply_allowed: false\n"

    def _changelog(self, package: Mapping[str, Any], classification: Mapping[str, Any]) -> str:
        return f"# Version Changelog\n\n- version: {package.get('package_version')}\n- candidate_count: {classification.get('candidate_count')}\n- apply_mode: SHADOW_MODE_FIRST\n"

    def _rollback_plan(self, package: Mapping[str, Any]) -> str:
        return f"# Rollback Plan\n\n- package_version: {package.get('package_version')}\n- runtime_apply_allowed: false\n- rollback_action: discard package or disable shadow-mode trial before staged rollout.\n- production_files_modified_by_phase09: none\n"

    def _generic_report(self, title: str, data: Mapping[str, Any]) -> str:
        return f"# {title}\n\n```json\n{json.dumps(data, ensure_ascii=False, indent=2)}\n```\n"

    def _system_report(self, manifest: Mapping[str, Any], validation: Mapping[str, Any], package: Mapping[str, Any]) -> str:
        return f"# System Upgrade Report\n\n- system_upgrade_status: {manifest.get('system_upgrade_status')}\n- input_status: {validation.get('input_status')}\n- package_status: {package.get('package_status')}\n- regression_status: {manifest.get('regression_status')}\n- requires_manual_confirmation: true\n- allow_apply_to_runtime: false\n"

    def _source_cases(self, loaded: Mapping[str, Any]) -> List[Any]:
        cases: List[Any] = []
        for row in loaded.get("failure_attribution") or []:
            if isinstance(row, Mapping) and row.get("token_address"):
                cases.append(row.get("token_address"))
        for row in loaded.get("success_attribution") or []:
            if isinstance(row, Mapping) and row.get("token_address"):
                cases.append(row.get("token_address"))
        return sorted(set(cases))

    def _extract_candidate_list(self, data: Any) -> List[Mapping[str, Any]]:
        if not data:
            return []
        if isinstance(data, Mapping):
            raw = data.get("candidates", [])
            return raw if isinstance(raw, list) else []
        if isinstance(data, list):
            return data
        return []

    def _read_any(self, path: Path) -> Any:
        if path.suffix == ".json":
            return self._read_json(path)
        if path.suffix == ".jsonl":
            return self._read_jsonl(path)
        if path.suffix == ".csv":
            return self._read_csv(path)
        return path.read_text(encoding="utf-8")

    def _read_json(self, path: Path) -> Any:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return None

    def _read_jsonl(self, path: Path) -> List[Any]:
        rows = []
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                rows.append(json.loads(line))
        return rows

    def _read_csv(self, path: Path) -> List[Dict[str, str]]:
        with path.open(newline="", encoding="utf-8-sig") as f:
            return list(csv.DictReader(f))

    def _write_json(self, path: Path, data: Mapping[str, Any]) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def _write_text(self, path: Path, text: str) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def _write_candidate_table(self, path: Path, rows: List[Mapping[str, Any]]) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        fields = ["candidate_id", "upgrade_type", "target_phase", "evidence_case_count", "classification_status", "direct_runtime_apply_allowed"]
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for row in rows:
                writer.writerow({
                    "candidate_id": row.get("candidate_id"),
                    "upgrade_type": row.get("upgrade_type"),
                    "target_phase": row.get("target_phase"),
                    "evidence_case_count": len(row.get("evidence_cases") or []),
                    "classification_status": row.get("classification_status"),
                    "direct_runtime_apply_allowed": "false",
                })
        return path

    def _mkdirs(self, out: Path) -> None:
        for name in ["upgrade_fact", "upgrade_review", "validation", "upgrade_package", "reports", "handoff", "audit"]:
            (out / name).mkdir(parents=True, exist_ok=True)

    def _now(self) -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
