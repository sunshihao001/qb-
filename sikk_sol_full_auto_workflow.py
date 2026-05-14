#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK-SOL GMGN/OKX one-shot compatibility workflow.

兼容路线说明：
- 本文件保留为 legacy/compat one-shot 验证入口，方便旧命令、旧任务包和一次性 readiness/sample 演练继续可用。
- canonical 主路线不是本文件，而是既有钱包结构系统：
  modules/source_wallet_bot → sikk_candidate_wallet_structure_pipeline.py →
  sikk_wallet_structure_gate.py → sikk_candidate_state_machine.py / sikk_live_run.py。
- 新 GMGN/OKX 只读 collector 能力应优先作为 Source Wallet Bot / 钱包结构 pipeline 的数据源，
  不应在本文件内扩展成第二套并行钱包结构分析系统。

安全边界：paper-only；只读；不执行真实 swap；不读取 .env/私钥；不签名；不 broadcast。
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from modules.shared_verification import validate_stage_output
from modules.source_wallet_bot.gmgn_okx_readonly_adapter import run_readonly_adapter_for_token

SAFETY_BOUNDARY = {
    "paper_only": True,
    "read_only_collectors": True,
    "real_swap_enabled": False,
    "private_key_required": False,
    "secret_file_reading_enabled": False,
    "signing_enabled": False,
    "broadcast_enabled": False,
    "live_disabled": True,
}

COMPATIBILITY_ROUTE = {
    "route_type": "legacy_compat_one_shot",
    "canonical_wallet_system": [
        "modules/source_wallet_bot",
        "sikk_candidate_wallet_structure_pipeline.py",
        "sikk_wallet_structure_gate.py",
        "sikk_candidate_state_machine.py",
        "sikk_live_run.py",
    ],
    "compat_policy": "保留旧 one-shot/readiness/sample 命令；新钱包结构能力必须优先接入 canonical source_wallet_bot + wallet_structure pipeline。",
    "not_primary_entry": True,
}

TOKEN_PASS = "SAFEPASS111111111111111111111111111111111111"
TOKEN_SAFETY_BLOCK = "SAFEBLOCK2222222222222222222222222222222222"
TOKEN_WATCH = "MARKETWATCH33333333333333333333333333333333"

GMGN_OKX_CAPABILITY_MAP = {
    "gmgn_market": {
        "role": "candidate_discovery_and_kline",
        "read_only": True,
        "can_do": ["trending", "trenches", "signal", "kline"],
        "stage_ids": ["stage_01_candidate_discovery", "stage_03_market_gate", "stage_08_kline_structure_analyzer"],
    },
    "gmgn_token": {
        "role": "token_wallet_behavior",
        "read_only": True,
        "can_do": ["info", "security", "pool", "holders", "traders"],
        "stage_ids": ["stage_02_safety_gate", "stage_05_early_wallet_analyzer", "stage_06_wallet_role_classifier"],
    },
    "okx_dex_token": {
        "role": "lp_cluster_toptrader_risk_metadata",
        "read_only": True,
        "can_do": ["price-info", "liquidity", "advanced-info", "holders", "top-trader", "trades", "cluster-overview", "cluster-top-holders", "cluster-list"],
        "stage_ids": ["stage_03_market_gate", "stage_04_lp_pool_dynamics", "stage_07_holder_cluster", "stage_09_chip_distribution_analyzer"],
    },
    "okx_dex_ws": {
        "role": "realtime_watch_stream",
        "read_only": True,
        "can_do": ["price", "candle", "price-info", "trades", "signals", "smartmoney_tracker", "address_tracker", "memepump_new_token", "memepump_update_metrics"],
        "stage_ids": ["stage_14_realtime_monitor", "stage_15_review_ops"],
    },
}


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(path: str | Path, payload: Mapping[str, Any]) -> str:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(p)


