# HER_DOC_FUNCTION_PIPELINE_RUNNABLE_WITH_GAPS

## HER 文档到功能自动化落实系统：主链路可运行版 v1.0

这一步不再继续拆复杂子阶段。当前目标只有一个：

```text
让真实 GPT 研究资料 / 系统建设资料进入 HER，
按主链路跑完，
生成完整文件输出，
保留 gap，
形成可验收、可复盘、可继续升级的结果。
```

最终状态：

```text
HER_DOC_FUNCTION_PIPELINE_RUNNABLE_WITH_GAPS
```

它不是最终成熟系统，也不是生产系统。它代表：

```text
主链路已经可运行；
真实文档可以进入；
系统可以输出 K00/F00/V00/A00/H00/U00/G00/O00 文件；
但仍然保留 gap，等待后续根据真实运行结果修复。
```

---

# 1. 当前阶段定位

## 1.1 正确目标

```yaml
phase_id: HER_DOC_FUNCTION_PIPELINE_RUNNABLE
status_code: HER_DOC_FUNCTION_PIPELINE_RUNNABLE_WITH_GAPS
mode: SAFE_MODE_ONLY
trigger: MANUAL_TRIGGER_ONLY
main_goal: real_document_to_function_pipeline
```

本阶段要实现：

```text
真实文档输入
→ K00 文档摄取与任务化
→ F00 功能落实映射
→ V00 验证与缺口识别
→ A00 总验收
→ H00 下游队列
→ U00 复盘升级
→ G00 治理候选
→ O00 总控报告
```

## 1.2 暂停的旁支

当前暂停：

```text
scheduler manual enable
operator confirmation packet
one-shot trial
long-run scheduler
paper runtime
live runtime
production readiness
复杂 dashboard
复杂 bot 自动化
```

这些以后根据真实运行结果再接，不在当前阶段继续扩展。

---

# 2. 主链路总结构

```text
HER_DOC_FUNCTION_PIPELINE_RUNNABLE_WITH_GAPS

input/
  raw_document.md
  operator_goal.json

K00/
  文档摄取
  文档护照
  语料索引
  系统映射
  K00 handoff

F00/
  功能映射
  功能资产
  实现任务包
  F00 handoff

V00/
  验证矩阵
  缺口注册表
  证据报告
  V00 handoff

A00/
  验收矩阵
  readiness certificate
  acceptance result

H00/
  downstream queue
  routing decision
  handoff packets

U00/
  review cases
  root cause analysis
  upgrade queue
  learning index

G00/
  governance candidates
  policy rules update

O00/
  run summary
  final report
  trace
  audit
```

---

# 3. 必须建立的目录

## 3.1 系统定义目录

```text
/root/sikk-gmgn/system/her_doc_function_pipeline/
  01_pipeline_manifest.yaml
  02_pipeline_context_pack.md
  03_pipeline_input_contract.json
  04_pipeline_output_contract.json
  05_pipeline_execution_protocol.md
  06_pipeline_acceptance_gate.yaml
  07_pipeline_state.json
  08_pipeline_handoff.schema.json
  09_status_code_policy.yaml
  10_forbidden_action_policy.yaml
  11_trace_audit_spec.yaml
  12_recovery_policy.md
  13_final_report_template.md
```

## 3.2 运行输出目录

```text
/root/sikk-gmgn/data/her_document_function_system/runs/<run_id>/
  input/
  k00/
  f00/
  v00/
  a00/
  h00/
  u00/
  g00/
  o00/
  trace.jsonl
  audit.jsonl
  recovery/
```

---

# 4. 必须建立的工具文件

```text
/root/sikk-gmgn/tools/
  o00_run_document_main.py
  k00_document_intake.py
  f00_function_mapping.py
  v00_validation_evidence.py
  a00_acceptance.py
  h00_downstream_queue.py
  u00_review_upgrade.py
  g00_governance_update.py
  her_pipeline_status.py
```

