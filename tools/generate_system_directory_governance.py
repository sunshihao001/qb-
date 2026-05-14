#!/usr/bin/env python3
"""Generate SIKK-GMGN directory governance package from current file inventory.
Copy-only planning: does not move/delete/copy project files.
"""
import csv, fnmatch, hashlib, json, os, re, sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path('/root/sikk-gmgn')
OUT = ROOT / 'reports/review_ops_bot/audit/system_directory_governance_20260506'
LEGACY = ROOT / 'legacy_compat'
DOCS = ROOT / 'docs'
INV = ROOT / 'reports/review_ops_bot/audit/system_directory_inventory/system_directory_file_inventory_20260506.md'
NOW = datetime.now().isoformat(timespec='seconds')

SECRET_PAT = re.compile(r'(api[_-]?key|secret|private[_-]?key|password|token|authorization|bearer)', re.I)
TOKEN_PAT = re.compile(r'([1-9A-HJ-NP-Za-km-z]{32,44})')

CANONICAL_DIRS = {
    'ai_context/': {'decision':'KEEP', 'label':'ai_context', 'owner':'shared', 'purpose':'AI 上下文材料；只读参考，不作为运行输出主路径。'},
    'audits/': {'decision':'LEGACY_KEEP', 'label':'audit_legacy', 'owner':'review_ops_bot', 'purpose':'历史审计材料；新审计报告主写 reports/review_ops_bot/audit/<asset_id>/。'},
    'config/': {'decision':'KEEP_RESTRICTED', 'label':'config_sensitive', 'owner':'shared', 'purpose':'配置文件；敏感值不得输出。'},
    'contracts/': {'decision':'KEEP', 'label':'contract', 'owner':'shared', 'purpose':'跨模块 / 跨 Bot 合同；新 shared 合同写 contracts/shared 或 contracts/bot_handoff。'},
    'data/': {'decision':'KEEP_WITH_ROUTING', 'label':'runtime_data', 'owner':'multi_bot', 'purpose':'运行数据根；新输出必须 data/<bot>/<mode>/<asset_id>/。'},
    'docs/': {'decision':'KEEP', 'label':'system_doc', 'owner':'shared', 'purpose':'系统文档、宪法、规则、设计说明。'},
    'imports/': {'decision':'KEEP', 'label':'import_staging', 'owner':'review_ops_bot', 'purpose':'外部资料 staging；新导入写 imports/staging/<import_id>/。'},
    'knowledge/': {'decision':'KEEP_REVIEW', 'label':'knowledge_base', 'owner':'shared', 'purpose':'知识库/吸收后资料；后续可 copy-only 到 research_loop/methodology。'},
    'legacy_compat/': {'decision':'KEEP', 'label':'legacy_compat_index', 'owner':'shared', 'purpose':'旧路径兼容索引；只放 manifest/path map/fallback，不存大数据。'},
    'logs/': {'decision':'KEEP_REVIEW', 'label':'logs', 'owner':'review_ops_bot', 'purpose':'日志；新日志按 bot/data manifest 或 reports audit 归档。'},
    'modules/': {'decision':'KEEP', 'label':'code', 'owner':'multi_bot', 'purpose':'功能代码模块；新代码必须 modules/<bot_or_domain>/。'},
    'outputs/': {'decision':'LEGACY_KEEP', 'label':'legacy_output', 'owner':'legacy', 'purpose':'旧输出目录；不作为新主写路径。'},
    'reports/': {'decision':'KEEP', 'label':'human_report', 'owner':'review_ops_bot', 'purpose':'人类可读报告与审计报告总索引。'},
    'research_loop/': {'decision':'KEEP', 'label':'methodology_or_long_task', 'owner':'shared', 'purpose':'方法论、长任务、checkpoint、资料吸收循环。'},
    'schemas/': {'decision':'KEEP', 'label':'schema', 'owner':'shared', 'purpose':'系统级 schema；模块 schema 写 modules/<bot>/schemas。'},
    'scripts/': {'decision':'KEEP_REVIEW', 'label':'script_tooling', 'owner':'shared', 'purpose':'辅助脚本；新功能代码优先 modules，新项目工具可 tools/scripts。'},
    'tasks/': {'decision':'LEGACY_KEEP', 'label':'legacy_task', 'owner':'review_ops_bot', 'purpose':'历史任务材料；新任务包写 research_loop/task_packages。'},
    'tests/': {'decision':'KEEP', 'label':'test', 'owner':'shared', 'purpose':'自动化测试。'},
    'tools/': {'decision':'KEEP', 'label':'project_tool', 'owner':'shared', 'purpose':'项目工具脚本。'},
    '结构分析/': {'decision':'LEGACY_KEEP', 'label':'legacy_behavior_material', 'owner':'legacy', 'purpose':'旧结构分析资料/备份；只兼容读取或 copy-only。'},
    '钱包数据分析/': {'decision':'LEGACY_KEEP', 'label':'legacy_wallet_material', 'owner':'legacy', 'purpose':'旧钱包数据分析资料/备份；只兼容读取或 copy-only。'},
}

