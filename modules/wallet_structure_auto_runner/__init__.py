"""L3 public module wrapper for Wallet Structure auto runner.

This package exposes the long-running read-only Wallet Structure automation
entrypoint while preserving the legacy root script compatibility.
"""
from __future__ import annotations

from sikk_wallet_structure_auto_runner import run_wallet_structure_auto_task
from sikk_wallet_structure_auto_runner import _build_guard_trend_index as build_guard_trend_index

__all__ = [
    'run_wallet_structure_auto_task',
    'build_guard_trend_index',
]
