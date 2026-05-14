import json
from pathlib import Path


def test_build_repomix_context_plan_writes_phase_specific_scripts(tmp_path):
    from sikk_repomix_context_planner import build_repomix_context_plan

    paths = build_repomix_context_plan(root=tmp_path, task_slug="share_repomix_deerflow")

    plan_json = Path(paths["plan_json"])
    plan_md = Path(paths["plan_md"])
    shell = Path(paths["shell_script"])

    assert plan_json.exists()
    assert plan_md.exists()
    assert shell.exists()
    payload = json.loads(plan_json.read_text(encoding="utf-8"))
    assert payload["安全边界"]["不读取私钥"] is True
    assert payload["安全边界"]["不广播"] is True
    phases = {item["phase"] for item in payload["contexts"]}
    assert {"full", "index", "wallet", "cluster", "case", "telegram", "web", "runtime", "audit"}.issubset(phases)
    assert "repomix" in shell.read_text(encoding="utf-8")
    assert "--compress" in shell.read_text(encoding="utf-8")
    assert "data/**" in shell.read_text(encoding="utf-8")


def test_build_repomix_context_plan_is_local_only_and_excludes_secrets(tmp_path):
    from sikk_repomix_context_planner import build_repomix_context_plan

    paths = build_repomix_context_plan(root=tmp_path, task_slug="safe")
    shell = Path(paths["shell_script"]).read_text(encoding="utf-8")
    assert ".env" in shell
    assert "*key*" in shell or "*secret*" in shell
    assert "gmgn_swap" not in shell
    assert "broadcast" not in shell.lower()
