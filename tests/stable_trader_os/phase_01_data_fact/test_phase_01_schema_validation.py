from pathlib import Path
import json, csv, re
ROOT = Path(__file__).resolve().parents[3]
PHASE = ROOT / "schemas/stable_trader_os/phase_01_data_fact"
CONFIG = ROOT / "configs/stable_trader_os/phase_01_data_fact"
CONTRACT = ROOT / "contracts/stable_trader_os/phase_01_data_fact"
EXAMPLES = ROOT / "examples/stable_trader_os/phase_01_data_fact"

def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

def test_all_schema_files_exist_and_have_chinese_descriptions():
    files = ["phase_01_field_schema.json","token_fact_schema.json","wallet_fact_table_schema.json","trade_fact_table_schema.json","holder_fact_table_schema.json","transfer_fact_table_schema.json","kline_fact_table_schema.json","quote_fact_schema.json","security_fact_schema.json","phase_01_quality_gate_schema.json"]
    for name in files:
        path = PHASE / name
        assert path.exists(), name
        data = load(path)
        assert data.get("phase_id") == "phase_01_data_fact_controller"
        assert data.get("fields"), name
        for field in data["fields"]:
            for key in ["field_name","field_chinese_name","data_type","required_level","unit","timezone","missing_value","source_candidates","preferred_source","downstream_used_by","description"]:
                assert key in field, f"{name}:{key}"
            assert re.search(r"[一-鿿]", field["field_chinese_name"])
            assert re.search(r"[一-鿿]", field["description"])