def append_jsonl(path: str | Path, row: Mapping[str, Any]) -> str:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(dict(row), ensure_ascii=False) + "\n")
    return str(p)


def run_command_probe(command: list[str], *, timeout: int = 12) -> dict[str, Any]:
    """Run non-secret help/probe commands only; never read .env or credential files."""
    executable = shutil.which(command[0])
    if not executable:
        return {"command": command[0], "available": False, "exit_code": None, "stdout_head": "", "stderr_head": ""}
    try:
        completed = subprocess.run(command, text=True, capture_output=True, timeout=timeout, check=False)
        return {
            "command": command[0],
            "available": True,
            "path": executable,
            "exit_code": completed.returncode,
            "stdout_head": completed.stdout[:500],
            "stderr_head": completed.stderr[:500],
        }
    except Exception as exc:  # pragma: no cover - defensive runtime capture
        return {"command": command[0], "available": True, "path": executable, "exit_code": "EXCEPTION", "error": type(exc).__name__}


def build_gmgn_okx_readiness() -> dict[str, Any]:
    gmgn_probe = run_command_probe(["gmgn-cli", "--help"])
    okx_probe = run_command_probe(["onchainos", "--help"])
    jq_probe = run_command_probe(["jq", "--version"])
    python_probe = run_command_probe(["python3", "--version"])
    ready = bool(gmgn_probe.get("available") and okx_probe.get("available") and gmgn_probe.get("exit_code") == 0 and okx_probe.get("exit_code") == 0)
    return {
        "checked_at": iso_now(),
        "overall_status": "READY_FOR_READONLY_RUN" if ready else "DEGRADED_SAMPLE_ONLY",
        "secret_policy": {
            "env_files_read": False,
            "private_keys_read": False,
            "secrets_printed": False,
            "note": "只执行 CLI help/probe；不读取 .env、私钥、助记词、连接串。",
        },
        "capability_map": GMGN_OKX_CAPABILITY_MAP,
        "tool_probes": {"gmgn_cli": gmgn_probe, "onchainos": okx_probe, "jq": jq_probe, "python3": python_probe},
        "missing_for_true_live_data": [
            "真实候选 token 地址或允许调用 market/trenches/hot-tokens 的只读发现窗口",
            "GMGN/OKX 返回 raw JSON 后的字段映射适配器",
            "OKX security token-scan 接入安全硬门禁",
            "GMGN holders/traders 与 OKX cluster/top-trader 的交叉验证器",
            "WebSocket session 生命周期控制与限频/空闲停止策略",
        ],
    }


def build_collector_command_plan(chain: str = "sol", token_address: str = "<token_address>") -> dict[str, Any]:
    return {
        "mode": "read_only_plan",
        "chain": chain,
        "token_address_placeholder": token_address,
        "commands": [
            {"source": "gmgn-market", "purpose": "候选发现/新币池", "cmd": f"gmgn-cli market trenches --chain {chain} --type new_creation --type near_completion --type completed --filter-preset safe --limit 80 --raw"},
            {"source": "gmgn-market", "purpose": "趋势发现", "cmd": f"gmgn-cli market trending --chain {chain} --interval 5m --order-by volume --limit 50 --raw"},
            {"source": "gmgn-token", "purpose": "token 基础/安全/池子", "cmd": f"gmgn-cli token info --chain {chain} --address {token_address} --raw && gmgn-cli token security --chain {chain} --address {token_address} --raw && gmgn-cli token pool --chain {chain} --address {token_address} --raw"},
            {"source": "gmgn-token", "purpose": "holder/trader 行为", "cmd": f"gmgn-cli token holders --chain {chain} --address {token_address} --limit 100 --raw && gmgn-cli token traders --chain {chain} --address {token_address} --limit 100 --raw"},
            {"source": "okx-dex-token", "purpose": "价格/LP/风险元数据", "cmd": f"onchainos token price-info --address {token_address} && onchainos token liquidity --address {token_address} && onchainos token advanced-info --address {token_address}"},
            {"source": "okx-dex-token", "purpose": "holder cluster/top trader", "cmd": f"onchainos token cluster-overview --address {token_address} && onchainos token cluster-top-holders --address {token_address} --range-filter 1 && onchainos token top-trader --address {token_address}"},
            {"source": "okx-dex-ws", "purpose": "实时流准备，不默认启动长连接", "cmd": "onchainos ws channels && onchainos ws channel-info --channel dex-market-memepump-new-token-openapi"},
        ],
        "blocked_commands": ["gmgn-cli swap", "onchainos swap", "broadcast", "sign", "send transaction"],
        "handoff_rule": "所有 collector raw 输出必须先转 StageOutput，再经 shared_verification PASS，才能进入状态机。",
    }


