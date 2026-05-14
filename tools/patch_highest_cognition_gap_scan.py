#!/usr/bin/env python3
"""Patch HER full-system scan artifacts with the SIKK highest cognition preamble and an executable repair task package.

Safe local artifact updater. It does not touch trading execution paths and does not run swaps.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BASE = Path('/root/sikk-gmgn/data/her_document_function_system/system_review/trading_system_full_gap_scan_20260514')
HIGHEST_COGNITION = (
    '最高认知： SIKK 交易结构系统的目标不是生成流程图，也不是把每个阶段文档写漂亮。 '
    '最终目标是： 让真实 token / candidate batch 在 HER 总控闭环下， '
    '按 P01-P10 完成事实采集、钱包结构推理、筹码结构推理、证据与反证控制、场景识别、策略门禁、paper-only 执行风控、P09 复盘回放、P10 受控升级。 '
    '所以当前正确选择不是直接分阶段补全， 而是先使用 HER_DOC-skill 对全体系做目标差距扫描， '
    '找出总目标还差什么、每个阶段还差什么、R00 为什么还不能跑真实 token、哪些缺口需要 GPT 深研、哪些缺口可以 HER 直接落地。 '
    '流程不是目的。 流程是为了让代币判断不跳步、不硬猜、可反证、可验收、可回放、可升级。'
)
GENERATED_AT = datetime.now(timezone.utc).isoformat()

AUTO_REPAIR_TASKS = [
    {
        'task_id': 'AUTO_REPAIR_001_RUNTIME_RUNNER_REGISTRY',
        'title': '建立 R00/07_runners 运行器注册与 P01-P10 phase_runner_binding',
        'her_doc_stage': 'F00→V00→A00→H00',
        'application_scenario': '每轮 sikk_live_run.py 或 fixed candidate batch 运行前，总控可根据 phase_runner_binding 判断哪个 runner 可合法执行。',
        'can_her_directly_land': True,
        'needs_gpt_deep_research': False,
        'target_files': [
            'sikk_stable_trader_os/07_runners/runner_registry.yaml',
            'sikk_stable_trader_os/07_runners/phase_runner_binding.yaml',
            'sikk_stable_trader_os/07_runners/runner_failure_policy.yaml',
            'sikk_stable_trader_os/07_runners/validation_runner_registry.yaml',
        ],
        'acceptance': ['文件级 PASS', '结构级 PASS', 'runner 不得绕过 Phase Controller', '仍为 paper-only'],
        'still_missing_data_to_judge_complete': ['真实 token batch 下每个 phase runner 的运行证据', 'runner 输出与 phase_output_index 的消费证据'],
        'priority': 'P0_BLOCKING',
    },
    {
        'task_id': 'AUTO_REPAIR_002_GOAL_CONTEXT_LOADING',
        'title': '补 runtime goal context loading 与 goal consumption report',
        'her_doc_stage': 'F00→V00→A00',
        'application_scenario': '每轮 runtime 读取 operator_goal、phase_goal、methodology_goal、acceptance_goal、forbidden_action_policy，并写 consumption report。',
        'can_her_directly_land': True,
        'needs_gpt_deep_research': False,
        'target_files': [
            'sikk_stable_trader_os/00_control/runtime_goal_context.schema.json',
            'sikk_stable_trader_os/00_trace/goal_consumption_report.schema.json',
            'modules/her_runtime_bridge/goal_context_loader.py',
        ],
        'acceptance': ['goal→phase→runner→artifact→acceptance 可追踪', '缺 goal 时降级 READY_WITH_GAPS，不假装 ACCEPTED'],
        'still_missing_data_to_judge_complete': ['runtime 实际调用记录', '每轮 token/candidate run_id 的 goal consumption JSON'],
        'priority': 'P0_BLOCKING',
    },
    {
        'task_id': 'AUTO_REPAIR_003_PHASE_OUTPUT_INDEX_TRACE',
        'title': '补 phase_output_index 与 runner_execution_trace 自动写入',
        'her_doc_stage': 'F00→V00→A00→H00',
        'application_scenario': '每个 P01-P10 阶段输出后写入统一索引和 trace，dashboard/验收/复盘都读这一层。',
        'can_her_directly_land': True,
        'needs_gpt_deep_research': False,
        'target_files': [
            'sikk_stable_trader_os/00_control/phase_output_index.json',
            'sikk_stable_trader_os/00_trace/runner_execution_trace.yaml',
            'modules/her_runtime_bridge/phase_output_indexer.py',
        ],
        'acceptance': ['每个 token/run_id 有 phase_id、runner_id、input_ref、output_ref、status、evidence_level', '索引失败不得影响 paper-only 主流程'],
        'still_missing_data_to_judge_complete': ['真实 runtime 输出路径覆盖率', '失败重试/恢复 trace'],
        'priority': 'P0_BLOCKING',
    },
    {
        'task_id': 'AUTO_REPAIR_004_WALLET_STRUCTURE_RUNTIME_EVIDENCE',
        'title': '修复/接通 P03-P04 钱包结构与筹码结构 runtime evidence',
        'her_doc_stage': 'F00→V00→A00',
        'application_scenario': '真实 token/candidate batch 必须有钱包实体、同源组、资金路径、筹码库存、派发进度、主导侧成本区 evidence。',
        'can_her_directly_land': True,
        'needs_gpt_deep_research': True,
        'gpt_research_needed_for': ['钱包角色字段全集', '同源组/资金路径反证规则', '主导侧成本区与派发进度计算模型', '筹码库存可信度等级'],
        'target_files': [
            'data/gmgn_candidates_live_run/wallet_structure/',
            'data/gmgn_candidates_live_run/intel-bot/logs/wallet_structure/',
            'modules/wallet_structure/',
            'sikk_stable_trader_os/00_data/wallet_structure_field_contract.yaml',
        ],
        'acceptance': ['P03/P04 不能只靠空目录或摘要', 'WALLET_SUPPORT 不等于买入信号', '缺钱包事实时 P07 不得 PAPER_READY'],
        'still_missing_data_to_judge_complete': ['最新 live run 的 wallet_structure summary 是否存在', 'GMGN wallet facts 原始来源质量', '筹码字段覆盖率'],
        'priority': 'P0_BLOCKING',
    },
    {
        'task_id': 'AUTO_REPAIR_005_HANDOFF_CONSUMPTION_ACCEPTANCE',
        'title': '补 P01-P10 handoff consumption status 与消费级/运行级 acceptance runner',
        'her_doc_stage': 'V00→A00→H00',
        'application_scenario': '上游阶段输出只有被下游正式读取并产出消费证据后，才允许从 READY_WITH_GAPS 升级。',
        'can_her_directly_land': True,
        'needs_gpt_deep_research': False,
        'target_files': [
            'sikk_stable_trader_os/09_handoff/handoff_consumption_status.json',
            'sikk_stable_trader_os/08_acceptance/runtime_acceptance_rules.yaml',
            'modules/her_runtime_bridge/runtime_acceptance_runner.py',
        ],
        'acceptance': ['五级验收完整输出：文件/结构/语义/消费/运行', '禁止把 READY_WITH_GAPS 说成 ACCEPTED'],
        'still_missing_data_to_judge_complete': ['downstream_executed=true 的实际证据', '每阶段消费失败原因'],
        'priority': 'P0_BLOCKING',
    },
    {
        'task_id': 'AUTO_REPAIR_006_REVIEW_TO_P10_UPGRADE_LOOP',
        'title': '绑定 P09 复盘回放 → P10 受控升级候选 → shadow validation → approval package',
        'her_doc_stage': 'U00→G00→A00',
        'application_scenario': 'paper failure attribution 不直接改规则，而是生成升级候选、回滚计划、shadow 验证和人工审批包。',
        'can_her_directly_land': True,
        'needs_gpt_deep_research': True,
        'gpt_research_needed_for': ['失败归因分类标准', 'shadow validation 样本设计', '规则升级收益/风险评估模型'],
        'target_files': [
            'sikk_stable_trader_os/02_phase_controllers/P10_self_upgrade/',
            'sikk_stable_trader_os/00_governance/review_to_upgrade_policy.yaml',
            'data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl',
        ],
        'acceptance': ['review result 不得直接 mutate live rules', 'P10 只产出候选/审批/回滚/shadow 证据'],
        'still_missing_data_to_judge_complete': ['足够 paper closed cases', '失败样本 replay 结果', 'shadow validation 通过率'],
        'priority': 'P1_HIGH',
    },
]

DATA_COMPLETENESS_JUDGEMENT = {
    'overall_status': 'NOT_COMPLETE_READY_WITH_GAPS',
    'professional_light_institution_standard': {
        'required': [
            '真实 token/candidate batch 每轮 P01-P10 分阶段输出',
            '每阶段 required fields + source + evidence_level + missing_policy',
            '钱包结构与筹码结构原始事实、推理证据、反证证据',
            '策略门禁与 paper-only 执行风控的可追踪 ticket',
            'P09/P10 review-upgrade 闭环证据',
        ],
        'currently_missing_or_partial': [
            'R00/07_runners 未完整建立',
            'runtime goal context loading 未完整接入',
            'phase_output_index / runner_execution_trace 未自动化',
            'P01-P10 handoff consumption 未完整证明',
            'wallet_structure runtime evidence 缺失/未接通',
            '消费级/运行级 acceptance runner 缺失或未落地',
        ],
        'judgement': '现在不能称为专业化完成，只能称为已具备系统骨架与 paper runtime，正在进入 R00 收编和数据完整性补全阶段。',
    },
}

def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))

def dump_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def ensure_meta_dict(data: Any) -> dict:
    if isinstance(data, dict):
        return data
    return {'items': data}

# Patch JSON artifacts with front meta.
for name in ['gpt_research_request_pack.json', 'full_trading_system_gap_matrix.json', 'stage_goal_preparation_gap_report.json']:
    p = BASE / name
    data = load_json(p)
    if isinstance(data, dict) and data.get('highest_cognition') == HIGHEST_COGNITION:
        continue
    wrapped = ensure_meta_dict(data)
    wrapped = {
        'highest_cognition': HIGHEST_COGNITION,
        'generated_or_patched_at': GENERATED_AT,
        'operating_principle': '先 HER_DOC 全体系目标差距扫描，再区分 GPT 深研 / HER 直接落地 / 数据未完善项；不直接分阶段堆文档。',
        'auto_repair_task_package': AUTO_REPAIR_TASKS,
        'data_completeness_judgement': DATA_COMPLETENESS_JUDGEMENT,
        **wrapped,
    }
    dump_json(p, wrapped)

# Patch methodology summary.
p = BASE / 'methodology_total_goal_gap_summary.json'
data = load_json(p)
data['highest_cognition'] = HIGHEST_COGNITION
data['generated_or_patched_at'] = GENERATED_AT
data['auto_repair_task_package'] = AUTO_REPAIR_TASKS
data['data_completeness_judgement'] = DATA_COMPLETENESS_JUDGEMENT
dump_json(p, data)

# Write standalone task package.
dump_json(BASE / 'her_doc_auto_repair_task_package_with_highest_cognition.json', {
    'highest_cognition': HIGHEST_COGNITION,
    'generated_at': GENERATED_AT,
    'status': 'READY_WITH_GAPS_AUTO_REPAIR_PACKAGE_READY',
    'goal': '把 HER_DOC 全体系缺口扫描转成可自动落地的修复任务包，并标出 GPT 深研项与数据未完善项。',
    'tasks': AUTO_REPAIR_TASKS,
    'data_completeness_judgement': DATA_COMPLETENESS_JUDGEMENT,
    'safety_boundary': {
        'paper_only': True,
        'no_real_swap': True,
        'no_private_key': True,
        'no_signing': True,
        'no_broadcast': True,
        'ready_with_gaps_not_accepted': True,
    },
})

# Patch markdown report at top.
mdp = BASE / 'full_gap_scan_report.md'
md = mdp.read_text(encoding='utf-8')
if HIGHEST_COGNITION not in md[:3000]:
    preamble = f"# 最高认知 / Highest Cognition\n\n> {HIGHEST_COGNITION}\n\n## 本轮处理原则\n\n- 先使用 HER_DOC-skill 对全体系做目标差距扫描。\n- 再判断：哪些缺口需要 GPT 深研、哪些可以 HER 直接落地、哪些数据仍未完善全面。\n- 自动化修复优先级不是写漂亮文档，而是让真实 token / candidate batch 能按 P01-P10 产生证据、反证、验收、回放与受控升级。\n- 当前状态必须保持 `READY_WITH_GAPS`，不能冒充 `ACCEPTED` 或实盘可用。\n\n"
    mdp.write_text(preamble + md, encoding='utf-8')

# Patch verification.
p = BASE / 'her_doc_full_gap_scan_verification.json'
ver = load_json(p)
ver['highest_cognition_present'] = True
ver['highest_cognition'] = HIGHEST_COGNITION
ver['patched_at'] = GENERATED_AT
ver['auto_repair_task_package'] = str(BASE / 'her_doc_auto_repair_task_package_with_highest_cognition.json')
ver['status'] = 'PASS_READY_WITH_GAPS_HIGHEST_COGNITION_PATCHED'
ver['ready_for_production'] = False
ver['no_real_trade_side_effects'] = True
dump_json(p, ver)

print(json.dumps({
    'status': 'patched',
    'base': str(BASE),
    'patched_files': [
        'gpt_research_request_pack.json',
        'full_trading_system_gap_matrix.json',
        'stage_goal_preparation_gap_report.json',
        'methodology_total_goal_gap_summary.json',
        'full_gap_scan_report.md',
        'her_doc_full_gap_scan_verification.json',
        'her_doc_auto_repair_task_package_with_highest_cognition.json',
    ],
    'tasks': len(AUTO_REPAIR_TASKS),
}, ensure_ascii=False, indent=2))
