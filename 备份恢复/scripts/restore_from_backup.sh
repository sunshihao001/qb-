#!/usr/bin/env bash
set -u
REPO="https://github.com/sunshihao001/qb-.git"
BRANCH="backup/full-system-20260514-215254"
COMMIT="83edf22ff1e1c0c5769d8ff9c2e06a0d1ae6014c"
TARGET="/root/restore-test/sikk-gmgn-20260514"
while [ $# -gt 0 ]; do
  case "$1" in
    --repo) REPO="$2"; shift 2 ;;
    --branch) BRANCH="$2"; shift 2 ;;
    --commit) COMMIT="$2"; shift 2 ;;
    --target) TARGET="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 2 ;;
  esac
done
if [ "$TARGET" = "/root/sikk-gmgn" ]; then
  echo "BLOCKED: target must not be live root /root/sikk-gmgn"
  exit 3
fi
if [ -e "$TARGET" ]; then
  echo "BLOCKED: target already exists: $TARGET"
  echo "Use a fresh isolated directory."
  exit 4
fi
mkdir -p "$(dirname "$TARGET")"
echo "CLONE $REPO -> $TARGET"
git clone --branch "$BRANCH" "$REPO" "$TARGET" || exit 10
cd "$TARGET" || exit 11
git checkout "$COMMIT" || exit 12
ACTUAL="$(git rev-parse HEAD)"
if [ "$ACTUAL" != "$COMMIT" ]; then
  echo "BLOCKED: commit mismatch actual=$ACTUAL expected=$COMMIT"
  exit 13
fi
REPORT="$TARGET/RESTORE_ACCEPTANCE_REPORT.md"
{
  echo "# RESTORE_ACCEPTANCE_REPORT"
  echo
  echo "- restored_at: $(date -Is)"
  echo "- source_repo: $REPO"
  echo "- source_branch: $BRANCH"
  echo "- expected_commit: $COMMIT"
  echo "- actual_commit: $ACTUAL"
  echo "- target_path: $TARGET"
  echo "- restore_mode: isolated_directory_first"
  echo "- private_key_restored: false"
  echo "- real_trade_enabled: false"
  echo "- broadcast_enabled: false"
  echo
} > "$REPORT"
append_result() {
  local name="$1"; shift
  echo "## $name" >> "$REPORT"
  echo >> "$REPORT"
  echo '```text' >> "$REPORT"
  "$@" >> "$REPORT" 2>&1
  code=$?
  echo '```' >> "$REPORT"
  echo >> "$REPORT"
  echo "exit_code: $code" >> "$REPORT"
  echo >> "$REPORT"
  return $code
}
restore_status="RESTORE_READY_FOR_PAPER_DRY_RUN"
if [ -d "备份恢复" ]; then
  echo "restore_package: present" >> "$REPORT"
else
  echo "restore_package: missing" >> "$REPORT"
  restore_status="RESTORE_BLOCKED"
fi
if command -v python3 >/dev/null 2>&1; then
  append_result "restore_readiness_package_check" bash "备份恢复/scripts/check_restore_readiness.sh" || restore_status="RESTORE_BLOCKED"
  if [ -f tools/validate_directory_constitution.py ]; then
    append_result "directory_constitution" python3 tools/validate_directory_constitution.py || restore_status="RESTORE_READY_WITH_ENV_GAPS"
  fi
  if [ -f tools/validate_system_directory_governance.py ]; then
    append_result "system_directory_governance" python3 tools/validate_system_directory_governance.py || restore_status="RESTORE_READY_WITH_ENV_GAPS"
  fi
  if python3 -m pytest --version >/dev/null 2>&1; then
    append_result "safety_guard_tests" python3 -m pytest tests/test_wallet_data_guard.py tests/test_wallet_data_guard_legacy_quarantine.py tests/test_sikk_transaction_broadcast_guard.py || restore_status="RESTORE_BLOCKED"
  else
    echo "## safety_guard_tests" >> "$REPORT"
    echo "pytest missing; environment gap, install pytest/dependencies before paper-run." >> "$REPORT"
    restore_status="RESTORE_READY_WITH_ENV_GAPS"
  fi
else
  echo "python3 missing; environment gap" >> "$REPORT"
  restore_status="RESTORE_READY_WITH_ENV_GAPS"
fi
{
  echo
  echo "## Final Restore Status"
  echo
  echo "$restore_status"
} >> "$REPORT"
echo "RESTORE_REPORT=$REPORT"
echo "RESTORE_STATUS=$restore_status"
if [ "$restore_status" = "RESTORE_BLOCKED" ]; then exit 20; fi
exit 0
