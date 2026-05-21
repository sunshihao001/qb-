"""Run isolation helper for SIKK operating backbone.

This module is deliberately control-plane only. It creates and verifies isolated
run containers; it does not call GMGN, compute features, generate structure
signals, create decision tickets, or run replay/backtest/paper-only workflows.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
import json
from typing import Any, Dict, Iterable, List, Optional

DEFAULT_FORBIDDEN_SCOPE = [
    "gmgn_runtime_call",
    "feature_generation",
    "structure_signal_generation",
    "decision_ticket_generation",
    "replay_backtest_paper_only",
    "live",
    "swap",
    "private_key",
    "signing",
    "broadcast",
]


class RunIsolationError(RuntimeError):
    """Raised when isolated run artifacts are missing or unsafe."""


@dataclass
class RunContext:
    run_id: str
    run_name: str
    expected_backbone_node: str
    root: Path = Path("data/operating_backbone/runs")
    allowed_scope: List[str] = field(default_factory=list)
    forbidden_scope: List[str] = field(default_factory=lambda: DEFAULT_FORBIDDEN_SCOPE.copy())
    canonical_write_allowed: bool = False
    promotion_allowed: bool = False
    runtime_validation_allowed: bool = False

    @property
    def run_dir(self) -> Path:
        return self.root / self.run_id

    def to_manifest(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "run_name": self.run_name,
            "expected_backbone_node": self.expected_backbone_node,
            "run_dir": str(self.run_dir),
            "allowed_scope": self.allowed_scope,
            "forbidden_scope": self.forbidden_scope,
            "canonical_write_allowed": self.canonical_write_allowed,
            "promotion_allowed": self.promotion_allowed,
            "runtime_validation_allowed": self.runtime_validation_allowed,
            "created_at_utc": utc_now(),
            "status": "RUN_ISOLATED_EXECUTION",
        }


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json_yaml(path: Path, data: Dict[str, Any]) -> None:
    """Write JSON-compatible YAML-lite without requiring PyYAML."""
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def create_run_context(
    run_id: str,
    run_name: str,
    expected_backbone_node: str,
    allowed_scope: Optional[Iterable[str]] = None,
    forbidden_scope: Optional[Iterable[str]] = None,
    root: Path | str = Path("data/operating_backbone/runs"),
    exist_ok: bool = False,
) -> RunContext:
    """Create an isolated run directory with manifest and audit log.

    The default gates are intentionally closed: no canonical write, promotion, or
    runtime validation is allowed unless a later, explicit gate changes policy.
    """
    ctx = RunContext(
        run_id=run_id,
        run_name=run_name,
        expected_backbone_node=expected_backbone_node,
        root=Path(root),
        allowed_scope=list(allowed_scope or []),
        forbidden_scope=list(forbidden_scope or DEFAULT_FORBIDDEN_SCOPE),
    )
    ctx.run_dir.mkdir(parents=True, exist_ok=exist_ok)
    _write_json_yaml(ctx.run_dir / "run_manifest.yaml", ctx.to_manifest())
    append_audit(ctx, "run_context_created", {"expected_backbone_node": expected_backbone_node})
    return ctx


def append_audit(ctx: RunContext, event: str, payload: Optional[Dict[str, Any]] = None) -> None:
    ctx.run_dir.mkdir(parents=True, exist_ok=True)
    with (ctx.run_dir / "audit_log.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": utc_now(), "event": event, **(payload or {})}, ensure_ascii=False) + "\n")


def write_final_report(
    ctx: RunContext,
    status: str,
    acceptance: Dict[str, Any],
    outputs: Optional[List[str]] = None,
    gaps: Optional[List[str]] = None,
) -> Path:
    report = {
        "run_id": ctx.run_id,
        "run_name": ctx.run_name,
        "status": status,
        "validated_at_utc": utc_now(),
        "outputs": outputs or [],
        "acceptance": acceptance,
        "gaps": gaps or [],
        "forbidden_actions_executed": False,
        "promotion_performed": False,
    }
    path = ctx.run_dir / "final_run_report.yaml"
    _write_json_yaml(path, report)
    append_audit(ctx, "final_report_written", {"status": status})
    return path


def verify_run_context(run_dir: Path | str) -> Dict[str, Any]:
    run_dir = Path(run_dir)
    required = ["run_manifest.yaml", "audit_log.jsonl", "final_run_report.yaml"]
    missing = [name for name in required if not (run_dir / name).exists()]
    manifest_text = (run_dir / "run_manifest.yaml").read_text(encoding="utf-8") if (run_dir / "run_manifest.yaml").exists() else ""
    unsafe_flags = []
    for flag in ["canonical_write_allowed", "promotion_allowed", "runtime_validation_allowed"]:
        if f'"{flag}": true' in manifest_text.lower():
            unsafe_flags.append(flag)
    return {
        "run_dir": str(run_dir),
        "required": required,
        "missing": missing,
        "unsafe_flags": unsafe_flags,
        "status": "PASS" if not missing and not unsafe_flags else "PATCH_REQUIRED",
    }
