# V00_REAL_VALIDATION_EVIDENCE_READY_WITH_GAPS

## HER 文档到功能自动化落实系统：真实验证证据层 v1.0

这个阶段的目标是把前面已经跑通的：

```text
O00_CLI_SAMPLE_REPLAY_READY_WITH_GAPS
```

继续推进到：

```text
V00_REAL_VALIDATION_EVIDENCE_READY_WITH_GAPS
```

它代表系统已经不再只是 **design-level replay**，而是开始具备真实验证能力：

```text
schema validation
contract validation
field model validation
rule logic validation
test command execution
stdout / stderr / exit_code 记录
replay input / output 记录
failure evidence 记录
trace / audit 记录
```

但它仍然是：

```text
READY_WITH_GAPS
```

不是：

```text
V00_ACCEPTED
```

原因是：此阶段只证明 **V00 真实验证证据链已经开始成立**，但还不代表所有 Controller、所有测试、所有 runner、所有 policy 都已经完整实现。

---

# 1. 阶段总定义

```yaml
status_code: V00_REAL_VALIDATION_EVIDENCE_READY_WITH_GAPS
status_family: VALIDATION_RUNTIME_STATUS
owner_controller: V00_validation_evidence_controller
upstream_required_status:
  - O00_CLI_SAMPLE_REPLAY_READY_WITH_GAPS
downstream_candidates:
  - R00_runner_tool_binding_controller
  - A00_acceptance_evidence_controller
  - U00_review_upgrade_controller
  - G00_governance_boundary_controller
```

中文定义：

```text
V00_REAL_VALIDATION_EVIDENCE_READY_WITH_GAPS 表示：
系统已经可以执行真实验证命令，生成真实验证证据，并能区分“测试计划”和“测试完成”；
但由于仍可能存在未覆盖测试、未完成真实 runner dry-run、未激活治理 policy、部分 controller 仍是 DESIGN_ONLY，所以最终状态只能是 READY_WITH_GAPS。
```

---

# 2. 和上一阶段的区别

## 2.1 上一阶段：O00_CLI_SAMPLE_REPLAY_READY_WITH_GAPS

上一阶段证明：

|能力|状态|
|---|---|
|CLI 可调用|已证明|
|registry 可读取|已证明|
|config 可读取|已证明|
|sample replay 可走通|已证明|
|final report 可生成|已证明|
|不伪装 TESTED / RUNNER_BOUND / POLICY_ACTIVE|已证明|
|真实测试执行|未证明|
|真实 schema validation|未充分证明|
|真实 contract validation|未充分证明|
|真实 replay evidence|未充分证明|

---

## 2.2 当前阶段：V00_REAL_VALIDATION_EVIDENCE_READY_WITH_GAPS

当前阶段要证明：

|能力|要求|
|---|---|
|JSON schema 能真实校验|必须|
|input / output contract 能真实校验|必须|
|field_model 能真实校验|必须|
|rule_logic 能真实校验|必须|
|pytest 或等价测试命令能执行|必须|
|stdout / stderr / exit_code 能记录|必须|
|replay input / output 能生成|必须|
|failure evidence 能记录|必须|
|trace / audit 能追加|必须|
|失败不会被伪装成通过|必须|
|READY_WITH_GAPS 能被保留|必须|

---

# 3. 本阶段不是做什么

|错误理解|正确理解|
|---|---|
|不是继续写设计文档|要建立真实验证执行器和证据输出|
|不是只生成 test plan|要执行命令并记录结果|
|不是把 sample replay 当真实测试|sample replay 只是输入之一|
|不是 runner binding|R00 负责 runner binding|
|不是 policy active|G00 负责 policy 激活|
|不是系统完全闭环|只是验证证据层可运行|
|不是生产运行|禁止 live / signing / deploy / trading|

---

# 4. 阶段核心目标

当前阶段要建立一个真实验证执行层：

```text
V00_real_validation_executor
```

它挂在 V00 下面，负责把 F00 / O00 / sample replay 产生的设计资产转化为真实验证证据。

核心链路：

```text
O00 sample replay output
↓
V00 real validation executor
↓
schema validation
↓
contract validation
↓
field model validation
↓
rule logic validation
↓
pytest / unit test execution
↓
replay execution
↓
failure evidence
↓
validation evidence bundle
↓
V00 acceptance result
↓
V00 handoff
```

---

# 5. 必须建立的目录结构

建议新增：

