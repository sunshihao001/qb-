import json
from pathlib import Path

import sikk_dashboard_site_builder as builder


def test_dashboard_data_contract_from_live_run_outputs():
    base = Path('data/gmgn_candidates_live_run')
    data = builder.build_dashboard_data(base)
    required = [
        'meta',
        'metadata',
        'kpi',
        'funnel',
        'tokens',
        'opportunities',
        'wallet_structure_summary',
        'wallet_missing_reasons',
        'entry_block_reasons',
        'paper_positions',
        'events',
        'system_health',
        'methodology',
        'sections',
    ]
    assert all(key in data for key in required)
    assert data['metadata']['boundary'].startswith('只读静态观察控制台')
    assert data['meta']['boundary'] == data['metadata']['boundary']
    assert isinstance(data['tokens'], list)
    assert data['kpi']['token_count'] == len(data['tokens'])
    assert data['paper_positions']['open_count'] == len(data['paper_positions']['open'])
    assert data['paper_positions']['closed_count'] == len(data['paper_positions']['closed'])
    assert data['system_health']['token_count'] == len(data['tokens'])
    assert 'coverage_diagnostics' in data
    diagnostics = data['coverage_diagnostics']
    for key in ['wallet_coverage', 'wallet_missing_count', 'wallet_missing_rate_pct', 'wallet_missing_repair_plan', 'paper_json_csv_sync', 'safety_defaults']:
        assert key in diagnostics
    assert diagnostics['safety_defaults']['real_swap_enabled'] is False
    assert diagnostics['safety_defaults']['broadcast_allowed'] is False
    for section in ['总控台', '候选漏斗', '重点机会', '代币总表', '单币详情', '纸面验证区']:
        assert section in data['sections']


def test_wallet_missing_reason_is_explainable_for_missing_wallet_rows():
    assert builder.infer_wallet_missing_reason('WATCHING', 'UNKNOWN', 'MISSING') == 'WAIT_SIGNAL'
    assert builder.infer_wallet_missing_reason('BLOCKED', 'S4_强确认信号', 'MISSING') == 'BLOCKED_BEFORE_WALLET'
    assert builder.infer_wallet_missing_reason('PAPER_READY', 'S4_强确认信号', 'MISSING') == 'NO_WALLET_INPUT'


def test_write_site_files_uses_chinese_labels_for_user_visible_dashboard(tmp_path):
    data = builder.build_dashboard_data(Path('data/gmgn_candidates_live_run'))
    builder.write_site_files(tmp_path, data)
    app_text = (tmp_path / 'app.js').read_text(encoding='utf-8')
    index_text = (tmp_path / 'index.html').read_text(encoding='utf-8')
    combined = index_text + app_text

    for text in [
        '候选币总数',
        '钱包结构覆盖',
        '开放纸面仓位',
        '已关闭胜率',
        '平均关闭收益',
        '候选漏斗',
        '代币总表',
        '搜索代币 / 原因',
        '下一步：',
        '入场价',
        '纸面买入时间',
        '纸面买入数量',
        '入场市值',
        '信号时间',
        '信号价格',
        '当前价',
        '当前收益',
        '控制台加载失败',
    ]:
        assert text in combined

    for english_label in [
        'Wallet Coverage',
        'Open Positions',
        'Closed Win Rate',
        'Avg Closed PnL',
        'Token 总表',
        'Pipeline 漏斗',
        'Next:',
        'Entry:',
        'Current:',
        'PnL:',
        'Dashboard load failed',
    ]:
        assert english_label not in combined


