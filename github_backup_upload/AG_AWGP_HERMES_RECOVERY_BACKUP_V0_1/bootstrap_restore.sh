#!/usr/bin/env bash
set -euo pipefail
BACKUP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_ROOT="${1:-$(pwd)}"
PACK_DIR="$BACKUP_DIR/recovery_pack"
LATEST_JSON="$BACKUP_DIR/LATEST_SNAPSHOT.json"
echo "[bootstrap] backup_dir=$BACKUP_DIR"
echo "[bootstrap] target_root=$TARGET_ROOT"
SNAP_REL="$(python3 - <<PY
import json
print(json.load(open('$LATEST_JSON'))['latest_snapshot']['archive'])
PY
)"
SNAPSHOT="$BACKUP_DIR/$SNAP_REL"
[ -d "$PACK_DIR" ] || { echo "[bootstrap][FAIL] missing $PACK_DIR" >&2; exit 1; }
[ -f "$SNAPSHOT" ] || { echo "[bootstrap][FAIL] missing $SNAPSHOT" >&2; exit 1; }
echo "[bootstrap] Step 1/5 restore protocol files"
bash "$PACK_DIR/scripts/restore_snapshot.sh" "$PACK_DIR" "$TARGET_ROOT"
echo "[bootstrap] Step 2/5 verify protocol recovery"
bash "$PACK_DIR/scripts/verify_restore.sh" "$TARGET_ROOT" "$PACK_DIR"
echo "[bootstrap] Step 3/5 verify full snapshot checksum"
bash "$PACK_DIR/scripts/verify_full_snapshot.sh" "$SNAPSHOT"
echo "[bootstrap] Step 4/5 extract full non-secret snapshot"
if [[ "$SNAPSHOT" == *.tar.zst ]]; then tar --zstd -xf "$SNAPSHOT" -C "$TARGET_ROOT"; else tar -xzf "$SNAPSHOT" -C "$TARGET_ROOT"; fi
echo "[bootstrap] Step 5/5 post-extract verify"
EXTRACTED_PACK="$TARGET_ROOT/recovery/AG_AWGP_HERMES_PORTABLE_RECOVERY_PACK_V0_1"
if [ -d "$EXTRACTED_PACK" ]; then bash "$EXTRACTED_PACK/scripts/verify_restore.sh" "$TARGET_ROOT" "$EXTRACTED_PACK"; else bash "$PACK_DIR/scripts/verify_restore.sh" "$TARGET_ROOT" "$PACK_DIR"; fi
echo "[bootstrap] RESTORE COMPLETE"
echo "Next: cp configs/templates/env.example .env (manual secrets only). Load docs/protocols/ag_awgp/AG_AWGP_TRIGGER_PROMPT.md."
