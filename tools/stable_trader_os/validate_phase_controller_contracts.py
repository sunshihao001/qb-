#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
try:
    import yaml
except Exception:
    yaml = None
ROOT=Path('/root/sikk-gmgn')
PHASES={
'P01':'p01_candidate_intake_controller','P02':'p02_source_data_fact_controller','P03':'p03_wallet_entity_controller','P04':'p04_chip_structure_controller','P05':'p05_evidence_controller','P06':'p06_scenario_recognition_controller','P07':'p07_strategy_gate_controller','P08':'p08_execution_risk_controller','P09':'p09_review_replay_controller','P10':'p10_self_upgrade_controller'}
REQ=['controller.yaml','context.md','input_contract.json','output_contract.json','task_tree.yaml','acceptance_gate.yaml','runner_binding.yaml','state_writeback_policy.yaml','handoff_packet.schema.json']
FORBID=['real_trade_enabled: true','signing_enabled: true','broadcast_enabled: true','swap_enabled: true','live_execution_allowed: true','auto_order_allowed: true']
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--phase', default='ALL'); args=ap.parse_args()
    phases=PHASES if args.phase=='ALL' else {args.phase:PHASES[args.phase]}
    problems=[]
    for pid,dname in phases.items():
        d=ROOT/'system/phase_controllers'/dname
        for f in REQ:
            p=d/f
            if not p.exists(): problems.append(f'{pid}: missing {p}')
            elif f.endswith('.json'):
                try: json.loads(p.read_text())
                except Exception as e: problems.append(f'{pid}: invalid json {p}: {e}')
        rb=d/'runner_binding.yaml'
        txt=rb.read_text(errors='ignore') if rb.exists() else ''
        if 'READ_ONLY_VALIDATOR_ONLY' not in txt: problems.append(f'{pid}: runner binding is not validator-only')
        for bad in FORBID:
            if bad in txt: problems.append(f'{pid}: forbidden enabled term in runner binding: {bad}')
    result={'status':'PASS' if not problems else 'FAIL','problems':problems}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not problems else 1
if __name__=='__main__': sys.exit(main())
