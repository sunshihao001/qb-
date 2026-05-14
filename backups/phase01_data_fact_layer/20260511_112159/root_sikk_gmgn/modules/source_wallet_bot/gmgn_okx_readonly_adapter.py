from __future__ import annotations

import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping

from modules.shared_verification import validate_stage_output

FORBIDDEN_COMMAND_TOKENS = {
    "swap",
    "multi-swap",
    "execute",
    "sign",
    "broadcast",
    "send",
    "private-key",
    "private_key",
    "mnemonic",
    "seed",
    "order",  # GMGN/OKX order routes are not part of raw read-only research collector.
}

SECRET_KEY_PATTERN = re.compile(r"(api[_-]?key|secret|private[_-]?key|mnemonic|seed[_-]?phrase|passphrase|access[_-]?token|auth[_-]?token)", re.I)
SOLANA_ADDRESS_RE = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$")


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(path: str | Path, payload: Any) -> str:
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


def redact_secrets(value: Any) -> Any:
    if isinstance(value, Mapping):
        cleaned: dict[str, Any] = {}
        for key, child in value.items():
            if SECRET_KEY_PATTERN.search(str(key)):
                cleaned[str(key)] = "[REDACTED]"
            else:
                cleaned[str(key)] = redact_secrets(child)
        return cleaned
    if isinstance(value, list):
        return [redact_secrets(item) for item in value]
    if isinstance(value, str):
        # Redact obvious inline secret assignments without mutating ordinary token addresses.
        return re.sub(r"(?i)(api[_-]?key|secret|private[_-]?key|mnemonic|seed[_-]?phrase|passphrase|access[_-]?token|auth[_-]?token)\s*[:=]\s*[^\s,;]+", r"\1=[REDACTED]", value)
    return value


def parse_json_or_text(text: str) -> Any:
    stripped = (text or "").strip()
    if not stripped:
        return {}
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        # Some CLIs emit human text. Preserve it as raw text; mapper will mark partial evidence.
        return {"raw_text": stripped[:20000], "parse_status": "TEXT_NOT_JSON"}


def validate_solana_token_address(token_address: str) -> None:
    if not SOLANA_ADDRESS_RE.match(token_address or ""):
        raise ValueError("token_address 必须是 Solana base58 地址，32-44 字符；拒绝执行 collector。")


def ensure_readonly_command(command: list[str]) -> None:
    if not command:
        raise ValueError("empty command")
    joined_tokens = {part.lower() for part in command}
    normalized_tokens = {part.lower().lstrip("-").replace("-", "_") for part in command}
    bad = sorted(FORBIDDEN_COMMAND_TOKENS.intersection(joined_tokens | normalized_tokens))
    joined = " ".join(command).lower()
    phrase_bad = [phrase for phrase in ["swap execute", "order strategy", "private key", ".env"] if phrase in joined]
    if bad or phrase_bad:
        raise ValueError(f"collector 只允许只读命令，拒绝：{' '.join(command)}")
    if command[0] == "gmgn-cli":
        allowed = [
            ["gmgn-cli", "token", "info"],
            ["gmgn-cli", "token", "security"],
            ["gmgn-cli", "token", "pool"],
            ["gmgn-cli", "token", "holders"],
            ["gmgn-cli", "token", "traders"],
            ["gmgn-cli", "market", "kline"],
        ]
        if not any(command[: len(prefix)] == prefix for prefix in allowed):
            raise ValueError(f"GMGN collector 命令不在白名单：{' '.join(command)}")
    elif command[0] == "onchainos":
        allowed = [
            ["onchainos", "token", "search"],
            ["onchainos", "token", "info"],
            ["onchainos", "token", "price-info"],
            ["onchainos", "token", "liquidity"],
            ["onchainos", "token", "advanced-info"],
            ["onchainos", "token", "holders"],
            ["onchainos", "token", "top-trader"],
            ["onchainos", "token", "cluster-overview"],
            ["onchainos", "token", "cluster-top-holders"],
            ["onchainos", "token", "cluster-list"],
            ["onchainos", "security", "token-scan"],
            ["onchainos", "market", "kline"],
            ["onchainos", "market", "price"],
        ]
        if not any(command[: len(prefix)] == prefix for prefix in allowed):
            raise ValueError(f"OKX collector 命令不在白名单：{' '.join(command)}")
    else:
        raise ValueError(f"collector 只允许 gmgn-cli/onchainos：{command[0]}")