def _stage_output(stage_id: str, token: Mapping[str, Any], status: str, *, facts: dict[str, Any] | None = None, stats: dict[str, Any] | None = None, evidence_refs: list[str] | None = None, inference: dict[str, Any] | None = None, counter_evidence: list[Any] | None = None, source_skill: list[str] | None = None, invalidation_condition: str = "数据过期或反证出现时失效。") -> dict[str, Any]:
    return {
        "stage_id": stage_id,
        "status": status,
        "facts": {"token_address": token["token_address"], "chain": token.get("chain", "solana"), **(facts or {})},
        "stats": stats or {},
        "evidence": [{"source": ref, "claim": "只读证据/样例证据"} for ref in (evidence_refs or [stage_id])],
        "inference": inference or {},
        "counter_evidence": counter_evidence or [],
        "inference_boundary": "本输出为结构证据/纸面验证输入，不代表真实交易建议。",
        "source_skill": source_skill or ["sample-local-fixture"],
        "source_fields": list((facts or {}).keys()) + list((stats or {}).keys()) + list((inference or {}).keys()) + ["token_address", "chain"],
        "evidence_refs": evidence_refs or [f"sample:{stage_id}"],
        "freshness": {"observed_at": iso_now(), "max_age_sec": 3600},
        "invalidation_condition": invalidation_condition,
        "paper_only": True,
        "live_disabled": True,
    }


def build_sample_candidates(limit: int | None = None) -> list[dict[str, Any]]:
    rows = [
        {"token_address": TOKEN_PASS, "chain": "solana", "symbol": "AUTO", "market_cap": 180000, "liquidity_usd": 45000, "safety_block": False, "market_block": False, "wallet_structure_status": "WALLET_SUPPORT", "kline_status": "CONTROL_BOX_RETEST_VALID", "strategy_status": "PAPER_READY_CANDIDATE"},
        {"token_address": TOKEN_SAFETY_BLOCK, "chain": "solana", "symbol": "RISK", "market_cap": 90000, "liquidity_usd": 20000, "safety_block": True, "market_block": False, "wallet_structure_status": "UNKNOWN", "kline_status": "SKIPPED_BY_SAFETY", "strategy_status": "NOT_READY"},
        {"token_address": TOKEN_WATCH, "chain": "solana", "symbol": "OBS", "market_cap": 900000, "liquidity_usd": 15000, "safety_block": False, "market_block": False, "wallet_structure_status": "WALLET_PAUSE", "kline_status": "BOX_PENDING", "strategy_status": "WATCHING"},
    ]
    return rows[:limit] if limit else rows


