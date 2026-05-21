from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
RUN_ID='bootstrap_directory_realign_v0_1'

def test_run_artifact_layout():
    run=ROOT/'data/runs'/RUN_ID
    assert (run/'run_manifest.json').exists()
    for p in ['s01_data_source_r02_r03','s02_feature_engineering_r04','s03_strategy_contract_r06','s04_structure_engine_r05','s05_decision_ticket_r07','s06_replay_backtest_r08_r09','s07_paper_only_r10','s08_attribution_r11','s09_upgrade_candidate_r12','s10_revalidation_release_r13']:
        assert (run/p).exists(), p
