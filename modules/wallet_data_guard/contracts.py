from __future__ import annotations

from enum import Enum


CANONICAL_WALLET_ROUTE = [
    "modules/source_wallet_bot",
    "sikk_candidate_wallet_structure_pipeline.py",
    "sikk_wallet_structure_gate.py",
    "sikk_candidate_state_machine.py",
    "sikk_live_run.py",
]

COMPATIBILITY_ROUTES = {
    "sikk_sol_full_auto_workflow.py": "legacy_compat_one_shot",
}


class SemanticLayer(str, Enum):
    QUARANTINE = "quarantine"
    RAW = "raw"
    NORMALIZED = "normalized"
    FACTS = "facts"
    EVIDENCE = "evidence"
    INFERENCE = "inference"
    HANDOFF = "handoff"
    STATE = "state"
    REPORT = "report"
    MANIFEST = "manifest"


class ProducerType(str, Enum):
    COLLECTOR = "collector"
    NORMALIZER = "normalizer"
    ANALYZER = "analyzer"
    GATE = "gate"
    STATE_MACHINE = "state_machine"
    REPORTER = "reporter"
    MANIFEST_BUILDER = "manifest_builder"
    COMPAT = "compat"


PRODUCER_ALLOWED_LAYERS = {
    ProducerType.COLLECTOR: {SemanticLayer.QUARANTINE, SemanticLayer.RAW, SemanticLayer.NORMALIZED, SemanticLayer.MANIFEST},
    ProducerType.NORMALIZER: {SemanticLayer.NORMALIZED, SemanticLayer.FACTS, SemanticLayer.MANIFEST},
    ProducerType.ANALYZER: {SemanticLayer.EVIDENCE, SemanticLayer.INFERENCE, SemanticLayer.REPORT, SemanticLayer.MANIFEST},
    ProducerType.GATE: {SemanticLayer.HANDOFF, SemanticLayer.REPORT, SemanticLayer.MANIFEST},
    ProducerType.STATE_MACHINE: {SemanticLayer.STATE, SemanticLayer.REPORT, SemanticLayer.MANIFEST},
    ProducerType.REPORTER: {SemanticLayer.REPORT, SemanticLayer.MANIFEST},
    ProducerType.MANIFEST_BUILDER: {SemanticLayer.MANIFEST},
    ProducerType.COMPAT: {SemanticLayer.QUARANTINE, SemanticLayer.RAW, SemanticLayer.NORMALIZED, SemanticLayer.REPORT, SemanticLayer.MANIFEST},
}

INFERENCE_LIKE_KEYS = {
    "inference",
    "dominant_lifecycle",
    "wallet_structure_status",
    "behavior_inference",
    "persona_primary",
    "entity_group_id",
    "same_source_candidate",
    "control_status",
    "risk_observation",
}

STATE_LIKE_KEYS = {
    "final_state",
    "state",
    "paper_status",
    "paper_ready",
    "transition_reason",
}

HANDOFF_LIKE_KEYS = {
    "handoff",
    "paper_gate_handoff",
    "state_machine_handoff",
    "gmgn_remark_handoff",
    "dashboard_handoff",
}

REQUIRED_BY_LAYER = {
    SemanticLayer.RAW: {"source_refs", "task_passport"},
    SemanticLayer.NORMALIZED: {"source_refs", "task_passport"},
    SemanticLayer.FACTS: {"source_refs", "task_passport"},
    SemanticLayer.EVIDENCE: {"source_refs", "task_passport"},
    SemanticLayer.INFERENCE: {"source_refs", "task_passport"},
    SemanticLayer.HANDOFF: {"source_refs", "task_passport"},
    SemanticLayer.STATE: {"source_refs", "task_passport"},
    SemanticLayer.REPORT: {"task_passport"},
}
