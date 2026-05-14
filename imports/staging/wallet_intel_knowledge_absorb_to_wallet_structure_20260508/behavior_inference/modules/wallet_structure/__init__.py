"""SIKK wallet structure module package."""

from .constants import PACKAGE_NAME, SCHEMA_VERSION, OUTPUT_FILENAMES
from .models import WalletStructureInput, WalletBundlePaths
from .source_reader import collect_wallet_snapshot, default_gmgn_wallet_collector
from .normalizer import normalize_wallet_rows, normalize_wallet_row
from .role_classifier import classify_wallet_rows, classify_wallet_row
from .edge_builder import build_wallet_edges
from .note_generator import generate_gmgn_notes
from .history_store import WalletHistoryStore
from .decision_builder import build_wallet_structure_decision, write_wallet_structure_bundle, build_bundle_from_request
from .quantitative_structure_models import (
    DominantCostZoneResult,
    WalletCostResult,
    StructureInventoryEstimateResult,
    DistributionProgressResult,
    MarkupMotivationResult,
    CounterpartyPressureResult,
    WalletPatternCostAlignmentResult,
)
from .dominant_cost_zone_calculator import calculate_dominant_cost_zone, calculate_wallet_cost, calculate_wallet_costs
from .structure_inventory_calculator import calculate_structure_inventory_estimate
from .distribution_progress_calculator import calculate_distribution_progress
from .markup_motivation_calculator import calculate_markup_motivation
from .counterparty_pressure_calculator import calculate_counterparty_pressure
from .wallet_pattern_cost_alignment_calculator import calculate_wallet_pattern_cost_alignment
from .token_cluster_analyzer import analyze_token_cluster, infer_dominant_lifecycle, classify_dominant_intent
from .quantitative_aggregator import build_quantitative_structure_report, render_quantitative_structure_report_md, write_quantitative_structure_report

__all__ = [
    'PACKAGE_NAME', 'SCHEMA_VERSION', 'OUTPUT_FILENAMES',
    'WalletStructureInput', 'WalletBundlePaths',
    'collect_wallet_snapshot', 'default_gmgn_wallet_collector',
    'normalize_wallet_rows', 'normalize_wallet_row',
    'classify_wallet_rows', 'classify_wallet_row',
    'build_wallet_edges', 'generate_gmgn_notes', 'WalletHistoryStore',
    'build_wallet_structure_decision', 'write_wallet_structure_bundle', 'build_bundle_from_request',
    'DominantCostZoneResult', 'WalletCostResult', 'StructureInventoryEstimateResult',
    'DistributionProgressResult', 'MarkupMotivationResult', 'CounterpartyPressureResult',
    'WalletPatternCostAlignmentResult',
    'calculate_dominant_cost_zone', 'calculate_wallet_cost', 'calculate_wallet_costs',
    'calculate_structure_inventory_estimate', 'calculate_distribution_progress', 'calculate_markup_motivation',
    'calculate_counterparty_pressure', 'calculate_wallet_pattern_cost_alignment',
    'analyze_token_cluster', 'infer_dominant_lifecycle', 'classify_dominant_intent',
    'build_quantitative_structure_report', 'render_quantitative_structure_report_md', 'write_quantitative_structure_report',
]