## 4.1 工具职责

|工具|职责|
|---|---|
|`o00_run_document_main.py`|主入口，总控 K00→F00→V00→A00→H00→U00→G00|
|`k00_document_intake.py`|保存 raw、生成 document passport、corpus index、system mapping|
|`f00_function_mapping.py`|把解释性资料转成功能落实项、资产清单、任务包|
|`v00_validation_evidence.py`|验证字段、合约、输出、缺口、证据|
|`a00_acceptance.py`|总验收，生成 READY / READY_WITH_GAPS / BLOCKED|
|`h00_downstream_queue.py`|根据 gap / task / handoff 生成下游队列|
|`u00_review_upgrade.py`|复盘 gap，生成 root cause 与 upgrade queue|
|`g00_governance_update.py`|提取治理候选、状态规则、禁止动作规则|
|`her_pipeline_status.py`|查询 run 状态和关键输出|

---

# 5. 输入合约

## `03_pipeline_input_contract.json`

```json
{
  "phase_id": "HER_DOC_FUNCTION_PIPELINE_RUNNABLE",
  "required_inputs": {
    "document": {
      "required": true,
      "description": "真实 GPT 研究资料、系统建设资料或方法论文档"
    },
    "operator_goal": {
      "required": true,
      "description": "本次文档希望落实到系统中的目标"
    },
    "repo_root": {
      "required": true,
      "default": "/root/sikk-gmgn"
    },
    "output_dir": {
      "required": true,
      "description": "本次 run 输出目录"
    },
    "safe_mode": {
      "required": true,
      "must_equal": true
    }
  },
  "optional_inputs": {
    "controller_registry": {
      "required": false,
      "description": "如已存在则读取，不存在则生成基础版本"
    },
    "pipeline_config": {
      "required": false,
      "description": "如已存在则读取，不存在则使用 safe-mode 默认配置"
    }
  },
  "forbidden_inputs": [
    "wallet_private_key",
    "live_runtime_request",
    "auto_deploy_request",
    "production_trading_request",
    "wallet_signing_request"
  ]
}
```

---

# 6. 输出合约

## `04_pipeline_output_contract.json`

```json
{
  "phase_id": "HER_DOC_FUNCTION_PIPELINE_RUNNABLE",
  "required_outputs": {
    "input_raw_document": "input/raw_document.md",
    "input_operator_goal": "input/operator_goal.json",

    "k00_document_passport": "k00/document_passport.json",
    "k00_corpus_index": "k00/corpus_index.json",
    "k00_system_mapping": "k00/system_mapping.json",
    "k00_handoff_packet": "k00/k00_handoff_packet.json",

    "f00_function_mapping": "f00/function_mapping.json",
    "f00_required_system_assets": "f00/required_system_assets.json",
    "f00_implementation_task_package": "f00/implementation_task_package.json",
    "f00_handoff_packet": "f00/f00_handoff_packet.json",

    "v00_validation_matrix": "v00/validation_matrix.json",
    "v00_gap_register": "v00/gap_register.json",
    "v00_evidence_report": "v00/evidence_report.json",
    "v00_handoff_packet": "v00/v00_handoff_packet.json",

    "a00_acceptance_matrix": "a00/acceptance_matrix.json",
    "a00_readiness_certificate": "a00/readiness_certificate.json",
    "a00_acceptance_result": "a00/a00_acceptance_result.json",

    "h00_downstream_queue": "h00/downstream_queue.json",
    "h00_routing_decision": "h00/routing_decision.json",
    "h00_handoff_packets": "h00/h00_handoff_packets.json",

    "u00_review_cases": "u00/review_cases.json",
    "u00_root_cause_analysis": "u00/root_cause_analysis.json",
    "u00_upgrade_queue": "u00/upgrade_queue.json",
    "u00_learning_index": "u00/learning_index.json",

    "g00_governance_candidates": "g00/governance_candidates.json",
    "g00_policy_rules_update": "g00/policy_rules_update.json",

    "o00_run_summary": "o00/run_summary.json",
    "o00_final_report": "o00/final_report.md",

    "trace_log": "trace.jsonl",
    "audit_log": "audit.jsonl"
  }
}
```