def test_write_site_files_builds_visual_console_v2_sections_and_interactions(tmp_path):
    data = builder.build_dashboard_data(Path('data/gmgn_candidates_live_run'))
    builder.write_site_files(tmp_path, data)
    app_text = (tmp_path / 'app.js').read_text(encoding='utf-8')
    index_text = (tmp_path / 'index.html').read_text(encoding='utf-8')
    css_text = (tmp_path / 'style.css').read_text(encoding='utf-8')
    dashboard_json = json.loads((tmp_path / 'dashboard_data.json').read_text(encoding='utf-8'))
    combined = index_text + app_text + css_text

    for text in [
        'SIKK-SOL Visual Console v2',
        '总控台',
        '覆盖诊断',
        '钱包结构缺口修复计划',
        'JSON/CSV 同步',
        '安全默认关闭',
        '候选漏斗',
        '重点机会',
        '代币总表',
        '单币详情',
        '纸面验证区',
        '系统健康',
        '最新事件',
        '自动刷新',
        '刷新时间',
        '状态筛选',
        '钱包筛选',
        '纸面筛选',
        '原因搜索',
        '优先级排序',
        '点击任意代币查看详情',
        '钱包结构表现',
        '失败原因 Top',
    ]:
        assert text in combined

    for js_hook in [
        "setInterval(loadData",
        "renderDetail",
        "sortByPriority",
        "stateFilter",
        "walletFilter",
        "paperFilter",
        "reasonInput",
    ]:
        assert js_hook in app_text

    assert 'system_health' in dashboard_json
    assert 'meta' in dashboard_json
    assert dashboard_json['system_health']['token_count'] == len(dashboard_json['tokens'])


def test_paper_positions_expose_entry_evidence_fields():
    data = builder.build_dashboard_data(Path('data/gmgn_candidates_live_run'))
    open_positions = data['paper_positions']['open']
    assert open_positions
    row = open_positions[0]
    for field in [
        'paper_entry_time',
        'paper_position_sol',
        'paper_entry_price',
        'paper_current_price',
        'paper_stop_price',
        'paper_signal_time',
        'paper_signal_price',
        'paper_pnl_pct',
    ]:
        assert field in row
    assert row['paper_entry_time']
    assert float(row['paper_position_sol']) > 0
    assert float(row['paper_entry_price']) > 0


def test_write_site_files_displays_paper_entry_evidence(tmp_path):
    data = builder.build_dashboard_data(Path('data/gmgn_candidates_live_run'))
    builder.write_site_files(tmp_path, data)
    app_text = (tmp_path / 'app.js').read_text(encoding='utf-8')
    for text in [
        '纸面买入 / 模拟持仓证据',
        '纸面买入时间',
        '纸面买入数量',
        '入场市值',
        '发现市值',
        '信号市值',
        '当前市值',
        '止损价',
        '剩余仓位',
        '更新时间',
    ]:
        assert text in app_text


def test_dashboard_data_contains_sikk_methodology_stages_and_rules():
    data = builder.build_dashboard_data(Path('data/gmgn_candidates_live_run'))
    methodology = data['methodology']
    assert methodology['boundary'].startswith('纸面验证')
    stages = methodology['stages']
    assert len(stages) >= 8
    for required_stage in ['P0_候选发现', 'P1_K线吸筹与信号', 'P2_钱包结构门禁', 'P3_报价安全确认', 'P4_纸面买入', 'P5_持仓监控与退出', 'P6_复盘校准', 'P7_人工确认后小额实盘准备']:
        assert any(stage['stage_id'] == required_stage for stage in stages)
    for stage in stages:
        for field in ['stage_id', 'stage_name', 'goal', 'entry_condition', 'checks', 'pass_condition', 'block_condition', 'outputs', 'token_fields']:
            assert field in stage
        assert stage['checks']
        assert stage['outputs']
    assert 'BLOCK_BUY' in methodology['risk_gate_rules']
    assert 'ALLOW_PAPER_TRADE' in methodology['risk_gate_rules']
    assert 'S3' in methodology['signal_rules']
    assert 'S4' in methodology['signal_rules']
    assert 'SX' in methodology['signal_rules']
    assert methodology['position_sizing']['max_position_sol'] == 0.2
    assert methodology['exit_plan']['take_profit_steps']


def test_write_site_files_displays_methodology_flow_and_stage_evidence(tmp_path):
    data = builder.build_dashboard_data(Path('data/gmgn_candidates_live_run'))
    builder.write_site_files(tmp_path, data)
    combined = (tmp_path / 'index.html').read_text(encoding='utf-8') + (tmp_path / 'app.js').read_text(encoding='utf-8')
    for text in [
        '方法论流程',
        '阶段证据核对',
        '风险门禁规则',
        '信号等级规则',
        '仓位计算',
        '退出计划',
        '只读，不执行真实 swap',
        'renderMethodology',
        'renderStageEvidence',
    ]:
        assert text in combined
    rendered_data = (tmp_path / 'dashboard_data.json').read_text(encoding='utf-8')
    for text in [
        'P0 候选发现',
        'P1 K线吸筹与信号',
        'P2 钱包结构门禁',
        'P3 报价安全确认',
        'P4 纸面买入',
        'P5 持仓监控与退出',
        'P6 复盘校准',
        'ALLOW_PAPER_TRADE',
        'BLOCK_BUY',
        'S3',
        'S4',
        'SX',
    ]:
        assert text in rendered_data



def test_dashboard_paper_lab_exposes_entry_quality_and_wallet_exit_policy():
    data = builder.build_dashboard_data(Path('data/gmgn_candidates_live_run'))
    assert 'wallet_exit_policy' in data['methodology']
    assert data['methodology']['wallet_exit_policy']['default_action'] == 'EXIT_MONITOR'
    assert data['methodology']['wallet_exit_policy']['require_delta_snapshots'] == 2
    assert 'entry_quality_summary' in data['paper_positions']
    assert 'wallet_exit_effectiveness' in data['paper_positions']
    for row in data['paper_positions']['open']:
        for field in ['market_cap_context_status', 'entry_delay_from_discovery_sec', 'entry_market_cap_change_from_discovery_pct', 'paper_size_usd', 'estimated_token_amount']:
            assert field in row


def test_write_site_files_displays_entry_quality_and_wallet_exit_policy(tmp_path):
    data = builder.build_dashboard_data(Path('data/gmgn_candidates_live_run'))
    builder.write_site_files(tmp_path, data)
    combined = (tmp_path / 'app.js').read_text(encoding='utf-8') + (tmp_path / 'dashboard_data.json').read_text(encoding='utf-8')
    for text in ['入场质量统计', '市值分桶', '发现到入场延迟', '钱包退出策略', '默认 EXIT_MONITOR', '强证据才 FORCE_PAPER_EXIT', '影子持仓复盘', 'market_cap_context_status', 'wallet_exit_effectiveness']:
        assert text in combined



