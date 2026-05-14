#!/usr/bin/env python3
import json, sys, re

DENY = [r'rm\s+-rf', r'git\s+push', r'git\s+reset\s+--hard', r'git\s+clean\s+-fd', r'private[_-]?key', r'secret', r'broadcast', r'swap']
ASK = [r'git\s+commit', r'pip\s+install', r'npm\s+install', r'write config', r'config\.yaml', r'\.env', r'mv\s+', r'cp\s+.*\s+/']

def classify(command):
    c = command.lower()
    if any(re.search(p, c) for p in DENY):
        return {'risk_tier':'R5', 'permission':'DENY'}
    if any(re.search(p, c) for p in ASK):
        return {'risk_tier':'R3', 'permission':'ASK'}
    if any(x in c for x in ['python', 'pytest', 'mkdir', 'touch']):
        return {'risk_tier':'R1', 'permission':'ALLOW'}
    return {'risk_tier':'R0', 'permission':'ALLOW'}

if __name__ == '__main__':
    command = ' '.join(sys.argv[1:])
    print(json.dumps({'command': command, **classify(command)}, ensure_ascii=False, indent=2))
