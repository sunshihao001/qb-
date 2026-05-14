from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


PHASES = [f"p{idx:02d}" for idx in range(1, 10)]

TASK_LAYERS: List[Dict[str, Any]] = [
    {
        "task_id": "task_0_full_system_bundle_bootstrap",
        "label": "Task 0：全系统任务包自举",
        "phases": [],
        "wave_id": "task_0",
        "mode": "bundle_only_no_business_code",
        "goal": "建立 P01-P09 全阶段任务包、总控协议、状态、审计、gap register。",
        "boundary": "Task 0 不写 P01-P09 业务代码，只建立全阶段任务包与控制协议。",
        "next_on_ready": "task_1_wave_1_p01_p03_foundation_runtime",
    },
    {
        "task_id": "task_1_wave_1_p01_p03_foundation_runtime",
        "label": "Task 1：Wave 1｜P01-P03 基础事实与结构运行",
        "phases": ["p01", "p02", "p03"],
        "wave_id": "wave_01_p01_p03",
        "mode": "code_test_replay_handoff",
        "goal": "运行 P01-P03 基础事实、结构地址、筹码控制代码落地、测试、replay 与 handoff。",
        "boundary": "只允许 paper-only/read-only research；禁止真实交易、签名、广播。",
        "next_on_ready": "task_2_wave_2_p04_p05_scenario_position_runtime",
    },
    {
        "task_id": "task_2_wave_2_p04_p05_scenario_position_runtime",
        "label": "Task 2：Wave 2｜P04-P05 场景与位置运行",
        "phases": ["p04", "p05"],
        "wave_id": "wave_02_p04_p05",
        "mode": "code_test_replay_handoff",
        "goal": "运行 P04-P05 场景识别与结构位置代码落地、测试、replay 与 handoff。",
        "boundary": "继承 Wave1 handoff；禁止用缺失字段推断确定结论。",
        "next_on_ready": "task_3_wave_3_p06_p07_strategy_execution_risk_runtime",
    },
    {
        "task_id": "task_3_wave_3_p06_p07_strategy_execution_risk_runtime",
        "label": "Task 3：Wave 3｜P06-P07 策略与执行风控运行",
        "phases": ["p06", "p07"],
        "wave_id": "wave_03_p06_p07",
        "mode": "code_test_replay_handoff_no_trade",
        "goal": "运行 P06-P07 策略门控与执行风控；只输出候选/风险/禁止项，不执行交易。",
        "boundary": "P06/P07 只能给出 paper decision 与 risk gate；禁止 swap、sign、broadcast。",
        "next_on_ready": "task_4_wave_4_p08_p09_review_upgrade_runtime",
    },
    {
        "task_id": "task_4_wave_4_p08_p09_review_upgrade_runtime",
        "label": "Task 4：Wave 4｜P08-P09 复盘与升级运行",
        "phases": ["p08", "p09"],
        "wave_id": "wave_04_p08_p09",
        "mode": "review_upgrade_package",
        "goal": "运行 P08-P09 复盘学习与系统升级建议包；只产生 review-only upgrade package。",
        "boundary": "P09 不自动改交易策略或上线能力，只生成审计后的升级候选。",
        "next_on_ready": "task_5_full_system_e2e_validation",
    },
    {
        "task_id": "task_5_full_system_e2e_validation",
        "label": "Task 5：Full System E2E 全链路验证",
        "phases": ["p01", "p02", "p03", "p04", "p05", "p06", "p07", "p08", "p09"],
        "wave_id": "full_system_e2e",
        "mode": "full_chain_validation",
        "goal": "验证 P01-P09 handoff、状态继承、missing 传播、hard-negative 继承、审计链完整性。",
        "boundary": "E2E 通过不等同 live-ready，不授权真实资金动作。",
        "next_on_ready": "FULL_SYSTEM_WORKFLOW_V4_READY_OR_READY_WITH_GAPS",
    },
    {
        "task_id": "task_6_patch_regression_loop",
        "label": "Task 6：Patch + Regression 修复回归循环",
        "phases": [],
        "wave_id": "patch_and_regression",
        "mode": "repair_failed_items_and_regression",
        "goal": "专门修复失败项、阻断项与降级项，并回归到失败 wave 或 E2E。",
        "boundary": "只修复已登记 issue；禁止绕过验收、删除旧数据或跳过审计。",
        "next_on_ready": "route_back_to_failed_wave_or_e2e",
    },
]

