from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


RUNTIME_DIR = Path("runtime_logs/full_system_runtime")

WAVE_ORDER = [
    "wave_01_p01_p03",
    "wave_02_p04_p05",
    "wave_03_p06_p07",
    "wave_04_p08_p09",
    "full_system_e2e",
    "patch_and_regression",
]

NEXT_ALLOWED_TASK = {
    "wave_01_p01_p03": "WAVE_02_P04_P05_SCENARIO_POSITION_RUNTIME",
    "wave_02_p04_p05": "WAVE_03_P06_P07_STRATEGY_EXECUTION_RUNTIME",
    "wave_03_p06_p07": "WAVE_04_P08_P09_REVIEW_UPGRADE_RUNTIME",
    "wave_04_p08_p09": "FULL_SYSTEM_E2E_RUNTIME",
    "full_system_e2e": "PATCH_AND_REGRESSION_LOOP",
    "patch_and_regression": "FULL_SYSTEM_AUTOMATION_READY",
}

DEFAULT_WAVE_STATE = {
    "wave_01_p01_p03": "PENDING",
    "wave_02_p04_p05": "LOCKED",
    "wave_03_p06_p07": "LOCKED",
    "wave_04_p08_p09": "LOCKED",
    "full_system_e2e": "LOCKED",
    "patch_and_regression": "LOCKED",
}

READY_STATUSES = {"READY", "READY_WITH_GAPS"}
REJECTED_STATUSES = {"REJECTED"}
ALLOWED_STATUSES = READY_STATUSES | REJECTED_STATUSES | {"PENDING", "LOCKED", "RUNNING"}


@dataclass(frozen=True)
class WaveApplyResult:
    wave_id: str
    status: str
    next_allowed_task: str
    wave_state_path: Path
    runtime_state_path: Path


class WaveStateController:
    """Small runtime controller for full-system Wave lock/unlock state.

    It is intentionally file-based and deterministic so HER long tasks can
    checkpoint, resume, and audit without a database or background server.
    """

    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.runtime_dir = self.root / RUNTIME_DIR
        self.runtime_dir.mkdir(parents=True, exist_ok=True)

    @property
    def wave_state_path(self) -> Path:
        return self.runtime_dir / "wave_state.json"

    @property
    def runtime_state_path(self) -> Path:
        return self.runtime_dir / "runtime_task_state.json"

    @property
    def checkpoint_state_path(self) -> Path:
        return self.runtime_dir / "checkpoint_state.json"

    @property
    def blocking_issues_path(self) -> Path:
        return self.runtime_dir / "current_blocking_issues.json"

    @property
    def degraded_issues_path(self) -> Path:
        return self.runtime_dir / "current_degraded_issues.json"

    def apply_wave_result(
        self,
        wave_id: str,
        status: str,
        blocking_issues: Optional[List[Dict[str, Any]]] = None,
        degraded_issues: Optional[List[Dict[str, Any]]] = None,
        audit_refs: Optional[List[str]] = None,
    ) -> WaveApplyResult:
        if wave_id not in WAVE_ORDER:
            raise ValueError(f"unknown wave_id: {wave_id}")
        status = status.upper()
        if status not in ALLOWED_STATUSES:
            raise ValueError(f"unsupported wave status: {status}")

        blocking_issues = blocking_issues or []
        degraded_issues = degraded_issues or []
        audit_refs = audit_refs or []

        wave_state = self._load_json(self.wave_state_path, DEFAULT_WAVE_STATE.copy())
        for key, value in DEFAULT_WAVE_STATE.items():
            wave_state.setdefault(key, value)

        wave_state[wave_id] = status
        next_allowed_task = "FIX_CURRENT_BLOCKING_ISSUES"

        if status in READY_STATUSES and not blocking_issues:
            next_wave = self._next_wave(wave_id)
            if next_wave:
                # Only unlock the immediate downstream wave. If later waves were
                # previously completed by an older/full-system run, preserve that
                # audited state; otherwise keep them locked. This prevents a
                # mid-pipeline reconciliation from silently downgrading historical
                # Wave3/4/E2E/Patch states while still enforcing sequential unlocks.
                wave_state[next_wave] = "PENDING"
                for later in WAVE_ORDER[WAVE_ORDER.index(next_wave) + 1 :]:
                    wave_state.setdefault(later, "LOCKED")
            next_allowed_task = NEXT_ALLOWED_TASK[wave_id]
        elif status in REJECTED_STATUSES or blocking_issues:
            for later in WAVE_ORDER[WAVE_ORDER.index(wave_id) + 1 :]:
                wave_state[later] = "LOCKED"

        runtime_state = self._load_json(
            self.runtime_state_path,
            {
                "task": "full_system_runtime",
                "current_allowed_task": "WAVE_01_P01_P03_FOUNDATION_RUNTIME",
                "waves": DEFAULT_WAVE_STATE.copy(),
                "final_status": "FULL_SYSTEM_BUNDLE_READY_WITH_GAPS",
            },
        )
        runtime_state["waves"] = wave_state
        runtime_state["current_allowed_task"] = next_allowed_task
        runtime_state["next_allowed_task"] = next_allowed_task
        runtime_state["updated_at"] = self._now()
        runtime_state["blocking_issues"] = blocking_issues
        runtime_state["degraded_issues"] = degraded_issues
        runtime_state["last_wave_result"] = {
            "wave_id": wave_id,
            "status": status,
            "audit_refs": audit_refs,
            "updated_at": runtime_state["updated_at"],
        }

        checkpoint_state = self._load_json(self.checkpoint_state_path, {})
        checkpoint_state.update(
            {
                "task": "full_system_runtime",
                "updated_at": runtime_state["updated_at"],
                "last_successful_checkpoint": {
                    "checkpoint_id": f"{wave_id.upper()}_{status}",
                    "checkpoint_name": "wave_result_applied",
                    "status": status,
                    "audit_refs": audit_refs,
                    "completed_at": runtime_state["updated_at"],
                },
            }
        )

        self._write_json(self.wave_state_path, wave_state)
        self._write_json(self.runtime_state_path, runtime_state)
        self._write_json(self.checkpoint_state_path, checkpoint_state)
        self._write_json(self.blocking_issues_path, blocking_issues)
        self._write_json(self.degraded_issues_path, degraded_issues)

        return WaveApplyResult(
            wave_id=wave_id,
            status=status,
            next_allowed_task=next_allowed_task,
            wave_state_path=self.wave_state_path,
            runtime_state_path=self.runtime_state_path,
        )

    def _next_wave(self, wave_id: str) -> Optional[str]:
        idx = WAVE_ORDER.index(wave_id)
        if idx + 1 >= len(WAVE_ORDER):
            return None
        return WAVE_ORDER[idx + 1]

    def _load_json(self, path: Path, default: Any) -> Any:
        if not path.exists():
            return default
        try:
            return json.loads(path.read_text())
        except json.JSONDecodeError:
            return default

    def _write_json(self, path: Path, payload: Any) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()
