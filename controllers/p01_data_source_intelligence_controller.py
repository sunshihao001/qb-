#!/usr/bin/env python3
"""P01 Data Source Intelligence Controller.

Control-plane-first implementation for the K00 accepted P01 DSIC task package.
It creates deterministic system artifacts and handoff/quality/audit packets without
performing live trading, signing, broadcasting, or direct downstream raw access.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

DOC_ID = "DOC-20260513-P01-DSIC-001"
SCHEMA_VERSION = "P01_DATA_SOURCE_INTELLIGENCE_V2_SCAFFOLD"
TOKEN_PLACEHOLDER = "SYSTEM_ARCHIVE"
STATUSES = {
    "source": ["SOURCE_RELIABLE", "SOURCE_DEGRADED", "SOURCE_UNSTABLE", "SOURCE_BLOCKED", "SOURCE_SCHEMA_REVIEW", "SOURCE_RATE_LIMITED", "SOURCE_REPLAY_ONLY"],
    "field": ["FIELD_PRESENT", "FIELD_MISSING_REQUIRED", "FIELD_MISSING_OPTIONAL", "FIELD_STALE", "FIELD_CONFLICTED", "FIELD_SCHEMA_CHANGED", "FIELD_SOURCE_LIMITED", "FIELD_DERIVED", "FIELD_LOW_CONFIDENCE"],
    "data": ["DATA_READY", "DATA_READY_WITH_LIMITATIONS", "DATA_PARTIAL_READY", "DATA_PAUSE", "DATA_BLOCK", "DATA_SCHEMA_REVIEW", "DATA_REPLAY_ONLY", "DATA_BACKFILL_REQUIRED"],
    "permission": ["ALLOW", "ALLOW_LIMITED", "PAUSE", "BLOCK", "REPLAY_ONLY", "SCHEMA_REVIEW_REQUIRED"],
}
PERMISSIONS = {
    "real_execution_allowed": False,
    "paper_runtime_allowed": False,
    "live_execution_allowed": False,
    "raw_direct_access_allowed": False,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ensure(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path: Path, data: Any) -> Path:
    ensure(path.parent)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def write_text(path: Path, content: str) -> Path:
    ensure(path.parent)
    path.write_text(content, encoding="utf-8")
    return path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


class P01DataSourceIntelligenceController:
    def __init__(self, run_dir: Path, repo_root: Path, token: str = TOKEN_PLACEHOLDER, chain: str = "solana") -> None:
        self.repo_root = repo_root
        self.run_dir = run_dir if run_dir.is_absolute() else repo_root / run_dir
        self.p01 = self.run_dir / "p01_data_fact"
        self.token = token
        self.chain = chain
        self.created: List[str] = []
        self.task_package = repo_root / "sikk_stable_trader_os/00_knowledge_intake/task_packages/task_execution_package_DOC-20260513-P01-DSIC-001.json"

    def record(self, path: Path) -> Path:
        self.created.append(str(path))
        return path

    def dirs(self) -> None:
        base_dirs = [
            "phase_identity", "source_registry", "source_health", "acquisition_planner",
            "raw/gmgn", "raw/okx", "schema_monitor", f"normalized/{self.token}",
            f"lineage/{self.token}", f"temporal/{self.token}", f"reconciliation/{self.token}",
            f"quality/{self.token}", f"handoff/{self.token}", "replay_fixture/fixture_tokens",
            "backfill", "audit", "multi_role_audit", "manifest",
        ]
        for d in base_dirs:
            ensure(self.p01 / d)

    def init_phase(self) -> Dict[str, Any]:
        self.dirs()
        yaml = """phase_id: P01\nphase_name: P01_data_source_intelligence_controller\nsource_doc_id: DOC-20260513-P01-DSIC-001\nrole: data_source_intelligence_controller\nnot_roles:\n  - strategy_decision\n  - wallet_structure_judgment\n  - paper_entry\n  - real_execution\npermissions:\n  real_execution_allowed: false\n  paper_runtime_allowed: false\n  live_execution_allowed: false\n  raw_direct_access_allowed: false\nstatus_codes:\n  source: [SOURCE_RELIABLE, SOURCE_DEGRADED, SOURCE_UNSTABLE, SOURCE_BLOCKED, SOURCE_SCHEMA_REVIEW, SOURCE_RATE_LIMITED, SOURCE_REPLAY_ONLY]\n  data: [DATA_READY, DATA_READY_WITH_LIMITATIONS, DATA_PARTIAL_READY, DATA_PAUSE, DATA_BLOCK, DATA_SCHEMA_REVIEW, DATA_REPLAY_ONLY, DATA_BACKFILL_REQUIRED]\n"""
        self.record(write_text(self.p01 / "phase_identity/phase_01_data_source_intelligence_controller.yaml", yaml))
        md = """# P01 数据源情报控制层\n\nP01 不是普通采集脚本集合，而是判断外部数据是否足以成为系统事实的控制层。\n\n## 负责\n- 数据源注册、健康、SLA\n- raw snapshot 与事件溯源\n- schema drift / freshness / lineage / reconciliation\n- completeness probability / missing root cause / quality decision\n- downstream permission handoff\n\n## 不负责\n- 不做策略判断\n- 不做钱包结构正向判断\n- 不做 paper entry\n- 不做真实交易、签名、广播、swap\n"""
        self.record(write_text(self.p01 / "phase_identity/phase_01_data_source_intelligence_controller.md", md))
        return {"mode": "init-phase", "status": "PHASE_IDENTITY_READY"}

    def source_registry(self) -> Dict[str, Any]:
        profiles = {
            "gmgn": {"source_id":"gmgn","source_type":"market_wallet_intelligence","live_fetch_enabled":False,"capabilities":["token_profile","trade_events","holder_list","wallet_profile"],"requires_live_audit":True},
            "okx": {"source_id":"okx","source_type":"quote_liquidity_security_route","live_fetch_enabled":False,"capabilities":["quote","liquidity","route","security"],"requires_live_audit":True},
            "manual": {"source_id":"manual","source_type":"human_supplied_evidence","live_fetch_enabled":False,"capabilities":["gap_fill","review_notes"]},
            "cache": {"source_id":"local_cache","source_type":"local_readonly_cache","live_fetch_enabled":False,"capabilities":["replay","fallback_read"]},
            "replay": {"source_id":"replay_fixture","source_type":"controlled_fixture","live_fetch_enabled":False,"capabilities":["offline_validation","regression"]},
        }
        for key, profile in profiles.items():
            self.record(write_json(self.p01 / f"source_registry/{key}_source_profile.json", profile))
        matrix = {"schema_version": SCHEMA_VERSION, "sources": profiles, "required_live_audits":["gmgn","okx"]}
        self.record(write_json(self.p01 / "source_registry/source_capability_matrix.json", matrix))
        self.record(write_json(self.p01 / "source_registry/source_dependency_graph.json", {"nodes": list(profiles), "edges": [{"from":"gmgn","to":"reconciliation"},{"from":"okx","to":"reconciliation"},{"from":"replay","to":"quality_brain"}]}))
        return {"mode":"source-registry","status":"SOURCE_REGISTRY_READY"}

    def source_health(self) -> Dict[str, Any]:
        self.source_registry()
        reports = {}
        for source_id, base in [("gmgn",0.55),("okx",0.55)]:
            report = {
                "source_id": source_id,
                "source_reliability_score": base,
                "availability_score": 0.5,
                "latency_score": 0.5,
                "success_rate_score": 0.5,
                "schema_stability_score": 0.5,
                "freshness_score": 0.0,
                "historical_failure_score": 0.5,
                "source_consistency_score": 0.0,
                "current_status": "SOURCE_REPLAY_ONLY",
                "failure_risk": "UNKNOWN_UNTIL_LIVE_AUDIT",
                "reason": "No live connector audit executed by this control-plane scaffold.",
            }
            reports[source_id] = report
            self.record(write_json(self.p01 / f"source_health/{source_id}_source_health_report.json", report))
        self.record(write_json(self.p01 / "source_health/source_reliability_scorecard.json", reports))
        self.record(write_json(self.p01 / "source_health/source_sla_report.json", {"status":"SLA_BASELINE_PENDING_LIVE_AUDIT","sources":reports}))
        return {"mode":"source-health","status":"SOURCE_HEALTH_REPLAY_ONLY", "sources": reports}

    def build_fetch_plan(self, limit: int = 50) -> Dict[str, Any]:
        plan = {
            "schema_version": SCHEMA_VERSION,
            "generated_at": utc_now(),
            "acquisition_priority_queue": [{"token_address": self.token, "acquisition_priority":"P4_REPLAY_ONLY", "reason":"system archive scaffold; live fetch disabled", "required_fetches":["gmgn.token_profile","okx.quote","okx.security"]}],
            "limit": limit,
            "live_fetch_allowed": False,
        }
        self.record(write_json(self.p01 / "acquisition_planner/acquisition_priority_queue.json", plan["acquisition_priority_queue"]))
        self.record(write_json(self.p01 / "acquisition_planner/token_fetch_plan.json", plan))
        self.record(write_json(self.p01 / "acquisition_planner/source_fetch_schedule.json", {"schedule_status":"REPLAY_ONLY_NO_LIVE_FETCH","items":plan["acquisition_priority_queue"]}))
        self.record(write_json(self.p01 / "acquisition_planner/fetch_dependency_graph.json", {"dependencies":["source_registry","source_health","schema_contracts"]}))
        return {"mode":"build-fetch-plan","status":"FETCH_PLAN_REPLAY_ONLY", "limit": limit}

    def fetch_candidates(self, limit: int = 20) -> Dict[str, Any]:
        self.build_fetch_plan(limit=limit)
        event = {"source_id":"system_scaffold","endpoint_or_skill":"none","request_params":{"token":self.token},"request_hash": hashlib.sha256(self.token.encode()).hexdigest(),"fetched_at":utc_now(),"response_status":"NOT_FETCHED_REPLAY_ONLY","record_count":0,"payload_hash":None,"error_type":"LIVE_FETCH_DISABLED"}
        self.record(write_json(self.p01 / "raw/raw_snapshot_manifest.json", {"schema_version":SCHEMA_VERSION,"events":[event],"raw_direct_access_allowed":False}))
        self.record(write_text(self.p01 / "raw/raw_event_log.jsonl", json.dumps(event, ensure_ascii=False)+"\n"))
        return {"mode":"fetch-candidates","status":"RAW_MANIFEST_READY_NO_LIVE_FETCH"}

    def schema_monitor(self) -> Dict[str, Any]:
        stable = {"schema_status":"SCHEMA_BASELINE_PENDING","detected_changes":[],"contract_impact":"BASELINE_ONLY","downstream_risk":"MEDIUM_UNTIL_LIVE_AUDIT"}
        self.record(write_json(self.p01 / "schema_monitor/schema_diff_report.json", stable))
        self.record(write_json(self.p01 / "schema_monitor/schema_validation_report.json", stable))
        self.record(write_text(self.p01 / "schema_monitor/schema_drift_events.jsonl", ""))
        self.record(write_json(self.p01 / "schema_monitor/contract_impact_report.json", {"decision":"SCHEMA_REVIEW_REQUIRED_BEFORE_LIVE_P01_READY"}))
        return {"mode":"schema-monitor","status":"SCHEMA_BASELINE_PENDING"}

    def normalize_and_lineage(self) -> Dict[str, Any]:
        self.schema_monitor()
        field = lambda value, status, missing=None: {"value": value, "source":"system_scaffold", "fetched_at": utc_now(), "confidence":0.2 if missing else 0.6, "freshness_status":"REPLAY_ONLY", "field_status":status, "missing_reason": missing}
        facts = {
            "normalized_token_fact.json": {"token_address": field(self.token,"FIELD_PRESENT"), "chain": field(self.chain,"FIELD_PRESENT")},
            "normalized_market_fact.json": {"market_cap_usd": field(None,"FIELD_MISSING_OPTIONAL","LIVE_SOURCE_NOT_AUDITED")},
            "normalized_wallet_fact.json": {"funding_relation_edges": field(None,"FIELD_MISSING_OPTIONAL","SOURCE_CAPABILITY_UNCONFIRMED")},
            "normalized_quote_fact.json": {"quote_price": field(None,"FIELD_MISSING_REQUIRED","LIVE_FETCH_DISABLED")},
        }
        for fname, data in facts.items():
            self.record(write_json(self.p01 / f"normalized/{self.token}/{fname}", {"schema_version":SCHEMA_VERSION, "token_address":self.token, "fields":data}))
        lineage = {"token_address":self.token,"lineage":[{"field":"token_address","steps":[{"step":"input","source":"controller argument"},{"step":"normalized","target":"normalized_token_fact.token_address"}],"confidence":0.6},{"field":"quote_price","steps":[{"step":"missing","source":"okx.quote not fetched"}],"confidence":0.0}]}
        self.record(write_json(self.p01 / f"lineage/{self.token}/field_lineage_graph.json", lineage))
        self.record(write_json(self.p01 / f"lineage/{self.token}/field_provenance_report.json", lineage))
        self.record(write_json(self.p01 / f"lineage/{self.token}/derived_field_formula_manifest.json", {"derived_fields":[],"status":"NO_DERIVED_FIELDS_IN_SCAFFOLD"}))
        return {"mode":"normalize-and-lineage","status":"NORMALIZED_SCAFFOLD_READY_WITH_MISSING_FIELDS"}

    def freshness(self) -> Dict[str, Any]:
        report = {"token_address":self.token,"freshness_status":"REPLAY_ONLY","fields":{"quote_price":{"age_sec":None,"max_allowed_age_sec":60,"status":"MISSING"},"wallet_profile":{"age_sec":None,"max_allowed_age_sec":86400,"status":"MISSING"}}}
        self.record(write_json(self.p01 / f"temporal/{self.token}/snapshot_index.json", {"snapshots":[],"status":"NO_LIVE_SNAPSHOTS"}))
        self.record(write_json(self.p01 / f"temporal/{self.token}/field_freshness_report.json", report))
        self.record(write_json(self.p01 / f"temporal/{self.token}/multi_snapshot_delta_report.json", {"status":"INSUFFICIENT_SNAPSHOTS"}))
        self.record(write_text(self.p01 / f"temporal/{self.token}/stale_field_events.jsonl", json.dumps({"field":"quote_price","event":"FIELD_MISSING_REQUIRED"}, ensure_ascii=False)+"\n"))
        return {"mode":"freshness","status":"FRESHNESS_REPLAY_ONLY"}

    def reconciliation(self) -> Dict[str, Any]:
        rec = {"token_address":self.token,"status":"RECONCILIATION_NOT_AVAILABLE","decision":"MARKET_FACT_PAUSE","reason":"GMGN/OKX live values unavailable in scaffold"}
        for name in ["price_reconciliation_report.json","liquidity_reconciliation_report.json","security_reconciliation_report.json"]:
            self.record(write_json(self.p01 / f"reconciliation/{self.token}/{name}", rec))
        self.record(write_text(self.p01 / f"reconciliation/{self.token}/source_conflict_events.jsonl", ""))
        return {"mode":"reconciliation","status":"RECONCILIATION_PENDING_LIVE_DATA"}

    def quality_brain(self) -> Dict[str, Any]:
        self.normalize_and_lineage(); self.freshness(); self.reconciliation()
        completeness = {"token_address":self.token,"completeness_probability":{"for_p02_wallet_structure":0.25,"for_p03_market_structure":0.2,"for_p06_paper_trading":0.0},"missing_critical_fields":["quote_price"],"decision":{"P02":"ALLOW_LIMITED","P03":"PAUSE","P06":"PAUSE"}}
        root = {"missing_fields":[{"missing_field":"quote_price","root_cause":"LIVE_FETCH_DISABLED","impact":"market facts paused","resolution_plan":"run OKX quote capability audit and replay fixture","priority":"HIGH"},{"missing_field":"funding_relation_edges","root_cause":"SOURCE_CAPABILITY_UNCONFIRMED","impact":"same-source confidence capped","resolution_plan":"audit GMGN/OKX or behavior similarity fallback","priority":"HIGH"}]}
        decision = {"data_fact_status":"DATA_REPLAY_ONLY","decision_reason":"Control-plane scaffold exists, but live GMGN/OKX evidence and replay fixtures are not yet audited.","downstream_permissions":{"P02_wallet_chip_structure_controller":"ALLOW_LIMITED","P03_market_structure_controller":"PAUSE","P04_scenario_recognition_controller":"PAUSE","P05_strategy_gate_controller":"PAUSE","P06_paper_trading_controller":"PAUSE","P07_real_execution_controller":False}}
        self.record(write_json(self.p01 / f"quality/{self.token}/data_completeness_probability_report.json", completeness))
        self.record(write_json(self.p01 / f"quality/{self.token}/missing_data_root_cause_report.json", root))
        self.record(write_json(self.p01 / f"quality/{self.token}/data_confidence_report.json", {"confidence_score":0.2,"source_conflict_level":"UNKNOWN"}))
        self.record(write_json(self.p01 / f"quality/{self.token}/p01_data_quality_brain_trace.json", {"inputs":["source_health","lineage","freshness","reconciliation"],"decision":decision}))
        self.record(write_json(self.p01 / f"quality/{self.token}/data_quality_decision.json", decision))
        return {"mode":"quality-brain","status":"DATA_QUALITY_DECISION_REPLAY_ONLY", "decision": decision}

    def build_handoff(self) -> Dict[str, Any]:
        self.source_health(); self.quality_brain()
        packet = {
            "schema_version": SCHEMA_VERSION,
            "phase_id":"P01",
            "doc_id": DOC_ID,
            "run_id": datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S"),
            "token_address": self.token,
            "chain": self.chain,
            "data_fact_status":"DATA_REPLAY_ONLY",
            "source_health": {
                "gmgn": json.loads((self.p01/"source_health/gmgn_source_health_report.json").read_text(encoding="utf-8")),
                "okx": json.loads((self.p01/"source_health/okx_source_health_report.json").read_text(encoding="utf-8")),
            },
            "normalized_files": {"token_fact": str(self.p01/f"normalized/{self.token}/normalized_token_fact.json"),"market_fact": str(self.p01/f"normalized/{self.token}/normalized_market_fact.json"),"wallet_fact": str(self.p01/f"normalized/{self.token}/normalized_wallet_fact.json"),"quote_fact": str(self.p01/f"normalized/{self.token}/normalized_quote_fact.json")},
            "lineage_files": {"field_lineage_graph": str(self.p01/f"lineage/{self.token}/field_lineage_graph.json"),"field_provenance_report": str(self.p01/f"lineage/{self.token}/field_provenance_report.json")},
            "temporal_files": {"field_freshness_report": str(self.p01/f"temporal/{self.token}/field_freshness_report.json"),"multi_snapshot_delta_report": str(self.p01/f"temporal/{self.token}/multi_snapshot_delta_report.json")},
            "quality_brain": {"completeness_probability":{"for_p02_wallet_structure":0.25,"for_p03_market_structure":0.2,"for_p06_paper_trading":0.0},"confidence_score":0.2,"source_conflict_level":"UNKNOWN","missing_critical_fields":["quote_price"],"missing_limited_fields":["funding_relation_edges"],"decision_reason":"Scaffold only; live source audit and replay fixtures required."},
            "downstream_permissions": {"P02_wallet_chip_structure_controller":"ALLOW_LIMITED","P03_market_structure_controller":"PAUSE","P04_scenario_recognition_controller":"PAUSE","P05_strategy_gate_controller":"PAUSE","P06_paper_trading_controller":"PAUSE","P07_real_execution_controller":False},
            "handoff_constraints": {"raw_direct_access_allowed":False,"real_execution_allowed":False,"paper_runtime_allowed":False,"live_execution_allowed":False,"replay_only":True,"requires_backfill":True,"requires_human_review":False},
            "backfill_plan": {"required":True,"missing_fields":["quote_price","funding_relation_edges"],"priority":"HIGH","impact":"P01 not ready for runtime/paper/live decisions"},
        }
        self.record(write_json(self.p01 / f"handoff/{self.token}/data_fact_handoff_packet.json", packet))
        self.record(write_json(self.p01 / f"handoff/{self.token}/downstream_permission_matrix.json", packet["downstream_permissions"]))
        md = "# P01 Downstream Readiness\n\n- status: DATA_REPLAY_ONLY\n- P02: ALLOW_LIMITED for ingestion/design only\n- P03/P04/P05/P06: PAUSE\n- P07 real execution: false\n"
        self.record(write_text(self.p01 / f"handoff/{self.token}/downstream_readiness_report.md", md))
        return {"mode":"build-handoff","status":"HANDOFF_READY_REPLAY_ONLY", "handoff": str(self.p01 / f"handoff/{self.token}/data_fact_handoff_packet.json")}

    def replay_backfill(self) -> Dict[str, Any]:
        fixture = {"fixture_status":"FIXTURE_MANIFEST_READY_EMPTY","required_samples":5,"current_samples":0,"reason":"Need 3-5 real token samples before model calibration."}
        self.record(write_json(self.p01 / "replay_fixture/fixture_manifest.json", fixture))
        self.record(write_json(self.p01 / "replay_fixture/replay_validation_report.json", {"status":"REPLAY_NOT_RUN_NO_FIXTURES"}))
        gaps = {"required":True,"items":[{"field":"quote_price","source":"okx","priority":"HIGH"},{"field":"funding_relation_edges","source":"gmgn_or_behavior_model","priority":"HIGH"}]}
        self.record(write_json(self.p01 / "backfill/backfill_plan.json", gaps))
        self.record(write_json(self.p01 / "backfill/backfill_status_report.json", {"status":"BACKFILL_REQUIRED_NOT_STARTED"}))
        self.record(write_json(self.p01 / "backfill/unresolved_data_gap_queue.json", gaps))
        return {"mode":"replay-backfill","status":"REPLAY_BACKFILL_QUEUE_READY"}

    def audit(self) -> Dict[str, Any]:
        self.build_handoff(); self.replay_backfill()
        role_reports = {
            "source_engineer_report.json":{"status":"REPLAY_ONLY","finding":"GMGN/OKX live connectors require audit."},
            "data_quality_officer_report.json":{"status":"DATA_REPLAY_ONLY","finding":"Critical live quote missing."},
            "schema_contract_auditor_report.json":{"status":"SCHEMA_BASELINE_PENDING","finding":"No live schema sample yet."},
            "field_lineage_officer_report.json":{"status":"LINEAGE_SCAFFOLD_READY","finding":"Known fields have scaffold lineage; live fields pending."},
            "temporal_consistency_officer_report.json":{"status":"NO_LIVE_SNAPSHOTS","finding":"Freshness cannot pass without snapshots."},
            "source_reconciliation_officer_report.json":{"status":"RECONCILIATION_PENDING","finding":"No GMGN/OKX paired values."},
            "downstream_permission_officer_report.json":{"status":"PERMISSION_CONTROLLED","finding":"P02 limited; P03-P06 paused; real false."},
        }
        for name, report in role_reports.items():
            self.record(write_json(self.p01 / f"multi_role_audit/{name}", report))
        runtime = {"doc_id":DOC_ID,"audit_at":utc_now(),"status":"P01_DSIC_MIN_AUTOMATION_SCAFFOLD_READY_WITH_GAPS","permissions":PERMISSIONS,"created_files":self.created}
        self.record(write_text(self.p01 / "audit/p01_runtime_log.jsonl", json.dumps(runtime, ensure_ascii=False)+"\n"))
        self.record(write_text(self.p01 / "audit/p01_error_events.jsonl", ""))
        self.record(write_text(self.p01 / "audit/p01_data_quality_events.jsonl", json.dumps({"event":"DATA_REPLAY_ONLY","reason":"live source audit pending"}, ensure_ascii=False)+"\n"))
        daily = "# P01 日报\n\n- 状态: P01_DSIC_MIN_AUTOMATION_SCAFFOLD_READY_WITH_GAPS\n- K00: K00_ACCEPTED\n- real_execution_allowed: false\n- paper_runtime_allowed: false\n- live_execution_allowed: false\n- raw_direct_access_allowed: false\n- 下一步: GMGN/OKX live capability audit + replay fixtures\n"
        self.record(write_text(self.p01 / "audit/p01_daily_report.md", daily))
        self.record(write_text(self.p01 / "audit/p01_gap_audit_report.md", "# P01 Gap Audit\n\n- GMGN live fields pending\n- OKX quote/liquidity/route/security pending\n- replay fixtures 3-5 tokens pending\n- downstream reader migration pending\n"))
        completion = "# P01 Completion Report\n\n当前仅完成系统档案 + 最小自动化控制骨架。不得声明 P01_READY / DATA_READY / PAPER_READY / LIVE_READY。\n"
        self.record(write_text(self.p01 / "audit/p01_completion_report.md", completion))
        manifest = {"schema_version":SCHEMA_VERSION,"status":"PASS_WITH_GAPS","created_files":self.created,"blocked_claims":["P01_READY","DATA_READY","PAPER_READY","LIVE_READY","REAL_EXECUTION_READY"]}
        self.record(write_json(self.p01 / "manifest/p01_dsic_manifest.json", manifest))
        return {"mode":"audit","status":"P01_DSIC_MIN_AUTOMATION_SCAFFOLD_READY_WITH_GAPS", "manifest": str(self.p01 / "manifest/p01_dsic_manifest.json")}

    def run(self, mode: str, limit: int) -> Dict[str, Any]:
        modes = {
            "init-phase": self.init_phase,
            "source-registry": self.source_registry,
            "source-health": self.source_health,
            "build-fetch-plan": lambda: self.build_fetch_plan(limit=limit),
            "fetch-candidates": lambda: self.fetch_candidates(limit=limit),
            "schema-monitor": self.schema_monitor,
            "normalize-and-lineage": self.normalize_and_lineage,
            "freshness": self.freshness,
            "reconciliation": self.reconciliation,
            "quality-brain": self.quality_brain,
            "build-handoff": self.build_handoff,
            "replay-backfill": self.replay_backfill,
            "audit": self.audit,
            "all": self.audit,
        }
        if mode not in modes:
            raise SystemExit(f"unknown mode: {mode}")
        result = modes[mode]()
        result.update({"run_dir": str(self.run_dir), "p01_dir": str(self.p01), "doc_id": DOC_ID, "permissions": PERMISSIONS})
        return result


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default="/root/sikk-gmgn")
    parser.add_argument("--run-dir", default="data/gmgn_candidates_live_run")
    parser.add_argument("--mode", default="all")
    parser.add_argument("--token", default=TOKEN_PLACEHOLDER)
    parser.add_argument("--chain", default="solana")
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args(argv)
    c = P01DataSourceIntelligenceController(Path(args.run_dir), Path(args.repo_root), token=args.token, chain=args.chain)
    result = c.run(args.mode, args.limit)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