ASSET_LABELS = {
    'methodology': '方法论/判断规则/反证/统计模型/字段映射',
    'code': '功能代码',
    'test': '自动化测试',
    'schema': 'Schema/结构合同',
    'contract': '跨模块/跨 Bot 合同',
    'runtime_data_source_wallet': 'Source 钱包事实运行数据',
    'runtime_data_intel': 'Intel 结构推断运行数据',
    'runtime_data_legacy': '旧 live runtime/token 输出',
    'report': '人类可读报告/审计报告',
    'import_staging': '外部导入 staging',
    'legacy_compat': '旧路径兼容索引',
    'config_sensitive': '敏感配置',
    'log': '日志',
    'root_doc': '根目录状态/入口文档',
    'unknown_review': '待人工确认',
}

ACTIONS = ['KEEP','LEGACY_KEEP','COPY_TO_NEW','INDEX_ONLY','REVIEW','KEEP_RESTRICTED','KEEP_WITH_ROUTING']

DENY_WRITE = [
    '/root/sikk-gmgn/*.json', '/root/sikk-gmgn/*.csv', '/root/sikk-gmgn/*.md',
    '/root/sikk-gmgn/data/gmgn_candidates_live_run/**',
    '/root/sikk-gmgn/outputs/**', '/root/sikk-gmgn/结构分析/**', '/root/sikk-gmgn/钱包数据分析/**',
    '/root/sikk-gmgn/data/source_wallet_bot/*.json', '/root/sikk-gmgn/data/*/*.json',
    '/root/sikk-gmgn/reports/*.json', '/root/sikk-gmgn/modules/*/*_runtime_output.json',
    '/root/sikk-gmgn/config/**',
]
ALLOW_ROOT_EXC = ['AGENTS.md','README.md','SIKK_*.md','sikk_*.py','run_sikk_gmgn_pipeline.py']


def rel(p):
    return str(p.relative_to(ROOT))

def ext(p):
    return p.suffix.lower()

def top_dir(r):
    parts = r.split('/')
    if len(parts)==1: return './'
    return parts[0] + '/'

def token_from_path(r):
    m = TOKEN_PAT.search(r)
    return m.group(1) if m else None

def asset_id_for(r):
    tok = token_from_path(r)
    if tok: return tok
    parts = r.split('/')
    for part in reversed(parts[:-1]):
        if part and part not in ('data','reports','audit','review_ops_bot','modules','docs','research_loop','methodology','legacy','live','ad_hoc','staging'):
            return part[:80]
    return 'general'

