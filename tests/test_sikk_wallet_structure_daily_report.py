import csv
import json
from pathlib import Path


def _write_jsonl(path: Path, rows: list[dict]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    return path


def _write_csv(path: Path, rows: list[dict]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_wallet_structure_daily_report_groups_by_failure_type_and_wallet_status(tmp_path):
    from sikk_wallet_structure_daily_report import build_wallet_structure_daily_report

    closed_positions = _write_csv(
        tmp_path / "paper_positions_closed.csv",
        [
            {
                "position_id": "p1",
                "代币地址": "T1",
                "代币符号": "SUP1",
                "status": "CLOSED",
                "wallet_structure_status": "WALLET_SUPPORT",
                "signal_level": "S4_强确认信号",
                "最终收益率_pct": "35",
                "net_pnl_sol": "0.035",
                "最大浮盈_pct": "80",
                "最大浮亏_pct": "-10",
                "failure_type": "TAKE_PROFIT",
                "paper_position_sol": "0.01",
            },
            {
                "position_id": "p2",
                "代币地址": "T2",
                "代币符号": "SUP2",
                "status": "CLOSED",
                "wallet_structure_status": "WALLET_SUPPORT",
                "signal_level": "S3_策略观察信号",
                "最终收益率_pct": "-12",
                "net_pnl_sol": "-0.012",
                "最大浮盈_pct": "10",
                "最大浮亏_pct": "-25",
                "failure_type": "WALLET_EXIT",
                "paper_position_sol": "0.01",
            },
            {
                "position_id": "p3",
                "代币地址": "T3",
                "代币符号": "BLK1",
                "status": "CLOSED",
                "wallet_structure_status": "WALLET_BLOCK",
                "signal_level": "S4_强确认信号",
                "最终收益率_pct": "-22",
                "net_pnl_sol": "-0.022",
                "最大浮盈_pct": "5",
                "最大浮亏_pct": "-30",
                "failure_type": "SAME_SOURCE_EXIT",
                "paper_position_sol": "0.01",
            },
            {
                "position_id": "p4",
                "代币地址": "T4",
                "代币符号": "NEU1",
                "status": "CLOSED",
                "wallet_structure_status": "WALLET_NEUTRAL",
                "signal_level": "S3_策略观察信号",
                "最终收益率_pct": "8",
                "net_pnl_sol": "0.008",
                "最大浮盈_pct": "20",
                "最大浮亏_pct": "-8",
                "failure_type": "TIME_STOP",
                "paper_position_sol": "0.01",
            },
        ],
    )
    failure_attribution = _write_jsonl(
        tmp_path / "failure_attribution.jsonl",
        [
            {"事件类型": "FORCE_PAPER_EXIT", "代币地址": "T2", "failure_type": "WALLET_EXIT", "failure_reason": "早期钱包卖出增加", "wallet_structure_status": "WALLET_SUPPORT"},
            {"事件类型": "FORCE_PAPER_EXIT", "代币地址": "T3", "failure_type": "SAME_SOURCE_EXIT", "failure_reason": "同源组同步卖出", "wallet_structure_status": "WALLET_BLOCK"},
        ],
    )

    paths = build_wallet_structure_daily_report(
        closed_positions_path=closed_positions,
        failure_attribution_path=failure_attribution,
        output_dir=tmp_path / "reports",
        report_date="20260502",
    )

    summary = _read_json(Path(paths["summary_json"]))
    assert summary["总体统计"]["关闭仓位数"] == 4
    assert summary["总体统计"]["胜率_pct"] == 50.0
    assert summary["按钱包结构状态"]["WALLET_SUPPORT"]["关闭仓位数"] == 2
    assert summary["按钱包结构状态"]["WALLET_SUPPORT"]["胜率_pct"] == 50.0
    assert summary["按失败归因"]["SAME_SOURCE_EXIT"]["关闭仓位数"] == 1
    assert summary["按失败归因"]["SAME_SOURCE_EXIT"]["平均收益率_pct"] == -22.0
    assert summary["按钱包结构状态与信号等级"]["WALLET_SUPPORT|S4_强确认信号"]["平均收益率_pct"] == 35.0
    assert summary["failure_attribution事件统计"]["SAME_SOURCE_EXIT"] == 1
    audit = summary["审计统计"]
    assert audit["样本独立性审计"]["unique_token_count"] == 4
    assert audit["样本独立性审计"]["duplicate_token_count"] == 0
    assert audit["加权收益审计"]["position_size_weighted_return_pct"] == 2.25
    assert audit["退出政策审计"]["force_paper_exit_count"] == 2
    assert "shadow hold" in audit["shadow_hold审计"]["audit_note"]

    md = Path(paths["summary_md"]).read_text(encoding="utf-8")
    assert "SIKK 钱包结构纸面交易日报" in md
    assert "按钱包结构状态统计" in md
    assert "按失败归因统计" in md
    assert "不执行真实 swap" in md

    csv_rows = list(csv.DictReader(Path(paths["summary_csv"]).open(encoding="utf-8-sig")))
    assert any(row["统计类型"] == "wallet_structure_status" and row["分组"] == "WALLET_SUPPORT" for row in csv_rows)
    assert any(row["统计类型"] == "failure_type" and row["分组"] == "SAME_SOURCE_EXIT" for row in csv_rows)


def test_wallet_structure_daily_report_handles_missing_inputs_as_empty_report(tmp_path):
    from sikk_wallet_structure_daily_report import build_wallet_structure_daily_report

    paths = build_wallet_structure_daily_report(
        closed_positions_path=tmp_path / "missing_positions.csv",
        failure_attribution_path=tmp_path / "missing_failure.jsonl",
        output_dir=tmp_path / "reports",
        report_date="20260502",
    )

    summary = _read_json(Path(paths["summary_json"]))
    assert summary["总体统计"]["关闭仓位数"] == 0
    assert summary["按钱包结构状态"] == {}
    assert Path(paths["summary_md"]).exists()
