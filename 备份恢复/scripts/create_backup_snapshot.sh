#!/usr/bin/env bash
set -u
ROOT="${1:-/root/sikk-gmgn}"
cd "$ROOT" || exit 2
TS="$(date +%Y%m%d-%H%M%S)"
BRANCH="backup/full-system-$TS"
echo "Creating backup branch: $BRANCH"
if [ -n "$(git status --porcelain)" ]; then
  echo "WARN: working tree has changes; they will be included if already intended. Review before running in production."
fi
python3 - <<'PY'
import pathlib, re, sys
root=pathlib.Path('.')
patterns=[
    re.compile(r'-----BEGIN (RSA|OPENSSH|EC|DSA|PRIVATE) KEY-----'),
    re.compile(r'(?i)(GITHUB_TOKEN|OPENAI_API_KEY|ANTHROPIC_API_KEY|SOLANA_PRIVATE_KEY|WALLET_PRIVATE_KEY|PRIVATE_KEY|API_KEY|SECRET|PASSWORD)\s*[:=]\s*["']?([^"'\s,}]{12,})'),
    re.compile(r'(?i)(mnemonic|seed_phrase|seed phrase)\s*[:=]\s*["']?([a-z]+\s+[a-z]+\s+[a-z]+)'),
]
hits=[]
for p in root.rglob('*'):
    if '.git' in p.parts or not p.is_file() or p.stat().st_size>2_000_000:
        continue
    try: txt=p.read_text(errors='ignore')
    except Exception: continue
    for i,line in enumerate(txt.splitlines(),1):
        if any(pat.search(line) for pat in patterns):
            low=line.lower()
            if any(x in low for x in ['false','not_requested','not used','forbidden','no_private_key','no_secret','example','placeholder','redacted','dummy','required_manual_injection']):
                continue
            hits.append((str(p),i,line[:160])); break
if hits:
    print('BLOCKED secret-like hits:')
    for h in hits[:50]: print(h)
    sys.exit(1)
print('PASS narrow secret scan')
PY
if [ $? -ne 0 ]; then exit 3; fi
git checkout -b "$BRANCH" || exit 4
git add -A
git commit -m "backup: full system snapshot $TS" || exit 5
git push -u origin "$BRANCH" || exit 6
git ls-remote --heads origin "$BRANCH"
echo "Backup branch pushed: $BRANCH"
