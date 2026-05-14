# P00_SYSTEM_BOOTSTRAP_CONTROLLER_LANDING_AND_ACCEPTANCE

任务类型：

```text
P00 系统建造控制器落盘与验收任务
不是 P01 运行任务
不是自动化交易任务
不是真实交易任务
```

---

# 一、任务目标

将已经设计好的：

```text
P00_system_bootstrap_controller
```

正式落盘为可被 HER 读取、验证、执行和回写的阶段控制器文件组。

本任务完成后，系统状态应从：

```text
P00_DESIGNED_NOT_LANDED
```

推进为：

```text
P00_LANDED_AND_ACCEPTANCE_CHECKED
```

如果验收全部通过，可进一步推进为：

```text
P00_BOOTSTRAP_READY_TO_EXECUTE
```

但仍然禁止进入 P01。

---

# 二、当前任务边界

## 本任务允许做

```text
1. 创建 P00 控制器目录。
2. 创建 P00 controller 文件组。
3. 创建 P00 输入合约。
4. 创建 P00 输出合约。
5. 创建 P00 任务树。
6. 创建 P00 验收门。
7. 创建 P00 runner 绑定说明。
8. 创建 P00 状态回写策略。
9. 创建 P00 handoff schema。
10. 创建 P00 bootstrap report 模板。
11. 创建 reports 目录。
12. 执行文件级 / 结构级 / 安全级自检。
13. 输出 P00 landing acceptance report。
```

## 本任务禁止做

```text
1. 禁止启动 P01。
2. 禁止运行自动化交易 workflow。
3. 禁止真实交易。
4. 禁止调用交易执行接口。
5. 禁止把 P00 落盘完成解释为系统集成完成。
6. 禁止把 P01 标记为 READY。
7. 禁止绕过 Data Plane。
8. 禁止删除 legacy runtime 数据。
9. 禁止覆盖已有文件而不备份。
```

---

# 三、必须创建目录

```text
/root/sikk-gmgn/sikk_stable_trader_os/06_phase_controllers/P00_system_bootstrap_controller/
/root/sikk-gmgn/sikk_stable_trader_os/06_phase_controllers/P00_system_bootstrap_controller/reports/
/root/sikk-gmgn/sikk_stable_trader_os/00_control/
/root/sikk-gmgn/sikk_stable_trader_os/00_trace/
/root/sikk-gmgn/sikk_stable_trader_os/08_acceptance/
/root/sikk-gmgn/sikk_stable_trader_os/09_handoff/
```

如目录已存在，不删除，继续使用。

如目标文件已存在，先备份：

```text
<filename>.bak_20260511
```

---

# 四、必须创建 P00 文件组

```text
/root/sikk-gmgn/sikk_stable_trader_os/06_phase_controllers/P00_system_bootstrap_controller/context.md

/root/sikk-gmgn/sikk_stable_trader_os/06_phase_controllers/P00_system_bootstrap_controller/controller.yaml

/root/sikk-gmgn/sikk_stable_trader_os/06_phase_controllers/P00_system_bootstrap_controller/input_contract.json

/root/sikk-gmgn/sikk_stable_trader_os/06_phase_controllers/P00_system_bootstrap_controller/output_contract.json

/root/sikk-gmgn/sikk_stable_trader_os/06_phase_controllers/P00_system_bootstrap_controller/task_tree.yaml

/root/sikk-gmgn/sikk_stable_trader_os/06_phase_controllers/P00_system_bootstrap_controller/acceptance_gate.yaml

/root/sikk-gmgn/sikk_stable_trader_os/06_phase_controllers/P00_system_bootstrap_controller/runner_binding.yaml

/root/sikk-gmgn/sikk_stable_trader_os/06_phase_controllers/P00_system_bootstrap_controller/state_writeback_policy.yaml

/root/sikk-gmgn/sikk_stable_trader_os/06_phase_controllers/P00_system_bootstrap_controller/handoff_packet.schema.json

/root/sikk-gmgn/sikk_stable_trader_os/06_phase_controllers/P00_system_bootstrap_controller/p00_bootstrap_report.template.json
```

---

# 五、P00 context.md 必须包含

```text
1. P00 阶段定位。
2. P00 是系统建造与方法论编译控制器。
3. P00 不是业务阶段。
4. P00 不是交易阶段。
5. P00 上游是 K00。
6. P00 必须读取 system_methodology_blueprint.md。
7. P00 必须读取 K00 phase_controller_candidate_spec。
8. P00 必须读取 K00_to_P00_handoff_packet。
9. P00 负责生成 Control Plane。
10. P00 负责生成 phase registry。
11. P00 负责生成 system asset index。
12. P00 负责生成 trace matrix。
13. P00 负责生成 acceptance policy。
14. P00 负责生成 handoff registry。
15. P00 负责创建 P01-P10 controller stub。
16. P00 必须阻断 P01。
17. P00 默认 paper_only=true。
18. P00 默认 real_trade_enabled=false。
```