```text
/root/sikk-gmgn/system/her_document_function_system/validation/
  v00_real_validation/
    01_v00_real_validation_manifest.yaml
    02_v00_real_validation_context_pack.md
    03_v00_real_validation_input_contract.json
    04_v00_real_validation_output_contract.json
    05_v00_real_validation_execution_protocol.md
    06_v00_real_validation_acceptance_gate.yaml
    07_v00_real_validation_state.json
    08_v00_real_validation_handoff.schema.json
    09_schema_validation_spec.schema.json
    10_contract_validation_spec.schema.json
    11_field_model_validation_spec.schema.json
    12_rule_logic_validation_spec.schema.json
    13_test_execution_evidence.schema.json
    14_replay_execution_evidence.schema.json
    15_failure_evidence.schema.json
    16_validation_evidence_bundle.schema.json
    17_trace_audit_spec.yaml
    18_recovery_policy.md
    19_v00_real_validation_report_template.md
```

运行输出目录：

```text
/root/sikk-gmgn/data/her_document_function_system/v00_real_validation_runs/<validation_run_id>/
  input/
  preflight/
  schema_validation/
  contract_validation/
  field_model_validation/
  rule_logic_validation/
  test_execution/
  replay_execution/
  failure_evidence/
  evidence_bundle/
  trace/
  audit/
  acceptance/
  handoff/
  reports/
```

---

# 6. 必须建立的工具文件

新增真实验证工具层：

```text
/root/sikk-gmgn/tools/
  v00_real_validation_executor.py
  v00_schema_validator.py
  v00_contract_validator.py
  v00_field_model_validator.py
  v00_rule_logic_validator.py
  v00_test_runner.py
  v00_replay_executor.py
  v00_evidence_bundle_builder.py
  v00_validation_status.py
```

每个文件职责如下：

|文件|责任|
|---|---|
|`v00_real_validation_executor.py`|V00 真实验证总入口|
|`v00_schema_validator.py`|校验 JSON schema|
|`v00_contract_validator.py`|校验 input / output / handoff contract|
|`v00_field_model_validator.py`|校验字段来源、类型、缺失策略|
|`v00_rule_logic_validator.py`|校验 rule_id、input_fields、condition、output_status|
|`v00_test_runner.py`|执行 pytest 或安全测试命令|
|`v00_replay_executor.py`|执行 replay input → output 检查|
|`v00_evidence_bundle_builder.py`|汇总 validation evidence|
|`v00_validation_status.py`|查询验证状态|

---

# 7. 输入合约

## 7.1 `03_v00_real_validation_input_contract.json`

```json
{
  "phase_id": "V00_REAL_VALIDATION",
  "required_inputs": {
    "o00_pipeline_run_ref": {
      "required": true,
      "description": "O00 sample replay 或 document pipeline 输出引用"
    },
    "f00_handoff_packet": {
      "required": true,
      "description": "F00 输出的功能落实交接包"
    },
    "function_mapping": {
      "required": true,
      "description": "概念到功能映射"
    },
    "field_model": {
      "required": true,
      "description": "字段模型"
    },
    "rule_logic": {
      "required": true,
      "description": "规则逻辑"
    },
    "schema_refs": {
      "required": true,
      "description": "需要验证的 schema 文件引用"
    },
    "contract_refs": {
      "required": true,
      "description": "需要验证的 input / output / handoff contract 引用"
    },
    "test_plan": {
      "required": true,
      "description": "F00 或 V00 生成的测试计划"
    },
    "replay_plan": {
      "required": true,
      "description": "replay 计划"
    },
    "execution_boundary": {
      "required": true,
      "description": "执行边界"
    },
    "repo_root": {
      "required": true,
      "description": "仓库根目录"
    },
    "safe_mode": {
      "required": true,
      "description": "必须为 true"
    }
  }
}
```

---

# 8. 输出合约

## 8.1 `04_v00_real_validation_output_contract.json`

