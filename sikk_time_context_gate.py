#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK 全系统时间上下文协同门禁模块。

只读读取现有 runtime 输出，统一抽取各阶段时间字段，计算 age/ttl/stale/
time_skew/refresh_required/temporal_sync_status/temporal_gate/time_context_score，
并写出 time_context_summary.json/csv/md/runtime_log.json。
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

DEFAULT_BASE_DIR = Path("data/gmgn_candidates_live_run")
DEFAULT_OUTPUT_SUBDIR = "time_context"
SCHEMA_PATH = DEFAULT_BASE_DIR / "time_context" / "time_context_schema.json"

STAGE_ORDER = [
    "S0_SYSTEM_BASELINE",
    "S1_CANDIDATE_DISCOVERY",
    "S2_KLINE_COLLECTION",
    "S3_PATTERN_RECOGNITION",
    "S4_WALLET_STRUCTURE",
    "S5_WALLET_PATTERN_ALIGNMENT",
    "S6_DOMINANT_LIFECYCLE",
    "S7_DOMINANT_INTENT",
    "S8_QUOTE_SECURITY_LIQUIDITY",
    "S9_FINAL_TRADE_GATE",
    "S10_PAPER_RUNNER",
    "S11_FAILURE_ATTRIBUTION",
    "S12_DAILY_REVIEW",
]

FALLBACK_STAGE_TTL = {
    "S0_SYSTEM_BASELINE": 3600,
    "S1_CANDIDATE_DISCOVERY": 86400,
    "S2_KLINE_COLLECTION": 300,
    "S3_PATTERN_RECOGNITION": 900,
    "S4_WALLET_STRUCTURE": 900,
    "S5_WALLET_PATTERN_ALIGNMENT": 900,
    "S6_DOMINANT_LIFECYCLE": 1800,
    "S7_DOMINANT_INTENT": 1800,
    "S8_QUOTE_SECURITY_LIQUIDITY": 120,
    "S9_FINAL_TRADE_GATE": 180,
    "S10_PAPER_RUNNER": 86400,
    "S11_FAILURE_ATTRIBUTION": 604800,
    "S12_DAILY_REVIEW": 129600,
}

FIELD_ALIASES = {
    "token_address": ["token_address", "代币地址", "address", "mint", "token", "tokenMint", "token_mint"],
    "token_symbol": ["token_symbol", "代币符号", "symbol"],
    "token_open_time": ["token_open_time", "开盘时间戳", "open_time", "pool_open_time", "launch_time", "created_at"],
    "pool_created_at": ["pool_created_at", "创建时间戳", "liquidity_created_at", "pair_created_at", "lp_created_at"],
    "discovered_at": ["discovered_at", "candidate_discovered_at", "发现时间", "first_seen_at", "扫描时间"],
    "candidate_discovered_at": ["candidate_discovered_at", "discovered_at", "first_seen_at", "first_seen_by_system_at"],
    "first_seen_at": ["first_seen_at", "first_seen_by_system_at", "discovered_at", "candidate_discovered_at"],
    "last_seen_at": ["last_seen_at", "last_update", "updated_at", "source_last_update", "last_update_time"],
    "candidate_snapshot_at": ["candidate_snapshot_at", "snapshot_time", "last_update", "generated_at", "扫描时间"],
    "signal_time": ["signal_time", "first_signal_at", "信号时间"],
    "signal_level": ["signal_level", "信号等级", "筛选等级", "signal_level_code"],
    "signal_stale": ["signal_stale", "signal_is_stale", "signal_expired"],
    "quote_stale": ["quote_stale", "quote_is_stale", "quote_expired"],
    "wallet_decision_time": ["wallet_decision_time", "wallet_decision_at", "decision_time"],
    "wallet_decision_created_at": ["wallet_decision_created_at", "wallet_decision_time", "wallet_decision_at", "decision_time"],
    "pattern_created_at": ["pattern_created_at", "pattern_time", "pattern_classified_at", "pattern.detected_at"],
    "lifecycle_created_at": ["lifecycle_created_at", "lifecycle_classified_at", "dominant_lifecycle_created_at"],
    "intent_created_at": ["intent_created_at", "intent_time", "dominant_intent_created_at"],
    "quote_time": ["quote_time", "quote_checked_at", "quote_received_at", "quote_requested_at"],
    "quote_requested_at": ["quote_requested_at", "quote_requested_time"],
    "quote_received_at": ["quote_received_at", "quote_time", "quote_checked_at"],
    "security_scan_time": ["security_scan_time", "security_checked_at", "security_time"],
    "final_gate_created_at": ["final_gate_created_at", "final_gate_time", "final_gate_checked_at"],
    "paper_entry_time": ["paper_entry_time", "paper_entry_at", "entry_time"],
    "paper_signal_time": ["paper_signal_time", "signal_time", "first_signal_at"],
    "entry_time": ["entry_time", "paper_entry_time", "paper_entry_at", "position_opened_at"],
    "exit_time": ["exit_time", "paper_exit_time", "paper_exit_at", "position_closed_at"],
    "last_update_time": ["last_update_time", "last_update", "updated_at", "source_last_update", "generated_at"],
    "failure_detected_at": ["failure_detected_at", "failed_at", "failure_time", "exit_triggered_at"],
    "report_generated_at": ["report_generated_at", "generated_at", "report_time", "summary_generated_at", "报告日期"],
}

PREFERRED_OUTPUT_FIELDS = [
    "token_address", "token_symbol", "generated_at", "pipeline_round_id",
    "token_open_time", "pool_created_at", "discovered_at", "first_seen_at", "last_seen_at", "candidate_snapshot_at",
    "token_age_sec", "discovery_delay_sec", "candidate_age_sec", "candidate_stage", "discovery_quality", "requires_pattern_review",
    "signal_time", "signal_level", "signal_stale",
    "kline_source_time", "latest_kline_time", "latest_kline_age_sec", "kline_ttl_sec", "kline_stale",
    "pattern_created_at", "pattern_age_sec", "pattern_ttl_sec", "pattern_stale",
    "wallet_decision_created_at", "wallet_snapshot_at", "wallet_decision_age_sec", "wallet_decision_ttl_sec", "wallet_decision_stale",
    "alignment_created_at", "alignment_age_sec", "alignment_ttl_sec", "alignment_stale", "alignment_time_skew_sec",
    "lifecycle_created_at", "lifecycle_age_sec", "lifecycle_ttl_sec", "lifecycle_stale",
    "intent_created_at", "intent_age_sec", "intent_ttl_sec", "intent_stale",
    "quote_time", "quote_age_sec", "quote_ttl_sec", "quote_stale",
    "security_scan_time", "security_scan_age_sec", "security_scan_ttl_sec", "security_scan_stale",
    "final_gate_created_at", "final_gate_age_sec", "final_gate_ttl_sec", "final_gate_stale",
    "paper_entry_time", "paper_signal_time", "paper_last_update_time", "position_opened_at", "position_age_sec",
    "failure_detected_at", "entry_time", "exit_time", "holding_duration_sec", "time_to_failure_sec",
    "report_window_start", "report_window_end", "report_generated_at",
    "time_skew_sec", "temporal_sync_status", "temporal_gate", "time_context_score", "time_context_grade",
    "missing_fields", "missing_sources", "refresh_required", "stale_sources", "temporal_reason",
    "stage_missing_fields_json", "stage_stale_flags_json",
]

REQUIRED_SOURCE_ATTEMPTS = [
    ("candidates.json", DEFAULT_BASE_DIR / "candidates.json"),
    ("state_machine/candidate_states.json", DEFAULT_BASE_DIR / "state_machine" / "candidate_states.json"),
    ("candidate_signal_outputs/candidate_signal_summary.json", DEFAULT_BASE_DIR / "candidate_signal_outputs" / "candidate_signal_summary.json"),
    ("patterns/market_pattern_summary.json", DEFAULT_BASE_DIR / "patterns" / "market_pattern_summary.json"),
    ("lifecycle/dominant_lifecycle_summary.json", DEFAULT_BASE_DIR / "lifecycle" / "dominant_lifecycle_summary.json"),
    ("intent/intent_inference_summary.json", DEFAULT_BASE_DIR / "intent" / "intent_inference_summary.json"),
]

SOURCE_PRIORITY = {
    "candidates.json": 100,
    "gmgn_new_token_filter/token_candidates.json": 100,
    "state_machine/candidate_states.json": 90,
    "candidate_signal_outputs/candidate_signal_summary.json": 80,
    "wallet_structure": 70,
    "patterns/market_pattern_summary.json": 60,
    "lifecycle/dominant_lifecycle_summary.json": 55,
    "intent/intent_inference_summary.json": 55,
    "quote_security": 50,
    "paper_live": 40,
    "failure_attribution": 30,
    "daily_report": 20,
    "dashboard_data.json": 10,
}


