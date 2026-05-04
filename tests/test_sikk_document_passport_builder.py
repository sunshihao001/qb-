import json
from pathlib import Path


def test_build_document_passport_outputs_json_and_md(tmp_path):
    from sikk_document_ingestor import ingest_document
    from sikk_document_passport_builder import build_document_passport

    root = tmp_path / "research_loop"
    source = tmp_path / "input.md"
    source.write_text("# Hermes and SIKK\n\npaper-only loop research.\n", encoding="utf-8")
    ingested = ingest_document(output_root=root, source=source)

    paths = build_document_passport(output_root=root, raw_doc_path=ingested["raw_doc_path"])
    passport_json = Path(paths["passport_json"])
    passport_md = Path(paths["passport_md"])
    assert passport_json.exists()
    assert passport_md.exists()

    payload = json.loads(passport_json.read_text(encoding="utf-8"))
    assert payload["doc_id"] == ingested["doc_id"]
    assert payload["title"] == "Hermes and SIKK"
    assert payload["source"]["source_type"] == "local_path"
    assert "paper-only" in payload["core_summary_zh"]
    assert payload["confidence"] >= 0.5
    assert isinstance(payload["usable_mechanisms"], list)

    md = passport_md.read_text(encoding="utf-8")
    assert "文档护照" in md
    assert "核心摘要" in md
    assert "可用机制" in md


def test_build_document_passport_handles_url_metadata(tmp_path):
    from sikk_document_passport_builder import build_document_passport

    root = tmp_path / "research_loop"
    raw_dir = root / "corpus" / "raw"
    raw_dir.mkdir(parents=True)
    raw_doc = raw_dir / "doc_001.md"
    raw_doc.write_text("# URL Sample\n\nA note.\n", encoding="utf-8")
    (raw_dir / "doc_001_metadata.json").write_text(json.dumps({
        "doc_id": "doc_001",
        "source_type": "url",
        "source_url": "https://example.com/doc",
        "source_path": "",
        "captured_at": "2026-05-04T00:00:00Z",
        "title": "URL Sample",
        "content_hash": "abc",
        "estimated_size": 20,
        "status": "captured",
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    paths = build_document_passport(output_root=root, raw_doc_path=raw_doc)
    payload = json.loads(Path(paths["passport_json"]).read_text(encoding="utf-8"))
    assert payload["source"]["source_type"] == "url"
    assert payload["source"]["source_url"] == "https://example.com/doc"