```json
{
  "phase_id": "V00_REAL_VALIDATION",
  "required_outputs": {
    "preflight_result": "preflight/v00_real_validation_preflight.json",
    "schema_validation_result": "schema_validation/schema_validation_result.json",
    "contract_validation_result": "contract_validation/contract_validation_result.json",
    "field_model_validation_result": "field_model_validation/field_model_validation_result.json",
    "rule_logic_validation_result": "rule_logic_validation/rule_logic_validation_result.json",
    "test_execution_evidence": "test_execution/test_execution_evidence.json",
    "test_stdout": "test_execution/test_stdout.log",
    "test_stderr": "test_execution/test_stderr.log",
    "replay_execution_evidence": "replay_execution/replay_execution_evidence.json",
    "failure_evidence": "failure_evidence/failure_evidence.json",
    "validation_evidence_bundle": "evidence_bundle/validation_evidence_bundle.json",
    "trace_log": "trace/v00_real_validation_trace.jsonl",
    "audit_log": "audit/v00_real_validation_audit.jsonl",
    "acceptance_result": "acceptance/v00_real_validation_acceptance.json",
    "handoff_packet": "handoff/v00_real_validation_to_a00_handoff.json",
    "final_report": "reports/v00_real_validation_report.md"
  }
}
```

---

# 9. 执行命令设计

## 9.1 主命令

```bash
cd /root/sikk-gmgn

python3 tools/v00_real_validation_executor.py \
  --pipeline-run data/her_document_function_system/o00_runs/<pipeline_run_id>/pipeline_run.json \
  --f00-handoff data/her_document_function_system/o00_runs/<pipeline_run_id>/handoffs/f00_to_v00_ref.json \
  --repo-root /root/sikk-gmgn \
  --output-dir data/her_document_function_system/v00_real_validation_runs/<validation_run_id> \
  --safe-mode
```

---

## 9.2 分步命令

### schema validation

```bash
python3 tools/v00_schema_validator.py \
  --schema-dir system/her_document_function_system/controllers \
  --output-dir data/her_document_function_system/v00_real_validation_runs/<validation_run_id>/schema_validation \
  --safe-mode
```

### contract validation

```bash
python3 tools/v00_contract_validator.py \
  --contracts-dir system/her_document_function_system/controllers \
  --output-dir data/her_document_function_system/v00_real_validation_runs/<validation_run_id>/contract_validation \
  --safe-mode
```

### field model validation

```bash
python3 tools/v00_field_model_validator.py \
  --field-model data/her_document_function_system/o00_runs/<pipeline_run_id>/evidence/field_model.json \
  --output-dir data/her_document_function_system/v00_real_validation_runs/<validation_run_id>/field_model_validation \
  --safe-mode
```

### rule logic validation

```bash
python3 tools/v00_rule_logic_validator.py \
  --rule-logic data/her_document_function_system/o00_runs/<pipeline_run_id>/evidence/rule_logic.json \
  --output-dir data/her_document_function_system/v00_real_validation_runs/<validation_run_id>/rule_logic_validation \
  --safe-mode
```

### test runner

```bash
python3 tools/v00_test_runner.py \
  --test-path tests/her_document_function_system \
  --output-dir data/her_document_function_system/v00_real_validation_runs/<validation_run_id>/test_execution \
  --safe-mode
```

### replay executor

```bash
python3 tools/v00_replay_executor.py \
  --replay-config system/her_document_function_system/replay/sample_cases/sample_001_document_to_function/run/replay_run_config.json \
  --output-dir data/her_document_function_system/v00_real_validation_runs/<validation_run_id>/replay_execution \
  --safe-mode
```

---

# 10. V00 真实验证内部流程

```text
V00_REAL.0 Preflight Gate
V00_REAL.1 Input Loader
V00_REAL.2 Schema Validation
V00_REAL.3 Contract Validation
V00_REAL.4 Field Model Validation
V00_REAL.5 Rule Logic Validation
V00_REAL.6 Test Execution
V00_REAL.7 Replay Execution
V00_REAL.8 Failure Evidence Builder
V00_REAL.9 Evidence Bundle Builder
V00_REAL.10 Acceptance Gate
V00_REAL.11 Handoff Writer
V00_REAL.12 Final Report Writer
```

---

# 11. V00_REAL.0 Preflight Gate

## 11.1 检查项

|检查项|要求|
|---|---|
|O00 pipeline run 是否存在|必须|
|F00 handoff 是否存在|必须|
|function_mapping 是否存在|必须|
|field_model 是否存在|必须|
|rule_logic 是否存在|必须|
|schema refs 是否存在|必须|
|contract refs 是否存在|必须|
|test plan 是否存在|必须|
|replay plan 是否存在|必须|
|safe_mode 是否为 true|必须|
|是否禁止 live / signing / deploy / trading|必须|

## 11.2 输出

