from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

STATUS_FAMILY = {
    "CONSTITUTION_READY": "ALLOW",
    "CONSTITUTION_GAP": "PAUSE",
    "CONSTITUTION_BLOCK": "BLOCK",
    "DATA_OK": "ALLOW",
    "DATA_WEAK": "PAUSE",
    "DATA_INVALID": "BLOCK",
    "WALLET_SUPPORT": "ALLOW",
    "WALLET_PAUSE": "PAUSE",
    "WALLET_BLOCK": "BLOCK",
    "CONTROL_RETAINED": "ALLOW",
    "CONTROL_WEAKENING": "PAUSE",
    "ACTIVE_DISTRIBUTION": "BLOCK",
    "STRUCTURE_COLLAPSE": "BLOCK",
    "SCENARIO_ALLOW": "ALLOW",
    "SCENARIO_PAUSE": "PAUSE",
    "SCENARIO_BLOCK": "BLOCK",
    "COMPLETION_PASS": "ALLOW",
    "COMPLETION_WAIT": "WAIT",
    "COMPLETION_FAIL": "BLOCK",
    "FATIGUE_BLOCK": "BLOCK",
    "STRATEGY_BLOCK": "BLOCK",
    "STRATEGY_PAUSE": "PAUSE",
    "PAPER_READY": "ALLOW",
    "READY_FOR_CONFIRMATION": "ALLOW",
    "EXECUTION_BLOCK": "BLOCK",
    "PAPER_EXECUTED": "ALLOW",
    "REVIEW_ONLY": "REVIEW_ONLY",
    "RULE_UPDATE_REQUIRED": "PAUSE",
    "MODEL_RECALIBRATION_REQUIRED": "PAUSE",
    "REVIEW_ARCHIVED": "ALLOW",
    "UPGRADE_PROPOSED": "PAUSE",
    "UPGRADE_REJECTED": "BLOCK",
    "UPGRADE_ACCEPTED": "ALLOW",
    "MODEL_RETIRED": "ALLOW",
}

CONFIDENCE_BY_FAMILY = {
    "ALLOW": "medium",
    "PAUSE": "low",
    "WAIT": "low",
    "BLOCK": "high",
    "REVIEW_ONLY": "low",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class CandidateState:
    token_address: str
    mode: str
    current_phase: str
    previous_phase: Optional[str]
    next_phase: Optional[str]
    status_code: str
    positive_evidence: List[Dict[str, Any]] = field(default_factory=list)
    negative_evidence: List[Dict[str, Any]] = field(default_factory=list)
    counter_evidence: List[Dict[str, Any]] = field(default_factory=list)
    hard_negative_trigger: Optional[str] = None
    invalidation_condition: str = "counter_evidence_or_hard_negative_triggered"
    confidence_level: Optional[str] = None
    missing_fields: List[str] = field(default_factory=list)
    gaps: List[str] = field(default_factory=list)
    audit_refs: List[str] = field(default_factory=list)
    source_refs: List[str] = field(default_factory=list)
    rule_version: str = "runtime_state_core_v1"
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)

    @property
    def status_family(self) -> str:
        return STATUS_FAMILY.get(self.status_code, "PAUSE")

    def to_dict(self) -> Dict[str, Any]:
        confidence = self.confidence_level or CONFIDENCE_BY_FAMILY.get(self.status_family, "low")
        return {
            "token_address": self.token_address,
            "mode": self.mode,
            "current_phase": self.current_phase,
            "previous_phase": self.previous_phase,
            "next_phase": self.next_phase,
            "status_code": self.status_code,
            "status_family": self.status_family,
            "positive_evidence": self.positive_evidence,
            "negative_evidence": self.negative_evidence,
            "counter_evidence": self.counter_evidence,
            "hard_negative_trigger": self.hard_negative_trigger,
            "invalidation_condition": self.invalidation_condition,
            "confidence_level": confidence,
            "missing_fields": self.missing_fields,
            "gaps": self.gaps,
            "audit_refs": self.audit_refs,
            "source_refs": self.source_refs,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "rule_version": self.rule_version,
        }


def create_candidate_state(**kwargs: Any) -> CandidateState:
    return CandidateState(**kwargs)
