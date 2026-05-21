from __future__ import annotations
import re, sys
from pathlib import Path
root = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
name_re = re.compile(r'(^|/)(\.env(\..*)?|.*\.(pem|key|secret|p12|pfx)|id_rsa.*|cookies?|browser_sessions?|wallets?|private)(/|$)', re.I)
text_re = re.compile(r'(BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY|api[_-]?key\s*=\s*[^\s<>{}\[\]]{16,}|token\s*=\s*[^\s<>{}\[\]]{20,}|secret\s*=\s*[^\s<>{}\[\]]{16,})', re.I)
violations=[]
for p in root.rglob('*'):
    if not p.is_file():
        continue
    rel = str(p.relative_to(root)).replace('\\\\','/')
    if name_re.search(rel):
        violations.append(f'secret-like filename: {rel}')
        continue
    if p.stat().st_size <= 1024*1024 and p.suffix.lower() in {'.txt','.md','.json','.yaml','.yml','.py','.sh','.env','.example'}:
        try:
            text = p.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        filtered_lines = []
        for line in text.splitlines():
            low = line.lower()
            if 'example' in low or 'redacted' in low or '<' in line:
                continue
            # Allow explicit test placeholders and policy words that are not credentials.
            if 'test_token' in low or 'token_address' in low or 'private_key_required' in low:
                continue
            filtered_lines.append(line)
        filtered = '\n'.join(filtered_lines)
        if text_re.search(filtered):
            violations.append(f'secret-like content: {rel}')
if violations:
    print('[secret-scan] FAIL')
    for v in violations:
        print(v)
    sys.exit(1)
print('[secret-scan] PASS')
