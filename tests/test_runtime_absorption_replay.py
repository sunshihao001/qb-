from __future__ import annotations

import json
from pathlib import Path

from modules.runtime.runtime_absorption import run_single_token_runtime_absorption_replay


ROOT = Path(__file__).resolve().parents[1]
TOKEN = "ECgweD7xkMj4bm8CcM9rusxKjyQGgdosCvVmhGUupump"


def _load_json(path: str | Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _load_jsonl(path: str | Path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


def test_runtime_absorption_phase_controller_writes_complete_trace_and_handoffs(tmp_path: Path):
    result = run_single_token_runtime_absorption_replay(root=ROOT, output_dir=tmp_path / "absorption", token_address=TOKEN)

    assert result["acceptance"] == "PHASE_REPLAY_PASS"
    assert result["phase_controller_used"] is True
    assert result["runner_bypass_detected"] is False
    assert result["live_strategy_mutation_allowed"] is False

    trace_path = Path(result["artifacts"]["phase_trace"])
    rows = _load_jsonl(trace_path)
    assert [row["phase_id"] for row in rows] == ["P01", "P02", "P03", "P04", "P05", "P06", "P07", "P08", "P09"]

    required = {
        "phase_id",
        "input_files",
        "output_files",
        "runner_used",
        "decision",
        "evidence_level",
        "counter_evidence",
        "missing_fields",
        "status",
        "failure_reason",
        "downstream_handoff",
        "phase_controller",
        "handoff_packet",
        "acceptance_status",
    }
    assert all(required <= row.keys() for row in rows)
    assert all(row["phase_controller"] == "runtime_absorption_phase_controller" for row in rows)
    assert all(row["handoff_packet"] and Path(row["handoff_packet"]).exists() for row in rows)
    assert all(row["status"] == "PASS" for row in rows)
    assert all(row["missing_fields"] == [] for row in rows)

    handoff = _load_json(result["artifacts"]["phase_handoff_packet"])
    assert handoff["acceptance"] == "PHASE_REPLAY_PASS"
    assert set(handoff["phase_outputs"]) == {row["phase_id"] for row in rows}
    assert handoff["p09_p10_boundary"] == "review/failure attribution may enter P09/P10 task package only"


def test_runtime_absorption_wallet_canonical_p06_p08_p09_gaps_closed_without_live_rule_mutation(tmp_path: Path):
    result = run_single_token_runtime_absorption_replay(root=ROOT, output_dir=tmp_path / "absorption", token_address=TOKEN)
    artifacts = result["artifacts"]

    wallet = _load_json(artifacts["wallet_canonical_packet"])
    assert wallet["canonical_status"] == "WALLET_CANONICAL_READY"
    assert wallet["missing_fields"] == []
    assert wallet["wallet_gate_mode"] == "observe_only"
    assert wallet["would_block"] is True
    assert wallet["runtime_rule_mutation_allowed"] is False
    assert wallet["canonical_fields"]
    assert all({"wallet_address", "role", "game_side", "evidence_level"} <= row.keys() for row in wallet["canonical_rows"])

    p06 = _load_json(artifacts["scenario_recognition_packet"])
    assert p06["native_bound_output"] is True
    assert p06["scenario"] in p06["candidate_scenarios_checked"] or " / " in p06["scenario"]
    assert p06["missing_fields"] == []

    p07 = _load_json(artifacts["strategy_gate_decision"])
    assert len(p07["consumed_handoffs"]) >= 6
    assert p07["paper_runner_allowed_next"] is True
    assert p07["wallet_observe_only_gap_status"] == "STATUSIZED_NOT_BLOCKING_PAPER_ONLY"

    p08 = _load_json(artifacts["paper_only_execution_gate"])
    assert p08["paper_only_allowed"] is True
    assert p08["max_price_impact_pct_status"]["status"] in {"PRESENT", "MISSING_STATUSIZED"}
    assert p08["missing_fields"] == []
    assert p08["safety_boundary"] == {
        "paper_only": True,
        "no_real_swap": True,
        "no_signing": True,
        "no_broadcast": True,
        "no_private_key": True,
    }

    p09 = _load_json(artifacts["failure_attribution_packet"])
    assert p09["token_level_failure_row_present"] is True
    assert p09["forbidden_mutation_observed"] is False
    assert p09["route_to"] == "P09_issue_registry_and_P10_candidate_fix_package_only"
    assert p09["missing_fields"] == []

    issue_registry = Path(artifacts["issue_registry"]).read_text(encoding="utf-8")
    assert "OPEN" not in issue_registry
    assert "realtime_rule_mutation_allowed: false" in issue_registry
