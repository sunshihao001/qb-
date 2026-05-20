#!/usr/bin/env bash
set -euo pipefail
SNAPSHOT="${1:?snapshot archive path required}"
SHA="${SNAPSHOT}.sha256"
if [ ! -f "$SNAPSHOT" ]; then echo "[FAIL] snapshot missing: $SNAPSHOT"; exit 1; fi
if [ ! -f "$SHA" ]; then echo "[FAIL] checksum missing: $SHA"; exit 1; fi
sha256sum -c "$SHA"
echo "FULL_SNAPSHOT_CHECKSUM: PASS"