```json
{
  "preflight_status": "PASSED",
  "safe_mode": true,
  "loaded_inputs": [
    "o00_pipeline_run",
    "f00_handoff",
    "function_mapping",
    "field_model",
    "rule_logic",
    "schema_refs",
    "contract_refs",
    "test_plan",
    "replay_plan"
  ],
  "forbidden_actions_checked": [
    "live_runtime",
    "wallet_signing",
    "auto_deploy",
    "production_trading"
  ],
  "blocking_gaps": []
}
```

---

# 12. Schema Validation

## 12.1 校验对象

必须至少校验：

```text
controller_registry.schema.json
pipeline_config.schema.json
o00_handoff_packet.schema.json
v00_handoff_packet.schema.json
test_execution_evidence.schema.json
replay_execution_evidence.schema.json
failure_evidence.schema.json
validation_evidence_bundle.schema.json
```

## 12.2 输出结构

```json
{
  "validation_type": "schema_validation",
  "status": "PASSED",
  "schemas_checked": [
    "controller_registry.schema.json",
    "pipeline_config.schema.json",
    "test_execution_evidence.schema.json"
  ],
  "valid_schemas": [],
  "invalid_schemas": [],
  "errors": [],
  "warnings": []
}
```

## 12.3 状态规则

|情况|状态|
|---|---|
|所有必需 schema 合法|`SCHEMA_VALIDATED`|
|非关键 schema 缺失|`SCHEMA_READY_WITH_GAPS`|
|关键 schema 不合法|`SCHEMA_INVALID`|
|schema 文件不存在|`SCHEMA_MISSING`|

---

# 13. Contract Validation

## 13.1 校验对象

```text
K00 input / output contract
F00 input / output contract
V00 input / output contract
R00 input / output contract
A00 input / output contract
H00 input / output contract
U00 input / output contract
G00 input / output contract
O00 input / output contract
```

## 13.2 必须检查

|检查项|要求|
|---|---|
|required_inputs 是否存在|必须|
|required_outputs 是否存在|必须|
|missing_policy 是否存在|必须|
|forbidden_actions 是否存在|必须|
|gap_refs 是否能交接|必须|
|trace_refs 是否能交接|必须|
|acceptance_result 是否存在|必须|
|handoff_refs 是否存在|必须|

## 13.3 输出结构

```json
{
  "validation_type": "contract_validation",
  "status": "PASSED",
  "contracts_checked": [],
  "valid_contracts": [],
  "invalid_contracts": [],
  "missing_required_fields": [],
  "errors": [],
  "warnings": []
}
```

---

# 14. Field Model Validation

## 14.1 必须校验字段

每个 field_model 必须具备：

```text
field_name
field_type
source
required
missing_policy
evidence_level
used_by
output_to
trace_required
```

专业级建议必须具备：

```text
source_path
validation_rule
counter_evidence_required
owner_phase
handoff_target
report_visibility
kv_indexed
```

## 14.2 输出结构

```json
{
  "validation_type": "field_model_validation",
  "status": "PASSED",
  "total_fields": 0,
  "valid_fields": 0,
  "invalid_fields": 0,
  "missing_source_fields": [],
  "missing_policy_fields": [],
  "warnings": []
}
```

## 14.3 阻断规则

```text
没有 field_name → BLOCK
没有 field_type → BLOCK
没有 source → BLOCK
没有 missing_policy → READY_WITH_GAPS 或 BLOCK，取决于字段重要性
没有 used_by → READY_WITH_GAPS
```

---

# 15. Rule Logic Validation

## 15.1 每条 rule 必须具备

```text
rule_id
rule_type
input_fields
calculation_method
threshold_or_condition
positive_evidence
counter_evidence
failure_condition
output_status
trace_required
```

## 15.2 输出结构

```json
{
  "validation_type": "rule_logic_validation",
  "status": "PASSED",
  "total_rules": 0,
  "valid_rules": 0,
  "invalid_rules": 0,
  "blocked_rules": [],
  "warnings": []
}
```

## 15.3 硬阻断规则

```text
只写“AI 判断” → REJECT
无 input_fields → BLOCK
无 output_status → BLOCK
无 failure_condition → READY_WITH_GAPS
无 trace_required → READY_WITH_GAPS
```

---

# 16. Test Execution Evidence

这是本阶段最关键的部分。

## 16.1 不能再只有 test_plan

必须生成真实：

```text
test_command
exit_code
stdout_path
stderr_path
started_at
ended_at
passed_count
failed_count
covered_functions
covered_rules
failure_reason
```

## 16.2 test_execution_evidence.json

