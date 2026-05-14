from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

REQUIRED_METADATA = [
    "planbook_id",
    "version",
    "status",
    "scope",
    "owner_layer",
    "source_type",
    "runtime_consumption",
    "control_plane_refs",
    "gap_policy",
    "audit_policy",
    "durable_cognition_policy",
    "safety_boundary",
]

ALLOWED_STATUSES = {
    "DRAFT",
    "ACTIVE_CONTROL_SURFACE",
    "RUNTIME_CONSUMABLE",
    "ARCHIVED",
    "REJECTED",
}

FORBIDDEN_EXECUTION_PATTERNS = [
    "private_key",
    "secret_key",
    "签名: 允许",
    "广播: 允许",
    "真实交易: 允许",
    "real trade: allowed",
    "signing: allowed",
    "broadcast: allowed",
    "execute_swap",
]


@dataclass
class PlanbookRepositoryPaths:
    root: Path

    @property
    def planbook_root(self) -> Path:
        return self.root / "research_loop" / "plan_books"

    @property
    def index_dir(self) -> Path:
        return self.planbook_root / "index"

    @property
    def index_path(self) -> Path:
        return self.index_dir / "planbook_index.json"

    @property
    def audit_dir(self) -> Path:
        return self.root / "reports" / "system_audit"

    @property
    def audit_path(self) -> Path:
        return self.audit_dir / "planbook_repository_validation.json"


class PlanbookRepository:
    """Runtime reader for SIKK/HER planbooks.

    This module makes trading-system design documents machine-readable and auditable.
    It never authorizes real trading, signing, broadcast, or secret access.
    """

    def __init__(self, root: str | Path):
        self.paths = PlanbookRepositoryPaths(Path(root))

    def validate(self) -> Dict[str, Any]:
        started_at = self._now()
        self._ensure_dirs()
        records = [self._read_planbook(path) for path in self._iter_planbooks()]
        gaps = self._collect_gaps(records)
        final_status = self._final_status(gaps)
        payload: Dict[str, Any] = {
            "module": "planbook_repository",
            "version": "v1.0",
            "started_at": started_at,
            "finished_at": self._now(),
            "final_status": final_status,
            "safety_boundary": {
                "paper_only": True,
                "signing_enabled": False,
                "broadcast_enabled": False,
                "real_trade_enabled": False,
                "secret_access": "not_requested_not_used",
            },
            "canonical_planbook_root": str(self.paths.planbook_root),
            "required_metadata": REQUIRED_METADATA,
            "planbooks": records,
            "gap_register": gaps,
        }
        self._write_outputs(payload)
        payload["index_path"] = str(self.paths.index_path)
        payload["audit_path"] = str(self.paths.audit_path)
        return payload

    def _ensure_dirs(self) -> None:
        for path in [self.paths.planbook_root / "active", self.paths.planbook_root / "draft", self.paths.planbook_root / "archived", self.paths.index_dir, self.paths.audit_dir]:
            path.mkdir(parents=True, exist_ok=True)

    def _iter_planbooks(self) -> Iterable[Path]:
        for subdir in ["active", "draft", "archived"]:
            yield from sorted((self.paths.planbook_root / subdir).glob("*.md"))

    def _read_planbook(self, path: Path) -> Dict[str, Any]:
        text = path.read_text(encoding="utf-8")
        metadata = self._parse_metadata(text)
        missing_metadata = [key for key in REQUIRED_METADATA if self._is_missing(metadata.get(key))]
        invalid_status = metadata.get("status") not in ALLOWED_STATUSES
        forbidden_hits = [pattern for pattern in FORBIDDEN_EXECUTION_PATTERNS if pattern.lower() in text.lower()]
        status = "PLANBOOK_READY"
        if forbidden_hits or metadata.get("status") == "REJECTED" or invalid_status:
            status = "PLANBOOK_REJECTED"
        elif missing_metadata:
            status = "PLANBOOK_READY_WITH_GAPS"
        return {
            "path": str(path),
            "relative_path": str(path.relative_to(self.paths.root)),
            "chars": len(text),
            "metadata": metadata,
            "missing_metadata": missing_metadata,
            "invalid_status": invalid_status,
            "forbidden_execution_patterns": forbidden_hits,
            "status": status,
        }

    def _parse_metadata(self, text: str) -> Dict[str, str]:
        metadata: Dict[str, str] = {}
        for line in text.splitlines()[:80]:
            match = re.match(r"^\s*-\s*([A-Za-z0-9_]+)\s*:\s*`?([^`]+?)`?\s*$", line)
            if match:
                metadata[match.group(1)] = match.group(2).strip()
        return metadata

    def _collect_gaps(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        gaps: List[Dict[str, Any]] = []
        if not records:
            gaps.append({
                "gap_id": "NO_PLANBOOKS_INDEXED",
                "severity": "degraded",
                "target": str(self.paths.planbook_root),
                "repair_route": "create planbook under research_loop/plan_books/active or draft",
            })
        for record in records:
            for key in record["missing_metadata"]:
                gaps.append({
                    "gap_id": f"PLANBOOK_MISSING_METADATA_{key.upper()}",
                    "severity": "degraded",
                    "target": record["relative_path"],
                    "repair_route": "fill required metadata or mark rejected explicitly",
                })
            if record["invalid_status"]:
                gaps.append({
                    "gap_id": "PLANBOOK_INVALID_STATUS",
                    "severity": "blocking",
                    "target": record["relative_path"],
                    "repair_route": "use allowed status value",
                })
            for pattern in record["forbidden_execution_patterns"]:
                gaps.append({
                    "gap_id": "PLANBOOK_FORBIDDEN_EXECUTION_PATTERN",
                    "severity": "blocking",
                    "target": record["relative_path"],
                    "pattern": pattern,
                    "repair_route": "remove real trading/signing/broadcast/secret authorization",
                })
        return gaps

    def _final_status(self, gaps: List[Dict[str, Any]]) -> str:
        if any(gap["severity"] == "blocking" for gap in gaps):
            return "PLANBOOK_REPOSITORY_REJECTED"
        if gaps:
            return "PLANBOOK_REPOSITORY_READY_WITH_GAPS"
        return "PLANBOOK_REPOSITORY_READY"

    def _write_outputs(self, payload: Dict[str, Any]) -> None:
        self.paths.index_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        self.paths.audit_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def _is_missing(self, value: Any) -> bool:
        return value is None or str(value).strip() in {"", "missing", "MISSING"}

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate SIKK/HER planbook repository")
    parser.add_argument("--root", default="/root/sikk-gmgn")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = PlanbookRepository(args.root).validate()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
