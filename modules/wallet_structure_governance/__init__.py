"""Wallet Structure Governance submodule.

Independent governance layer for wallet-structure system standards:
scan -> task package -> runtime adapters -> registry -> integration -> consumption.
"""
from .gap_scanner import scan_wallet_structure_system_gaps, consume_interface_inventory_runtime_adapters
from .runtime_adapters import apply_gap_action
from .registry import build_runtime_adapter_registry
from .integration import integrate_runtime_adapters
from .consumption import consume_runtime_registry
from .cycle import run_governance_cycle
from .maturity_scanner import scan_module_maturity
from modules.module_maturity_governance import (
    build_maturity_design_contract,
    evaluate_capability_maturity,
    write_maturity_design_contract,
)

__all__ = [
    'scan_wallet_structure_system_gaps',
    'consume_interface_inventory_runtime_adapters',
    'apply_gap_action',
    'build_runtime_adapter_registry',
    'integrate_runtime_adapters',
    'consume_runtime_registry',
    'run_governance_cycle',
    'scan_module_maturity',
    'evaluate_capability_maturity',
    'build_maturity_design_contract',
    'write_maturity_design_contract',
]