@dataclass(frozen=True)
class CollectorCommand:
    source: str
    endpoint: str
    command: list[str]
    required: bool = False
    timeout: int = 90


def build_token_readonly_commands(token_address: str, *, gmgn_chain: str = "sol", okx_chain: str = "solana", limit: int = 50, include_kline: bool = False) -> list[CollectorCommand]:
    validate_solana_token_address(token_address)
    gmgn_base = ["--chain", gmgn_chain, "--address", token_address]
    cmds: list[CollectorCommand] = [
        CollectorCommand("gmgn", "token_info", ["gmgn-cli", "token", "info", *gmgn_base, "--raw"], True),
        CollectorCommand("gmgn", "token_security", ["gmgn-cli", "token", "security", *gmgn_base, "--raw"], True),
        CollectorCommand("gmgn", "token_pool", ["gmgn-cli", "token", "pool", *gmgn_base, "--raw"], True),
        CollectorCommand("gmgn", "token_holders", ["gmgn-cli", "token", "holders", *gmgn_base, "--limit", str(limit), "--order-by", "amount_percentage", "--direction", "desc", "--raw"], False),
        CollectorCommand("gmgn", "token_traders", ["gmgn-cli", "token", "traders", *gmgn_base, "--limit", str(limit), "--order-by", "profit", "--direction", "desc", "--raw"], False),
        CollectorCommand("gmgn", "holders_transfer_in", ["gmgn-cli", "token", "holders", *gmgn_base, "--limit", str(min(limit, 20)), "--tag", "transfer_in", "--order-by", "amount_percentage", "--direction", "desc", "--raw"], False),
        CollectorCommand("gmgn", "holders_bundler", ["gmgn-cli", "token", "holders", *gmgn_base, "--limit", str(min(limit, 20)), "--tag", "bundler", "--order-by", "amount_percentage", "--direction", "desc", "--raw"], False),
        CollectorCommand("gmgn", "holders_fresh", ["gmgn-cli", "token", "holders", *gmgn_base, "--limit", str(min(limit, 20)), "--tag", "fresh_wallet", "--order-by", "amount_percentage", "--direction", "desc", "--raw"], False),
        CollectorCommand("okx", "token_search", ["onchainos", "token", "search", "--query", token_address, "--chains", "501"], False),
        CollectorCommand("okx", "token_info", ["onchainos", "token", "info", "--address", token_address, "--chain", okx_chain], False),
        CollectorCommand("okx", "price_info", ["onchainos", "token", "price-info", "--address", token_address, "--chain", okx_chain], True),
        CollectorCommand("okx", "liquidity", ["onchainos", "token", "liquidity", "--address", token_address, "--chain", okx_chain], False),
        CollectorCommand("okx", "advanced_info", ["onchainos", "token", "advanced-info", "--address", token_address, "--chain", okx_chain], False),
        CollectorCommand("okx", "holders", ["onchainos", "token", "holders", "--address", token_address, "--chain", okx_chain, "--limit", str(limit)], False),
        CollectorCommand("okx", "top_trader", ["onchainos", "token", "top-trader", "--address", token_address, "--chain", okx_chain, "--limit", str(limit)], False),
        CollectorCommand("okx", "cluster_overview", ["onchainos", "token", "cluster-overview", "--address", token_address, "--chain", okx_chain], False),
        CollectorCommand("okx", "cluster_top_holders_10", ["onchainos", "token", "cluster-top-holders", "--address", token_address, "--chain", okx_chain, "--range-filter", "1"], False),
        CollectorCommand("okx", "cluster_top_holders_50", ["onchainos", "token", "cluster-top-holders", "--address", token_address, "--chain", okx_chain, "--range-filter", "2"], False),
        CollectorCommand("okx", "cluster_top_holders_100", ["onchainos", "token", "cluster-top-holders", "--address", token_address, "--chain", okx_chain, "--range-filter", "3"], False),
        CollectorCommand("okx", "cluster_list", ["onchainos", "token", "cluster-list", "--address", token_address, "--chain", okx_chain], False),
        CollectorCommand("okx", "security_token_scan", ["onchainos", "security", "token-scan", "--tokens", f"501:{token_address}"], False),
    ]
    if include_kline:
        cmds.extend([
            CollectorCommand("gmgn", "market_kline_1m", ["gmgn-cli", "market", "kline", "--chain", gmgn_chain, "--address", token_address, "--resolution", "1m", "--raw"], False),
            CollectorCommand("okx", "market_kline", ["onchainos", "market", "kline", "--address", token_address, "--chain", okx_chain], False),
        ])
    for cmd in cmds:
        ensure_readonly_command(cmd.command)
    return cmds


