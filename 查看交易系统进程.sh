#!/usr/bin/env bash
set -euo pipefail

pgrep -af 'python3 sikk_live_run.py|sikk_live_run.py' || true
