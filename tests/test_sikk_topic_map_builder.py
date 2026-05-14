import json
from pathlib import Path


def test_build_topic_map_creates_outline_and_topic_map(tmp_path):
    from sikk_document_ingestor import ingest_document
    from sikk_document_passport_builder import build_document_passport
    from sikk_topic_map_builder import build_topic_map

    root = tmp_path / "research_loop"
    source = tmp_path / "input.md"
    source.write_text("# Topic Map Sample\n\nInput → Passport → Outline → Topic Map.\n", encoding="utf-8")
    ingested = ingest_document(output_root=root, source=source)
    passport = build_document_passport(output_root=root, raw_doc_path=ingested["raw_doc_path"])

    paths = build_topic_map(output_root=root, passport_json_path=passport["passport_json"])
    outline_json = Path(paths["outline_json"])
    topic_map_md = Path(paths["topic_map_md"])
    assert outline_json.exists()
    assert topic_map_md.exists()

    payload = json.loads(outline_json.read_text(encoding="utf-8"))
    assert payload["doc_id"] == ingested["doc_id"]
    assert payload["title"] == "Topic Map Sample"
    assert payload["topic_count"] >= 3
    assert "信息热点" in payload

    md = topic_map_md.read_text(encoding="utf-8")
    assert "主题地图" in md
    assert "热点" in md
    assert "潜在路径" in md


def test_build_topic_map_derives_hotspots_and_paths(tmp_path):
    from sikk_topic_map_builder import build_topic_map

    passport_json = tmp_path / "research_loop" / "corpus" / "passports" / "doc_passport.json"
    passport_json.parent.mkdir(parents=True)
    passport_json.write_text(json.dumps({
        "doc_id": "doc_x",
        "title": "Map Me",
        "core_summary_zh": "This is about paper-only loop, audit, task packages, and review.",
        "usable_mechanisms": ["paper-only", "audit", "review"],
        "key_tags": ["paper-only", "loop"],
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    paths = build_topic_map(output_root=tmp_path / "research_loop", passport_json_path=passport_json)
    payload = json.loads(Path(paths["outline_json"]).read_text(encoding="utf-8"))
    assert payload["topic_count"] >= 3
    assert any("audit" in item.lower() for item in payload["hotspots"])
