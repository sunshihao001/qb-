import json
from pathlib import Path


def _write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_full_pipeline_defaults_wallet_structure_mode_to_observe_sidecar(tmp_path):
    from run_sikk_gmgn_pipeline import run_full_pipeline

    token = "TokenObserve111111111111111111111111111111"

    def fake_trenches_runner(_command):
        return {
            "data": [
                {
                    "代币地址": token,
                    "代币符号": "OBS",
                    "筛选等级": "S3_进入SIKK结构分析",
                    "是否进入候选池": True,
                    "address": token,
                    "symbol": "OBS",
                    "market_cap": 100000,
                    "liquidity": 50000,
                    "volume_24h": 80000,
                    "net_inflow": 10000,
                    "top10_holder_rate": 0.2,
                    "dev_hold_rate": 0.01,
                }
            ]
        }

    def fake_kline_runner(_command):
        return {"data": {"klines": []}}

    def fake_wallet_structure_runner(*, candidate_states_path, output_dir):
        payload = _read_json(Path(candidate_states_path))
        return {
            "summary_json": str(_write_json(
                Path(output_dir) / "candidate_wallet_structure_summary.json",
                {
                    "处理结果": [
                        {
                            "代币地址": token,
                            "钱包结构结论": "WALLET_BLOCK",
                            "钱包结构系数": 0,
                            "钱包结构评分": 10,
                            "钱包风险评分": 99,
                            "对手盘压力评分": 90,
                            "状态调整原因": "测试：对手盘压力高",
                        }
                    ]
                },
            )),
            "summary_csv": str(Path(output_dir) / "candidate_wallet_structure_summary.csv"),
            "summary_md": str(Path(output_dir) / "candidate_wallet_structure_summary.md"),
        }

    result = run_full_pipeline(
        output_root=tmp_path / "run",
        trenches_runner=fake_trenches_runner,
        kline_runner=fake_kline_runner,
        limit=1,
        run_quote_security=False,
        wallet_structure_runner=fake_wallet_structure_runner,
    )

    manifest = _read_json(Path(result["manifest_json"]))
    states_path = Path(manifest["输出文件"]["状态机JSON"])
    states = _read_json(states_path)
    row = states["候选状态"][0]
    assert manifest["参数"]["wallet_structure_mode"] == "observe"
    assert states["输入文件"]["钱包结构模式"] == "observe"
    assert row["当前状态"] == "WATCHING"
    assert row["钱包结构结论"] == "WALLET_BLOCK"
    assert row["钱包门禁效果"] == "OBSERVE_ONLY"
    assert row["would_block"] is True


def test_full_pipeline_hard_wallet_structure_mode_blocks_when_explicit(tmp_path):
    from run_sikk_gmgn_pipeline import run_full_pipeline

    token = "TokenHard111111111111111111111111111111111"

    def fake_trenches_runner(_command):
        return {
            "data": [
                {
                    "代币地址": token,
                    "代币符号": "HARD",
                    "筛选等级": "S3_进入SIKK结构分析",
                    "是否进入候选池": True,
                    "address": token,
                    "symbol": "HARD",
                    "market_cap": 100000,
                    "liquidity": 50000,
                    "volume_24h": 80000,
                    "net_inflow": 10000,
                    "top10_holder_rate": 0.2,
                    "dev_hold_rate": 0.01,
                }
            ]
        }

    def fake_kline_runner(_command):
        return {"data": {"klines": []}}

    def fake_wallet_structure_runner(*, candidate_states_path, output_dir):
        return {
            "summary_json": str(_write_json(
                Path(output_dir) / "candidate_wallet_structure_summary.json",
                {
                    "处理结果": [
                        {
                            "代币地址": token,
                            "钱包结构结论": "WALLET_BLOCK",
                            "钱包结构系数": 0,
                            "钱包结构评分": 10,
                            "钱包风险评分": 99,
                            "对手盘压力评分": 90,
                            "状态调整原因": "测试：hard 模式阻断",
                        }
                    ]
                },
            )),
            "summary_csv": str(Path(output_dir) / "candidate_wallet_structure_summary.csv"),
            "summary_md": str(Path(output_dir) / "candidate_wallet_structure_summary.md"),
        }

    result = run_full_pipeline(
        output_root=tmp_path / "run_hard",
        trenches_runner=fake_trenches_runner,
        kline_runner=fake_kline_runner,
        limit=1,
        run_quote_security=False,
        wallet_structure_runner=fake_wallet_structure_runner,
        wallet_structure_mode="hard",
    )

    manifest = _read_json(Path(result["manifest_json"]))
    states = _read_json(Path(manifest["输出文件"]["状态机JSON"]))
    row = states["候选状态"][0]
    assert manifest["参数"]["wallet_structure_mode"] == "hard"
    assert row["当前状态"] == "BLOCKED"
    assert row["钱包门禁效果"] == "HARD_BLOCK"