---

# 六、P00 controller.yaml 必须包含

```yaml
controller_id: P00_system_bootstrap_controller
controller_name_cn: 系统建造与方法论编译控制器
version: v1.0-institutional
status: LANDED_PENDING_ACCEPTANCE
controller_type: system_bootstrap_and_methodology_compiler

primary_goal: >
  将 K00 生成的知识资产、Phase Controller 候选规格和 system_methodology_blueprint.md
  编译为正式系统结构，包括治理平面、领域平面、数据平面、控制平面、阶段注册表、
  资产索引、追踪矩阵、验收矩阵、下游交接包和 P01-P10 Phase Controller stub。

authority_scope:
  can:
    - 读取 system_methodology_blueprint.md
    - 读取 K00 phase_controller_candidate_spec
    - 读取 K00_to_P00_handoff_packet
    - 扫描系统目录结构
    - 建立 current_system_state.json
    - 建立 phase_registry.yaml
    - 建立 system_asset_index.json
    - 建立 task_consumption_log.json
    - 建立 trace matrix
    - 建立 acceptance policy
    - 建立 handoff registry
    - 创建 P01-P10 controller stub
    - 裁决下一合法阶段
    - 阻断非法阶段

  cannot:
    - 执行真实交易
    - 生成买卖指令
    - 启动 P01-P10 业务运行
    - 绕过 Data Plane
    - 绕过 Control Plane
    - 把文件级验收当成系统级验收
    - 把 K00 候选规格直接当成正式控制器

required_inputs:
  - 00_methodology/system_methodology_blueprint.md
  - 00_knowledge_intake/phase_controller_candidates/
  - 00_knowledge_intake/handoff_packets/

required_outputs:
  - 00_control/current_system_state.json
  - 00_control/phase_registry.yaml
  - 00_control/system_asset_index.json
  - 00_control/task_consumption_log.json
  - 00_control/current_blockers.json
  - 00_control/next_stage_decision.json
  - 00_trace/methodology_implementation_trace_matrix.yaml
  - 00_trace/asset_consumption_matrix.yaml
  - 00_trace/acceptance_coverage_matrix.yaml
  - 08_acceptance/global_acceptance_policy.yaml
  - 09_handoff/handoff_packet_registry.yaml

safety_policy:
  paper_only: true
  real_trade_enabled: false
  auto_order_allowed: false
  private_key_allowed: false
  seed_phrase_allowed: false

default_next_legal_stage: P00_BOOTSTRAP_EXECUTION
p01_runtime_connection_allowed: false
```

---

# 七、P00 input_contract.json 必须检查

```json
{
  "contract_id": "P00_INPUT_CONTRACT_001",
  "stage": "P00_system_bootstrap_controller",
  "required_inputs": [
    {
      "name": "system_methodology_blueprint",
      "path": "00_methodology/system_methodology_blueprint.md",
      "required": true,
      "missing_policy": "BLOCK_P00"
    },
    {
      "name": "k00_phase_controller_candidate_spec",
      "path": "00_knowledge_intake/phase_controller_candidates/",
      "required": true,
      "missing_policy": "BLOCK_P00"
    },
    {
      "name": "k00_to_p00_handoff_packet",
      "path": "00_knowledge_intake/handoff_packets/",
      "required": true,
      "missing_policy": "BLOCK_P00"
    }
  ],
  "forbidden_inputs": [
    "private_key",
    "seed_phrase",
    "direct_real_trade_instruction",
    "unverified_live_buy_signal"
  ],
  "safety_boundary": {
    "paper_only": true,
    "real_trade_enabled": false,
    "auto_order_allowed": false
  }
}
```

---

# 八、P00 output_contract.json 必须定义