def utc_now_text() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def format_utc(value):
    dt = parse_time(value)
    if dt is None:
        return None
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_time(value):
    if value in (None, "", [], {}):
        return None
    if isinstance(value, (int, float)):
        ts = float(value)
        if ts > 10_000_000_000:
            ts /= 1000.0
        try:
            return datetime.fromtimestamp(ts, tz=timezone.utc)
        except Exception:
            return None
    text = str(value).strip()
    if not text:
        return None
    if re.fullmatch(r"-?\d+(?:\.\d+)?", text):
        try:
            ts = float(text)
            if ts > 10_000_000_000:
                ts /= 1000.0
            return datetime.fromtimestamp(ts, tz=timezone.utc)
        except Exception:
            return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(text)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None


def seconds_between(start, end):
    s = parse_time(start)
    e = parse_time(end)
    if not s or not e:
        return None
    return round((e - s).total_seconds(), 3)


def as_bool(value):
    if value in (None, ""):
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    text = str(value).strip().lower()
    if text in {"true", "1", "yes", "y", "fresh", "正常", "stale", "过期"}:
        return text not in {"false", "0", "no", "n", "fresh", "正常"}
    if text in {"false", "0", "no", "n", "fresh", "正常"}:
        return False
    return None


def first_nonempty(values):
    for v in values:
        if v not in (None, "", [], {}):
            return v
    return None


