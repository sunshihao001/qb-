#!/usr/bin/env bash
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
fail=0
check_file() { if [ -f "$1" ]; then echo "PASS file $1"; else echo "FAIL missing file $1"; fail=1; fi; }
check_exec() { if [ -x "$1" ]; then echo "PASS executable $1"; else echo "FAIL not executable $1"; fail=1; fi; }
check_file "备份恢复/README.md"
check_file "备份恢复/BACKUP_RESTORE_MANIFEST.json"
check_file "备份恢复/RESTORE_RUNBOOK.md"
check_file "备份恢复/RECOVERY_TEST_MATRIX.md"
check_file "备份恢复/SECRETS_REQUIRED.md"
check_file "备份恢复/RESTORE_ACCEPTANCE_TEMPLATE.md"
check_exec "备份恢复/scripts/restore_from_backup.sh"
check_exec "备份恢复/scripts/create_backup_snapshot.sh"
python3 - <<'PY'
import json, pathlib, sys
p=pathlib.Path('备份恢复/BACKUP_RESTORE_MANIFEST.json')
try:
    data=json.loads(p.read_text())
except Exception as e:
    print('FAIL manifest_json', e)
    sys.exit(1)
required=['manifest_version','backup_id','source','restore_policy','restore_entrypoints','minimum_acceptance_commands']
missing=[k for k in required if k not in data]
if missing:
    print('FAIL manifest_missing', missing)
    sys.exit(1)
print('PASS manifest_json')
print('PASS source_branch', data['source'].get('branch'))
print('PASS source_commit', data['source'].get('base_commit'))
PY
if [ $? -ne 0 ]; then fail=1; fi
if [ -f requirements.txt ] || [ -f pyproject.toml ]; then
  echo "PASS dependency_lock_present"
else
  echo "WARN dependency_lock_missing: restore can clone/check, but environment install is best-effort"
fi
exit "$fail"
