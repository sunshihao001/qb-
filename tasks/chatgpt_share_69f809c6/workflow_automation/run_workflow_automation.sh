#!/usr/bin/env bash
set -euo pipefail
cd /root/sikk-gmgn
PYTHONPATH=/root/sikk-gmgn python3 sikk_her_task_router.py 'https://chatgpt.com/share/69f809c6-e7ac-83ab-823a-02d6cd8e5426' --root /root/sikk-gmgn --execute-absorption --workflow-package