---

# 7. 每个阶段必须做什么

## 7.1 K00：文档摄取与任务化

### 目标

K00 不能只保存文档，必须把文档变成系统可处理对象。

### 必须输出

```text
k00/document_passport.json
k00/corpus_index.json
k00/system_mapping.json
k00/k00_handoff_packet.json
```

### `document_passport.json`

```json
{
  "doc_id": "doc_<timestamp>",
  "source_name": "raw_document.md",
  "source_type": "SYSTEM_CONSTRUCTION_MATERIAL",
  "received_at": "",
  "raw_path": "input/raw_document.md",
  "document_role": {
    "primary_role": "system_building_material",
    "secondary_roles": [
      "methodology",
      "controller_design",
      "function_realization",
      "validation_or_governance"
    ]
  },
  "summary": {
    "core_intent": "",
    "key_points": []
  },
  "system_mapping": {
    "affected_planes": [],
    "affected_controllers": [],
    "affected_outputs": []
  },
  "status": "K00_READY_WITH_GAPS"
}
```

### K00 验收标准

```text
1. raw_document.md 已保存。
2. document_passport.json 存在。
3. corpus_index.json 存在。
4. system_mapping.json 存在。
5. k00_handoff_packet.json 存在。
6. 不能只保存 raw 就标记完成。
```

---

## 7.2 F00：功能落实映射

### 目标

F00 是当前系统最关键部分。它要解决：

```text
GPT 里的解释性资料，如何转成功能、字段、文件、命令、测试、验收。
```

### 必须输出

```text
f00/function_mapping.json
f00/required_system_assets.json
f00/implementation_task_package.json
f00/f00_handoff_packet.json
```

### `function_mapping.json`

```json
{
  "mapping_id": "f00_mapping_<timestamp>",
  "source_doc_id": "",
  "functional_intent": "",
  "mapped_functions": [
    {
      "function_id": "func_001",
      "function_name": "",
      "description": "",
      "target_controller": "",
      "required_inputs": [],
      "required_outputs": [],
      "required_fields": [],
      "required_files": [],
      "required_tools": [],
      "validation_needed": true,
      "implementation_status": "TASK_REQUIRED"
    }
  ],
  "unmapped_items": [],
  "status": "F00_FUNCTION_MAPPING_READY_WITH_GAPS"
}
```

### `required_system_assets.json`

```json
{
  "assets": [
    {
      "asset_id": "asset_001",
      "asset_type": "tool",
      "path": "tools/<tool_name>.py",
      "purpose": "",
      "required_by": "",
      "status": "TO_BE_CREATED_OR_UPDATED"
    },
    {
      "asset_id": "asset_002",
      "asset_type": "schema",
      "path": "system/her_doc_function_pipeline/<schema>.json",
      "purpose": "",
      "status": "TO_BE_CREATED_OR_UPDATED"
    }
  ]
}
```

### F00 验收标准

```text
1. 解释性文档必须转成功能项。
2. 每个功能项必须有 target_controller。
3. 每个功能项必须有 required_inputs / required_outputs。
4. 每个功能项必须说明 required_files / required_tools。
5. 不能把“建议”当作“已实现”。
6. 未能映射的内容必须进入 unmapped_items。
```

---

## 7.3 V00：验证证据

### 目标

V00 不负责美化结果，只负责判断：

```text
字段是否完整？
输出是否存在？
证据是否足够？
哪里是 gap？
哪里不能宣称 READY？
```

### 必须输出

```text
v00/validation_matrix.json
v00/gap_register.json
v00/evidence_report.json
v00/v00_handoff_packet.json
```