REQUIRED_CONTROL_FILES = [
    "00_full_bundle_manifest.md",
    "04_stop_condition_protocol.md",
    "15_full_system_acceptance_protocol.md",
    "patch_and_regression_loop.md",
]

TASKBOOK_SUFFIXES = ["stage_data", "code_landing", "acceptance_check"]

QUALITY_TERM_ALIASES = {
    "目标": ["目标"],
    "边界": ["边界", "boundary"],
    "输入": ["输入", "input"],
    "输出": ["输出", "output"],
    "handoff": ["handoff"],
    "状态码": ["状态码", "最终状态", "status"],
    "missing": ["missing"],
    "阻断": ["阻断", "blocking", "REJECTED"],
    "降级": ["降级", "READY_WITH_GAPS"],
    "验收": ["验收", "Acceptance", "检查"],
    "审计": ["审计", "audit"],
}


@dataclass
class WorkflowPaths:
    root: Path

    @property
    def bundle_dir(self) -> Path:
        return self.root / "task_books" / "full_system_runtime_bundle"

    @property
    def generated_dir(self) -> Path:
        return self.bundle_dir / "generated" / "workflow_v4"

    @property
    def audit_dir(self) -> Path:
        return self.root / "reports" / "system_audit"

    @property
    def runtime_dir(self) -> Path:
        return self.root / "runtime_logs" / "full_system_runtime"

    @property
    def handoff_dir(self) -> Path:
        return self.root / "shared_handoff" / "full_system_workflow_v4"