```json
{
  "evidence_id": "test_evidence_v00_real_<timestamp>",
  "validation_run_id": "v00_real_<timestamp>",
  "test_type": "pytest",
  "test_command": "pytest tests/her_document_function_system -q",
  "started_at": "",
  "ended_at": "",
  "exit_code": 0,
  "stdout_path": "test_execution/test_stdout.log",
  "stderr_path": "test_execution/test_stderr.log",
  "passed_count": 0,
  "failed_count": 0,
  "skipped_count": 0,
  "covered_functions": [],
  "covered_rules": [],
  "status": "TESTED",
  "failure_reason": null
}
```

## 16.3 状态规则

|情况|状态|
|---|---|
|有 command、exit_code、stdout、stderr，且 exit_code=0|`TESTED`|
|有 command、exit_code，但失败|`TEST_FAILED`|
|只有 test_plan|`TEST_PLANNED_ONLY`|
|没有 command|`TEST_NOT_EXECUTED`|
|没有 stdout/stderr|`TEST_EVIDENCE_INCOMPLETE`|

---

# 17. Replay Execution Evidence

## 17.1 replay 必须生成

```text
replay_input.json
replay_output.json
replay_trace.jsonl
replay_expected.json
replay_comparison.json
replay_evidence.json
```

## 17.2 replay_execution_evidence.json

```json
{
  "replay_id": "replay_v00_real_<timestamp>",
  "validation_run_id": "v00_real_<timestamp>",
  "replay_config": "replay_run_config.json",
  "replay_input": "replay_execution/replay_input.json",
  "replay_output": "replay_execution/replay_output.json",
  "replay_expected": "replay_execution/replay_expected.json",
  "replay_comparison": "replay_execution/replay_comparison.json",
  "trace_path": "replay_execution/replay_trace.jsonl",
  "status": "REPLAY_TESTED",
  "matched_checks": [],
  "failed_checks": [],
  "warnings": []
}
```

## 17.3 状态规则

|情况|状态|
|---|---|
|replay input/output/trace/comparison 全部存在|`REPLAY_TESTED`|
|replay 执行但有非阻断差异|`REPLAY_READY_WITH_GAPS`|
|replay 执行失败|`REPLAY_FAILED`|
|只有 replay plan|`REPLAY_PLANNED_ONLY`|

---

# 18. Failure Evidence

失败不能丢失。

## 18.1 failure_evidence.json

```json
{
  "failure_evidence_id": "failure_v00_real_<timestamp>",
  "validation_run_id": "v00_real_<timestamp>",
  "failures": [
    {
      "failure_id": "failure_001",
      "failure_type": "TEST_FAILED",
      "source_step": "V00_REAL.6",
      "affected_asset": "tests/her_document_function_system",
      "gap_level": "BLOCKING_GAP",
      "failure_reason": "pytest exit_code != 0",
      "evidence_refs": [
        "test_execution/test_stdout.log",
        "test_execution/test_stderr.log"
      ],
      "required_fix": "Fix failing tests and rerun V00 real validation",
      "can_continue": false
    }
  ]
}
```

## 18.2 failure 类型

```text
SCHEMA_INVALID
CONTRACT_INVALID
FIELD_MODEL_INVALID
RULE_LOGIC_INVALID
TEST_FAILED
TEST_EVIDENCE_INCOMPLETE
REPLAY_FAILED
TRACE_MISSING
AUDIT_MISSING
FORBIDDEN_ACTION_DETECTED
```

---

# 19. Validation Evidence Bundle

所有验证证据必须汇总成 evidence bundle。

## 19.1 validation_evidence_bundle.json

```json
{
  "bundle_id": "validation_evidence_bundle_v00_real_<timestamp>",
  "validation_run_id": "v00_real_<timestamp>",
  "source_pipeline_run_id": "o00_run_<timestamp>",
  "evidence_groups": {
    "schema_validation": [],
    "contract_validation": [],
    "field_model_validation": [],
    "rule_logic_validation": [],
    "test_execution": [],
    "replay_execution": [],
    "failure_evidence": [],
    "trace_audit": []
  },
  "summary": {
    "schema_status": "SCHEMA_VALIDATED",
    "contract_status": "CONTRACT_VALIDATED",
    "field_model_status": "FIELD_MODEL_VALIDATED",
    "rule_logic_status": "RULE_LOGIC_VALIDATED",
    "test_status": "TESTED",
    "replay_status": "REPLAY_TESTED",
    "final_validation_status": "V00_REAL_VALIDATION_EVIDENCE_READY_WITH_GAPS"
  },
  "open_gaps": [],
  "blocking_gaps": [],
  "ready_for_a00": true,
  "ready_for_r00": false
}
```

