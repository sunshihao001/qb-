#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${SIKK_RESTORE_REPO_URL:-https://github.com/sunshihao001/qb-.git}"
BRANCH="${SIKK_RESTORE_BRANCH:-main}"
TARGET_DIR="${SIKK_RESTORE_TARGET_DIR:-${1:-$PWD/sikk-quant-runner-restored}}"
WORK_DIR="${SIKK_RESTORE_WORK_DIR:-}"
KEEP_WORK_DIR="${SIKK_RESTORE_KEEP_WORK_DIR:-0}"
RUN_VERIFY="${SIKK_RESTORE_RUN_VERIFY:-1}"

if ! command -v git >/dev/null 2>&1; then
  echo "[sikk-restore] ERROR: git is required" >&2
  exit 1
fi
if ! command -v python >/dev/null 2>&1 && ! command -v python3 >/dev/null 2>&1; then
  echo "[sikk-restore] ERROR: python or python3 is required" >&2
  exit 1
fi
PYTHON_BIN="$(command -v python || command -v python3)"

if [ -z "$WORK_DIR" ]; then
  WORK_DIR="$(mktemp -d /tmp/sikk-github-restore.XXXXXX)"
else
  mkdir -p "$WORK_DIR"
fi
cleanup() {
  if [ "$KEEP_WORK_DIR" != "1" ]; then
    rm -rf "$WORK_DIR"
  else
    echo "[sikk-restore] kept work dir: $WORK_DIR"
  fi
}
trap cleanup EXIT

REPO_DIR="$WORK_DIR/repo"
echo "[sikk-restore] cloning $REPO_URL#$BRANCH"
git clone --depth 1 --branch "$BRANCH" "$REPO_URL" "$REPO_DIR" >/dev/null

LATEST_POINTER="$REPO_DIR/LATEST_SIKK_BACKUP.txt"
if [ -f "$LATEST_POINTER" ]; then
  BACKUP_DIR_NAME="$(tr -d '[:space:]' < "$LATEST_POINTER")"
else
  BACKUP_DIR_NAME="$(cd "$REPO_DIR" && find . -maxdepth 1 -type d -name 'SIKK_GITHUB_RECOVERY_BACKUP_V0_1_*' -printf '%f\n' | sort | tail -n 1)"
fi

if [ -z "${BACKUP_DIR_NAME:-}" ] || [ ! -d "$REPO_DIR/$BACKUP_DIR_NAME/recovery_pack" ]; then
  echo "[sikk-restore] ERROR: no valid SIKK_GITHUB_RECOVERY_BACKUP_V0_1_* recovery_pack found" >&2
  exit 1
fi

PACK_DIR="$REPO_DIR/$BACKUP_DIR_NAME/recovery_pack"
echo "[sikk-restore] selected backup: $BACKUP_DIR_NAME"
echo "[sikk-restore] target: $TARGET_DIR"
mkdir -p "$TARGET_DIR"

if [ -f "$PACK_DIR/scripts/scan_for_secrets.py" ]; then
  "$PYTHON_BIN" "$PACK_DIR/scripts/scan_for_secrets.py" "$REPO_DIR/$BACKUP_DIR_NAME"
fi

bash "$PACK_DIR/scripts/restore_snapshot.sh" "$PACK_DIR" "$TARGET_DIR"

if [ "$RUN_VERIFY" = "1" ]; then
  bash "$TARGET_DIR/recovery/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z/scripts/verify_restore.sh" "$TARGET_DIR" "$TARGET_DIR/recovery/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z"
fi

cat > "$TARGET_DIR/SIKK_RESTORE_SOURCE.json" <<EOF
{
  "repo_url": "$REPO_URL",
  "branch": "$BRANCH",
  "backup_dir": "$BACKUP_DIR_NAME",
  "restored_at_utc": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "verify_ran": "$RUN_VERIFY"
}
EOF

echo "[sikk-restore] PASS"
echo "[sikk-restore] restored target: $TARGET_DIR"
echo "[sikk-restore] source record: $TARGET_DIR/SIKK_RESTORE_SOURCE.json"
