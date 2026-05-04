#!/usr/bin/env bash
set -euo pipefail
cd /root/sikk-gmgn
PYTHONPATH=/root/sikk-gmgn python3 sikk_her_task_router.py 'https://chatgpt.com/share/69f868b8-19c0-83ab-9c04-6339a93258bc' --root /root/sikk-gmgn --execute-absorption --workflow-package
