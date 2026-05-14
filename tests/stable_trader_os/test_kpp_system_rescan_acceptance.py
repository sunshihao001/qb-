from pathlib import Path
import json
import subprocess

ROOT = Path('/root/sikk-gmgn')
PHASE_DIRS = [
'p01_candidate_intake_controller','p02_source_data_fact_controller','p03_wallet_entity_controller','p04_chip_structure_controller','p05_evidence_controller','p06_scenario_recognition_controller','p07_strategy_gate_controller','p08_execution_risk_controller','p09_review_replay_controller','p10_self_upgrade_controller']
REQ = ['controller.yaml','context.md','input_contract.json','output_contract.json','task_tree.yaml','acceptance_gate.yaml','runner_binding.yaml','state_writeback_policy.yaml','handoff_packet.schema.json']
SLUGS = ['phase_01_candidate_intake','phase_02_source_data_fact','phase_03_wallet_entity','phase_04_chip_structure','phase_05_evidence','phase_06_scenario_recognition','phase_07_strategy_gate','phase_08_execution_risk','phase_09_review_replay','phase_10_self_upgrade']

def test_gap_registry_and_task_package_exist():
    assert (ROOT/'data/knowledge_processing_program/system_rescan/gaps/system_rescan_gap_registry.yaml').exists()
    assert (ROOT/'data/knowledge_processing_program/system_rescan/task_packages/her_kpp_system_rescan_autofix_task_package.yaml').exists()

def test_standard_phase_controller_assets_exist_and_json_valid():
    for d in PHASE_DIRS:
        base = ROOT/'system/phase_controllers'/d
        for f in REQ:
            p = base/f
            assert p.exists(), str(p)
            if f.endswith('.json'):
                json.loads(p.read_text())

def test_current_contract_schema_wrappers_exist():
    for slug in SLUGS:
        assert (ROOT/'contracts/stable_trader_os'/slug/'index.yaml').exists()
        assert (ROOT/'schemas/stable_trader_os'/slug/'index.yaml').exists()

def test_validator_passes_and_safety_boundary_kept():
    proc = subprocess.run(['python3','tools/stable_trader_os/validate_phase_controller_contracts.py','--phase','ALL'], cwd=ROOT, text=True, capture_output=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert 'real_trade_enabled: true' not in proc.stdout
