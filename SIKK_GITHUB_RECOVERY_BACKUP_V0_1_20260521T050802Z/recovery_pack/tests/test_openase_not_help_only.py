import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')
def test_openase_not_help_only():
 o=json.load(open(ROOT/'data/openase_runs/gmgn_read_only_to_decision/latest/openase_artifact_manifest.json'))
 assert o['used_entrypoint']=='/usr/local/bin/openase'; assert o['not_help_only'] is True
 assert o['openase_execution_mode'] in ['REAL_CLI_TICKET_HARNESS_ONLY','REAL_CLI_WORKFLOW_RUN']
 assert o['commands']; assert all('--help' not in c['command'] for c in o['commands'])
