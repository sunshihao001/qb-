import csv
import json
from pathlib import Path


TOKEN_A = "Good111111111111111111111111111111111111111"
TOKEN_B = "Bad2222222222222222222222222222222222222222"


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_kline(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    ts = 1770000000
    # 前 6 根形成第一波控盘箱体：low=0.00009 high=0.00012。
    for i in range(6):
        rows.append({
            "timestamp": ts + i * 60,
            "open": 0.00010,
            "high": 0.00012,
            "low": 0.00009,
            "close": 0.000105,
            "volume": 1200 + i * 100,
        })
    # 第 7 根突破并回踩不破 0.382，runner 应识别为 S4。
    rows.append({
        "timestamp": ts + 6 * 60,
        "open": 0.000115,
        "high": 0.000140,
        "low": 0.000110,
        "close": 0.000135,
        "volume": 3500,
    })
    rows.append({
        "timestamp": ts + 7 * 60,
        "open": 0.000135,
        "high": 0.000150,
        "low": 0.000125,
        "close": 0.000145,
        "volume": 4200,
    })
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "open", "high", "low", "close", "volume"])
        writer.writeheader()
        writer.writerows(rows)


def _build_kline_summary(tmp_path: Path) -> Path:
    root = tmp_path / "gmgn_candidates"
    token_dir = root / TOKEN_A
    kline_path = token_dir / "kline_1m.csv"
    accumulation_path = token_dir / "accumulation_outputs" / "accumulation_window.json"
    _write_kline(kline_path)
    _write_json(accumulation_path, {
        "token": TOKEN_A,
        "T_start": "2026-02-02 02:43:00 UTC",
        "T_start_timestamp": 1770000300,
        "T_end": "2026-02-02 02:47:00 UTC",
        "T_end_timestamp": 1770000420,
        "POC_price": 0.000112,
        "VAH_price": 0.000125,
        "VAL_price": 0.000098,
        "latest_AVWAP": 0.000108,
        "breakout_type": "突破最近LH，形成HL/HH",
        "window_status": "valid",
    })
    summary_path = root / "candidate_kline_pipeline_summary.json"
    _write_json(summary_path, {
        "模块": "SIKK 候选币 K线接入管道",
        "候选来源": "fake",
        "处理统计": {"读取候选数": 2, "处理候选数": 2, "成功数量": 1, "失败数量": 1},
        "处理结果": [
            {
                "代币地址": TOKEN_A,
                "代币符号": "GOOD",
                "筛选等级": "S3_进入SIKK结构分析",
                "输出目录": str(token_dir),
                "K线文件": {"1m": str(kline_path)},
                "吸筹窗口输出": str(accumulation_path),
                "状态": "ok",
            },
            {
                "代币地址": TOKEN_B,
                "代币符号": "BAD",
                "筛选等级": "S3_进入SIKK结构分析",
                "输出目录": str(root / TOKEN_B),
                "K线文件": {},
                "吸筹窗口输出": "",
                "状态": "failed",
                "错误": "K线缺失",
            },
        ],
    })
    return summary_path


def test_candidate_signal_pipeline_writes_readiness_outputs_and_summary(tmp_path):
    from sikk_candidate_signal_pipeline import run_candidate_signal_pipeline

    kline_summary = _build_kline_summary(tmp_path)
    result = run_candidate_signal_pipeline(kline_summary, output_root=tmp_path / "signal_outputs")

    summary_path = Path(result["summary_json"])
    csv_path = Path(result["summary_csv"])
    assert summary_path.exists()
    assert csv_path.exists()

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["处理统计"]["成功数量"] == 1
    assert summary["处理统计"]["跳过数量"] == 1
    row = summary["信号结果"][0]
    assert row["代币地址"] == TOKEN_A
    assert row["信号等级"] == "S4_强确认信号"
    assert row["风险门禁"] == "ALLOW_PAPER_TRADE_允许纸面交易"
    assert row["模式"] == "paper"
    assert Path(row["自动准备输出"]["json"]).exists()
    assert Path(row["自动准备输出"]["signal"]).exists()

    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        csv_rows = list(csv.DictReader(f))
    assert csv_rows[0]["代币地址"] == TOKEN_A
    assert csv_rows[0]["信号等级"] == "S4_强确认信号"


def test_candidate_signal_pipeline_is_paper_only_and_skips_failed_kline_items(tmp_path):
    from sikk_candidate_signal_pipeline import run_candidate_signal_pipeline

    kline_summary = _build_kline_summary(tmp_path)
    result = run_candidate_signal_pipeline(kline_summary, output_root=tmp_path / "signal_outputs")
    summary = json.loads(Path(result["summary_json"]).read_text(encoding="utf-8"))

    assert summary["说明"] == "本模块只生成 SIKK 自动交易准备/纸面信号，不执行真实 swap。"
    assert summary["处理统计"]["跳过数量"] == 1
    assert summary["跳过结果"][0]["代币地址"] == TOKEN_B
    assert summary["跳过结果"][0]["状态"] == "skipped"

    text = Path(result["summary_json"]).read_text(encoding="utf-8")
    assert "gmgn-cli swap" not in text
    assert "onchainos swap execute" not in text
