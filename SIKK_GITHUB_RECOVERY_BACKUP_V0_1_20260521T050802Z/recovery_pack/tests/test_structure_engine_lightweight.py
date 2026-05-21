import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/gmgn_read_only/latest/structure_engine"

def load(name):
    return json.loads((BASE/name).read_text(encoding="utf-8"))

def test_structure_signal_required_blocks():
    sig = load("structure_signal.json")
    for key in ["market_structure","wallet_structure","chip_structure","security_structure","counter_evidence","structure_confidence","recommended_decision_bias"]:
        assert key in sig
    assert sig["market_structure"]["signal"] in {"SUPPORTIVE","NEUTRAL","RISKY","UNKNOWN"}
    assert sig["security_structure"]["signal"] in {"PASS","RISKY","MISSING","UNKNOWN"}

def test_decision_ticket_consumes_structure_signal():
    ticket = load("decision_ticket_after_structure.json")
    assert ticket["input_structure_signal"] == "data/gmgn_read_only/latest/structure_engine/structure_signal.json"
    assert ticket["decision_state"] in {"EXCLUDE","WATCH","RISK_MONITOR","PAPER_READY_CANDIDATE","PATCH_REQUIRED"}
    assert ticket["structure_evidence_summary"]
    assert ticket["current_stage_must_not_create_paper_position"] is True
    assert ticket["no_paper_position_created"] is True

def test_security_missing_blocks_paper_candidate():
    sig = load("structure_signal.json")
    ticket = load("decision_ticket_after_structure.json")
    if sig["security_structure"]["signal"] == "MISSING":
        assert ticket["decision_state"] != "PAPER_READY_CANDIDATE"
        assert ticket["paper_candidate_allowed"] is False

def test_acceptance_and_forbidden_scope():
    report = load("structure_engine_acceptance_report.json")
    assert report["acceptance_status"] == "PASS"
    forbidden = report["forbidden_scope"]
    assert forbidden["paper_position_created"] is False
    assert forbidden["swap_or_order_quote_called"] is False
    assert forbidden["private_key_signing_broadcast_used"] is False
    assert forbidden["live_trading_used"] is False
    assert report["gmgn_skill_called"] is False
