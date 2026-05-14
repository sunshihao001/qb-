
from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping

class WalletHistoryStore:
    """Lightweight file-based history store for wallet structure profiles.

    No database dependency. Designed for incremental wallet profile updates and
    cross-token reuse checks.
    """

    def __init__(self, base_dir: str | Path):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.base_dir / 'history_index.json'
        self.snapshots_dir = self.base_dir / 'snapshots'
        self.snapshots_dir.mkdir(parents=True, exist_ok=True)

    def _load_json(self, path: Path, default: Any) -> Any:
        if not path.exists():
            return default
        return json.loads(path.read_text(encoding='utf-8'))

    def load_index(self) -> Dict[str, Any]:
        data = self._load_json(self.index_path, {'wallets': {}})
        if not isinstance(data, dict):
            return {'wallets': {}}
        data.setdefault('wallets', {})
        return data

    def update(self, rows: Iterable[Mapping[str, Any]], snapshot_name: str = '') -> Dict[str, Any]:
        index = self.load_index()
        wallets = index.setdefault('wallets', {})
        snapshot_name = snapshot_name or 'latest'
        snapshot_path = self.snapshots_dir / f'{snapshot_name}.json'
        snapshot_rows = []
        for row in rows:
            record = dict(row)
            if is_dataclass(row):
                record = asdict(row)
            wallet = str(record.get('wallet_address') or record.get('address') or '')
            if not wallet:
                continue
            wallets[wallet] = {
                'wallet_address': wallet,
                'token_address': record.get('token_address', ''),
                'token_symbol': record.get('token_symbol', ''),
                'role_name': record.get('role_name', record.get('当前角色', '普通交易钱包')),
                'role_code': record.get('role_code', ''),
                'evidence_level': record.get('evidence_level', record.get('wallet_evidence_level', 'E0')),
                'risk_level': record.get('risk_level', 'R0'),
                'tracking_level': record.get('tracking_level', 'A1'),
                'same_source_group_id': record.get('same_source_group_id', ''),
                'funding_source_address': record.get('funding_source_address', ''),
                'last_seen_snapshot': snapshot_name,
            }
            snapshot_rows.append(record)
        self.index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding='utf-8')
        snapshot_path.write_text(json.dumps(snapshot_rows, ensure_ascii=False, indent=2), encoding='utf-8')
        return {'index_path': str(self.index_path), 'snapshot_path': str(snapshot_path), 'wallet_count': len(wallets)}

    def get(self, wallet_address: str) -> Dict[str, Any]:
        return dict(self.load_index().get('wallets', {}).get(wallet_address, {}))
