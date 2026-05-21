from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
RUN_ID='bootstrap_directory_realign_v0_1'

def test_operating_directory_layout():
    for p in ['configs','docs','contracts','src','scripts','data','reports','tests','logs','tools','contracts/strategy_contracts','contracts/schemas','contracts/packets','contracts/acceptance','src/sikk_quant_runner/s01_data_source']:
        assert (ROOT/p).exists(), p
