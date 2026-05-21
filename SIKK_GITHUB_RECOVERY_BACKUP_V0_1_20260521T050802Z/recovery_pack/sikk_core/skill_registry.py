"""Skill registry skeleton for SIKK operating backbone.

The registry validates skill contracts and invocation gates. It never invokes a
skill and never produces runtime strategy/validation artifacts.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
from typing import Any, Dict, List

REQUIRED_SKILL_FIELDS = [
    "skill_id",
    "skill_name",
    "owned_capability",
    "backbone_node",
    "input_artifacts",
    "output_artifacts",
    "downstream_consumers",
    "forbidden_scope",
    "maturity_status",
    "allowed_invocation_context",
]

FORBIDDEN_OUTPUT_TOKENS = ["BUY", "SELL", "EXECUTE", "LIVE_READY", "SWAP_READY", "PAPER_READY"]


@dataclass(frozen=True)
class SkillRecord:
    raw: Dict[str, Any]

    @property
    def skill_id(self) -> str:
        return str(self.raw.get("skill_id", "<unknown>"))

    def validate(self) -> List[str]:
        errors: List[str] = []
        for field in REQUIRED_SKILL_FIELDS:
            if field not in self.raw:
                errors.append(f"{self.skill_id}: missing {field}")
        if not self.raw.get("downstream_consumers"):
            errors.append(f"{self.skill_id}: missing downstream_consumers")
        if not self.raw.get("forbidden_scope"):
            errors.append(f"{self.skill_id}: missing forbidden_scope")
        outputs = " ".join(map(str, self.raw.get("output_artifacts", []))).upper()
        for token in FORBIDDEN_OUTPUT_TOKENS:
            if token in outputs:
                errors.append(f"{self.skill_id}: forbidden output token {token}")
        return errors


class SkillRegistry:
    def __init__(self, records: List[SkillRecord]):
        self.records = records
        self.by_id = {record.skill_id: record for record in records}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SkillRegistry":
        return cls([SkillRecord(item) for item in data.get("skills", [])])

    @classmethod
    def from_json_file(cls, path: Path | str) -> "SkillRegistry":
        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))

    def validate(self) -> Dict[str, Any]:
        errors: List[str] = []
        for record in self.records:
            errors.extend(record.validate())
        return {
            "status": "PASS" if not errors else "PATCH_REQUIRED",
            "skill_count": len(self.records),
            "errors": errors,
        }

    def invocation_allowed(self, skill_id: str, expected_backbone_node: str) -> Dict[str, Any]:
        record = self.by_id.get(skill_id)
        if record is None:
            return {"allowed": False, "reason": "skill_not_registered", "skill_id": skill_id}
        actual_node = record.raw.get("backbone_node")
        if actual_node != expected_backbone_node:
            return {
                "allowed": False,
                "reason": "backbone_node_mismatch",
                "skill_id": skill_id,
                "registered_node": actual_node,
                "expected_backbone_node": expected_backbone_node,
            }
        return {"allowed": True, "reason": "registered_and_node_matched", "skill_id": skill_id}


def validate_registry_file(path: Path | str) -> Dict[str, Any]:
    return SkillRegistry.from_json_file(path).validate()
