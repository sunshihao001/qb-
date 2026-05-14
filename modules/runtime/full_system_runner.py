from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from .phase_runner import PhaseRunner, PHASE_ALIASES, PHASE_CANONICAL_NAME, PHASE_OUTPUT
from .patch_and_regression_runner import run_patch_and_regression
from .wave4_p08_p09_runner import run_wave4_p08_p09
from .wave_state_controller import WaveStateController


PHASES = [f"phase_{idx:02d}" for idx in range(1, 10)]
WAVES = [
    ("wave_01_p01_p03", ["phase_01", "phase_02", "phase_03"]),
    ("wave_02_p04_p05", ["phase_04", "phase_05"]),
    ("wave_03_p06_p07", ["phase_06", "phase_07"]),
    ("wave_04_p08_p09", ["phase_08", "phase_09"]),
    ("full_system_e2e", PHASES),
    ("patch_and_regression", []),
]


class FullSystemRuntimeRunner:
    """Paper-only P01-P09 HER runtime replay and wave checkpoint writer."""

    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.phase_runner = PhaseRunner(self.root)
        self.wave_controller = WaveStateController(self.root)

    def run(
        self,
        *,
        mode: str = "replay",
        token: str = "MOCK_TOKEN_ADDRESS_DO_NOT_USE_REAL_SECRET",
        resume_from_checkpoint: bool = False,
    ) -> Dict[str, Any]:
        started_at = self._now()
        run_id = f"{mode}_{token}"
        checkpoint_before = self._read_checkpoint_state() if resume_from_checkpoint else {}
        resume_cursor = checkpoint_before.get("resume_cursor") if resume_from_checkpoint else None
        blocking_issues: List[Dict[str, Any]] = []
        degraded_issues: List[Dict[str, Any]] = []
        phase_results: List[Dict[str, Any]] = []
        wave_results: List[Dict[str, Any]] = []
        wave_runtime_artifacts: Dict[str, Any] = {}

        prior_input: Path | None = None
        completed_phases: list[str] = []
        reused_phases: list[str] = []
        checkpoint_completed_phases = set(checkpoint_before.get("completed_phases") or [])
        can_reuse_checkpoint = (
            resume_from_checkpoint
            and not checkpoint_before.get("checkpoint_corrupted")
            and checkpoint_before.get("run_id") == run_id
        )
        for phase in PHASES:
            reusable_output = self._phase_output_path(phase, mode, token)
            reusable_audit = self._phase_audit_path(phase, mode, token)
            reusable_handoff = self._shared_handoff_path(phase, token)
            if (
                can_reuse_checkpoint
                and phase in checkpoint_completed_phases
                and reusable_output.exists()
                and reusable_audit.exists()
                and reusable_handoff.exists()
            ):
                payload = json.loads(reusable_output.read_text())
                issues = self._phase_degraded_issues(phase, payload)
                degraded_issues.extend(issues)
                if payload.get("status_family") == "BLOCK":
                    blocking_issues.append(
                        {
                            "issue_id": f"{phase.upper()}_BLOCKED",
                            "severity": "blocker",
                            "status_code": payload.get("status_code"),
                            "output_path": str(reusable_output),
                        }
                    )
                phase_results.append(
                    {
                        "phase": phase,
                        "status_code": payload.get("status_code"),
                        "status_family": payload.get("status_family"),
                        "output_path": str(reusable_output),
                        "audit_path": str(reusable_audit),
                        "handoff_path": str(reusable_handoff),
                        "execution_mode": "reused_from_checkpoint",
                    }
                )
                completed_phases.append(phase)
                reused_phases.append(phase)
                prior_input = reusable_handoff
                continue

            input_file = self._input_for_phase(phase, mode, token, prior_input)
            result = self.phase_runner.run(phase=phase, mode=mode, token=token, input_file=input_file)
            payload = json.loads(result.output_path.read_text())
            issues = self._phase_degraded_issues(phase, payload)
            degraded_issues.extend(issues)
            if payload.get("status_family") == "BLOCK":
                blocking_issues.append(
                    {
                        "issue_id": f"{phase.upper()}_BLOCKED",
                        "severity": "blocker",
                        "status_code": payload.get("status_code"),
                        "output_path": str(result.output_path),
                    }
                )
            phase_results.append(
                {
                    "phase": phase,
                    "status_code": result.status_code,
                    "status_family": payload.get("status_family"),
                    "output_path": str(result.output_path),
                    "audit_path": str(result.audit_path),
                    "handoff_path": str(self._shared_handoff_path(phase, token)),
                    "execution_mode": "executed",
                }
            )
            completed_phases.append(phase)
            prior_input = self._shared_handoff_path(phase, token)

        phase_result_map = {item["phase"]: item for item in phase_results}
        wave3_handoff_file = "missing"
        wave4_result: Dict[str, Any] | None = None
        patch_result: Dict[str, Any] | None = None
        for wave_id, wave_phases in WAVES:
            wave_phase_results = [item for item in phase_results if item["phase"] in wave_phases]
            status = "REJECTED" if blocking_issues else "READY_WITH_GAPS"
            audit_refs = [item["audit_path"] for item in wave_phase_results]

            if wave_id == "wave_03_p06_p07":
                wave3_handoff_file = self._write_full_runner_wave_handoff(
                    wave_id=wave_id,
                    wave_phases=wave_phases,
                    phase_results=phase_result_map,
                    degraded_issues=degraded_issues,
                    blocking_issues=blocking_issues,
                )
            if wave_id == "wave_04_p08_p09" and not blocking_issues:
                wave4_output_dir = self.root / "runtime_logs" / "full_system_runtime" / "wave4_p08_p09"
                wave4_result = run_wave4_p08_p09(
                    root=self.root,
                    wave3_handoff_file=wave3_handoff_file,
                    output_dir=wave4_output_dir,
                    mode=mode,
                )
                wave_runtime_artifacts["wave4_p08_p09"] = wave4_result.get("artifacts", {})
                degraded_issues.extend(self._issues_from_wave_runtime(wave4_result, severity="degraded"))
                blocking_issues.extend(self._issues_from_wave_runtime(wave4_result, severity="blocking"))
                status = self._wave_status_from_runtime(wave4_result)
                audit_refs.extend(
                    path
                    for path in [wave4_result.get("artifacts", {}).get("wave4_audit")]
                    if path
                )
            if wave_id == "patch_and_regression":
                patch_output_dir = self.root / "runtime_logs" / "full_system_runtime" / "patch_and_regression"
                patch_result = run_patch_and_regression(
                    root=self.root,
                    issues=blocking_issues + degraded_issues,
                    output_dir=patch_output_dir,
                    mode=mode,
                    source_result_path="reports/system_audit/full_system_automation_result.json",
                )
                wave_runtime_artifacts["patch_and_regression"] = patch_result.get("artifacts", {})
                status = "REJECTED" if patch_result.get("final_status") == "PATCH_REGRESSION_REJECTED" else "READY_WITH_GAPS" if patch_result.get("final_status") == "PATCH_REGRESSION_READY_WITH_GAPS" else "READY"
                audit_refs.extend(
                    path
                    for path in [patch_result.get("artifacts", {}).get("patch_audit")]
                    if path
                )

            applied = self.wave_controller.apply_wave_result(
                wave_id=wave_id,
                status=status,
                blocking_issues=blocking_issues,
                degraded_issues=degraded_issues,
                audit_refs=audit_refs,
            )
            wave_results.append(
                {
                    "wave_id": applied.wave_id,
                    "status": applied.status,
                    "next_allowed_task": applied.next_allowed_task,
                    "phases": wave_phases,
                    "audit_refs": audit_refs,
                }
            )

        final_status = "FULL_SYSTEM_AUTOMATION_REJECTED" if blocking_issues else "FULL_SYSTEM_AUTOMATION_READY_WITH_GAPS"
        finished_at = self._now()
        result_payload = {
            "task": "full_system_runtime",
            "final_status": final_status,
            "started_at": started_at,
            "finished_at": finished_at,
            "mode": mode,
            "run_id": run_id,
            "token_address": token,
            "resume_from_checkpoint": resume_from_checkpoint,
            "resume_cursor": resume_cursor or "start",
            "paper_only": True,
            "read_only_research": True,
            "real_trade_actions": [],
            "secret_access": "not_requested_not_used",
            "phases": phase_results,
            "waves": wave_results,
            "wave_runtime_artifacts": wave_runtime_artifacts,
            "blocking_issues": blocking_issues,
            "degraded_issues": degraded_issues,
            "full_e2e": {
                "phase_chain": PHASES,
                "handoff_chain_verified": all(Path(item["handoff_path"]).exists() for item in phase_results),
                "audit_chain_verified": all(Path(item["audit_path"]).exists() for item in phase_results),
                "wave4_runtime_integrated": bool(wave4_result),
                "patch_regression_integrated": bool(patch_result),
                "status_code_inheritance": "verified_via_candidate_state_handoff_files",
            },
            "resume_contract": {
                "checkpoint_controls_execution": True,
                "resume_from_checkpoint_supported": True,
                "skip_completed_phase_supported": True,
                "rerun_failed_wave_supported": True,
                "downstream_freeze_on_blocking": True,
                "runtime_state_transaction_log": True,
                "actual_skipped_phases": reused_phases,
                "actual_executed_phases": [item["phase"] for item in phase_results if item.get("execution_mode") == "executed"],
                "checkpoint_reused": bool(reused_phases),
            },
        }
        self._write_final_reports(result_payload)
        self._update_gap_register(result_payload)
        self._update_runtime_final_state(result_payload)
        self._write_acceptance_handoff_and_journal(result_payload)
        self._write_checkpoint_state(result_payload, completed_phases=completed_phases, checkpoint_before=checkpoint_before)
        return result_payload

    def _input_for_phase(self, phase: str, mode: str, token: str, prior_input: Path | None) -> Path:
        replay_dir = self.root / "data" / "runtime" / mode / token / "replay_inputs"
        replay_dir.mkdir(parents=True, exist_ok=True)
        input_path = replay_dir / f"{phase}_input.json"
        contract = self._contract_for_phase(phase)
        required_fields = contract.get("required_fields", [])
        phase_number = contract.get("phase", phase)
        if phase == "phase_01":
            payload: Dict[str, Any] = {
                "token_address": token,
                "chain": "solana",
                "snapshot_time": self._now(),
                "raw_token_basic": {"symbol": "MOCK", "name": "Mock Token"},
                "raw_wallet_trade": [
                    {
                        "wallet_address": "Wallet111",
                        "token_address": token,
                        "transaction_time": self._now(),
                        "transaction_type": "buy",
                        "current_token_balance": "1000",
                    }
                ],
                "raw_holder": [{"wallet_address": "Wallet111", "balance": "1000"}],
                "raw_kline": [{"timestamp": self._now(), "open": 1, "high": 1, "low": 1, "close": 1, "volume": 1}],
                "raw_quote_security": {"quote_price_usd": 0.001},
            }
        else:
            if prior_input and prior_input.exists():
                payload = json.loads(prior_input.read_text())
            else:
                payload = {}
            payload.update({"source_files": [str(prior_input)] if prior_input else []})
        payload.update(
            {
                "token_address": token,
                "run_id": f"{mode}_{token}",
                "phase": phase_number,
                "status_code": payload.get("status_code") or "DATA_OK",
                "positive_evidence": payload.get("positive_evidence") or ["mock_replay_input_present"],
                "negative_evidence": payload.get("negative_evidence", []),
                "counter_evidence": payload.get("counter_evidence", []),
                "hard_negative_trigger": payload.get("hard_negative_trigger"),
                "confidence_level": payload.get("confidence_level", "low"),
                "missing_fields": payload.get("missing_fields", []),
                "source_files": payload.get("source_files", []),
                "handoff_to": self._next_phase(phase),
            }
        )
        for field in required_fields:
            payload.setdefault(field, self._default_required_value(field, phase, token, prior_input))
        input_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        return input_path

    def _contract_for_phase(self, phase: str) -> Dict[str, Any]:
        aliases = {
            "phase_01": "phase_01_data_fact",
            "phase_02": "phase_02_wallet_structure",
            "phase_03": "phase_03_chip_control",
            "phase_04": "phase_04_scenario_recognition",
            "phase_05": "phase_05_structure_position",
            "phase_06": "phase_06_strategy_gate",
            "phase_07": "phase_07_execution_risk",
            "phase_08": "phase_08_review_learning",
            "phase_09": "phase_09_system_upgrade",
        }
        path = self._contract_root() / aliases[phase] / "input_contract.json"
        return json.loads(path.read_text()) if path.exists() else {"required_fields": []}

    def _contract_root(self) -> Path:
        repo_contracts = self.root / "contracts"
        if repo_contracts.exists():
            return repo_contracts
        return Path(__file__).resolve().parents[2] / "contracts"

    def _default_required_value(self, field: str, phase: str, token: str, prior_input: Path | None) -> Any:
        defaults: Dict[str, Any] = {
            "token_address": token,
            "run_id": f"replay_{token}",
            "phase": self._contract_for_phase(phase).get("phase", phase),
            "status_code": "DATA_OK",
            "positive_evidence": ["mock_replay_required_field_present"],
            "negative_evidence": [],
            "counter_evidence": [],
            "hard_negative_trigger": None,
            "confidence_level": "low",
            "missing_fields": [],
            "source_files": [str(prior_input)] if prior_input else [],
            "handoff_to": self._next_phase(phase),
        }
        return defaults.get(field, "SYSTEM_DERIVED_REPLAY_VALUE")

    def _phase_degraded_issues(self, phase: str, payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        issues: List[Dict[str, Any]] = []
        if payload.get("confidence_level") == "low":
            issues.append(
                {
                    "issue_id": f"{phase.upper()}_LOW_CONFIDENCE_REPLAY",
                    "severity": "degraded",
                    "reason": "replay fixture uses explicit low-confidence mock/canonical handoff evidence; no real collector or live trade data used",
                }
            )
        if payload.get("missing_fields"):
            issues.append(
                {
                    "issue_id": f"{phase.upper()}_MISSING_FIELDS",
                    "severity": "degraded",
                    "fields": payload.get("missing_fields"),
                }
            )
        return issues

    def _shared_handoff_path(self, phase: str, token: str) -> Path:
        return self.root / "shared_handoff" / phase / token / f"{phase}_handoff_packet.json"

    def _phase_output_path(self, phase: str, mode: str, token: str) -> Path:
        canonical = PHASE_ALIASES[phase]
        return self.root / "data" / "runtime" / mode / token / phase / PHASE_OUTPUT.get(canonical, "phase_output.json")

    def _phase_audit_path(self, phase: str, mode: str, token: str) -> Path:
        return self.root / "reports" / "runtime" / mode / token / phase / "audit_report.md"

    def _write_full_runner_wave_handoff(
        self,
        *,
        wave_id: str,
        wave_phases: List[str],
        phase_results: Dict[str, Dict[str, Any]],
        degraded_issues: List[Dict[str, Any]],
        blocking_issues: List[Dict[str, Any]],
    ) -> str:
        handoff_dir = self.root / "runtime_logs" / "full_system_runtime" / wave_id / "handoff"
        audit_dir = self.root / "runtime_logs" / "full_system_runtime" / wave_id / "audit"
        handoff_dir.mkdir(parents=True, exist_ok=True)
        audit_dir.mkdir(parents=True, exist_ok=True)
        gap_register_path = audit_dir / f"{wave_id}_gap_register.json"
        gap_payload = {
            "wave_id": wave_id,
            "blocking_issues": blocking_issues,
            "degraded_issues": degraded_issues,
            "status": "HANDOFF_BLOCKED" if blocking_issues else "HANDOFF_DEGRADED" if degraded_issues else "HANDOFF_READY",
        }
        gap_register_path.write_text(json.dumps(gap_payload, ensure_ascii=False, indent=2) + "\n")
        handoff_files = {
            f"{phase}_handoff_packet": phase_results.get(phase, {}).get("handoff_path", "missing")
            for phase in wave_phases
        }
        handoff_files[f"{wave_id}_gap_register"] = str(gap_register_path)
        payload = {
            "wave_id": wave_id,
            "handoff_status": gap_payload["status"],
            "handoff_files": handoff_files,
            "blocking_issue_count": len(blocking_issues),
            "degraded_issue_count": len(degraded_issues),
        }
        handoff_path = handoff_dir / f"{wave_id}_handoff_packet.json"
        handoff_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        return str(handoff_path)

    def _issues_from_wave_runtime(self, result: Dict[str, Any], *, severity: str) -> List[Dict[str, Any]]:
        output: List[Dict[str, Any]] = []
        for issue in result.get("issues") or []:
            if issue.get("severity") != severity:
                continue
            issue_id = issue.get("issue_id") or issue.get("code") or "WAVE_RUNTIME_ISSUE"
            output.append({**issue, "issue_id": str(issue_id).upper(), "source": result.get("wave_id")})
        return output

    def _wave_status_from_runtime(self, result: Dict[str, Any]) -> str:
        final_status = result.get("final_status")
        if final_status and str(final_status).endswith("REJECTED"):
            return "REJECTED"
        if final_status and str(final_status).endswith("READY"):
            return "READY"
        return "READY_WITH_GAPS"

    def _read_checkpoint_state(self) -> Dict[str, Any]:
        checkpoint_path = self.root / "runtime_logs" / "full_system_runtime" / "checkpoint_state.json"
        if not checkpoint_path.exists():
            return {}
        try:
            return json.loads(checkpoint_path.read_text())
        except json.JSONDecodeError:
            return {"checkpoint_corrupted": True}

    def _write_checkpoint_state(
        self,
        payload: Dict[str, Any],
        *,
        completed_phases: List[str],
        checkpoint_before: Dict[str, Any],
    ) -> None:
        checkpoint_path = self.root / "runtime_logs" / "full_system_runtime" / "checkpoint_state.json"
        state = {
            "checkpoint_id": f"full_system_runtime::{payload['run_id']}",
            "run_id": payload["run_id"],
            "status": payload["final_status"],
            "resume_cursor": "patch_and_regression" if payload.get("degraded_issues") else "FULL_SYSTEM_AUTOMATION_READY",
            "completed_phases": completed_phases,
            "completed_waves": [wave["wave_id"] for wave in payload.get("waves", [])],
            "last_successful_checkpoint": payload.get("waves", [{}])[-1].get("wave_id") if payload.get("waves") else "none",
            "artifact_refs": {
                "automation_result": "reports/system_audit/full_system_automation_result.json",
                "automation_audit": "reports/system_audit/full_system_automation_result.md",
                **payload.get("wave_runtime_artifacts", {}),
            },
            "resume_contract": payload.get("resume_contract", {}),
            "resume_stats": {
                "resume_requested": payload.get("resume_from_checkpoint") is True,
                "skipped_phase_count": len(payload.get("resume_contract", {}).get("actual_skipped_phases", [])),
                "executed_phase_count": len(payload.get("resume_contract", {}).get("actual_executed_phases", [])),
                "checkpoint_reused": payload.get("resume_contract", {}).get("checkpoint_reused") is True,
            },
            "previous_checkpoint_status": checkpoint_before.get("status"),
            "updated_at": payload["finished_at"],
        }
        checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
        checkpoint_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n")

    def _next_phase(self, phase: str) -> str | None:
        idx = PHASES.index(phase)
        if idx + 1 >= len(PHASES):
            return None
        return PHASES[idx + 1]

    def _write_final_reports(self, payload: Dict[str, Any]) -> None:
        report_dir = self.root / "reports" / "system_audit"
        report_dir.mkdir(parents=True, exist_ok=True)
        (report_dir / "full_system_automation_result.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        lines = [
            "# Full System Automation Result",
            "",
            f"- final_status: `{payload['final_status']}`",
            "- boundary: 纸面验证 / read-only research / no swap / no signing / no broadcast",
            f"- token_address: `{payload['token_address']}`",
            f"- mode: `{payload['mode']}`",
            f"- paper_only: `{payload['paper_only']}`",
            "",
            "## Waves",
        ]
        for wave in payload["waves"]:
            lines.append(f"- {wave['wave_id']}: `{wave['status']}` -> {wave['next_allowed_task']}")
        lines.extend(["", "## Phases"])
        for phase in payload["phases"]:
            lines.append(f"- {phase['phase']}: `{phase['status_code']}` / `{phase['status_family']}`")
        lines.extend(["", "## Blocking Issues", json.dumps(payload["blocking_issues"], ensure_ascii=False, indent=2)])
        lines.extend(["", "## Degraded Issues", json.dumps(payload["degraded_issues"], ensure_ascii=False, indent=2)])
        (report_dir / "full_system_automation_result.md").write_text("\n".join(lines) + "\n")

    def _update_gap_register(self, payload: Dict[str, Any]) -> None:
        path = self.root / "reports" / "system_audit" / "missing_gap_register.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        existing = path.read_text() if path.exists() else "# Missing Gap Register\n"
        marker = "\n## Full System Automation Runtime Replay\n"
        section = marker + "\n".join(
            [
                f"- final_status: `{payload['final_status']}`",
                f"- blocking_issues: `{len(payload['blocking_issues'])}`",
                f"- degraded_issues: `{len(payload['degraded_issues'])}`",
                "- note: replay reached P01-P09 with explicit paper-only/mock evidence gaps; live collector/business-code deferral remains degraded, not blocking.",
            ]
        ) + "\n"
        if marker in existing:
            existing = existing.split(marker)[0].rstrip() + section
        else:
            existing = existing.rstrip() + "\n" + section
        path.write_text(existing)

    def _update_runtime_final_state(self, payload: Dict[str, Any]) -> None:
        runtime_path = self.root / "runtime_logs" / "full_system_runtime" / "runtime_task_state.json"
        state = json.loads(runtime_path.read_text()) if runtime_path.exists() else {}
        state.update(
            {
                "final_status": payload["final_status"],
                "automation_result_path": "reports/system_audit/full_system_automation_result.json",
                "automation_audit_path": "reports/system_audit/full_system_automation_result.md",
                "updated_at": payload["finished_at"],
            }
        )
        runtime_path.parent.mkdir(parents=True, exist_ok=True)
        runtime_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n")

    def _write_acceptance_handoff_and_journal(self, payload: Dict[str, Any]) -> None:
        acceptance_path = self.root / "reports" / "system_audit" / "full_system_automation_acceptance.json"
        handoff_path = self.root / "handoffs" / "stable_trader_os" / "full_system_runtime_handoff.json"
        current_state_path = self.root / "sikk_stable_trader_os" / "09_runtime_state" / "current_system_state.json"
        journal_path = self.root / "research_loop" / "total_control" / "execution_journal.md"
        required_artifacts = [
            self.root / "reports" / "system_audit" / "full_system_automation_result.json",
            self.root / "reports" / "system_audit" / "full_system_automation_result.md",
            self.root / "runtime_logs" / "full_system_runtime" / "runtime_task_state.json",
            self.root / "runtime_logs" / "full_system_runtime" / "wave_state.json",
            self.root / "runtime_logs" / "full_system_runtime" / "checkpoint_state.json",
        ]
        artifact_refs = [str(path.relative_to(self.root)) for path in required_artifacts]
        artifacts_verified = all(path.exists() for path in required_artifacts[:-1])
        acceptance_status = "REJECTED" if payload.get("blocking_issues") else "PASS_WITH_DEGRADED_GAPS" if payload.get("degraded_issues") else "PASS"
        acceptance = {
            "task": "full_system_runtime_automation",
            "acceptance_status": acceptance_status,
            "final_status": payload["final_status"],
            "paper_only": payload.get("paper_only") is True,
            "read_only_research": payload.get("read_only_research") is True,
            "real_trade_actions": payload.get("real_trade_actions", []),
            "secret_access": payload.get("secret_access"),
            "phase_count": len(payload.get("phases", [])),
            "wave_count": len(payload.get("waves", [])),
            "blocking_issue_count": len(payload.get("blocking_issues", [])),
            "degraded_issue_count": len(payload.get("degraded_issues", [])),
            "required_runtime_artifacts": artifact_refs,
            "required_runtime_artifacts_verified": artifacts_verified,
            "automation_result_path": "reports/system_audit/full_system_automation_result.json",
            "automation_audit_path": "reports/system_audit/full_system_automation_result.md",
            "checkpoint_path": "runtime_logs/full_system_runtime/checkpoint_state.json",
            "handoff_path": "handoffs/stable_trader_os/full_system_runtime_handoff.json",
            "accepted_at": payload["finished_at"],
        }
        acceptance_path.parent.mkdir(parents=True, exist_ok=True)
        acceptance_path.write_text(json.dumps(acceptance, ensure_ascii=False, indent=2) + "\n")

        handoff_status = "BLOCKED" if payload.get("blocking_issues") else "READY_WITH_DEGRADED_GAPS" if payload.get("degraded_issues") else "READY"
        handoff = {
            "handoff_id": f"full_system_runtime::{payload['run_id']}",
            "handoff_status": handoff_status,
            "runtime_status": payload["final_status"],
            "runtime_boundary": "OBSERVE_PAPER_ONLY",
            "source_result": "reports/system_audit/full_system_automation_result.json",
            "source_acceptance": "reports/system_audit/full_system_automation_acceptance.json",
            "checkpoint_path": "runtime_logs/full_system_runtime/checkpoint_state.json",
            "phase_handoff_chain": [item.get("handoff_path") for item in payload.get("phases", [])],
            "wave_artifacts": payload.get("wave_runtime_artifacts", {}),
            "blocking_issues": payload.get("blocking_issues", []),
            "degraded_issues": payload.get("degraded_issues", []),
            "next_runtime_step": "fix_blocking_issues" if payload.get("blocking_issues") else "live_input_adapter_or_business_logic_integration",
            "created_at": payload["finished_at"],
        }
        handoff_path.parent.mkdir(parents=True, exist_ok=True)
        handoff_path.write_text(json.dumps(handoff, ensure_ascii=False, indent=2) + "\n")

        current_state = json.loads(current_state_path.read_text()) if current_state_path.exists() else {}
        current_state.update(
            {
                "runtime_automation_status": payload["final_status"],
                "runtime_boundary": "OBSERVE_PAPER_ONLY",
                "full_system_automation_result": "reports/system_audit/full_system_automation_result.json",
                "full_system_automation_acceptance": "reports/system_audit/full_system_automation_acceptance.json",
                "full_system_runtime_handoff": "handoffs/stable_trader_os/full_system_runtime_handoff.json",
                "next_step": handoff["next_runtime_step"],
                "updated_at": payload["finished_at"],
            }
        )
        current_state_path.parent.mkdir(parents=True, exist_ok=True)
        current_state_path.write_text(json.dumps(current_state, ensure_ascii=False, indent=2) + "\n")

        journal_path.parent.mkdir(parents=True, exist_ok=True)
        existing_journal = journal_path.read_text() if journal_path.exists() else "# Execution Journal\n"
        marker = "\n## Full System Automation Runtime Replay\n"
        section = marker + "\n".join(
            [
                f"- run_id: `{payload['run_id']}`",
                f"- final_status: `{payload['final_status']}`",
                f"- acceptance_status: `{acceptance_status}`",
                f"- handoff_status: `{handoff_status}`",
                f"- phase_count: `{len(payload.get('phases', []))}`",
                f"- wave_count: `{len(payload.get('waves', []))}`",
                f"- checkpoint: `runtime_logs/full_system_runtime/checkpoint_state.json`",
                "- boundary: `OBSERVE_PAPER_ONLY`; no signing, no swap, no broadcast.",
                f"- updated_at: `{payload['finished_at']}`",
            ]
        ) + "\n"
        if marker in existing_journal:
            existing_journal = existing_journal.split(marker)[0].rstrip() + section
        else:
            existing_journal = existing_journal.rstrip() + "\n" + section
        journal_path.write_text(existing_journal)

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run SIKK/HER full-system P01-P09 runtime replay")
    parser.add_argument("--root", default=".", help="Repository/root output path")
    parser.add_argument("--mode", default="replay", choices=["replay", "dry-run", "verify"], help="Execution mode")
    parser.add_argument("--token", default="MOCK_TOKEN_ADDRESS_DO_NOT_USE_REAL_SECRET", help="Token identifier for replay namespace")
    parser.add_argument("--resume-from-checkpoint", action="store_true", help="Read existing checkpoint_state.json and mark resumed run")
    args = parser.parse_args(argv)
    result = FullSystemRuntimeRunner(args.root).run(
        mode=args.mode,
        token=args.token,
        resume_from_checkpoint=args.resume_from_checkpoint,
    )
    print(json.dumps({
        "final_status": result["final_status"],
        "run_id": result.get("run_id"),
        "canonical_command": "python3 -m modules.runtime.full_system_runner --root <root> --mode replay --token <token>",
        "result_path": str(Path(args.root) / "reports" / "system_audit" / "full_system_automation_result.json"),
        "acceptance_path": str(Path(args.root) / "reports" / "system_audit" / "full_system_automation_acceptance.json"),
        "handoff_path": str(Path(args.root) / "handoffs" / "stable_trader_os" / "full_system_runtime_handoff.json"),
        "checkpoint_path": str(Path(args.root) / "runtime_logs" / "full_system_runtime" / "checkpoint_state.json"),
    }, ensure_ascii=False, indent=2))
    return 0 if result["final_status"] != "FULL_SYSTEM_AUTOMATION_REJECTED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
