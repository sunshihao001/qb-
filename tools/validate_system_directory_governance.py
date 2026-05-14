#!/usr/bin/env python3
"""Validate SIKK-GMGN directory governance artifacts."""
import csv, json, os, sys
from pathlib import Path
ROOT=Path('/root/sikk-gmgn')
OUT=ROOT/'reports/review_ops_bot/audit/system_directory_governance_20260506'
checks=[]

def add(name, ok, detail=''):
    checks.append({'check':name,'ok':bool(ok),'detail':detail})

def json_ok(path):
    try:
        json.load(open(path,encoding='utf-8')); return True,''
    except Exception as e: return False,str(e)

required_files=[
 'docs/system_directory_constitution.md',
 'docs/system_directory_routes.json',
 'docs/new_task_write_routing_table.json',
 'docs/forbidden_write_paths.json',
 'legacy_compat/manifests/copy_only_migration_plan_20260506.json',
 'legacy_compat/read_fallbacks/system_legacy_read_fallback_rules_20260506.md',
 'reports/review_ops_bot/audit/system_directory_governance_20260506/file_routing_matrix_20260506.csv',
 'reports/review_ops_bot/audit/system_directory_governance_20260506/directory_official_decisions_20260506.md',
 'reports/review_ops_bot/audit/system_directory_governance_20260506/new_task_write_routing_table_20260506.json',
 'reports/review_ops_bot/audit/system_directory_governance_20260506/forbidden_write_paths_20260506.json',
 'reports/review_ops_bot/audit/system_directory_governance_20260506/legacy_read_fallback_rules_20260506.json',
 'reports/review_ops_bot/audit/system_directory_governance_20260506/copy_only_migration_plan_20260506.json',
 'reports/review_ops_bot/audit/system_directory_governance_20260506/directory_validator_acceptance_standard_20260506.json',
]
for rel in required_files:
    p=ROOT/rel; add(f'exists:{rel}', p.exists(), f'{p.stat().st_size} bytes' if p.exists() else 'missing')
for rel in [r for r in required_files if r.endswith('.json')]:
    ok,err=json_ok(ROOT/rel); add(f'json_parse:{rel}',ok,err)
# dirs
for d in ['docs','modules','tests','data','reports','research_loop','imports','schemas','contracts','tools','legacy_compat','legacy_compat/manifests','legacy_compat/path_maps','legacy_compat/read_fallbacks']:
    add(f'dir:{d}', (ROOT/d).is_dir())
# copy manifest no move/delete
p=ROOT/'legacy_compat/manifests/copy_only_migration_plan_20260506.json'
if p.exists():
    m=json.load(open(p,encoding='utf-8'))
    bad=[it for it in m.get('items',[]) if it.get('delete_old') or it.get('move_old')]
    add('copy_manifest_no_delete_no_move', not bad, f'bad={len(bad)} planned={m.get("planned_count")}')
# no new task route to gmgn_candidates_live_run primary
p=ROOT/'docs/new_task_write_routing_table.json'
if p.exists():
    r=json.load(open(p,encoding='utf-8'))
    bad=[]
    for k,v in r.get('new_task_write_routes',{}).items():
        if 'data/gmgn_candidates_live_run' in str(v): bad.append((k,v))
    add('new_routes_do_not_target_legacy_runtime', not bad, str(bad))
# matrix row count and headers
p=OUT/'file_routing_matrix_20260506.csv'
if p.exists():
    with open(p,encoding='utf-8') as f:
        reader=csv.DictReader(f); rows=list(reader)
    required_cols={'current_path','asset_label','suggested_action','suggested_target','owner_bot_or_domain','asset_id'}
    add('matrix_required_columns', required_cols.issubset(reader.fieldnames or []), str(reader.fieldnames))
    add('matrix_has_rows', len(rows)>0, f'rows={len(rows)}')
# forbidden path doc includes legacy dirs
p=ROOT/'docs/forbidden_write_paths.json'
if p.exists():
    fbd=json.load(open(p,encoding='utf-8'))
    pats='\n'.join(fbd.get('deny_write_patterns',[]))
    add('forbidden_includes_legacy_runtime', 'data/gmgn_candidates_live_run' in pats)
    add('forbidden_includes_old_cn_dirs', '结构分析' in pats and '钱包数据分析' in pats)
status='PASS' if all(c['ok'] for c in checks) else 'FAIL'
report={'status':status,'checked_at':__import__('datetime').datetime.now().isoformat(timespec='seconds'),'checks':checks}
out=OUT/'directory_governance_validation_report_20260506.json'
out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
md=['# 目录治理校验报告 20260506','',f'- status: `{status}`','']
for c in checks:
    md.append(f"- {'✅' if c['ok'] else '❌'} {c['check']}: {c.get('detail','')}")
(OUT/'directory_governance_validation_report_20260506.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
print(json.dumps({'status':status,'report':str(out),'total_checks':len(checks),'failed':[c for c in checks if not c['ok']]},ensure_ascii=False,indent=2))
sys.exit(0 if status=='PASS' else 1)
