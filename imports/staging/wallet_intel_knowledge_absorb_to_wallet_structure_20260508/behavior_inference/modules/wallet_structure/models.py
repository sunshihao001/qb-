
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional

@dataclass(slots=True)
class WalletStructureInput:
    token_address: str
    token_symbol: str = ''
    chain: str = 'sol'
    discovery_time: Optional[str] = None
    analysis_time: Optional[str] = None
    analysis_window: str = 'CUSTOM'
    max_wallets: int = 100
    include_holders: bool = True
    include_traders: bool = True
    include_fresh: bool = True
    include_bundler: bool = True
    include_transfer_in: bool = True
    include_smart: bool = True
    include_rat: bool = True
    include_funding_source: bool = False
    include_token_flow: bool = False
    update_history: bool = False
    output_gmgn_notes: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            'token_address': self.token_address,
            'token_symbol': self.token_symbol,
            'chain': self.chain,
            'discovery_time': self.discovery_time,
            'analysis_time': self.analysis_time,
            'analysis_window': self.analysis_window,
            'max_wallets': self.max_wallets,
            'include_holders': self.include_holders,
            'include_traders': self.include_traders,
            'include_fresh': self.include_fresh,
            'include_bundler': self.include_bundler,
            'include_transfer_in': self.include_transfer_in,
            'include_smart': self.include_smart,
            'include_rat': self.include_rat,
            'include_funding_source': self.include_funding_source,
            'include_token_flow': self.include_token_flow,
            'update_history': self.update_history,
            'output_gmgn_notes': self.output_gmgn_notes,
        }

@dataclass(slots=True)
class WalletBundlePaths:
    output_dir: Path
    raw_snapshot_csv: Path
    normalized_csv: Path
    classification_csv: Path
    funding_edges_csv: Path
    token_flow_edges_csv: Path
    same_source_groups_csv: Path
    distribution_paths_csv: Path
    backflow_paths_csv: Path
    gmgn_note_table_csv: Path
    decision_json: Path
    report_md: Path
    manifest_json: Path

    def as_dict(self) -> Dict[str, str]:
        return {k: str(v) for k, v in self.__dict__.items()}

@dataclass(slots=True)
class WalletRoleResult:
    wallet_address: str
    role_name: str
    role_code: str
    evidence_level: str
    risk_level: str
    tracking_level: str
    gmgn_note: str = ''
    note_template: str = ''
    score: float = 0.0
    signals: List[str] = field(default_factory=list)

    def to_row(self) -> Dict[str, Any]:
        return {
            'wallet_address': self.wallet_address,
            'role_name': self.role_name,
            'role_code': self.role_code,
            'evidence_level': self.evidence_level,
            'risk_level': self.risk_level,
            'tracking_level': self.tracking_level,
            'gmgn_note': self.gmgn_note,
            'note_template': self.note_template,
            'score': self.score,
            'signals': '|'.join(self.signals),
        }
