from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

PHASE01_REQUIRED_CONFIG = ["run_id", "token_address", "chain", "run_mode", "data_snapshot_time"]


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _first_existing(base: Path, candidates: list[str]) -> Path | None:
    for rel in candidates:
        p = base / rel
        if p.exists():
            return p
    return None


def _copy_json(src: Path | None, dst: Path, default: Any) -> str:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src and src.exists():
        shutil.copyfile(src, dst)
    else:
        dst.write_text(json.dumps(default, ensure_ascii=False, indent=2), encoding="utf-8")
    return dst.name


def build_phase01_input_from_source_wallet_run(
    *,
    token_address: str,
    source_wallet_run_dir: str | Path,
    output_file: str | Path,
    run_id: str,
    chain: str = "sol",
) -> Dict[str, Any]:
    """Adapt a read-only source_wallet_bot run into Stable Trader OS Phase01 input_contract.

    The adapter is fact-only: it copies upstream normalized/raw JSON artifacts next to
    the generated input package and returns source references consumable by Phase01Runner.
    It does not classify wallets, infer scenarios, sign, broadcast, or trade.
    """
    source_dir = Path(source_wallet_run_dir)
    output = Path(output_file)
    out_dir = output.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    wallet_trade = _first_existing(source_dir, ["wallet_data/normalized/wallet_trade_normalized.json"])
    wallet_profile = _first_existing(source_dir, ["wallet_data/normalized/wallet_entity_profile_normalized.json"])
    quote_security = _first_existing(source_dir, ["wallet_data/normalized/quote_security_normalized.json"])
    transfer = _first_existing(source_dir, ["wallet_data/normalized/token_transfer_normalized.json"])
    holder_delta = _first_existing(source_dir, ["wallet_data/normalized/holder_delta_normalized.json"])

    sources = {
        "gmgn_traders": _copy_json(wallet_trade, out_dir / "gmgn_traders.json", {"record_count": 0, "records": []}),
        "gmgn_holders": _copy_json(wallet_profile or holder_delta or wallet_trade, out_dir / "gmgn_holders.json", {"record_count": 0, "records": []}),
        "quote_security": _copy_json(quote_security, out_dir / "quote_security.json", {"status": "missing", "missing": True}),
        "transfer": _copy_json(transfer, out_dir / "transfer.json", {"record_count": 0, "records": []}),
        "kline": _copy_json(None, out_dir / "kline.json", {"record_count": 0, "records": [], "fact_status": "missing"}),
    }

    snapshot_time = _now()
    for candidate in [wallet_trade, wallet_profile, quote_security, transfer, holder_delta]:
        if candidate and candidate.exists():
            try:
                data = _load_json(candidate)
                if isinstance(data, dict):
                    for key in ("generated_at", "created_at", "data_snapshot_time", "snapshot_time"):
                        if data.get(key):
                            snapshot_time = str(data[key])
                            raise StopIteration
            except StopIteration:
                break
            except Exception:
                pass

    missing = []
    if quote_security is None:
        missing.append("quote_security")
    if holder_delta is None and wallet_profile is None:
        missing.append("holder_profile")
    if transfer is None:
        missing.append("transfer")
    missing.append("kline")

    payload: Dict[str, Any] = {
        "run_id": run_id,
        "token_address": token_address,
        "chain": chain,
        "run_mode": "real_ca_readonly",
        "data_snapshot_time": snapshot_time,
        "sources": sources,
        "contains_mock_data": False,
        "missing_fields_demo": sorted(set(missing)),
        "anomaly_demo": [],
        "adapter": {
            "name": "gmgn_source_wallet_to_phase01",
            "source_wallet_run_dir": str(source_dir),
            "fact_only": True,
            "readonly": True,
        },
    }
    for key in PHASE01_REQUIRED_CONFIG:
        if not payload.get(key):
            raise ValueError(f"missing Phase01 required_config: {key}")
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload
