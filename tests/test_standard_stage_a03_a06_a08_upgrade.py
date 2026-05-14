import json
import subprocess
import sys
from pathlib import Path

ROOT = Path("/root/sikk-gmgn")
PHASES = [f"K{i:02d}" for i in range(0, 9)] + [f"P{i:02d}" for i in range(0, 11)] + [f"I{i:02d}" for i in range(1, 6)] + ["R00"]
FORBIDDEN = ["swap", "private_key", "signing", "broadcast", "real_trade"]


def load_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_a03_replay_evidence_packets_are_persisted_and_manifested():
    manifest_path = ROOT / "system/stable_trader_os/replay_evidence_plane/manifest.json"
    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["status"] == "REPLAY_EVIDENCE_PACKET_PERSISTENCE_READY_PAPER_ONLY"
    assert manifest["safety"]["paper_only"] is True
    assert manifest["safety"]["forbidden_real_execution"] == FORBIDDEN
    assert set(PHASES).issubset(set(manifest["phases"].keys()))
    for phase in PHASES:
        record = manifest["phases"][phase]
        evidence_path = ROOT / record["latest_evidence_packet"]
        assert evidence_path.exists(), phase
        packet = json.loads(evidence_path.read_text(encoding="utf-8"))
        assert packet["phase_id"] == phase
        assert packet["runtime_mode"] == "paper_only"
        assert packet["status"] == "REPLAY_EVIDENCE_PACKET_PERSISTED"
        assert packet["input_hash"]
        assert packet["output_hash"]
        assert packet["source_artifact"]
        assert packet["acceptance_evidence"]
        assert packet["semantic_replay_cases"]
        assert packet["forbidden_action_scan"]["status"] == "PASS"
        assert packet["forbidden_action_scan"]["blocked_actions"] == FORBIDDEN


def test_a06_legacy_absorption_registry_and_old_runner_blocklist_exist():
    registry = load_json("system/stable_trader_os/legacy_control/legacy_absorption_registry.json")
    blocklist = load_json("system/stable_trader_os/legacy_control/old_runner_blocklist.json")
    policy = load_json("system/stable_trader_os/legacy_control/legacy_read_only_policy.json")
    assert registry["status"] == "LEGACY_ABSORPTION_REGISTRY_READY"
    assert blocklist["status"] == "OLD_RUNNER_BLOCKLIST_ENFORCED_PAPER_ONLY"
    assert policy["status"] == "LEGACY_READ_ONLY_POLICY_READY"
    assert registry["candidate_count"] >= 1
    assert blocklist["blocked_call_policy"] == "must_route_through_standard_stage_closure"
    assert policy["write_policy"] == "read_only_except_compat_index"
    assert policy["real_execution_allowed"] is False
    assert any(item["route_policy"] == "BLOCK_DIRECT_CALL_REQUIRE_CANONICAL_ROUTER" for item in blocklist["blocked_runners"])


def test_a08_telegram_canonical_router_runs_manifest_to_runtime_to_acceptance_panel():
    from modules.stable_trader_os.telegram_canonical_router import route_telegram_command

    result = route_telegram_command({
        "command": "/sikk_stage_run",
        "phase_id": "K00",
        "run_id": "TEST_TELEGRAM_CANONICAL_ROUTE",
        "source": "telegram_test",
    })
    assert result["status"] == "TELEGRAM_CANONICAL_ROUTE_ACCEPTED_PAPER_ONLY"
    assert result["route_chain"] == ["telegram_command", "canonical_router", "standard_stage_closure_manifest", "runtime_entry", "acceptance_gate", "reply_panel"]
    assert result["phase_id"] == "K00"
    assert result["runtime_result"]["runtime_mode"] == "paper_only"
    assert result["runtime_result"]["semantic_acceptance"]["status"] in {"SEMANTIC_REPLAY_ACCEPTED", "SEMANTIC_REPLAY_ACCEPTED_WITH_DOWNGRADE"}
    assert result["reply_panel"]["runtime_mode"] == "paper_only"
    assert result["reply_panel"]["real_execution_allowed"] is False
    assert result["reply_panel"]["blocked_real_execution"] == FORBIDDEN
    assert (ROOT / result["reply_panel_path"]).exists()


def test_a03_a06_a08_upgrade_validator_passes():
    result = subprocess.run(
        [sys.executable, "tools/stable_trader_os/a03_a06_a08_upgrade.py", "validate", "--root", str(ROOT)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "A03_A06_A08_UPGRADE_VALIDATION_PASS" in result.stdout