### `validation_matrix.json`

```json
{
  "validation_id": "v00_validation_<timestamp>",
  "checks": [
    {
      "check_id": "check_k00_outputs",
      "target": "K00",
      "required_outputs": [
        "document_passport.json",
        "corpus_index.json",
        "system_mapping.json",
        "k00_handoff_packet.json"
      ],
      "status": "PASSED"
    },
    {
      "check_id": "check_f00_function_mapping",
      "target": "F00",
      "required_outputs": [
        "function_mapping.json",
        "required_system_assets.json",
        "implementation_task_package.json"
      ],
      "status": "PASSED_WITH_GAPS"
    }
  ],
  "overall_status": "V00_REAL_VALIDATION_EVIDENCE_READY_WITH_GAPS"
}
```

### `gap_register.json`

```json
{
  "gaps": [
    {
      "gap_id": "gap_001",
      "origin_phase": "F00",
      "gap_type": "missing_implementation_evidence",
      "gap_level": "HIGH_GAP",
      "description": "Function mapping exists, but actual implementation has not been applied.",
      "route_to": "U00",
      "status": "OPEN"
    }
  ]
}
```

### V00 验收标准

```text
1. 必须生成 validation_matrix。
2. 必须生成 gap_register。
3. 每个 gap 必须有 level / route_to / status。
4. test_plan 不能当作 TESTED。
5. mapping_ready 不能当作 implemented。
6. READY_WITH_GAPS 必须保留 gap。
```

---

## 7.4 A00：总验收

### 目标

A00 判断当前 run 到底处于什么状态。

允许状态：

```text
PIPELINE_READY
PIPELINE_READY_WITH_GAPS
PIPELINE_BLOCKED
PIPELINE_REJECTED
```

当前目标通常是：

```text
PIPELINE_READY_WITH_GAPS
```

### 必须输出

```text
a00/acceptance_matrix.json
a00/readiness_certificate.json
a00/a00_acceptance_result.json
```

### `a00_acceptance_result.json`

```json
{
  "acceptance_id": "a00_acceptance_<timestamp>",
  "final_status": "HER_DOC_FUNCTION_PIPELINE_RUNNABLE_WITH_GAPS",
  "k00_status": "PASSED",
  "f00_status": "PASSED_WITH_GAPS",
  "v00_status": "PASSED_WITH_GAPS",
  "blocking_gaps": [],
  "non_blocking_gaps": [
    "missing_implementation_evidence",
    "real_tool_execution_not_yet_verified"
  ],
  "ready_for_h00": true,
  "ready_for_production": false,
  "forbidden_claims_blocked": [
    "PRODUCTION_READY",
    "FULLY_AUTOMATED",
    "LIVE_READY",
    "IMPLEMENTED_WITHOUT_EVIDENCE"
  ]
}
```

---

## 7.5 H00：下游队列

### 目标

H00 把当前 run 中的 gap、任务和下游工作变成 queue。

### 必须输出

```text
h00/downstream_queue.json
h00/routing_decision.json
h00/h00_handoff_packets.json
```

### `downstream_queue.json`

```json
{
  "queue_id": "h00_queue_<timestamp>",
  "queue_status": "QUEUE_READY_WITH_GAPS",
  "items": [
    {
      "queue_item_id": "queue_item_001",
      "source_gap": "gap_001",
      "target_controller": "U00",
      "task_type": "REVIEW_AND_UPGRADE",
      "priority": "P1_HIGH",
      "status": "QUEUED"
    },
    {
      "queue_item_id": "queue_item_002",
      "source_function": "func_001",
      "target_controller": "F00",
      "task_type": "IMPLEMENTATION_TASK_REFINEMENT",
      "priority": "P2_MEDIUM",
      "status": "QUEUED"
    }
  ]
}
```

### H00 验收标准

