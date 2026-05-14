from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

from .validator import Phase01Validator

PHASE_ID = "phase_01_data_fact_controller"
NEXT_STAGE = "phase_02_wallet_structure_controller"


class Phase01Runner:
    """Professional Phase 01 runtime runner.

    Converts a Phase 01 input package into normalized fact artifacts, quality
    gate, handoff packet, validation reports, and runtime trace. This runner is
    deliberately read-only with respect to trading execution: it never signs,
    broadcasts, swaps, or emits buy/sell permission.
    """

    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.validator = Phase01Validator(self.root)

    def run(self, input_file: str | Path, output_dir: str | Path | None = None) -> Dict[str, Any]:
        input_file = Path(input_file)
        payload = json.loads(input_file.read_text())
        run_id = payload.get("run_id", "phase_01_run_missing")
        output_dir = Path(output_dir) if output_dir else self.root / "data" / "stable_trader_os" / "runs" / run_id
        phase_dir = output_dir / "01_data_fact"
        raw_dir = phase_dir / "raw"
        normalized_dir = phase_dir / "normalized"
        audit_dir = phase_dir / "audit"
        handoff_dir = phase_dir / "handoff"
        report_dir = phase_dir / "reports"
        summary_dir = phase_dir / "summary"
        shared_handoff_dir = output_dir / "shared_handoff" / str(payload.get("token_address", "missing"))
        for d in (raw_dir, normalized_dir, audit_dir, handoff_dir, report_dir, summary_dir, shared_handoff_dir):
            d.mkdir(parents=True, exist_ok=True)

        trace: List[Dict[str, Any]] = []
        def event(name: str, **extra: Any) -> None:
            trace.append({"ts": self._now(), "phase": PHASE_ID, "event": name, **extra})

        event("input_loaded", input_file=str(input_file))
        verdict = self.validator.validate_input(input_file)
        event("input_validated", gate_status=verdict["gate_status"], allowed=verdict["allowed"])

        raw_manifest = self._write_raw_manifest(raw_dir, payload, input_file)
        event("raw_snapshot_written", path=str(raw_manifest))

        token_fact_path = normalized_dir / "token_fact.json"
        token_basic_path = normalized_dir / "token_basic_normalized.json"
        token_market_context_path = normalized_dir / "token_market_context.json"
        token_fact = self._token_fact(payload)
        self._write_json(token_fact_path, token_fact)
        self._write_json(token_basic_path, {**token_fact, "schema_name": "token_basic_normalized"})
        self._write_json(token_market_context_path, self._token_market_context(payload))
        event("token_fact_written", path=str(token_fact_path))

        wallet_path = normalized_dir / "wallet_fact_table.csv"
        trade_path = normalized_dir / "trade_fact_table.csv"
        holder_path = normalized_dir / "holder_fact_table.csv"
        kline_path = normalized_dir / "kline_fact_table.csv"
        quote_path = normalized_dir / "quote_fact.json"
        security_path = normalized_dir / "security_fact.json"
        wallet_normalized_path = normalized_dir / "wallet_trade_normalized.csv"
        holder_normalized_path = normalized_dir / "holder_normalized.csv"
        kline_normalized_path = normalized_dir / "kline_normalized.csv"
        quote_security_normalized_path = normalized_dir / "quote_security_normalized.json"
        wallet_rows = self._wallet_rows(payload, input_file.parent)
        trade_rows = self._trade_rows(payload, input_file.parent)
        holder_rows = self._holder_rows(payload, input_file.parent)
        kline_rows = self._kline_rows(payload, input_file.parent)
        self._write_csv(wallet_path, ["wallet_address", "source", "fact_status", "evidence_ref"], wallet_rows)
        self._write_csv(trade_path, ["wallet_address", "side", "amount", "price", "timestamp", "fact_status", "evidence_ref"], trade_rows)
        self._write_csv(holder_path, ["wallet_address", "holding_amount", "holding_pct", "fact_status", "evidence_ref"], holder_rows)
        self._write_csv(kline_path, ["timestamp", "open", "high", "low", "close", "volume", "fact_status", "evidence_ref"], kline_rows)
        self._write_csv(wallet_normalized_path, ["wallet_address", "side", "amount", "price", "timestamp", "fact_status", "evidence_ref"], trade_rows)
        self._write_csv(holder_normalized_path, ["wallet_address", "holding_amount", "holding_pct", "fact_status", "evidence_ref"], holder_rows)
        self._write_csv(kline_normalized_path, ["timestamp", "open", "high", "low", "close", "volume", "fact_status", "evidence_ref"], kline_rows)
        quote_security = {"quote_status": "missing", "security_status": "missing", "fact_status": "missing", "evidence_ref": "missing"}
        self._write_json(quote_path, {"quote_status": "missing", "fact_status": "missing", "evidence_ref": "missing"})
        self._write_json(security_path, {"security_status": "missing", "fact_status": "missing", "evidence_ref": "missing"})
        self._write_json(quote_security_normalized_path, quote_security)
        event("normalized_facts_written", directory=str(normalized_dir))

        missing_fields = sorted(set(verdict.get("missing_fields", []) + payload.get("missing_fields_demo", [])))
        anomaly_fields = list(payload.get("anomaly_demo", []))
        if missing_fields and verdict["gate_status"] == "PASS":
            verdict["gate_status"] = "PASS_WITH_WARNING"
        status_code = self._status_code(verdict["gate_status"], missing_fields)
        quality = {
            "phase": PHASE_ID,
            "status_code": status_code,
            "gate_status": verdict["gate_status"],
            "phase_state": self._phase_state(verdict["gate_status"]),
            "allowed_next_stage": verdict["gate_status"] in {"PASS", "PASS_WITH_WARNING"},
            "next_stage": NEXT_STAGE,
            "positive_evidence": verdict.get("positive_evidence", []),
            "negative_evidence": verdict.get("negative_evidence", []),
            "counter_evidence": verdict.get("counter_evidence", []),
            "missing_fields": missing_fields,
            "anomaly_fields": anomaly_fields,
            "hard_negative_triggered": verdict["gate_status"] == "BLOCK",
            "hard_negative_reasons": verdict.get("hard_negative_reasons", []),
            "forbidden_judgement_leakage": "forbidden_judgement_leakage" in verdict.get("hard_negative_reasons", []),
        }
        quality_path = audit_dir / "phase_01_quality_gate.json"
        data_quality_summary_path = summary_dir / "data_quality_summary.json"
        self._write_json(quality_path, quality)
        self._write_json(data_quality_summary_path, quality)
        event("quality_gate_written", path=str(quality_path), gate_status=quality["gate_status"])

        missing_report = audit_dir / "missing_fields_report.md"
        missing_report.write_text(self._missing_report(missing_fields), encoding="utf-8")
        anomaly_report = audit_dir / "anomaly_fields_report.csv"
        self._write_csv(anomaly_report, ["field", "anomaly_type", "action"], [[a, "demo_or_detected", "degrade_or_review"] for a in anomaly_fields])
        event("missing_and_anomaly_reports_written")

        handoff_path = handoff_dir / "phase_01_to_phase_02_handoff_packet.json"
        canonical_handoff_path = handoff_dir / "phase_01_handoff_packet.json"
        shared_handoff_path = shared_handoff_dir / "phase_01_handoff_packet.json"
        handoff = self._handoff_packet(payload, quality, normalized_dir, audit_dir)
        handoff["audit_file"] = str(audit_dir / "phase_01_quality_gate.json")
        self._write_json(handoff_path, handoff)
        self._write_json(canonical_handoff_path, handoff)
        self._write_json(shared_handoff_path, handoff)
        event("handoff_written", path=str(canonical_handoff_path), next_stage=NEXT_STAGE)

        output_validation_path = audit_dir / "output_validation_report.json"
        handoff_validation_path = audit_dir / "handoff_validation_report.json"
        required = [raw_manifest, token_fact_path, token_basic_path, token_market_context_path, wallet_path, trade_path, holder_path, kline_path, quote_path, security_path, wallet_normalized_path, holder_normalized_path, kline_normalized_path, quote_security_normalized_path, quality_path, data_quality_summary_path, missing_report, anomaly_report, handoff_path, canonical_handoff_path, shared_handoff_path]
        output_validation = {"status": "PASS" if all(p.exists() for p in required) else "FAIL", "checked_files": [str(p) for p in required]}
        self._write_json(output_validation_path, output_validation)
        handoff_validation = {"status": "PASS" if handoff.get("next_stage") == NEXT_STAGE else "FAIL", "next_stage": handoff.get("next_stage")}
        self._write_json(handoff_validation_path, handoff_validation)
        gaps_path = audit_dir / "gaps.md"
        gaps_path.write_text("# gaps\n\n- missing\n" if missing_fields else "# gaps\n\n- none\n", encoding="utf-8")
        event("audit_validation_written")

        report_path = report_dir / "phase_01_data_fact_report.md"
        report_path.write_text(self._report(payload, quality, handoff_path), encoding="utf-8")
        event("report_written", path=str(report_path))

        trace_path = audit_dir / "phase_01_runtime_trace.jsonl"
        trace_path.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in trace) + "\n", encoding="utf-8")

        manifest_path = phase_dir / "run_manifest.json"
        manifest = {
            "run_id": run_id,
            "phase_id": PHASE_ID,
            "professional_level": "runtime_executable_with_contract_validation",
            "status": quality["gate_status"],
            "phase_state": quality["phase_state"],
            "input_file": str(input_file),
            "output_dir": str(output_dir),
            "artifacts": {
                "run_manifest": str(manifest_path),
                "quality_gate": str(quality_path),
                "data_quality_summary": str(data_quality_summary_path),
                "handoff_packet": str(canonical_handoff_path),
                "shared_handoff_packet": str(shared_handoff_path),
                "runtime_trace": str(trace_path),
                "report": str(report_path),
            },
        }
        self._write_json(manifest_path, manifest)
        return {
            "status": quality["gate_status"],
            "phase_state": quality["phase_state"],
            "run_manifest": str(manifest_path),
            "quality_gate": str(quality_path),
            "handoff_packet": str(handoff_path),
            "canonical_handoff_packet": str(canonical_handoff_path),
            "shared_handoff_packet": str(shared_handoff_path),
            "data_quality_summary": str(data_quality_summary_path),
            "runtime_trace": str(trace_path),
        }

    def _status_code(self, gate_status: str, missing_fields: List[str]) -> str:
        if gate_status == "BLOCK":
            return "DATA_INVALID"
        if gate_status == "PAUSE":
            return "DATA_WEAK"
        if missing_fields or gate_status == "PASS_WITH_WARNING":
            return "DATA_PARTIAL"
        return "DATA_OK"

    def _phase_state(self, gate_status: str) -> str:
        if gate_status == "BLOCK":
            return "P01_BLOCKED"
        if gate_status == "PAUSE":
            return "P01_PAUSED"
        return "P01_COMPLETE"

    def _now(self) -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    def _write_json(self, path: Path, payload: Dict[str, Any]) -> None:
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def _write_csv(self, path: Path, header: List[str], rows: Iterable[Iterable[Any]]) -> None:
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for row in rows:
                writer.writerow(list(row))

    def _write_raw_manifest(self, raw_dir: Path, payload: Dict[str, Any], input_file: Path) -> Path:
        manifest = raw_dir / "raw_source_manifest.json"
        sources = payload.get("sources", {}) if isinstance(payload.get("sources", {}), dict) else {}
        self._write_json(manifest, {
            "input_file": str(input_file),
            "token_address": payload.get("token_address", "missing"),
            "sources": sources,
            "source_count": len(sources),
            "fact_only": True,
        })
        return manifest

    def _load_source(self, sources: Dict[str, str], key: str, base_dir: Path) -> Any:
        ref = sources.get(key)
        if not ref:
            return None
        p = base_dir / ref
        try:
            return json.loads(p.read_text())
        except Exception:
            return None

    def _token_fact(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "token_address": payload.get("token_address", "missing"),
            "chain": payload.get("chain", "missing"),
            "data_snapshot_time": payload.get("data_snapshot_time", "missing"),
            "run_mode": payload.get("run_mode", "missing"),
            "fact_status": "observed",
            "forbidden_judgement": "not_present",
        }

    def _token_market_context(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "token_address": payload.get("token_address", "missing"),
            "chain": payload.get("chain", "missing"),
            "data_snapshot_time": payload.get("data_snapshot_time", "missing"),
            "market_context_status": "missing",
            "liquidity_usd": "missing",
            "volume_24h": "missing",
            "fact_status": "missing",
            "evidence_ref": "missing",
        }

    def _wallet_rows(self, payload: Dict[str, Any], base_dir: Path) -> List[List[Any]]:
        traders = self._load_source(payload.get("sources", {}), "gmgn_traders", base_dir) or []
        if isinstance(traders, dict):
            traders = traders.get("traders", traders.get("data", []))
        rows = []
        for item in traders if isinstance(traders, list) else []:
            wallet = item.get("wallet") or item.get("address") or item.get("wallet_address") or "missing"
            rows.append([wallet, "gmgn_traders", "observed" if wallet != "missing" else "missing", "gmgn_traders"])
        return rows or [["missing", "gmgn_traders", "missing", "missing"]]

    def _trade_rows(self, payload: Dict[str, Any], base_dir: Path) -> List[List[Any]]:
        traders = self._load_source(payload.get("sources", {}), "gmgn_traders", base_dir) or []
        if isinstance(traders, dict):
            traders = traders.get("trades", traders.get("traders", traders.get("data", [])))
        rows = []
        for item in traders if isinstance(traders, list) else []:
            rows.append([
                item.get("wallet") or item.get("address") or item.get("wallet_address") or "missing",
                item.get("side", "missing"), item.get("amount", "missing"), item.get("price", "missing"), item.get("timestamp", "missing"),
                "observed", "gmgn_traders",
            ])
        return rows or [["missing", "missing", "missing", "missing", "missing", "missing", "missing"]]

    def _holder_rows(self, payload: Dict[str, Any], base_dir: Path) -> List[List[Any]]:
        holders = self._load_source(payload.get("sources", {}), "gmgn_holders", base_dir) or []
        if isinstance(holders, dict):
            holders = holders.get("holders", holders.get("data", []))
        rows = []
        for item in holders if isinstance(holders, list) else []:
            rows.append([item.get("wallet") or item.get("address") or "missing", item.get("amount", "missing"), item.get("pct", item.get("holding_pct", "missing")), "observed", "gmgn_holders"])
        return rows or [["missing", "missing", "missing", "missing", "missing"]]

    def _kline_rows(self, payload: Dict[str, Any], base_dir: Path) -> List[List[Any]]:
        kline = self._load_source(payload.get("sources", {}), "kline", base_dir) or []
        if isinstance(kline, dict):
            kline = kline.get("kline", kline.get("data", []))
        rows = []
        for item in kline if isinstance(kline, list) else []:
            rows.append([item.get("timestamp", "missing"), item.get("open", "missing"), item.get("high", "missing"), item.get("low", "missing"), item.get("close", "missing"), item.get("volume", "missing"), "observed", "kline"])
        return rows or [["missing", "missing", "missing", "missing", "missing", "missing", "missing", "missing"]]

    def _missing_report(self, missing_fields: List[str]) -> str:
        lines = ["# missing_fields_report", ""]
        if not missing_fields:
            lines.append("- none")
        else:
            for f in missing_fields:
                lines.append(f"- {f}: missing")
        return "\n".join(lines) + "\n"

    def _handoff_packet(self, payload: Dict[str, Any], quality: Dict[str, Any], normalized_dir: Path, audit_dir: Path) -> Dict[str, Any]:
        return {
            "phase": PHASE_ID,
            "token_address": payload.get("token_address", "missing"),
            "snapshot_id": payload.get("run_id", "missing"),
            "phase_status": quality["status_code"],
            "primary_status": quality["status_code"],
            "handoff_status": "HANDOFF_BLOCKED" if quality["gate_status"] == "BLOCK" else ("HANDOFF_DEGRADED" if quality["missing_fields"] else "HANDOFF_READY"),
            "phase_state": quality["phase_state"],
            "allow_next_stage": quality["allowed_next_stage"],
            "next_stage": NEXT_STAGE,
            "required_files_for_next_stage": {
                "token_basic_normalized": str(normalized_dir / "token_basic_normalized.json"),
                "token_market_context": str(normalized_dir / "token_market_context.json"),
                "token_fact": str(normalized_dir / "token_fact.json"),
                "wallet_fact_table": str(normalized_dir / "wallet_fact_table.csv"),
                "trade_fact_table": str(normalized_dir / "trade_fact_table.csv"),
                "holder_fact_table": str(normalized_dir / "holder_fact_table.csv"),
                "quality_gate": str(audit_dir / "phase_01_quality_gate.json"),
            },
            "positive_evidence": quality["positive_evidence"],
            "negative_evidence": quality["negative_evidence"],
            "counter_evidence": quality["counter_evidence"],
            "hard_negative_triggered": quality["hard_negative_triggered"],
            "block_reason": ";".join(quality["hard_negative_reasons"]),
            "degrade_reason": "missing_fields" if quality["missing_fields"] else "",
            "missing_fields": quality["missing_fields"],
            "audit_file": str(audit_dir / "phase_01_quality_gate.json"),
        }

    def _report(self, payload: Dict[str, Any], quality: Dict[str, Any], handoff_path: Path) -> str:
        return "\n".join([
            "# Phase 01 数据事实层 Runtime Report",
            "",
            f"- token_address: `{payload.get('token_address', 'missing')}`",
            f"- gate_status: `{quality['gate_status']}`",
            f"- phase_state: `{quality['phase_state']}`",
            f"- next_stage: `{NEXT_STAGE}`",
            f"- missing_fields: `{quality['missing_fields']}`",
            f"- hard_negative_triggered: `{quality['hard_negative_triggered']}`",
            f"- handoff_packet: `{handoff_path}`",
            "",
            "## 边界",
            "- Phase 01 只输出事实与质量门禁，不输出买卖点、庄家定性或交易许可。",
        ]) + "\n"