def load_json_or_none(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def load_jsonl_or_json(path):
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8", errors="ignore").strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except Exception:
        rows = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception:
                continue
        if rows:
            return rows
    return None


def flatten_keys(obj, out=None):
    if out is None:
        out = defaultdict(list)
    if isinstance(obj, dict):
        for k, v in obj.items():
            if v not in (None, "", [], {}):
                out[str(k)].append(v)
                flatten_keys(v, out)
    elif isinstance(obj, list):
        for item in obj:
            flatten_keys(item, out)
    return out


def pick_alias(obj, canonical, aliases=None):
    aliases = aliases or FIELD_ALIASES.get(canonical, [canonical])
    flat = flatten_keys(obj)
    for alias in aliases:
        if alias in flat:
            val = first_nonempty(flat[alias])
            if val not in (None, "", [], {}):
                return val
    return None


def normalize_record(raw, source_name=None, fallback_token=None, fallback_symbol=None):
    if raw is None:
        return {}
    record = raw if isinstance(raw, dict) else {}
    out = {}
    for canonical in FIELD_ALIASES:
        val = pick_alias(record, canonical)
        if val not in (None, "", [], {}):
            out[canonical] = val
    # common raw top-level names not covered by aliases
    if fallback_token and not out.get("token_address"):
        out["token_address"] = fallback_token
    if fallback_symbol and not out.get("token_symbol"):
        out["token_symbol"] = fallback_symbol
    if source_name:
        out["_source_name"] = source_name
    return out


def extract_rows_from_payload(payload, source_name, path_hint=None, fallback_token=None, fallback_symbol=None):
    rows = []
    if payload is None:
        return rows
    if isinstance(payload, list):
        for item in payload:
            rows.append(normalize_record(item, source_name, fallback_token, fallback_symbol))
        return rows
    if isinstance(payload, dict):
        for key in ["候选列表", "排除列表", "候选状态", "信号结果", "tokens", "items", "rows", "data", "positions", "open", "closed", "events"]:
            if isinstance(payload.get(key), list):
                for item in payload[key]:
                    rows.append(normalize_record(item, source_name, fallback_token, fallback_symbol))
                if rows:
                    return rows
        rows.append(normalize_record(payload, source_name, fallback_token, fallback_symbol))
        for key in ["候选列表", "排除列表"]:
            if isinstance(payload.get(key), list):
                for item in payload[key]:
                    rows.append(normalize_record(item, source_name, fallback_token, fallback_symbol))
        return rows
    return rows


def load_schema(base_dir):
    schema_path = base_dir / "time_context" / "time_context_schema.json"
    schema = load_json_or_none(schema_path) or {}
    common_fields = schema.get("common_required_time_fields") or [
        "source_time", "created_at", "input_window_start", "input_window_end", "age_sec", "ttl_sec",
        "stale", "elapsed_sec", "time_skew_sec", "refresh_required", "stale_action",
    ]
    stage_meta = {s.get("id"): s for s in schema.get("stages", []) if isinstance(s, dict)}
    canonical_map = schema.get("canonical_field_map") or {}
    enums = schema.get("enums") or {}
    hard_rules = (schema.get("temporal_gate_rules") or {}).get("hard_rules", [])
    ttl_defaults = {sid: stage_meta.get(sid, {}).get("ttl", FALLBACK_STAGE_TTL[sid]) for sid in STAGE_ORDER}
    return {
        "schema": schema,
        "common_fields": common_fields,
        "stage_meta": stage_meta,
        "canonical_map": canonical_map,
        "enums": enums,
        "hard_rules": hard_rules,
        "ttl_defaults": ttl_defaults,
    }


def collect_source_inventory(base_dir):
    inventory = []
    missing = []
    for label, path in REQUIRED_SOURCE_ATTEMPTS:
        inventory.append({"label": label, "path": str(path), "exists": path.exists()})
        if not path.exists():
            missing.append(str(path))
    # required candidate seed source and fallbacks
    extra_attempts = [
        ("gmgn_new_token_filter/token_candidates.json", base_dir / "gmgn_new_token_filter" / "token_candidates.json"),
        ("live_state.json", base_dir / "live_state.json"),
        ("site/dashboard_data.json", base_dir / "site" / "dashboard_data.json"),
        ("paper_live/failure_attribution.jsonl", base_dir / "paper_live" / "failure_attribution.jsonl"),
        ("reports/wallet_structure_daily_report_20260504.json", base_dir / "reports" / "wallet_structure_daily_report_20260504.json"),
    ]
    for label, path in extra_attempts:
        inventory.append({"label": label, "path": str(path), "exists": path.exists()})
        if not path.exists():
            missing.append(str(path))
    return inventory, missing


def gather_candidate_rows(base_dir, inventory):
    rows = []
    source_rows = defaultdict(list)
    missing_sources = []

    def add_payload(label, path, payload, fallback_token=None, fallback_symbol=None):
        if payload is None:
            missing_sources.append(str(path))
            return
        extracted = extract_rows_from_payload(payload, label, str(path), fallback_token, fallback_symbol)
        if not extracted:
            missing_sources.append(str(path))
            return
        for row in extracted:
            row["_source_label"] = label
            row["_source_path"] = str(path)
            source_rows[label].append(row)
            rows.append(row)

    # explicit files that define candidate universe
    for label, path in [
        ("candidates.json", base_dir / "candidates.json"),
        ("gmgn_new_token_filter/token_candidates.json", base_dir / "gmgn_new_token_filter" / "token_candidates.json"),
        ("state_machine/candidate_states.json", base_dir / "state_machine" / "candidate_states.json"),
        ("candidate_signal_outputs/candidate_signal_summary.json", base_dir / "candidate_signal_outputs" / "candidate_signal_summary.json"),
        ("site/dashboard_data.json", base_dir / "site" / "dashboard_data.json"),
        ("live_state.json", base_dir / "live_state.json"),
    ]:
        payload = load_json_or_none(path)
        add_payload(label, path, payload)

    # wallet structure decisions
    ws_dir = base_dir / "wallet_structure"
    if ws_dir.exists():
        for file in ws_dir.rglob("wallet_structure_decision.json"):
            payload = load_json_or_none(file)
            fallback_token = file.parent.name
            add_payload("wallet_structure", file, payload, fallback_token=fallback_token)
    else:
        missing_sources.append(str(ws_dir / "*/wallet_structure_decision.json"))

    # other stage folders
    for label, path in [
        ("patterns/market_pattern_summary.json", base_dir / "patterns" / "market_pattern_summary.json"),
        ("lifecycle/dominant_lifecycle_summary.json", base_dir / "lifecycle" / "dominant_lifecycle_summary.json"),
        ("intent/intent_inference_summary.json", base_dir / "intent" / "intent_inference_summary.json"),
    ]:
        payload = load_json_or_none(path)
        add_payload(label, path, payload)

    # quote/security family
    qs_dir = base_dir / "quote_security"
    if qs_dir.exists():
        for file in qs_dir.rglob("*"):
            if file.is_file() and file.suffix.lower() in {".json", ".jsonl"}:
                payload = load_jsonl_or_json(file)
                add_payload("quote_security", file, payload)
    else:
        missing_sources.append(str(qs_dir / "*"))

    # paper_live family
    paper_dir = base_dir / "paper_live"
    if paper_dir.exists():
        for file in paper_dir.rglob("*"):
            if file.is_file() and file.suffix.lower() in {".json", ".jsonl"}:
                payload = load_jsonl_or_json(file)
                add_payload("paper_live", file, payload)
            elif file.is_file() and file.suffix.lower() in {".md", ".txt"}:
                text = file.read_text(encoding="utf-8", errors="ignore")
                ts = re.findall(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", text)
                if ts:
                    add_payload("paper_live_text", file, {"report_generated_at": ts[0], "generated_at": ts[0], "raw_text": text[:2000]})
    else:
        missing_sources.append(str(paper_dir / "*"))

    # failure_attribution files
    for file in sorted(base_dir.rglob("*failure_attribution*")):
        if file.is_file() and file.suffix.lower() in {".json", ".jsonl"}:
            payload = load_jsonl_or_json(file)
            add_payload("failure_attribution", file, payload)

    # daily_report files
    for file in sorted(base_dir.rglob("*daily_report*")):
        if file.is_file():
            if file.suffix.lower() in {".json", ".jsonl"}:
                payload = load_jsonl_or_json(file)
                add_payload("daily_report", file, payload)
            else:
                text = file.read_text(encoding="utf-8", errors="ignore")
                ts = re.findall(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", text)
                if ts:
                    add_payload("daily_report_text", file, {"report_generated_at": ts[0], "generated_at": ts[0], "raw_text": text[:2000]})

    # if no rows, still return empty
    return rows, source_rows, missing_sources


def merge_records(rows):
    merged = {}
    for row in rows:
        token = row.get("token_address") or row.get("代币地址") or row.get("address")
        if not token:
            continue
        token = str(token)
        dest = merged.setdefault(token, {})
        priority = SOURCE_PRIORITY.get(row.get("_source_label", ""), 0)
        existing_priority = dest.get("_priority", -1)
        if priority >= existing_priority:
            dest["_priority"] = priority
        for key, value in row.items():
            if key.startswith("_"):
                continue
            if value in (None, "", [], {}):
                continue
            if key not in dest or dest.get(key) in (None, "", [], {}):
                dest[key] = value
    for token, record in merged.items():
        record.pop("_priority", None)
    return merged


def stage_required_fields(schema):
    fields = set(schema.get("common_fields", []))
    for stage in schema.get("stage_meta", {}).values():
        fields.update(stage.get("required_input_fields", []))
    return fields


def stage_alias_map(schema):
    canonical_map = schema.get("canonical_map") or {}
    alias_map = {}
    for canonical, aliases in FIELD_ALIASES.items():
        alias_map[canonical] = list(dict.fromkeys(list(aliases) + list(canonical_map.get(canonical, []))))
    for key, aliases in canonical_map.items():
        if key not in alias_map:
            alias_map[key] = list(dict.fromkeys([key] + list(aliases)))
        else:
            alias_map[key] = list(dict.fromkeys(alias_map[key] + list(aliases)))
    return alias_map


def pick_value(row, key, alias_map):
    aliases = alias_map.get(key, [key])
    for alias in aliases:
        val = pick_alias(row, key, [alias])
        if val not in (None, "", [], {}):
            return val
    # allow searching nested sections by same key if present directly
    if isinstance(row, dict) and key in row and row.get(key) not in (None, "", [], {}):
        return row.get(key)
    return None


def stage_ttl(schema, stage_id):
    return int(schema.get("ttl_defaults", {}).get(stage_id, FALLBACK_STAGE_TTL.get(stage_id, 900)))


def compute_candidate_stage(token_age_sec, token_open_time):
    if token_open_time in (None, "", [], {}):
        return "STAGE_UNKNOWN"
    if token_age_sec is None:
        return "STAGE_UNKNOWN"
    if token_age_sec < 180:
        return "D0_SCOUT_ONLY"
    if token_age_sec <= 900:
        return "D1_EARLY_STRUCTURE_WINDOW"
    if token_age_sec <= 2700:
        return "D2_MAIN_TRADING_WINDOW"
    if token_age_sec <= 7200:
        return "D3_LATE_WINDOW"
    return "D4_OLD_TOKEN"


def compute_discovery_quality(discovery_delay_sec, discovered_at, token_open_time):
    if discovered_at in (None, "", [], {}) or token_open_time in (None, "", [], {}):
        return "DISCOVERY_UNKNOWN"
    if discovery_delay_sec is None:
        return "DISCOVERY_UNKNOWN"
    if discovery_delay_sec <= 180:
        return "EARLY_DISCOVERY"
    if discovery_delay_sec <= 900:
        return "NORMAL_DISCOVERY"
    if discovery_delay_sec <= 2700:
        return "LATE_DISCOVERY"
    return "VERY_LATE_DISCOVERY"


def compute_temporal_sync_status(time_skew_sec, critical_missing):
    if critical_missing or time_skew_sec is None:
        return "TEMPORAL_UNKNOWN"
    if time_skew_sec <= 180:
        return "TEMPORAL_SYNCED"
    if time_skew_sec <= 600:
        return "TEMPORAL_PARTIAL_SYNC"
    return "TEMPORAL_DESYNC"


def compute_gate(candidate_stage, quote_stale, signal_stale, sync_status, critical_missing):
    if quote_stale:
        return "TEMPORAL_EXPIRED"
    if signal_stale:
        return "TEMPORAL_EXPIRED"
    if critical_missing:
        return "TEMPORAL_UNKNOWN"
    if candidate_stage == "D0_SCOUT_ONLY":
        return "TEMPORAL_WATCH"
    if sync_status == "TEMPORAL_DESYNC":
        return "TEMPORAL_PAUSE"
    if sync_status in {"TEMPORAL_SYNCED", "TEMPORAL_PARTIAL_SYNC"}:
        return "TEMPORAL_ALLOW"
    return "TEMPORAL_UNKNOWN"


def score_candidate_stage(stage):
    return {"D0_SCOUT_ONLY": 8, "D1_EARLY_STRUCTURE_WINDOW": 20, "D2_MAIN_TRADING_WINDOW": 18, "D3_LATE_WINDOW": 12, "D4_OLD_TOKEN": 6}.get(stage, 0)


def score_discovery_quality(quality):
    return {"EARLY_DISCOVERY": 15, "NORMAL_DISCOVERY": 12, "LATE_DISCOVERY": 6, "VERY_LATE_DISCOVERY": 2}.get(quality, 0)


def score_sync(sync_status):
    return {"TEMPORAL_SYNCED": 15, "TEMPORAL_PARTIAL_SYNC": 8, "TEMPORAL_DESYNC": 0, "TEMPORAL_UNKNOWN": 0}.get(sync_status, 0)


def score_freshness(stale_flags):
    score = 40
    deductions = {
        "signal_stale": 10,
        "kline_stale": 8,
        "pattern_stale": 8,
        "wallet_decision_stale": 8,
        "quote_stale": 15,
        "security_scan_stale": 8,
    }
    for key, penalty in deductions.items():
        if stale_flags.get(key) is True:
            score -= penalty
    return max(0, score)


def score_completeness(missing_required_count):
    if missing_required_count <= 2:
        return 10
    if missing_required_count <= 5:
        return 5
    return 0


def describe_reason(gate, candidate_stage, sync_status, stale_flags, missing_count):
    parts = []
    if candidate_stage == "D0_SCOUT_ONLY":
        parts.append("D0_SCOUT_ONLY")
    if candidate_stage == "D4_OLD_TOKEN":
        parts.append("D4_OLD_TOKEN_requires_pattern_review")
    if stale_flags.get("quote_stale"):
        parts.append("quote_stale=true")
    if stale_flags.get("signal_stale"):
        parts.append("signal_stale=true")
    if sync_status == "TEMPORAL_DESYNC":
        parts.append("time_desync")
    if missing_count:
        parts.append(f"missing_fields={missing_count}")
    if not parts:
        parts.append("fresh_inputs")
    parts.append(f"gate={gate}")
    return "; ".join(parts)


def build_stage_context(stage_id, row, alias_map, schema, now_dt):
    stage = schema.get("stage_meta", {}).get(stage_id, {})
    ttl = stage_ttl(schema, stage_id)
    required_inputs = stage.get("required_input_fields", []) or []
    optional_inputs = stage.get("optional_input_fields", []) or []
    all_inputs = required_inputs + optional_inputs

    ctx = {}
    missing = []
    for field in all_inputs:
        val = pick_value(row, field, alias_map)
        if val in (None, "", [], {}):
            missing.append(field)
        else:
            ctx[field] = val

    # stage-specific source_time / created_at inference
    if stage_id == "S1_CANDIDATE_DISCOVERY":
        ctx["source_time"] = first_nonempty([pick_value(row, "token_open_time", alias_map), pick_value(row, "candidate_snapshot_at", alias_map), pick_value(row, "discovered_at", alias_map)])
        ctx["created_at"] = first_nonempty([pick_value(row, "candidate_snapshot_at", alias_map), pick_value(row, "discovered_at", alias_map), pick_value(row, "first_seen_at", alias_map)])
        ctx["input_window_start"] = pick_value(row, "token_open_time", alias_map)
        ctx["input_window_end"] = pick_value(row, "last_seen_at", alias_map) or pick_value(row, "candidate_snapshot_at", alias_map)
    elif stage_id == "S2_KLINE_COLLECTION":
        ctx["source_time"] = first_nonempty([pick_value(row, "latest_kline_time", alias_map), pick_value(row, "quote_time", alias_map)])
        ctx["created_at"] = pick_value(row, "latest_kline_time", alias_map) or pick_value(row, "quote_time", alias_map)
        ctx["input_window_start"] = pick_value(row, "token_open_time", alias_map)
        ctx["input_window_end"] = pick_value(row, "latest_kline_time", alias_map)
    elif stage_id == "S3_PATTERN_RECOGNITION":
        ctx["source_time"] = pick_value(row, "pattern_created_at", alias_map)
        ctx["created_at"] = pick_value(row, "pattern_created_at", alias_map)
        ctx["input_window_start"] = pick_value(row, "token_open_time", alias_map)
        ctx["input_window_end"] = pick_value(row, "latest_kline_time", alias_map)
    elif stage_id == "S4_WALLET_STRUCTURE":
        ctx["source_time"] = first_nonempty([pick_value(row, "wallet_decision_created_at", alias_map), pick_value(row, "wallet_decision_time", alias_map)])
        ctx["created_at"] = first_nonempty([pick_value(row, "wallet_decision_created_at", alias_map), pick_value(row, "wallet_decision_time", alias_map)])
        ctx["input_window_start"] = pick_value(row, "pattern_created_at", alias_map)
        ctx["input_window_end"] = pick_value(row, "wallet_decision_created_at", alias_map)
    elif stage_id == "S5_WALLET_PATTERN_ALIGNMENT":
        ctx["source_time"] = first_nonempty([pick_value(row, "alignment_created_at", alias_map), pick_value(row, "wallet_decision_created_at", alias_map), pick_value(row, "pattern_created_at", alias_map)])
        ctx["created_at"] = pick_value(row, "alignment_created_at", alias_map)
        ctx["input_window_start"] = pick_value(row, "wallet_decision_created_at", alias_map)
        ctx["input_window_end"] = pick_value(row, "pattern_created_at", alias_map)
    elif stage_id == "S6_DOMINANT_LIFECYCLE":
        ctx["source_time"] = pick_value(row, "lifecycle_created_at", alias_map)
        ctx["created_at"] = pick_value(row, "lifecycle_created_at", alias_map)
        ctx["input_window_start"] = pick_value(row, "wallet_decision_created_at", alias_map)
        ctx["input_window_end"] = pick_value(row, "lifecycle_created_at", alias_map)
    elif stage_id == "S7_DOMINANT_INTENT":
        ctx["source_time"] = pick_value(row, "intent_created_at", alias_map)
        ctx["created_at"] = pick_value(row, "intent_created_at", alias_map)
        ctx["input_window_start"] = pick_value(row, "lifecycle_created_at", alias_map)
        ctx["input_window_end"] = pick_value(row, "intent_created_at", alias_map)
    elif stage_id == "S8_QUOTE_SECURITY_LIQUIDITY":
        ctx["source_time"] = first_nonempty([pick_value(row, "quote_time", alias_map), pick_value(row, "security_scan_time", alias_map)])
        ctx["created_at"] = first_nonempty([pick_value(row, "quote_time", alias_map), pick_value(row, "security_scan_time", alias_map)])
        ctx["input_window_start"] = pick_value(row, "quote_requested_at", alias_map)
        ctx["input_window_end"] = first_nonempty([pick_value(row, "quote_received_at", alias_map), pick_value(row, "security_scan_time", alias_map)])
    elif stage_id == "S9_FINAL_TRADE_GATE":
        ctx["source_time"] = pick_value(row, "final_gate_created_at", alias_map)
        ctx["created_at"] = pick_value(row, "final_gate_created_at", alias_map)
        ctx["input_window_start"] = pick_value(row, "quote_time", alias_map)
        ctx["input_window_end"] = pick_value(row, "final_gate_created_at", alias_map)
    elif stage_id == "S10_PAPER_RUNNER":
        ctx["source_time"] = first_nonempty([pick_value(row, "paper_entry_time", alias_map), pick_value(row, "paper_signal_time", alias_map), pick_value(row, "entry_time", alias_map)])
        ctx["created_at"] = first_nonempty([pick_value(row, "paper_entry_time", alias_map), pick_value(row, "entry_time", alias_map), pick_value(row, "paper_signal_time", alias_map)])
        ctx["input_window_start"] = pick_value(row, "paper_signal_time", alias_map)
        ctx["input_window_end"] = first_nonempty([pick_value(row, "paper_entry_time", alias_map), pick_value(row, "position_opened_at", alias_map)])
    elif stage_id == "S11_FAILURE_ATTRIBUTION":
        ctx["source_time"] = pick_value(row, "failure_detected_at", alias_map)
        ctx["created_at"] = pick_value(row, "failure_detected_at", alias_map)
        ctx["input_window_start"] = pick_value(row, "entry_time", alias_map)
        ctx["input_window_end"] = pick_value(row, "exit_time", alias_map)
    elif stage_id == "S12_DAILY_REVIEW":
        ctx["source_time"] = pick_value(row, "report_generated_at", alias_map)
        ctx["created_at"] = pick_value(row, "report_generated_at", alias_map)
        ctx["input_window_start"] = pick_value(row, "report_window_start", alias_map)
        ctx["input_window_end"] = pick_value(row, "report_window_end", alias_map)
    else:
        ctx["source_time"] = pick_value(row, "source_time", alias_map)
        ctx["created_at"] = pick_value(row, "created_at", alias_map)
        ctx["input_window_start"] = pick_value(row, "input_window_start", alias_map)
        ctx["input_window_end"] = pick_value(row, "input_window_end", alias_map)

    age_sec = seconds_between(ctx.get("created_at"), now_dt)
    stale = None if age_sec is None else age_sec > ttl
    elapsed_sec = None
    if stage_id == "S2_KLINE_COLLECTION":
        elapsed_sec = seconds_between(ctx.get("quote_requested_at") or pick_value(row, "quote_requested_at", alias_map), pick_value(row, "quote_received_at", alias_map))
    elif stage_id == "S4_WALLET_STRUCTURE":
        elapsed_sec = seconds_between(pick_value(row, "wallet_refresh_started_at", alias_map), pick_value(row, "wallet_refresh_finished_at", alias_map))
    elif stage_id == "S8_QUOTE_SECURITY_LIQUIDITY":
        elapsed_sec = seconds_between(pick_value(row, "quote_requested_at", alias_map), pick_value(row, "quote_received_at", alias_map))
    elif stage_id == "S10_PAPER_RUNNER":
        elapsed_sec = seconds_between(pick_value(row, "paper_entry_requested_at", alias_map), pick_value(row, "paper_entry_created_at", alias_map))
    elif stage_id == "S11_FAILURE_ATTRIBUTION":
        elapsed_sec = seconds_between(pick_value(row, "entry_time", alias_map), pick_value(row, "exit_time", alias_map))
    elif stage_id == "S12_DAILY_REVIEW":
        elapsed_sec = seconds_between(pick_value(row, "report_window_start", alias_map), pick_value(row, "report_window_end", alias_map))

    return {
        "source_time": format_utc(ctx.get("source_time")),
        "created_at": format_utc(ctx.get("created_at")),
        "input_window_start": format_utc(ctx.get("input_window_start")),
        "input_window_end": format_utc(ctx.get("input_window_end")),
        "age_sec": age_sec,
        "ttl_sec": ttl,
        "stale": stale,
        "elapsed_sec": elapsed_sec,
        "missing_fields": missing,
        "required_inputs": required_inputs,
        "optional_inputs": optional_inputs,
    }


def evaluate_time_context_gate(row, schema=None, now=None):
    schema = schema or load_schema(DEFAULT_BASE_DIR)
    now_text = now or utc_now_text()
    now_dt = parse_time(now_text)
    alias_map = stage_alias_map(schema)

    token_address = pick_value(row, "token_address", alias_map)
    token_symbol = pick_value(row, "token_symbol", alias_map)
    token_address = str(token_address) if token_address not in (None, "") else ""
    token_symbol = str(token_symbol) if token_symbol not in (None, "") else ""

    token_open_time = format_utc(pick_value(row, "token_open_time", alias_map))
    pool_created_at = format_utc(pick_value(row, "pool_created_at", alias_map))
    discovered_at = format_utc(pick_value(row, "discovered_at", alias_map))
    candidate_discovered_at = format_utc(pick_value(row, "candidate_discovered_at", alias_map))
    first_seen_at = format_utc(pick_value(row, "first_seen_at", alias_map))
    last_seen_at = format_utc(pick_value(row, "last_seen_at", alias_map))
    candidate_snapshot_at = format_utc(pick_value(row, "candidate_snapshot_at", alias_map))
    signal_time = format_utc(pick_value(row, "signal_time", alias_map))
    signal_level = pick_value(row, "signal_level", alias_map)
    wallet_decision_created_at = format_utc(pick_value(row, "wallet_decision_created_at", alias_map))
    wallet_snapshot_at = format_utc(pick_value(row, "wallet_snapshot_at", alias_map))
    pattern_created_at = format_utc(pick_value(row, "pattern_created_at", alias_map))
    lifecycle_created_at = format_utc(pick_value(row, "lifecycle_created_at", alias_map))
    intent_created_at = format_utc(pick_value(row, "intent_created_at", alias_map))
    quote_requested_at = format_utc(pick_value(row, "quote_requested_at", alias_map))
    quote_received_at = format_utc(pick_value(row, "quote_received_at", alias_map))
    quote_time = format_utc(pick_value(row, "quote_time", alias_map))
    security_scan_time = format_utc(pick_value(row, "security_scan_time", alias_map))
    final_gate_created_at = format_utc(pick_value(row, "final_gate_created_at", alias_map))
    paper_entry_time = format_utc(pick_value(row, "paper_entry_time", alias_map))
    paper_signal_time = format_utc(pick_value(row, "paper_signal_time", alias_map))
    paper_last_update_time = format_utc(pick_value(row, "paper_last_update_time", alias_map) or pick_value(row, "last_update_time", alias_map))
    position_opened_at = format_utc(pick_value(row, "position_opened_at", alias_map) or paper_entry_time)
    failure_detected_at = format_utc(pick_value(row, "failure_detected_at", alias_map))
    entry_time = format_utc(pick_value(row, "entry_time", alias_map))
    exit_time = format_utc(pick_value(row, "exit_time", alias_map))
    report_window_start = format_utc(pick_value(row, "report_window_start", alias_map))
    report_window_end = format_utc(pick_value(row, "report_window_end", alias_map))
    report_generated_at = format_utc(pick_value(row, "report_generated_at", alias_map))

    # candidate metrics
    token_age_sec = seconds_between(token_open_time, now_dt)
    discovery_delay_sec = seconds_between(token_open_time, discovered_at) if token_open_time and discovered_at else None
    candidate_age_sec = seconds_between(candidate_snapshot_at or discovered_at or first_seen_at, now_dt)
    candidate_stage = compute_candidate_stage(token_age_sec, token_open_time)
    discovery_quality = compute_discovery_quality(discovery_delay_sec, discovered_at, token_open_time)
    requires_pattern_review = candidate_stage == "D4_OLD_TOKEN"

    # stage ages and stale flags
    latest_kline_time = format_utc(pick_value(row, "latest_kline_time", alias_map))
    kline_source_time = latest_kline_time
    latest_kline_age_sec = seconds_between(latest_kline_time, now_dt)
    kline_ttl_sec = stage_ttl(schema, "S2_KLINE_COLLECTION")
    kline_stale = None if latest_kline_age_sec is None else latest_kline_age_sec > kline_ttl_sec

    pattern_age_sec = seconds_between(pattern_created_at, now_dt)
    pattern_ttl_sec = stage_ttl(schema, "S3_PATTERN_RECOGNITION")
    pattern_stale = None if pattern_age_sec is None else pattern_age_sec > pattern_ttl_sec

    wallet_decision_age_sec = seconds_between(wallet_decision_created_at, now_dt)
    wallet_decision_ttl_sec = stage_ttl(schema, "S4_WALLET_STRUCTURE")
    wallet_decision_stale = None if wallet_decision_age_sec is None else wallet_decision_age_sec > wallet_decision_ttl_sec

    alignment_created_at = None
    alignment_age_sec = None
    alignment_ttl_sec = stage_ttl(schema, "S5_WALLET_PATTERN_ALIGNMENT")
    alignment_stale = None
    alignment_time_skew_sec = None
    if wallet_decision_created_at and pattern_created_at:
        wd = parse_time(wallet_decision_created_at)
        pt = parse_time(pattern_created_at)
        if wd and pt:
            alignment_created_at = format_utc(max(wd, pt))
            alignment_age_sec = seconds_between(alignment_created_at, now_dt)
            alignment_time_skew_sec = round(abs((wd - pt).total_seconds()), 3)
            alignment_stale = alignment_age_sec > alignment_ttl_sec if alignment_age_sec is not None else None

    lifecycle_age_sec = seconds_between(lifecycle_created_at, now_dt)
    lifecycle_ttl_sec = stage_ttl(schema, "S6_DOMINANT_LIFECYCLE")
    lifecycle_stale = None if lifecycle_age_sec is None else lifecycle_age_sec > lifecycle_ttl_sec

    intent_age_sec = seconds_between(intent_created_at, now_dt)
    intent_ttl_sec = stage_ttl(schema, "S7_DOMINANT_INTENT")
    intent_stale = None if intent_age_sec is None else intent_age_sec > intent_ttl_sec

    quote_age_sec = seconds_between(quote_time or quote_received_at, now_dt)
    quote_ttl_sec = stage_ttl(schema, "S8_QUOTE_SECURITY_LIQUIDITY")

    # signal/quote stale detection prefers explicit raw flags when present.
    raw_signal_stale = row.get("signal_stale") if isinstance(row, dict) else None
    raw_quote_stale = row.get("quote_stale") if isinstance(row, dict) else None
    signal_stale = as_bool(raw_signal_stale)
    if signal_stale is None:
        signal_stale = as_bool(pick_value(row, "signal_stale", alias_map))
    if signal_stale is None and signal_time:
        signal_age = seconds_between(signal_time, now_dt)
        if signal_age is not None:
            signal_stale = signal_age > 900
    quote_stale = as_bool(raw_quote_stale)
    if quote_stale is None:
        quote_stale = as_bool(pick_value(row, "quote_stale", alias_map))
    if quote_stale is None:
        quote_stale = None if quote_age_sec is None else quote_age_sec > quote_ttl_sec

    security_scan_age_sec = seconds_between(security_scan_time, now_dt)
    security_scan_ttl_sec = stage_ttl(schema, "S8_QUOTE_SECURITY_LIQUIDITY")
    security_scan_stale = None if security_scan_age_sec is None else security_scan_age_sec > security_scan_ttl_sec

    final_gate_age_sec = seconds_between(final_gate_created_at, now_dt)
    final_gate_ttl_sec = stage_ttl(schema, "S9_FINAL_TRADE_GATE")
    final_gate_stale = None if final_gate_age_sec is None else final_gate_age_sec > final_gate_ttl_sec

    position_age_sec = seconds_between(position_opened_at, now_dt)
    holding_duration_sec = seconds_between(entry_time, exit_time)
    time_to_failure_sec = seconds_between(entry_time, failure_detected_at) if entry_time and failure_detected_at else None

    # collect ages for skew
    ages = []
    for value in [
        candidate_age_sec, latest_kline_age_sec, pattern_age_sec, wallet_decision_age_sec, alignment_age_sec,
        lifecycle_age_sec, intent_age_sec, quote_age_sec, security_scan_age_sec, final_gate_age_sec, position_age_sec,
        seconds_between(failure_detected_at, now_dt), seconds_between(report_generated_at, now_dt),
    ]:
        if value is not None:
            ages.append(float(value))
    time_skew_sec = round(max(ages) - min(ages), 3) if len(ages) >= 2 else None

    # sync-critical fields: enough to establish a coherent temporal chain without requiring every stage
    sync_anchor_values = [
        token_open_time,
        discovered_at,
        latest_kline_time,
        pattern_created_at,
        wallet_decision_created_at,
        alignment_created_at,
        lifecycle_created_at,
        intent_created_at,
        quote_time,
        security_scan_time,
        final_gate_created_at,
    ]
    sync_anchor_count = sum(1 for value in sync_anchor_values if value is not None)
    critical_missing = time_skew_sec is None or sync_anchor_count < 2

    critical_required = stage_required_fields(schema)
    missing_fields = [field for field in sorted(critical_required) if pick_value(row, field, alias_map) in (None, "", [], {})]

    temporal_sync_status = compute_temporal_sync_status(time_skew_sec, critical_missing)
    gate = compute_gate(candidate_stage, bool(quote_stale), bool(signal_stale), temporal_sync_status, critical_missing)
    if candidate_stage == "D0_SCOUT_ONLY":
        gate = "TEMPORAL_WATCH"
    if candidate_stage == "D4_OLD_TOKEN":
        requires_pattern_review = True
        if gate == "TEMPORAL_BLOCK":
            gate = "TEMPORAL_UNKNOWN"
    if quote_stale:
        gate = "TEMPORAL_EXPIRED"
    if signal_stale and str(signal_level).upper() in {"S3", "S4"}:
        gate = "TEMPORAL_EXPIRED"
    if temporal_sync_status == "TEMPORAL_DESYNC" and gate not in {"TEMPORAL_EXPIRED", "TEMPORAL_WATCH"}:
        gate = "TEMPORAL_PAUSE"
    if gate == "TEMPORAL_ALLOW" and critical_missing:
        gate = "TEMPORAL_UNKNOWN"

    stale_flags = {
        "signal_stale": signal_stale is True,
        "kline_stale": kline_stale is True,
        "pattern_stale": pattern_stale is True,
        "wallet_decision_stale": wallet_decision_stale is True,
        "quote_stale": quote_stale is True,
        "security_scan_stale": security_scan_stale is True,
    }
    freshness_score = score_freshness(stale_flags)
    candidate_stage_score = score_candidate_stage(candidate_stage)
    discovery_quality_score = score_discovery_quality(discovery_quality)
    sync_score = score_sync(temporal_sync_status)
    missing_required_count = len(missing_fields)
    completeness_score = score_completeness(missing_required_count)
    time_context_score = max(0, min(100, candidate_stage_score + discovery_quality_score + freshness_score + sync_score + completeness_score))
    if candidate_stage == "STAGE_UNKNOWN" and discovery_quality == "DISCOVERY_UNKNOWN" and critical_missing:
        time_context_score = min(time_context_score, 20)
    if gate == "TEMPORAL_UNKNOWN" and time_context_score > 49:
        time_context_score = max(0, time_context_score - 10)
    if gate == "TEMPORAL_EXPIRED" and time_context_score > 64:
        time_context_score = max(0, time_context_score - 5)

    if time_context_score >= 80:
        time_context_grade = "TIME_STRONG"
    elif time_context_score >= 65:
        time_context_grade = "TIME_VALID"
    elif time_context_score >= 50:
        time_context_grade = "TIME_WEAK"
    elif time_context_score >= 30:
        time_context_grade = "TIME_PAUSE"
    else:
        time_context_grade = "TIME_INVALID"

    stale_sources = [k for k, v in stale_flags.items() if v]
    missing_sources = []
    if token_open_time is None:
        missing_sources.append("candidate_discovery")
    if latest_kline_time is None:
        missing_sources.append("kline_collection")
    if pattern_created_at is None:
        missing_sources.append("pattern_recognition")
    if wallet_decision_created_at is None:
        missing_sources.append("wallet_structure")
    if alignment_created_at is None:
        missing_sources.append("wallet_pattern_alignment")
    if lifecycle_created_at is None:
        missing_sources.append("dominant_lifecycle")
    if intent_created_at is None:
        missing_sources.append("dominant_intent")
    if quote_time is None and security_scan_time is None:
        missing_sources.append("quote_security")
    if final_gate_created_at is None:
        missing_sources.append("final_gate")
    if paper_entry_time is None and paper_signal_time is None:
        missing_sources.append("paper_runner")
    if failure_detected_at is None:
        missing_sources.append("failure_attribution")
    if report_generated_at is None:
        missing_sources.append("daily_review")

    temporal_reason = describe_reason(gate, candidate_stage, temporal_sync_status, stale_flags, len(missing_fields))

    out = {
        "token_address": token_address,
        "token_symbol": token_symbol,
        "generated_at": now_text,
        "pipeline_round_id": f"time_context_{now_text.replace(':', '').replace('-', '').replace('Z', '')}",
        "token_open_time": token_open_time,
        "pool_created_at": format_utc(pool_created_at),
        "discovered_at": discovered_at,
        "first_seen_at": first_seen_at,
        "last_seen_at": last_seen_at,
        "candidate_snapshot_at": candidate_snapshot_at,
        "token_age_sec": token_age_sec,
        "discovery_delay_sec": discovery_delay_sec,
        "candidate_age_sec": candidate_age_sec,
        "candidate_stage": candidate_stage,
        "discovery_quality": discovery_quality,
        "requires_pattern_review": requires_pattern_review,
        "signal_time": signal_time,
        "signal_level": signal_level,
        "signal_stale": signal_stale,
        "kline_source_time": kline_source_time,
        "latest_kline_time": latest_kline_time,
        "latest_kline_age_sec": latest_kline_age_sec,
        "kline_ttl_sec": kline_ttl_sec,
        "kline_stale": kline_stale,
        "pattern_created_at": pattern_created_at,
        "pattern_age_sec": pattern_age_sec,
        "pattern_ttl_sec": pattern_ttl_sec,
        "pattern_stale": pattern_stale,
        "wallet_decision_created_at": wallet_decision_created_at,
        "wallet_snapshot_at": wallet_snapshot_at,
        "wallet_decision_age_sec": wallet_decision_age_sec,
        "wallet_decision_ttl_sec": wallet_decision_ttl_sec,
        "wallet_decision_stale": wallet_decision_stale,
        "alignment_created_at": alignment_created_at,
        "alignment_age_sec": alignment_age_sec,
        "alignment_ttl_sec": alignment_ttl_sec,
        "alignment_stale": alignment_stale,
        "alignment_time_skew_sec": alignment_time_skew_sec,
        "lifecycle_created_at": lifecycle_created_at,
        "lifecycle_age_sec": lifecycle_age_sec,
        "lifecycle_ttl_sec": lifecycle_ttl_sec,
        "lifecycle_stale": lifecycle_stale,
        "intent_created_at": intent_created_at,
        "intent_age_sec": intent_age_sec,
        "intent_ttl_sec": intent_ttl_sec,
        "intent_stale": intent_stale,
        "quote_time": quote_time,
        "quote_age_sec": quote_age_sec,
        "quote_ttl_sec": quote_ttl_sec,
        "quote_stale": quote_stale,
        "security_scan_time": security_scan_time,
        "security_scan_age_sec": security_scan_age_sec,
        "security_scan_ttl_sec": security_scan_ttl_sec,
        "security_scan_stale": security_scan_stale,
        "final_gate_created_at": final_gate_created_at,
        "final_gate_age_sec": final_gate_age_sec,
        "final_gate_ttl_sec": final_gate_ttl_sec,
        "final_gate_stale": final_gate_stale,
        "paper_entry_time": paper_entry_time,
        "paper_signal_time": paper_signal_time,
        "paper_last_update_time": paper_last_update_time,
        "position_opened_at": position_opened_at,
        "position_age_sec": position_age_sec,
        "failure_detected_at": failure_detected_at,
        "entry_time": entry_time,
        "exit_time": exit_time,
        "holding_duration_sec": holding_duration_sec,
        "time_to_failure_sec": time_to_failure_sec,
        "report_window_start": report_window_start,
        "report_window_end": report_window_end,
        "report_generated_at": report_generated_at,
        "time_skew_sec": time_skew_sec,
        "temporal_sync_status": temporal_sync_status,
        "temporal_gate": gate,
        "time_context_score": time_context_score,
        "time_context_grade": time_context_grade,
        "missing_fields": missing_fields,
        "missing_sources": sorted(set(missing_sources)),
        "refresh_required": bool(critical_missing or any(v for v in stale_flags.values()) or gate in {"TEMPORAL_UNKNOWN", "TEMPORAL_PAUSE", "TEMPORAL_EXPIRED"}),
        "stale_sources": stale_sources,
        "temporal_reason": temporal_reason,
        "time_context_gate": "time_context_gate",
        "stage_missing_fields": {},
        "stage_stale_flags": {},
        "stage_missing_fields_json": "{}",
        "stage_stale_flags_json": "{}",
    }

    # stage-specific context for report/debugging
    stage_missing_fields = {}
    stage_stale_flags = {}
    for stage_id in STAGE_ORDER:
        sc = build_stage_context(stage_id, row, alias_map, schema, now_dt)
        stage_missing_fields[stage_id] = sc["missing_fields"]
        stage_stale_flags[stage_id] = bool(sc["stale"])
        if stage_id == "S0_SYSTEM_BASELINE":
            out["report_generated_at"] = out["report_generated_at"] or sc["created_at"]
        if stage_id == "S1_CANDIDATE_DISCOVERY":
            out["candidate_snapshot_at"] = out["candidate_snapshot_at"] or sc["created_at"]
        if stage_id == "S2_KLINE_COLLECTION":
            out["latest_kline_time"] = out["latest_kline_time"] or sc["created_at"]
        if stage_id == "S3_PATTERN_RECOGNITION":
            out["pattern_created_at"] = out["pattern_created_at"] or sc["created_at"]
        if stage_id == "S4_WALLET_STRUCTURE":
            out["wallet_decision_created_at"] = out["wallet_decision_created_at"] or sc["created_at"]
        if stage_id == "S5_WALLET_PATTERN_ALIGNMENT":
            out["alignment_created_at"] = out["alignment_created_at"] or sc["created_at"]
        if stage_id == "S6_DOMINANT_LIFECYCLE":
            out["lifecycle_created_at"] = out["lifecycle_created_at"] or sc["created_at"]
        if stage_id == "S7_DOMINANT_INTENT":
            out["intent_created_at"] = out["intent_created_at"] or sc["created_at"]
        if stage_id == "S8_QUOTE_SECURITY_LIQUIDITY":
            out["quote_time"] = out["quote_time"] or sc["created_at"]
            out["security_scan_time"] = out["security_scan_time"] or sc["created_at"]
        if stage_id == "S9_FINAL_TRADE_GATE":
            out["final_gate_created_at"] = out["final_gate_created_at"] or sc["created_at"]
        if stage_id == "S10_PAPER_RUNNER":
            out["paper_entry_time"] = out["paper_entry_time"] or sc["created_at"]
        if stage_id == "S11_FAILURE_ATTRIBUTION":
            out["failure_detected_at"] = out["failure_detected_at"] or sc["created_at"]
        if stage_id == "S12_DAILY_REVIEW":
            out["report_generated_at"] = out["report_generated_at"] or sc["created_at"]
    out["stage_missing_fields"] = stage_missing_fields
    out["stage_stale_flags"] = stage_stale_flags
    out["stage_missing_fields_json"] = json.dumps(stage_missing_fields, ensure_ascii=False)
    out["stage_stale_flags_json"] = json.dumps(stage_stale_flags, ensure_ascii=False)

    # D4 rule: requires_pattern_review always true, but never hard-blocked.
    if candidate_stage == "D4_OLD_TOKEN":
        out["requires_pattern_review"] = True
        if out["temporal_gate"] == "TEMPORAL_BLOCK":
            out["temporal_gate"] = "TEMPORAL_UNKNOWN"

    # D0 rule enforced
    if candidate_stage == "D0_SCOUT_ONLY" and out["temporal_gate"] == "TEMPORAL_ALLOW":
        out["temporal_gate"] = "TEMPORAL_WATCH"

    return out


def summarize(rows):
    stage_stale_counts = Counter(k for r in rows for k, v in r.get("stage_stale_flags", {}).items() if v)
    return {
        "token_count": len(rows),
        "temporal_gate": Counter(r.get("temporal_gate", "TEMPORAL_UNKNOWN") for r in rows),
        "candidate_stage": Counter(r.get("candidate_stage", "STAGE_UNKNOWN") for r in rows),
        "discovery_quality": Counter(r.get("discovery_quality", "DISCOVERY_UNKNOWN") for r in rows),
        "temporal_sync_status": Counter(r.get("temporal_sync_status", "TEMPORAL_UNKNOWN") for r in rows),
        "stale_counts": Counter(k for r in rows for k, v in {
            "signal_stale": r.get("signal_stale"),
            "kline_stale": r.get("kline_stale"),
            "pattern_stale": r.get("pattern_stale"),
            "wallet_decision_stale": r.get("wallet_decision_stale"),
            "quote_stale": r.get("quote_stale"),
            "security_scan_stale": r.get("security_scan_stale"),
            "final_gate_stale": r.get("final_gate_stale"),
        }.items() if v),
        "missing_fields_top10": Counter(field for r in rows for field in r.get("missing_fields", [])).most_common(10),
        "missing_sources": sorted(set(src for r in rows for src in r.get("missing_sources", []))),
        "stage_stale_counts": stage_stale_counts,
    }


def build_input_audit(rows_raw, merged, runtime, base_dir):
    merged_rows = list(merged.values())
    valid_token_rows = [row for row in rows_raw if row.get("token_address")]
    token_before_dedup = len(valid_token_rows)
    token_after_dedup = len(merged_rows)
    duplicate_tokens = max(0, token_before_dedup - token_after_dedup)

    source_file_counts = Counter()
    for row in rows_raw:
        source = row.get("_source_path")
        if source:
            source_file_counts[str(source)] += 1

    token_source_labels = Counter()
    for row in rows_raw:
        if row.get("token_address") and row.get("_source_label"):
            token_source_labels[str(row["_source_label"])] += 1

    fields = [
        "token_open_time",
        "discovered_at",
        "first_seen_at",
        "last_seen_at",
        "signal_time",
        "signal_level",
        "wallet_decision_created_at",
        "quote_time",
        "security_scan_time",
    ]
    field_stats = {}
    for field in fields:
        available = 0
        path_counts = Counter()
        for row in merged_rows:
            if row.get(field) not in (None, "", [], {}):
                available += 1
        for row in rows_raw:
            if row.get(field) not in (None, "", [], {}):
                path = str(row.get("_source_path") or "unknown")
                path_counts[path] += 1
        field_stats[field] = {
            "available_count": available,
            "available_rate": round((available / token_after_dedup) if token_after_dedup else 0.0, 6),
            "top_paths": [
                {"path": path, "count": count}
                for path, count in path_counts.most_common(10)
            ],
        }

    stage_unknown_count = sum(1 for row in merged_rows if row.get("candidate_stage") == "STAGE_UNKNOWN")
    temporal_unknown_count = sum(1 for row in merged_rows if row.get("temporal_gate") == "TEMPORAL_UNKNOWN")

    fallback_token_source = "gmgn_new_token_filter/token_candidates.json"
    source_priority = [
        "candidates.json",
        "gmgn_new_token_filter/token_candidates.json",
        "state_machine/candidate_states.json",
        "candidate_signal_outputs/candidate_signal_summary.json",
        "site/dashboard_data.json",
        "live_state.json",
    ]

    audit = {
        "generated_at": runtime["generated_at"],
        "run_dir": str(base_dir),
        "token_source_priority": source_priority,
        "fallback_token_source_when_candidates_missing": fallback_token_source,
        "token_before_dedup": token_before_dedup,
        "token_after_dedup": token_after_dedup,
        "duplicate_tokens": duplicate_tokens,
        "source_file_counts": dict(source_file_counts.most_common()),
        "token_source_label_counts": dict(token_source_labels.most_common()),
        "field_availability": field_stats,
        "stage_unknown_count": stage_unknown_count,
        "temporal_unknown_count": temporal_unknown_count,
        "why_stage_unknown": [
            "candidate input sources are mixed and incomplete across gmgn_new_token_filter, state_machine, candidate_signal_outputs, dashboard_data, live_state, paper_live, quote_security",
            "first_seen_at is absent for all observed merged tokens, and token_open_time appears in only a single source row",
            "many rows only carry downstream paper/report artifacts rather than canonical discovery-stage fields",
        ],
        "why_temporal_unknown": [
            "compute_temporal_sync_status returns TEMPORAL_UNKNOWN when the temporal chain is incomplete",
            "critical anchors are sparse: token_open_time, quote_time, security_scan_time, wallet_decision_created_at, pattern_created_at are missing for most tokens",
            "missing_fields remain high because the merged rows do not have a complete cross-stage timeline",
        ],
        "missing_fields_top10": runtime.get("missing_fields_top10", []),
        "token_source_files": [
            {"path": path, "count": count}
            for path, count in source_file_counts.most_common()
        ],
    }
    return audit


def write_outputs(rows, base_dir, out_dir, schema, runtime):
    out_dir.mkdir(parents=True, exist_ok=True)
    now_text = runtime["generated_at"]
    summary = summarize(rows)
    summary["d0_temporal_allow_count"] = sum(1 for r in rows if r.get("candidate_stage") == "D0_SCOUT_ONLY" and r.get("temporal_gate") == "TEMPORAL_ALLOW")
    summary["d4_wrong_block_count"] = sum(1 for r in rows if r.get("candidate_stage") == "D4_OLD_TOKEN" and r.get("temporal_gate") == "TEMPORAL_BLOCK")
    summary["quote_stale_allow_count"] = sum(1 for r in rows if r.get("quote_stale") and r.get("temporal_gate") == "TEMPORAL_ALLOW")
    summary["s3_s4_expired_count"] = sum(1 for r in rows if str(r.get("signal_level") or "").upper() in {"S3", "S4"} and r.get("signal_stale") and r.get("temporal_gate") == "TEMPORAL_EXPIRED")
    # Preserve compatibility for downstream tests and reporting.
    summary["stage_stale_counts"] = Counter(k for r in rows for k, v in r.get("stage_stale_flags", {}).items() if v)

    schema_path = out_dir / "time_context_schema.json"
    if not schema_path.exists():
        schema_payload = {
            "module": "sikk_time_context_gate.py",
            "generated_at": now_text,
            "stage_order": STAGE_ORDER,
            "boundary": "只读时间治理；不修改状态机、钱包结构、盘型识别、paper runner、实盘逻辑。",
            "notes": "Generated alongside time-context outputs.",
        }
        schema_path.write_text(json.dumps(schema_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    payload = {
        "meta": {
            "module": "sikk_time_context_gate.py",
            "generated_at": now_text,
            "run_dir": str(base_dir),
            "output_dir": str(out_dir),
            "boundary": "只读时间治理；不修改状态机、钱包结构、盘型识别、paper runner、实盘逻辑。",
        },
        "summary": {
            **summary,
            "d0_temporal_allow_count": summary["d0_temporal_allow_count"],
            "d4_wrong_block_count": summary["d4_wrong_block_count"],
            "quote_stale_allow_count": summary["quote_stale_allow_count"],
            "s3_s4_expired_count": summary["s3_s4_expired_count"],
        },
        "tokens": rows,
    }
    (out_dir / "time_context_summary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    csv_fields = list(PREFERRED_OUTPUT_FIELDS)
    for row in rows:
        for key in row.keys():
            if key not in csv_fields:
                csv_fields.append(key)

    with (out_dir / "time_context_summary.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            csv_row = {}
            for field in csv_fields:
                value = row.get(field)
                if isinstance(value, (dict, list)):
                    csv_row[field] = json.dumps(value, ensure_ascii=False)
                elif value is None:
                    csv_row[field] = ""
                else:
                    csv_row[field] = value
            writer.writerow(csv_row)

    audit = build_input_audit(runtime.get("rows_raw", []), runtime.get("merged", {}), runtime, base_dir)
    (out_dir / "time_context_input_audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")

    audit_lines = []
    audit_lines.append("# SIKK 时间上下文输入源收敛审计")
    audit_lines.append("")
    audit_lines.append(f"- 生成时间：{runtime['generated_at']}")
    audit_lines.append(f"- token 去重前数量：{audit['token_before_dedup']}")
    audit_lines.append(f"- token 去重后数量：{audit['token_after_dedup']}")
    audit_lines.append(f"- 重复 token 数量：{audit['duplicate_tokens']}")
    audit_lines.append(f"- candidates.json 缺失时当前 fallback token 来源：{audit['fallback_token_source_when_candidates_missing']}")
    audit_lines.append("")
    audit_lines.append("## token 来源文件")
    for item in audit["token_source_files"]:
        audit_lines.append(f"- {item['path']}: {item['count']}")
    audit_lines.append("")
    audit_lines.append("## 关键字段可用率与主要路径")
    for field, info in audit["field_availability"].items():
        audit_lines.append(f"- {field}: {info['available_count']}/{audit['token_after_dedup']} ({info['available_rate']:.2%})")
        for item in info["top_paths"][:5]:
            audit_lines.append(f"  - {item['path']}: {item['count']}")
    audit_lines.append("")
    audit_lines.append(f"- candidate_stage 大量 STAGE_UNKNOWN 的原因：{'; '.join(audit['why_stage_unknown'])}")
    audit_lines.append(f"- temporal_gate 大量 TEMPORAL_UNKNOWN 的原因：{'; '.join(audit['why_temporal_unknown'])}")
    audit_lines.append("")
    audit_lines.append("## 缺失最多的字段 Top 10")
    for field, count in summary["missing_fields_top10"]:
        audit_lines.append(f"- {field}: {count}")
    (out_dir / "time_context_input_audit.md").write_text("\n".join(audit_lines) + "\n", encoding="utf-8")

    report_lines = []
    report_lines.append("# SIKK 全系统时间上下文协同门禁报告")
    report_lines.append("")
    report_lines.append(f"- 生成时间：{now_text}")
    report_lines.append(f"- token 总数：{summary['token_count']}")
    report_lines.append(f"- candidate_stage 分布：{json.dumps(dict(summary['candidate_stage']), ensure_ascii=False)}")
    report_lines.append(f"- discovery_quality 分布：{json.dumps(dict(summary['discovery_quality']), ensure_ascii=False)}")
    report_lines.append(f"- temporal_gate 分布：{json.dumps(dict(summary['temporal_gate']), ensure_ascii=False)}")
    report_lines.append(f"- temporal_sync_status 分布：{json.dumps(dict(summary['temporal_sync_status']), ensure_ascii=False)}")
    report_lines.append(f"- stale 字段统计：{json.dumps(dict(summary['stale_counts']), ensure_ascii=False)}")
    report_lines.append("")
    report_lines.append("## missing_fields Top 10")
    for field, count in summary["missing_fields_top10"]:
        report_lines.append(f"- {field}: {count}")
    report_lines.append("")
    report_lines.append("## missing_sources 列表")
    for src in summary["missing_sources"]:
        report_lines.append(f"- {src}")
    report_lines.append("")
    report_lines.append(f"- D0 是否出现 TEMPORAL_ALLOW：{'是' if summary['d0_temporal_allow_count'] else '否'}")
    report_lines.append(f"- D4 是否被错误 TEMPORAL_BLOCK：{'是' if summary['d4_wrong_block_count'] else '否'}")
    report_lines.append(f"- quote_stale=true 是否出现 TEMPORAL_ALLOW：{'是' if summary['quote_stale_allow_count'] else '否'}")
    report_lines.append(f"- S3/S4 signal_stale=true 是否正确 TEMPORAL_EXPIRED：{'是' if summary['s3_s4_expired_count'] else '否'}")
    report_lines.append("")
    report_lines.append("## token 明细")
    for row in rows:
        report_lines.append(
            f"- {row.get('token_symbol') or 'UNKNOWN'} / {row.get('token_address')}: gate={row.get('temporal_gate')} "
            f"sync={row.get('temporal_sync_status')} score={row.get('time_context_score')} grade={row.get('time_context_grade')}"
        )
    (out_dir / "time_context_report.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    runtime_log = {
        "module": "sikk_time_context_gate.py",
        "generated_at": now_text,
        "run_dir": str(base_dir),
        "output_dir": str(out_dir),
        "read_attempts": runtime["inventory"],
        "missing_inputs": runtime["missing_input_files"],
        "missing_sources": runtime["global_missing_sources"],
        "token_count": len(rows),
        "candidate_sources_seen": runtime["source_counts"],
        "notes": [
            "只读时间门禁，不修改状态机/钱包结构/paper runner/实盘逻辑。",
            "缺字段写 null 并记录到 missing_fields / missing_sources。",
            "每个 candidate 输出一行。",
        ],
    }
    (out_dir / "time_context_runtime_log.json").write_text(json.dumps(runtime_log, ensure_ascii=False, indent=2), encoding="utf-8")

    return payload


def run_time_context_gate(base_dir=DEFAULT_BASE_DIR, output_dir=None, now=None):
    base_dir = Path(base_dir)
    output_dir = Path(output_dir) if output_dir else base_dir / DEFAULT_OUTPUT_SUBDIR
    schema = load_schema(base_dir)
    now_text = now or utc_now_text()
    inventory, missing_input_files = collect_source_inventory(base_dir)
    rows_raw, source_rows, global_missing_sources = gather_candidate_rows(base_dir, inventory)
    merged = merge_records(rows_raw)

    # If we still have no tokens, try seed fallback from dashboard/candidate files again.
    if not merged:
        for path in [base_dir / "gmgn_new_token_filter" / "token_candidates.json", base_dir / "state_machine" / "candidate_states.json"]:
            payload = load_json_or_none(path)
            if payload:
                rows_raw.extend(extract_rows_from_payload(payload, path.name, str(path)))
        merged = merge_records(rows_raw)

    results = []
    for token in sorted(merged.keys()):
        row = merged[token]
        result = evaluate_time_context_gate(row, schema=schema, now=now_text)
        results.append(result)

    # If a token only exists in one source tree but missing token_address, we keep the row out.
    payload = write_outputs(results, base_dir, output_dir, schema, {
        "generated_at": now_text,
        "inventory": inventory,
        "missing_input_files": missing_input_files,
        "global_missing_sources": sorted(set(global_missing_sources)),
        "source_counts": {k: len(v) for k, v in source_rows.items()},
        "rows_raw": rows_raw,
        "merged": merged,
        "missing_fields_top10": summarize(results)["missing_fields_top10"],
    })
    return payload


def main(argv=None):
    parser = argparse.ArgumentParser(description="SIKK 全系统时间上下文协同门禁")
    parser.add_argument("--run-dir", default="")
    parser.add_argument("--base-dir", default="")
    parser.add_argument("--output-dir", default="")
    parser.add_argument("--now", default="")
    args = parser.parse_args(argv)
    base_dir = args.run_dir or args.base_dir or str(DEFAULT_BASE_DIR)
    payload = run_time_context_gate(base_dir=base_dir, output_dir=args.output_dir or None, now=args.now or None)
    print(json.dumps({"status": "ok", "token_count": payload["summary"]["token_count"], "output_dir": args.output_dir or str(Path(base_dir) / DEFAULT_OUTPUT_SUBDIR)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
