#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fixed-CA runtime pipeline control shell for SIKK/GMGN.

边界：固定 CA → 结构快照 → trade gate → state/live/journal/audit；
只读/纸面观察，不签名、不广播、不执行真实 swap。
"""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Mapping

from sikk_candidate_state_machine import run_candidate_state_machine
from sikk_gmgn_trade_gate_adapter import convert_structural_snapshot, write_runtime_outputs
from sikk_live_run import build_enriched_runtime_statuses, _write_live_state, _write_trade_gate_journal


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _write_json(path: str | Path, payload: Mapping[str, Any]) -> str:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(p)


def _append_jsonl(path: str | Path, payload: Mapping[str, Any]) -> str:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return str(p)


def _read_json(path: str | Path) -> Dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _permission_manifest(*, token_address: str, status: str = "PAPER_OBSERVE_ONLY", reason: str = "read_only_runtime") -> Dict[str, Any]:
    return {
        "token_address": token_address,
        "permission_status": status,
        "mode": "paper_observe_only",
        "real_trade_enabled": False,
        "signing_enabled": False,
        "broadcast_transaction": False,
        "secret_access": "not_requested_not_used",
        "max_real_position_sol": 0,
        "reason": reason,
        "scope_note": "只读/纸面观察，不执行真实 swap。",
    }


def _audit_ca(token_address: str, snapshot: Mapping[str, Any], outputs: Mapping[str, Any] | None = None) -> Dict[str, Any]:
    checked = {"snapshot.token_address": str(snapshot.get("token_address") or "")}
    if outputs:
        for name, payload in outputs.items():
            if isinstance(payload, Mapping):
                checked[f"{name}.token_address"] = str(payload.get("token_address") or "")
    mismatches = {k: v for k, v in checked.items() if v != token_address}
    return {
        "token_address": token_address,
        "checked_fields": checked,
        "mismatches": mismatches,
        "overall_passed": not mismatches,
        "scope_note": "固定 CA 一致性审计；不执行真实 swap。",
    }


def _runtime_context(*, token_address: str, snapshot_path: Path, output_root: Path, mode: str, run_id: str) -> Dict[str, Any]:
    return {
        "run_id": run_id,
        "token_address": token_address,
        "chain": "sol",
        "mode": mode,
        "fixed_ca_mode": True,
        "no_discovery": True,
        "snapshot_path": str(snapshot_path),
        "output_root": str(output_root),
        "started_at": _now(),
        "safety_boundary": {
            "real_trade_enabled": False,
            "signing_enabled": False,
            "broadcast_enabled": False,
            "secret_access": "not_requested_not_used",
        },
    }


def _record_stage(ledger: Path, stage: str, status: str, **extra: Any) -> None:
    row = {"time": _now(), "stage": stage, "status": status, **extra}
    _append_jsonl(ledger, row)


def _trade_gate_summary(result: Mapping[str, Any]) -> Dict[str, Any]:
    gate = dict(result["trade_gate_decision"])
    evidence = result.get("evidence_bundle", {})
    risk = result.get("risk_control_profile", {})
    wallet = result.get("wallet_decision", {})
    execution = result.get("execution_intent", {})
    gate.update({
        "token_symbol": result.get("token_intake", {}).get("token_symbol", ""),
        "funding_status": evidence.get("funding_status", ""),
        "risk_level": risk.get("risk_level", ""),
        "execution_action": execution.get("action", ""),
        "wallet_structure_status": wallet.get("wallet_structure_status", ""),
        "wallet_structure_score": wallet.get("wallet_structure_score", ""),
        "wallet_risk_score": wallet.get("wallet_risk_score", ""),
    })
    return {"处理结果": [gate], "说明": "固定 CA trade gate runtime summary；不执行真实 swap。"}


def _candidate_payload(result: Mapping[str, Any]) -> Dict[str, Any]:
    intake = result["token_intake"]
    return {
        "候选结果": [{
            "代币地址": intake.get("token_address"),
            "代币符号": intake.get("token_symbol", ""),
            "筛选等级": "FIXED_CA_RUNTIME_INPUT",
            "是否进入候选池": True,
        }],
        "说明": "用户指定 CA 输入，禁用发现覆盖。",
    }


def _completion_audit(*, token_address: str, output_root: Path, permission: Mapping[str, Any], ca_audit: Mapping[str, Any], required_paths: Mapping[str, str]) -> Dict[str, Any]:
    missing = [key for key, path in required_paths.items() if not Path(path).exists()]
    safety_passed = (
        permission.get("real_trade_enabled") is False
        and permission.get("signing_enabled") is False
        and permission.get("broadcast_transaction") is False
    )
    passed = not missing and ca_audit.get("overall_passed") is True and safety_passed
    return {
        "token_address": token_address,
        "overall_passed": passed,
        "missing_outputs": missing,
        "ca_consistency_passed": ca_audit.get("overall_passed") is True,
        "safety_boundary_passed": safety_passed,
        "output_root": str(output_root),
        "scope_note": "完成审计仅证明固定 CA 纸面/观察链路产物齐全，不代表实盘授权。",
    }


def _final_report(token_address: str, result: Mapping[str, Any], live_state: Mapping[str, Any], completion: Mapping[str, Any]) -> str:
    gate = result["trade_gate_decision"]
    risk = result["risk_control_profile"]
    evidence = result["evidence_bundle"]
    token_symbol = result["token_intake"].get("token_symbol", "") or "-"
    status = (live_state.get("tokens") or [{}])[0]
    return "\n".join([
        f"# 固定 CA 运行报告：{token_symbol} / {token_address}",
        "",
        "## 结论",
        "",
        f"- 状态机：{status.get('current_state', '')}",
        f"- 系统动作：{status.get('latest_action', '')}",
        f"- 交易门控：{gate.get('decision')} / {gate.get('final_status')}",
        f"- 真实交易：{gate.get('permission')}；real_trade_enabled={gate.get('real_trade_enabled')}",
        f"- 合约权限：{gate.get('contract_permission')}",
        f"- 最大实盘仓位：{risk.get('max_position_sol', 0)}",
        "- 边界：不执行真实 swap，不签名，不广播。",
        "",
        "## 主要原因",
        "",
        f"- 资金状态：{evidence.get('funding_status')}",
        f"- 风险等级：{risk.get('risk_level')}",
        f"- 原因码：{', '.join(gate.get('reason_codes') or [])}",
        f"- 缺失证据：{', '.join(evidence.get('missing_evidence') or [])}",
        "",
        "## 完成审计",
        "",
        f"- overall_passed：{completion.get('overall_passed')}",
        f"- ca_consistency_passed：{completion.get('ca_consistency_passed')}",
        f"- safety_boundary_passed：{completion.get('safety_boundary_passed')}",
        "",
    ]) + "\n"


def run_ca_runtime_pipeline(
    *,
    token_address: str,
    snapshot_path: str | Path,
    output_root: str | Path,
    mode: str = "live",
    run_id: str | None = None,
) -> Dict[str, str]:
    root = Path(output_root)
    root.mkdir(parents=True, exist_ok=True)
    snapshot_p = Path(snapshot_path)
    run_id = run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    ledger = root / "stage_ledger.jsonl"
    if ledger.exists():
        ledger.unlink()

    context = _runtime_context(token_address=token_address, snapshot_path=snapshot_p, output_root=root, mode=mode, run_id=run_id)
    context_json = _write_json(root / "runtime_context.json", context)
    _record_stage(ledger, "runtime_context", "OK", output=context_json)

    snapshot = _read_json(snapshot_p)
    initial_audit = _audit_ca(token_address, snapshot)
    audit_json = _write_json(root / "ca_consistency_audit.json", initial_audit)
    _record_stage(ledger, "ca_consistency_audit", "OK" if initial_audit["overall_passed"] else "FAILED", output=audit_json)

    if not initial_audit["overall_passed"]:
        permission = _permission_manifest(token_address=token_address, status="CA_MISMATCH_BLOCKED", reason="snapshot_ca_mismatch")
        permission_json = _write_json(root / "permission_gate.json", permission)
        _record_stage(ledger, "permission_gate", "BLOCKED", output=permission_json)
        return {
            "status": "BLOCKED_CA_MISMATCH",
            "runtime_context_json": context_json,
            "permission_gate_json": permission_json,
            "stage_ledger_jsonl": str(ledger),
            "ca_consistency_audit_json": audit_json,
        }

    permission = _permission_manifest(token_address=token_address)
    permission_json = _write_json(root / "permission_gate.json", permission)
    _record_stage(ledger, "permission_gate", "OK", output=permission_json)

    converted = convert_structural_snapshot(snapshot)
    trade_gate_paths = write_runtime_outputs(converted, root / "trade_gate")
    _record_stage(ledger, "trade_gate_adapter", "OK", outputs=trade_gate_paths)

    final_ca_audit = _audit_ca(token_address, snapshot, converted)
    audit_json = _write_json(root / "ca_consistency_audit.json", final_ca_audit)

    trade_summary = _trade_gate_summary(converted)
    trade_summary_json = _write_json(root / "trade_gate_runtime" / "trade_gate_runtime_summary.json", trade_summary)
    candidates_json = _write_json(root / "fixed_ca_candidates.json", _candidate_payload(converted))
    _record_stage(ledger, "trade_gate_summary", "OK", output=trade_summary_json)

    state_paths = run_candidate_state_machine(
        candidates_path=candidates_json,
        trade_gate_summary_path=trade_summary_json,
        output_dir=root / "state_machine",
    )
    _record_stage(ledger, "state_machine", "OK", outputs=state_paths)

    now = _now()
    statuses = build_enriched_runtime_statuses(root, now)
    live_state_json = _write_live_state(root, statuses, now)
    live_state = _read_json(live_state_json)
    journal_jsonl = _write_trade_gate_journal(root, statuses, now)
    _record_stage(ledger, "live_state_and_journal", "OK", live_state=live_state_json, journal=journal_jsonl)

    review = dict(converted["review_writeback"])
    review.update({
        "runtime_review_status": "PENDING_HUMAN_REVIEW",
        "ca_pipeline_run_id": run_id,
        "journal_path": journal_jsonl,
        "scope_note": "复盘写回候选；不改变实盘权限。",
    })
    review_json = _write_json(root / "review_writeback.json", review)

    required = {
        "runtime_context_json": context_json,
        "permission_gate_json": permission_json,
        "stage_ledger_jsonl": str(ledger),
        "ca_consistency_audit_json": audit_json,
        "trade_gate_summary_json": trade_summary_json,
        "candidate_states_json": state_paths["states_json"],
        "live_state_json": live_state_json,
        "trade_gate_journal_jsonl": journal_jsonl,
        "review_writeback_json": review_json,
    }
    completion = _completion_audit(token_address=token_address, output_root=root, permission=permission, ca_audit=final_ca_audit, required_paths=required)
    completion_json = _write_json(root / "completion_audit.json", completion)
    _record_stage(ledger, "completion_audit", "OK" if completion["overall_passed"] else "FAILED", output=completion_json)

    report_md = root / "final_report_zh.md"
    report_md.write_text(_final_report(token_address, converted, live_state, completion), encoding="utf-8")

    return {
        "status": "OK" if completion["overall_passed"] else "DEGRADED",
        "runtime_context_json": context_json,
        "permission_gate_json": permission_json,
        "stage_ledger_jsonl": str(ledger),
        "ca_consistency_audit_json": audit_json,
        "trade_gate_summary_json": trade_summary_json,
        "candidate_states_json": state_paths["states_json"],
        "live_state_json": live_state_json,
        "trade_gate_journal_jsonl": journal_jsonl,
        "completion_audit_json": completion_json,
        "final_report_md": str(report_md),
        "review_writeback_json": review_json,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run fixed-CA SIKK runtime pipeline; paper/observe only.")
    parser.add_argument("--ca", required=True, help="requested token CA")
    parser.add_argument("--snapshot", required=True, help="structural snapshot JSON")
    parser.add_argument("--output-root", required=True, help="runtime output root")
    parser.add_argument("--mode", default="live")
    parser.add_argument("--run-id", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_ca_runtime_pipeline(
        token_address=args.ca,
        snapshot_path=args.snapshot,
        output_root=args.output_root,
        mode=args.mode,
        run_id=args.run_id,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
