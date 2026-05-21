#!/usr/bin/env bash
set -euo pipefail
PACK_DIR="${1:-recovery/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z}"
TARGET_ROOT="${2:-.}"
mkdir -p "$TARGET_ROOT"
cd "$TARGET_ROOT"
mkdir -p recovery/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z
# Copy pack itself for future verification.
if [ "$(cd "$PACK_DIR" && pwd)" != "$(pwd)/recovery/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z" ]; then
  cp -a "$PACK_DIR"/. "recovery/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z/"
fi
cp -a "recovery/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z/docs" . 2>/dev/null || true
cp -a "recovery/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z/sikk_core" . 2>/dev/null || true
cp -a "recovery/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z/tests" . 2>/dev/null || true
mkdir -p data/operating_backbone/canonical/current data/operating_backbone/runs
cp -f "recovery/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z/current_state/CURRENT_STATE_POINTER.json" "data/operating_backbone/canonical/current/CURRENT_STATE_POINTER.json"
if [ -d "recovery/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z/run_evidence" ]; then
  cp -a "recovery/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z/run_evidence"/. "data/operating_backbone/runs/"
fi
echo "[restore] restored SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z into $TARGET_ROOT"
echo "[restore] next: bash recovery/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z/scripts/verify_restore.sh . recovery/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z"
