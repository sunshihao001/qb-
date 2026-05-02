import json
from pathlib import Path


TOKEN = "Pipe111111111111111111111111111111111111111"


def _fake_trenches_runner(cmd):
    joined = " ".join(cmd)
    assert "gmgn-cli market trenches" in joined
    assert "gmgn-cli swap" not in joined
    assert "order strategy create" not in joined
    return {
        "completed": [
            {
                "address": TOKEN,
                "symbol": "PIPE",
                "name": "Pipeline Token",
                "usd_market_cap": 180000,
                "liquidity": 35000,
                "volume_24h": 160000,
                "net_buy_24h": 18000,
                "net_inflow_24h": 18000,
                "swaps_24h": 260,
                "buys_24h": 170,
                "sells_24h": 60,
                "top_10_holder_rate": 0.24,
                "creator_balance_rate": 0.01,
                "top_rat_trader_percentage": 0.03,
                "bot_degen_rate": 0.11,
                "whale_hold_rate": 0.13,
                "creator_open_count": 2,
                "rug_ratio": 0.08,
                "top_bundler_trader_percentage": 0.03,
                "fresh_wallet_rate": 0.18,
                "wallet_tags_stat": {
                    "smart_wallets": 2,
                    "renowned_wallets": 1,
                    "sniper_wallets": 2,
                    "bundler_wallets": 1,
                    "fresh_wallets": 12,
                },
                "open_timestamp": 1770000000,
                "creation_timestamp": 1769999900,
                "total_supply": 1000000000,
                "launchpad_platform": "pump",
            }
        ]
    }


def _fake_kline_runner(cmd):
    joined = " ".join(cmd)
    assert "gmgn-cli market kline" in joined
    assert "swap" not in joined
    resolution = cmd[cmd.index("--resolution") + 1]
    start = int(cmd[cmd.index("--from") + 1])
    step = 60 if resolution == "1m" else 300
    candles = []
    price = 0.0001
    for i in range(80):
        # 构造一段温和抬升 K线，重点验证 orchestrator 跑通而非强行制造买点。
        close = price * (1 + 0.002 * i)
        open_ = close * 0.995
        high = close * 1.02
        low = close * 0.96
        volume = 6000 + i * 120
        candles.append({
            "time": (start + i * step) * 1000,
            "open": open_,
            "high": high,
            "low": low,
            "close": close,
            "volume": volume,
            "amount": volume / close,
        })
    return {"data": {"list": candles}}


def test_orchestrator_runs_full_pipeline_and_writes_manifest(tmp_path):
    from run_sikk_gmgn_pipeline import run_full_pipeline

    result = run_full_pipeline(
        output_root=tmp_path,
        trenches_runner=_fake_trenches_runner,
        kline_runner=_fake_kline_runner,
        include_s2=False,
        limit=10,
    )

    manifest_path = Path(result["manifest_json"])
    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest["模块"] == "SIKK-GMGN Pipeline Orchestrator v1.0"
    assert manifest["模式"] == "paper/readiness"
    assert manifest["阶段统计"]["新币筛选"]["进入候选池"] == 1
    assert manifest["阶段统计"]["K线吸筹管道"]["成功数量"] == 1
    assert manifest["阶段统计"]["信号管道"]["成功数量"] == 1
    assert manifest["阶段统计"]["状态机"]["候选数量"] == 1
    assert "不执行真实 swap" in manifest["说明"]

    assert Path(manifest["输出文件"]["候选池JSON"]).exists()
    assert Path(manifest["输出文件"]["K线管道汇总"]).exists()
    assert Path(manifest["输出文件"]["信号汇总JSON"]).exists()
    assert Path(manifest["输出文件"]["状态机JSON"]).exists()
    assert Path(manifest["输出文件"]["运行报告MD"]).exists()

    report = Path(manifest["输出文件"]["运行报告MD"]).read_text(encoding="utf-8")
    assert "SIKK-GMGN 一键管道运行报告" in report
    assert "执行边界" in report


def test_orchestrator_can_skip_signal_and_state_when_requested(tmp_path):
    from run_sikk_gmgn_pipeline import run_full_pipeline

    result = run_full_pipeline(
        output_root=tmp_path,
        trenches_runner=_fake_trenches_runner,
        kline_runner=_fake_kline_runner,
        run_signal=False,
        run_state=False,
    )
    manifest = json.loads(Path(result["manifest_json"]).read_text(encoding="utf-8"))
    assert manifest["阶段统计"]["信号管道"]["状态"] == "skipped"
    assert manifest["阶段统计"]["状态机"]["状态"] == "skipped"
    assert manifest["阶段统计"]["报价安全确认层"]["状态"] == "skipped"
    assert manifest["输出文件"]["信号汇总JSON"] == ""
    assert manifest["输出文件"]["状态机JSON"] == ""
    assert manifest["输出文件"]["报价安全汇总JSON"] == ""