```json
{
  "contract_id": "P00_OUTPUT_CONTRACT_001",
  "stage": "P00_system_bootstrap_controller",
  "required_outputs": [
    "00_control/current_system_state.json",
    "00_control/phase_registry.yaml",
    "00_control/system_asset_index.json",
    "00_control/task_consumption_log.json",
    "00_control/current_blockers.json",
    "00_control/next_stage_decision.json",
    "00_trace/methodology_implementation_trace_matrix.yaml",
    "00_trace/asset_consumption_matrix.yaml",
    "00_trace/domain_to_data_trace_matrix.yaml",
    "00_trace/data_to_phase_trace_matrix.yaml",
    "00_trace/acceptance_coverage_matrix.yaml",
    "08_acceptance/global_acceptance_policy.yaml",
    "09_handoff/handoff_packet_registry.yaml",
    "06_phase_controllers/P00_system_bootstrap_controller/reports/p00_landing_acceptance_report.json"
  ],
  "required_controller_stubs": [
    "06_phase_controllers/P01_data_fact_controller/controller.yaml",
    "06_phase_controllers/P02_wallet_structure_controller/controller.yaml",
    "06_phase_controllers/P03_chip_control_controller/controller.yaml",
    "06_phase_controllers/P04_market_structure_controller/controller.yaml",
    "06_phase_controllers/P05_scenario_classification_controller/controller.yaml",
    "06_phase_controllers/P06_strategy_gate_controller/controller.yaml",
    "06_phase_controllers/P07_execution_risk_controller/controller.yaml",
    "06_phase_controllers/P08_paper_trading_controller/controller.yaml",
    "06_phase_controllers/P09_review_learning_controller/controller.yaml",
    "06_phase_controllers/P10_system_upgrade_controller/controller.yaml"
  ],
  "output_invariants": [
    "P01 must not be READY before Data Plane acceptance.",
    "paper_only must be true.",
    "real_trade_enabled must be false.",
    "p01_runtime_connection_allowed must be false."
  ]
}
```

---

# 九、P00 task_tree.yaml 必须包含任务树

```yaml
task_tree_id: P00_LANDING_AND_ACCEPTANCE_TASK_TREE_001
stage: P00_system_bootstrap_controller

root_task:
  task_id: P00_ROOT
  name_cn: P00 控制器落盘与验收
  goal: 将 P00 从设计状态推进为正式落盘并完成自检验收

tasks:
  - task_id: P00_T01
    name_cn: 创建 P00 目录
    output:
      - 06_phase_controllers/P00_system_bootstrap_controller/

  - task_id: P00_T02
    name_cn: 创建 P00 控制器文件组
    output:
      - context.md
      - controller.yaml
      - input_contract.json
      - output_contract.json
      - task_tree.yaml
      - acceptance_gate.yaml
      - runner_binding.yaml
      - state_writeback_policy.yaml
      - handoff_packet.schema.json
      - p00_bootstrap_report.template.json

  - task_id: P00_T03
    name_cn: 创建系统控制面目录
    output:
      - 00_control/
      - 00_trace/
      - 08_acceptance/
      - 09_handoff/

  - task_id: P00_T04
    name_cn: 执行文件级验收
    checks:
      - required_files_exist
      - json_files_parse
      - yaml_files_parse

  - task_id: P00_T05
    name_cn: 执行结构级验收
    checks:
      - p00_has_input_contract
      - p00_has_output_contract
      - p00_has_acceptance_gate
      - p00_has_state_writeback_policy
      - p00_has_handoff_schema

  - task_id: P00_T06
    name_cn: 执行安全级验收
    checks:
      - paper_only_true
      - real_trade_enabled_false
      - p01_runtime_connection_allowed_false

  - task_id: P00_T07
    name_cn: 生成 P00 落盘验收报告
    output:
      - 06_phase_controllers/P00_system_bootstrap_controller/reports/p00_landing_acceptance_report.json

  - task_id: P00_T08
    name_cn: 裁决下一合法阶段
    output:
      - next_legal_stage: P00_BOOTSTRAP_EXECUTION
```

---

# 十、P00 acceptance_gate.yaml 必须包含

```yaml
acceptance_gate_id: P00_LANDING_ACCEPTANCE_GATE_001
stage: P00_system_bootstrap_controller

file_level:
  required_files:
    - context.md
    - controller.yaml
    - input_contract.json
    - output_contract.json
    - task_tree.yaml
    - acceptance_gate.yaml
    - runner_binding.yaml
    - state_writeback_policy.yaml
    - handoff_packet.schema.json
    - p00_bootstrap_report.template.json

structure_level:
  required_checks:
    - controller_has_authority_scope
    - controller_has_required_inputs
    - controller_has_required_outputs
    - controller_has_safety_policy
    - input_contract_exists
    - output_contract_exists
    - task_tree_exists
    - state_writeback_policy_exists
    - handoff_schema_exists

semantic_level:
  required_checks:
    - p00_defined_as_system_bootstrap_controller
    - p00_not_business_stage
    - p00_consumes_k00
    - p00_consumes_methodology_blueprint
    - p00_blocks_p01_before_data_plane

safety_level:
  required_checks:
    - paper_only_true
    - real_trade_enabled_false
    - auto_order_allowed_false
    - p01_runtime_connection_allowed_false

hard_fail_conditions:
  - missing_controller_yaml
  - missing_input_contract
  - missing_output_contract
  - missing_acceptance_gate
  - p01_runtime_connection_allowed_true
  - real_trade_enabled_true
  - private_key_detected
  - seed_phrase_detected

success_state:
  p00_landing_acceptance_passed: true
  p00_status: LANDED_AND_ACCEPTANCE_CHECKED
  next_legal_stage: P00_BOOTSTRAP_EXECUTION
  p01_runtime_connection_allowed: false
  paper_only: true
  real_trade_enabled: false
```

