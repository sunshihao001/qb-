import csv
import json
from pathlib import Path

from modules.stable_trader_os.phase_09_system_upgrade_controller import Phase09SystemUpgradeController


def _write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def _write_jsonl(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
    return path


def _write_csv(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields or ["empty"])
        writer.writeheader()
        if rows:
            writer.writerows(rows)
    return path


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _read_csv(path):
    with Path(path).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _phase08_package(tmp_path: Path, *, include_rule_candidates=True, invalid_candidate=False, regression_should_fail=False, no_update_required=False, optional_missing=False):
    run = tmp_path / "phase08_run" / "08_review_learning"
    token = "[REDACTED]"
    now = "2026-05-09T00:00:00+00:00"

    failures = [
        {
            "timestamp": now,
            "token_address": token,
            "source_phase": "phase_07_execution_risk_controller" if not regression_should_fail else "phase_06_strategy_gate_controller",
            "failure_type": "SLIPPAGE_TOO_HIGH" if not regression_should_fail else "PAPER_TRADE_LOSS",
            "failure_category": "execution_block_review" if not regression_should_fail else "paper_trade_result",
            "pnl_pct": -9.5 if regression_should_fail else None,
            "evidence_refs": ["risk_events.jsonl", "execution_risk_decision.json"],
            "suggested_followup": "review_SLIPPAGE_TOO_HIGH",
            "absolute_conclusion": False,
        }
    ]
    successes = [] if regression_should_fail else [
        {
            "timestamp": now,
            "token_address": token,
            "source_phase": "phase_06_strategy_gate_controller",
            "success_type": "PAPER_TRADE_PROFIT",
            "pnl_pct": 18.2,
            "evidence_refs": ["paper_positions_closed.json", "strategy_gate_decision.json"],
            "rule_effective": True,
            "absolute_conclusion": False,
        }
    ]
    _write_jsonl(run / "attribution" / "failure_attribution.jsonl", failures)
    _write_jsonl(run / "attribution" / "success_attribution.jsonl", successes)

    summary = {
        "phase": "phase_08_review_learning",
        "token_address": token,
        "input_status": "PHASE_08_INPUT_READY",
        "review_status": "REVIEW_COMPLETE",
        "failure_count": len(failures),
        "success_count": len(successes),
        "blocked_sample_count": 0 if regression_should_fail else 1,
        "manual_review_queue_count": 0,
        "direct_rule_change_allowed": False,
        "missing_fields": [],
        "block_reasons": [],
    }
    _write_json(run / "learning" / "review_learning_summary.json", summary)

    candidates = []
    if include_rule_candidates:
        candidate = {
            "candidate_id": "rule-1",
            "target_phase": "phase_07_execution_risk_controller",
            "candidate_type": "HARD_NEGATIVE_STRENGTHEN",
            "reason": "SLIPPAGE_TOO_HIGH repeated before paper execution",
            "evidence_cases": [token],
            "evidence_refs": ["risk_events.jsonl", "execution_risk_decision.json"],
            "phase09_only": True,
        }
        if invalid_candidate:
            candidate.pop("evidence_cases")
        candidates.append(candidate)
    rule_update_candidates = {
        "phase": "phase_08_review_learning",
        "direct_rule_change_allowed": False,
        "no_update_required": no_update_required,
        "candidates": candidates,
    }
    if include_rule_candidates:
        _write_json(run / "learning" / "rule_update_candidates.json", rule_update_candidates)

    threshold_candidates = {
        "phase": "phase_08_review_learning",
        "phase09_only": True,
        "candidates": [
            {
                "candidate_id": "threshold-1",
                "target_phase": "phase_07_execution_risk_controller",
                "metric": "SLIPPAGE_TOO_HIGH",
                "review_reason": "execution risk block appeared in reviewed sample",
                "evidence_cases": [token],
                "phase09_only": True,
            }
        ],
    }
    _write_json(run / "learning" / "threshold_review_candidates.json", threshold_candidates)
    _write_json(run / "learning" / "model_recalibration_candidates.json", {"phase": "phase_08_review_learning", "phase09_only": True, "candidates": []})
    _write_json(run / "learning" / "scenario_case_library.json", {"phase": "phase_08_review_learning", "direct_rule_change_allowed": False, "cases": [{"token_address": token, "scenario": "risk_scene", "outcome": "failure", "source_phase_trace": ["phase_06_strategy_gate_controller", "phase_07_execution_risk_controller"], "evidence_refs": ["phase_decision_trace.json"]}]})
    _write_json(run / "learning" / "strategy_performance_summary.json", {"phase": "phase_08_review_learning", "token_address": token, "closed_position_count": 1 if regression_should_fail else 2, "win_count": 0 if regression_should_fail else 1, "loss_count": 1, "failure_count": len(failures), "success_count": len(successes)})
    _write_csv(run / "learning" / "address_history_update.csv", [{"token_address": token, "address": token, "update_mode": "patch", "direct_overwrite_allowed": "false", "source_phase": "phase_08_review_learning"}])
    _write_json(run / "review_trace" / "evidence_chain_manifest.json", {
        "phase": "phase_08_review_learning_controller",
        "token_address": token,
        "snapshot_id": "snapshot-phase09-test",
        "evidence_chain_status": "EVIDENCE_CHAIN_COMPLETE",
        "required_phase_count": 7,
        "present_phase_count": 7,
        "missing_evidence_chain": [],
        "links": [
            {
                "phase": "phase_07_execution_risk_controller",
                "source_key": "execution_risk_decision",
                "source_path": "execution_risk_decision.json",
                "present": True,
                "status": "EXECUTION_BLOCK" if not regression_should_fail else "PAPER_READY",
                "evidence_level": "EVIDENCE_STRONG",
            }
        ],
        "absolute_conclusion_allowed": False,
    })

    required_files = {
        "review_learning_summary": str(run / "learning" / "review_learning_summary.json"),
        "failure_attribution": str(run / "attribution" / "failure_attribution.jsonl"),
        "success_attribution": str(run / "attribution" / "success_attribution.jsonl"),
        "evidence_chain_manifest": str(run / "review_trace" / "evidence_chain_manifest.json"),
        "threshold_review_candidates": str(run / "learning" / "threshold_review_candidates.json"),
        "model_recalibration_candidates": str(run / "learning" / "model_recalibration_candidates.json"),
    }
    if include_rule_candidates:
        required_files["rule_update_candidates"] = str(run / "learning" / "rule_update_candidates.json")
    if not optional_missing:
        required_files.update({
            "scenario_case_library": str(run / "learning" / "scenario_case_library.json"),
            "address_history_update": str(run / "learning" / "address_history_update.csv"),
            "strategy_performance_summary": str(run / "learning" / "strategy_performance_summary.json"),
        })
    handoff = {
        "phase": "phase_08_review_learning_controller",
        "token_address": token,
        "snapshot_id": "snapshot-phase09-test",
        "phase_status": "REVIEW_COMPLETE",
        "allow_next_stage": True,
        "next_stage": "phase_09_system_upgrade_controller",
        "required_files_for_next_stage": required_files,
        "positive_evidence": ["phase08_review_complete"],
        "negative_evidence": [],
        "hard_negative_triggered": False,
        "block_reason": "",
        "degrade_reason": "",
        "missing_fields": [],
        "audit_file": str(run / "audit" / "audit_report.md"),
    }
    return _write_json(run / "handoff" / "phase_08_handoff_packet.json", handoff)


def test_phase09_builds_controlled_upgrade_package_from_phase08_candidates(tmp_path: Path):
    handoff = _phase08_package(tmp_path)
    result = Phase09SystemUpgradeController().run(phase08_handoff_file=handoff, output_dir=tmp_path / "out")
    assert result["phase"] == "phase_09_system_upgrade_controller"
    assert result["status"] == "SYSTEM_UPGRADE_READY"
    artifacts = result["artifacts"]
    required = [
        "upgrade_input_validation",
        "upgrade_candidate_classification",
        "upgrade_candidate_table",
        "evidence_strength_review",
        "rule_update_review",
        "hard_negative_update_review",
        "threshold_calibration_review",
        "model_recalibration_review",
        "schema_contract_update_review",
        "status_code_update_review",
        "telegram_panel_update_review",
        "regression_validation_plan",
        "known_success_preservation_review",
        "rollback_validation_report",
        "shadow_mode_plan",
        "regression_validation_report",
        "rule_update_package",
        "system_upgrade_manifest",
        "version_changelog",
        "rollback_plan",
        "system_upgrade_feedback_map",
        "system_upgrade_report",
        "handoff_packet",
        "audit_report",
        "output_validation_report",
        "handoff_validation_report",
        "gaps",
    ]
    for key in required:
        assert key in artifacts
        assert Path(artifacts[key]).exists(), key

    validation = _load(artifacts["upgrade_input_validation"])
    assert validation["input_status"] == "PHASE_09_INPUT_READY"
    assert validation["direct_runtime_apply_allowed"] is False

    classification = _load(artifacts["upgrade_candidate_classification"])
    assert classification["candidate_count"] >= 2
    assert all(c["target_phase"] != "missing" for c in classification["candidates"])
    assert all(c["evidence_cases"] for c in classification["candidates"])
    rows = _read_csv(artifacts["upgrade_candidate_table"])
    assert rows and {"candidate_id", "upgrade_type", "target_phase", "evidence_case_count"} <= set(rows[0].keys())

    evidence = _load(artifacts["evidence_strength_review"])
    assert evidence["overall_evidence_level"] in {"EVIDENCE_WEAK", "EVIDENCE_MODERATE", "EVIDENCE_STRONG", "EVIDENCE_CRITICAL"}
    assert all(r["review_decision"] in {"HOLD_FOR_MORE_DATA", "ACCEPT_FOR_REGRESSION", "REJECT_CANDIDATE", "REQUIRES_MANUAL_CONFIRMATION", "SHADOW_MODE_REQUIRED"} for r in evidence["candidate_reviews"])

    regression_plan = _load(artifacts["regression_validation_plan"])
    assert "known_success_preservation_check" in regression_plan["checks"]
    assert "rollback_plan_check" in regression_plan["checks"]
    assert "shadow_mode_gate_check" in regression_plan["checks"]

    known_success = _load(artifacts["known_success_preservation_review"])
    assert known_success["known_success_status"] == "KNOWN_SUCCESS_PRESERVED"
    assert known_success["known_success_case_count"] == 1
    assert known_success["allow_apply_to_runtime"] is False
    assert all(case["preservation_decision"] == "PRESERVE_BEFORE_UPGRADE" for case in known_success["protected_cases"])

    rollback = _load(artifacts["rollback_validation_report"])
    assert rollback["rollback_validation_status"] == "ROLLBACK_VALID"
    assert rollback["checks"]["runtime_apply_blocked"] is True
    assert rollback["checks"]["no_production_files_modified_by_phase09"] is True

    shadow = _load(artifacts["shadow_mode_plan"])
    assert shadow["shadow_mode_status"] == "SHADOW_MODE_REQUIRED"
    assert shadow["runtime_apply_allowed"] is False
    assert shadow["broadcast_allowed"] is False
    assert shadow["signing_allowed"] is False

    regression = _load(artifacts["regression_validation_report"])
    assert regression["known_success_status"] == "KNOWN_SUCCESS_PRESERVED"
    assert regression["rollback_validation_status"] == "ROLLBACK_VALID"
    assert regression["shadow_mode_status"] == "SHADOW_MODE_REQUIRED"

    package = _load(artifacts["rule_update_package"])
    assert package["package_status"] == "UPGRADE_PACKAGE_READY"
    assert package["regression_status"] == "REGRESSION_TEST_PASS"
    assert package["requires_manual_confirmation"] is True
    assert package["allow_apply_to_runtime"] is False
    assert package["rollback_plan"].endswith("rollback_plan.md")

    handoff_out = _load(artifacts["handoff_packet"])
    assert handoff_out["system_upgrade_status"] == "SYSTEM_UPGRADE_READY"
    assert handoff_out["requires_manual_confirmation"] is True
    assert handoff_out["allow_apply_to_runtime"] is False
    assert handoff_out["recommended_apply_mode"] == "SHADOW_MODE_FIRST"


def test_phase09_exposes_phase08_evidence_chain_in_validation_package_and_handoff(tmp_path: Path):
    handoff = _phase08_package(tmp_path)
    result = Phase09SystemUpgradeController().run(phase08_handoff_file=handoff, output_dir=tmp_path / "out")

    validation = _load(result["artifacts"]["upgrade_input_validation"])
    assert "evidence_chain_manifest" in validation["loaded_inputs"]

    evidence = _load(result["artifacts"]["evidence_strength_review"])
    assert evidence["phase08_evidence_chain_status"] == "EVIDENCE_CHAIN_COMPLETE"
    assert evidence["phase08_evidence_chain_links"]
    assert evidence["absolute_conclusion_allowed"] is False

    package = _load(result["artifacts"]["rule_update_package"])
    assert package["source_phase08_evidence_chain_status"] == "EVIDENCE_CHAIN_COMPLETE"
    assert package["source_phase08_evidence_chain_manifest"].endswith("evidence_chain_manifest.json")

    handoff_out = _load(result["artifacts"]["handoff_packet"])
    assert handoff_out["evidence_chain_status"] == "EVIDENCE_CHAIN_COMPLETE"
    assert handoff_out["required_files_for_next_stage"]["evidence_chain_manifest"].endswith("evidence_chain_manifest.json")


def test_phase09_handoff_exposes_regression_shadow_rollback_and_known_success_artifacts(tmp_path: Path):
    handoff = _phase08_package(tmp_path)
    result = Phase09SystemUpgradeController().run(phase08_handoff_file=handoff, output_dir=tmp_path / "out")
    handoff_out = _load(result["artifacts"]["handoff_packet"])

    required = handoff_out["required_files_for_next_stage"]
    for key in [
        "known_success_preservation_review",
        "regression_validation_report",
        "shadow_mode_plan",
        "rollback_validation_report",
        "rollback_plan",
        "rule_update_package",
        "system_upgrade_manifest",
    ]:
        assert key in required
        assert Path(required[key]).exists(), key

    known_success = _load(required["known_success_preservation_review"])
    assert known_success["protected_cases"]
    assert known_success["regression_fixture_required"] is True

    regression = _load(required["regression_validation_report"])
    assert regression["known_success_case_count"] == known_success["known_success_case_count"]
    assert regression["shadow_mode_status"] == "SHADOW_MODE_REQUIRED"
    assert regression["rollback_validation_status"] == "ROLLBACK_VALID"


def test_phase09_blocks_missing_phase08_handoff_without_fabricating_package(tmp_path: Path):
    missing_handoff = tmp_path / "missing" / "phase_08_handoff_packet.json"
    result = Phase09SystemUpgradeController().run(phase08_handoff_file=missing_handoff, output_dir=tmp_path / "out")
    assert result["status"] == "SYSTEM_UPGRADE_BLOCKED"
    validation = _load(result["artifacts"]["upgrade_input_validation"])
    assert validation["input_status"] == "PHASE_09_INPUT_BLOCKED"
    assert "phase_08_handoff_packet_missing" in validation["block_reasons"]
    package = _load(result["artifacts"]["rule_update_package"])
    assert package["package_status"] == "UPGRADE_PACKAGE_REJECTED"
    assert package["approved_rule_updates"] == []
    handoff = _load(result["artifacts"]["handoff_packet"])
    assert handoff["handoff_status"] == "HANDOFF_BLOCKED"
    assert handoff["allow_apply_to_runtime"] is False


def test_phase09_rejects_candidates_without_target_phase_or_evidence_cases(tmp_path: Path):
    handoff = _phase08_package(tmp_path, invalid_candidate=True)
    result = Phase09SystemUpgradeController().run(phase08_handoff_file=handoff, output_dir=tmp_path / "out")
    validation = _load(result["artifacts"]["upgrade_input_validation"])
    assert validation["input_status"] == "PHASE_09_INPUT_BLOCKED"
    assert any("evidence_cases" in reason for reason in validation["block_reasons"])
    review = _load(result["artifacts"]["rule_update_review"])
    assert review["rule_reviews"]
    assert all(r["review_decision"] in {"REJECT_UPDATE", "HOLD_FOR_MORE_DATA"} for r in review["rule_reviews"])
    package = _load(result["artifacts"]["rule_update_package"])
    assert package["package_status"] == "UPGRADE_PACKAGE_REJECTED"


def test_phase09_degrades_optional_missing_and_holds_thresholds_for_more_data(tmp_path: Path):
    handoff = _phase08_package(tmp_path, optional_missing=True)
    result = Phase09SystemUpgradeController().run(phase08_handoff_file=handoff, output_dir=tmp_path / "out")
    validation = _load(result["artifacts"]["upgrade_input_validation"])
    assert validation["input_status"] == "PHASE_09_INPUT_DEGRADED"
    assert "scenario_case_library" in validation["missing_optional_inputs"]
    threshold = _load(result["artifacts"]["threshold_calibration_review"])
    assert threshold["threshold_reviews"]
    assert all(r["calibration_decision"] in {"HOLD_FOR_MORE_DATA", "SHADOW_MODE_REQUIRED", "ACCEPT_FOR_REGRESSION"} for r in threshold["threshold_reviews"])
    assert all(r["direct_threshold_change_allowed"] is False for r in threshold["threshold_reviews"])


def test_phase09_regression_failure_blocks_applicable_upgrade_package(tmp_path: Path):
    handoff = _phase08_package(tmp_path, regression_should_fail=True)
    result = Phase09SystemUpgradeController().run(phase08_handoff_file=handoff, output_dir=tmp_path / "out")
    regression = _load(result["artifacts"]["regression_validation_report"])
    assert regression["regression_status"] == "REGRESSION_TEST_FAIL"
    assert regression["decision"] == "UPGRADE_BLOCKED"
    package = _load(result["artifacts"]["rule_update_package"])
    assert package["package_status"] == "UPGRADE_PACKAGE_REJECTED"
    assert package["allow_apply_to_runtime"] is False
    handoff = _load(result["artifacts"]["handoff_packet"])
    assert handoff["system_upgrade_status"] == "SYSTEM_UPGRADE_BLOCKED"


def test_phase09_static_contract_schema_controller_files_exist():
    root = Path("/root/sikk-gmgn")
    required = [
        root / "research_loop/phase_09_system_upgrade_layer/README.md",
        root / "contracts/stable_trader_os/phase_09_system_upgrade/phase_09_input_contract.json",
        root / "contracts/stable_trader_os/phase_09_system_upgrade/phase_09_output_contract.json",
        root / "contracts/stable_trader_os/phase_09_system_upgrade/required_fields.md",
        root / "contracts/stable_trader_os/phase_09_system_upgrade/handoff_rules.md",
        root / "schemas/stable_trader_os/phase_09_system_upgrade/upgrade_candidate_classification.schema.json",
        root / "schemas/stable_trader_os/phase_09_system_upgrade/rule_update_package.schema.json",
        root / "schemas/stable_trader_os/phase_09_system_upgrade/phase_09_handoff_packet.schema.json",
        root / "configs/stable_trader_os/phase_09_system_upgrade/phase_09_status_codes.json",
        root / "modules/stable_trader_os/phase_09_system_upgrade_controller/runner.py",
        root / "skills/sikk_stable_trader_os/phase_controllers/phase_09_system_upgrade_controller.md",
    ]
    missing = [str(p) for p in required if not p.exists() or p.stat().st_size == 0]
    assert not missing
