import json
from pathlib import Path


def _write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_paper_live_runner_carries_wallet_structure_fields_into_position_and_trades(tmp_path):
    from sikk_paper_live_runner import run_paper_live_cycle

    token = "TokenWallet11111111111111111111111111111111"
    states_path = _write_json(
        tmp_path / "candidate_states.json",
        {
            "候选状态": [
                {
                    "代币地址": token,
                    "代币符号": "WAL",
                    "当前状态": "PAPER_READY",
                    "信号价格": 1.0,
                    "建议纸面仓位SOL": 0.2,
                    "钱包结构结论": "WALLET_SUPPORT",
                    "钱包结构系数": 0.5,
                    "钱包结构评分": 48,
                    "钱包风险评分": 12,
                    "钱包结构原因": "E3/E4 正向结构钱包仍有持仓或结果证据",
                }
            ]
        },
    )
    signal_summary_path = _write_json(
        tmp_path / "candidate_signal_summary.json",
        {"信号结果": [{"代币地址": token, "代币符号": "WAL", "信号价格": 1.0, "建议纸面仓位SOL": 0.2}]},
    )
    quote_security_summary_path = _write_json(
        tmp_path / "quote_security.json",
        {"处理结果": [{"代币地址": token, "交易前状态": "READY_FOR_CONFIRMATION", "最终权限": "ALLOW_CONFIRMATION_LAYER"}]},
    )

    paths = run_paper_live_cycle(
        candidate_states_path=states_path,
        signal_summary_path=signal_summary_path,
        quote_security_summary_path=quote_security_summary_path,
        output_dir=tmp_path / "paper_live",
        price_provider=lambda _token: {"price": 1.1, "source": "okx", "snapshot_time": "2026-05-01T04:00:00Z"},
        snapshot_time="2026-05-01T04:00:00Z",
    )

    open_payload = _read_json(Path(paths["open_positions_json"]))
    position = open_payload["open_positions"][0]
    assert position["wallet_structure_status"] == "WALLET_SUPPORT"
    assert position["wallet_structure_factor"] == 0.5
    assert position["wallet_structure_score"] == 48
    assert position["wallet_risk_score"] == 12
    assert position["position_sol"] == 0.1

    trades = Path(paths["paper_trades_csv"]).read_text(encoding="utf-8-sig")
    assert "wallet_structure_status" in trades
    assert "WALLET_SUPPORT" in trades
