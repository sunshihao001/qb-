#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-/root/sikk-quant-runner}"
OUT_DIR="${2:-$ROOT/recovery/snapshots}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
NAME="AG_AWGP_HERMES_FULL_NONSECRET_RECOVERY_SNAPSHOT_${STAMP}"
mkdir -p "$OUT_DIR"
cd "$ROOT"

EXCLUDES=(
  --exclude='.git'
  --exclude='.env'
  --exclude='.env.*'
  --exclude='*.key'
  --exclude='*.pem'
  --exclude='*.secret'
  --exclude='secrets'
  --exclude='private'
  --exclude='wallets'
  --exclude='cookies'
  --exclude='browser_sessions'
  --exclude='node_modules'
  --exclude='venv'
  --exclude='.venv'
  --exclude='__pycache__'
  --exclude='*.log'
  --exclude='tmp'
  --exclude='cache'
)

# Secret pre-scan: block known dangerous filenames before packaging.
if find .   -path './.git' -prune -o   \( -name '.env' -o -name '*.pem' -o -name '*.key' -o -name '*.secret' -o -name 'id_rsa*' \) -print | grep -q .; then
  echo "[BLOCKED] Secret-like files exist in project tree. Review exclusions before snapshot." >&2
  find . -path './.git' -prune -o \( -name '.env' -o -name '*.pem' -o -name '*.key' -o -name '*.secret' -o -name 'id_rsa*' \) -print >&2
  exit 2
fi

# Prefer zstd if available, fallback to gzip.
if command -v zstd >/dev/null 2>&1; then
  ARCHIVE="$OUT_DIR/${NAME}.tar.zst"
  tar "${EXCLUDES[@]}" -I 'zstd -19 -T0' -cf "$ARCHIVE" .
else
  ARCHIVE="$OUT_DIR/${NAME}.tar.gz"
  tar "${EXCLUDES[@]}" -czf "$ARCHIVE" .
fi

sha256sum "$ARCHIVE" > "$ARCHIVE.sha256"

MANIFEST="$OUT_DIR/${NAME}.manifest.json"
python3 - <<PY
import json, os, time
archive=os.environ.get('ARCHIVE', '$ARCHIVE')
manifest={
  'snapshot_name':'$NAME',
  'created_at':'$STAMP',
  'source_root':'$ROOT',
  'archive':archive,
  'checksum_file':archive+'.sha256',
  'secret_policy':'Excluded .env, keys, wallet/secret/signing/live credential material. Secrets must be restored externally.',
  'restore_hint':'Extract into clean project root, then run recovery/.../scripts/verify_restore.sh and checksum verification.',
  'excluded_patterns':['.git','.env','.env.*','*.key','*.pem','*.secret','secrets','private','wallets','cookies','browser_sessions','node_modules','venv','.venv','__pycache__','*.log','tmp','cache'],
  'archive_size_bytes':os.path.getsize(archive),
}
open('$MANIFEST','w').write(json.dumps(manifest, ensure_ascii=False, indent=2))
PY

echo "$ARCHIVE"
echo "$ARCHIVE.sha256"
echo "$MANIFEST"
