
from __future__ import annotations

import csv
import json
import subprocess
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Mapping

from .constants import DEFAULT_CHAIN, DEFAULT_MAX_WALLETS
from .models import WalletStructureInput

WalletCollector = Callable[[str, str], List[Dict[str, Any]]]

def _ensure_readonly_command(command: List[str]) -> None:
    joined = ' '.join(command)
    forbidden = ['swap', 'broadcast', 'sign', 'paper_execute']
    if any(token in joined for token in forbidden):
        raise ValueError(f'wallet structure collector is read-only: {joined}')

def _run_json_command(command: List[str], timeout: int = 90) -> Dict[str, Any]:
    _ensure_readonly_command(command)
    completed = subprocess.run(command, check=True, capture_output=True, text=True, timeout=timeout)
    text = (completed.stdout or '{}').strip() or '{}'
    return json.loads(text)

def _safe_text(row: Mapping[str, Any], *keys: str, default: str = '') -> str:
    for key in keys:
        value = row.get(key)
        if value not in (None, '', [], {}):
            return str(value)
    return default

def default_gmgn_wallet_collector(token_address: str, token_symbol: str = '', chain: str = DEFAULT_CHAIN, max_wallets: int = DEFAULT_MAX_WALLETS) -> List[Dict[str, Any]]:
    """Read-only GMGN snapshot collector.

    Collects holders/traders subsets and merges wallet-level evidence while
    preserving source provenance.
    """
    commands = [
        ['gmgn-cli', 'token', 'holders', '--chain', chain, '--address', token_address, '--limit', str(max_wallets), '--order-by', 'amount_percentage', '--direction', 'desc', '--raw'],
        ['gmgn-cli', 'token', 'traders', '--chain', chain, '--address', token_address, '--limit', str(max_wallets), '--order-by', 'profit', '--direction', 'desc', '--raw'],
        ['gmgn-cli', 'token', 'holders', '--chain', chain, '--address', token_address, '--limit', str(max_wallets), '--tag', 'transfer_in', '--order-by', 'amount_percentage', '--direction', 'desc', '--raw'],
        ['gmgn-cli', 'token', 'holders', '--chain', chain, '--address', token_address, '--limit', str(max_wallets), '--tag', 'bundler', '--order-by', 'amount_percentage', '--direction', 'desc', '--raw'],
        ['gmgn-cli', 'token', 'holders', '--chain', chain, '--address', token_address, '--limit', str(max_wallets), '--tag', 'fresh_wallet', '--order-by', 'amount_percentage', '--direction', 'desc', '--raw'],
        ['gmgn-cli', 'token', 'holders', '--chain', chain, '--address', token_address, '--limit', str(max_wallets), '--tag', 'smart_degen', '--order-by', 'amount_percentage', '--direction', 'desc', '--raw'],
        ['gmgn-cli', 'token', 'holders', '--chain', chain, '--address', token_address, '--limit', str(max_wallets), '--tag', 'rat_trader', '--order-by', 'amount_percentage', '--direction', 'desc', '--raw'],
    ]
    merged: Dict[str, Dict[str, Any]] = {}
    for command in commands:
        payload = _run_json_command(command)
        source_name = '_'.join(command[1:3])
        for row in payload.get('list', []) or []:
            address = _safe_text(row, 'address')
            if not address:
                continue
            current = merged.setdefault(address, dict(row))
            current.setdefault('tags', [])
            current.setdefault('maker_token_tags', [])
            current['tags'] = list({*current.get('tags', []), *row.get('tags', [])})
            current['maker_token_tags'] = list({*current.get('maker_token_tags', []), *row.get('maker_token_tags', [])})
            current.setdefault('source_lists', [])
            current['source_lists'].append(source_name)
        time.sleep(0.25)
    raw_rows = []
    for row in merged.values():
        item = dict(row)
        item.setdefault('token_address', token_address)
        item.setdefault('token_symbol', token_symbol)
        item.setdefault('chain', chain)
        raw_rows.append(item)
    return raw_rows

def collect_wallet_snapshot(request: WalletStructureInput | Mapping[str, Any], collector: WalletCollector = default_gmgn_wallet_collector) -> Dict[str, Any]:
    if isinstance(request, Mapping):
        req = WalletStructureInput(
            token_address=str(request.get('token_address') or ''),
            token_symbol=str(request.get('token_symbol') or ''),
            chain=str(request.get('chain') or DEFAULT_CHAIN),
            discovery_time=request.get('discovery_time'),
            analysis_time=request.get('analysis_time'),
            analysis_window=str(request.get('analysis_window') or 'CUSTOM'),
            max_wallets=int(request.get('max_wallets') or DEFAULT_MAX_WALLETS),
            include_holders=bool(request.get('include_holders', True)),
            include_traders=bool(request.get('include_traders', True)),
            include_fresh=bool(request.get('include_fresh', True)),
            include_bundler=bool(request.get('include_bundler', True)),
            include_transfer_in=bool(request.get('include_transfer_in', True)),
            include_smart=bool(request.get('include_smart', True)),
            include_rat=bool(request.get('include_rat', True)),
            include_funding_source=bool(request.get('include_funding_source', False)),
            include_token_flow=bool(request.get('include_token_flow', False)),
            update_history=bool(request.get('update_history', False)),
            output_gmgn_notes=bool(request.get('output_gmgn_notes', True)),
        )
    else:
        req = request
    rows = collector(req.token_address, req.token_symbol)
    return {
        'request': req.to_dict(),
        'rows': rows,
        'token_address': req.token_address,
        'token_symbol': req.token_symbol,
        'chain': req.chain,
        'analysis_time': req.analysis_time,
        'discovery_time': req.discovery_time,
    }

def write_raw_snapshot_csv(path: str | Path, rows: Iterable[Mapping[str, Any]]) -> str:
    rows = list(rows)
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)
    with p.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return str(p)