def run_stage_pipeline(token: Mapping[str, Any], prebuilt_stage_outputs: list[dict[str, Any]] | None = None) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    stage_outputs: list[dict[str, Any]] = []
    validator_summaries: list[dict[str, Any]] = []
    if prebuilt_stage_outputs:
        for stage in prebuilt_stage_outputs:
            if "validation" not in stage:
                stage["validation"] = validate_stage_output(stage)
            stage_outputs.append(stage)
            validator_summaries.append({"token_address": token["token_address"], "stage_id": stage["stage_id"], **stage["validation"]})
        return stage_outputs, validator_summaries
    stages = [
        _stage_output("stage_01_candidate_discovery", token, "PASS", facts={"discovered_at": iso_now(), "symbol": token["symbol"]}, evidence_refs=["gmgn-market:trenches_or_trending", "okx-token:hot-tokens_optional"], source_skill=["gmgn-market", "okx-dex-token"]),
        _stage_output("stage_02_safety_gate", token, "BLOCK" if token.get("safety_block") else "PASS", facts={"safety_status": "SAFETY_BLOCK" if token.get("safety_block") else "SAFETY_PASS"}, evidence_refs=["gmgn-token:security", "okx-security:token-scan_pending"], source_skill=["gmgn-token", "okx-security"]),
        _stage_output("stage_03_market_gate", token, "BLOCK" if token.get("market_block") else "PASS", stats={"market_cap": token["market_cap"], "liquidity_usd": token["liquidity_usd"]}, evidence_refs=["gmgn-token:info", "gmgn-token:pool", "okx-token:price-info", "okx-token:liquidity"], source_skill=["gmgn-token", "okx-dex-token"]),
    ]
    if not token.get("safety_block") and not token.get("market_block"):
        stages.extend([
            _stage_output("stage_04_lp_pool_dynamics", token, "PASS", stats={"lp_dynamic_status": "STABLE_OR_PENDING", "liquidity_usd": token["liquidity_usd"]}, evidence_refs=["okx-token:liquidity", "gmgn-token:pool"], source_skill=["okx-dex-token", "gmgn-token"]),
            _stage_output("stage_05_early_wallet_analyzer", token, "PASS", facts={"early_wallet_count": 8}, evidence_refs=["gmgn-token:holders", "gmgn-token:traders"], source_skill=["gmgn-token"]),
            _stage_output("stage_06_wallet_role_classifier", token, "PASS", inference={"wallet_structure_status": token["wallet_structure_status"]}, evidence_refs=["gmgn-token:holders_tags", "gmgn-token:traders_pnl"], source_skill=["gmgn-token", "sikk-gmgn-structural-intelligence"]),
            _stage_output("stage_07_holder_cluster", token, "PASS" if token["wallet_structure_status"] == "WALLET_SUPPORT" else "WARN", inference={"holder_cluster_status": "CLUSTER_SUPPORT_PENDING_RAW" if token["wallet_structure_status"] == "WALLET_SUPPORT" else "CLUSTER_UNKNOWN"}, evidence_refs=["okx-token:cluster-overview", "okx-token:cluster-top-holders", "okx-token:cluster-list"], source_skill=["okx-dex-token"]),
            _stage_output("stage_08_kline_structure_analyzer", token, "PASS" if token["kline_status"] == "CONTROL_BOX_RETEST_VALID" else "WARN", inference={"kline_status": token["kline_status"]}, evidence_refs=["gmgn-market:kline", "okx-ws:candle_optional"], source_skill=["gmgn-market", "okx-dex-ws"]),
            _stage_output("stage_09_chip_distribution_analyzer", token, "PASS" if token["wallet_structure_status"] == "WALLET_SUPPORT" else "WARN", inference={"chip_control_status": "CONTROL_RETAINED" if token["wallet_structure_status"] == "WALLET_SUPPORT" else "PARTIAL_OR_UNKNOWN"}, evidence_refs=["gmgn-token:holders", "okx-token:cluster-list", "okx-token:top-trader"], source_skill=["gmgn-token", "okx-dex-token"]),
            _stage_output("stage_12_strategy_fit_engine", token, "PASS" if token["strategy_status"] == "PAPER_READY_CANDIDATE" else "WARN", inference={"strategy_fit_status": token["strategy_status"]}, evidence_refs=["sikk:strategy_fit", "gmgn-market:kline"], source_skill=["sikk-sol-auto-trading-readiness", "gmgn-market"]),
        ])
    for stage in stages:
        validation = validate_stage_output(stage)
        stage["validation"] = validation
        stage_outputs.append(stage)
        validator_summaries.append({"token_address": token["token_address"], "stage_id": stage["stage_id"], **validation})
    return stage_outputs, validator_summaries


