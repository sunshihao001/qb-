import json
from pathlib import Path


def test_route_method_lens_writes_route_json_and_selects_supported_lenses(tmp_path):
    from sikk_method_lens_router import route_method_lens

    root = tmp_path / "research_loop"
    passport_json = root / "corpus" / "passports" / "doc_passport.json"
    passport_json.parent.mkdir(parents=True)
    passport_json.write_text(json.dumps({
        "doc_id": "doc_123",
        "title": "Audit and Timeline Notes",
        "core_summary_zh": "This document covers audit flow and timeline review.",
        "key_tags": ["audit", "timeline"],
        "usable_mechanisms": ["scan", "review"],
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    paths = route_method_lens(output_root=root, passport_json_path=passport_json)
    route_json = Path(paths["route_json"])
    assert route_json.exists()

    payload = json.loads(route_json.read_text(encoding="utf-8"))
    assert payload["doc_id"] == "doc_123"
    assert payload["primary_lens"] in {"TIMELINE", "SCAN", "OVERVIEW"}
    assert set(payload["selected_lenses"]).issubset({"SCAN", "DEEP", "ANGLE", "MIX", "HYP", "VOICES", "CHALLENGE", "TIMELINE", "STATUS", "OVERVIEW", "ARTEFACT"})
    assert "route.json" in payload["acceptance"]


def test_route_method_lens_defaults_to_overview_for_general_content(tmp_path):
    from sikk_method_lens_router import route_method_lens

    root = tmp_path / "research_loop"
    passport_json = root / "corpus" / "passports" / "doc_passport.json"
    passport_json.parent.mkdir(parents=True)
    passport_json.write_text(json.dumps({
        "doc_id": "doc_abc",
        "title": "General Notes",
        "core_summary_zh": "A neutral document.",
        "key_tags": ["loop"],
        "usable_mechanisms": ["paper-only"],
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    payload = json.loads(Path(route_method_lens(output_root=root, passport_json_path=passport_json)["route_json"]).read_text(encoding="utf-8"))
    assert payload["primary_lens"] == "OVERVIEW"
    assert payload["selected_lenses"][0] == "OVERVIEW"
