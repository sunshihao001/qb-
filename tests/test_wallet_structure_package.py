
import json
from pathlib import Path

def _fake_collector(token_address, token_symbol=''):
    return [
        {
            'address': 'W1',
            'tags': ['smart_degen'],
            'maker_token_tags': ['transfer_in'],
            'sell_amount_percentage': 0.1,
            'amount_percentage': 0.18,
            'profit': 5200,
            'transfer_in': True,
            'native_transfer': {'from_address': 'FUND1'},
            'token_transfer_in': {'address': 'SRC1'},
            'token_transfer_out': {'address': 'DST1'},
            'funding_source_type': 'wallet',
            'holder_rank': 1,
            'amount': 180000,
            'amount_percentage': 0.18,
            'usd_value': 36000,
            'top10_holder_pct': 0.42,
            'top20_holder_pct': 0.58,
            'holder_count': 1200,
            'holder_delta': 25,
        },
        {
            'address': 'W2',
            'tags': ['bundler'],
            'maker_token_tags': ['bundler'],
            'sell_amount_percentage': 0.88,
            'amount_percentage': 0.07,
            'profit': -1200,
            'transfer_in': True,
            'native_transfer': {'from_address': 'FUND1'},
            'token_transfer_in': {'address': 'SRC1'},
            'holder_rank': 2,
            'amount': 70000,
            'amount_percentage': 0.07,
            'usd_value': 14000,
            'top10_holder_pct': 0.42,
            'top20_holder_pct': 0.58,
            'holder_count': 1200,
            'holder_delta': 25,
        },
        {
            'address': 'W3',
            'tags': [],
            'maker_token_tags': ['rat_trader'],
            'sell_amount_percentage': 0.5,
            'amount_percentage': 0.03,
            'profit': 0,
            'transfer_in': False,
            'holder_rank': 3,
            'amount': 30000,
            'amount_percentage': 0.03,
            'usd_value': 6000,
            'top10_holder_pct': 0.42,
            'top20_holder_pct': 0.58,
            'holder_count': 1200,
            'holder_delta': 25,
        },
    ]

def test_package_exports_and_end_to_end_bundle(tmp_path):
    from modules.wallet_structure import WalletStructureInput, build_bundle_from_request

    request = WalletStructureInput(
        token_address='Token111111111111111111111111111111111111',
        token_symbol='ABC',
        analysis_time='2026-05-04T12:00:00Z',
        discovery_time='2026-05-04T11:55:00Z',
        include_funding_source=True,
        include_token_flow=True,
    ).to_dict()

    out = build_bundle_from_request(request, collector=_fake_collector, output_dir=tmp_path / 'bundle')
    required = [
        'wallet_raw_snapshot_csv', 'wallet_normalized_csv', 'wallet_role_classification_csv',
        'wallet_funding_edges_csv', 'wallet_token_flow_edges_csv', 'same_source_groups_csv',
        'distribution_paths_csv', 'backflow_paths_csv', 'gmgn_note_table_csv',
        'wallet_structure_decision_json', 'wallet_structure_report_md', 'bundle_manifest_json',
        'holder_snapshot_normalized_json', 'wallet_structure_normalized_json',
    ]
    for key in required:
        assert Path(out[key]).exists(), key

    decision = json.loads(Path(out['wallet_structure_decision_json']).read_text(encoding='utf-8'))
    assert decision['token_address'] == request['token_address']
    assert decision['bot_scope'] == 'WALLET_EVIDENCE_PACKET_ONLY'
    assert decision['evidence_packet']['packet_type'] == 'wallet_structure_evidence_packet'
    assert decision['wallet_structure_status'] in {'WALLET_SUPPORT', 'WALLET_PAUSE', 'WALLET_BLOCK', 'WALLET_UNKNOWN'}
    assert 'wallet_structure_factor' in decision
    assert 'recommended_state_action' in decision
    assert isinstance(decision['evidence_chain'], list)
    assert decision['gmgn_note_file'].endswith('gmgn_note_table.csv')
    holders = json.loads(Path(out['holder_snapshot_normalized_json']).read_text(encoding='utf-8'))
    assert holders[0]['token_address'] == request['token_address']
    for key in ['snapshot_time', 'holder_rank', 'wallet_address', 'holding_amount', 'holding_pct', 'holding_value_usd', 'top10_holder_pct', 'top20_holder_pct', 'holder_count', 'holder_delta']:
        assert key in holders[0]
    wallet_structure = json.loads(Path(out['wallet_structure_normalized_json']).read_text(encoding='utf-8'))
    assert wallet_structure['token_address'] == request['token_address']
    assert wallet_structure['intel_bot_usage_zh'] == ['结构侧剩余库存', 'Top Holder 稳定性', '对手盘承接', '筹码迁移']
    assert wallet_structure['holder_metrics']['top10_holder_pct'] == 0.42