def run_command(command: list[str], *, timeout: int) -> dict[str, Any]:
    ensure_readonly_command(command)
    executable = shutil.which(command[0])
    if not executable:
        return {
            "available": False,
            "exit_code": None,
            "stdout": "",
            "stderr": f"{command[0]} not installed",
            "parsed": {},
        }
    completed = subprocess.run(command, text=True, capture_output=True, timeout=timeout, check=False)
    stdout = completed.stdout or ""
    stderr = completed.stderr or ""
    return {
        "available": True,
        "exit_code": completed.returncode,
        "stdout": stdout[:200000],
        "stderr": stderr[:20000],
        "parsed": redact_secrets(parse_json_or_text(stdout)),
    }


def collect_token_raw_snapshot(
    token_address: str,
    *,
    output_root: str | Path,
    gmgn_chain: str = "sol",
    okx_chain: str = "solana",
    limit: int = 50,
    include_kline: bool = False,
    allow_network: bool = True,
) -> dict[str, Any]:
    """Run read-only GMGN/OKX token collectors and persist raw snapshots.

    Directory governance answers:
    - Bot/domain: source_wallet_bot + sikk_sol_full_auto_workflow collector adapter
    - Asset: runtime data raw snapshot / StageOutput evidence
    - Asset ID: token_address
    - Route: data/source_wallet_bot/{mode}/{token_address}/wallet_data/raw/
    """
    validate_solana_token_address(token_address)
    root = Path(output_root)
    raw_dir = root / "wallet_data" / "raw"
    manifest_dir = root / "manifest"
    raw_dir.mkdir(parents=True, exist_ok=True)
    manifest_dir.mkdir(parents=True, exist_ok=True)
    commands = build_token_readonly_commands(token_address, gmgn_chain=gmgn_chain, okx_chain=okx_chain, limit=limit, include_kline=include_kline)
    rows: list[dict[str, Any]] = []
    for item in commands:
        started = iso_now()
        if allow_network:
            try:
                result = run_command(item.command, timeout=item.timeout)
            except Exception as exc:  # noqa: BLE001 - record external CLI failures as data quality facts
                result = {"available": shutil.which(item.command[0]) is not None, "exit_code": "EXCEPTION", "stdout": "", "stderr": f"{type(exc).__name__}: {exc}", "parsed": {}}
        else:
            result = {"available": shutil.which(item.command[0]) is not None, "exit_code": "SKIPPED_NO_NETWORK", "stdout": "", "stderr": "network collection disabled", "parsed": {}}
        record = {
            "source": item.source,
            "endpoint": item.endpoint,
            "required": item.required,
            "command_redacted": item.command,
            "started_at": started,
            "finished_at": iso_now(),
            "available": result.get("available"),
            "exit_code": result.get("exit_code"),
            "stderr_head": str(result.get("stderr") or "")[:1000],
            "parsed": result.get("parsed", {}),
        }
        rows.append(record)
        write_json(raw_dir / f"{item.source}_{item.endpoint}.raw.json", record)
    success_count = sum(1 for row in rows if row.get("exit_code") == 0)
    required_failures = [row for row in rows if row.get("required") and row.get("exit_code") != 0]
    manifest = {
        "token_address": token_address,
        "chain": "solana",
        "gmgn_chain": gmgn_chain,
        "okx_chain": okx_chain,
        "created_at": iso_now(),
        "mode": "read_only_raw_collector",
        "paper_only": True,
        "live_disabled": True,
        "commands_total": len(rows),
        "commands_success": success_count,
        "required_failures": [{"source": r["source"], "endpoint": r["endpoint"], "exit_code": r["exit_code"], "stderr_head": r["stderr_head"]} for r in required_failures],
        "raw_files": [str(raw_dir / f"{row['source']}_{row['endpoint']}.raw.json") for row in rows],
        "no_secret_files_read": True,
        "no_trade_commands": True,
    }
    write_json(manifest_dir / "token_output_manifest.json", manifest)
    return {"manifest": manifest, "records": rows, "raw_dir": str(raw_dir)}


