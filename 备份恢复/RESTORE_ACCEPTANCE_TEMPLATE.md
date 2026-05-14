# RESTORE_ACCEPTANCE_REPORT

## 1. 恢复基本信息

- restore_id:
- restored_at:
- operator:
- source_repo:
- source_branch:
- source_commit:
- target_path:

## 2. 隔离检查

- target_is_not_live_root: true/false
- live_root_overwritten: true/false
- restore_mode: isolated_directory_first

## 3. Git 校验

- clone_success: true/false
- checkout_success: true/false
- actual_commit:
- expected_commit:
- commit_match: true/false

## 4. 恢复包完整性

- backup_restore_dir_exists: true/false
- manifest_exists: true/false
- runbook_exists: true/false
- restore_script_exists: true/false
- test_matrix_exists: true/false
- secrets_required_exists: true/false

## 5. 安全边界

- env_restored_from_backup: false
- private_key_restored: false
- mnemonic_restored: false
- real_trade_enabled: false
- broadcast_enabled: false
- paper_only: true

## 6. 验收命令结果

### directory_constitution

- command: `python3 tools/validate_directory_constitution.py`
- exit_code:
- result:

### system_directory_governance

- command: `python3 tools/validate_system_directory_governance.py`
- exit_code:
- result:

### safety_guard_tests

- command: `python3 -m pytest tests/test_wallet_data_guard.py tests/test_wallet_data_guard_legacy_quarantine.py tests/test_sikk_transaction_broadcast_guard.py`
- exit_code:
- result:

## 7. 已知 gap

- 

## 8. 恢复结论

选择一个：

- RESTORE_READY_FOR_PAPER_DRY_RUN
- RESTORE_READY_WITH_ENV_GAPS
- RESTORE_BLOCKED

## 9. 下一步

- 如果 READY：执行 sample-token dry-run / paper-run。
- 如果 WITH_ENV_GAPS：补依赖锁或人工注入必要 secret。
- 如果 BLOCKED：不要启动系统，先修复 blocker。
