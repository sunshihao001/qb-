#!/usr/bin/env python3
"""Generate a human-readable HER_DOC auto-repair route from the highest-cognition task package."""
from __future__ import annotations

import json
from pathlib import Path

BASE = Path('/root/sikk-gmgn/data/her_document_function_system/system_review/trading_system_full_gap_scan_20260514')
SRC = BASE / 'her_doc_auto_repair_task_package_with_highest_cognition.json'
OUT = BASE / 'her_doc_auto_repair_route.md'

data = json.loads(SRC.read_text(encoding='utf-8'))
highest = data['highest_cognition']
tasks = data['tasks']
completeness = data['data_completeness_judgement']

her_direct = [t for t in tasks if t.get('can_her_directly_land')]
gpt_research = [t for t in tasks if t.get('needs_gpt_deep_research')]
blocking = [t for t in tasks if t.get('priority') == 'P0_BLOCKING']

lines = []
lines.append('# HER_DOC 自动化修复路线 / Auto Repair Route')
lines.append('')
lines.append('## 最高认知')
lines.append('')
lines.append(f'> {highest}')
lines.append('')
lines.append('## 当前结论')
lines.append('')
lines.append('- 当前不是“直接分阶段补全文档”的阶段。')
lines.append('- 当前是“HER_DOC 全体系目标差距扫描 → 缺口分流 → 自动化修复任务包 → 验收”的阶段。')
lines.append('- 状态保持：`READY_WITH_GAPS`，不能标记为 `ACCEPTED`，更不能标记为实盘可用。')
lines.append('- 修复方向：优先让真实 token / candidate batch 可以按 P01-P10 产生可追踪证据，而不是继续写漂亮模板。')
lines.append('')
lines.append('## 一、HER 可以直接落地的任务')
lines.append('')
for t in her_direct:
    lines.append(f"### {t['task_id']} — {t['title']}")
    lines.append(f"- 优先级：`{t['priority']}`")
    lines.append(f"- HER_DOC 阶段：`{t['her_doc_stage']}`")
    lines.append(f"- 应用场景：{t['application_scenario']}")
    lines.append('- 目标文件/目录：')
    for p in t.get('target_files', []):
        lines.append(f'  - `{p}`')
    lines.append('- 验收：')
    for a in t.get('acceptance', []):
        lines.append(f'  - {a}')
    lines.append('- 仍缺数据/证据：')
    for m in t.get('still_missing_data_to_judge_complete', []):
        lines.append(f'  - {m}')
    lines.append('')

lines.append('## 二、需要 GPT 深研后再回填的缺口')
lines.append('')
if not gpt_research:
    lines.append('- 暂无。')
else:
    for t in gpt_research:
        lines.append(f"### {t['task_id']} — {t['title']}")
        lines.append(f"- 优先级：`{t['priority']}`")
        lines.append('- 需要 GPT 深研：')
        for q in t.get('gpt_research_needed_for', []):
            lines.append(f'  - {q}')
        lines.append('- 回填位置：')
        for p in t.get('target_files', []):
            lines.append(f'  - `{p}`')
        lines.append('')

lines.append('## 三、P0 阻断项先后顺序')
lines.append('')
for i, t in enumerate(blocking, 1):
    lines.append(f"{i}. `{t['task_id']}` — {t['title']}")
lines.append('')
lines.append('## 四、为什么 R00 现在还不能跑真实 token')
lines.append('')
lines.append('R00/真实 token batch 不能被称为专业化完成，原因不是系统没有方向，而是缺少运行级证据链：')
lines.append('')
for item in completeness['professional_light_institution_standard']['currently_missing_or_partial']:
    lines.append(f'- {item}')
lines.append('')
lines.append('因此当前可运行边界仍然是：`paper-only / observe / read-only quote-security`。')
lines.append('')
lines.append('## 五、专业轻机构级完成标准还需要什么')
lines.append('')
for item in completeness['professional_light_institution_standard']['required']:
    lines.append(f'- {item}')
lines.append('')
lines.append('## 六、下一合法执行顺序')
lines.append('')
lines.append('1. 先落地 `AUTO_REPAIR_001_RUNTIME_RUNNER_REGISTRY`：建立 runner registry 与 phase_runner_binding。')
lines.append('2. 再落地 `AUTO_REPAIR_002_GOAL_CONTEXT_LOADING`：runtime 每轮加载最高认知、总目标、阶段目标、禁区 policy。')
lines.append('3. 再落地 `AUTO_REPAIR_003_PHASE_OUTPUT_INDEX_TRACE`：每阶段输出写 phase_output_index 与 runner_execution_trace。')
lines.append('4. 并行修复 `AUTO_REPAIR_004_WALLET_STRUCTURE_RUNTIME_EVIDENCE`：补 P03-P04 钱包/筹码证据。')
lines.append('5. 再落地 `AUTO_REPAIR_005_HANDOFF_CONSUMPTION_ACCEPTANCE`：五级验收与 handoff consumption。')
lines.append('6. 最后接 `AUTO_REPAIR_006_REVIEW_TO_P10_UPGRADE_LOOP`：P09→P10 受控升级，禁止复盘直接改 live rules。')
lines.append('')
lines.append('## 七、安全边界')
lines.append('')
for k, v in data['safety_boundary'].items():
    lines.append(f'- {k}: `{v}`')
lines.append('')
lines.append('## 八、当前状态')
lines.append('')
lines.append(f"- status: `{data['status']}`")
lines.append(f"- overall_status: `{completeness['overall_status']}`")
lines.append(f"- judgement: {completeness['professional_light_institution_standard']['judgement']}")

OUT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(OUT)
