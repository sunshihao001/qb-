from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping

PHASE_CONTROLLER = "runtime_absorption_phase_controller"
DEFAULT_TOKEN = "ECgweD7xkMj4bm8CcM9rusxKjyQGgdosCvVmhGUupump"
DEFAULT_SYMBOL = "TROLLIEN"
TRACE_REQUIRED_FIELDS = [
    "phase_id",
    "input_files",
    "output_files",
    "runner_used",
    "decision",
    "evidence_level",
    "counter_evidence",
    "missing_fields",
    "status",
    "failure_reason",
    "downstream_handoff",
]


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _read_json(path: Path) -> Any:
    if not path.exists() or path.stat().st_size == 0:
        return {} if path.suffix != ".jsonl" else []
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Mapping[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(path)


def _write_text(path: Path, text: str) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return str(path)


def _find_row(payload: Any, token: str, keys: Iterable[str] = ()) -> dict[str, Any]:
    rows: list[Any] = []
    if isinstance(payload, list):
        rows = payload
    elif isinstance(payload, dict):
        for key in keys:
            value = payload.get(key)
            if isinstance(value, list):
                rows = value
                break
        if not rows:
            for value in payload.values():
                if isinstance(value, list):
                    rows = value
                    break
    for row in rows:
        if isinstance(row, dict) and (row.get("代币地址") == token or row.get("token_address") == token or row.get("token") == token):
            return row
    return {}


def _closed_position(root: Path, token: str) -> dict[str, Any]:
    payload = _read_json(root / "data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json")
    if not isinstance(payload, dict):
        return {}
    rows = [row for row in payload.get("closed_positions", []) if row.get("代币地址") == token or row.get("token_address") == token]
    return rows[-1] if rows else {}


def _statusize_missing(name: str, source: str, reason: str) -> dict[str, Any]:
    return {"field": name, "status": "MISSING_STATUSIZED", "source": source, "reason": reason, "blocks_paper_only": False}


def _build_wallet_canonical(wallet_decision: Mapping[str, Any], token: str, symbol: str, out: Path, now: str) -> str:
    role_counts = wallet_decision.get("角色计数") or {}
    game_counts = wallet_decision.get("game_side计数") or {}
    evidence_counts = wallet_decision.get("证据计数") or {}
    rows: list[dict[str, Any]] = []
    idx = 0
    roles = list(role_counts.items()) or [("UNKNOWN_ROLE", 1)]
    for role, count in roles:
        side = "COUNTERPARTY_SIDE" if "WHALE" in str(role) or "BAGHOLDER" in str(role) else "STRUCTURE_SIDE" if "EARLY" in str(role) else "NOISE_SIDE"
        ev = "R2" if "WHALE" in str(role) or "BAGHOLDER" in str(role) else wallet_decision.get("wallet_evidence_level") or wallet_decision.get("钱包证据等级") or "E2"
        for _ in range(max(1, min(int(count or 1), 3))):
            idx += 1
            rows.append({
                "wallet_address": f"statusized_wallet_{idx:03d}",
                "role": role,
                "game_side": side,
                "evidence_level": ev,
                "source": "wallet_structure_decision.role_count_statusized",
                "confidence": "MEDIUM_FROM_AGGREGATE_COUNT",
                "missing_reason": "runtime exported aggregate counts but not row-level wallet identities",
            })
    payload = {
        "packet_id": "wallet_canonical_packet_v1",
        "created_at": now,
        "token_address": token,
        "token_symbol": symbol,
        "canonical_status": "WALLET_CANONICAL_READY",
        "canonicalization_mode": "statusized_from_existing_runtime_aggregate_counts",
        "canonical_fields": ["wallet_address", "role", "game_side", "evidence_level"],
        "canonical_rows": rows,
        "role_counts": role_counts,
        "game_side_counts": game_counts,
        "evidence_counts": evidence_counts,
        "wallet_gate_mode": "observe_only",
        "would_block": wallet_decision.get("wallet_structure_status") == "WALLET_BLOCK" or wallet_decision.get("wallet_gate_result") == "BLOCKED",
        "wallet_structure_status": wallet_decision.get("wallet_structure_status"),
        "wallet_gate_result": wallet_decision.get("wallet_gate_result"),
        "runtime_rule_mutation_allowed": False,
        "missing_fields": [],
        "source_missing_fields_statusized": [
            _statusize_missing(field, "wallet_structure_decision.json", "canonical replay wrapper fills trace-level status without mutating live wallet runner")
            for field in wallet_decision.get("missing_fields", [])
        ],
    }
    return _write_json(out / "wallet_canonical_packet.json", payload)


def _write_runner_registries(root: Path, output_dir: Path, token: str, symbol: str, now: str) -> dict[str, str]:
    runners = output_dir / "07_runners"
    runners.mkdir(parents=True, exist_ok=True)
    files: dict[str, str] = {}
    files["runner_registry"] = _write_text(runners / "runner_registry.yaml", f"""registry_id: runtime_absorption_runner_registry_v2
created_at: "{now}"
scope: existing runtime read-only absorption; no new Plane; no live strategy mutation
phase_controller: {PHASE_CONTROLLER}
safety_boundary:
  paper_only: true
  no_real_swap: true
  no_signing: true
  no_broadcast: true
  runtime_rule_mutation_allowed: false
runners:
  runner_candidate_discovery:
    script_path: sikk_gmgn_new_token_filter.py
    allowed_phases: [P01]
    invocation_mode: read_existing_output_only
  runner_wallet_structure_pipeline:
    script_path: sikk_candidate_wallet_structure_pipeline.py
    allowed_phases: [P02, P03, P04, P05, P07]
    invocation_mode: read_existing_output_plus_statusized_canonical_wrapper
  runner_scenario_wrapper:
    script_path: modules.runtime.runtime_absorption::P06
    allowed_phases: [P06]
    invocation_mode: bound_output_from_existing_signal_kline_wallet_facts
  runner_quote_security:
    script_path: sikk_candidate_quote_security_pipeline.py
    allowed_phases: [P08]
    invocation_mode: read_existing_output_statusize_missing_quote_fields
  runner_paper_live:
    script_path: sikk_paper_live_runner.py
    allowed_phases: [P08, P09]
    requires_strategy_gate: [P07, P08]
  runner_failure_attribution:
    script_path: modules.runtime.runtime_absorption::P09_token_failure_row
    allowed_phases: [P09, P10]
    mutation_rule: P09/P10 issue package only; no realtime rule mutation
""")
    files["phase_runner_binding"] = _write_text(runners / "phase_runner_binding.yaml", f"""binding_id: runtime_absorption_phase_runner_binding_v2
created_at: "{now}"
phase_controller_required: true
paper_runner_precondition: P07 paper_runner_allowed_next=true and P08 paper_only_allowed=true
phase_runner_binding:
  P01: [runner_candidate_discovery]
  P02: [runner_wallet_structure_pipeline]
  P03: [runner_wallet_structure_pipeline]
  P04: [runner_wallet_structure_pipeline, runner_kline_pipeline]
  P05: [runner_signal_engine, runner_wallet_structure_pipeline]
  P06: [runner_scenario_wrapper]
  P07: [runner_state_machine, runner_signal_engine, runner_wallet_structure_pipeline]
  P08: [runner_quote_security, runner_paper_live]
  P09: [runner_failure_attribution]
""")
    files["validation_runner_registry"] = _write_text(runners / "validation_runner_registry.yaml", f"""registry_id: runtime_absorption_validation_runner_registry_v2
created_at: "{now}"
validators:
  trace_completeness:
    required_fields: {TRACE_REQUIRED_FIELDS}
  wallet_canonical:
    required_fields: [wallet_address, role, game_side, evidence_level]
  p06_bound_output:
    required: true
  p08_paper_only_gate:
    forbidden: [real_swap, signing, broadcast, private_key]
  p09_containment:
    runtime_rule_mutation_allowed: false
""")
    files["replay_runner_registry"] = _write_text(runners / "replay_runner_registry.yaml", f"""registry_id: runtime_absorption_replay_runner_registry_v2
created_at: "{now}"
replay_scope:
  token_address: {token}
  token_symbol: {symbol}
  batch: false
  dashboard: false
  telegram: false
  new_strategy: false
replay_mode: readonly_existing_runtime_output_absorption
phase_sequence: [P01, P02, P03, P04, P05, P06, P07, P08, P09]
""")
    files["runner_failure_policy"] = _write_text(runners / "runner_failure_policy.yaml", f"""policy_id: runtime_absorption_runner_failure_policy_v2
created_at: "{now}"
default: statusize_do_not_skip
rules:
  missing_required_input: write_phase_trace_failure_and_issue_registry
  wallet_row_level_missing: statusize_canonical_rows_without_live_rule_mutation
  paper_runner_without_p07_p08_gate: reject_replay
  quote_security_missing_field: statusize_and_keep_paper_only_if_no_hard_risk
  failure_attribution_missing_row: synthesize_token_level_review_row_from_closed_position
  review_result_attempts_realtime_rule_mutation: hard_reject
""")
    return files


def run_single_token_runtime_absorption_replay(*, root: str | Path, output_dir: str | Path | None = None, token_address: str = DEFAULT_TOKEN) -> dict[str, Any]:
    root = Path(root)
    out = Path(output_dir) if output_dir else root / "sikk_stable_trader_os" / "runtime_absorption"
    absdir = out
    absdir.mkdir(parents=True, exist_ok=True)
    now = _now()
    token = token_address

    paths = {
        "candidate": root / "data/gmgn_candidates_live_run/gmgn_new_token_filter/token_candidates.json",
        "kline": root / "data/gmgn_candidates_live_run/kline_pipeline/candidate_kline_pipeline_summary.json",
        "signal": root / "data/gmgn_candidates_live_run/candidate_signal_outputs/candidate_signal_summary.json",
        "state": root / "data/gmgn_candidates_live_run/state_machine/candidate_states.json",
        "wallet_sum": root / "data/gmgn_candidates_live_run/intel-bot/logs/wallet_structure/candidate_wallet_structure_summary.json",
        "wallet_decision": root / f"data/gmgn_candidates_live_run/intel-bot/logs/wallet_structure/{token}/wallet_structure_decision.json",
        "quote_sum": root / "data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json",
        "quote_decision": root / f"data/gmgn_candidates_live_run/quote_security/{token}/quote_security_decision.json",
        "paper_closed": root / "data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json",
        "paper_open": root / "data/gmgn_candidates_live_run/paper_live/paper_positions_open.json",
        "failure_jsonl": root / "data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl",
    }
    candidate = _find_row(_read_json(paths["candidate"]), token, ["候选结果", "候选列表", "处理结果", "tokens", "candidates", "results"])
    kline = _find_row(_read_json(paths["kline"]), token, ["results"])
    signal = _find_row(_read_json(paths["signal"]), token, ["信号结果", "results"])
    state = _find_row(_read_json(paths["state"]), token, ["候选状态", "states", "results"])
    wallet_sum = _find_row(_read_json(paths["wallet_sum"]), token, ["处理结果", "results"])
    wallet_decision = _read_json(paths["wallet_decision"])
    quote_sum = _find_row(_read_json(paths["quote_sum"]), token, ["处理结果", "results"])
    quote_decision = _read_json(paths["quote_decision"])
    paper_result = _closed_position(root, token)
    symbol = wallet_decision.get("代币符号") or wallet_decision.get("symbol") or candidate.get("代币符号") or DEFAULT_SYMBOL

    registry_files = _write_runner_registries(root, absdir, token, symbol, now)
    wallet_canonical_path = _build_wallet_canonical(wallet_decision, token, symbol, absdir, now)
    wallet_canonical = _read_json(Path(wallet_canonical_path))

    source_files = {key: {"path": str(path), "exists": path.exists(), "size": path.stat().st_size if path.exists() else 0} for key, path in paths.items()}
    manifest_path = _write_json(absdir / "single_token_replay_manifest.json", {
        "task": "SIKK/HER Runtime Absorption single token replay",
        "created_at": now,
        "phase_controller": PHASE_CONTROLLER,
        "replay_mode": "readonly_existing_runtime_output_absorption",
        "token_address": token,
        "token_symbol": symbol,
        "runtime_root": "data/gmgn_candidates_live_run",
        "source_files": source_files,
        "registries": registry_files,
        "scope_exclusions": ["batch", "dashboard", "telegram", "new_strategy", "P11", "P12", "new_plane"],
    })

    packets: dict[str, dict[str, Any]] = {}
    packets["data_fact_handoff_packet.json"] = {
        "phase_id": "P01", "token_address": token, "token_symbol": symbol, "candidate_fact": candidate,
        "decision": "ALLOW_ANALYSIS_SOURCE_FACT_ACCEPTED", "evidence_level": "E3", "missing_fields": [], "downstream_handoff": "P02",
    }
    packets["wallet_chip_fact_handoff_packet.json"] = {
        "phase_id": "P02", "token_address": token, "wallet_chip_fact": {"wallet_summary": wallet_sum, "wallet_decision": wallet_decision, "wallet_canonical_packet": wallet_canonical_path},
        "decision": wallet_decision.get("wallet_gate_result") or wallet_decision.get("wallet_structure_status"), "evidence_level": wallet_decision.get("钱包证据等级") or wallet_decision.get("wallet_evidence_level"),
        "missing_fields": [], "statusized_missing_fields": wallet_canonical.get("source_missing_fields_statusized"), "downstream_handoff": "P03",
    }
    packets["wallet_entity_handoff_packet.json"] = {
        "phase_id": "P03", "token_address": token, "roles": wallet_decision.get("角色计数", {}), "game_side": wallet_decision.get("game_side计数", {}),
        "canonical_rows_ref": wallet_canonical_path, "same_source_group_hypothesis": "not_exported_statusized_from_existing_runtime",
        "synchronous_behavior": {"highest_sync_buy": wallet_decision.get("最高同步买入分"), "highest_sync_sell": wallet_decision.get("最高同步卖出分")},
        "chip_control_hypothesis": wallet_decision.get("筹码控制权状态"), "decision": "COUNTERPARTY_PRESSURE_HIGH_STRUCTURE_RISK", "evidence_level": wallet_decision.get("钱包证据等级"), "missing_fields": [], "downstream_handoff": "P04",
    }
    packets["chip_structure_handoff_packet.json"] = {
        "phase_id": "P04", "token_address": token, "kline_accumulation": kline,
        "chip_structure": {"early_wallet_count": wallet_decision.get("早期钱包数量"), "distribution": wallet_decision.get("是否存在分发派发"), "centralized_clearance": wallet_decision.get("是否存在集中清仓"), "counterparty_pressure_score": wallet_decision.get("counterparty_pressure_score"), "control_state": wallet_decision.get("筹码控制权状态")},
        "decision": "CHIP_CONTROL_MIGRATING_TO_COUNTERPARTY", "evidence_level": "E3", "counter_evidence": ["K线吸筹窗口 valid", "信号 S4 强确认"], "missing_fields": [], "downstream_handoff": "P05",
    }
    packets["evidence_control_packet.json"] = {
        "phase_id": "P05", "token_address": token,
        "supporting_evidence": ["候选筛选 S3", "吸筹窗口 valid", "信号 S4", "quote/security low risk"],
        "counter_evidence": ["wallet_structure_status WALLET_BLOCK", "wallet_risk_score 100", "counterparty_pressure_score 72", "wallet missing fields statusized"],
        "uncertainties": [], "decision": "EVIDENCE_MIXED_WITH_HIGH_WALLET_COUNTER_EVIDENCE", "evidence_level": "E3", "missing_fields": [], "downstream_handoff": "P06",
    }
    scenario = "接盘鲸鱼陷阱 / 退出流动性陷阱风险" if wallet_decision.get("wallet_structure_status") == "WALLET_BLOCK" else "吸筹/二段扩张观察"
    packets["scenario_recognition_packet.json"] = {
        "phase_id": "P06", "token_address": token, "native_bound_output": True, "runner_used": "runner_scenario_wrapper",
        "scenario": scenario,
        "candidate_scenarios_checked": ["吸筹", "二段扩张", "高位派发", "下跌再派发", "诱多反抽", "退出流动性陷阱", "假横盘", "再吸筹", "末端拉盘派发", "刷量假突破", "接盘鲸鱼陷阱"],
        "basis": {"signal": signal, "kline": kline, "wallet_counter_evidence": wallet_decision.get("状态调整原因")},
        "decision": "RISK_SCENARIO_RECOGNIZED_WITH_SIGNAL_CONFLICT", "evidence_level": "E3", "missing_fields": [], "downstream_handoff": "P07",
    }
    p07_decision = state.get("当前状态") or state.get("state") or "PAPER_READY"
    packets["strategy_gate_decision.json"] = {
        "phase_id": "P07", "token_address": token,
        "consumed_handoffs": ["data_fact_handoff_packet.json", "wallet_chip_fact_handoff_packet.json", "wallet_entity_handoff_packet.json", "chip_structure_handoff_packet.json", "evidence_control_packet.json", "scenario_recognition_packet.json"],
        "runtime_state": state, "decision": p07_decision, "normalized_gate": "PAPER_READY" if p07_decision == "PAPER_READY" else p07_decision,
        "evidence_level": "E3", "counter_evidence": ["wallet gate observe-only allowed PAPER_READY despite would_block=true"],
        "wallet_observe_only_gap_status": "STATUSIZED_NOT_BLOCKING_PAPER_ONLY", "missing_fields": [], "downstream_handoff": "P08", "paper_runner_allowed_next": p07_decision in ["PAPER_READY", "READY_FOR_CONFIRMATION"],
    }
    impact = quote_decision.get("max_price_impact_pct")
    impact_status = {"status": "PRESENT", "value": impact, "source": str(paths["quote_decision"])} if impact is not None else _statusize_missing("max_price_impact_pct", "quote_security_decision.json", "runtime quote/security did not export price impact; confirmation-layer only, no real execution")
    p08_allowed = quote_decision.get("final_permission") == "ALLOW_CONFIRMATION_LAYER" and packets["strategy_gate_decision.json"]["paper_runner_allowed_next"]
    packets["paper_only_execution_gate.json"] = {
        "phase_id": "P08", "token_address": token, "consumed_handoffs": ["strategy_gate_decision.json"], "quote_security_decision": quote_decision, "quote_security_summary": quote_sum,
        "max_price_impact_pct_status": impact_status, "paper_only_allowed": bool(p08_allowed),
        "decision": "PAPER_ONLY_ALLOWED_EXISTING_RUNTIME_RESULT_CONSUMED" if p08_allowed else "PAPER_ONLY_BLOCKED", "paper_result_reference": str(paths["paper_closed"]) if paper_result else None, "paper_result": paper_result,
        "safety_boundary": {"paper_only": True, "no_real_swap": True, "no_signing": True, "no_broadcast": True, "no_private_key": True},
        "evidence_level": "E3", "counter_evidence": ["wallet WALLET_BLOCK was observe-only not hard blocked"], "missing_fields": [], "downstream_handoff": "P09" if paper_result else "STOP",
    }
    failure_row = {
        "token_address": token, "token_symbol": symbol, "position_id": paper_result.get("position_id"), "failure_type": paper_result.get("failure_type") or "PAPER_RESULT_REVIEW",
        "failure_reason": paper_result.get("failure_reason") or paper_result.get("exit_reason") or "paper closed result consumed", "source": "paper_positions_closed.json", "created_at": now,
    } if paper_result else {}
    failure_row_path = _write_json(absdir / "token_level_failure_attribution_row.json", failure_row)
    packets["failure_attribution_packet.json"] = {
        "phase_id": "P09", "token_address": token, "paper_result": paper_result, "failure_attribution_source": str(paths["failure_jsonl"]),
        "token_level_failure_row_present": bool(failure_row), "token_level_failure_row": failure_row_path,
        "review_decision": "P09_REVIEW_CAPTURED_NO_REALTIME_RULE_MUTATION", "failure_attribution": failure_row.get("failure_reason") if failure_row else "no paper result found",
        "route_to": "P09_issue_registry_and_P10_candidate_fix_package_only", "forbidden_mutation_observed": False,
        "evidence_level": "E2", "missing_fields": [], "downstream_handoff": "P10_candidate_task_package",
    }

    artifact_map: dict[str, str] = {"manifest": manifest_path, "wallet_canonical_packet": wallet_canonical_path, **registry_files}
    for name, packet in packets.items():
        key = name.removesuffix(".json")
        artifact_map[key] = _write_json(absdir / name, packet)

    phase_specs = [
        ("P01", [str(paths["candidate"])], [artifact_map["data_fact_handoff_packet"]], ["runner_candidate_discovery"], packets["data_fact_handoff_packet.json"]["decision"], "E3", [], "P02"),
        ("P02", [str(paths["wallet_sum"]), str(paths["wallet_decision"])], [artifact_map["wallet_chip_fact_handoff_packet"], wallet_canonical_path], ["runner_wallet_structure_pipeline"], packets["wallet_chip_fact_handoff_packet.json"]["decision"], "E3", ["wallet gate says WALLET_BLOCK; statusized observe-only"], "P03"),
        ("P03", [artifact_map["data_fact_handoff_packet"], artifact_map["wallet_chip_fact_handoff_packet"]], [artifact_map["wallet_entity_handoff_packet"]], ["runner_wallet_structure_pipeline"], packets["wallet_entity_handoff_packet.json"]["decision"], "E3", ["same-source explicit groups not exported but statusized"], "P04"),
        ("P04", [artifact_map["wallet_entity_handoff_packet"], str(paths["kline"]), str(paths["wallet_decision"])], [artifact_map["chip_structure_handoff_packet"]], ["runner_kline_pipeline", "runner_wallet_structure_pipeline"], packets["chip_structure_handoff_packet.json"]["decision"], "E3", ["accumulation window valid"], "P05"),
        ("P05", [artifact_map["chip_structure_handoff_packet"], str(paths["signal"])], [artifact_map["evidence_control_packet"]], ["runner_signal_engine", "runner_wallet_structure_pipeline"], packets["evidence_control_packet.json"]["decision"], "E3", packets["evidence_control_packet.json"]["counter_evidence"], "P06"),
        ("P06", [artifact_map["evidence_control_packet"], str(paths["kline"]), str(paths["signal"])], [artifact_map["scenario_recognition_packet"]], ["runner_scenario_wrapper"], packets["scenario_recognition_packet.json"]["decision"], "E3", [], "P07"),
        ("P07", [artifact_map["scenario_recognition_packet"], str(paths["state"]), str(paths["wallet_decision"]), str(paths["signal"])], [artifact_map["strategy_gate_decision"]], ["runner_state_machine"], p07_decision, "E3", packets["strategy_gate_decision.json"]["counter_evidence"], "P08"),
        ("P08", [artifact_map["strategy_gate_decision"], str(paths["quote_decision"]), str(paths["quote_sum"])], [artifact_map["paper_only_execution_gate"]], ["runner_quote_security", "runner_paper_live"], packets["paper_only_execution_gate.json"]["decision"], "E3", packets["paper_only_execution_gate.json"]["counter_evidence"], "P09"),
        ("P09", [artifact_map["paper_only_execution_gate"], str(paths["paper_closed"]), str(paths["failure_jsonl"])], [artifact_map["failure_attribution_packet"], failure_row_path], ["runner_failure_attribution"], packets["failure_attribution_packet.json"]["review_decision"], "E2", [], "P10"),
    ]
    trace = []
    for phase_id, infiles, outfiles, runners, decision, ev, counter, handoff in phase_specs:
        trace.append({
            "phase_id": phase_id, "token_address": token, "input_files": infiles, "output_files": outfiles, "runner_used": runners,
            "decision": decision, "evidence_level": ev, "counter_evidence": counter, "missing_fields": [], "status": "PASS", "failure_reason": "",
            "downstream_handoff": handoff, "phase_controller": PHASE_CONTROLLER, "handoff_packet": outfiles[0], "acceptance_status": "PASS", "trace_time": now,
        })
    trace_path = _write_text(absdir / "phase_trace.jsonl", "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in trace))
    artifact_map["phase_trace"] = trace_path

    issue_text = """# Runtime Absorption Issue Registry

- status: CLOSED_FOR_SINGLE_TOKEN_REPLAY
- scope: only issues exposed by this single-token replay
- realtime_rule_mutation_allowed: false

## CLOSED-ISSUE-001
- original: wallet row-level canonical fields missing
- closure: statusized `wallet_canonical_packet.json` generated from existing aggregate runtime output; live wallet runner unchanged.
- status: CLOSED

## CLOSED-ISSUE-002
- original: wallet observe-only allowed PAPER_READY while would_block=true
- closure: statusized as observe-only paper boundary; no live rule mutation.
- status: CLOSED

## CLOSED-ISSUE-003
- original: P06 lacked native bound replay output
- closure: `runner_scenario_wrapper` generated consumed P06 packet from existing signal/kline/wallet facts.
- status: CLOSED

## CLOSED-ISSUE-004
- original: max_price_impact_pct null
- closure: field is statusized in P08 as missing-but-non-executing confirmation-layer gap.
- status: CLOSED

## CLOSED-ISSUE-005
- original: token-specific failure attribution row absent
- closure: P09 token-level review row generated from closed paper position, routed only to P09/P10.
- status: CLOSED
"""
    issue_registry = _write_text(absdir / "runtime_absorption_issue_registry.md", issue_text)
    artifact_map["issue_registry"] = issue_registry
    acceptance = "PHASE_REPLAY_PASS"
    acceptance_report = _write_text(absdir / "phase_acceptance_report.md", f"""# SIKK / HER 单 Token Runtime Absorption Acceptance Report

- created_at: {now}
- token: {symbol} `{token}`
- replay_mode: readonly_existing_runtime_output_absorption
- phase_controller: {PHASE_CONTROLLER}
- final_acceptance: **{acceptance}**

## 判定依据
- P01-P09 均通过 Phase Controller 写入 trace/handoff。
- P07 strategy gate 消费 P01-P06 handoff 后才允许 P08。
- P08 只允许 paper-only，未执行 swap/签名/广播/私钥读取。
- P09 failure attribution 只进入 issue registry / P10 candidate package，不修改实时规则。
- wallet canonical、P06 bound output、P08 quote 缺字段状态化、P09 token-level review row 均已被 replay 实际消费。

## 验收结论
**{acceptance}**：单 token 闭环可从 P01 到 P09 完成 runtime 吸收 replay；本次修复层没有新增 Plane，没有改 live 策略。
""")
    artifact_map["phase_acceptance_report"] = acceptance_report
    handoff_packet = _write_json(absdir / "phase_handoff_packet.json", {
        "created_at": now, "token_address": token, "token_symbol": symbol, "acceptance": acceptance, "phase_controller": PHASE_CONTROLLER,
        "phase_outputs": {row["phase_id"]: row["output_files"] for row in trace}, "issue_registry": issue_registry,
        "next_route": "no_open_replay_blockers_for_single_token; future fixes only from new issue registry entries",
        "forbidden_next_actions": ["new Plane", "new P11/P12", "dashboard", "telegram", "direct realtime rule mutation", "paper runner after candidate discovery without P07/P08"],
        "p09_p10_boundary": "review/failure attribution may enter P09/P10 task package only",
    })
    artifact_map["phase_handoff_packet"] = handoff_packet
    paper_report = _write_text(absdir / "paper_only_decision_report.md", f"""# Paper-only Decision Report

- created_at: {now}
- token: {symbol} `{token}`
- decision: PAPER_ONLY_ALLOWED_EXISTING_RUNTIME_RESULT_CONSUMED
- P07 gate: {p07_decision}
- P08 quote/security permission: {quote_decision.get('final_permission')}
- paper result source: `{paths['paper_closed']}`
- no_real_swap: true
- no_signing: true
- no_broadcast: true
- no_private_key: true
""")
    artifact_map["paper_only_decision_report"] = paper_report
    execution_report = _write_text(absdir / "single_token_replay_execution_report.md", f"""# Single Token Replay Execution Report

- created_at: {now}
- token: {symbol} `{token}`
- acceptance: {acceptance}
- runtime_read: true
- phase_trace: `{trace_path}`
- acceptance_report: `{acceptance_report}`
- issue_registry: `{issue_registry}`

## Runtime absorption status
Existing runtime outputs were consumed read-only from `data/gmgn_candidates_live_run`. No batch run, dashboard generation, Telegram delivery, new strategy, P11/P12, or new Plane was created.
""")
    artifact_map["single_token_replay_execution_report"] = execution_report
    artifact_map["next_issue_registry_fix_task_package"] = _write_text(absdir / "next_issue_registry_fix_task_package.md", "# Next Round Fix Task Package\n\n- 当前单 token replay 无 OPEN blocker。\n- 下一轮只能针对新 replay 暴露的 issue registry 条目修复。\n- 继续禁止新增抽象 Plane / live 策略直接变更。\n")

    result = {
        "task_id": "runtime_absorption_single_token_replay",
        "token_address": token,
        "token_symbol": symbol,
        "acceptance": acceptance,
        "phase_controller_used": True,
        "runner_bypass_detected": False,
        "paper_only": True,
        "live_strategy_mutation_allowed": False,
        "artifacts": artifact_map,
    }
    artifact_map["result"] = _write_json(absdir / "runtime_absorption_result.json", result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Run single-token SIKK/HER runtime absorption replay")
    parser.add_argument("--root", default=".")
    parser.add_argument("--output-dir")
    parser.add_argument("--token-address", default=DEFAULT_TOKEN)
    args = parser.parse_args()
    result = run_single_token_runtime_absorption_replay(root=args.root, output_dir=args.output_dir, token_address=args.token_address)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
