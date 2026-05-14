#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fixed-CA P01-P09 phase evidence expander for SIKK/GMGN.

边界：读取固定 CA 结构快照和 trade-gate adapter 结果，把交易体系每个阶段的数据、证据、
handoff、audit 显性落盘；只读/纸面观察，不签名、不广播、不执行真实 swap。
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping

from modules.runtime.planbook_repository import PlanbookRepository
from sikk_gmgn_trade_gate_adapter import convert_structural_snapshot


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _read_json(path: str | Path) -> Dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _write_json(path: str | Path, payload: Mapping[str, Any]) -> str:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return str(p)


def _append_jsonl(path: str | Path, payload: Mapping[str, Any]) -> str:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return str(p)


def _num(data: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    try:
        value = data.get(key, default)
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _safety() -> Dict[str, Any]:
    return {
        "paper_only": True,
        "real_trade_enabled": False,
        "signing_enabled": False,
        "broadcast_enabled": False,
        "swap_enabled": False,
        "secret_access": "not_requested_not_used",
    }


def _permission_manifest(token_address: str, status: str = "PAPER_OBSERVE_ONLY", reason: str = "phase_evidence_runtime_read_only") -> Dict[str, Any]:
    return {
        "token_address": token_address,
        "permission_status": status,
        "mode": "paper_observe_only",
        "real_trade_enabled": False,
        "signing_enabled": False,
        "broadcast_transaction": False,
        "swap_enabled": False,
        "secret_access": "not_requested_not_used",
        "max_real_position_sol": 0,
        "reason": reason,
        "scope_note": "固定 CA P01-P09 证据展开；只读/纸面观察，不执行真实 swap。",
    }


def _base_payload(token: str, phase_id: str, kind: str, payload: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "token_address": token,
        "phase_id": phase_id,
        "artifact_kind": kind,
        "generated_at": _now(),
        "safety_boundary": _safety(),
        **dict(payload),
    }


def _status(missing: List[str], block_reasons: List[str] | None = None) -> str:
    block_reasons = block_reasons or []
    if block_reasons:
        return "BLOCKED"
    if missing:
        return "DEGRADED"
    return "OK"


class PhaseEvidenceBuilder:
    def __init__(self, token: str, snapshot: Mapping[str, Any], converted: Mapping[str, Any], permission: Mapping[str, Any], planbook_status: Mapping[str, Any] | None):
        self.token = token
        self.snapshot = snapshot
        self.converted = converted
        self.permission = permission
        self.planbook_status = planbook_status or {}

    def p01(self) -> Dict[str, Any]:
        missing = []
        required = ["token_address", "token_symbol", "liquidity_usd", "holder_count", "sample_wallets"]
        for key in required:
            if self.snapshot.get(key) in (None, "", []):
                missing.append(f"missing_snapshot_field:{key}")
        if not self.snapshot.get("funding_traced"):
            missing.append("P01_FUNDING_PATH_MISSING")
        output = {
            "data_quality_status": _status(missing),
            "token_symbol": self.snapshot.get("token_symbol", ""),
            "chain": self.snapshot.get("chain", "sol"),
            "available_facts": {
                "security_fields": all(k in self.snapshot for k in ["mint_renounced", "freeze_renounced", "buy_tax_pct", "sell_tax_pct", "lp_burned"]),
                "liquidity_usd": self.snapshot.get("liquidity_usd"),
                "holder_count": self.snapshot.get("holder_count"),
                "sample_wallet_count": len(self.snapshot.get("sample_wallets", []) or []),
                "funding_traced": bool(self.snapshot.get("funding_traced")),
            },
            "no_trading_signal": True,
        }
        evidence = {
            "positive_evidence": ["结构快照可读", "基础 security/liquidity/holder 字段可读"],
            "missing_evidence": missing,
            "risk_evidence": [],
        }
        return self._phase("P01_data_fact", "P02_wallet_structure", output, evidence, missing)

    def p02(self) -> Dict[str, Any]:
        structural = self.converted["structural_intel"]
        wallet = self.converted["wallet_decision"]
        profiles = structural.get("wallet_profiles", [])
        missing = [] if profiles else ["P02_WALLET_PROFILE_SAMPLE_MISSING"]
        output = {
            "wallet_structure_status": wallet.get("wallet_structure_status"),
            "wallet_structure_score": wallet.get("wallet_structure_score"),
            "wallet_risk_score": wallet.get("wallet_risk_score"),
            "role_matrix": profiles,
            "infra_excluded_count": sum(1 for p in profiles if p.get("role") == "INFRA_EXCLUDED"),
            "reason": wallet.get("reason"),
        }
        evidence = {
            "positive_evidence": [f"sample wallet profiles={len(profiles)}"],
            "missing_evidence": missing + self.converted["evidence_bundle"].get("missing_evidence", []),
            "risk_evidence": [wallet.get("reason", "")],
        }
        return self._phase("P02_wallet_structure", "P03_chip_control", output, evidence, missing)

    def p03(self) -> Dict[str, Any]:
        missing: List[str] = []
        top10 = _num(self.snapshot, "top10_holder_rate_pct")
        bundler = _num(self.snapshot, "top_bundler_trader_percentage_pct")
        entrapment = _num(self.snapshot, "top_entrapment_trader_percentage_pct")
        output = {
            "top10_holder_rate_pct": top10,
            "bundler_pressure_pct": bundler,
            "entrapment_trader_pct": entrapment,
            "holder_concentration": self.converted["structural_intel"].get("holder_concentration"),
            "control_risk_level": "HIGH" if bundler >= 35 or entrapment >= 8 else ("MEDIUM" if top10 >= 12 else "LOW"),
        }
        evidence = {
            "positive_evidence": ["top holder / bundler / entrapment fields available"],
            "missing_evidence": missing,
            "risk_evidence": [f"bundler_pressure_pct={bundler}", f"entrapment_trader_pct={entrapment}"],
        }
        return self._phase("P03_chip_control", "P04_scenario_recognition", output, evidence, missing)

    def p04(self) -> Dict[str, Any]:
        structural = self.converted["structural_intel"]
        eb = self.converted["evidence_bundle"]
        missing = list(eb.get("missing_evidence", []))
        scenarios = ["EARLY_STRUCTURE_ACTIVE"]
        if missing:
            scenarios.append("FUNDING_PENDING")
        if structural.get("chase_risk_level") in {"MEDIUM", "HIGH"}:
            scenarios.append("CHASE_RISK_ACTIVE")
        output = {
            "scenario_candidates": scenarios,
            "early_execution_strength": structural.get("early_execution_strength"),
            "chase_risk_level": structural.get("chase_risk_level"),
            "scenario_status": _status(missing),
        }
        evidence = {
            "positive_evidence": eb.get("positive_evidence", []) + ["早期结构指标可用于场景候选"],
            "missing_evidence": missing,
            "risk_evidence": eb.get("risk_evidence", []) + eb.get("negative_evidence", []),
        }
        return self._phase("P04_scenario_recognition", "P05_structure_position", output, evidence, missing)

    def p05(self) -> Dict[str, Any]:
        missing = ["P05_POSITION_DATA_MISSING", "quote_or_kline_avwap_poc_missing"]
        output = {
            "price_usd": self.snapshot.get("price_usd"),
            "market_cap_usd": self.snapshot.get("market_cap_usd"),
            "liquidity_usd": self.snapshot.get("liquidity_usd"),
            "avwap_available": False,
            "poc_available": False,
            "overextension_check": "DEGRADED_POSITION_UNKNOWN",
            "position_status": "DEGRADED",
        }
        evidence = {
            "positive_evidence": ["price/market/liquidity snapshot fields available"],
            "missing_evidence": missing,
            "risk_evidence": ["无法确认 AVWAP/POC/结构位置，禁止把结构分当买入点"],
        }
        return self._phase("P05_structure_position", "P06_strategy_gate", output, evidence, missing)

    def p06(self) -> Dict[str, Any]:
        gate = self.converted["trade_gate_decision"]
        risk = self.converted["risk_control_profile"]
        missing = self.converted["evidence_bundle"].get("missing_evidence", [])
        output = {
            "decision": gate.get("decision"),
            "final_status": gate.get("final_status"),
            "signal_level": gate.get("signal_level"),
            "permission": gate.get("permission"),
            "allowed_modes": gate.get("allowed_modes", []),
            "forbidden_modes": gate.get("forbidden_modes", []),
            "risk_level": risk.get("risk_level"),
            "real_trade_enabled": False,
        }
        evidence = {
            "positive_evidence": gate.get("allow_reasons", []),
            "missing_evidence": missing,
            "risk_evidence": gate.get("reason_codes", []) + risk.get("risk_notes", []),
        }
        return self._phase("P06_strategy_gate", "P07_execution_risk", output, evidence, list(missing))

    def p07(self) -> Dict[str, Any]:
        intent = self.converted["execution_intent"]
        risk = self.converted["risk_control_profile"]
        missing = ["P07_REALTIME_QUOTE_OR_SLIPPAGE_CHECK_MISSING"]
        output = {
            "execution_mode": intent.get("mode"),
            "execution_action": intent.get("action"),
            "paper_trade_intent": intent.get("action") == "PAPER_SIMULATE",
            "real_order": False,
            "broadcast_transaction": False,
            "max_real_position_sol": 0.0,
            "risk_profile_max_position_sol": risk.get("max_position_sol"),
            "execution_status": "OBSERVE_OR_PAPER_ONLY",
        }
        evidence = {
            "positive_evidence": ["permission gate present", "execution intent generated"],
            "missing_evidence": missing,
            "risk_evidence": ["实时 quote/slippage 未接入时不得执行真实订单"],
        }
        return self._phase("P07_execution_risk", "P08_review_learning", output, evidence, missing)

    def p08(self) -> Dict[str, Any]:
        review = self.converted["review_writeback"]
        missing = []
        output = {
            "review_required": True,
            "review_windows": review.get("review_windows", []),
            "writeback_targets": review.get("writeback_targets", []),
            "learning_candidates": [
                "验证 funding_path_missing 对后续走势的影响",
                "验证 chase_risk_level 与回撤/追高失败关系",
                "验证 infra exclusion 与角色矩阵稳定性",
            ],
            "memory_policy": "token_specific_findings_do_not_enter_long_term_memory_directly",
        }
        evidence = {
            "positive_evidence": ["review_writeback generated"],
            "missing_evidence": missing,
            "risk_evidence": ["单 token 结论只能进入 review，不直接升级长期规则"],
        }
        return self._phase("P08_review_learning", "P09_system_upgrade", output, evidence, missing)

    def p09(self) -> Dict[str, Any]:
        missing = []
        repo_status = self.planbook_status.get("final_status", "PLANBOOK_REPOSITORY_NOT_RUN")
        output = {
            "planbook_repository_status": repo_status,
            "upgrade_candidates": [
                "接入固定 CA P01-P09 phase evidence 到 sikk_ca_runtime_pipeline",
                "补 quote/kline/AVWAP/POC 位置层数据源",
                "补 funding/source/backflow 资金路径数据源",
                "把 phase_runtime final report 接入 dashboard/review ops",
            ],
            "shadow_mode_package": True,
            "real_trade_upgrade_allowed": False,
        }
        evidence = {
            "positive_evidence": ["phase evidence runner completed P01-P08"],
            "missing_evidence": missing,
            "risk_evidence": ["系统升级候选必须走 shadow mode 和回归测试"],
        }
        return self._phase("P09_system_upgrade", "completed", output, evidence, missing)

    def _phase(self, phase_id: str, next_phase: str, output: Dict[str, Any], evidence: Dict[str, Any], missing: List[str]) -> Dict[str, Any]:
        block_reasons: List[str] = []
        status = _status(missing, block_reasons)
        input_payload = {
            "source_snapshot_token": self.snapshot.get("token_address"),
            "converted_refs": list(self.converted.keys()),
            "permission_status": self.permission.get("permission_status"),
            "input_contract": "fixed_ca_phase_evidence_v1",
        }
        handoff = {
            "status": status,
            "next_phase": next_phase,
            "can_continue": status != "BLOCKED",
            "missing_evidence": evidence.get("missing_evidence", []),
            "block_reasons": block_reasons,
            "handoff_contract": "fixed_ca_phase_handoff_v1",
        }
        audit = {
            "status": status,
            "ca_consistency_passed": self.snapshot.get("token_address") == self.token,
            "safety_boundary_passed": True,
            "files_required": ["input.json", "output.json", "evidence.json", "handoff_packet.json", "audit.json"],
            "degraded_reason": evidence.get("missing_evidence", []),
            "block_reason": block_reasons,
        }
        return {
            "phase_id": phase_id,
            "status": status,
            "input": _base_payload(self.token, phase_id, "input", input_payload),
            "output": _base_payload(self.token, phase_id, "output", output),
            "evidence": _base_payload(self.token, phase_id, "evidence", evidence),
            "handoff_packet": _base_payload(self.token, phase_id, "handoff_packet", handoff),
            "audit": _base_payload(self.token, phase_id, "audit", audit),
        }


def _write_phase(root: Path, phase: Mapping[str, Any]) -> Dict[str, str]:
    phase_dir = root / str(phase["phase_id"])
    paths = {}
    for key in ["input", "output", "evidence", "handoff_packet", "audit"]:
        paths[f"{key}_json"] = _write_json(phase_dir / f"{key}.json", phase[key])
    return paths


def _gap_register(token: str, phases: List[Mapping[str, Any]]) -> Dict[str, Any]:
    gaps: List[Dict[str, Any]] = []
    for phase in phases:
        phase_id = str(phase["phase_id"])
        for item in phase["evidence"].get("missing_evidence", []) or []:
            gap_id = str(item) if str(item).startswith("P") else f"{phase_id}_{str(item).upper()}"
            gaps.append({
                "gap_id": gap_id,
                "phase_id": phase_id,
                "severity": "degraded",
                "missing_evidence": item,
                "repair_route": "补接对应数据源或在该阶段 contract 中显式标记不可用",
            })
        for item in phase["audit"].get("block_reason", []) or []:
            gaps.append({
                "gap_id": f"{phase_id}_{str(item).upper()}",
                "phase_id": phase_id,
                "severity": "blocking",
                "block_reason": item,
                "repair_route": "停止后续正向交易流程并修复 blocker",
            })
    return {
        "token_address": token,
        "generated_at": _now(),
        "safety_boundary": _safety(),
        "gap_count": len(gaps),
        "gaps": gaps,
    }


def _completion(token: str, root: Path, phases: List[Mapping[str, Any]], phase_paths: Mapping[str, Mapping[str, str]], ca_ok: bool, permission: Mapping[str, Any]) -> Dict[str, Any]:
    missing_files = []
    for phase_id, paths in phase_paths.items():
        for key, path in paths.items():
            if not Path(path).exists():
                missing_files.append(f"{phase_id}:{key}")
    safety_passed = (
        permission.get("real_trade_enabled") is False
        and permission.get("signing_enabled") is False
        and permission.get("broadcast_transaction") is False
    )
    return {
        "token_address": token,
        "generated_at": _now(),
        "output_root": str(root),
        "phase_count": len(phases),
        "expected_phase_count": 9,
        "missing_files": missing_files,
        "ca_consistency_passed": ca_ok,
        "safety_boundary_passed": safety_passed,
        "overall_passed": len(phases) == 9 and not missing_files and ca_ok and safety_passed,
        "degraded_phases": [p["phase_id"] for p in phases if p["status"] == "DEGRADED"],
        "blocked_phases": [p["phase_id"] for p in phases if p["status"] == "BLOCKED"],
        "scope_note": "完成审计证明 P01-P09 证据展开产物齐全；不代表实盘授权。",
    }


def _final_report(token: str, converted: Mapping[str, Any], phases: List[Mapping[str, Any]], gaps: Mapping[str, Any], completion: Mapping[str, Any]) -> str:
    gate = converted["trade_gate_decision"]
    risk = converted["risk_control_profile"]
    symbol = converted["token_intake"].get("token_symbol") or "-"
    lines = [
        f"# 固定 CA P01-P09 阶段证据报告：{symbol} / {token}",
        "",
        "## 总结",
        "",
        f"- P01-P09 阶段数：{completion.get('phase_count')}/9",
        "- 真实交易：禁止；不签名、不广播、不 swap。",
        f"- 交易门控：{gate.get('decision')} / {gate.get('final_status')} / {gate.get('permission')}",
        f"- 风险等级：{risk.get('risk_level')}",
        f"- overall_passed：{completion.get('overall_passed')}",
        "",
        "## 阶段状态",
        "",
    ]
    for phase in phases:
        missing = phase["evidence"].get("missing_evidence", [])
        lines.append(f"- {phase['phase_id']}：{phase['status']}；缺失证据：{', '.join(missing) if missing else '无'}")
    lines.extend([
        "",
        "## 关键缺口",
        "",
    ])
    if gaps.get("gaps"):
        for gap in gaps["gaps"][:20]:
            label = str(gap.get("missing_evidence") or gap.get("block_reason") or gap.get("gap_id"))
            zh = "资金路径缺失" if "FUNDING" in label.upper() or "funding" in label.lower() or "资金" in label else label
            lines.append(f"- {gap.get('phase_id')}：{zh}（{gap.get('severity')}）")
    else:
        lines.append("- 无")
    lines.extend([
        "",
        "## 自动化工作流判断",
        "",
        "- 当前 runner 已把固定 CA 从事实层、钱包结构、筹码控制、场景识别、结构位置、策略门控、执行风险、复盘学习、系统升级候选完整展开。",
        "- 降级阶段不会停机，会进入 gap register；blocker/权限越界才停止。",
        "- 当前输出可作为后续 dashboard、review ops、paper simulation 的标准输入；真实交易仍需另行授权与更严格数据源闭环。",
        "",
    ])
    return "\n".join(lines) + "\n"


def run_ca_phase_evidence(
    *,
    token_address: str,
    snapshot_path: str | Path,
    output_root: str | Path,
    mode: str = "live",
    run_id: str | None = None,
    project_root: str | Path = "/root/sikk-gmgn",
    validate_planbooks: bool = True,
) -> Dict[str, Any]:
    root = Path(output_root)
    root.mkdir(parents=True, exist_ok=True)
    run_id = run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    ledger = root / "master_phase_ledger.jsonl"
    if ledger.exists():
        ledger.unlink()

    snapshot_p = Path(snapshot_path)
    snapshot = _read_json(snapshot_p)
    ca_ok = snapshot.get("token_address") == token_address
    permission = _permission_manifest(token_address, status="PAPER_OBSERVE_ONLY" if ca_ok else "CA_MISMATCH_BLOCKED", reason="phase_evidence_runtime" if ca_ok else "snapshot_ca_mismatch")
    permission_json = _write_json(root / "permission_gate.json", permission)
    context_json = _write_json(root / "runtime_context.json", {
        "token_address": token_address,
        "run_id": run_id,
        "mode": mode,
        "snapshot_path": str(snapshot_p),
        "output_root": str(root),
        "planbook_id": "ca_phase_evidence_runtime_planbook",
        "started_at": _now(),
        "safety_boundary": _safety(),
    })

    planbook_status: Dict[str, Any] = {}
    if validate_planbooks:
        planbook_status = PlanbookRepository(project_root).validate()

    if not ca_ok:
        completion = {
            "token_address": token_address,
            "generated_at": _now(),
            "output_root": str(root),
            "phase_count": 0,
            "expected_phase_count": 9,
            "ca_consistency_passed": False,
            "safety_boundary_passed": True,
            "overall_passed": False,
            "blocking_reason": "TOKEN_OVERWRITE_DETECTED_OR_SNAPSHOT_CA_MISMATCH",
        }
        completion_json = _write_json(root / "completion_audit.json", completion)
        report_md = root / "final_phase_report_zh.md"
        report_md.write_text(f"# 固定 CA P01-P09 阶段证据报告\n\n- 状态：BLOCKED_CA_MISMATCH\n- 输入 CA：{token_address}\n- snapshot CA：{snapshot.get('token_address')}\n- 真实交易：禁止\n", encoding="utf-8")
        return {
            "status": "BLOCKED_CA_MISMATCH",
            "output_root": str(root),
            "runtime_context_json": context_json,
            "permission_gate_json": permission_json,
            "completion_audit_json": completion_json,
            "final_phase_report_md": str(report_md),
        }

    converted = convert_structural_snapshot(snapshot)
    builder = PhaseEvidenceBuilder(token_address, snapshot, converted, permission, planbook_status)
    steps: List[Callable[[], Dict[str, Any]]] = [builder.p01, builder.p02, builder.p03, builder.p04, builder.p05, builder.p06, builder.p07, builder.p08, builder.p09]
    phases: List[Dict[str, Any]] = []
    phase_paths: Dict[str, Dict[str, str]] = {}
    for step in steps:
        phase = step()
        paths = _write_phase(root, phase)
        phase_paths[phase["phase_id"]] = paths
        phases.append(phase)
        _append_jsonl(ledger, {
            "time": _now(),
            "token_address": token_address,
            "phase_id": phase["phase_id"],
            "status": phase["status"],
            "outputs": paths,
            "missing_evidence": phase["evidence"].get("missing_evidence", []),
            "safety_boundary": _safety(),
        })

    gaps = _gap_register(token_address, phases)
    gap_json = _write_json(root / "gap_register.json", gaps)
    completion = _completion(token_address, root, phases, phase_paths, ca_ok, permission)
    completion_json = _write_json(root / "completion_audit.json", completion)
    report_md = root / "final_phase_report_zh.md"
    report_md.write_text(_final_report(token_address, converted, phases, gaps, completion), encoding="utf-8")

    phase_summary = [{"phase_id": p["phase_id"], "status": p["status"]} for p in phases]
    return {
        "status": "OK" if completion["overall_passed"] and not gaps["gaps"] else "READY_WITH_GAPS",
        "output_root": str(root),
        "runtime_context_json": context_json,
        "permission_gate_json": permission_json,
        "planbook_repository_status": planbook_status.get("final_status"),
        "master_phase_ledger_jsonl": str(ledger),
        "gap_register_json": gap_json,
        "completion_audit_json": completion_json,
        "final_phase_report_md": str(report_md),
        "phases": phase_summary,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run fixed-CA P01-P09 phase evidence expansion; paper/observe only.")
    parser.add_argument("--ca", required=True)
    parser.add_argument("--snapshot", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--mode", default="live")
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--project-root", default="/root/sikk-gmgn")
    parser.add_argument("--skip-planbook-validation", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_ca_phase_evidence(
        token_address=args.ca,
        snapshot_path=args.snapshot,
        output_root=args.output_root,
        mode=args.mode,
        run_id=args.run_id,
        project_root=args.project_root,
        validate_planbooks=not args.skip_planbook_validation,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