def _first_mapping(payload: Any) -> Mapping[str, Any]:
    if isinstance(payload, Mapping):
        if isinstance(payload.get("data"), Mapping):
            return payload["data"]
        if isinstance(payload.get("result"), Mapping):
            return payload["result"]
        return payload
    if isinstance(payload, list) and payload and isinstance(payload[0], Mapping):
        return payload[0]
    return {}


def _list_len(payload: Any) -> int:
    if isinstance(payload, Mapping):
        for key in ("list", "data", "result", "items"):
            val = payload.get(key)
            if isinstance(val, list):
                return len(val)
        return 1 if payload else 0
    if isinstance(payload, list):
        return len(payload)
    return 0


def _num(*values: Any) -> float | None:
    for value in values:
        if value in (None, "", [], {}):
            continue
        try:
            return float(value)
        except (TypeError, ValueError):
            continue
    return None


def _get_nested(data: Mapping[str, Any], path: str) -> Any:
    cur: Any = data
    for part in path.split("."):
        if not isinstance(cur, Mapping):
            return None
        cur = cur.get(part)
    return cur


def _record_map(snapshot: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    result: dict[str, Mapping[str, Any]] = {}
    for row in snapshot.get("records", []) or []:
        if isinstance(row, Mapping):
            result[f"{row.get('source')}:{row.get('endpoint')}"] = row
    return result




def _list_payload(payload: Any) -> list[Mapping[str, Any]]:
    """Return list rows from common GMGN/OKX raw payload shapes."""
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, Mapping)]
    if isinstance(payload, Mapping):
        for key in ("list", "data", "result", "items", "rows"):
            val = payload.get(key)
            if isinstance(val, list):
                return [row for row in val if isinstance(row, Mapping)]
        nested = payload.get("data") or payload.get("result")
        if isinstance(nested, Mapping):
            return _list_payload(nested)
    return []


def _text_from_mapping(row: Mapping[str, Any], *keys: str) -> str:
    for key in keys:
        value = row.get(key)
        if value not in (None, "", [], {}):
            return str(value)
    return ""


def _float_from_mapping(row: Mapping[str, Any], *keys: str, default: float = 0.0) -> float:
    for key in keys:
        value = row.get(key)
        if value in (None, "", [], {}):
            continue
        try:
            return float(str(value).strip().rstrip("%"))
        except (TypeError, ValueError):
            continue
    return default


def _merge_tag_list(*values: Any) -> list[str]:
    tags: list[str] = []
    for value in values:
        if isinstance(value, str):
            candidates = [part.strip() for part in re.split(r"[,;|]", value) if part.strip()]
        elif isinstance(value, Iterable) and not isinstance(value, (bytes, Mapping)):
            candidates = [str(part).strip() for part in value if str(part).strip()]
        else:
            candidates = []
        for item in candidates:
            if item not in tags:
                tags.append(item)
    return tags


