#!/usr/bin/env bash
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$ROOT" || exit 2

TARGET="${1:-/tmp/sikk-gmgn-restore-smoke-$(date +%Y%m%d-%H%M%S)}"
REPO="$(git remote get-url origin 2>/dev/null || echo 'https://github.com/sunshihao001/qb-.git')"
BRANCH="$(git branch --show-current 2>/dev/null || echo 'backup/full-system-20260514-215254')"
COMMIT="$(git rev-parse HEAD)"

# Run an actual clone/checkout restore smoke test from the current backup branch.
bash "$SCRIPT_DIR/restore_from_backup.sh" \
  --repo "$REPO" \
  --branch "$BRANCH" \
  --commit "$COMMIT" \
  --target "$TARGET"
RC=$?

REPORT_DIR="$ROOT/备份恢复/results"
mkdir -p "$REPORT_DIR"
RESULT="$REPORT_DIR/latest_restore_result.md"
{
  echo "# 最新恢复演练结果"
  echo
  echo "- generated_at: $(date -Is)"
  echo "- source_repo: $REPO"
  echo "- source_branch: $BRANCH"
  echo "- source_commit: $COMMIT"
  echo "- target_path: $TARGET"
  echo "- restore_script_exit_code: $RC"
  if [ -f "$TARGET/RESTORE_ACCEPTANCE_REPORT.md" ]; then
    echo "- acceptance_report: $TARGET/RESTORE_ACCEPTANCE_REPORT.md"
    echo
    echo "## 恢复报告摘要"
    echo
    sed -n '1,220p' "$TARGET/RESTORE_ACCEPTANCE_REPORT.md"
  else
    echo "- acceptance_report: missing"
  fi
} > "$RESULT"

echo "RESULT_FILE=$RESULT"
exit "$RC"
