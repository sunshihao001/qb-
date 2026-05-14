# SIKK Stable Trader OS Total Control Execution Protocol v2.0

## Core Definition

Phase Controller 不是阶段说明文档。Phase Controller 是一个可调度的阶段运行单元，负责把系统目标拆成阶段目标，把阶段目标拆成任务树，把任务树绑定到输入合约、输出合约、Atomic Skill、代码工具、验收门、状态回写和下游交接包。它不追求一次性给出智能判断，而是保证每一个判断都有字段来源、证据等级、反证记录、失败处理和可复盘路径。

## HER Read Order

1. `00_system_registry/system_manifest.yaml`
2. `00_system_registry/phase_registry.yaml`
3. `00_system_registry/status_code_registry.yaml`
4. `00_system_registry/evidence_registry.yaml`
5. `00_system_registry/hard_negative_registry.yaml`
6. active phase package under `02_phase_controllers/`

## Boundary

Total control routes and validates. It does not add trading logic and does not authorize real trading.
