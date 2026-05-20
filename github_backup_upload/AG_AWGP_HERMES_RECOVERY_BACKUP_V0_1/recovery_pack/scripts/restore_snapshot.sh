#!/usr/bin/env bash
set -euo pipefail
PACK_DIR="${1:-recovery/AG_AWGP_HERMES_PORTABLE_RECOVERY_PACK_V0_1}"
TARGET_ROOT="${2:-.}"
echo "[restore] Using pack: $PACK_DIR"
echo "[restore] Target root: $TARGET_ROOT"
if [ ! -d "$PACK_DIR" ]; then
  echo "[restore][ERROR] Pack directory not found: $PACK_DIR" >&2
  exit 1
fi
mkdir -p "$TARGET_ROOT/docs/protocols/ag_awgp" "$TARGET_ROOT/docs/recovery" "$TARGET_ROOT/configs/templates" "$TARGET_ROOT/scripts/recovery"
cp -f "$PACK_DIR/doctrine/AG_AWGP_FULL_PROTOCOL.md" "$TARGET_ROOT/docs/protocols/ag_awgp/" || true
cp -f "$PACK_DIR/doctrine/AG_AWGP_REHYDRATION_CAPSULE.md" "$TARGET_ROOT/docs/protocols/ag_awgp/" || true
cp -f "$PACK_DIR/doctrine/AG_AWGP_TRIGGER_PROMPT.md" "$TARGET_ROOT/docs/protocols/ag_awgp/" || true
cp -f "$PACK_DIR/agents/AG_AWGP_AGENT_BOUNDARY_MATRIX.yaml" "$TARGET_ROOT/docs/protocols/ag_awgp/" || true
cp -f "$PACK_DIR/tests/AG_AWGP_REGRESSION_TEST_CASES.yaml" "$TARGET_ROOT/docs/protocols/ag_awgp/" || true
cp -f "$PACK_DIR/RESTORE_RUNBOOK.md" "$TARGET_ROOT/docs/recovery/" || true
cp -f "$PACK_DIR/RECOVERY_ACCEPTANCE_CHECKLIST.md" "$TARGET_ROOT/docs/recovery/" || true
cp -f "$PACK_DIR/templates/env.example" "$TARGET_ROOT/configs/templates/" || true
echo "[restore] Restore copy complete. Run scripts/recovery/verify_restore.sh or pack scripts/verify_restore.sh."
