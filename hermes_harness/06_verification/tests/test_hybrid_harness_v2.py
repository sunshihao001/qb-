import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read_jsonl(path: Path):
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return [json.loads(line) for line in lines]


def test_v2_core_directories_and_pre_audit_exist():
    expected_dirs = [
        "17_control_registry",
        "18_thread_rollout_state/threads",
        "18_thread_rollout_state/rollouts",
        "18_thread_rollout_state/state_snapshots",
        "19_exec_policy",
        "20_context_budget/compact_snapshots",
        "20_context_budget/post_compact_context",
        "20_context_budget/context_overflow_reports",
        "21_judgment_benchmark/benchmark_cases",
        "21_judgment_benchmark/expected_judgments",
        "21_judgment_benchmark/judgment_runs",
        "21_judgment_benchmark/judgment_error_logs",
        "21_judgment_benchmark/regression_reports",
        "22_anti_self_deception",
    ]
    for rel in expected_dirs:
        assert (ROOT / rel).is_dir(), rel
    assert (ROOT / "10_audit/task_audit_reports/HERMES_HARNESS_V2_PRE_AUDIT.md").is_file()


def test_control_registry_schema_and_12_invariants():
    entries = read_jsonl(ROOT / "17_control_registry/control_registry.jsonl")
    required = {"rule_id", "source", "type", "scope", "precedence", "content", "status", "superseded_by"}
    assert len(entries) >= 12
    for entry in entries:
        assert required.issubset(entry), entry
        assert entry["status"] in {"active", "expired", "superseded", "draft"}
    contents = "\n".join(e["content"] for e in entries)
    for phrase in [
        "每条规则必须有 source/type/scope/precedence",
        "每个任务必须有 thread_id",
        "每一轮动作必须写入 rollout event",
        "每个 tool_call 必须有 tool_result",
        "执行者不得验证自己",
        "验证报告本身必须接受 meta-verification",
        "任何记忆被引用前必须检查是否 stale / superseded",
    ]:
        assert phrase in contents


def test_exec_policy_checker_allow_ask_deny_and_json_output():
    script = ROOT / "09_scripts/hermes_exec_policy_check.py"
    assert script.is_file()
    safe = subprocess.run(
        [sys.executable, str(script), "--tool", "read_file", "--action", "read README", "--path", str(ROOT / "README.md"), "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    safe_payload = json.loads(safe.stdout)
    assert safe_payload["decision"] == "allow"
    assert safe_payload["risk_level"] in {"R0", "R1"}

    risky = subprocess.run(
        [sys.executable, str(script), "--tool", "terminal", "--action", "rm -rf /tmp/x", "--path", "/root/sikk-gmgn", "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    risky_payload = json.loads(risky.stdout)
    assert risky_payload["decision"] == "deny"
    assert risky_payload["risk_level"] == "R5"
    assert "rm -rf" in risky_payload["matched_policy"]


def test_thread_rollout_runner_creates_auditable_state():
    script = ROOT / "09_scripts/hermes_v2_thread_rollout_run.py"
    assert script.is_file()
    result = subprocess.run(
        [sys.executable, str(script), "--problem", "验证 V2.0 thread rollout state bridge", "--dry-run", "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    payload = json.loads(result.stdout)
    assert payload["status"] == "COMPLETED"
    assert payload["route"] == "hermes_hybrid_judgment_runtime_v2"
    assert payload["thread_id"].startswith("hermes.thread.")
    run_dir = Path(payload["run_dir"])
    assert (run_dir / "thread_state.json").is_file()
    assert (run_dir / "rollout_events.jsonl").is_file()
    assert (run_dir / "state_bridge.json").is_file()
    events = read_jsonl(run_dir / "rollout_events.jsonl")
    event_types = {e["event_type"] for e in events}
    assert {"thread_created", "tool_policy_check", "verification", "meta_verification", "anti_self_deception_audit"}.issubset(event_types)
    for event in events:
        assert "thread_id" in event
        assert "turn_id" in event
        assert "actor" in event
        assert "status" in event


def test_context_budget_benchmark_and_anti_self_deception_assets():
    state = json.loads((ROOT / "20_context_budget/context_budget_state.json").read_text(encoding="utf-8"))
    assert state["version"] == "v2.0"
    assert "control_plane" in state["priority_order"]
    assert "historical_noise" in state["drop_or_summarize"]

    cases = sorted((ROOT / "21_judgment_benchmark/benchmark_cases").glob("*.json"))
    assert len(cases) >= 8
    names = "\n".join(json.loads(p.read_text(encoding="utf-8"))["case_name"] for p in cases)
    assert "只生成文档但未接入流程" in names
    assert "计划被误认为执行" in names

    for rel in [
        "22_anti_self_deception/fake_completion_audit.md",
        "22_anti_self_deception/document_only_audit.md",
        "22_anti_self_deception/dry_run_vs_real_run_audit.md",
        "22_anti_self_deception/plan_vs_execution_audit.md",
        "22_anti_self_deception/self_scoring_audit.md",
    ]:
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert "不得" in text or "不能" in text


def test_v2_verification_and_final_report_exist_and_do_not_claim_real_improvement():
    verification = ROOT / "06_verification/verification_reports/HERMES_HARNESS_V2_VERIFICATION.md"
    report = ROOT / "08_reports/final_reports/HERMES_HARNESS_V2_REPORT.md"
    assert verification.is_file()
    assert report.is_file()
    text = report.read_text(encoding="utf-8")
    assert "混合式判断运行时系统" in text
    assert "不等于真实跨轮可靠性已经被证明" in text
    assert "Claude Code 式运行时纪律" in text
    assert "Codex 式显式控制面" in text
