"""Wallet Data Guard: anti-contamination submodule for SIKK wallet analysis.

This module protects the existing canonical wallet-analysis system. It is not a
parallel wallet-analysis workflow.
"""

from .contracts import CANONICAL_WALLET_ROUTE, COMPATIBILITY_ROUTES, SemanticLayer, ProducerType
from .write_gate import WriteGateError, validate_write_contract, write_controlled_artifact
from .source_manifest import build_source_manifest, validate_source_manifest
from .contamination_scan import scan_wallet_data_contamination
from .legacy_quarantine import build_legacy_quarantine_index, enrich_contamination_report_with_legacy_quarantine

__all__ = [
    "CANONICAL_WALLET_ROUTE",
    "COMPATIBILITY_ROUTES",
    "SemanticLayer",
    "ProducerType",
    "WriteGateError",
    "validate_write_contract",
    "write_controlled_artifact",
    "build_source_manifest",
    "validate_source_manifest",
    "scan_wallet_data_contamination",
    "build_legacy_quarantine_index",
    "enrich_contamination_report_with_legacy_quarantine",
]
