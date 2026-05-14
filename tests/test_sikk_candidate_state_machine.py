import csv
import json
from pathlib import Path


TOKEN_READY = "Ready11111111111111111111111111111111111111"
TOKEN_ACCUM = "Accum22222222222222222222222222222222222222"
TOKEN_WATCH = "Watch33333333333333333333333333333333333333"
TOKEN_BLOCK = "Block44444444444444444444444444444444444444"
TOKEN_FAIL = "Fail555555555555555555555555555555555555555"


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _build_inputs(tmp_path: Path) -> dict:
    root = tmp_path / "inputs"
    candidates = root / "token_candidates.json"
    kline = root / "candidate_kline_pipeline_summary.json"
    signals = root / "candidate_signal_summary.json"

    _write_json(candidates, {
        "候选结果": [
            {"代币地址": TOKEN_READY, "代币符号": "READY", "筛选等级": "S3_进入SIKK结构分析", "是否进入候选池": True},
            {"代币地址": TOKEN_ACCUM, "代币符号": "ACCUM", "筛选等级": "S3_进入SIKK结构分析", "是否进入候选池": True},
            {"代币地址": TOKEN_WATCH, "代币符号": "WATCH", "筛选等级": "S2_重点观察", "是否进入候选池": True},
            {"代币地址": TOKEN_BLOCK, "代币符号": "BLOCK", "筛选等级": "S3_进入SIKK结构分析", "是否进入候选池": True},
            {"代币地址": TOKEN_FAIL, "代币符号": "FAIL", "筛选等级": "S3_进入SIKK结构分析", "是否进入候选池": True},
        ]
    })

    ready_acc = root / TOKEN_READY / "accumulation_window.json"
    accum_acc = root / TOKEN_ACCUM / "accumulation_window.json"
    block_acc = root / TOKEN_BLOCK / "accumulation_window.json"
    _write_json(ready_acc, {"window_status": "valid", "T_start": "2026-01-01 00:01:00 UTC", "T_end": "2026-01-01 00:08:00 UTC", "POC_price": 0.1})
    _write_json(accum_acc, {"window_status": "pending", "T_start": "2026-01-01 00:02:00 UTC", "T_end": "", "POC_price": 0.2})
    _write_json(block_acc, {"window_status": "invalid", "T_start": "2026-01-01 00:02:00 UTC", "T_end": "", "POC_price": 0.3})

    _write_json(kline, {
        "处理结果": [
            {"代币地址": TOKEN_READY, "代币符号": "READY", "状态": "ok", "吸筹窗口输出": str(ready_acc)},
            {"代币地址": TOKEN_ACCUM, "代币符号": "ACCUM", "状态": "ok", "吸筹窗口输出": str(accum_acc)},
            {"代币地址": TOKEN_BLOCK, "代币符号": "BLOCK", "状态": "ok", "吸筹窗口输出": str(block_acc)},
            {"代币地址": TOKEN_FAIL, "代币符号": "FAIL", "状态": "failed", "错误": "K线缺失", "吸筹窗口输出": ""},
        ]
    })

    _write_json(signals, {
        "信号结果": [
            {"代币地址": TOKEN_READY, "代币符号": "READY", "信号等级": "S4_强确认信号", "风险门禁": "ALLOW_PAPER_TRADE_允许纸面交易", "建议纸面仓位SOL": 0.12, "策略类型": "SIKK-B 控盘箱体突破回踩", "信号时间": "2026-01-01 00:09:00 UTC"},
            {"代币地址": TOKEN_BLOCK, "代币符号": "BLOCK", "信号等级": "SX_失效信号", "风险门禁": "ALLOW_PAPER_TRADE_允许纸面交易", "建议纸面仓位SOL": 0, "策略类型": "风险监控", "信号时间": "2026-01-01 00:04:00 UTC"},
        ],
        "跳过结果": [
            {"代币地址": TOKEN_FAIL, "代币符号": "FAIL", "状态": "skipped", "原因": "上游 K线管道未成功"}
        ],
    })
    return {"candidates": candidates, "kline": kline, "signals": signals}


def test_candidate_state_machine_writes_all_outputs_and_states(tmp_path):
    from sikk_candidate_state_machine import run_candidate_state_machine

    inputs = _build_inputs(tmp_path)
    result = run_candidate_state_machine(
        candidates_path=inputs["candidates"],
        kline_summary_path=inputs["kline"],
        signal_summary_path=inputs["signals"],
        output_dir=tmp_path / "state_machine",
    )

    for key in ["states_json", "states_csv", "events_jsonl", "summary_md"]:
        assert Path(result[key]).exists()

    payload = json.loads(Path(result["states_json"]).read_text(encoding="utf-8"))
    states = {row["代币地址"]: row["当前状态"] for row in payload["候选状态"]}
    assert states[TOKEN_READY] == "PAPER_READY"
    assert states[TOKEN_ACCUM] == "ACCUMULATING"
    assert states[TOKEN_WATCH] == "WATCHING"
    assert states[TOKEN_BLOCK] == "BLOCKED"
    assert states[TOKEN_FAIL] == "FAILED"
    assert payload["状态统计"]["PAPER_READY"] == 1
    assert payload["状态统计"]["FAILED"] == 1

    with Path(result["states_csv"]).open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    assert rows[0]["代币地址"]
    assert "状态原因" in rows[0]


def test_candidate_state_machine_event_log_and_markdown_are_chinese_first(tmp_path):
    from sikk_candidate_state_machine import run_candidate_state_machine

    inputs = _build_inputs(tmp_path)
    result = run_candidate_state_machine(
        candidates_path=inputs["candidates"],
        kline_summary_path=inputs["kline"],
        signal_summary_path=inputs["signals"],
        output_dir=tmp_path / "state_machine",
    )

    events = [json.loads(line) for line in Path(result["events_jsonl"]).read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(events) == 5
    assert {e["to_state"] for e in events} >= {"PAPER_READY", "ACCUMULATING", "WATCHING", "BLOCKED", "FAILED"}

    md = Path(result["summary_md"]).read_text(encoding="utf-8")
    assert "# SIKK 候选币状态机汇总" in md
    assert "PAPER_READY" in md
    assert "不执行真实 swap" in md
    assert "gmgn-cli swap" not in md