```text
1. 每个 HIGH_GAP / CRITICAL_GAP 必须进入 queue。
2. queue_created 不能等于 task_completed。
3. 每个 queue item 必须有 target_controller。
4. 必须生成 routing_decision。
```

---

## 7.6 U00：复盘升级

### 目标

U00 把 gap 转成：

```text
review case
root cause
upgrade candidate
upgrade queue
learning index
```

### 必须输出

```text
u00/review_cases.json
u00/root_cause_analysis.json
u00/upgrade_queue.json
u00/learning_index.json
```

### `upgrade_queue.json`

```json
{
  "upgrade_queue_id": "u00_upgrade_queue_<timestamp>",
  "queue_status": "UPGRADE_QUEUE_READY_WITH_GAPS",
  "items": [
    {
      "upgrade_item_id": "upgrade_001",
      "source_gap": "gap_001",
      "target_controller": "F00",
      "upgrade_type": "FUNCTION_MAPPING_HARDENING",
      "description": "Improve function mapping so implementation evidence is separated from mapping evidence.",
      "priority": "P1_HIGH",
      "status": "QUEUED"
    }
  ]
}
```

### U00 验收标准

```text
1. 每个 HIGH_GAP 必须有 review case。
2. 每个 review case 必须有 root cause。
3. upgrade candidate 不能等于 upgrade applied。
4. learning_index 必须记录本次运行教训。
```

---

## 7.7 G00：治理候选

### 目标

G00 只做主链路必要治理，不扩展复杂 policy registry。

### 必须输出

```text
g00/governance_candidates.json
g00/policy_rules_update.json
```

### `governance_candidates.json`

```json
{
  "governance_candidates": [
    {
      "candidate_id": "gov_no_ready_without_evidence",
      "rule_type": "STATUS_RULE",
      "rule_statement": "READY must not be claimed when only task package or mapping exists without execution evidence.",
      "priority": "P1_HIGH",
      "source_gap": "gap_001",
      "status": "CANDIDATE"
    },
    {
      "candidate_id": "gov_no_raw_only_k00_completion",
      "rule_type": "PROCESS_RULE",
      "rule_statement": "K00 cannot be marked complete when only raw document is saved.",
      "priority": "P1_HIGH",
      "status": "CANDIDATE"
    }
  ]
}
```

---

## 7.8 O00：总控总结

### 目标

O00 输出最终运行结果，让你能直接看懂：

```text
文档是什么
识别出了什么
映射了哪些功能
缺什么
哪些任务进入队列
下一步该修什么
当前状态是什么
```

### 必须输出

```text
o00/run_summary.json
o00/final_report.md
trace.jsonl
audit.jsonl
```

### `run_summary.json`

```json
{
  "run_id": "her_doc_run_<timestamp>",
  "final_status": "HER_DOC_FUNCTION_PIPELINE_RUNNABLE_WITH_GAPS",
  "document_processed": true,
  "k00_completed": true,
  "f00_completed": true,
  "v00_completed": true,
  "a00_completed": true,
  "h00_completed": true,
  "u00_completed": true,
  "g00_completed": true,
  "blocking_gaps": [],
  "non_blocking_gaps_count": 3,
  "upgrade_items_count": 2,
  "governance_candidates_count": 2,
  "ready_for_next_run": true,
  "ready_for_production": false
}
```

---

# 8. 状态码标准

## 8.1 允许状态

```text
HER_DOC_FUNCTION_PIPELINE_READY
HER_DOC_FUNCTION_PIPELINE_RUNNABLE_WITH_GAPS
HER_DOC_FUNCTION_PIPELINE_BLOCKED
HER_DOC_FUNCTION_PIPELINE_REJECTED
```

当前建议默认目标：

```text
HER_DOC_FUNCTION_PIPELINE_RUNNABLE_WITH_GAPS
```

## 8.2 禁止伪状态

