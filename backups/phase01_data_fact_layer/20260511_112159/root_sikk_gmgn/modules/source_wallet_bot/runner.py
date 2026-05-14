from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .handoff_exporter import build_handoff_packet
from .io_utils import read_json, write_json
from .phase01_fact_store_router import build_fact_store_index
from .role_classifier import classify_wallet
from .schema_validator import validate_source_wallet_design_package
from .source_group_engine import build_same_source_groups
from .wallet_profile_normalizer import normalize_wallet_profile
from .wallet_trade_normalizer import normalize_wallet_trades


def _load_records(path: str | Path) -> list[dict[str, Any]]:
    payload = read_json(path)
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("records"), list):
        return payload["records"]
    raise SystemExit(f"input must be a list or object with records list: {path}")


def cmd_normalize_wallet_trade(args: argparse.Namespace) -> int:
    rows = _load_records(args.input)
    records = normalize_wallet_trades(rows)
    payload = {
        "artifact_type": "wallet_trade_normalized",
        "record_count": len(records),
        "records": [record.to_dict() for record in records],
    }
    write_json(args.output, payload)
    print(f"wallet_trade_normalized_written={args.output}")
    return 0


def cmd_build_source_groups(args: argparse.Namespace) -> int:
    profile_rows = _load_records(args.profiles)
    trade_rows = _load_records(args.trades)
    profiles = [normalize_wallet_profile(row) for row in profile_rows]
    trades = normalize_wallet_trades(trade_rows)
    groups = build_same_source_groups(profiles, trades)
    write_json(args.output, {
        "artifact_type": "same_source_evidence_normalized",
        "record_count": len(groups),
        "records": [group.to_dict() for group in groups],
    })
    print(f"same_source_groups_written={args.output}")
    return 0


def cmd_classify_wallets(args: argparse.Namespace) -> int:
    profile_rows = _load_records(args.profiles)
    trade_rows = _load_records(args.trades)
    profiles = [normalize_wallet_profile(row) for row in profile_rows]
    trades = normalize_wallet_trades(trade_rows)
    groups = build_same_source_groups(profiles, trades)
    profile_by_wallet = {profile.wallet_address: profile for profile in profiles}
    decisions = [classify_wallet(trade, profile_by_wallet.get(trade.wallet_address), groups) for trade in trades]
    write_json(args.output, {
        "artifact_type": "wallet_intelligence_decision",
        "record_count": len(decisions),
        "records": [decision.to_dict() for decision in decisions],
    })
    print(f"wallet_decisions_written={args.output}")
    return 0


def cmd_build_handoff(args: argparse.Namespace) -> int:
    profile_rows = _load_records(args.profiles)
    trade_rows = _load_records(args.trades)
    profiles = [normalize_wallet_profile(row) for row in profile_rows]
    trades = normalize_wallet_trades(trade_rows)
    groups = build_same_source_groups(profiles, trades)
    profile_by_wallet = {profile.wallet_address: profile for profile in profiles}
    decisions = [classify_wallet(trade, profile_by_wallet.get(trade.wallet_address), groups) for trade in trades]
    token_address = args.token_address or (trades[0].token_address if trades else "missing")
    packet = build_handoff_packet(
        token_address=token_address,
        wallet_trades=trades,
        wallet_profiles=profiles,
        source_groups=groups,
        decisions=decisions,
    )
    write_json(args.output, packet.to_dict())
    print(f"bot2_handoff_packet_written={args.output}")
    return 0


def cmd_validate_package(args: argparse.Namespace) -> int:
    result = validate_source_wallet_design_package(args.root)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    if not result["ok"]:
        return 1
    print("SOURCE_WALLET_BOT_IMPLEMENTATION_PACKAGE_OK")
    return 0


def cmd_index_fact_store(args: argparse.Namespace) -> int:
    index = build_fact_store_index(
        args.token_address,
        mode=args.mode,
        root=Path(args.root),
        write=not args.no_write,
    )
    print(json.dumps(index.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    if index.quality_status in {"PASS", "PASS_WITH_WARNING"}:
        return 0
    return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SIKK Source Wallet Intelligence Bot runner")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("normalize-wallet-trade")
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    p.set_defaults(func=cmd_normalize_wallet_trade)

    p = sub.add_parser("build-source-groups")
    p.add_argument("--profiles", required=True)
    p.add_argument("--trades", required=True)
    p.add_argument("--output", required=True)
    p.set_defaults(func=cmd_build_source_groups)

    p = sub.add_parser("classify-wallets")
    p.add_argument("--profiles", required=True)
    p.add_argument("--trades", required=True)
    p.add_argument("--output", required=True)
    p.set_defaults(func=cmd_classify_wallets)

    p = sub.add_parser("build-handoff")
    p.add_argument("--profiles", required=True)
    p.add_argument("--trades", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--token-address", default="")
    p.set_defaults(func=cmd_build_handoff)

    p = sub.add_parser("validate-package")
    p.add_argument("--root", default="/root/sikk-gmgn")
    p.set_defaults(func=cmd_validate_package)

    p = sub.add_parser("index-fact-store")
    p.add_argument("--token-address", required=True)
    p.add_argument("--mode", default="live", choices=["ad_hoc", "archive", "legacy", "live", "live_test"])
    p.add_argument("--root", default="/root/sikk-gmgn")
    p.add_argument("--no-write", action="store_true")
    p.set_defaults(func=cmd_index_fact_store)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