def test_dashboard_paper_positions_expose_case_file_links(tmp_path):
    from sikk_dashboard_site_builder import build_dashboard_data, write_site_files

    base = tmp_path / "run"
    paper_dir = base / "paper_live"
    case_dir = paper_dir / "case_files"
    case_dir.mkdir(parents=True)
    (paper_dir / "paper_positions_open.json").write_text(json.dumps({"open_positions": [{
        "position_id": "paper-case-1",
        "token_address": "TokenCase111",
        "token_symbol": "CASE",
        "status": "OPEN",
        "paper_entry_time": "2026-05-03T12:20:02Z",
    }]}, ensure_ascii=False), encoding="utf-8")
    (paper_dir / "paper_positions_closed.json").write_text(json.dumps({"closed_positions": []}, ensure_ascii=False), encoding="utf-8")
    source_md = case_dir / "paper-case-1.md"
    source_json = case_dir / "paper-case-1.json"
    source_md.write_text("# CASE 实战档案\n\n什么时候发现：2026-05-03T12:20:02Z\n为什么入场：纸面验证。\n", encoding="utf-8")
    source_json.write_text(json.dumps({"position_id": "paper-case-1", "token_symbol": "CASE", "why_entry": "纸面验证"}, ensure_ascii=False), encoding="utf-8")
    (case_dir / "case_files_manifest.json").write_text(json.dumps({"case_files": [{
        "position_id": "paper-case-1",
        "token_address": "TokenCase111",
        "case_file_json": str(source_json),
        "case_file_md": str(source_md),
    }]}, ensure_ascii=False), encoding="utf-8")

    data = build_dashboard_data(base)
    row = data["paper_positions"]["open"][0]
    assert row["case_file_json"].endswith("paper-case-1.json")
    assert row["case_file_md"].endswith("paper-case-1.md")
    assert "case_quality_level" in row
    assert "case_completeness_score" in row
    assert "evidence_missing_fields" in row
    assert "case_field_source_count" in row
    out = tmp_path / "site"
    write_site_files(out, data)
    site_data = json.loads((out / "dashboard_data.json").read_text(encoding="utf-8"))
    site_row = site_data["paper_positions"]["open"][0]

    # 网站里必须使用静态站点可访问的相对路径，不能暴露 data/... 或绝对路径；并且文件要真实复制到 site/case_files。
    assert site_row["case_file_md"] == "case_files/paper-case-1.html"
    assert site_row["case_file_json"] == "case_files/paper-case-1.json"
    html_text = (out / site_row["case_file_md"]).read_text(encoding="utf-8")
    assert '<meta charset="utf-8">' in html_text
    assert "CASE 实战档案" in html_text
    assert (out / "case_files/paper-case-1.md").read_text(encoding="utf-8").startswith("# CASE 实战档案")
    assert json.loads((out / site_row["case_file_json"]).read_text(encoding="utf-8"))["token_symbol"] == "CASE"

    app = (out / "app.js").read_text(encoding="utf-8")
    assert "case_file_md" in app
    assert "实战档案" in app
    assert "Case File 质量与证据缺口" in app
    assert "档案质量" in app
    assert "字段来源数" in app
    assert "缺失证据" in app
    assert 'href="${fmt(p.case_file_md)}"' in app



def test_dashboard_data_exposes_live_and_signal_pnl_metrics_for_paper_positions(tmp_path):
    from sikk_dashboard_site_builder import build_dashboard_data

    base = tmp_path / "run"
    paper_dir = base / "paper_live"
    paper_dir.mkdir(parents=True)
    (paper_dir / "paper_positions_open.json").write_text(json.dumps({"open_positions": [{
        "token_address": "TokenDualPnL111",
        "token_symbol": "DUAL",
        "status": "OPEN",
        "paper_entry_time": "2026-05-03T12:20:02Z",
        "paper_entry_price": 1.0,
        "current_price": 1.4,
        "live_pnl_pct": 40.0,
        "signal_pnl_pct": 28.0,
        "entry_price_mode": "live",
        "entry_raw_quote_price": 0.98,
        "entry_simulated_price": 1.0,
    }]}, ensure_ascii=False), encoding="utf-8")
    (paper_dir / "paper_positions_closed.json").write_text(json.dumps({"closed_positions": []}, ensure_ascii=False), encoding="utf-8")
    (paper_dir / "strategy_metrics.json").write_text(json.dumps({"统计": {"当前开放仓位数": 1, "累计关闭仓位数": 0, "已关闭胜率_pct": 0.0, "已关闭平均收益率_pct": 0.0}}, ensure_ascii=False), encoding="utf-8")

    data = build_dashboard_data(base)
    row = data["paper_positions"]["open"][0]
    assert row["entry_price_mode"] == "live"
    assert row["live_pnl_pct"] == 40.0
    assert row["signal_pnl_pct"] == 28.0
    assert data["strategy_panel"]["entry_price_mode_counts"]["live"] == 1
    assert data["strategy_panel"]["live_signal_pnl_gap_avg_pct"] == 12.0