def _classify_readonly_wallet_row(row: Mapping[str, Any], *, source: str) -> dict[str, Any]:
    """Map GMGN/OKX holder/trader rows into the existing wallet-structure gate input.

    This intentionally feeds the canonical `sikk_candidate_wallet_structure_pipeline` /
    `sikk_wallet_structure_gate` contract instead of creating a second wallet-analysis system.
    """
    tags = _merge_tag_list(row.get("tags"), row.get("tag"), row.get("wallet_tags"), row.get("walletTag"))
    maker_tags = _merge_tag_list(row.get("maker_token_tags"), row.get("makerTokenTags"), row.get("token_tags"), row.get("tokenTags"))
    all_tags = {tag.lower() for tag in [*tags, *maker_tags]}
    sell_ratio = _float_from_mapping(row, "sell_amount_percentage", "sell_ratio", "sellRatio", "sold_pct", "soldPct", default=0.0)
    if sell_ratio > 1:
        sell_ratio = sell_ratio / 100.0
    hold_ratio = _float_from_mapping(row, "amount_percentage", "holding_ratio", "holdingRatio", "hold_pct", "holdPct", "balance_pct", default=0.0)
    if hold_ratio > 1:
        hold_ratio = hold_ratio / 100.0
    profit = _float_from_mapping(row, "profit", "total_profit", "pnl", "realized_profit", "unrealized_profit", default=0.0)
    roi = _text_from_mapping(row, "profit_percentage", "roi", "pnl_rate", "pnlRate")
    is_transfer = bool(row.get("transfer_in") or row.get("transferIn") or row.get("current_transfer_in_amount")) or "transfer_in" in all_tags
    is_new = bool(row.get("is_new") or row.get("isNew")) or "fresh_wallet" in all_tags
    suspicious = bool(row.get("is_suspicious") or row.get("isSuspicious")) or bool({"wash_trader", "rat_trader"}.intersection(all_tags))

    role = "普通交易钱包"
    evidence = "E1"
    status = "仍持有" if hold_ratio > 0 else "未知"
    if is_transfer and sell_ratio >= 0.6:
        role, evidence, status = "分发派发钱包", "E4", "已清仓"
    elif is_transfer:
        role, evidence = "Token接收钱包", "E3"
    elif suspicious:
        role, evidence = "可疑中转节点", "R2"
    elif "bundler" in all_tags and is_new:
        role, evidence = "临时执行钱包", "E3"
    elif "sniper" in all_tags or is_new:
        role, evidence = "新钱包狙击", "E2"
    elif {"smart_degen", "smart", "kol", "renowned"}.intersection(all_tags) and profit > 0:
        role, evidence = "结果钱包", "E3"
    elif profit > 5000 and hold_ratio > 0:
        role, evidence = "高结果鲸鱼", "E4"
    elif sell_ratio >= 0.7:
        role, evidence, status = "接盘鲸鱼", "R2", "已清仓"

    address = _text_from_mapping(row, "address", "wallet_address", "walletAddress", "holderAddress", "traderAddress", "owner")
    return {
        "钱包地址": address,
        "wallet_address": address,
        "当前角色": role,
        "role": role,
        "证据等级": evidence,
        "evidence_level": evidence,
        "当前状态": status,
        "收益倍数": roi,
        "卖出占比": sell_ratio,
        "sell_ratio": sell_ratio,
        "持仓占比": hold_ratio,
        "holding_ratio": hold_ratio,
        "GMGN标签": ",".join([*tags, *maker_tags]),
        "资金来源状态": "资金待查",
        "主要原因": f"只读{source}证据；tags={','.join([*tags, *maker_tags]) or '无'}；profit={profit}；hold={hold_ratio}；sell_ratio={sell_ratio}",
        "原始证据引用": source,
        "source_time": _text_from_mapping(row, "source_time", "snapshot_time", "updated_at", "last_active_time") or iso_now(),
    }