```text
RAW_SAVED_AS_K00_COMPLETE
TASK_PACKAGE_AS_IMPLEMENTED
MAPPING_AS_CODE_DONE
TEST_PLAN_AS_TESTED
QUEUE_CREATED_AS_COMPLETED
UPGRADE_CANDIDATE_AS_APPLIED
READY_WITH_GAPS_AS_READY
SAFE_MODE_AS_PRODUCTION_READY
```

---

# 9. 主命令

HER 只需要先支持一个核心命令：

```bash
cd /root/sikk-gmgn

python3 tools/o00_run_document_main.py \
  --document <真实文档路径> \
  --goal <目标描述或 goal.json> \
  --repo-root /root/sikk-gmgn \
  --output-dir data/her_document_function_system/runs/<run_id> \
  --safe-mode
```

可选增加状态查询：

```bash
python3 tools/her_pipeline_status.py \
  --run-dir data/her_document_function_system/runs/<run_id>
```

---

# 10. 主链路执行协议

```text
O00.0 读取输入
O00.1 创建 run_id 和输出目录
O00.2 复制 raw_document.md
O00.3 写 operator_goal.json
O00.4 调用 K00
O00.5 校验 K00 输出
O00.6 调用 F00
O00.7 校验 F00 输出
O00.8 调用 V00
O00.9 校验 V00 输出
O00.10 调用 A00
O00.11 如果 A00 BLOCKED，停止并写 recovery
O00.12 如果 A00 READY_WITH_GAPS，继续 H00
O00.13 调用 H00
O00.14 调用 U00
O00.15 调用 G00
O00.16 写 run_summary
O00.17 写 final_report
O00.18 写 trace / audit
```

---

# 11. Trace / Audit 要求

## `trace.jsonl`

每步必须写：

```json
{
  "timestamp": "",
  "run_id": "",
  "phase": "K00",
  "event": "phase_started",
  "status": "STARTED"
}
```

```json
{
  "timestamp": "",
  "run_id": "",
  "phase": "F00",
  "event": "function_mapping_written",
  "output": "f00/function_mapping.json",
  "status": "WRITTEN"
}
```

## `audit.jsonl`

必须记录：

```json
{
  "timestamp": "",
  "run_id": "",
  "event": "forbidden_action_check",
  "forbidden_actions": [
    "live_runtime",
    "wallet_signing",
    "auto_deploy",
    "production_trading"
  ],
  "violations": [],
  "status": "PASSED"
}
```

---

# 12. 最终报告模板

## `o00/final_report.md`

```markdown
# HER Document Function Pipeline Report

## 1. Run Info

- run_id:
- document:
- operator_goal:
- safe_mode:
- final_status:

## 2. Document Understanding

- document_role:
- core_intent:
- affected_controllers:
- affected_system_planes:

## 3. Function Mapping

| Function | Target Controller | Required Asset | Status |
|---|---|---|---|

## 4. Validation Result

| Check | Status | Gap |
|---|---|---|

## 5. Acceptance Decision

- final_status:
- blocking_gaps:
- non_blocking_gaps:
- ready_for_next_run:

## 6. Downstream Queue

| Queue Item | Target | Priority | Status |
|---|---|---|---|

## 7. Review / Upgrade

| Upgrade | Target | Priority | Status |
|---|---|---|---|

## 8. Governance Candidates

| Rule | Type | Priority |
|---|---|---|

## 9. Forbidden Claims Blocked

## 10. Next Action

- Continue fixing queued upgrade items.
- Run another real document after fixes.
```

---

# 13. 测试文件

```text
/root/sikk-gmgn/tests/her_doc_function_pipeline/
  test_o00_run_document_requires_real_document.py
  test_o00_run_document_safe_mode_required.py
  test_k00_outputs_required.py
  test_f00_function_mapping_required.py
  test_v00_gap_register_required.py
  test_a00_acceptance_result_required.py
  test_h00_downstream_queue_required.py
  test_u00_upgrade_queue_required.py
  test_g00_governance_candidates_required.py
  test_trace_audit_required.py
  test_no_production_ready_claim.py
```