def derive_token_from_stage_outputs(stage_outputs: list[Mapping[str, Any]], fallback_token_address: str) -> dict[str, Any]:
    facts: dict[str, Any] = {}
    stats: dict[str, Any] = {}
    inference: dict[str, Any] = {}
    stage_status = {str(stage.get("stage_id")): str(stage.get("status")) for stage in stage_outputs}
    for stage in stage_outputs:
        if isinstance(stage.get("facts"), Mapping):
            facts.update(stage["facts"])
        if isinstance(stage.get("stats"), Mapping):
            stats.update({k: v for k, v in stage["stats"].items() if v is not None})
        if isinstance(stage.get("inference"), Mapping):
            inference.update(stage["inference"])
    wallet_structure_status = "WALLET_SUPPORT" if stage_status.get("stage_05_early_wallet_analyzer") == "PASS" and stage_status.get("stage_09_chip_distribution_analyzer") == "PASS" else "WALLET_PAUSE"
    if stage_status.get("stage_07_holder_cluster") in {"PASS", "WARN"} and wallet_structure_status == "WALLET_SUPPORT":
        wallet_structure_status = "WALLET_SUPPORT"
    return {
        "token_address": str(facts.get("token_address") or fallback_token_address),
        "chain": str(facts.get("chain") or "solana"),
        "symbol": str(facts.get("symbol") or "RAW"),
        "market_cap": float(stats.get("market_cap") or 0),
        "liquidity_usd": float(stats.get("liquidity_usd") or 0),
        "safety_block": stage_status.get("stage_02_safety_gate") == "BLOCK",
        "market_block": stage_status.get("stage_03_market_gate") == "BLOCK",
        "wallet_structure_status": wallet_structure_status,
        "kline_status": "RAW_KLINE_PENDING",
        "strategy_status": "PAPER_READY_CANDIDATE" if wallet_structure_status == "WALLET_SUPPORT" else "WATCHING",
        "raw_stage_status": stage_status,
        "raw_inference": inference,
    }


def derive_state(token: Mapping[str, Any], stages: list[Mapping[str, Any]]) -> dict[str, Any]:
    stage_status = {stage["stage_id"]: stage["status"] for stage in stages}
    if stage_status.get("stage_02_safety_gate") == "BLOCK":
        final_state = "EXCLUDE"; reason = "安全硬风险 BLOCK，禁止进入后续结构分析。"
    elif stage_status.get("stage_03_market_gate") == "BLOCK":
        final_state = "RECORD_ONLY"; reason = "市场硬风险 BLOCK，仅记录不进入结构机会判断。"
    elif token.get("wallet_structure_status") == "WALLET_SUPPORT" and token.get("kline_status") == "CONTROL_BOX_RETEST_VALID" and token.get("strategy_status") == "PAPER_READY_CANDIDATE":
        final_state = "PAPER_READY"; reason = "安全/市场通过，钱包结构支持、K线箱体回踩有效、策略适配通过；仅进入纸面验证。"
    elif token.get("wallet_structure_status") == "WALLET_PAUSE":
        final_state = "WATCHING"; reason = "钱包结构暂停或证据不足，继续观察。"
    else:
        final_state = "WATCHING"; reason = "证据不足，保持观察。"
    evidence_refs: list[str] = []
    for stage in stages:
        evidence_refs.extend(stage.get("evidence_refs") or [])
    state_output = _stage_output("stage_13_state_machine", token, final_state, inference={"wallet_structure_status": token.get("wallet_structure_status"), "final_state": final_state, "paper_ready_reason": reason}, evidence_refs=evidence_refs, source_skill=["sikk-runtime-architecture", "shared-verification"], invalidation_condition="安全/市场转 BLOCK、钱包结构转 PAUSE/BLOCK、K线结构破坏或纸面验证失败。")
    validation = validate_stage_output(state_output)
    return {"token_address": token["token_address"], "symbol": token["symbol"], "final_state": final_state, "transition_reason": reason, "support_evidence": evidence_refs, "counter_evidence": [], "invalidation_condition": state_output["invalidation_condition"], "next_review_at": iso_now(), "live_disabled": True, "validation": validation}


