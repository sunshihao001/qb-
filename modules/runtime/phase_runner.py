from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

from .candidate_state import create_candidate_state
from .contract_validator import ContractValidator
from .hard_negative_engine import HardNegativeEngine

PHASE_ALIASES = {
    "phase_00": "phase_00_system_constitution",
    "phase_01": "phase_01_data_fact_layer",
    "phase_02": "phase_02_wallet_structure_layer",
    "phase_03": "phase_03_chip_control_layer",
    "phase_04": "phase_04_scenario_recognition_layer",
    "phase_05": "phase_05_structure_position_layer",
    "phase_06": "phase_06_strategy_gate_layer",
    "phase_07": "phase_07_execution_risk_layer",
    "phase_08": "phase_08_review_learning_layer",
    "phase_09": "phase_09_system_upgrade_layer",
    "phase_00_system_constitution": "phase_00_system_constitution",
    "phase_01_data_fact": "phase_01_data_fact_layer",
    "phase_02_wallet_structure": "phase_02_wallet_structure_layer",
    "phase_03_chip_control": "phase_03_chip_control_layer",
    "phase_04_scenario_recognition": "phase_04_scenario_recognition_layer",
    "phase_05_structure_position": "phase_05_structure_position_layer",
    "phase_06_strategy_gate": "phase_06_strategy_gate_layer",
    "phase_07_execution_risk": "phase_07_execution_risk_layer",
    "phase_08_review_learning": "phase_08_review_learning_layer",
    "phase_09_system_upgrade": "phase_09_system_upgrade_layer",
    "phase_01_data_fact_layer": "phase_01_data_fact_layer",
    "phase_02_wallet_structure_layer": "phase_02_wallet_structure_layer",
    "phase_03_chip_control_layer": "phase_03_chip_control_layer",
    "phase_04_scenario_recognition_layer": "phase_04_scenario_recognition_layer",
    "phase_05_structure_position_layer": "phase_05_structure_position_layer",
    "phase_06_strategy_gate_layer": "phase_06_strategy_gate_layer",
    "phase_07_execution_risk_layer": "phase_07_execution_risk_layer",
    "phase_08_review_learning_layer": "phase_08_review_learning_layer",
    "phase_09_system_upgrade_layer": "phase_09_system_upgrade_layer",
}

PHASE_CONTRACT_ALIASES = {
    "phase_00_system_constitution": ["phase_00_system_constitution", "phase_00"],
    "phase_01_data_fact_layer": ["phase_01_data_fact", "phase_01", "phase_01_data_fact_layer"],
    "phase_02_wallet_structure_layer": ["phase_02_wallet_structure", "phase_02", "phase_02_wallet_structure_layer"],
    "phase_03_chip_control_layer": ["phase_03_chip_control", "phase_03", "phase_03_chip_control_layer"],
    "phase_04_scenario_recognition_layer": ["phase_04_scenario_recognition", "phase_04", "phase_04_scenario_recognition_layer"],
    "phase_05_structure_position_layer": ["phase_05_structure_position", "phase_05", "phase_05_structure_position_layer"],
    "phase_06_strategy_gate_layer": ["phase_06_strategy_gate", "phase_06", "phase_06_strategy_gate_layer"],
    "phase_07_execution_risk_layer": ["phase_07_execution_risk", "phase_07", "phase_07_execution_risk_layer"],
    "phase_08_review_learning_layer": ["phase_08_review_learning", "phase_08", "phase_08_review_learning_layer"],
    "phase_09_system_upgrade_layer": ["phase_09_system_upgrade", "phase_09", "phase_09_system_upgrade_layer"],
}

PHASE_CANONICAL_NAME = {
    "phase_00_system_constitution": "phase_00",
    "phase_01_data_fact_layer": "phase_01",
    "phase_02_wallet_structure_layer": "phase_02",
    "phase_03_chip_control_layer": "phase_03",
    "phase_04_scenario_recognition_layer": "phase_04",
    "phase_05_structure_position_layer": "phase_05",
    "phase_06_strategy_gate_layer": "phase_06",
    "phase_07_execution_risk_layer": "phase_07",
    "phase_08_review_learning_layer": "phase_08",
    "phase_09_system_upgrade_layer": "phase_09",
}