## 关键测试原则

```text
1. 没有真实文档不能运行。
2. safe_mode=false 必须阻断。
3. K00 缺 document_passport 必须失败。
4. F00 缺 function_mapping 必须失败。
5. V00 缺 gap_register 必须失败。
6. A00 缺 acceptance_result 必须失败。
7. H00 缺 downstream_queue 必须失败。
8. U00 缺 upgrade_queue 必须失败。
9. trace / audit 必须存在。
10. safe-mode 不能标记 production ready。
```

---

# 14. HER 执行任务书

```text
任务：建立 HER_DOC_FUNCTION_PIPELINE_RUNNABLE_WITH_GAPS 主链路

当前停止继续扩展 scheduler / confirmation / manual enable / one-shot trial 等复杂子阶段。

目标：
在 /root/sikk-gmgn 中建立一个可运行的 HER 文档到功能处理主链路。系统必须能读取一份真实 GPT 研究资料或系统建设资料，并按 K00→F00→V00→A00→H00→U00→G00→O00 safe-mode pipeline 生成完整输出。

运行模式：
- safe-mode only
- manual trigger only
- no scheduler
- no background run
- no paper runtime
- no live runtime
- no wallet signing
- no auto deploy
- no production trading

必须建立目录：

/root/sikk-gmgn/system/her_doc_function_pipeline/
/root/sikk-gmgn/data/her_document_function_system/runs/

必须创建系统文件：

system/her_doc_function_pipeline/01_pipeline_manifest.yaml
system/her_doc_function_pipeline/02_pipeline_context_pack.md
system/her_doc_function_pipeline/03_pipeline_input_contract.json
system/her_doc_function_pipeline/04_pipeline_output_contract.json
system/her_doc_function_pipeline/05_pipeline_execution_protocol.md
system/her_doc_function_pipeline/06_pipeline_acceptance_gate.yaml
system/her_doc_function_pipeline/07_pipeline_state.json
system/her_doc_function_pipeline/08_pipeline_handoff.schema.json
system/her_doc_function_pipeline/09_status_code_policy.yaml
system/her_doc_function_pipeline/10_forbidden_action_policy.yaml
system/her_doc_function_pipeline/11_trace_audit_spec.yaml
system/her_doc_function_pipeline/12_recovery_policy.md
system/her_doc_function_pipeline/13_final_report_template.md

必须创建工具文件：

tools/o00_run_document_main.py
tools/k00_document_intake.py
tools/f00_function_mapping.py
tools/v00_validation_evidence.py
tools/a00_acceptance.py
tools/h00_downstream_queue.py
tools/u00_review_upgrade.py
tools/g00_governance_update.py
tools/her_pipeline_status.py

必须创建测试文件：

tests/her_doc_function_pipeline/test_o00_run_document_requires_real_document.py
tests/her_doc_function_pipeline/test_o00_run_document_safe_mode_required.py
tests/her_doc_function_pipeline/test_k00_outputs_required.py
tests/her_doc_function_pipeline/test_f00_function_mapping_required.py
tests/her_doc_function_pipeline/test_v00_gap_register_required.py
tests/her_doc_function_pipeline/test_a00_acceptance_result_required.py
tests/her_doc_function_pipeline/test_h00_downstream_queue_required.py
tests/her_doc_function_pipeline/test_u00_upgrade_queue_required.py
tests/her_doc_function_pipeline/test_g00_governance_candidates_required.py
tests/her_doc_function_pipeline/test_trace_audit_required.py
tests/her_doc_function_pipeline/test_no_production_ready_claim.py

必须支持命令：

cd /root/sikk-gmgn

python3 tools/o00_run_document_main.py \
  --document <真实文档路径> \
  --goal <目标描述或 goal.json> \
  --repo-root /root/sikk-gmgn \
  --output-dir data/her_document_function_system/runs/<run_id> \
  --safe-mode

必须输出：

data/her_document_function_system/runs/<run_id>/
  input/raw_document.md
  input/operator_goal.json

  k00/document_passport.json
  k00/corpus_index.json
  k00/system_mapping.json
  k00/k00_handoff_packet.json

  f00/function_mapping.json
  f00/required_system_assets.json
  f00/implementation_task_package.json
  f00/f00_handoff_packet.json

  v00/validation_matrix.json
  v00/gap_register.json
  v00/evidence_report.json
  v00/v00_handoff_packet.json

  a00/acceptance_matrix.json
  a00/readiness_certificate.json
  a00/a00_acceptance_result.json

  h00/downstream_queue.json
  h00/routing_decision.json
  h00/h00_handoff_packets.json

  u00/review_cases.json
  u00/root_cause_analysis.json
  u00/upgrade_queue.json
  u00/learning_index.json

  g00/governance_candidates.json
  g00/policy_rules_update.json

  o00/run_summary.json
  o00/final_report.md

  trace.jsonl
  audit.jsonl

验收标准：

1. 真实文档可以被读取。
2. operator_goal 可以被保存。
3. K00 不只是保存 raw，必须生成 passport / index / mapping / handoff。
4. F00 必须把解释性文档转成功能落实项。
5. F00 必须输出 required_system_assets 和 implementation_task_package。
6. V00 必须生成 validation_matrix 和 gap_register。
7. A00 必须生成 acceptance_result，且保留 READY_WITH_GAPS。
8. H00 必须生成 downstream_queue。
9. U00 必须生成 review_cases / root_cause_analysis / upgrade_queue。
10. G00 必须生成 governance_candidates / policy_rules_update。
11. O00 必须生成 run_summary 和 final_report。
12. trace.jsonl / audit.jsonl 必须存在。
13. safe_mode=false 必须阻断。
14. 禁止 live_runtime / wallet_signing / auto_deploy / production_trading。
15. 禁止把 task package 标记为 implemented。
16. 禁止把 READY_WITH_GAPS 改写为 READY。
17. 最终状态必须是 HER_DOC_FUNCTION_PIPELINE_RUNNABLE_WITH_GAPS，除非出现 blocking failure。

当前只追求：
真实文档 → 主链路运行 → 文件输出 → gap 保留 → 可验收 → 可复盘。
```

