from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from core.decision_engine import build_decision_ticket

RUN_DIR = Path("data/runs/4pMsh7JF5wXjkx8sK6gJgv14xkBy1kUoMv4ixN8npump/skill_raw_handoff_probe")
STRATEGY = Path("contracts/strategy_contract.json")
SCHEMA = Path("contracts/decision_ticket_schema.json")


def test_decision_ticket_schema_valid():
    ticket, _, _, _ = build_decision_ticket(RUN_DIR, STRATEGY)
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(ticket)


def test_required_decision_fields_present():
    ticket, _, _, _ = build_decision_ticket(RUN_DIR, STRATEGY)
    for key in [
        "ticket_id", "run_id", "token", "strategy_id", "contract_version", "contract_hash",
        "feature_snapshot_path", "decision_status", "paper_ready", "live_eligible", "swap_allowed",
        "rule_evaluation", "evidence_summary", "counter_evidence", "reason_codes", "risk_boundary",
        "replay_pointer", "created_at",
    ]:
        assert key in ticket
