import json
from pathlib import Path


SAMPLE_TEXT = """# Sample Document\n\n这是一个用于研究循环的示例文档。\n"""


def test_ingest_document_from_local_markdown_file_writes_raw_doc_and_metadata(tmp_path):
    from sikk_document_ingestor import ingest_document

    source = tmp_path / "input.md"
    source.write_text(SAMPLE_TEXT, encoding="utf-8")

    paths = ingest_document(output_root=tmp_path / "research_loop", source=source)

    raw_path = Path(paths["raw_doc_path"])
    metadata_path = Path(paths["metadata_path"])
    assert raw_path.exists()
    assert metadata_path.exists()
    assert raw_path.read_text(encoding="utf-8") == SAMPLE_TEXT

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    assert metadata["source_type"] == "local_path"
    assert metadata["source_path"] == str(source)
    assert metadata["source_url"] == ""
    assert metadata["title"] == "Sample Document"
    assert metadata["status"] == "captured"
    assert metadata["content_hash"]
    assert metadata["estimated_size"] == len(SAMPLE_TEXT.encode("utf-8"))
    assert metadata["doc_id"] in raw_path.name


def test_ingest_document_from_url_with_explicit_content_keeps_url_and_hash(tmp_path):
    from sikk_document_ingestor import ingest_document

    url = "https://example.com/research-note"
    paths = ingest_document(
        output_root=tmp_path / "research_loop",
        source=url,
        source_type="url",
        content=SAMPLE_TEXT,
        title="URL Sample",
    )

    metadata = json.loads(Path(paths["metadata_path"]).read_text(encoding="utf-8"))
    assert metadata["source_type"] == "url"
    assert metadata["source_url"] == url
    assert metadata["source_path"] == ""
    assert metadata["title"] == "URL Sample"
    assert metadata["status"] == "captured"
    assert metadata["doc_id"] == paths["doc_id"]
    assert Path(paths["raw_doc_path"]).read_text(encoding="utf-8") == SAMPLE_TEXT