def classify(r, is_dir=False):
    name = Path(r).name
    e = Path(r).suffix.lower()
    td = top_dir(r)
    # root
    if '/' not in r:
        if name in ('AGENTS.md','README.md') or fnmatch.fnmatch(name,'SIKK_*.md'):
            return 'root_doc','KEEP','./','shared','根目录允许的项目状态/入口文档'
        if name.endswith('.py') and (name.startswith('sikk_') or name=='run_sikk_gmgn_pipeline.py'):
            return 'code','KEEP','modules/<bot_or_domain>/ 或保留薄入口脚本','shared','既有入口脚本保留；新代码不再写根目录'
        if name.startswith('.'):
            return 'config_sensitive' if SECRET_PAT.search(name) else 'unknown_review','REVIEW','docs/ 或 config/','shared','隐藏/兼容文件需人工确认'
        return 'unknown_review','REVIEW','research_loop/plans/<task>.md','shared','根目录散文件需人工确认'
    # top-level dirs
    if r.startswith('config/'):
        return 'config_sensitive','KEEP_RESTRICTED','config/','shared','配置文件只保留，不输出敏感值'
    if r.startswith('modules/'):
        if '/schemas/' in r or e == '.json' and 'schema' in name.lower(): return 'schema','KEEP',r,'module','模块 schema/代码资产'
        if '/contracts/' in r: return 'contract','KEEP',r,'module','模块合同'
        return 'code','KEEP',r,'module','功能代码模块'
    if r.startswith('tests/'):
        return 'test','KEEP',r,'shared','测试文件'
    if r.startswith('contracts/'):
        return 'contract','KEEP',r,'shared','跨模块/跨 Bot 合同'
    if r.startswith('schemas/'):
        return 'schema','KEEP',r,'shared','系统级 schema'
    if r.startswith('docs/'):
        return 'system_doc','KEEP',r,'shared','系统文档/宪法/规则'
    if r.startswith('research_loop/methodology/'):
        return 'methodology','KEEP',r,'shared','方法论资产'
    if r.startswith('research_loop/'):
        return 'methodology','KEEP',r,'shared','长任务/方法轮/状态资产'
    if r.startswith('imports/'):
        return 'import_staging','KEEP',r,'review_ops_bot','导入 staging 或导入资产'
    if r.startswith('legacy_compat/'):
        return 'legacy_compat','KEEP',r,'shared','旧路径兼容索引'
    if r.startswith('reports/'):
        return 'report','KEEP',r,'review_ops_bot','人类可读报告/审计报告'
    if r.startswith('audits/'):
        return 'report','LEGACY_KEEP',f'reports/review_ops_bot/audit/{asset_id_for(r)}/','review_ops_bot','历史审计材料，旧路径保留'
    if r.startswith('knowledge/'):
        return 'methodology','COPY_TO_NEW','research_loop/methodology/','shared','知识库资料可 copy-only 方法论化'
    if r.startswith('outputs/'):
        return 'runtime_data_legacy','LEGACY_KEEP','legacy_compat/path_maps/outputs_to_new_layout.json','legacy','旧输出目录不再扩大'
    if r.startswith('tasks/'):
        return 'methodology','LEGACY_KEEP','research_loop/task_packages/legacy/<task_id>/','review_ops_bot','历史任务材料旧路径保留'
    if r.startswith('logs/'):
        return 'log','REVIEW','reports/review_ops_bot/logs/<asset_id>/','review_ops_bot','日志需按来源归档'
    if r.startswith('tools/') or r.startswith('scripts/'):
        return 'code','KEEP_REVIEW','tools/ 或 modules/<domain>/','shared','工具/脚本保留，新功能入 modules'
    if r.startswith('ai_context/'):
        return 'methodology','INDEX_ONLY','research_loop/methodology/passports/','shared','AI 上下文只索引/护照化，不直接搬大文件'
    if r.startswith('结构分析/'):
        return 'runtime_data_legacy','LEGACY_KEEP','legacy_compat/path_maps/legacy_behavior_to_intel.json','legacy','旧结构分析资料，只兼容读取/copy-only'
    if r.startswith('钱包数据分析/'):
        return 'runtime_data_legacy','LEGACY_KEEP','legacy_compat/path_maps/legacy_wallet_to_source.json','legacy','旧钱包资料，只兼容读取/copy-only'
    if r.startswith('data/gmgn_candidates_live_run/'):
        name_l = name.lower()
        tok = token_from_path(r) or '<asset_id>'
        if 'wallet' in name_l or name in ('wallet_structure_normalized.json','chip_distribution_summary.json','same_source_groups.json','fund_flow_edges.csv','address_history.json','wallet_fact_report.md'):
            return 'runtime_data_source_wallet','COPY_TO_NEW',f'data/source_wallet_bot/legacy/{tok}/','source_wallet_bot','legacy runtime 钱包事实 copy-only 到 Source'
        if 'dominant' in name_l or 'behavior' in name_l or 'intel' in r:
            return 'runtime_data_intel','COPY_TO_NEW',f'data/intel_bot/legacy/{tok}/','intel_bot','legacy runtime 结构推断 copy-only 到 Intel'
        if 'paper' in name_l or 'dashboard' in name_l or 'site' in r or 'state_machine' in name_l:
            return 'runtime_data_legacy','INDEX_ONLY','legacy_compat/path_maps/gmgn_candidates_live_run_legacy.json','legacy','paper/dashboard/state_machine 旧输出只索引，不反推事实'
        return 'runtime_data_legacy','LEGACY_KEEP','legacy_compat/path_maps/gmgn_candidates_live_run_legacy.json','legacy','历史混合运行区保留，不作为新写入'
    if r.startswith('data/source_wallet_bot/'):
        return 'runtime_data_source_wallet','KEEP',r,'source_wallet_bot','Source 新主路径运行数据'
    if r.startswith('data/intel_bot/'):
        return 'runtime_data_intel','KEEP',r,'intel_bot','Intel 新主路径运行数据'
    if r.startswith('data/'):
        return 'runtime_data_legacy','REVIEW','data/<bot>/<mode>/<asset_id>/','multi_bot','data 下未识别运行数据需确认 bot/mode/asset_id'
    return 'unknown_review','REVIEW','research_loop/plans/<task>.md','shared','无法自动归类，需人工确认'

