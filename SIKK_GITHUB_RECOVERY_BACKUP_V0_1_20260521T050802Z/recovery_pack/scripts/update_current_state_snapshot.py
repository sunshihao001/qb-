from pathlib import Path
import subprocess, sys
ROOT = Path(__file__).resolve().parents[3]
print('Create a new versioned pack instead of overwriting old directories:')
print('python scripts/create_sikk_portable_recovery_pack.py')
