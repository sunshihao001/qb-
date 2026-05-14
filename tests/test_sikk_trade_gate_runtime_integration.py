import json
from pathlib import Path


TOKEN = "4ZEzC3aX7yLv8VEBiuoT6PgEMPEoxGB7WS3Qt3iPpump"


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def test_state_machine_consumes_trade_gate_runtime_summary_and_blocks_real_trade(tmp_path):
    from sikk_candidate_state_machine import run_candidate_state_machine

    candidates = tmp_path / "token_candidates.json"
    trade_gate_summary = tmp_path / "trade_gate_runtime_summary.json"
    out = tmp_path / "state_machine"

    _write_json(candidates, {
        "候选结果": [
            {"代币地址": TOKEN, "代币符号": "AGI", "筛选等级": "S3_进入SIKK结构分析", "是否进入候选池": True}
        ]
    })
    _write_json(trade_gate_summary, {
        "处理结果": [
            {
                "token_address": TOKEN,
                "token_symbol": "AGI",
                "final_status": "OBSERVE",
                "signal_level": "S1",
                "decision": "OBSERVE_ONLY",
                "permission": "BLOCK_REAL_TRADE",
                "contract_permission": "PAUSE_NEED_CONFIRM_需要人工确认",
                "real_trade_enabled": False,
                "risk_level": "MEDIUM_HIGH",
                "execution_action": "OBSERVE",
                "funding_status": "资金待查",
                "wallet_structure_status": "WALLET_PAUSE",
                "wallet_structure_score": 72.96,
                "wallet_risk_score": 76.37,
                "reason_codes": ["STRUCTURAL_PAUSE", "FUNDING_PENDING"],
            }
        ]
    })

    result = run_candidate_state_machine(
        candidates_path=candidates,
        trade_gate_summary_path=trade_gate_summary,
        output_dir=out,
    )

    payload = json.loads(Path(result["states_json"]).read_text(encoding="utf-8"))
    row = payload["候选状态"][0]
    assert row["代币地址"] == TOKEN
    assert row["当前状态"] == "WATCHING"
    assert row["交易门控决策"] == "OBSERVE_ONLY"
    assert row["交易门控状态"] == "OBSERVE"
    assert row["合约门控权限"] == "PAUSE_NEED_CONFIRM_需要人工确认"
    assert row["真实交易允许"] is False
    assert row["资金状态"] == "资金待查"
    assert "STRUCTURAL_PAUSE" in row["交易门控原因码"]
    assert "交易门控暂停" in row["状态原因"]


def test_live_run_enriches_token_status_with_trade_gate_runtime_and_journal(tmp_path):
    import sikk_live_run

    def fake_pipeline_runner(**kwargs):
        root = Path(kwargs["output_root"])
        (root / "state_machine").mkdir(parents=True, exist_ok=True)
        (root / "candidate_signal_outputs").mkdir(parents=True, exist_ok=True)
        (root / "quote_security").mkdir(parents=True, exist_ok=True)
        (root / "wallet_structure").mkdir(parents=True, exist_ok=True)
        (root / "trade_gate_runtime").mkdir(parents=True, exist_ok=True)
        _write_json(root / "state_machine" / "candidate_states.json", {
            "候选状态": [{
                "代币地址": TOKEN,
                "代币符号": "AGI",
                "当前状态": "WATCHING",
                "交易门控决策": "OBSERVE_ONLY",
                "交易门控状态": "OBSERVE",
                "合约门控权限": "PAUSE_NEED_CONFIRM_需要人工确认",
                "真实交易允许": False,
                "资金状态": "资金待查",
            }]
        })
        _write_json(root / "candidate_signal_outputs" / "candidate_signal_summary.json", {"处理结果": []})
        _write_json(root / "quote_security" / "candidate_quote_security_summary.json", {"处理结果": []})
        _write_json(root / "trade_gate_runtime" / "trade_gate_runtime_summary.json", {
            "处理结果": [{
                "token_address": TOKEN,
                "token_symbol": "AGI",
                "decision": "OBSERVE_ONLY",
                "final_status": "OBSERVE",
                "contract_permission": "PAUSE_NEED_CONFIRM_需要人工确认",
                "real_trade_enabled": False,
                "execution_action": "OBSERVE",
                "funding_status": "资金待查",
                "risk_level": "MEDIUM_HIGH",
                "reason_codes": ["STRUCTURAL_PAUSE", "FUNDING_PENDING"],
            }]
        })
        return {"candidate_states": str(root / "state_machine" / "candidate_states.json")}

    def fake_paper_runner(**kwargs):
        out = Path(kwargs["output_dir"])
        out.mkdir(parents=True, exist_ok=True)
        _write_json(out / "paper_positions_open.json", {"open_positions": []})
        _write_json(out / "paper_positions_closed.json", {"closed_positions": []})
        (out / "failure_attribution.jsonl").write_text("", encoding="utf-8")
        return {"open_positions_json": str(out / "paper_positions_open.json"), "closed_positions_json": str(out / "paper_positions_closed.json")}

    paths = sikk_live_run.run_live_once(
        output_root=tmp_path,
        limit=1,
        now="2026-05-10T17:30:00Z",
        pipeline_runner=fake_pipeline_runner,
        paper_runner=fake_paper_runner,
    )

    live_state = json.loads(Path(paths["live_state_json"]).read_text(encoding="utf-8"))
    status = live_state["tokens"][0]
    assert status["token_address"] == TOKEN
    assert status["trade_gate"]["decision"] == "OBSERVE_ONLY"
    assert status["trade_gate"]["real_trade_enabled"] is False
    assert status["latest_action"] == "STRUCTURE_OBSERVE"
    assert "交易门控" in status["latest_reason"]

    journal = tmp_path / "trade_gate_journal" / "trade_gate_review.jsonl"
    assert journal.exists()
    rows = [json.loads(line) for line in journal.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert rows[0]["token_address"] == TOKEN
    assert rows[0]["decision"] == "OBSERVE_ONLY"
    assert rows[0]["real_trade_enabled"] is False
