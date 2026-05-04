from pathlib import Path

import sikk_query


def test_build_query_index_exposes_board_and_token_detail():
    base = Path('data/gmgn_candidates_live_run')
    index = sikk_query.build_query_index(base)

    assert index['boundary'].startswith('只读统一查询层')
    assert index['board']['token_count'] >= 0
    assert 'paper_open_count' in index['board']
    assert 'coverage_diagnostics' in index
    assert 'paper_json_csv_sync' in index['coverage_diagnostics']
    assert isinstance(index['tokens'], list)
    assert isinstance(index['paper_positions']['open'], list)

    if index['paper_positions']['open']:
        token = index['paper_positions']['open'][0]['token_address']
        detail = sikk_query.get_token_detail(index, token)
        assert detail['token_address'] == token
        assert detail['paper_position'] is not None
        assert 'case_file_md' in detail['paper_position']
        assert 'stage_evidence' in detail
        assert 'next_action' in detail


def test_token_detail_can_match_symbol_or_address_case_insensitive():
    base = Path('data/gmgn_candidates_live_run')
    index = sikk_query.build_query_index(base)
    assert index['tokens']
    row = index['tokens'][0]
    query = row.get('token_symbol') or row.get('token_address')

    detail = sikk_query.get_token_detail(index, query.lower())

    assert detail['token_address'] == row['token_address']
    assert detail['token_symbol'] == row['token_symbol']


def test_format_token_detail_is_chinese_and_explains_missing_evidence():
    base = Path('data/gmgn_candidates_live_run')
    index = sikk_query.build_query_index(base)
    row = index['tokens'][0]
    detail = sikk_query.get_token_detail(index, row['token_address'])
    text = sikk_query.format_token_detail(detail)

    for label in ['代币', '状态', '钱包结构', '纸面仓位', '证据质量', '下一步动作', '安全边界']:
        assert label in text
    assert '不执行真实 swap' in text


def test_cli_board_and_token_commands(tmp_path):
    base = Path('data/gmgn_candidates_live_run')
    board_text = sikk_query.run_cli(['board', '--base-dir', str(base)])
    assert 'SIKK 统一查询层总览' in board_text
    assert '候选币总数' in board_text
    assert '覆盖诊断' in board_text
    assert 'JSON/CSV 同步' in board_text

    index = sikk_query.build_query_index(base)
    token = index['tokens'][0]['token_address']
    token_text = sikk_query.run_cli(['token', token, '--base-dir', str(base)])
    assert 'SIKK 单币详情' in token_text
    assert token in token_text
