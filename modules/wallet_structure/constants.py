
from __future__ import annotations

PACKAGE_NAME = 'wallet_structure'
SCHEMA_VERSION = '1.0.0'
DEFAULT_CHAIN = 'sol'
DEFAULT_MAX_WALLETS = 100
INTEL_BOT_ROOT = 'data/gmgn_candidates_live_run/intel-bot'
INTEL_BOT_CODE_DIR = f'{INTEL_BOT_ROOT}/code'
INTEL_BOT_LOG_DIR = f'{INTEL_BOT_ROOT}/logs'

OUTPUT_FILENAMES = [
    'wallet_raw_snapshot.csv',
    'wallet_normalized.csv',
    'wallet_role_classification.csv',
    'wallet_funding_edges.csv',
    'wallet_token_flow_edges.csv',
    'same_source_groups.csv',
    'distribution_paths.csv',
    'backflow_paths.csv',
    'gmgn_note_table.csv',
    'wallet_structure_decision.json',
    'wallet_structure_report.md',
    'bundle_manifest.json',
]

ROLE_TO_CODE = {
    '疑似新钱包狙击': 'NEW_SNIPER',
    '疑似临时执行钱包': 'TEMP_EXEC',
    '疑似同源执行组成员': 'SAME_SRC_MEMBER',
    '疑似 Token 接收钱包': 'DIST_RECV',
    '疑似分发派发钱包': 'DIST_SEND',
    '疑似利润回收钱包': 'PROFIT_BACKFLOW',
    '疑似核心资金源候选': 'CORE_FUND_SRC',
    '疑似结果钱包': 'RESULT_WALLET',
    '疑似接盘鲸鱼': 'BAG_WHALE',
    '疑似套牢钱包': 'TRAPPED_HOLDER',
    '可疑中转节点': 'SUSPICIOUS_TRANSIT',
    '基础设施地址': 'INFRA',
    '普通参与者': 'NORMAL',
    '噪音钱包': 'NOISE',
    # legacy aliases retained for import compatibility; user-visible values are normalized to Chinese judgement names.
    '新钱包狙击': 'NEW_SNIPER',
    '临时执行钱包': 'TEMP_EXEC',
    '同源执行组成员': 'SAME_SRC_MEMBER',
    '分发接收钱包': 'DIST_RECV',
    '分发派发钱包': 'DIST_SEND',
    '利润回流节点': 'PROFIT_BACKFLOW',
    '核心资金源候选': 'CORE_FUND_SRC',
    '结果钱包': 'RESULT_WALLET',
    '接盘鲸鱼': 'BAG_WHALE',
    '套牢钱包': 'TRAPPED_HOLDER',
    'LP/池子/路由器/基础设施': 'INFRA',
    '普通交易钱包': 'NORMAL',
}

CANONICAL_ROLE_BY_CODE = {
    'NEW_SNIPER': '疑似新钱包狙击',
    'TEMP_EXEC': '疑似临时执行钱包',
    'SAME_SRC_MEMBER': '疑似同源执行组成员',
    'DIST_RECV': '疑似 Token 接收钱包',
    'DIST_SEND': '疑似分发派发钱包',
    'PROFIT_BACKFLOW': '疑似利润回收钱包',
    'CORE_FUND_SRC': '疑似核心资金源候选',
    'RESULT_WALLET': '疑似结果钱包',
    'BAG_WHALE': '疑似接盘鲸鱼',
    'TRAPPED_HOLDER': '疑似套牢钱包',
    'SUSPICIOUS_TRANSIT': '可疑中转节点',
    'INFRA': '基础设施地址',
    'NORMAL': '普通参与者',
    'NOISE': '噪音钱包',
}

CODE_TO_ROLE = CANONICAL_ROLE_BY_CODE.copy()
