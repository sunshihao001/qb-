#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-.}"
PACK_DIR="${2:-$ROOT/recovery/AG_AWGP_HERMES_PORTABLE_RECOVERY_PACK_V0_1}"
fail=0
check_file(){
  local p="$1"
  if [ -f "$p" ]; then echo "[PASS] $p"; else echo "[FAIL] missing $p"; fail=1; fi
}
check_absent_secret(){
  local pattern="$1"
  if find "$ROOT" -path '*/.git/*' -prune -o -name "$pattern" -print | grep -q .; then
    echo "[WARN] Found files matching $pattern. Ensure they are examples only or excluded.";
  else echo "[PASS] no $pattern files found"; fi
}
check_file "$PACK_DIR/doctrine/AG_AWGP_REHYDRATION_CAPSULE.md"
check_file "$PACK_DIR/doctrine/AG_AWGP_TRIGGER_PROMPT.md"
check_file "$PACK_DIR/agents/AG_AWGP_AGENT_BOUNDARY_MATRIX.yaml"
check_file "$PACK_DIR/templates/AG_AWGP_OPERATIONAL_BRIEF_TEMPLATE.yaml"
check_file "$PACK_DIR/tests/AG_AWGP_REGRESSION_TEST_CASES.yaml"
check_file "$PACK_DIR/RESTORE_RUNBOOK.md"
check_file "$PACK_DIR/RECOVERY_ACCEPTANCE_CHECKLIST.md"
check_file "$PACK_DIR/BACKUP_MANIFEST.json"
check_file "$PACK_DIR/CHECKSUMS.sha256"
check_file "$PACK_DIR/agents/HERMES_OPERATING_PROFILE.yaml"
check_file "$PACK_DIR/agents/GBRAIN_OPERATING_PROFILE.yaml"
check_file "$PACK_DIR/agents/OPENASE_OPERATING_PROFILE.yaml"
check_absent_secret ".env"
check_absent_secret "*.pem"
check_absent_secret "*.key"
if command -v sha256sum >/dev/null 2>&1 && [ -f "$PACK_DIR/CHECKSUMS.sha256" ]; then
  (cd "$PACK_DIR" && sha256sum -c CHECKSUMS.sha256 >/tmp/ag_awgp_verify_checksum.log 2>&1) || { echo "[FAIL] checksum verification failed"; cat /tmp/ag_awgp_verify_checksum.log; fail=1; }
  if [ "$fail" -eq 0 ]; then echo "[PASS] checksum verification"; fi
fi
if [ "$fail" -eq 0 ]; then echo "VERIFY_RESTORE: PASS"; else echo "VERIFY_RESTORE: FAIL"; fi
exit "$fail"
