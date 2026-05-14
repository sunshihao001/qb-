import csv
import json
from pathlib import Path


TOKEN_A = "Good111111111111111111111111111111111111111"
TOKEN_B = "Watch22222222222222222222222222222222222222"
TOKEN_C = "Skip333333333333333333333333333333333333333"


def make_candidate_file(path: Path):
    payload = {
        "模块": "SIKK-GMGN 新币筛选",
        "候选列表": [
            {
                "代币地址": TOKEN_A,
                "代币符号": "GOOD",
                "代币名称": "Good Token",
                "筛选等级": "S3_进入SIKK结构分析",
                "是否进入候选池": True,
                "开盘时间戳": 1770000000,
                "创建时间戳": 1769999700,
                "总供应量": 1_000_000_000,
            },
            {
                "代币地址": TOKEN_B,
                "代币符号": "WATCH",
                "代币名称": "Watch Token",
                "筛选等级": "S2_重点观察",
                "是否进入候选池": True,
                "open_timestamp": 1770000100,
                "total_supply": 1_000_000_000,
            },
            {
                "代币地址": TOKEN_C,
                "代币符号": "SKIP",
                "代币名称": "Skip Token",
                "筛选等级": "S1_普通观察",
                "是否进入候选池": True,
                "开盘时间戳": 1770000200,
            },
        ],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def fake_kline_response(start_ms=1770000000000, count=36):
    rows = []
    price = 0.00010
    for i in range(count):
        # 构造稳定可解析的 GMGN K线：time 是毫秒，volume 是 USD 成交额。
        open_p = price * (1 + i * 0.004)
        close_p = open_p * (1.01 if i % 4 else 0.995)
        high_p = max(open_p, close_p) * 1.025
        low_p = min(open_p, close_p) * 0.965
        volume = 1200 + i * 80
        rows.append(
            {
                "time": start_ms + i * 60_000,
                "open": str(open_p),
                "high": str(high_p),
                "low": str(low_p),
                "close": str(close_p),
                "volume": str(volume),
                "amount": str(volume / close_p),
            }
        )
    return {"list": rows}


def test_build_gmgn_kline_command_is_readonly_and_uses_seconds():
    from sikk_candidate_kline_pipeline import build_gmgn_kline_command

    cmd = build_gmgn_kline_command(
        token_address=TOKEN_A,
        resolution="1m",
        start_ts=1770000000,
        end_ts=1770007200,
        chain="sol",
    )
    joined = " ".join(cmd)

    assert cmd[:3] == ["gmgn-cli", "market", "kline"]
    assert "--chain sol" in joined
    assert f"--address {TOKEN_A}" in joined
    assert "--resolution 1m" in joined
    assert "--from 1770000000" in joined
    assert "--to 1770007200" in joined
    assert "--raw" in cmd
    assert "gmgn-cli swap" not in joined
    assert "order strategy create" not in joined
    assert "onchainos swap execute" not in joined


def test_convert_gmgn_kline_to_detector_csv(tmp_path):
    from sikk_candidate_kline_pipeline import write_kline_csv

    csv_path = tmp_path / "kline_1m.csv"
    rows = write_kline_csv(
        raw_payload=fake_kline_response(count=5),
        csv_path=csv_path,
        supply=1_000_000_000,
    )

    assert rows == 5
    with csv_path.open(encoding="utf-8-sig") as f:
        parsed = list(csv.DictReader(f))
    assert parsed[0]["timestamp"] == "1770000000"
    assert set(["timestamp", "open", "high", "low", "close", "volume", "amount", "market_cap"]).issubset(parsed[0])
    assert float(parsed[0]["market_cap"]) > 0


def test_pipeline_reads_s3_candidates_fetches_kline_and_runs_accumulation(tmp_path):
    from sikk_candidate_kline_pipeline import run_candidate_kline_pipeline

    candidate_path = tmp_path / "token_candidates.json"
    make_candidate_file(candidate_path)
    calls = []

    def fake_runner(cmd):
        calls.append(cmd)
        assert cmd[:3] == ["gmgn-cli", "market", "kline"]
        return fake_kline_response(count=40)

    outputs = run_candidate_kline_pipeline(
        candidates_path=candidate_path,
        output_root=tmp_path / "data" / "gmgn_candidates",
        runner=fake_runner,
        include_levels=["S3_进入SIKK结构分析"],
        resolutions=["1m", "5m"],
        one_minute_minutes=120,
        five_minute_minutes=360,
        run_accumulation=True,
    )

    assert len(calls) == 2  # 只处理 S3，且拉 1m/5m
    assert outputs["summary_path"].exists()
    summary = json.loads(outputs["summary_path"].read_text(encoding="utf-8"))
    assert summary["处理统计"]["处理候选数"] == 1
    assert summary["处理结果"][0]["代币地址"] == TOKEN_A

    token_dir = tmp_path / "data" / "gmgn_candidates" / TOKEN_A
    assert (token_dir / "kline_1m.csv").exists()
    assert (token_dir / "kline_5m.csv").exists()
    assert (token_dir / "kline_normalized.json").exists()
    assert (token_dir / "market_pattern_source_snapshot.json").exists()
    normalized = json.loads((token_dir / "kline_normalized.json").read_text(encoding="utf-8"))
    assert normalized[0]["token_address"] == TOKEN_A
    assert normalized[0]["timeframe"] == "1m"
    for key in [
        "kline_window_start", "kline_window_end", "latest_kline_time", "open", "high", "low",
        "close", "volume", "vwap", "avwap_if_available", "high_low_range",
        "control_box_high", "control_box_low", "breakout_time", "pullback_time",
        "volume_expansion_ratio",
    ]:
        assert key in normalized[0]
    pattern_snapshot = json.loads((token_dir / "market_pattern_source_snapshot.json").read_text(encoding="utf-8"))
    assert pattern_snapshot["token_address"] == TOKEN_A
    assert pattern_snapshot["source_files"]["kline_normalized"].endswith("kline_normalized.json")
    assert pattern_snapshot["pattern_inputs"]["timeframes"] == ["1m", "5m"]
    assert (token_dir / "accumulation_outputs" / "accumulation_window.json").exists()
    acc = json.loads((token_dir / "accumulation_outputs" / "accumulation_window.json").read_text(encoding="utf-8"))
    assert acc["token"] == TOKEN_A


def test_pipeline_can_include_s2_when_configured(tmp_path):
    from sikk_candidate_kline_pipeline import select_candidates_for_kline

    candidate_path = tmp_path / "token_candidates.json"
    make_candidate_file(candidate_path)

    s3_only = select_candidates_for_kline(candidate_path, include_levels=["S3_进入SIKK结构分析"])
    s2_s3 = select_candidates_for_kline(candidate_path, include_levels=["S3_进入SIKK结构分析", "S2_重点观察"])

    assert [c["代币地址"] for c in s3_only] == [TOKEN_A]
    assert [c["代币地址"] for c in s2_s3] == [TOKEN_A, TOKEN_B]
