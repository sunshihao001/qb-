import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_v21_real_task_benchmark_directories_and_fixture_cases_exist():
    expected_dirs = [
        "23_real_task_regression",
        "23_real_task_regression/task_fixtures",
        "23_real_task_regression/expected_outcomes",
        "23_real_task_regression/regression_runs",
        "23_real_task_regression/error_taxonomy",
        "23_real_task_regression/memory_lifecycle_reviews",
        "23_real_task_regression/meta_verification",
    ]
    for rel in expected_dirs:
        assert (ROOT / rel).is_dir(), rel

    fixtures = sorted((ROOT / "23_real_task_regression/task_fixtures").glob("*.json"))
    assert len(fixtures) >= 5
    names = "\n".join(read_json(p)["task_name"] for p in fixtures)
    for phrase in [
        "真实任务样本",
        "证据不足必须降级",
        "dry-run 不能宣称真实完成",
        "memory stale 必须复核",
        "危险执行必须 deny",
    ]:
        assert phrase in names


def test_v21_regression_runner_scores_fixture_cases_and_writes_audit_state():
    script = ROOT / "09_scripts/hermes_v21_real_task_regression_run.py"
    assert script.is_file()
    result = subprocess.run(
        [sys.executable, str(script), "--fixture-set", "core", "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    payload = json.loads(result.stdout)
    assert payload["status"] == "COMPLETED"
    assert payload["route"] == "hermes_real_task_regression_v2_1"
    assert payload["fixture_set"] == "core"
    assert payload["total_cases"] >= 5
    assert payload["passed_cases"] == payload["total_cases"]
    assert payload["failed_cases"] == 0
    assert payload["overall_passed"] is True
    assert payload["reliability_claim"] == "fixture_regression_passed_not_proven_in_live_tasks"

    run_dir = Path(payload["run_dir"])
    assert (run_dir / "regression_summary.json").is_file()
    assert (run_dir / "case_results.jsonl").is_file()
    assert (run_dir / "judgment_error_log.jsonl").is_file()
    assert (run_dir / "memory_lifecycle_review.json").is_file()
    assert (run_dir / "meta_verification_report.md").is_file()
    assert (run_dir / "anti_self_deception_audit.md").is_file()

    case_results = read_jsonl(run_dir / "case_results.jsonl")
    assert len(case_results) == payload["total_cases"]
    for case in case_results:
        assert case["passed"] is True
        assert case["expected_decision"] == case["actual_decision"]
        assert case["expected_action"] == case["actual_action"]
        assert case["evidence_checked"] is True
        assert case["policy_checked"] is True
        assert case["anti_self_deception_checked"] is True


def test_v21_runner_supports_single_case_replay_and_error_taxonomy():
    script = ROOT / "09_scripts/hermes_v21_real_task_regression_run.py"
    result = subprocess.run(
        [sys.executable, str(script), "--case-id", "rt_v21_003", "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    payload = json.loads(result.stdout)
    assert payload["status"] == "COMPLETED"
    assert payload["total_cases"] == 1
    assert payload["case_ids"] == ["rt_v21_003"]

    taxonomy = read_json(ROOT / "23_real_task_regression/error_taxonomy/judgment_error_taxonomy_v2_1.json")
    categories = {item["error_type"] for item in taxonomy["error_types"]}
    for expected in [
        "fake_completion",
        "evidence_insufficiency",
        "unsafe_execution",
        "stale_memory_contamination",
        "plan_execution_confusion",
    ]:
        assert expected in categories


def test_v21_reports_and_readme_boundary_do_not_overclaim_live_reliability():
    verification = ROOT / "06_verification/verification_reports/HERMES_HARNESS_V2_1_REAL_TASK_REGRESSION_VERIFICATION.md"
    report = ROOT / "08_reports/final_reports/HERMES_HARNESS_V2_1_REAL_TASK_REGRESSION_REPORT.md"
    readme = ROOT / "README.md"
    assert verification.is_file()
    assert report.is_file()
    text = report.read_text(encoding="utf-8")
    assert "V2.1 Real Task Regression Layer" in text
    assert "fixture regression passed" in text
    assert "不等于线上真实任务可靠性已经被长期证明" in text
    assert "live task" in text
    assert "V2.1 Real Task Regression Layer" in readme.read_text(encoding="utf-8")