---

# 20. 为什么仍然是 READY_WITH_GAPS

即使本阶段能真实执行测试，也不应该马上标记为完全通过。

原因：

```text
1. 当前只验证文档到功能系统的核心 schema / contract / test / replay。
2. 不代表所有 K00/F00/V00/R00/A00/H00/U00/G00 控制器都已完整实现。
3. 不代表 R00 runner binding 已真实 dry-run。
4. 不代表 G00 policy 已 active。
5. 不代表 run-document 真实生产文档流程已大量验证。
6. 不代表系统可以接 paper runtime / live runtime。
```

所以最终状态应该是：

```text
V00_REAL_VALIDATION_EVIDENCE_READY_WITH_GAPS
```

而不是：

```text
V00_ACCEPTED
SYSTEM_FULLY_VALIDATED
PIPELINE_ACCEPTED
```

---

# 21. 本阶段最终状态判定

## 21.1 可以达成的状态

```text
SCHEMA_VALIDATED
CONTRACT_VALIDATED
FIELD_MODEL_VALIDATED
RULE_LOGIC_VALIDATED
TESTED
REPLAY_TESTED
VALIDATION_EVIDENCE_BUNDLE_READY
V00_REAL_VALIDATION_EVIDENCE_READY_WITH_GAPS
```

## 21.2 禁止伪状态

```text
RUNNER_BOUND
POLICY_ACTIVE
PRODUCTION_READY
LIVE_READY
SYSTEM_FULLY_IMPLEMENTED
PIPELINE_ACCEPTED
```

---

# 22. 验收门

## 22.1 必须通过项

|验收项|要求|
|---|---|
|preflight_result 存在|必须|
|schema_validation_result 存在|必须|
|contract_validation_result 存在|必须|
|field_model_validation_result 存在|必须|
|rule_logic_validation_result 存在|必须|
|test_execution_evidence 存在|必须|
|test_stdout.log 存在|必须|
|test_stderr.log 存在|必须|
|exit_code 存在|必须|
|replay_execution_evidence 存在|必须|
|replay_input / output 存在|必须|
|failure_evidence 存在|必须，即使为空|
|validation_evidence_bundle 存在|必须|
|trace / audit 存在|必须|
|final report 存在|必须|
|final status = READY_WITH_GAPS|必须|

---

## 22.2 不允许通过的情况

```text
只有 test_plan
没有 test_command
没有 exit_code
没有 stdout/stderr
只有 replay_plan
没有 replay_output
schema 未校验
contract 未校验
rule_logic 只有自然语言
failure 被隐藏
trace/audit 缺失
safe_mode=false
触发 live/runtime/signing/deploy/trading
```

---

# 23. 推荐测试目录

建议新增：

```text
/root/sikk-gmgn/tests/her_document_function_system/
  test_controller_registry_schema.py
  test_pipeline_config_schema.py
  test_o00_sample_replay_expected_status.py
  test_v00_test_plan_not_tested.py
  test_v00_test_evidence_required_fields.py
  test_v00_rule_logic_required_fields.py
  test_a00_status_consistency.py
  test_g00_evidence_policy_candidate.py
```

---

# 24. 关键测试用例

## 24.1 test_plan 不能等于 TESTED

```python
def test_test_plan_cannot_satisfy_tested_status():
    test_plan_only = {
        "test_plan": "pytest tests/her_document_function_system",
        "status": "TESTED"
    }

    required_evidence_fields = [
        "test_command",
        "exit_code",
        "stdout_path",
        "stderr_path",
        "passed_count",
        "failed_count"
    ]

    missing = [field for field in required_evidence_fields if field not in test_plan_only]

    assert missing
    assert test_plan_only["status"] != "VALID_TESTED_STATUS"
```

---

## 24.2 TESTED 必须有 exit_code

```python
def test_tested_requires_exit_code():
    evidence = {
        "test_command": "pytest tests/her_document_function_system",
        "stdout_path": "stdout.log",
        "stderr_path": "stderr.log",
        "passed_count": 3,
        "failed_count": 0
    }

    assert "exit_code" not in evidence
```

真实实现时应由 validator 返回：

```text
TEST_EVIDENCE_INCOMPLETE
```

---

## 24.3 runner_binding_required=false 时不能 RUNNER_BOUND

