"""Module Maturity Governance.

HER bottom-level system design module for deciding whether a capability is only functional code (L1), runtime-integrated (L2), or a standalone callable submodule (L3).
"""
from .scanner import (
    CAPABILITY_CATALOG,
    build_maturity_design_contract,
    evaluate_capability_maturity,
    scan_module_maturity,
    write_maturity_design_contract,
)

__all__ = [
    'CAPABILITY_CATALOG',
    'scan_module_maturity',
    'evaluate_capability_maturity',
    'build_maturity_design_contract',
    'write_maturity_design_contract',
]
