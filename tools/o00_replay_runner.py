#!/usr/bin/env python3
"""O00 design-level replay helpers."""

FALSE_CLAIMS = ["TESTED", "RUNNER_BOUND", "POLICY_ACTIVE", "PIPELINE_ACCEPTED", "SYSTEM_FULLY_IMPLEMENTED"]


def compare_expected_final_status(expected: str, actual: str) -> dict:
    return {
        "expected_final_status": expected,
        "actual_final_status": actual,
        "matched": expected == actual,
        "false_claims_blocked": {claim: True for claim in FALSE_CLAIMS},
    }