def test_orchestrator_can_run_optional_quote_security_layer(tmp_path):
    from run_sikk_gmgn_pipeline import run_full_pipeline

    calls = []

    def fake_quote_security_runner(**kwargs):
        calls.append(kwargs)
        assert Path(kwargs["candidate_states_path"]).name == "candidate_states.json"
        assert Path(kwargs["signal_summary_path"]).name == "candidate_signal_summary.json"
        assert kwargs["wallet_address"] == "Wallet1111111111111111111111111111111111"
        assert kwargs["quote_sources"] == ("okx",)
        out = Path(kwargs["output_dir"])
        out.mkdir(parents=True, exist_ok=True)
        summary = out / "candidate_quote_security_summary.json"
        csv_path = out / "candidate_quote_security_summary.csv"
        md_path = out / "candidate_quote_security_summary.md"
        summary.write_text(json.dumps({
            "处理统计": {
                "读取状态数": 1,
                "PAPER_READY数量": 1,
                "成功数量": 1,
                "READY_FOR_CONFIRMATION": 1,
                "PAUSE": 0,
                "BLOCK": 0,
            },
            "说明": "本层只生成报价/安全确认文件，不执行真实 swap。",
        }, ensure_ascii=False), encoding="utf-8")
        csv_path.write_text("代币地址,交易前状态\nPipe11,READY_FOR_CONFIRMATION\n", encoding="utf-8")
        md_path.write_text("# 候选币报价安全确认层\n\n不执行真实 swap。\n", encoding="utf-8")
        return {"summary_json": str(summary), "summary_csv": str(csv_path), "summary_md": str(md_path)}

    result = run_full_pipeline(
        output_root=tmp_path,
        trenches_runner=_fake_trenches_runner,
        kline_runner=_fake_kline_runner,
        run_quote_security=True,
        quote_security_runner=fake_quote_security_runner,
        quote_sources=("okx",),
        wallet_address="Wallet1111111111111111111111111111111111",
        default_quote_amount_sol=0.01,
    )

    assert len(calls) == 1
    manifest = json.loads(Path(result["manifest_json"]).read_text(encoding="utf-8"))
    assert manifest["阶段统计"]["报价安全确认层"]["成功数量"] == 1
    assert manifest["输出文件"]["报价安全汇总JSON"].endswith("candidate_quote_security_summary.json")
    assert Path(manifest["输出文件"]["报价安全汇总JSON"]).exists()
    report = Path(manifest["输出文件"]["运行报告MD"]).read_text(encoding="utf-8")
    assert "报价 + 安全扫描 + 确认层" in report
    assert "不执行真实 swap" in report


def test_parse_args_uses_gmgn_wallet_env_as_default(monkeypatch):
    from run_sikk_gmgn_pipeline import parse_args

    wallet = "6m6dSTyv7aJQYJpAQKq2VnHjNtfj2mE5KFSJNevHjgSp"
    monkeypatch.setenv("GMGN_WALLET_ADDRESS", wallet)
    monkeypatch.setattr("sys.argv", ["run_sikk_gmgn_pipeline.py"])

    args = parse_args()

    assert args.wallet_address == wallet


def test_parse_args_reads_gmgn_wallet_from_config_env_file(monkeypatch, tmp_path):
    from run_sikk_gmgn_pipeline import parse_args

    wallet = "6m6dSTyv7aJQYJpAQKq2VnHjNtfj2mE5KFSJNevHjgSp"
    config_dir = tmp_path / ".config" / "gmgn"
    config_dir.mkdir(parents=True)
    (config_dir / ".env").write_text(f"GMGN_WALLET_ADDRESS={wallet}\n", encoding="utf-8")
    monkeypatch.delenv("GMGN_WALLET_ADDRESS", raising=False)
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setattr("sys.argv", ["run_sikk_gmgn_pipeline.py"])

    args = parse_args()

    assert args.wallet_address == wallet


def test_parse_args_wallet_cli_overrides_env(monkeypatch):
    from run_sikk_gmgn_pipeline import parse_args

    env_wallet = "6m6dSTyv7aJQYJpAQKq2VnHjNtfj2mE5KFSJNevHjgSp"
    cli_wallet = "Wallet1111111111111111111111111111111111"
    monkeypatch.setenv("GMGN_WALLET_ADDRESS", env_wallet)
    monkeypatch.setattr("sys.argv", ["run_sikk_gmgn_pipeline.py", "--wallet-address", cli_wallet])

    args = parse_args()

    assert args.wallet_address == cli_wallet