def sha256_small(path, max_bytes=1024*1024):
    try:
        if path.stat().st_size > max_bytes: return ''
        h = hashlib.sha256()
        with path.open('rb') as f: h.update(f.read())
        return h.hexdigest()
    except Exception: return ''

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (LEGACY/'manifests').mkdir(parents=True, exist_ok=True)
    (LEGACY/'path_maps').mkdir(parents=True, exist_ok=True)
    (LEGACY/'read_fallbacks').mkdir(parents=True, exist_ok=True)
    rows=[]
    for p in ROOT.rglob('*'):
        # skip .git and generated huge recursive old audit? include reports but not .git
        if '.git' in p.parts: continue
        if p.is_dir(): continue
        r=rel(p)
        label, action, target, owner, note = classify(r)
        rows.append({
            'current_path': r,
            'file_name': p.name,
            'size_bytes': p.stat().st_size,
            'ext': p.suffix.lower(),
            'top_dir': top_dir(r),
            'asset_label': label,
            'owner_bot_or_domain': owner,
            'asset_id': asset_id_for(r),
            'suggested_action': action,
            'suggested_target': target,
            'legacy_read_allowed': action in ('LEGACY_KEEP','COPY_TO_NEW','INDEX_ONLY'),
            'copy_only_allowed': action == 'COPY_TO_NEW',
            'deny_new_write_here': any(fnmatch.fnmatch(str(ROOT/r), pat) or fnmatch.fnmatch(r, pat) for pat in DENY_WRITE),
            'sensitive_name': bool(SECRET_PAT.search(r)),
            'note': note,
            'sha256_if_small': sha256_small(p),
        })
    # CSV matrix
    matrix_csv = OUT/'file_routing_matrix_20260506.csv'
    with matrix_csv.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    # JSON compact index without sha? keep all
    safe_rows = [{k:v for k,v in row.items() if k!='sha256_if_small'} for row in rows]
    (OUT/'file_routing_matrix_20260506.json').write_text(json.dumps({'generated_at':NOW,'root':str(ROOT),'count':len(rows),'rows':safe_rows}, ensure_ascii=False, indent=2), encoding='utf-8')
    # Markdown summary top + selected all? Don't dump 7k rows, point to csv/json
    counts_label=Counter(r['asset_label'] for r in rows)
    counts_action=Counter(r['suggested_action'] for r in rows)
    counts_top=Counter(r['top_dir'] for r in rows)
    # governance docs
    official = {
        'generated_at': NOW,
        'project_root': str(ROOT),
        'directory_decisions': CANONICAL_DIRS,
        'asset_labels': ASSET_LABELS,
        'actions': {a: {'description': {
            'KEEP':'当前位置合理，保留并允许按宪法继续使用',
            'LEGACY_KEEP':'旧路径保留，不删除不移动，不再扩大',
            'COPY_TO_NEW':'后续按 manifest copy-only 到新规范目录，旧文件保留',
            'INDEX_ONLY':'只进入兼容索引，不搬大文件/旧 runtime',
            'REVIEW':'需要人工确认 bot/domain/asset_id 后再处理',
            'KEEP_RESTRICTED':'保留但敏感受限，禁止输出密钥值',
            'KEEP_WITH_ROUTING':'根目录保留，但子路径必须按路由写入'
        }[a]} for a in ACTIONS},
    }
    (OUT/'directory_official_decisions_20260506.json').write_text(json.dumps(official, ensure_ascii=False, indent=2), encoding='utf-8')
    md = ['# SIKK-GMGN 目录治理正式裁决 20260506','',f'- generated_at: {NOW}',f'- project_root: `{ROOT}`','', '## 1. 每个目录的正式裁决','']
    for d,meta in CANONICAL_DIRS.items():
        md += [f'### `{d}`', f'- 正式裁决: `{meta["decision"]}`', f'- 归属标签: `{meta["label"]}`', f'- owner: `{meta["owner"]}`', f'- 用途: {meta["purpose"]}', '']
    md += ['## 2. 每类文件的归属标签','']
    for k,v in ASSET_LABELS.items(): md += [f'- `{k}`: {v}']
    md += ['', '## 3. 动作定义','']
    for a in ACTIONS: md += [f'- `{a}`: {official["actions"][a]["description"]}']
    (OUT/'directory_official_decisions_20260506.md').write_text('\n'.join(md)+'\n', encoding='utf-8')

    routing = {
        'generated_at': NOW,
        'new_task_write_routes': {
            'methodology': 'research_loop/methodology/{subtype}/{asset_id}.{ext}',
            'plan': 'research_loop/plans/{task_name}.md',
            'state': 'research_loop/state/{task_id}/loop_state.json',
            'task_package': 'research_loop/task_packages/{status}/{task_id}/',
            'source_wallet_runtime': 'data/source_wallet_bot/{mode}/{token_address}/',
            'source_wallet_report': 'reports/source_wallet_bot/{mode}/{token_address}/',
            'intel_runtime': 'data/intel_bot/{mode}/{token_address}/',
            'intel_report': 'reports/intel_bot/{mode}/{token_address}/',
            'strategy_gate_runtime': 'data/strategy_gate_bot/{mode}/{token_address}/',
            'review_audit_report': 'reports/review_ops_bot/audit/{asset_id}/',
            'code': 'modules/{bot_or_domain}/',
            'test': 'tests/test_{module}_{feature}.py',
            'schema': 'modules/{bot}/schemas/{schema_name}.json OR schemas/shared/{schema_name}.json',
            'contract': 'modules/{bot}/contracts/{name}.md OR contracts/bot_handoff/{name}.md',
            'import_staging': 'imports/staging/{import_id}/',
            'legacy_manifest': 'legacy_compat/manifests/{manifest_name}.json',
            'legacy_path_map': 'legacy_compat/path_maps/{map_name}.json',
            'legacy_read_fallback': 'legacy_compat/read_fallbacks/{fallback_name}.md',
        },
        'required_prewrite_questions': ['bot_or_domain','asset_class','asset_id','route_key','target_path','is_legacy_copy_only'],
        'default_mode': 'ad_hoc',
        'legacy_mode': 'legacy',
    }
    (OUT/'new_task_write_routing_table_20260506.json').write_text(json.dumps(routing, ensure_ascii=False, indent=2), encoding='utf-8')
    (DOCS/'new_task_write_routing_table.json').write_text(json.dumps(routing, ensure_ascii=False, indent=2), encoding='utf-8')

    forbidden = {'generated_at':NOW,'deny_write_patterns':DENY_WRITE,'allowed_root_file_exceptions':ALLOW_ROOT_EXC,'rules':['禁止删除旧文件','禁止移动旧文件','禁止在 legacy runtime 扩大新主输出','禁止从 paper/dashboard/report 反推 Source/Intel 事实','config 下敏感值不得输出']}
    (OUT/'forbidden_write_paths_20260506.json').write_text(json.dumps(forbidden, ensure_ascii=False, indent=2), encoding='utf-8')
    (DOCS/'forbidden_write_paths.json').write_text(json.dumps(forbidden, ensure_ascii=False, indent=2), encoding='utf-8')

    fallback = {
        'generated_at': NOW,
        'default_policy': 'new_path_first_legacy_fallback_read_only',
        'rules': [
            {'legacy_path':'data/gmgn_candidates_live_run/**','allowed_reader':'review_ops_bot/audit 或 copy-only migrator','fallback_allowed':True,'write_allowed':False,'note':'混合旧 runtime，只读兼容，不作为新主写路径'},
            {'legacy_path':'outputs/**','allowed_reader':'legacy migrator/review_ops_bot','fallback_allowed':True,'write_allowed':False,'note':'旧输出目录，只索引或 copy-only'},
            {'legacy_path':'结构分析/**','allowed_reader':'intel_bot legacy adapter/review_ops_bot','fallback_allowed':True,'write_allowed':False,'note':'旧结构分析资料，只读兼容'},
            {'legacy_path':'钱包数据分析/**','allowed_reader':'source_wallet_bot legacy adapter/review_ops_bot','fallback_allowed':True,'write_allowed':False,'note':'旧钱包事实资料，只读兼容'},
            {'legacy_path':'audits/**','allowed_reader':'review_ops_bot','fallback_allowed':True,'write_allowed':False,'note':'历史审计只读'},
        ],
        'resolution_order': ['new canonical path','manifest old_path->new_path','legacy_compat/path_maps','legacy read fallback path'],
        'must_record': ['reader_name','legacy_path','reason','new_target_if_copy','read_time'],
    }
    (OUT/'legacy_read_fallback_rules_20260506.json').write_text(json.dumps(fallback, ensure_ascii=False, indent=2), encoding='utf-8')
    (LEGACY/'read_fallbacks/system_legacy_read_fallback_rules_20260506.md').write_text('# Legacy 路径兼容读取规则 20260506\n\n```json\n'+json.dumps(fallback, ensure_ascii=False, indent=2)+'\n```\n', encoding='utf-8')

    copy_plan=[]
    for row in rows:
        if row['suggested_action']=='COPY_TO_NEW':
            copy_plan.append({'old_path': row['current_path'], 'new_path_template': row['suggested_target'], 'asset_label': row['asset_label'], 'owner': row['owner_bot_or_domain'], 'asset_id': row['asset_id'], 'status':'planned_copy_only', 'delete_old':False, 'move_old':False})
    copy_manifest={'generated_at':NOW,'policy':'copy_only_no_delete_no_move','planned_count':len(copy_plan),'items':copy_plan[:5000], 'truncated': len(copy_plan)>5000}
    (OUT/'copy_only_migration_plan_20260506.json').write_text(json.dumps(copy_manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    (LEGACY/'manifests/copy_only_migration_plan_20260506.json').write_text(json.dumps(copy_manifest, ensure_ascii=False, indent=2), encoding='utf-8')

    path_maps = defaultdict(list)
    for row in rows:
        if row['suggested_action'] in ('COPY_TO_NEW','INDEX_ONLY','LEGACY_KEEP'):
            key = row['top_dir'].strip('/').replace('./','root') or 'root'
            path_maps[key].append({'old_path':row['current_path'],'suggested_action':row['suggested_action'],'suggested_target':row['suggested_target'],'asset_label':row['asset_label'],'asset_id':row['asset_id']})
    for key, items in path_maps.items():
        (LEGACY/f'path_maps/{key}_path_map_20260506.json').write_text(json.dumps({'generated_at':NOW,'items':items}, ensure_ascii=False, indent=2), encoding='utf-8')

    acceptance = {
        'generated_at': NOW,
        'validator_script': 'tools/validate_system_directory_governance.py',
        'acceptance_criteria': [
            'docs/system_directory_constitution.md exists',
            'docs/system_directory_routes.json exists and parses',
            'docs/new_task_write_routing_table.json exists and parses',
            'docs/forbidden_write_paths.json exists and parses',
            'legacy_compat/manifests/copy_only_migration_plan_20260506.json exists and parses',
            'legacy_compat/read_fallbacks/system_legacy_read_fallback_rules_20260506.md exists',
            'reports/review_ops_bot/audit/system_directory_governance_20260506/file_routing_matrix_20260506.csv exists',
            'No planned migration item has delete_old=True or move_old=True',
            'Required canonical directories exist',
            'No new runtime write route targets data/gmgn_candidates_live_run as primary path',
        ]
    }
    (OUT/'directory_validator_acceptance_standard_20260506.json').write_text(json.dumps(acceptance, ensure_ascii=False, indent=2), encoding='utf-8')

    summary = ['# SIKK-GMGN 文件级路由矩阵摘要 20260506','',f'- generated_at: {NOW}',f'- total_files_scanned: {len(rows)}',f'- matrix_csv: `{matrix_csv}`',f'- matrix_json: `{OUT/"file_routing_matrix_20260506.json"}`','', '## 按动作统计']
    for k,v in counts_action.most_common(): summary.append(f'- `{k}`: {v}')
    summary += ['', '## 按归属标签统计']
    for k,v in counts_label.most_common(): summary.append(f'- `{k}`: {v}')
    summary += ['', '## 按顶层目录统计']
    for k,v in counts_top.most_common(): summary.append(f'- `{k}`: {v}')
    summary += ['', '## 使用方式', '', '手机上不要打开 JSON 大文件，先看本摘要和正式裁决。需要查单文件时用 CSV grep/awk 或 Python 查询。']
    (OUT/'file_routing_matrix_summary_20260506.md').write_text('\n'.join(summary)+'\n', encoding='utf-8')

    print(json.dumps({'status':'generated','out_dir':str(OUT),'files_scanned':len(rows),'action_counts':dict(counts_action),'label_counts':dict(counts_label),'copy_only_planned':len(copy_plan)}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