def test_normalizer_and_classifier_create_stable_role_fields():
    from modules.wallet_structure.normalizer import normalize_wallet_row
    from modules.wallet_structure.role_classifier import classify_wallet_row

    row = normalize_wallet_row(
        {
            'address': 'W1',
            'tags': ['smart_degen'],
            'maker_token_tags': ['transfer_in'],
            'sell_amount_percentage': 0.12,
            'amount_percentage': 0.20,
            'profit': 8000,
            'transfer_in': True,
            'native_transfer': {'from_address': 'SRC1'},
        },
        token_address='TokenX',
        token_symbol='ABC',
    )
    result = classify_wallet_row(row)
    assert row['wallet_address'] == 'W1'
    assert row['token_address'] == 'TokenX'
    assert result.role_name in {'疑似 Token 接收钱包', '疑似结果钱包', '普通参与者'}
    assert result.role_code
    assert result.evidence_level
    assert result.risk_level
    assert result.tracking_level

def test_user_visible_wallet_outputs_are_chinese(tmp_path):
    from modules.wallet_structure import WalletStructureInput, build_bundle_from_request

    request = WalletStructureInput(token_address='TokenZh11111111111111111111111111111111111', token_symbol='中文测', analysis_time='2026-05-04T12:00:00Z').to_dict()
    out = build_bundle_from_request(request, collector=_fake_collector, output_dir=tmp_path / 'zh_bundle')
    decision = json.loads(Path(out['wallet_structure_decision_json']).read_text(encoding='utf-8'))
    report = Path(out['wallet_structure_report_md']).read_text(encoding='utf-8')
    notes = Path(out['gmgn_note_table_csv']).read_text(encoding='utf-8-sig')

    assert decision['wallet_structure_status_zh'] in {'钱包结构支持', '钱包结构中性', '钱包结构暂停', '钱包结构阻断', '钱包结构未知'}
    assert decision['wallet_evidence_level_zh']
    assert decision['recommended_state_action_zh'] in {'忽略', '观察', '跟踪', '重点跟踪', '高风险监控', '写入历史库', '生成 GMGN 备注', '进入后续门禁', '暂停等待刷新', '阻断进入交易流程'}
    assert 'SIKK 钱包结构证据包' in report
    assert 'Bot 边界：' in report
    assert '不直接判断主导侧动机、对手盘压力或派发是否完成' in report
    assert '新狙' in notes or '分发' in notes or '普通' in notes

def test_evidence_packet_boundary_excludes_deterministic_operator_claims(tmp_path):
    from modules.wallet_structure import WalletStructureInput, build_bundle_from_request

    request = WalletStructureInput(token_address='TokenScope111111111111111111111111111111111', token_symbol='SCOPE', analysis_time='2026-05-04T12:00:00Z').to_dict()
    out = build_bundle_from_request(request, collector=_fake_collector, output_dir=tmp_path / 'scope_bundle')
    decision = json.loads(Path(out['wallet_structure_decision_json']).read_text(encoding='utf-8'))
    packet = decision['evidence_packet']
    rendered = json.dumps(packet, ensure_ascii=False)

    assert '确定庄家' not in json.dumps({k: v for k, v in packet.items() if k != 'scope_limits_zh'}, ensure_ascii=False)
    assert any('不输出确定庄家' in item for item in packet['scope_limits_zh'])
    assert packet['field_coverage']['standardized_wallet_rows'] >= 1
    assert packet['time_alignment']['analysis_time'] == request['analysis_time']
    assert packet['traceability']
    assert decision['dominant_side_status_zh'] == '仅供下游模型参考，不由钱包证据包直接裁决'
    assert decision['chip_transfer_status_zh'] == '仅保留候选筹码流向证据，不判断派发是否完成'

def test_decision_json_is_manifest_and_compatible(tmp_path):
    from modules.wallet_structure import WalletStructureInput, build_bundle_from_request

    request = WalletStructureInput(token_address='Token222222222222222222222222222222222222', token_symbol='DEF', analysis_time='2026-05-04T12:00:00Z').to_dict()
    out = build_bundle_from_request(request, collector=_fake_collector, output_dir=tmp_path / 'bundle2')
    manifest = json.loads(Path(out['bundle_manifest_json']).read_text(encoding='utf-8'))
    assert manifest['wallet_structure_decision']['wallet_structure_status']
    assert manifest['files']['wallet_structure_decision.json'] == out['wallet_structure_decision_json']
    assert manifest['schema_version']

def test_default_wallet_bundle_output_stays_under_intel_bot_directory(monkeypatch, tmp_path):
    from modules.wallet_structure import WalletStructureInput, build_bundle_from_request

    monkeypatch.chdir(tmp_path)
    request = WalletStructureInput(
        token_address='TokenIntelDir111111111111111111111111111111',
        token_symbol='IBOT',
        analysis_time='2026-05-04T12:00:00Z',
    ).to_dict()

    out = build_bundle_from_request(request, collector=_fake_collector)

    expected_root = tmp_path / 'data' / 'gmgn_candidates_live_run' / 'intel-bot' / 'logs' / 'wallet_structure' / request['token_address']
    assert Path(out['wallet_structure_decision_json']).resolve().parent == expected_root
    assert Path(out['wallet_structure_report_md']).resolve().parent == expected_root
    assert not (tmp_path / 'data' / 'gmgn_candidates_live_run' / 'wallet_structure').exists()