PHASE_FLOW = {
    "phase_00_system_constitution": (None, "phase_01_data_fact_layer", "CONSTITUTION_READY"),
    "phase_01_data_fact_layer": ("phase_00_system_constitution", "phase_02_wallet_structure_layer", "DATA_OK"),
    "phase_02_wallet_structure_layer": ("phase_01_data_fact_layer", "phase_03_chip_control_layer", "WALLET_SUPPORT"),
    "phase_03_chip_control_layer": ("phase_02_wallet_structure_layer", "phase_04_scenario_recognition_layer", "CONTROL_RETAINED"),
    "phase_04_scenario_recognition_layer": ("phase_03_chip_control_layer", "phase_05_structure_position_layer", "SCENARIO_ALLOW"),
    "phase_05_structure_position_layer": ("phase_04_scenario_recognition_layer", "phase_06_strategy_gate_layer", "COMPLETION_PASS"),
    "phase_06_strategy_gate_layer": ("phase_05_structure_position_layer", "phase_07_execution_risk_layer", "PAPER_READY"),
    "phase_07_execution_risk_layer": ("phase_06_strategy_gate_layer", "phase_08_review_learning_layer", "PAPER_EXECUTED"),
    "phase_08_review_learning_layer": ("phase_07_execution_risk_layer", "phase_09_system_upgrade_layer", "REVIEW_ARCHIVED"),
    "phase_09_system_upgrade_layer": ("phase_08_review_learning_layer", None, "UPGRADE_PROPOSED"),
}

PHASE_OUTPUT = {
    "phase_00_system_constitution": "system_constitution.json",
    "phase_01_data_fact_layer": "data_quality_summary.json",
    "phase_02_wallet_structure_layer": "wallet_structure_decision.json",
    "phase_03_chip_control_layer": "chip_control_summary.json",
    "phase_04_scenario_recognition_layer": "primary_scenario.json",
    "phase_05_structure_position_layer": "structure_position_decision.json",
    "phase_06_strategy_gate_layer": "strategy_gate_decision.json",
    "phase_07_execution_risk_layer": "paper_trade_decision.json",
    "phase_08_review_learning_layer": "failure_attribution.json",
    "phase_09_system_upgrade_layer": "rule_update_package.json",
}


@dataclass
class PhaseRunResult:
    status_code: str
    output_path: Path
    audit_path: Path


