from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


DEFAULT_REGISTRY = {
    "rules": [
        {"code": "DATA_INVALID", "match_status_codes": ["DATA_INVALID"], "block_status_family": "BLOCK", "reason": "数据事实无效"},
        {"code": "SECURITY_RISK_BLOCK", "match_status_codes": ["SECURITY_RISK_BLOCK"], "block_status_family": "BLOCK", "reason": "安全风险硬否决"},
        {"code": "ACTIVE_DISTRIBUTION", "match_status_codes": ["ACTIVE_DISTRIBUTION"], "block_status_family": "BLOCK", "reason": "主动派发硬否决"},
        {"code": "STRUCTURE_COLLAPSE", "match_status_codes": ["STRUCTURE_COLLAPSE"], "block_status_family": "BLOCK", "reason": "结构坍塌硬否决"},
        {"code": "SCENARIO_BLOCK", "match_status_codes": ["SCENARIO_BLOCK"], "block_status_family": "BLOCK", "reason": "场景否决"},
        {"code": "COMPLETION_FAIL", "match_status_codes": ["COMPLETION_FAIL"], "block_status_family": "BLOCK", "reason": "结构位置失败"},
        {"code": "FATIGUE_BLOCK", "match_status_codes": ["FATIGUE_BLOCK"], "block_status_family": "BLOCK", "reason": "疲劳拖延硬否决"},
        {"code": "STRATEGY_BLOCK", "match_status_codes": ["STRATEGY_BLOCK"], "block_status_family": "BLOCK", "reason": "策略门禁否决"},
        {"code": "EXECUTION_BLOCK", "match_status_codes": ["EXECUTION_BLOCK"], "block_status_family": "BLOCK", "reason": "执行风控否决"},
    ]
}


@dataclass
class HardNegativeResult:
    blocked: bool
    trigger: Optional[str] = None
    status_family: str = "ALLOW"
    reason: str = "no_hard_negative"


class HardNegativeEngine:
    def __init__(self, registry: Dict[str, Any] | None = None):
        self.registry = registry or DEFAULT_REGISTRY

    def evaluate(self, state_or_payload: Dict[str, Any]) -> HardNegativeResult:
        status_code = state_or_payload.get("status_code")
        explicit_trigger = state_or_payload.get("hard_negative_trigger")
        for rule in self.registry.get("rules", []):
            if status_code in rule.get("match_status_codes", []) or explicit_trigger == rule.get("code"):
                return HardNegativeResult(
                    blocked=True,
                    trigger=rule.get("code"),
                    status_family=rule.get("block_status_family", "BLOCK"),
                    reason=rule.get("reason", "hard_negative_triggered"),
                )
        return HardNegativeResult(blocked=False)
