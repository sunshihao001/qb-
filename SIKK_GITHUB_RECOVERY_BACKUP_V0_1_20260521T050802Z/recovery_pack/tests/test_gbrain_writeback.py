import subprocess
import sys
from pathlib import Path


def test_gbrain_writeback_creates_card(tmp_path):
    script = Path("scripts/gbrain_writeback.py")
    assert script.exists(), "scripts/gbrain_writeback.py must exist"

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--card-type",
            "run",
            "--title",
            "test gbrain bridge",
            "--summary",
            "test summary",
            "--stage",
            "KNOWLEDGE_BRIDGE_PREP",
            "--brain-root",
            str(tmp_path / "brain" / "sikk-quant-runner"),
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    out_path = Path(result.stdout.strip())
    assert out_path.exists()
    content = out_path.read_text(encoding="utf-8")

    assert "card_type: run" in content
    assert "SIKK Quant Runner" in content
    assert "GBrain is the long-term knowledge workflow layer" in content
    assert "no decision_engine integration" in content
    assert "no PAPER_READY / BLOCKED decision" in content


def test_gbrain_writeback_rejects_invalid_card_type(tmp_path):
    script = Path("scripts/gbrain_writeback.py")
    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--card-type",
            "runtime_signal",
            "--title",
            "bad",
            "--summary",
            "bad",
            "--brain-root",
            str(tmp_path),
        ],
        text=True,
        capture_output=True,
    )

    assert result.returncode != 0
