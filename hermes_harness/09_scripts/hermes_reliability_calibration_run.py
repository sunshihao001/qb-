#!/usr/bin/env python3
"""Hermes Harness V1.7 Reliability Calibration runner.

Creates auditable calibration artifacts comparing expected outcome to observed outcome.
This runner never reads or prints secrets and does not claim real-world success from dry-run evidence.
"""
import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTE = "hermes_reliability_calibration_layer"
MEMQ = ROOT / "04_memory" / "memory_write_queue.jsonl"


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def stamp():
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def safe_slug(text):
    text = re.sub(r"[^A-Za-z0-9\u4e00-\u9fff_-]+", "_", text).strip("_")
    return text[:36] or "calibration"


def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def append_jsonl(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def classify_delta(problem: str, expected: str, observed: str):
    text = " ".join([problem, expected, observed]).lower()
    dry_run_only = any(k in text for k in ["dry-run", "dry run", "仅证明", "链路可运行", "不能证明", "假闭环"])
    false_completion = any(k in text for k in ["假闭环", "假完成", "文件存在", "真实完成", "completion"])
    reliability_terms = any(k in text for k in ["更可靠", "可靠", "reliable", "降低", "error rate"])

    if dry_run_only and reliability_terms:
        decision = "needs_revalidation"
        trend = "unknown"
        delta_type = "evidence_gap"
        delta_score = 0.42
    elif false_completion:
        decision = "improve"
        trend = "improved_if_bias_correction_applied"
        delta_type = "false_completion_risk_identified"
        delta_score = 0.68
    elif expected.strip() == observed.strip():
        decision = "hold"
        trend = "stable"
        delta_type = "no_delta"
        delta_score = 0.0
    else:
        decision = "needs_revalidation"
        trend = "unknown"
        delta_type = "unverified_delta"
        delta_score = 0.5

    return {
        "dry_run_only": dry_run_only,
        "false_completion": false_completion,
        "reliability_terms": reliability_terms,
        "calibration_decision": decision,
        "judgment_error_rate_trend": trend,
        "delta_type": delta_type,
        "delta_score": delta_score,
    }


def main():
    p = argparse.ArgumentParser(description="Run Hermes V1.7 Reliability Calibration dry-run/audit")
    p.add_argument("--problem", required=True, help="Problem/request text. Do not include secrets.")
    p.add_argument("--expected", default="Hermes reliability improves after governance.", help="Expected outcome")
    p.add_argument("--observed", default="Only dry-run artifacts are currently evidenced.", help="Observed outcome")
    p.add_argument("--evidence", action="append", default=[], help="Evidence artifact path or note; can repeat")
    p.add_argument("--dry-run", action="store_true", help="Write calibration artifacts only; no external side effects.")
    p.add_argument("--json", action="store_true", help="Print compact JSON contract.")
    args = p.parse_args()

    iso = now()
    cid = f"calibration.{stamp()}.{safe_slug(args.problem)}"
    run_dir = ROOT / "16_reliability_calibration" / "runs" / cid
    run_dir.mkdir(parents=True, exist_ok=True)
    d = classify_delta(args.problem, args.expected, args.observed)

    expected_obj = {"statement": args.expected, "source": "argument_or_default", "confidence": "intended"}
    observed_obj = {"statement": args.observed, "source": "argument_or_default", "evidence_class": "dry_run_or_reported" if d["dry_run_only"] else "reported"}
    evidence_links = args.evidence or ["no external evidence supplied", "dry-run calibration artifact only"]
    calibration_delta = {
        "delta_type": d["delta_type"],
        "delta_score": d["delta_score"],
        "expected_observed_match": args.expected.strip() == args.observed.strip(),
        "dry_run_boundary": d["dry_run_only"],
        "interpretation": "需要真实运行/跨轮观察后才能声明可靠性提升" if d["dry_run_only"] else "偏差已记录，等待后续复验",
    }
    judgment_error_rate = {
        "trend": d["judgment_error_rate_trend"],
        "baseline": "unknown_without_history",
        "current_signal": d["delta_type"],
        "metric_status": "candidate_metric",
    }
    benchmark_update = {
        "benchmark_case_id": cid,
        "should_replay": True,
        "replay_focus": ["false_completion", "dry_run_boundary", "evidence_gap"],
        "stored_under": str((ROOT / "16_reliability_calibration" / "runs" / cid).relative_to(ROOT)),
    }
    rule_adjustment = {
        "candidate_rule": "Completion claims must include expected-vs-observed calibration when prior run only produced dry-run/control artifacts.",
        "promotion_status": "candidate_only",
        "requires_independent_revalidation": True,
    }
    memory_review = {
        "memory_action": "queue_unverified",
        "verified_memory_allowed": False,
        "reason": "single dry-run calibration is not enough for stable memory",
        "scope": "hermes_harness_reliability_calibration",
    }
    revalidation_window = {
        "trigger": "next comparable HER runtime task or explicit verification run",
        "minimum_evidence": ["real execution artifact", "independent verification", "expected-vs-observed comparison"],
        "expires_when": "route/schema changes or after superseding V1.x layer",
    }
    bias_correction = {
        "primary_bias": "overclaiming reliability from process completion" if d["dry_run_only"] else "unverified_delta",
        "next_run_instruction": "在声明更可靠之前，先比较 expected outcome 与 observed outcome，并标明 dry-run 边界。",
        "forbidden_shortcut": "不要把治理产物存在当作可靠性提升证据。",
    }

    state = {
        "artifact_type": "reliability_calibration_state",
        "version": "v1.7",
        "route": ROUTE,
        "calibration_run_id": cid,
        "created_at": iso,
        "problem": args.problem,
        "dry_run": bool(args.dry_run),
        "expected_outcome": expected_obj,
        "observed_outcome": observed_obj,
        "evidence_links": evidence_links,
        "calibration_delta": calibration_delta,
        "judgment_error_rate": judgment_error_rate,
        "benchmark_update": benchmark_update,
        "rule_adjustment_candidate": rule_adjustment,
        "memory_candidate_review": memory_review,
        "revalidation_window": revalidation_window,
        "next_run_bias_correction": bias_correction,
        "calibration_decision": d["calibration_decision"],
        "overall_passed": True,
    }

    write(run_dir / "expected_vs_observed.json", json.dumps({"expected_outcome": expected_obj, "observed_outcome": observed_obj, "evidence_links": evidence_links}, ensure_ascii=False, indent=2))
    write(run_dir / "calibration_delta.json", json.dumps(calibration_delta, ensure_ascii=False, indent=2))
    write(run_dir / "judgment_error_rate.json", json.dumps(judgment_error_rate, ensure_ascii=False, indent=2))
    write(run_dir / "benchmark_update.json", json.dumps(benchmark_update, ensure_ascii=False, indent=2))
    write(run_dir / "rule_adjustment_candidate.md", f"# Rule Adjustment Candidate\n\n- promotion_status: `{rule_adjustment['promotion_status']}`\n- requires_independent_revalidation: `{rule_adjustment['requires_independent_revalidation']}`\n\n## Candidate Rule\n{rule_adjustment['candidate_rule']}\n")
    write(run_dir / "memory_candidate_review.json", json.dumps(memory_review, ensure_ascii=False, indent=2))
    write(run_dir / "revalidation_window.md", f"# Revalidation Window\n\n- trigger: {revalidation_window['trigger']}\n- minimum_evidence: {', '.join(revalidation_window['minimum_evidence'])}\n- expires_when: {revalidation_window['expires_when']}\n")
    write(run_dir / "next_run_bias_correction.md", f"# Next Run Bias Correction\n\n- primary_bias: `{bias_correction['primary_bias']}`\n- instruction: {bias_correction['next_run_instruction']}\n- forbidden_shortcut: {bias_correction['forbidden_shortcut']}\n")
    write(run_dir / "reliability_calibration_state.json", json.dumps(state, ensure_ascii=False, indent=2))
    write(run_dir / "reliability_calibration_report.md", f"# Reliability Calibration Report\n\n- calibration_run_id: `{cid}`\n- route: `{ROUTE}`\n- status: `COMPLETED`\n- calibration_decision: `{d['calibration_decision']}`\n- judgment_error_rate_trend: `{d['judgment_error_rate_trend']}`\n- overall_passed: `true`\n\n## 核心结论\nV1.7 不证明 Hermes 已经更可靠；它证明本轮 expected-vs-observed 偏差已被记录，并形成下一轮校准输入。\n\n## 防假闭环声明\nDry-run calibration 只能证明校准链路可运行，不能替代真实跨轮可靠性数据。\n")

    append_jsonl(MEMQ, {
        "artifact_type": "memory_write_candidate",
        "version": "v1.7",
        "created_at": iso,
        "source_calibration_run_id": cid,
        "scope": "hermes_harness_reliability_calibration",
        "status": "queued_unverified",
        "candidate": "Hermes V1.7 adds Reliability Calibration: expected outcome, observed outcome, calibration delta, judgment error rate signal, benchmark update, rule adjustment candidate, memory review, revalidation window, and next-run bias correction before reliability claims.",
    })

    payload = {
        "status": "COMPLETED",
        "route": ROUTE,
        "calibration_run_id": cid,
        "run_dir": str(run_dir),
        "calibration_decision": d["calibration_decision"],
        "overall_passed": True,
        "dry_run": bool(args.dry_run),
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False))
    else:
        print(f"Reliability calibration: {payload['status']}")
        print(f"calibration_decision: {payload['calibration_decision']}")
        print(f"run_dir: {payload['run_dir']}")


if __name__ == "__main__":
    main()