---

# 十一、P00 landing acceptance report 标准输出

保存为：

```text
/root/sikk-gmgn/sikk_stable_trader_os/06_phase_controllers/P00_system_bootstrap_controller/reports/p00_landing_acceptance_report.json
```

内容结构：

```json
{
  "report_id": "P00_LANDING_ACCEPTANCE_REPORT_20260511",
  "stage": "P00_system_bootstrap_controller",
  "task": "P00_SYSTEM_BOOTSTRAP_CONTROLLER_LANDING_AND_ACCEPTANCE",
  "p00_landing_acceptance_passed": false,

  "file_level": {
    "passed": false,
    "missing_files": [],
    "created_files": [],
    "parse_errors": []
  },

  "structure_level": {
    "passed": false,
    "controller_yaml_exists": false,
    "input_contract_exists": false,
    "output_contract_exists": false,
    "task_tree_exists": false,
    "acceptance_gate_exists": false,
    "runner_binding_exists": false,
    "state_writeback_policy_exists": false,
    "handoff_schema_exists": false
  },

  "semantic_level": {
    "passed": false,
    "p00_defined_as_system_bootstrap_controller": false,
    "p00_consumes_k00": false,
    "p00_consumes_methodology_blueprint": false,
    "p00_blocks_p01": false
  },

  "safety_level": {
    "passed": false,
    "paper_only": true,
    "real_trade_enabled": false,
    "auto_order_allowed": false,
    "p01_runtime_connection_allowed": false
  },

  "current_status_after_task": {
    "p00_status": "LANDED_AND_ACCEPTANCE_CHECKED",
    "p01_status": "BLOCKED_BY_DATA_PLANE",
    "next_legal_stage": "P00_BOOTSTRAP_EXECUTION",
    "system_integration_repaired": false
  },

  "blocking_gaps": [],
  "non_blocking_gaps": [],
  "next_actions": [
    "Run P00_BOOTSTRAP_EXECUTION to generate Control Plane, Phase Registry, Asset Index, Trace Matrix, Acceptance Policy and Handoff Registry."
  ]
}
```

---

# 十二、当前任务完成后的正确系统状态

P00 落盘验收通过后，状态应更新为：

```json
{
  "current_authoritative_stage": "P00_system_bootstrap_controller",
  "p00_status": "LANDED_AND_ACCEPTANCE_CHECKED",
  "control_plane_status": "PENDING_BOOTSTRAP_EXECUTION",
  "governance_plane_status": "PENDING",
  "domain_plane_status": "PENDING",
  "data_plane_status": "PENDING",
  "p01_runtime_connection_allowed": false,
  "next_legal_stage": "P00_BOOTSTRAP_EXECUTION",
  "paper_only": true,
  "real_trade_enabled": false
}
```

注意：

```text
system_integration_repaired = false
```

这是正确状态。

因为 P00 只是落盘并验收，还没有真正执行系统编译。

---

# 十三、HER 执行指令

直接发给 HER：

