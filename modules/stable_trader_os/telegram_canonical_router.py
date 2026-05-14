"""Telegram canonical command router for SIKK Stable Trader OS.

Routes Telegram requests through the standard-stage closure manifest into the
selected phase runtime_entry and returns a paper-only reply panel. This module
must never call legacy runners directly and must never enable real execution.
"""
from __future__ import annotations

import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

FORBIDDEN_REAL_EXECUTION = ["swap", "private_key", "signing", "broadcast", "real_trade"]
ROUTE_CHAIN = [
    "telegram_command",
    "canonical_router",
    "standard_stage_closure_manifest",
    "runtime_entry",
    "acceptance_gate",
    "reply_panel",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _import_runtime(runtime_path: Path, phase_id: str):
    spec = importlib.util.spec_from_file_location(f"telegram_runtime_{phase_id.lower()}", runtime_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import runtime for {phase_id}: {runtime_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def route_telegram_command(command_packet: Dict[str, Any]) -> Dict[str, Any]:
    root = repo_root()
    phase_id = command_packet.get("phase_id", "K00")
    manifest_path = root / "system/stable_trader_os/standard_stage_closure/manifest.json"
    manifest = _load_json(manifest_path)
    phase_record = manifest["phases"][phase_id]
    runtime_path = root / phase_record["runtime_entry"]
    acceptance_path = root / phase_record["acceptance"]
    runtime_module = _import_runtime(runtime_path, phase_id)
    runtime_result = runtime_module.run({
        "run_id": command_packet.get("run_id", "TELEGRAM_CANONICAL_RUN"),
        "source": command_packet.get("source", "telegram"),
        "telegram_command": command_packet.get("command", "/sikk_stage_run"),
        "phase_id": phase_id,
        "source_artifact": "telegram_canonical_command_packet",
    })
    acceptance_gate = _load_json(acceptance_path)
    reply_panel = {
        "panel_id": f"TELEGRAM_REPLY_PANEL_{phase_id}_{command_packet.get('run_id', 'RUN')}",
        "phase_id": phase_id,
        "status": "PAPER_ONLY_STAGE_REPLY_READY",
        "runtime_mode": "paper_only",
        "real_execution_allowed": False,
        "blocked_real_execution": FORBIDDEN_REAL_EXECUTION,
        "semantic_acceptance_status": runtime_result.get("semantic_acceptance", {}).get("status"),
        "acceptance_depth": acceptance_gate.get("acceptance_depth"),
        "route_chain": ROUTE_CHAIN,
        "message": f"{phase_id} paper-only standard-stage runtime completed via canonical Telegram route.",
    }
    run_id = command_packet.get("run_id", "TELEGRAM_CANONICAL_RUN")
    out_dir = root / "data/stable_trader_os/telegram_canonical_router" / run_id / phase_id
    out_dir.mkdir(parents=True, exist_ok=True)
    rel_panel_path = out_dir.relative_to(root) / "reply_panel.json"
    (root / rel_panel_path).write_text(json.dumps(reply_panel, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "status": "TELEGRAM_CANONICAL_ROUTE_ACCEPTED_PAPER_ONLY",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "phase_id": phase_id,
        "route_chain": ROUTE_CHAIN,
        "manifest_path": str(manifest_path.relative_to(root)),
        "runtime_entry": phase_record["runtime_entry"],
        "acceptance_gate": phase_record["acceptance"],
        "runtime_result": runtime_result,
        "reply_panel": reply_panel,
        "reply_panel_path": str(rel_panel_path),
        "safety": {"paper_only": True, "forbidden_real_execution": FORBIDDEN_REAL_EXECUTION},
    }


__all__ = ["route_telegram_command", "ROUTE_CHAIN", "FORBIDDEN_REAL_EXECUTION"]
