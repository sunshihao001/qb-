from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class ValidationResult:
    ok: bool
    status_code: str
    missing_fields: List[str] = field(default_factory=list)
    positive_evidence: List[Dict[str, Any]] = field(default_factory=list)
    negative_evidence: List[Dict[str, Any]] = field(default_factory=list)
    counter_evidence: List[Dict[str, Any]] = field(default_factory=list)
    hard_negative_trigger: Optional[str] = None
    payload: Dict[str, Any] = field(default_factory=dict)


class ContractValidator:
    """Minimal contract validator for HER runtime phases.

    Contract format supports:
    {
      "required_fields": ["token_address", ...]
    }
    """

    def validate_file(self, payload_path: Path | str, contract_path: Path | str) -> ValidationResult:
        payload_path = Path(payload_path)
        contract_path = Path(contract_path)

        if not payload_path.exists():
            return ValidationResult(
                ok=False,
                status_code="DATA_INVALID",
                missing_fields=[str(payload_path)],
                negative_evidence=[{"field": "input_file", "reason": "missing", "path": str(payload_path)}],
                counter_evidence=[{"rule": "input_file_missing"}],
                hard_negative_trigger="INPUT_FILE_MISSING",
            )
        if not contract_path.exists():
            return ValidationResult(
                ok=False,
                status_code="DATA_INVALID",
                missing_fields=[str(contract_path)],
                negative_evidence=[{"field": "input_contract", "reason": "missing", "path": str(contract_path)}],
                counter_evidence=[{"rule": "input_contract_missing"}],
                hard_negative_trigger="INPUT_CONTRACT_MISSING",
            )

        try:
            payload = json.loads(payload_path.read_text())
            contract = json.loads(contract_path.read_text())
        except json.JSONDecodeError as exc:
            return ValidationResult(
                ok=False,
                status_code="DATA_INVALID",
                negative_evidence=[{"field": "json", "reason": "invalid_json", "error": str(exc)}],
                counter_evidence=[{"rule": "invalid_json"}],
                hard_negative_trigger="INVALID_JSON",
            )

        required = contract.get("required_fields", [])
        missing = [field for field in required if field not in payload]
        positive = [{"field": field, "reason": "present"} for field in required if field in payload]
        negative = [{"field": field, "reason": "missing"} for field in missing]

        if missing:
            return ValidationResult(
                ok=False,
                status_code="DATA_WEAK",
                missing_fields=missing,
                positive_evidence=positive,
                negative_evidence=negative,
                counter_evidence=[{"rule": "required_field_missing", "fields": missing}],
                payload=payload,
            )

        return ValidationResult(
            ok=True,
            status_code="DATA_OK",
            positive_evidence=positive or [{"field": "contract", "reason": "no_required_fields_or_all_present"}],
            payload=payload,
        )