def map_raw_snapshot_to_wallet_structure_rows(snapshot: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Map read-only GMGN/OKX raw snapshot into canonical wallet-structure rows.

    Output rows are consumed by the already-existing wallet structure system:
    `sikk_candidate_wallet_structure_pipeline.run_candidate_wallet_structure_pipeline` and
    `sikk_wallet_structure_gate.evaluate_wallet_structure_gate`.
    """
    records = _record_map(snapshot)
    sources = [
        ("gmgn:token_holders", records.get("gmgn:token_holders", {}).get("parsed", {})),
        ("gmgn:token_traders", records.get("gmgn:token_traders", {}).get("parsed", {})),
        ("gmgn:holders_transfer_in", records.get("gmgn:holders_transfer_in", {}).get("parsed", {})),
        ("gmgn:holders_bundler", records.get("gmgn:holders_bundler", {}).get("parsed", {})),
        ("gmgn:holders_fresh", records.get("gmgn:holders_fresh", {}).get("parsed", {})),
        ("okx:holders", records.get("okx:holders", {}).get("parsed", {})),
        ("okx:top_trader", records.get("okx:top_trader", {}).get("parsed", {})),
    ]
    by_address: dict[str, dict[str, Any]] = {}
    for source, payload in sources:
        for raw_row in _list_payload(payload):
            mapped = _classify_readonly_wallet_row(raw_row, source=source)
            address = mapped.get("wallet_address") or mapped.get("钱包地址")
            if not address:
                continue
            existing = by_address.setdefault(str(address), mapped)
            if existing is mapped:
                continue
            # Preserve the strongest/most useful evidence while merging tags and refs.
            existing["GMGN标签"] = ",".join(_merge_tag_list(existing.get("GMGN标签"), mapped.get("GMGN标签")))
            existing["原始证据引用"] = ";".join(_merge_tag_list(existing.get("原始证据引用"), mapped.get("原始证据引用")))
            existing["持仓占比"] = max(float(existing.get("持仓占比") or 0), float(mapped.get("持仓占比") or 0))
            existing["holding_ratio"] = existing["持仓占比"]
            existing["卖出占比"] = max(float(existing.get("卖出占比") or 0), float(mapped.get("卖出占比") or 0))
            existing["sell_ratio"] = existing["卖出占比"]
            evidence_order = {"E0": 0, "E1": 1, "E2": 2, "R1": 2, "E3": 3, "R2": 3, "E4": 4, "R3": 4, "E5": 5}
            if evidence_order.get(str(mapped.get("evidence_level")), 0) > evidence_order.get(str(existing.get("evidence_level")), 0):
                for key in ["当前角色", "role", "证据等级", "evidence_level", "当前状态", "主要原因"]:
                    existing[key] = mapped[key]
    return list(by_address.values())


def collect_wallet_structure_rows_for_token(
    token_address: str,
    symbol: str = "",
    *,
    output_root: str | Path,
    limit: int = 50,
    include_kline: bool = False,
    allow_network: bool = True,
) -> list[dict[str, Any]]:
    """Collector callable for the existing wallet-structure pipeline.

    Use this as `wallet_collector` in `run_candidate_wallet_structure_pipeline`; it writes raw
    evidence under the canonical source_wallet_bot token directory and returns wallet rows in the
    existing gate contract. `symbol` is accepted for API compatibility.
    """
    del symbol
    snapshot = collect_token_raw_snapshot(
        token_address,
        output_root=output_root,
        limit=limit,
        include_kline=include_kline,
        allow_network=allow_network,
    )
    rows = map_raw_snapshot_to_wallet_structure_rows(snapshot)
    normalized_dir = Path(output_root) / "wallet_data" / "normalized"
    write_json(normalized_dir / "wallet_structure_collector_rows.json", {"artifact_type": "wallet_structure_collector_rows", "token_address": token_address, "record_count": len(rows), "records": rows})
    return rows


def _stage_output(stage_id: str, status: str, token_address: str, *, facts: dict[str, Any] | None = None, stats: dict[str, Any] | None = None, inference: dict[str, Any] | None = None, evidence_refs: list[str] | None = None, source_skill: list[str] | None = None, counter_evidence: list[Any] | None = None, invalidation_condition: str = "数据过期、源返回冲突或反证出现时失效。") -> dict[str, Any]:
    return {
        "stage_id": stage_id,
        "status": status,
        "facts": {"token_address": token_address, "chain": "solana", **(facts or {})},
        "stats": stats or {},
        "evidence": [{"source": ref, "claim": "GMGN/OKX read-only raw evidence"} for ref in (evidence_refs or [])],
        "inference": inference or {},
        "counter_evidence": counter_evidence or [],
        "inference_boundary": "本输出由只读 raw collector 映射，仅用于结构证据/纸面验证，不代表真实交易建议。",
        "source_skill": source_skill or [],
        "source_fields": ["token_address", "chain", *list((facts or {}).keys()), *list((stats or {}).keys()), *list((inference or {}).keys())],
        "evidence_refs": evidence_refs or [stage_id],
        "freshness": {"observed_at": iso_now(), "max_age_sec": 900},
        "invalidation_condition": invalidation_condition,
        "paper_only": True,
        "live_disabled": True,
    }


def map_raw_snapshot_to_stage_outputs(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    token_address = str(snapshot.get("manifest", {}).get("token_address") or "")
    records = _record_map(snapshot)
    required_failures = snapshot.get("manifest", {}).get("required_failures") or []
    gmgn_info = _first_mapping(records.get("gmgn:token_info", {}).get("parsed", {}))
    gmgn_sec = _first_mapping(records.get("gmgn:token_security", {}).get("parsed", {}))
    gmgn_pool = _first_mapping(records.get("gmgn:token_pool", {}).get("parsed", {}))
    okx_price = _first_mapping(records.get("okx:price_info", {}).get("parsed", {}))
    okx_adv = _first_mapping(records.get("okx:advanced_info", {}).get("parsed", {}))
    okx_liq = _first_mapping(records.get("okx:liquidity", {}).get("parsed", {}))
    okx_cluster = _first_mapping(records.get("okx:cluster_overview", {}).get("parsed", {}))
    security_scan = _first_mapping(records.get("okx:security_token_scan", {}).get("parsed", {}))

    symbol = str(gmgn_info.get("symbol") or okx_price.get("symbol") or okx_adv.get("tokenSymbol") or "UNKNOWN")
    market_cap = _num(gmgn_info.get("market_cap"), _get_nested(gmgn_info, "stat.market_cap"), okx_price.get("marketCap"), okx_price.get("market_cap"))
    price = _num(gmgn_info.get("price"), okx_price.get("price"), okx_price.get("currentPrice"))
    circulating_supply = _num(gmgn_info.get("circulating_supply"), gmgn_info.get("total_supply"), okx_price.get("circulatingSupply"), okx_price.get("totalSupply"))
    if market_cap is None and price is not None and circulating_supply is not None:
        market_cap = price * circulating_supply
    liquidity = _num(gmgn_info.get("liquidity"), _get_nested(gmgn_info, "pool.liquidity"), gmgn_pool.get("liquidity"), okx_price.get("liquidity"), okx_liq.get("liquidityUsd"))
    top10 = _num(gmgn_sec.get("top_10_holder_rate"), gmgn_info.get("top_10_holder_rate"), _get_nested(gmgn_info, "stat.top_10_holder_rate"), okx_adv.get("top10HoldPercent"), okx_adv.get("top10HoldPct"))
    rug_ratio = _num(gmgn_sec.get("rug_ratio"), okx_adv.get("rugPullPercent"), okx_cluster.get("clusterRugPullPercent"))
    creator_hold = str(gmgn_sec.get("creator_token_status") or _get_nested(gmgn_info, "dev.creator_token_status") or "")
    risk_level = str(okx_adv.get("riskControlLevel") or security_scan.get("riskLevel") or "")
    holders_count = _list_len(records.get("gmgn:token_holders", {}).get("parsed", {}))
    traders_count = _list_len(records.get("gmgn:token_traders", {}).get("parsed", {}))
    okx_top_trader_count = _list_len(records.get("okx:top_trader", {}).get("parsed", {}))
    okx_cluster_count = _list_len(records.get("okx:cluster_list", {}).get("parsed", {}))

    has_required_failure = bool(required_failures)
    safety_hard = False
    safety_reasons: list[str] = []
    if str(gmgn_sec.get("is_honeypot", "")).lower() == "yes":
        safety_hard = True; safety_reasons.append("GMGN honeypot=yes")
    if gmgn_sec.get("renounced_mint") is False:
        safety_reasons.append("SOL mint authority not renounced")
    if gmgn_sec.get("renounced_freeze_account") is False:
        safety_reasons.append("SOL freeze authority not renounced")
    if rug_ratio is not None and rug_ratio > 0.3:
        safety_hard = True; safety_reasons.append("rug_ratio > 0.3")
    if "high" in risk_level.lower() or "danger" in risk_level.lower():
        safety_reasons.append("OKX riskControlLevel high/danger")

    market_block = False
    market_reasons: list[str] = []
    if liquidity is not None and liquidity < 10_000:
        market_block = True; market_reasons.append("liquidity < 10K")
    if market_cap is not None and not (50_000 <= market_cap <= 1_500_000):
        market_reasons.append("market_cap outside GMGN V1 watch band")
    if top10 is not None and top10 > 0.5:
        market_block = True; market_reasons.append("top10 holder concentration > 50%")

    stage_outputs = [
        _stage_output(
            "stage_01_candidate_discovery",
            "PASS" if not has_required_failure else "WARN",
            token_address,
            facts={"discovered_at": snapshot.get("manifest", {}).get("created_at") or iso_now(), "symbol": symbol, "collector_mode": "gmgn_okx_readonly_raw"},
            evidence_refs=["gmgn:token_info", "okx:token_search", "okx:price_info"],
            source_skill=["gmgn-token", "okx-dex-token"],
        ),
        _stage_output(
            "stage_02_safety_gate",
            "BLOCK" if safety_hard else ("WARN" if safety_reasons or has_required_failure else "PASS"),
            token_address,
            facts={"safety_status": "SAFETY_BLOCK" if safety_hard else "SAFETY_PASS_OR_WARN", "safety_reasons": safety_reasons},
            stats={"rug_ratio": rug_ratio} if rug_ratio is not None else {},
            evidence_refs=["gmgn:token_security", "okx:advanced_info", "okx:security_token_scan"],
            source_skill=["gmgn-token", "okx-dex-token", "okx-security"],
            counter_evidence=required_failures,
        ),
        _stage_output(
            "stage_03_market_gate",
            "BLOCK" if market_block else ("WARN" if market_reasons or market_cap is None or liquidity is None else "PASS"),
            token_address,
            stats={"market_cap": market_cap, "liquidity_usd": liquidity, "price_usd": price, "top10_holder_rate": top10},
            inference={"market_reasons": market_reasons},
            evidence_refs=["gmgn:token_info", "gmgn:token_pool", "okx:price_info", "okx:liquidity"],
            source_skill=["gmgn-token", "okx-dex-token"],
        ),
        _stage_output(
            "stage_05_early_wallet_analyzer",
            "PASS" if holders_count or traders_count else "INSUFFICIENT_DATA",
            token_address,
            facts={"gmgn_holder_rows": holders_count, "gmgn_trader_rows": traders_count},
            evidence_refs=["gmgn:token_holders", "gmgn:token_traders", "gmgn:holders_transfer_in", "gmgn:holders_bundler", "gmgn:holders_fresh"],
            source_skill=["gmgn-token"],
        ),
        _stage_output(
            "stage_07_holder_cluster",
            "PASS" if okx_cluster_count or okx_cluster else "WARN",
            token_address,
            facts={"okx_cluster_rows": okx_cluster_count},
            inference={"holder_cluster_status": "OKX_CLUSTER_EVIDENCE" if okx_cluster_count or okx_cluster else "OKX_CLUSTER_PENDING_OR_UNAVAILABLE"},
            evidence_refs=["okx:cluster_overview", "okx:cluster_top_holders_10", "okx:cluster_top_holders_50", "okx:cluster_top_holders_100", "okx:cluster_list"],
            source_skill=["okx-dex-token"],
            invalidation_condition="OKX cluster 过期、GMGN 行为反证或资金路径反证出现时失效；单独 cluster 不等于同源确认。",
        ),
        _stage_output(
            "stage_09_chip_distribution_analyzer",
            "PASS" if (holders_count and okx_top_trader_count) else "WARN",
            token_address,
            facts={"gmgn_holder_rows": holders_count, "okx_top_trader_rows": okx_top_trader_count},
            inference={"chip_distribution_status": "DUAL_SOURCE_AVAILABLE" if (holders_count and okx_top_trader_count) else "PARTIAL_SOURCE_ONLY"},
            evidence_refs=["gmgn:token_holders", "gmgn:token_traders", "okx:top_trader", "okx:cluster_list"],
            source_skill=["gmgn-token", "okx-dex-token"],
            invalidation_condition="Top holder/trader 快照变化、清仓、回流或 K线结构破坏时失效。",
        ),
    ]
    for stage in stage_outputs:
        stage["validation"] = validate_stage_output(stage)
    return {
        "token_address": token_address,
        "created_at": iso_now(),
        "field_summary": {
            "symbol": symbol,
            "market_cap": market_cap,
            "liquidity_usd": liquidity,
            "price_usd": price,
            "top10_holder_rate": top10,
            "rug_ratio": rug_ratio,
            "risk_level": risk_level,
            "holders_count": holders_count,
            "traders_count": traders_count,
            "okx_top_trader_count": okx_top_trader_count,
            "okx_cluster_count": okx_cluster_count,
            "required_failures_count": len(required_failures),
        },
        "stage_outputs": stage_outputs,
    }


def run_readonly_adapter_for_token(
    token_address: str,
    *,
    output_root: str | Path,
    limit: int = 50,
    include_kline: bool = False,
    allow_network: bool = True,
) -> dict[str, Any]:
    snapshot = collect_token_raw_snapshot(token_address, output_root=output_root, limit=limit, include_kline=include_kline, allow_network=allow_network)
    mapped = map_raw_snapshot_to_stage_outputs(snapshot)
    root = Path(output_root)
    normalized_dir = root / "wallet_data" / "normalized"
    intelligence_dir = root / "structure_analysis" / "intelligence"
    write_json(normalized_dir / "gmgn_okx_raw_stage_outputs.json", mapped)
    append_jsonl(intelligence_dir / "stage_outputs.jsonl", {"token_address": token_address, "created_at": iso_now(), "stage_outputs": mapped["stage_outputs"]})
    return {"snapshot": snapshot, "mapped": mapped, "stage_outputs_path": str(normalized_dir / "gmgn_okx_raw_stage_outputs.json")}
