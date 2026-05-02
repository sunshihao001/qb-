import json
from pathlib import Path

from tests.test_run_sikk_gmgn_pipeline import _fake_kline_runner, _fake_trenches_runner


def test_orchestrator_runs_wallet_structure_layer_before_quote_security(tmp_path):
    from run_sikk_gmgn_pipeline import run_full_pipeline

    calls = {"wallet": [], "quote": []}

    def fake_wallet_structure_runner(**kwargs):
        calls["wallet"].append(kwargs)
        out = Path(kwargs["output_dir"])
        out.mkdir(parents=True, exist_ok=True)
        summary = out / "candidate_wallet_structure_summary.json"
        csv_path = out / "candidate_wallet_structure_summary.csv"
        md_path = out / "candidate_wallet_structure_summary.md"
        summary.write_text(json.dumps({
            "统计": {"处理数量": 1, "WALLET_SUPPORT": 1},
            "处理结果": [{
                "代币地址": "Pipe111111111111111111111111111111111111111",
                "钱包结构结论": "WALLET_SUPPORT",
                "钱包结构系数": 1.0,
                "钱包结构评分": 45,
                "钱包风险评分": 10,
                "建议状态调整": "保持或允许 PAPER_READY",
                "状态调整原因": "E3/E4 正向结构钱包仍有持仓或结果证据",
            }],
        }, ensure_ascii=False), encoding="utf-8")
        csv_path.write_text("代币地址,钱包结构结论\nPipe11...1111,WALLET_SUPPORT\n", encoding="utf-8")
        md_path.write_text("# SIKK 候选币钱包结构门禁汇总\n", encoding="utf-8")
        return {"summary_json": str(summary), "summary_csv": str(csv_path), "summary_md": str(md_path)}

    def fake_quote_security_runner(**kwargs):
        calls["quote"].append(kwargs)
        states = json.loads(Path(kwargs["candidate_states_path"]).read_text(encoding="utf-8"))
        ready = [row for row in states["候选状态"] if row["当前状态"] == "PAPER_READY"]
        assert ready
        assert ready[0]["钱包结构结论"] == "WALLET_SUPPORT"
        out = Path(kwargs["output_dir"])
        out.mkdir(parents=True, exist_ok=True)
        summary = out / "candidate_quote_security_summary.json"
        csv_path = out / "candidate_quote_security_summary.csv"
        md_path = out / "candidate_quote_security_summary.md"
        summary.write_text(json.dumps({"处理统计": {"成功数量": 1}, "处理结果": []}, ensure_ascii=False), encoding="utf-8")
        csv_path.write_text("代币地址,交易前状态\n", encoding="utf-8")
        md_path.write_text("# 候选币报价安全确认层\n", encoding="utf-8")
        return {"summary_json": str(summary), "summary_csv": str(csv_path), "summary_md": str(md_path)}

    result = run_full_pipeline(
        output_root=tmp_path,
        trenches_runner=_fake_trenches_runner,
        kline_runner=_fake_kline_runner,
        run_wallet_structure=True,
        wallet_structure_runner=fake_wallet_structure_runner,
        run_quote_security=True,
        quote_security_runner=fake_quote_security_runner,
        wallet_address="Wallet1111111111111111111111111111111111",
    )

    assert len(calls["wallet"]) == 1
    assert len(calls["quote"]) == 1
    assert Path(calls["wallet"][0]["candidate_states_path"]).name == "candidate_states.json"
    manifest = json.loads(Path(result["manifest_json"]).read_text(encoding="utf-8"))
    assert manifest["阶段统计"]["钱包结构门禁"]["处理数量"] == 1
    assert manifest["输出文件"]["钱包结构汇总JSON"].endswith("candidate_wallet_structure_summary.json")
    assert Path(manifest["输出文件"]["钱包结构汇总JSON"]).exists()