def test_write_site_files_displays_strategy_panel_and_dual_pnl_metrics(tmp_path):
    from sikk_dashboard_site_builder import build_dashboard_data, write_site_files

    base = tmp_path / "run"
    paper_dir = base / "paper_live"
    paper_dir.mkdir(parents=True)
    (paper_dir / "paper_positions_open.json").write_text(json.dumps({"open_positions": [{
        "token_address": "TokenStrategy111",
        "token_symbol": "STRAT",
        "status": "OPEN",
        "paper_entry_time": "2026-05-03T12:20:02Z",
        "paper_entry_price": 1.0,
        "current_price": 1.5,
        "live_pnl_pct": 50.0,
        "signal_pnl_pct": 35.0,
        "entry_price_mode": "live",
    }]}, ensure_ascii=False), encoding="utf-8")
    (paper_dir / "paper_positions_closed.json").write_text(json.dumps({"closed_positions": [{
        "token_address": "TokenClosed111",
        "token_symbol": "CLOSE",
        "status": "CLOSED",
        "final_pnl_pct": 18.0,
        "signal_level": "S4",
        "failure_type": "DATA_QUALITY_FAIL",
    }]}, ensure_ascii=False), encoding="utf-8")
    (paper_dir / "strategy_metrics.json").write_text(json.dumps({"统计": {"当前开放仓位数": 1, "累计关闭仓位数": 1, "已关闭胜率_pct": 100.0, "已关闭平均收益率_pct": 18.0}}, ensure_ascii=False), encoding="utf-8")
    (paper_dir / "failure_attribution.jsonl").write_text(json.dumps({"代币地址": "TokenClosed111", "failure_type": "DATA_QUALITY_FAIL", "failure_reason": "数据质量不足"}, ensure_ascii=False) + "\n", encoding="utf-8")

    data = build_dashboard_data(base)
    write_site_files(tmp_path / "site", data)
    combined = (tmp_path / "site" / "index.html").read_text(encoding="utf-8") + (tmp_path / "site" / "app.js").read_text(encoding="utf-8") + (tmp_path / "site" / "dashboard_data.json").read_text(encoding="utf-8")
    for text in [
        '策略评估面板',
        '日报概览',
        '信号表现',
        '失败原因 Top',
        'live 平均收益',
        'signal 平均收益',
        'entry_price_mode_counts',
        'live_signal_pnl_gap_avg_pct',
    ]:
        assert text in combined


def test_strategy_panel_includes_daily_grouping_for_reports(tmp_path):
    from sikk_dashboard_site_builder import build_dashboard_data

    base = tmp_path / 'run'
    paper_dir = base / 'paper_live'
    paper_dir.mkdir(parents=True)
    (paper_dir / 'paper_positions_open.json').write_text(json.dumps({"open_positions": [
        {
            "token_address": "TokenDayA",
            "token_symbol": "DAYA",
            "status": "OPEN",
            "paper_entry_time": "2026-05-01T01:02:03Z",
            "paper_entry_price": 1.0,
            "live_pnl_pct": 20.0,
            "signal_pnl_pct": 10.0,
            "entry_price_mode": "live",
            "signal_level": "S3",
            "wallet_structure_status": "WALLET_SUPPORT",
            "failure_type": "HOLD",
        },
        {
            "token_address": "TokenDayB",
            "token_symbol": "DAYB",
            "status": "OPEN",
            "paper_entry_time": "2026-05-01T08:09:10Z",
            "paper_entry_price": 1.0,
            "live_pnl_pct": -5.0,
            "signal_pnl_pct": -2.0,
            "entry_price_mode": "signal",
            "signal_level": "SX",
            "wallet_structure_status": "WALLET_BLOCK",
            "failure_type": "WALLET_BLOCK",
        },
        {
            "token_address": "TokenDayC",
            "token_symbol": "DAYC",
            "status": "OPEN",
            "paper_entry_time": "2026-05-02T01:02:03Z",
            "paper_entry_price": 1.0,
            "live_pnl_pct": 30.0,
            "signal_pnl_pct": 18.0,
            "entry_price_mode": "live",
            "signal_level": "S4",
            "wallet_structure_status": "WALLET_NEUTRAL",
            "failure_type": "HOLD",
        }
    ]}, ensure_ascii=False), encoding="utf-8")
    (paper_dir / "paper_positions_closed.json").write_text(json.dumps({"closed_positions": []}, ensure_ascii=False), encoding="utf-8")
    (paper_dir / "strategy_metrics.json").write_text(json.dumps({"统计": {"当前开放仓位数": 3, "累计关闭仓位数": 0, "已关闭胜率_pct": 0.0, "已关闭平均收益率_pct": 0.0}}, ensure_ascii=False), encoding="utf-8")

    data = build_dashboard_data(base)
    panel = data['strategy_panel']
    assert 'daily_groups' in panel
    assert 'signal_groups' in panel
    assert 'wallet_groups' in panel
    assert panel['daily_groups']['2026-05-01']['count'] == 2
    assert panel['daily_groups']['2026-05-01']['entry_price_mode_counts']['live'] == 1
    assert panel['daily_groups']['2026-05-01']['failure_reason_top']['HOLD'] == 1
    assert panel['daily_groups']['2026-05-02']['avg_live_pnl_pct'] == 30.0
    assert panel['daily_groups']['2026-05-02']['win_rate_pct'] == 100.0
    assert panel['signal_groups']['S3']['count'] == 1
    assert panel['signal_groups']['S3']['avg_live_pnl_pct'] == 20.0
    assert panel['signal_groups']['SX']['win_rate_pct'] == 0.0
    assert panel['signal_groups']['S4']['count'] == 1
    assert panel['signal_groups']['S4']['occurrence_pct'] == 33.3333
    assert panel['wallet_groups']['WALLET_SUPPORT']['count'] == 1
    assert panel['wallet_groups']['WALLET_BLOCK']['avg_signal_pnl_pct'] == -2.0
    assert panel['wallet_groups']['WALLET_NEUTRAL']['win_rate_pct'] == 100.0


