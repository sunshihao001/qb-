from pathlib import Path
import json

from modules.stable_trader_os.phase_01_data_fact import Phase01Runner

ROOT = Path(__file__).resolve().parents[3]
EXAMPLE = ROOT / "examples" / "stable_trader_os" / "phase_01_data_fact" / "mock_phase_01_input.json"


def test_phase_01_runner_writes_canonical_data_fact_outputs_and_shared_handoff(tmp_path):
    result = Phase01Runner(ROOT).run(EXAMPLE, tmp_path / "run")

    canonical_required = [
        "01_data_fact/normalized/token_basic_normalized.json",
        "01_data_fact/normalized/token_market_context.json",
        "01_data_fact/normalized/wallet_trade_normalized.csv",
        "01_data_fact/normalized/holder_normalized.csv",
        "01_data_fact/normalized/kline_normalized.csv",
        "01_data_fact/normalized/quote_security_normalized.json",
        "01_data_fact/summary/data_quality_summary.json",
        "01_data_fact/handoff/phase_01_handoff_packet.json",
    ]
    for rel in canonical_required:
        assert (tmp_path / "run" / rel).exists(), rel

    shared_handoff = tmp_path / "run" / "shared_handoff" / "MOCK_TOKEN_ADDRESS_DO_NOT_USE_REAL_SECRET" / "phase_01_handoff_packet.json"
    assert shared_handoff.exists()

    handoff = json.loads(shared_handoff.read_text(encoding="utf-8"))
    assert handoff["phase"] == "phase_01_data_fact_controller"
    assert handoff["handoff_status"] in {"HANDOFF_READY", "HANDOFF_DEGRADED", "HANDOFF_BLOCKED"}
    assert handoff["next_stage"] == "phase_02_wallet_structure_controller"
    assert handoff["required_files_for_next_stage"]["token_basic_normalized"].endswith("token_basic_normalized.json")

    summary = json.loads((tmp_path / "run" / "01_data_fact/summary/data_quality_summary.json").read_text(encoding="utf-8"))
    assert summary["phase"] == "phase_01_data_fact_controller"
    assert summary["status_code"] in {"DATA_OK", "DATA_PARTIAL", "DATA_WEAK", "DATA_INVALID", "DATA_STALE", "DATA_SOURCE_CONFLICT"}
    assert isinstance(summary["positive_evidence"], list)
    assert isinstance(summary["negative_evidence"], list)
    assert isinstance(summary["counter_evidence"], list)
    assert "buy_signal" not in json.dumps(summary)
    assert "certain_dealer" not in json.dumps(summary)

    assert result["shared_handoff_packet"].endswith("phase_01_handoff_packet.json")