---

# 15. 当前阶段状态判断

```text
HER_DOC_FUNCTION_PIPELINE_RUNNABLE_WITH_GAPS 阶段体系：已完成设计
专业化程度：主链路专业化、压缩复杂旁支、保留关键数据与验收
数据完整性：覆盖 input、K00、F00、V00、A00、H00、U00、G00、O00、trace、audit、report
工程状态：需要 HER 实际创建文件并运行 o00_run_document_main.py
当前真实状态：HER_DOC_FUNCTION_PIPELINE_RUNNABLE_BLUEPRINT_READY
```

不能宣称：

```text
PIPELINE_EXECUTED
PRODUCTION_READY
FULLY_AUTOMATED
SCHEDULER_ENABLED
PAPER_RUNTIME_READY
LIVE_READY
```

---

# 16. 下一步只做一件事

不要继续拆阶段。下一步就是让 HER 执行：

```text
建立工具文件
跑一份真实文档
检查输出目录
看 final_report.md
看 gap_register.json
看 upgrade_queue.json
```

如果跑不起来，再围绕实际报错修：

```text
缺文件 → 补文件
缺字段 → 补 schema
缺输出 → 修工具
缺 trace → 补日志
缺验收 → 修 A00
缺 queue → 修 H00
```

最终目标：

```text
先跑起来。
跑起来后，再根据真实结果升级系统。
```