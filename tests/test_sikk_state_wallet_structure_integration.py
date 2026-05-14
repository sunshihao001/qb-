import json
from pathlib import Path


def _write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_state_machine_default_observe_records_wallet_block_without_blocking(tmp_path):
    from tests.test_sikk_candidate_state_machine import _build_inputs, TOKEN_READY
    from sikk_candidate_state_machine import run_candidate_state_machine

    inputs = _build_inputs(tmp_path)
    wallet_summary = _write_json(
        tmp_path / "wallet_structure" / "candidate_wallet_structure_summary.json",
        {
            "处理结果": [
                {
                    "代币地址": TOKEN_READY,
                    "钱包结构结论": "WALLET_BLOCK",
                    "钱包结构系数": 0.0,
                    "钱包结构评分": 12,
                    "钱包风险评分": 99,
                    "对手盘压力评分": 99,
                    "状态调整原因": "对手盘压力高",
                }
            ]
        },
    )

    result = run_candidate_state_machine(
        candidates_path=inputs["candidates"],
        kline_summary_path=inputs["kline"],
        signal_summary_path=inputs["signals"],
        wallet_structure_summary_path=wallet_summary,
        output_dir=tmp_path / "state_machine",
    )

    payload = _read_json(Path(result["states_json"]))
    row = next(item for item in payload["候选状态"] if item["代币地址"] == TOKEN_READY)
    assert row["当前状态"] == "PAPER_READY"
    assert row["钱包结构结论"] == "WALLET_BLOCK"
    assert row["钱包门禁模式"] == "observe"
    assert row["钱包门禁效果"] == "OBSERVE_ONLY"
    assert row["would_block"] is True


def test_state_machine_applies_wallet_structure_gate_to_paper_ready_candidates_in_hard_mode(tmp_path):
    from tests.test_sikk_candidate_state_machine import _build_inputs, TOKEN_READY
    from sikk_candidate_state_machine import run_candidate_state_machine

    inputs = _build_inputs(tmp_path)
    wallet_summary = _write_json(
        tmp_path / "wallet_structure" / "candidate_wallet_structure_summary.json",
        {
            "处理结果": [
                {
                    "代币地址": TOKEN_READY,
                    "钱包结构结论": "WALLET_BLOCK",
                    "钱包结构系数": 0.0,
                    "钱包结构评分": 12,
                    "钱包风险评分": 70,
                    "建议状态调整": "调整为 BLOCKED",
                    "状态调整原因": "发现分发派发/接收相关钱包 2 个",
                }
            ]
        },
    )

    result = run_candidate_state_machine(
        candidates_path=inputs["candidates"],
        kline_summary_path=inputs["kline"],
        signal_summary_path=inputs["signals"],
        wallet_structure_summary_path=wallet_summary,
        wallet_structure_mode="hard",
        output_dir=tmp_path / "state_machine",
    )

    payload = _read_json(Path(result["states_json"]))
    row = next(item for item in payload["候选状态"] if item["代币地址"] == TOKEN_READY)
    assert row["当前状态"] == "BLOCKED"
    assert row["钱包结构结论"] == "WALLET_BLOCK"
    assert row["钱包结构系数"] == 0.0
    assert "钱包结构门禁阻断" in row["状态原因"]
    assert payload["输入文件"]["钱包结构门禁"].endswith("candidate_wallet_structure_summary.json")


def test_state_machine_pauses_wallet_structure_pause_candidates(tmp_path):
    from tests.test_sikk_candidate_state_machine import _build_inputs, TOKEN_READY
    from sikk_candidate_state_machine import run_candidate_state_machine

    inputs = _build_inputs(tmp_path)
    wallet_summary = _write_json(
        tmp_path / "wallet_structure" / "candidate_wallet_structure_summary.json",
        {
            "处理结果": [
                {
                    "代币地址": TOKEN_READY,
                    "钱包结构结论": "WALLET_PAUSE",
                    "钱包结构系数": 0.3,
                    "钱包结构评分": 18,
                    "钱包风险评分": 35,
                    "建议状态调整": "降级为 WATCHING/PAUSE",
                    "状态调整原因": "多个新钱包/临时执行钱包资金待查",
                }
            ]
        },
    )

    result = run_candidate_state_machine(
        candidates_path=inputs["candidates"],
        kline_summary_path=inputs["kline"],
        signal_summary_path=inputs["signals"],
        wallet_structure_summary_path=wallet_summary,
        wallet_structure_mode="hard",
        output_dir=tmp_path / "state_machine",
    )

    payload = _read_json(Path(result["states_json"]))
    row = next(item for item in payload["候选状态"] if item["代币地址"] == TOKEN_READY)
    assert row["当前状态"] == "WATCHING"
    assert row["钱包结构结论"] == "WALLET_PAUSE"
    assert "钱包结构门禁暂停" in row["状态原因"]