def build_explanation(state: Mapping[str, Any]) -> dict[str, Any]:
    return {"token_address": state["token_address"], "final_state": state["final_state"], "claim_type": "state_machine_handoff", "summary": state["transition_reason"], "evidence_refs": state["support_evidence"], "counter_evidence": state["counter_evidence"], "inference_boundary": "状态输出只用于排除/记录/观察/纸面验证/人工确认，不代表真实买入。", "audit_status": "PASS" if state["validation"]["overall_status"] == "PASS" else "FAIL"}


def build_paper_validation(state: Mapping[str, Any]) -> dict[str, Any]:
    if state["final_state"] != "PAPER_READY":
        return {"token_address": state["token_address"], "paper_status": "SKIPPED", "reason": "不是 PAPER_READY，不进入纸面验证。", "live_disabled": True}
    return {"token_address": state["token_address"], "paper_status": "PAPER_CANDIDATE_CREATED", "paper_entry": "WAIT_FOR_MANUAL_OR_NEXT_TICK_CONFIRMATION", "max_position_sol": 0.01, "exit_condition": state["invalidation_condition"], "live_disabled": True}


def run_full_auto_workflow(*, output_root: str | Path = "data/sikk_sol_full_auto_workflow", mode: str = "sample", max_candidates: int | None = None, token_address: str | None = None, allow_network: bool = True) -> dict[str, Any]:
    root = Path(output_root)
    now = iso_now()
    execution_log = root / "execution_log.jsonl"
    if execution_log.exists(): execution_log.unlink()
    active_task_state = {"task": "sikk_sol_gmgn_okx_full_auto_workflow", "mode": mode, "started_at": now, "safety_boundary": SAFETY_BOUNDARY, "compatibility_route": COMPATIBILITY_ROUTE, "state": "RUNNING"}
    active_task_state_json = write_json(root / "active_task_state.json", active_task_state)
    append_jsonl(execution_log, {"at": now, "phase": "START", "status": "OK", "note": "paper-only read-only one-shot compatibility workflow; canonical wallet route remains source_wallet_bot + wallet_structure_pipeline"})

    readiness = build_gmgn_okx_readiness()
    readiness_json = write_json(root / "readiness" / "gmgn_okx_readiness.json", readiness)
    command_plan = build_collector_command_plan()
    command_plan_json = write_json(root / "readiness" / "collector_command_plan.json", command_plan)
    append_jsonl(execution_log, {"at": iso_now(), "phase": "READINESS", "status": readiness["overall_status"]})

    if mode not in {"sample", "readiness", "auto-readonly"}:
        raise ValueError("仅支持 sample/readiness/auto-readonly；真实交易模式被禁用。")

    # auto-readonly: 若提供 token_address，则真实调用 GMGN/OKX 只读 raw collector；失败或未提供则降级 sample。
    raw_stage_by_token: dict[str, list[dict[str, Any]]] = {}
    if mode == "auto-readonly" and token_address:
        token_root = root / "source_wallet_bot" / "paper" / token_address
        adapter_result = run_readonly_adapter_for_token(token_address, output_root=token_root, limit=max_candidates or 50, allow_network=allow_network)
        raw_stage_outputs = adapter_result["mapped"]["stage_outputs"]
        raw_token = derive_token_from_stage_outputs(raw_stage_outputs, token_address)
        candidates = [raw_token]
        raw_stage_by_token[raw_token["token_address"]] = raw_stage_outputs
        facts_payload = {"candidates": candidates, "created_at": now, "candidate_source": "gmgn_okx_readonly_raw_adapter", "adapter_stage_outputs_path": adapter_result["stage_outputs_path"], "gmgn_okx_readiness": readiness["overall_status"]}
    else:
        # 当前自动发现真实 token 的 raw 适配器未提供地址时，自动降级到可验证 sample 候选；不中断工作流。
        candidates = build_sample_candidates(max_candidates)
        facts_payload = {"candidates": candidates, "created_at": now, "candidate_source": "sample_fallback_after_readiness", "gmgn_okx_readiness": readiness["overall_status"]}
    write_json(root / "facts" / "candidates.json", facts_payload)

    all_stage_outputs: list[dict[str, Any]] = []
    all_validator_summaries: list[dict[str, Any]] = []
    states: list[dict[str, Any]] = []
    explanations: list[dict[str, Any]] = []
    paper_validations: list[dict[str, Any]] = []
    for token in candidates:
        append_jsonl(execution_log, {"at": iso_now(), "phase": "TOKEN_START", "token_address": token["token_address"]})
        stages, validations = run_stage_pipeline(token, raw_stage_by_token.get(token["token_address"]))
        all_stage_outputs.extend(stages); all_validator_summaries.extend(validations)
        state = derive_state(token, stages); states.append(state)
        explanations.append(build_explanation(state)); paper_validations.append(build_paper_validation(state))
        append_jsonl(execution_log, {"at": iso_now(), "phase": "TOKEN_DONE", "token_address": token["token_address"], "final_state": state["final_state"]})

    states_payload = {"created_at": iso_now(), "states": states, "state_counts": dict(Counter(row["final_state"] for row in states)), "safety_boundary": SAFETY_BOUNDARY, "compatibility_route": COMPATIBILITY_ROUTE}
    state_machine_json = write_json(root / "state_machine" / "candidate_states.validated.json", states_payload)
    stage_outputs_json = write_json(root / "stage_outputs" / "stage_outputs.validated.json", {"stage_outputs": all_stage_outputs})
    explanation_json = write_json(root / "explanation" / "explanation_audit.json", {"explanations": explanations})
    paper_json = write_json(root / "paper_validation" / "paper_validation.json", {"paper_validations": paper_validations})

    validation_failures = [item for item in all_validator_summaries if item.get("overall_status") != "PASS"]
    state_validation_failures = [row for row in states if row.get("validation", {}).get("overall_status") != "PASS"]
    verification = {"overall_status": "PASS" if not validation_failures and not state_validation_failures else "FAIL", "stage_outputs_checked": len(all_stage_outputs), "state_outputs_checked": len(states), "validation_failures": validation_failures, "state_validation_failures": state_validation_failures, "no_real_trading": True, "read_only_collectors": True, "readiness_status": readiness["overall_status"], "safety_boundary": SAFETY_BOUNDARY, "checked_at": iso_now()}
    verification_report_json = write_json(root / "verification" / "verification_report.json", verification)

    final_lines = ["# SIKK-SOL GMGN/OKX 兼容路线 one-shot 工作流报告", "", f"- 模式：{mode}；GMGN/OKX readiness + sample fallback 兼容验证。", "- 兼容定位：本文件保留为 legacy/compat one-shot 路线，不是钱包结构分析主入口。", "- 主路线：modules/source_wallet_bot → sikk_candidate_wallet_structure_pipeline.py → sikk_wallet_structure_gate.py → sikk_live_run.py。", "- 边界：paper-only；只读；不执行真实交易；不读取 .env/私钥；不签名；不 broadcast。", f"- GMGN/OKX readiness：{readiness['overall_status']}", f"- 总候选：{len(candidates)}", f"- 阶段输出：{len(all_stage_outputs)}", f"- 验证状态：{verification['overall_status']}", "", "## GMGN/OKX 已准备能力", "- GMGN market：trenches/trending/signal/kline。", "- GMGN token：info/security/pool/holders/traders。", "- OKX token：price-info/liquidity/advanced-info/top-trader/trades/cluster。", "- OKX ws：price/candle/trades/signals/memepump。", "", "## 兼容路线规则", "- 保留旧命令、旧任务包和一次性 readiness/sample 演练。", "- 新钱包结构能力必须优先接入 canonical source_wallet_bot + wallet_structure pipeline。", "- 不在本文件内扩展第二套并行钱包结构分析系统。", "", "## 仍需接入项", *[f"- {x}" for x in readiness["missing_for_true_live_data"]], "", "## 状态统计"]
    for state, count in states_payload["state_counts"].items(): final_lines.append(f"- {state}: {count}")
    final_lines.extend(["", "## Token 输出"])
    for row in states: final_lines.append(f"- {row['symbol']} `{row['token_address']}`：{row['final_state']}｜{row['transition_reason']}")
    final_lines.extend(["", "## 下一步", "- 已生成 collector_command_plan.json；真实 GMGN/OKX raw 输出必须先转 StageOutput，再由 shared_verification 放行。"])
    final_report_md = root / "reports" / "SIKK_SOL_GMGN_OKX_FULL_AUTO_WORKFLOW_REPORT.md"
    final_report_md.parent.mkdir(parents=True, exist_ok=True)
    final_report_md.write_text("\n".join(final_lines) + "\n", encoding="utf-8")

    manifest = {"workflow_status": "COMPLETED_WITH_VERIFICATION" if verification["overall_status"] == "PASS" else "COMPLETED_WITH_VALIDATION_FAILURES", "created_at": iso_now(), "output_root": str(root), "active_task_state_json": active_task_state_json, "execution_log_jsonl": str(execution_log), "readiness_json": readiness_json, "collector_command_plan_json": command_plan_json, "stage_outputs_json": stage_outputs_json, "state_machine_json": state_machine_json, "explanation_json": explanation_json, "paper_validation_json": paper_json, "verification_report_json": verification_report_json, "final_report_md": str(final_report_md), "safety_boundary": SAFETY_BOUNDARY, "compatibility_route": COMPATIBILITY_ROUTE}
    workflow_manifest_json = write_json(root / "workflow_manifest.json", manifest)
    active_task_state.update({"state": manifest["workflow_status"], "finished_at": iso_now(), "workflow_manifest_json": workflow_manifest_json})
    write_json(active_task_state_json, active_task_state)
    append_jsonl(execution_log, {"at": iso_now(), "phase": "FINISH", "status": manifest["workflow_status"], "verification": verification["overall_status"]})
    return {**manifest, "workflow_manifest_json": workflow_manifest_json}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SIKK-SOL GMGN/OKX 兼容路线 one-shot 工作流（paper-only/read-only；非主钱包结构入口）")
    parser.add_argument("--output-root", default="data/sikk_sol_full_auto_workflow")
    parser.add_argument("--mode", default="readiness", choices=["sample", "readiness", "auto-readonly"])
    parser.add_argument("--max-candidates", type=int, default=None)
    parser.add_argument("--token-address", default=None, help="auto-readonly 模式下接入 GMGN/OKX 只读 raw collector 的 Solana token 地址")
    parser.add_argument("--no-network", action="store_true", help="测试/演练：不调用外部 CLI，仅生成降级 raw 记录")
    parser.add_argument("--paper-only", action="store_true", help="必须显式传入；确认不执行真实交易")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.paper_only:
        raise SystemExit("安全拒绝：必须显式传入 --paper-only；本文件不支持真实交易。")
    print(json.dumps(run_full_auto_workflow(output_root=args.output_root, mode=args.mode, max_candidates=args.max_candidates, token_address=args.token_address, allow_network=not args.no_network), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