class PhaseRunner:
    def __init__(self, root: Path | str):
        self.root = Path(root)
        self.validator = ContractValidator()
        self.hard_negative_engine = HardNegativeEngine()

    def run(self, phase: str, mode: str, token: str, input_file: Path | str) -> PhaseRunResult:
        phase = self._normalize_phase(phase)
        previous_phase, next_phase, default_ok_status = PHASE_FLOW[phase]
        input_file = Path(input_file)
        contract = self._resolve_contract(phase)

        validation = self.validator.validate_file(input_file, contract)
        status_code = default_ok_status if validation.ok else validation.status_code

        hard_negative = self.hard_negative_engine.evaluate({
            "status_code": status_code,
            "hard_negative_trigger": validation.hard_negative_trigger,
        })

        hard_negative_trigger = validation.hard_negative_trigger or (hard_negative.trigger if hard_negative.blocked else None)
        gaps = []
        if validation.missing_fields:
            gaps.append("系统推导：输入字段缺失，阶段只能输出 PAUSE/WEAK 状态，不能升级为强通过。")

        canonical_phase = PHASE_CANONICAL_NAME.get(phase, phase)
        out_dir = self.root / "data" / "runtime" / mode / token / canonical_phase
        audit_dir = self.root / "reports" / "runtime" / mode / token / canonical_phase
        out_dir.mkdir(parents=True, exist_ok=True)
        audit_dir.mkdir(parents=True, exist_ok=True)
        output_path = out_dir / PHASE_OUTPUT.get(phase, "phase_output.json")
        audit_path = audit_dir / "audit_report.md"

        state = create_candidate_state(
            token_address=token,
            mode=mode,
            current_phase=phase,
            previous_phase=previous_phase,
            next_phase=next_phase,
            status_code=status_code,
            positive_evidence=validation.positive_evidence,
            negative_evidence=validation.negative_evidence,
            counter_evidence=validation.counter_evidence,
            hard_negative_trigger=hard_negative_trigger,
            missing_fields=validation.missing_fields,
            gaps=gaps,
            audit_refs=[str(audit_path)],
            source_refs=[str(input_file)],
        )
        payload = state.to_dict()
        payload.setdefault("run_id", f"{mode}_{token}")
        payload.setdefault("phase", canonical_phase)
        payload["source_files"] = payload.get("source_refs", [])
        payload["handoff_to"] = next_phase or "FULL_SYSTEM_AUTOMATION_RESULT"
        if hard_negative.blocked:
            payload["status_family"] = "BLOCK"
            payload["hard_negative_reason"] = hard_negative.reason

        output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
        audit_path.write_text(self._audit_text(phase, input_file, contract, payload, validation.ok))

        self._write_canonical_handoff_copy(
            phase=phase,
            token=token,
            output_path=output_path,
        )

        return PhaseRunResult(status_code=status_code, output_path=output_path, audit_path=audit_path)

    def _write_canonical_handoff_copy(self, phase: str, token: str, output_path: Path) -> None:
        canonical_phase = PHASE_CANONICAL_NAME.get(phase, phase)
        if not canonical_phase.startswith("phase_"):
            return
        handoff_name = f"{canonical_phase}_handoff_packet.json"
        runtime_handoff = output_path.parent / handoff_name
        shared_handoff = self.root / "shared_handoff" / canonical_phase / token / handoff_name
        shared_handoff.parent.mkdir(parents=True, exist_ok=True)
        if output_path.name != handoff_name:
            shutil.copyfile(output_path, runtime_handoff)
        else:
            runtime_handoff = output_path
        shutil.copyfile(runtime_handoff, shared_handoff)

    def _normalize_phase(self, phase: str) -> str:
        if phase not in PHASE_ALIASES:
            raise ValueError(f"unknown phase: {phase}")
        return PHASE_ALIASES[phase]

    def _resolve_contract(self, phase: str) -> Path:
        contract_root = self.root / "contracts"
        if not contract_root.exists():
            contract_root = Path(__file__).resolve().parents[2] / "contracts"
        for alias in PHASE_CONTRACT_ALIASES.get(phase, [phase]):
            contract = contract_root / alias / "input_contract.json"
            if contract.exists():
                return contract
        canonical = PHASE_CONTRACT_ALIASES.get(phase, [phase])[0]
        return contract_root / canonical / "input_contract.json"

    def _audit_text(self, phase: str, input_file: Path, contract: Path, payload: Dict, validation_ok: bool) -> str:
        return "\n".join([
            f"# {phase} audit_report",
            "",
            "## 执行顺序",
            "- 读取输入：完成",
            f"- 输入文件：`{input_file}`",
            "- 校验字段：完成" if validation_ok else "- 校验字段：发现缺口或无效输入",
            f"- 合约文件：`{contract}`",
            "- 识别缺口：完成",
            "- 运行正向规则：完成",
            "- 运行反证规则：完成",
            "- 检查硬否决：完成",
            "- 生成状态码：完成",
            "- 写输出文件：完成",
            "- 写审计报告：完成",
            "- 交给下一阶段：完成" if payload.get("next_phase") else "- 交给下一阶段：无下游阶段",
            "",
            "## 状态",
            f"- status_code: `{payload.get('status_code')}`",
            f"- status_family: `{payload.get('status_family')}`",
            f"- hard_negative_trigger: `{payload.get('hard_negative_trigger')}`",
            f"- missing_fields: `{payload.get('missing_fields')}`",
            "",
            "## 证据链",
            f"- positive_evidence: `{payload.get('positive_evidence')}`",
            f"- negative_evidence: `{payload.get('negative_evidence')}`",
            f"- counter_evidence: `{payload.get('counter_evidence')}`",
        ])


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Stable Trader OS canonical phase replay runner")
    parser.add_argument("--root", default=".")
    parser.add_argument("--phase", required=True)
    parser.add_argument("--mode", default="replay")
    parser.add_argument("--token", required=True)
    parser.add_argument("--replay", required=True, help="Input/replay fixture file")
    args = parser.parse_args(argv)

    result = PhaseRunner(args.root).run(args.phase, args.mode, args.token, args.replay)
    canonical = (
        "python3 -m modules.runtime.phase_runner "
        f"--phase {args.phase} --replay {args.replay} --mode {args.mode} --token {args.token}"
    )
    print(f"canonical_command={canonical}")
    print(f"status_code={result.status_code}")
    print(f"output_path={result.output_path}")
    print(f"audit_path={result.audit_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
