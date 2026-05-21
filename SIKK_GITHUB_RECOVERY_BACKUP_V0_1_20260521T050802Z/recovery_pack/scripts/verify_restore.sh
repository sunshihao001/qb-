#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-.}"
PACK_DIR="${2:-$ROOT/recovery/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z}"
fail=0
check_file() { if [ ! -f "$1" ]; then echo "[FAIL] missing $1"; fail=1; else echo "[PASS] $1"; fi; }
check_dir() { if [ ! -d "$1" ]; then echo "[FAIL] missing $1"; fail=1; else echo "[PASS] $1"; fi; }
check_file "$PACK_DIR/BACKUP_MANIFEST.json"
check_file "$PACK_DIR/CHECKSUMS.sha256"
check_file "$PACK_DIR/scripts/restore_snapshot.sh"
check_file "$PACK_DIR/scripts/verify_restore.sh"
check_file "$PACK_DIR/scripts/scan_for_secrets.py"
check_file "$ROOT/data/operating_backbone/canonical/current/CURRENT_STATE_POINTER.json"
check_dir "$ROOT/docs/operating_backbone/clean_rehydration_v0_1"
check_dir "$ROOT/docs/operating_backbone/invocation_contracts_v0_1"
check_dir "$ROOT/docs/operating_backbone/storage_topology_v0_1"
python "$PACK_DIR/scripts/scan_for_secrets.py" "$PACK_DIR"
if command -v python >/dev/null 2>&1 && [ -f "$ROOT/tests/test_clean_rehydration_protocol.py" ]; then
  (cd "$ROOT" && PYTHONPATH="$ROOT" python -m pytest tests/test_clean_rehydration_protocol.py -q)
fi
if [ "$fail" -ne 0 ]; then echo "[verify] FAIL"; exit 1; fi
echo "[verify] PASS"