class FullSystemWorkflowV4:
    """HER full-system v4 controller: scan, generate taskbooks, audit, route.

    这是 Task0 后的总协议驱动器：只建立全自动化工作流任务体系与运行状态，
    不执行真实交易、不签名、不广播，也不把 paper replay 宣称为 live-ready。
    """

    def __init__(self, root: str | Path):
        self.paths = WorkflowPaths(Path(root))

    def run(self, *, mode: str = "plan-only") -> Dict[str, Any]:
        started_at = self._now()
        self._ensure_dirs()
        control_files = self._read_control_files()
        gap_register = self._scan_gaps(control_files)
        generated_taskbooks = self._generate_taskbooks(gap_register=gap_register, mode=mode)
        routing = self._route(gap_register)
        final_status = self._final_status(gap_register)
        finished_at = self._now()

        payload: Dict[str, Any] = {
            "workflow_version": "full_system_workflow_v4",
            "mode": mode,
            "started_at": started_at,
            "finished_at": finished_at,
            "final_status": final_status,
            "safety_boundary": {
                "paper_only": True,
                "real_trade_actions": [],
                "signing_enabled": False,
                "broadcast_enabled": False,
                "secret_access": "not_requested_not_used",
            },
            "task_layers": TASK_LAYERS,
            "control_files": control_files,
            "gap_register": gap_register,
            "generated_taskbooks": generated_taskbooks,
            "routing": routing,
        }
        output_paths = self._write_outputs(payload)
        payload.update(output_paths)
        return payload

    def _ensure_dirs(self) -> None:
        for path in [self.paths.generated_dir, self.paths.audit_dir, self.paths.runtime_dir, self.paths.handoff_dir]:
            path.mkdir(parents=True, exist_ok=True)

    def _read_control_files(self) -> List[Dict[str, Any]]:
        records: List[Dict[str, Any]] = []
        for name in REQUIRED_CONTROL_FILES:
            path = self.paths.bundle_dir / name
            if not path.exists():
                records.append({"file": name, "exists": False, "status": "missing", "path": str(path)})
                continue
            text = path.read_text(encoding="utf-8")
            records.append(
                {
                    "file": name,
                    "exists": True,
                    "status": "read",
                    "path": str(path),
                    "chars": len(text),
                    "has_stop_condition": "阻断" in text or "Stop" in text or "stop" in text,
                }
            )
        return records

    def _scan_gaps(self, control_files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        gaps: List[Dict[str, Any]] = []
        for record in control_files:
            if not record["exists"]:
                gaps.append(
                    {
                        "gap_id": "MISSING_CONTROL_FILE_" + record["file"].replace(".", "_").upper(),
                        "severity": "blocking",
                        "target": record["file"],
                        "repair_route": "task_6_patch_regression_loop",
                    }
                )
        for phase in PHASES:
            for suffix in TASKBOOK_SUFFIXES:
                name = f"{phase}_{suffix}.md"
                path = self.paths.bundle_dir / name
                if not path.exists():
                    gaps.append(
                        {
                            "gap_id": f"MISSING_PHASE_TASKBOOK_{phase.upper()}_{suffix.upper()}",
                            "severity": "degraded",
                            "target": name,
                            "repair_route": "task_6_patch_regression_loop",
                        }
                    )
                    continue
                text = path.read_text(encoding="utf-8")
                missing_terms = [
                    term for term, aliases in QUALITY_TERM_ALIASES.items() if not any(alias in text for alias in aliases)
                ]
                if missing_terms:
                    gaps.append(
                        {
                            "gap_id": f"INCOMPLETE_PHASE_TASKBOOK_{phase.upper()}_{suffix.upper()}",
                            "severity": "degraded",
                            "target": name,
                            "missing_terms": missing_terms,
                            "repair_route": "task_6_patch_regression_loop",
                        }
                    )
        return gaps

    def _generate_taskbooks(self, *, gap_register: List[Dict[str, Any]], mode: str) -> List[Dict[str, Any]]:
        generated: List[Dict[str, Any]] = []
        gap_lines = "\n".join(f"- {gap['gap_id']}｜{gap['severity']}｜{gap['target']}" for gap in gap_register) or "- none"
        for layer in TASK_LAYERS:
            path = self.paths.generated_dir / f"{layer['task_id']}.md"
            text = self._render_taskbook(layer, gap_lines=gap_lines, mode=mode)
            path.write_text(text, encoding="utf-8")
            generated.append(
                {
                    "task_id": layer["task_id"],
                    "path": str(path),
                    "status": "generated",
                    "wave_id": layer["wave_id"],
                    "phases": layer["phases"],
                }
            )
        return generated

    def _render_taskbook(self, layer: Dict[str, Any], *, gap_lines: str, mode: str) -> str:
        phase_text = ", ".join(layer["phases"]) if layer["phases"] else "not_applicable"
        return f"""# {layer['label']}

- workflow_version: `full_system_workflow_v4`
- task_id: `{layer['task_id']}`
- wave_id: `{layer['wave_id']}`
- mode: `{mode}`

## 目标
{layer['goal']}

## 边界
{layer['boundary']}
真实交易：禁止。签名：禁止。广播：禁止。密钥读取：禁止。

## 输入
- full_system_runtime_bundle 总控文件
- 对应 P01-P09 stage_data / code_landing / acceptance_check 任务书
- runtime_task_state.json / wave_state.json / checkpoint_state.json
- missing_gap_register 与 workflow_v4_gap_register

## 输出
- 阶段任务书
- 代码骨架任务书
- 验收任务书
- pytest/replay/handoff/audit 结果引用
- runtime state 与 gap register 回填

## phases
{phase_text}

## handoff
- READY：进入 `{layer['next_on_ready']}`
- READY_WITH_GAPS：允许继续但必须继承 gap register
- REJECTED：停止当前 Wave，进入 `task_6_patch_regression_loop`

## 状态码
- READY
- READY_WITH_GAPS
- REJECTED

## missing
缺失字段、缺失文件、缺失证据必须写为 `missing`，不得写空值或系统猜测值。

## 阻断
- required control file missing
- JSON/state 不可解析
- 出现真实交易、签名、广播或密钥读取动作
- 删除/移动旧数据

## 降级
- mock replay / paper-only evidence
- phase taskbook 缺项
- profile/gateway/live collector 未接入

## 验收
- 任务书生成完整
- 状态码可路由
- pytest/replay/handoff/audit 引用存在或明确写 missing
- gap register 已回填
- paper-only 安全边界未破坏

## 审计
审计写入 `reports/system_audit/full_system_workflow_v4_audit.md` 与 JSON 结果。

## 当前 gap register
{gap_lines}
"""

    def _route(self, gap_register: List[Dict[str, Any]]) -> Dict[str, Any]:
        has_blocking = any(gap["severity"] == "blocking" for gap in gap_register)
        has_gap = bool(gap_register)
        if has_blocking:
            return {
                "stop_condition_triggered": True,
                "current_allowed_task": "task_6_patch_regression_loop",
                "next_allowed_task": "task_6_patch_regression_loop",
                "reason": "blocking gaps found; stop current wave and repair",
            }
        if has_gap:
            return {
                "stop_condition_triggered": False,
                "current_allowed_task": "task_6_patch_regression_loop",
                "next_allowed_task": "task_1_wave_1_p01_p03_foundation_runtime_after_regression",
                "reason": "degraded gaps found; route through Patch + Regression before Wave execution",
            }
        return {
            "stop_condition_triggered": False,
            "current_allowed_task": "task_1_wave_1_p01_p03_foundation_runtime",
            "next_allowed_task": "task_1_wave_1_p01_p03_foundation_runtime",
            "reason": "bundle complete; Wave 1 may start under paper-only boundary",
        }

    def _final_status(self, gap_register: List[Dict[str, Any]]) -> str:
        if any(gap["severity"] == "blocking" for gap in gap_register):
            return "FULL_SYSTEM_BUNDLE_REJECTED"
        if gap_register:
            return "FULL_SYSTEM_BUNDLE_READY_WITH_GAPS"
        return "FULL_SYSTEM_BUNDLE_READY"

    def _write_outputs(self, payload: Dict[str, Any]) -> Dict[str, str]:
        result_json = self.paths.audit_dir / "full_system_workflow_v4_result.json"
        audit_md = self.paths.audit_dir / "full_system_workflow_v4_audit.md"
        gap_json = self.paths.audit_dir / "full_system_workflow_v4_gap_register.json"
        runtime_state = self.paths.runtime_dir / "workflow_v4_state.json"
        handoff_json = self.paths.handoff_dir / "workflow_v4_handoff_packet.json"

        result_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        gap_json.write_text(json.dumps(payload["gap_register"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        runtime_state.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        handoff_payload = {
            "workflow_version": payload["workflow_version"],
            "final_status": payload["final_status"],
            "routing": payload["routing"],
            "generated_taskbooks": payload["generated_taskbooks"],
            "gap_register_path": str(gap_json),
            "audit_path": str(audit_md),
        }
        handoff_json.write_text(json.dumps(handoff_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        audit_md.write_text(self._render_audit(payload, gap_json=gap_json, handoff_json=handoff_json), encoding="utf-8")

        return {
            "result_path": str(result_json),
            "audit_path": str(audit_md),
            "gap_register_path": str(gap_json),
            "runtime_state_path": str(runtime_state),
            "handoff_path": str(handoff_json),
            "generated_dir": str(self.paths.generated_dir),
        }

    def _render_audit(self, payload: Dict[str, Any], *, gap_json: Path, handoff_json: Path) -> str:
        lines = [
            "# Full System Workflow v4 Audit",
            "",
            f"- final_status: `{payload['final_status']}`",
            "- boundary: paper-only / no real trade / no signing / no broadcast / no secrets",
            f"- task_layers: `{len(payload['task_layers'])}`",
            f"- generated_taskbooks: `{len(payload['generated_taskbooks'])}`",
            f"- gap_count: `{len(payload['gap_register'])}`",
            f"- routing.current_allowed_task: `{payload['routing']['current_allowed_task']}`",
            f"- routing.next_allowed_task: `{payload['routing']['next_allowed_task']}`",
            "",
            "## 7 Task Layers",
        ]
        for layer in payload["task_layers"]:
            lines.append(f"- {layer['label']}｜`{layer['task_id']}`｜{layer['mode']}")
        lines.extend([
            "",
            "## Gap Register",
            f"- path: `{gap_json}`",
        ])
        if payload["gap_register"]:
            for gap in payload["gap_register"]:
                lines.append(f"- {gap['gap_id']}｜{gap['severity']}｜{gap['target']}｜Patch + Regression")
        else:
            lines.append("- none")
        lines.extend([
            "",
            "## Handoff",
            f"- path: `{handoff_json}`",
            "",
            "## Acceptance",
            "- 自动读取总控：DONE",
            "- 自动扫描阶段缺口：DONE",
            "- 自动生成阶段任务书/代码骨架任务书/验收任务书：DONE",
            "- 自动记录 gap：DONE",
            "- 自动 handoff/audit/runtime state：DONE",
            "- 自动路由下一阶段或 Patch + Regression：DONE",
        ])
        return "\n".join(lines) + "\n"

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run HER full_system_workflow_v4 controller")
    parser.add_argument("--root", default="/root/sikk-gmgn")
    parser.add_argument("--mode", default="plan-only")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = FullSystemWorkflowV4(args.root).run(mode=args.mode)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
