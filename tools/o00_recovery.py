#!/usr/bin/env python3
"""O00 recovery helper."""

FORBIDDEN_ACTIONS = ["live_runtime", "wallet_signing", "auto_deploy", "production_trading", "execute_real_order"]


def build_recovery_report(run_id: str, reason: str = "manual_recover") -> dict:
    return {
        "status": "RECOVERY_REPORT_GENERATED",
        "run_id": run_id,
        "reason": reason,
        "decision": "RUN_VALIDATE_CONFIG_OR_RERUN_SAMPLE_IN_SAFE_MODE",
        "forbidden_actions": FORBIDDEN_ACTIONS,
    }