```python
def test_no_runner_bound_when_runner_binding_not_required():
    replay_context = {
        "runner_binding_required": False,
        "r00_status": "SKIPPED_WITH_REASON"
    }

    assert replay_context["r00_status"] != "RUNNER_BOUND"
```

---

# 25. Final Report 模板

```markdown
# V00 Real Validation Evidence Report

## 1. Run Info

- validation_run_id:
- source_pipeline_run_id:
- repo_root:
- safe_mode:
- started_at:
- completed_at:
- final_status:

## 2. Input Evidence

- O00 pipeline run:
- F00 handoff:
- function_mapping:
- field_model:
- rule_logic:
- schema refs:
- contract refs:
- test plan:
- replay plan:

## 3. Preflight

- input_loaded:
- safe_mode_checked:
- forbidden_actions_checked:

## 4. Schema Validation

- status:
- schemas_checked:
- invalid_schemas:
- warnings:

## 5. Contract Validation

- status:
- contracts_checked:
- invalid_contracts:
- warnings:

## 6. Field Model Validation

- status:
- total_fields:
- invalid_fields:
- missing_source_fields:

## 7. Rule Logic Validation

- status:
- total_rules:
- invalid_rules:
- blocked_rules:

## 8. Test Execution Evidence

- test_command:
- exit_code:
- stdout_path:
- stderr_path:
- passed_count:
- failed_count:
- status:

## 9. Replay Evidence

- replay_input:
- replay_output:
- replay_trace:
- replay_comparison:
- status:

## 10. Failure Evidence

- blocking_failures:
- non_blocking_failures:
- recovery_required:

## 11. Evidence Bundle

- bundle_path:
- final_validation_status:

## 12. Gap Summary

## 13. Allowed Next Actions

## 14. Forbidden Next Actions

## 15. Final Decision
```

---

# 26. 可直接给 HER 的执行任务书

