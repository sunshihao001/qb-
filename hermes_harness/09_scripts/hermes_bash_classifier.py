#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path
BASE = Path(__file__).resolve().parents[1]

def classify(cmd):
    s=cmd.strip().lower()
    # B6 external/secrets first
    if re.search(r'\b(env|printenv)\b', s) or any(x in s for x in ['private', 'secret', 'token', '.env', 'id_rsa', 'curl http', 'curl https', 'wget http', 'broadcast', 'swap', 'trade', 'sign']):
        return 'B6','DENY','external_or_secret_risk'
    if re.search(r'\b(rm|git\s+reset|git\s+clean|docker\s+.*prune)\b', s):
        return 'B5','DENY','destructive_high_risk'
    if re.search(r'\b(mv|cp|sed\s+-i|systemctl|service\s+.*restart|docker\s+compose\s+down)\b', s):
        return 'B4','ASK','project_or_system_modification'
    if re.search(r'\b(python3?|bash|node|npm|pnpm|pytest|make)\b', s):
        return 'B3','ALLOW_WITH_STDOUT_STDERR_LOG','script_execution'
    if any(x in s for x in ['>', 'tee ', 'write_file']) or re.search(r'\bcat\s+>\b', s):
        return 'B2','ALLOW_IN_TASK_SCOPE','document_write_or_redirection'
    if re.search(r'\b(mkdir|touch)\b', s):
        return 'B1','ALLOW','low_risk_creation'
    if re.search(r'\b(pwd|ls|cat|grep|find|wc|sha256sum|head|tail|stat)\b', s):
        return 'B0','ALLOW','read_only_query'
    return 'B3','ALLOW_WITH_STDOUT_STDERR_LOG','unknown_command_treat_as_script_or_needs_log'

def main():
    p=argparse.ArgumentParser(description='Hermes bash risk classifier')
    p.add_argument('--dry-run', action='store_true', help='Do not write files')
    p.add_argument('--base', default=str(BASE), help='Hermes harness root; defaults to this hermes_harness')
    p.add_argument('command', nargs='*', help='Command to classify')
    a=p.parse_args()
    cmd=' '.join(a.command).strip()
    klass,perm,reason=classify(cmd)
    out={'command':cmd,'bash_risk_class':klass,'permission':perm,'reason':reason,'stdout_stderr_required':klass=='B3','dry_run':a.dry_run}
    print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__':
    main()