```text
任务名称：
P00_SYSTEM_BOOTSTRAP_CONTROLLER_LANDING_AND_ACCEPTANCE

任务类型：
P00 系统建造控制器落盘与验收任务。
不是 P01 运行任务。
不是自动化交易任务。
不是真实交易任务。

目标：
将 P00_system_bootstrap_controller 正式落盘为可被 HER 读取、验证、执行和回写的阶段控制器文件组。
完成后生成 P00 landing acceptance report。
本任务只完成 P00 落盘与验收，不执行 P00 bootstrap，不启动 P01。

必须创建目录：
/root/sikk-gmgn/sikk_stable_trader_os/06_phase_controllers/P00_system_bootstrap_controller/
/root/sikk-gmgn/sikk_stable_trader_os/06_phase_controllers/P00_system_bootstrap_controller/reports/
/root/sikk-gmgn/sikk_stable_trader_os/00_control/
/root/sikk-gmgn/sikk_stable_trader_os/00_trace/
/root/sikk-gmgn/sikk_stable_trader_os/08_acceptance/
/root/sikk-gmgn/sikk_stable_trader_os/09_handoff/

必须创建文件：
1. 06_phase_controllers/P00_system_bootstrap_controller/context.md
2. 06_phase_controllers/P00_system_bootstrap_controller/controller.yaml
3. 06_phase_controllers/P00_system_bootstrap_controller/input_contract.json
4. 06_phase_controllers/P00_system_bootstrap_controller/output_contract.json
5. 06_phase_controllers/P00_system_bootstrap_controller/task_tree.yaml
6. 06_phase_controllers/P00_system_bootstrap_controller/acceptance_gate.yaml
7. 06_phase_controllers/P00_system_bootstrap_controller/runner_binding.yaml
8. 06_phase_controllers/P00_system_bootstrap_controller/state_writeback_policy.yaml
9. 06_phase_controllers/P00_system_bootstrap_controller/handoff_packet.schema.json
10. 06_phase_controllers/P00_system_bootstrap_controller/p00_bootstrap_report.template.json
11. 06_phase_controllers/P00_system_bootstrap_controller/reports/p00_landing_acceptance_report.json

文件要求：
- controller.yaml 必须明确 P00 是系统建造与方法论编译控制器。
- controller.yaml 必须明确 P00 消费 K00 与 system_methodology_blueprint.md。
- controller.yaml 必须明确 P00 禁止真实交易。
- controller.yaml 必须明确 P00 禁止启动 P01。
- input_contract.json 必须定义 P00 必须读取的方法论蓝图、K00 candidate spec、K00 handoff。
- output_contract.json 必须定义 P00 后续要生成的 Control Plane、Trace Plane、Acceptance Plane、Handoff Plane 和 P01-P10 stubs。
- acceptance_gate.yaml 必须区分文件级、结构级、语义级、安全级验收。
- state_writeback_policy.yaml 必须明确 P00 当前只能写入 P00 落盘验收状态，不能把 P01 标记为 READY。
- handoff_packet.schema.json 必须保持 p01_runtime_connection_allowed=false。

验收标准：
1. P00 目录存在。
2. P00 必要文件全部存在。
3. JSON 文件可解析。
4. YAML 文件可解析。
5. P00 controller 明确 authority_scope。
6. P00 input_contract 明确 required_inputs。
7. P00 output_contract 明确 required_outputs。
8. P00 acceptance_gate 明确 hard_fail_conditions。
9. P00 state_writeback_policy 明确 p01_runtime_connection_allowed=false。
10. P00 landing acceptance report 已生成。
11. paper_only=true。
12. real_trade_enabled=false。
13. P01 未被启动。
14. P01 未被标记为 READY。
15. 下一合法阶段是 P00_BOOTSTRAP_EXECUTION。

失败条件：
- 缺少 controller.yaml。
- 缺少 input_contract.json。
- 缺少 output_contract.json。
- 缺少 acceptance_gate.yaml。
- 任一 JSON/YAML 不可解析。
- real_trade_enabled=true。
- p01_runtime_connection_allowed=true。
- P01 被标记为 READY。
- 试图运行自动化交易 workflow。

最终输出：
1. 创建文件清单。
2. 备份文件清单。
3. 验收结果。
4. 当前 P00 状态。
5. 当前 P01 状态。
6. 下一合法阶段。
7. 是否允许进入 P01：必须回答否。
```

---

# 十四、执行完成后的下一步

本任务完成后，不是进 P01。

下一步是：

```text
P00_BOOTSTRAP_EXECUTION
```

目标是让 P00 真正生成：

```text
00_control/current_system_state.json
00_control/phase_registry.yaml
00_control/system_asset_index.json
00_trace/methodology_implementation_trace_matrix.yaml
08_acceptance/global_acceptance_policy.yaml
09_handoff/handoff_packet_registry.yaml
```

最终顺序仍然是：

```text
P00 落盘与验收
  ↓
P00 Bootstrap Execution
  ↓
Control Plane 生成
  ↓
Governance Plane 生成
  ↓
Domain Plane 生成
  ↓
Data Plane 生成
  ↓
Data Plane Acceptance Review
  ↓
P01 Preflight
  ↓
P01 READY_FOR_EXECUTE
```

当前裁决：

```text
P01 仍然禁止启动。
下一合法阶段：P00_BOOTSTRAP_EXECUTION。
```