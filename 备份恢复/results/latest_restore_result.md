# 最新恢复演练结果

- generated_at: 2026-05-14T22:50:57+00:00
- source_repo: https://github.com/sunshihao001/qb-.git
- source_branch: backup/full-system-20260514-215254
- source_commit: 57c9993a19815145ed6026816984594d6de3e804
- target_path: /tmp/sikk-gmgn-restore-smoke-20260514-225052
- restore_script_exit_code: 0
- acceptance_report: /tmp/sikk-gmgn-restore-smoke-20260514-225052/RESTORE_ACCEPTANCE_REPORT.md

## 恢复报告摘要

# RESTORE_ACCEPTANCE_REPORT

- restored_at: 2026-05-14T22:50:57+00:00
- source_repo: https://github.com/sunshihao001/qb-.git
- source_branch: backup/full-system-20260514-215254
- expected_commit: 57c9993a19815145ed6026816984594d6de3e804
- actual_commit: 57c9993a19815145ed6026816984594d6de3e804
- target_path: /tmp/sikk-gmgn-restore-smoke-20260514-225052
- restore_mode: isolated_directory_first
- private_key_restored: false
- real_trade_enabled: false
- broadcast_enabled: false

restore_package: present
## restore_readiness_package_check

```text
PASS file 备份恢复/README.md
PASS file 备份恢复/BACKUP_RESTORE_MANIFEST.json
PASS file 备份恢复/RESTORE_RUNBOOK.md
PASS file 备份恢复/RECOVERY_TEST_MATRIX.md
PASS file 备份恢复/SECRETS_REQUIRED.md
PASS file 备份恢复/RESTORE_ACCEPTANCE_TEMPLATE.md
PASS executable 备份恢复/scripts/restore_from_backup.sh
PASS executable 备份恢复/scripts/create_backup_snapshot.sh
PASS manifest_json
PASS source_branch backup/full-system-20260514-215254
PASS source_commit 83edf22ff1e1c0c5769d8ff9c2e06a0d1ae6014c
WARN dependency_lock_missing: restore can clone/check, but environment install is best-effort
```

exit_code: 0

## directory_constitution

```text
{
  "root": "/root/sikk-gmgn",
  "missing_dirs": [],
  "missing_files": [],
  "routes_json_ok": true,
  "routes_version": "1.1.0",
  "policy_ok": true,
  "agents_mentions_constitution": true,
  "ok": true
}
```

exit_code: 0

## system_directory_governance

```text
{
  "status": "PASS",
  "report": "/root/sikk-gmgn/reports/review_ops_bot/audit/system_directory_governance_20260506/directory_governance_validation_report_20260506.json",
  "total_checks": 42,
  "failed": []
}
```

exit_code: 0

## safety_guard_tests

```text
============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-9.0.3, pluggy-1.6.0
rootdir: /tmp/sikk-gmgn-restore-smoke-20260514-225052
configfile: pytest.ini
plugins: anyio-4.13.0, xdist-3.8.0, asyncio-1.3.0, typeguard-4.4.3
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 12 items

tests/test_wallet_data_guard.py ......                                   [ 50%]
tests/test_wallet_data_guard_legacy_quarantine.py ..                     [ 66%]
tests/test_sikk_transaction_broadcast_guard.py ....                      [100%]

============================== 12 passed in 0.08s ==============================
```

exit_code: 0


## Final Restore Status

RESTORE_READY_FOR_PAPER_DRY_RUN