```text
任务：建立并执行 V00_REAL_VALIDATION_EVIDENCE_READY_WITH_GAPS 阶段

你不是继续写 V00 设计说明，而是建立真实验证证据执行层，让 V00 从 design-level replay 进入 real validation evidence 阶段。

目标：
在 /root/sikk-gmgn 中建立 V00 real validation 工具链，执行真实 schema validation、contract validation、field_model validation、rule_logic validation、test execution、replay execution，并输出 stdout、stderr、exit_code、failure_evidence、validation_evidence_bundle、trace、audit 和 final report。

必须建立目录：

/root/sikk-gmgn/system/her_document_function_system/validation/v00_real_validation/
/root/sikk-gmgn/data/her_document_function_system/v00_real_validation_runs/

必须创建系统文件：

01_v00_real_validation_manifest.yaml
02_v00_real_validation_context_pack.md
03_v00_real_validation_input_contract.json
04_v00_real_validation_output_contract.json
05_v00_real_validation_execution_protocol.md
06_v00_real_validation_acceptance_gate.yaml
07_v00_real_validation_state.json
08_v00_real_validation_handoff.schema.json
09_schema_validation_spec.schema.json
10_contract_validation_spec.schema.json
11_field_model_validation_spec.schema.json
12_rule_logic_validation_spec.schema.json
13_test_execution_evidence.schema.json
14_replay_execution_evidence.schema.json
15_failure_evidence.schema.json
16_validation_evidence_bundle.schema.json
17_trace_audit_spec.yaml
18_recovery_policy.md
19_v00_real_validation_report_template.md

必须创建工具文件：

tools/v00_real_validation_executor.py
tools/v00_schema_validator.py
tools/v00_contract_validator.py
tools/v00_field_model_validator.py
tools/v00_rule_logic_validator.py
tools/v00_test_runner.py
tools/v00_replay_executor.py
tools/v00_evidence_bundle_builder.py
tools/v00_validation_status.py

必须创建测试文件：

tests/her_document_function_system/test_controller_registry_schema.py
tests/her_document_function_system/test_pipeline_config_schema.py
tests/her_document_function_system/test_o00_sample_replay_expected_status.py
tests/her_document_function_system/test_v00_test_plan_not_tested.py
tests/her_document_function_system/test_v00_test_evidence_required_fields.py
tests/her_document_function_system/test_v00_rule_logic_required_fields.py
tests/her_document_function_system/test_a00_status_consistency.py
tests/her_document_function_system/test_g00_evidence_policy_candidate.py

必须执行命令：

cd /root/sikk-gmgn

python3 tools/v00_real_validation_executor.py \
  --pipeline-run data/her_document_function_system/o00_runs/<pipeline_run_id>/pipeline_run.json \
  --repo-root /root/sikk-gmgn \
  --output-dir data/her_document_function_system/v00_real_validation_runs/<validation_run_id> \
  --safe-mode

必须输出：

- preflight/v00_real_validation_preflight.json
- schema_validation/schema_validation_result.json
- contract_validation/contract_validation_result.json
- field_model_validation/field_model_validation_result.json
- rule_logic_validation/rule_logic_validation_result.json
- test_execution/test_execution_evidence.json
- test_execution/test_stdout.log
- test_execution/test_stderr.log
- replay_execution/replay_execution_evidence.json
- replay_execution/replay_input.json
- replay_execution/replay_output.json
- replay_execution/replay_trace.jsonl
- failure_evidence/failure_evidence.json
- evidence_bundle/validation_evidence_bundle.json
- trace/v00_real_validation_trace.jsonl
- audit/v00_real_validation_audit.jsonl
- acceptance/v00_real_validation_acceptance.json
- handoff/v00_real_validation_to_a00_handoff.json
- reports/v00_real_validation_report.md

必须保证：

1. safe_mode 必须为 true。
2. 禁止 live_runtime。
3. 禁止 wallet_signing。
4. 禁止 auto_deploy。
5. 禁止 production_trading。
6. 禁止把 test_plan 标记为 TESTED。
7. TESTED 必须有 test_command、exit_code、stdout_path、stderr_path、passed_count、failed_count。
8. REPLAY_TESTED 必须有 replay_input、replay_output、replay_trace、replay_comparison。
9. schema validation 必须真实执行。
10. contract validation 必须真实执行。
11. field_model validation 必须真实执行。
12. rule_logic validation 必须真实执行。
13. pytest 或等价测试命令必须真实执行。
14. stdout / stderr / exit_code 必须记录。
15. failure evidence 必须存在，即使没有失败也要写空结构。
16. trace / audit 必须追加写入，不能覆盖。
17. 最终状态必须是 V00_REAL_VALIDATION_EVIDENCE_READY_WITH_GAPS，除非出现 blocking failure。
18. 不能宣称 RUNNER_BOUND。
19. 不能宣称 POLICY_ACTIVE。
20. 不能宣称 PIPELINE_ACCEPTED。

验收标准：

- 所有系统文件存在。
- 所有 tools/v00_*.py 文件存在。
- 所有 tests/her_document_function_system/*.py 文件存在。
- v00_real_validation_executor.py 可执行。
- test_execution_evidence.json 包含 command、exit_code、stdout_path、stderr_path。
- replay_execution_evidence.json 包含 input、output、trace、comparison。
- validation_evidence_bundle.json 汇总全部验证结果。
- final report 存在。
- final status = V00_REAL_VALIDATION_EVIDENCE_READY_WITH_GAPS。
```

---

# 27. 当前设计状态判断

```text
V00_REAL_VALIDATION_EVIDENCE_READY_WITH_GAPS 阶段体系：已建立
专业化程度：轻量机构级真实验证证据层设计完成
数据完整性：覆盖 schema、contract、field_model、rule_logic、test、replay、failure、evidence bundle、trace、audit、handoff
工程状态：需要 HER 实际创建文件并运行 v00_real_validation_executor.py
当前真实状态：REAL_VALIDATION_BLUEPRINT_READY
不能宣称：
- V00_REAL_VALIDATION_EXECUTED
- TESTED
- REPLAY_TESTED
- VALIDATION_EVIDENCE_BUNDLE_READY
- V00_ACCEPTED
```

---

# 28. 下一步

完成这个阶段后，系统会从：

```text
O00 CLI 样例可回放
```

升级到：

```text
V00 真实验证证据可生成
```

下一阶段应该是：

```text
R00_REAL_SAFE_DRY_RUN_BINDING_READY_WITH_GAPS
```

也就是让 runner / tool binding 从“设计”推进到：

```text
真实 safe dry-run
真实 command contract
真实 generated_outputs_manifest
真实 dry_run stdout / stderr / exit_code
```

最终判断：

```text
V00_REAL_VALIDATION_EVIDENCE_READY_WITH_GAPS 是从“样例回放”进入“真实验证”的关键门槛。

它证明系统不再只是设计逻辑，而是开始具备真实测试、真实校验、真实 replay、真实证据记录能力。

但只要 runner binding 未真实 dry-run、G00 policy 未 active、run-document 未大量验证，就必须保留 READY_WITH_GAPS。
```