def test_write_site_files_renders_grouped_strategy_sections(tmp_path):
    from sikk_dashboard_site_builder import build_dashboard_data, write_site_files

    base = tmp_path / 'run'
    paper_dir = base / 'paper_live'
    paper_dir.mkdir(parents=True)
    (paper_dir / 'paper_positions_open.json').write_text(json.dumps({"open_positions": [
        {
            "token_address": "TokenGroupA",
            "token_symbol": "GRPA",
            "status": "OPEN",
            "paper_entry_time": "2026-05-01T01:02:03Z",
            "paper_entry_price": 1.0,
            "live_pnl_pct": 12.0,
            "signal_pnl_pct": 8.0,
            "entry_price_mode": "live",
            "signal_level": "S3",
            "wallet_structure_status": "WALLET_SUPPORT",
        },
        {
            "token_address": "TokenGroupB",
            "token_symbol": "GRPB",
            "status": "OPEN",
            "paper_entry_time": "2026-05-02T01:02:03Z",
            "paper_entry_price": 1.0,
            "live_pnl_pct": -4.0,
            "signal_pnl_pct": -2.0,
            "entry_price_mode": "signal",
            "signal_level": "SX",
            "wallet_structure_status": "WALLET_BLOCK",
        }
    ]}, ensure_ascii=False), encoding='utf-8')
    (paper_dir / "paper_positions_closed.json").write_text(json.dumps({"closed_positions": []}, ensure_ascii=False), encoding='utf-8')
    (paper_dir / "strategy_metrics.json").write_text(json.dumps({"统计": {"当前开放仓位数": 2, "累计关闭仓位数": 0, "已关闭胜率_pct": 0.0, "已关闭平均收益率_pct": 0.0}}, ensure_ascii=False), encoding='utf-8')

    data = build_dashboard_data(base)
    write_site_files(tmp_path / 'site', data)
    combined = (tmp_path / 'site' / 'index.html').read_text(encoding='utf-8') + (tmp_path / 'site' / 'app.js').read_text(encoding='utf-8') + (tmp_path / 'site' / 'dashboard_data.json').read_text(encoding='utf-8')
    for text in [
        '信号分层',
        '钱包结构分层',
        '出现次数',
        'live 平均收益',
        'signal 平均收益',
        'strategySignalCards',
        'strategyWalletBars',
        'S3 观察信号',
        'S4 强信号',
        'SX 风险/排除信号',
        '出现率',
    ]:
        assert text in combined
