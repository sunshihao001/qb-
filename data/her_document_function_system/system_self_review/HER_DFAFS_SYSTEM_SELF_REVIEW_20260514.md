# 文档自动化处理系统体系梳理与补全任务包

- report_id: HER-DFAFS-SYSTEM-SELF-REVIEW-20260514
- system_root: `/root/sikk-gmgn/system/her_document_function_system/`
- data_root: `/root/sikk-gmgn/data/her_document_function_system/`
- repo_root: `/root/sikk-gmgn/`
- review_method: 使用文档自动化处理系统自身的 HER 阶段体系反向梳理自身，即按 G00/O00/K00/F00/V00/R00/A00/H00/U00 分层检查系统定义、运行数据、控制面、验收面与缺口闭环。
- status: `SYSTEM_BLUEPRINT_AND_SAFE_MODE_RUNTIME_PARTIALLY_READY_WITH_GAPS`

## 1. 总结判断

文档自动化处理系统已经不只是单份文档或单脚本，而是形成了一个较完整的 HER 文档→功能→验证→队列→治理闭环体系：

- 系统定义层已存在：`README.md`、`CANONICAL_ROUTE.json`、`registry/`、`config/`、`controllers/`、`orchestrator/`、`governance/`、`acceptance/`、`handoff/`、`validation/`、`cli/` 等。
- 阶段控制器资产较完整：A00/F00/G00/H00/O00/R00/U00/V00 控制器目录均有 manifest、input/output contract、execution protocol、acceptance gate、state、handoff schema 等基础文件。
- 运行数据层已存在：`k00_runs`、`f00_runs`、`v00_runs`、`r00_runs`、`a00_runs`、`h00_runs`、`o00_runs`、`o00_run_document_runs`、`cli_runs`、`*_real_*_runs`、`runtime_index`、`kv`、`passports`、`handoff`、`gaps`、`system_mapping`、`acceptance` 等。
- 真实工具层已存在：`tools/o00_cli.py`、`tools/o00_run_document_main.py`、`tools/k00_document_intake.py`、`tools/f00_function_mapping.py`、`tools/v00_validation_evidence.py`、`tools/a00_acceptance.py`、`tools/h00_downstream_queue.py`、`tools/u00_review_upgrade.py`、`tools/g00_governance_update.py` 等。
- 测试层已存在：`tests/her_document_function_system/` 下覆盖 controller registry、pipeline config、V00、A00、H00、G00 等规则测试；repo 根 tests 还有 O00 CLI、O00 run document、F00/V00/R00 等测试。

但系统目前仍应被标记为：

- `RUNNABLE_WITH_GAPS`：可以安全模式运行文档处理链路并产出阶段文件。
- 不是 `PRODUCTION_READY`。
- 不是 `PIPELINE_ACCEPTED` 全闭环。
- 不是 `POLICY_ACTIVE` 全局治理已生效。
- 不是 `RUNNER_BOUND` 真实调度器/生产 runner 已绑定。

核心缺口不是“完全没有体系”，而是：**系统设计资产很完整，safe-mode 运行链路已出现，但系统定义层、真实工具层、运行产物层之间存在双轨/命名/证据强度不一致，需要补一个系统自身的 canonical inventory、阶段状态矩阵、数据契约矩阵和 gap closure backlog。**

## 2. 系统自身阶段链路抽象

按系统自身 HER 体系，应抽象为以下主链路：

1. G00 Governance Boundary / Policy Load
   - 职责：加载治理边界、状态码、证据规则、gap 规则、禁止动作规则。
   - 当前资产：`governance/g00_real_policy_registry/`、`controllers/G00_governance_boundary_controller/`、`config/pipeline_config.safe_mode.json`。
   - 当前状态：政策候选和边界文件较完整，但不能声明 `POLICY_ACTIVE`。

2. O00 Full Pipeline Orchestrator / CLI Entry
   - 职责：作为总控，接受 document + goal，执行 safe-mode pipeline，生成 trace/audit/report。
   - 当前资产：`orchestrator/o00_run_document_safe_mode/`、`controllers/O00_full_pipeline_orchestrator/`、`cli/`、`tools/o00_cli.py`、`tools/o00_run_document_main.py`。
   - 当前状态：有两个实现轨道：
     - `tools/o00_cli.py`：偏 design-level replay，产出 `o00_runs` 和 `o00_run_document_runs` 下的模拟/安全证据。
     - `tools/o00_run_document_main.py`：偏真实文档 safe-mode 文件流水线，直接调用 K00/F00/V00/A00/H00/U00/G00 工具并输出到指定 run 目录。

3. K00 Intake / Document Understanding
   - 职责：保存原始文档、生成 document passport、corpus index、system mapping、K00 handoff。
   - 当前工具：`tools/k00_document_intake.py`。
   - 当前状态：能生成基础事实文件，但语义抽取较模板化，仍是 `K00_READY_WITH_GAPS`。

4. F00 Function Realization Mapping
   - 职责：将文档意图映射为功能项、系统资产、实现任务包、F00 handoff。
   - 当前工具：`tools/f00_function_mapping.py`。
   - 当前状态：能输出功能映射和任务包，但 mapped functions 偏固定模板，未真正细粒度吸收文档内容；应保持 `F00_FUNCTION_MAPPING_READY_WITH_GAPS`。

5. V00 Validation Evidence
   - 职责：检查 K00/F00 输出、生成 validation matrix、gap register、evidence report、V00 handoff。
   - 当前工具：`tools/v00_validation_evidence.py`。
   - 当前状态：可验证基础文件存在，但尚未进行 schema-level/field-level 深验证；应保持 `V00_REAL_VALIDATION_EVIDENCE_READY_WITH_GAPS`。

6. R00 Runner Tool Binding
   - 职责：runner/CLI/tool/orchestrator binding 的安全 dry-run 或绑定设计。
   - 当前资产：`controllers/R00_runner_tool_binding_controller/`、`r00_real_binding_runs/`、相关测试。
   - 当前状态：设计资产存在，真实 production runner binding 未启用；多数 run 中 R00 被跳过或 DESIGN_ONLY。

7. A00 Acceptance Evidence
   - 职责：基于证据矩阵给出 READY_WITH_GAPS/BLOCKED/ACCEPTED 等状态，阻止假 ready。
   - 当前工具：`tools/a00_acceptance.py`。
   - 当前状态：可以生成 readiness certificate 和 acceptance result，但对 open gaps 的分级与最终状态仍偏宽松，需要更细的 status policy。

8. H00 Handoff Downstream Queue
   - 职责：把 gap 和后续任务写入下游队列，不直接执行。
   - 当前工具：`tools/h00_downstream_queue.py`。
   - 当前状态：可生成 queue/routing/handoff packets，但 queue item 尚未形成统一任务执行闭环。

9. U00 Review Upgrade
   - 职责：把 gap 转为 review case、root cause、upgrade queue、learning index。
   - 当前工具：`tools/u00_review_upgrade.py`。
   - 当前状态：可生成升级队列，但未绑定自动补全/回写控制器资产的执行器。

10. G00 Governance Candidate Update
   - 职责：把重复问题沉淀为治理候选，不直接变成 active policy。
   - 当前工具：`tools/g00_governance_update.py`。
   - 当前状态：可产出候选规则，但缺少正式 policy activation / consumption / conflict check 的闭环执行。

## 3. 数据层现状

### 3.1 系统定义数据

- `system/her_document_function_system/README.md`：系统总览。
- `system/her_document_function_system/CANONICAL_ROUTE.json`：canonical route。
- `system/her_document_function_system/registry/controller_registry.json`：控制器注册表。
- `system/her_document_function_system/config/pipeline_config.safe_mode.json`：safe-mode stage plan 与边界。
- `system/her_document_function_system/controllers/*`：各阶段控制器文件包。
- `system/her_document_function_system/cli/*`：CLI entry 文档/契约。
- `system/her_document_function_system/orchestrator/o00_run_document_safe_mode/*`：O00 safe-mode 编排器定义。

### 3.2 运行数据

已观测到的主要运行目录：

- `data/her_document_function_system/k00_runs/`：4 个目录。
- `data/her_document_function_system/f00_runs/`：3 个目录。
- `data/her_document_function_system/v00_runs/`：1 个目录。
- `data/her_document_function_system/r00_runs/`：1 个目录。
- `data/her_document_function_system/a00_runs/`：1 个目录 + 1 个验证文件。
- `data/her_document_function_system/h00_runs/`：1 个目录。
- `data/her_document_function_system/u00_runs/`：空。
- `data/her_document_function_system/g00_runs/`：空。
- `data/her_document_function_system/o00_runs/`：45 个目录。
- `data/her_document_function_system/o00_run_document_runs/`：21 个目录/基础子目录混合。
- `data/her_document_function_system/cli_runs/`：152 个 CLI run 目录。
- `data/her_document_function_system/v00_real_validation_runs/`：1 个目录。
- `data/her_document_function_system/r00_real_binding_runs/`：1 个目录。
- `data/her_document_function_system/a00_real_acceptance_runs/`：1 个目录。
- `data/her_document_function_system/h00_real_queue_runs/`：1 个目录。
- `data/her_document_function_system/u00_real_review_runs/`：2 个目录。
- `data/her_document_function_system/g00_real_policy_runs/`：1 个目录。

判断：运行数据已经丰富，但缺一个统一的 `system_self_review/` 或 `inventory/` 汇总层，把这些运行目录和阶段状态映射成一个可读的系统健康画像。

## 4. 控制面现状

控制面由四类资产构成：

1. Registry 控制面
   - `registry/controller_registry.json`
   - `registry/controller_capability_matrix.json`
   - `registry/controller_contract_index.json`
   - `registry/controller_dependency_graph.json`
   - `registry/controller_handoff_index.json`
   - `registry/controller_policy_binding.json`
   - `registry/controller_status_index.json`

2. Config 控制面
   - `config/pipeline_config.safe_mode.json`
   - `config/pipeline_config.default.json`
   - `config/pipeline_config.design_only.json`
   - `config/pipeline_config.full_safe_replay.json`
   - `config/pipeline_config.validation_only.json`
   - `config/execution_boundary.default.json`
   - `config/replay_policy.default.json`
   - `config/write_policy.default.json`

3. Controller file pack 控制面
   - A00/F00/G00/H00/O00/R00/U00/V00 均有 manifest、contracts、protocol、acceptance gate、state、handoff schema。
   - 但 registry 中包含 K00，而当前 `controllers/` 目录扫描未发现独立 `K00_*_controller` 文件包；K00 有运行工具和 run 数据，但控制器定义可能在别处或缺失。

4. CLI / Tool 控制面
   - `tools/o00_cli.py` 提供 init/validate-config/run-sample/run-document/status/show-gaps/show-report/recover/resume 等入口。
   - `tools/o00_run_document_main.py` 提供真实文档 safe-mode 流水线。
   - 当前存在“双轨入口”：CLI design-level replay 与 real document main runner 的状态码、目录结构、产物 schema 不完全统一。

## 5. 验收面现状

当前验收面具备：

- A00 控制器资产与 real acceptance 目录。
- `tools/a00_acceptance.py` 可以输出：
  - `a00/acceptance_matrix.json`
  - `a00/readiness_certificate.json`
  - `a00/a00_acceptance_result.json`
- 测试覆盖：
  - 不允许 open gaps 下声明 pipeline accepted。
  - readiness certificate 必须有字段。
  - phase status matrix 必须包含阶段。
  - artifact manifest 必须有资产。
  - gap propagation 必须保留 open gaps。
  - G00 policy 不得未激活却声明 active。

但验收面仍有缺口：

- `tools/a00_acceptance.py` 当前只读 `v00/gap_register.json`，没有完整读取 K00/F00/V00/R00/H00/U00/G00 的阶段证据矩阵。
- 当前 final status 使用 `HER_DOC_FUNCTION_PIPELINE_RUNNABLE_WITH_GAPS`，与 config/registry 中 `PIPELINE_READY_WITH_GAPS`、`A00_READY_WITH_GAPS`、`DESIGN_ONLY` 等状态体系需要建立状态码映射表。
- 缺统一 `artifact_manifest` 汇总每个 run 的所有关键文件、sha256、schema 校验结果。

## 6. 关键缺口清单

### GAP-001: K00 controller file pack 缺失或未纳入 canonical controller scan

- 现象：`controller_registry.json` 和 stage plan 都要求 K00，但 `/system/her_document_function_system/controllers/` 目录扫描到 A00/F00/G00/H00/O00/R00/U00/V00，没有 K00 独立控制器目录。
- 影响：系统入口阶段的 contract/protocol/acceptance gate 不能和其他阶段同级治理。
- 建议任务：创建或定位并注册 `controllers/K00_document_intake_controller/`，补齐 01-09 基础文件和必要 schema。
- 优先级：P0。

### GAP-002: O00 双轨运行体系未统一

- 现象：`tools/o00_cli.py` 使用 `make_pipeline_run()` 生成 design-level replay 结构；`tools/o00_run_document_main.py` 调用真实 K00/F00/V00/A00/H00/U00/G00 工具生成另一套 `runs/her_doc_run_*` 结构。
- 影响：同一个系统有两套 run shape、状态码、报告路径，不利于长期自动化。
- 建议任务：定义 `run_shape_contract_v1`，统一 `o00_runs`、`o00_run_document_runs`、`runs/` 的目录语义；CLI run-document 应显式调用或包装 `o00_run_document_main.py` 的真实 safe-mode runner，而不是仅模拟。
- 优先级：P0。

### GAP-003: F00 仍是模板映射，不是真正文档功能抽取

- 现象：`tools/f00_function_mapping.py` 固定生成 8 个功能项，不根据输入文档的细粒度需求变化。
- 影响：用户要求“把文档内容转成方法护照、逻辑库、字段合约、模块地图、规则模板、输出合约、下一轮实现任务”尚未完全实现。
- 建议任务：F00 增加文档资产六分类抽取：判断逻辑资产、字段需求资产、反证规则资产、量化模型资产、行为推断资产、输出模板资产；再映射到方法护照/逻辑库/字段合约/模块地图/规则模板/输出合约/实现任务。
- 优先级：P0。

### GAP-004: V00 验证粒度不足

- 现象：`tools/v00_validation_evidence.py` 主要验证文件存在，不做 JSON schema、字段必填、状态码一致性、handoff refs 可解析检查。
- 影响：容易把“文件存在”误判为“证据充分”。
- 建议任务：V00 增加 schema validator、field validator、status transition validator、handoff ref resolver。
- 优先级：P1。

### GAP-005: A00 验收缺全阶段 artifact manifest 和 evidence bundle

- 现象：`tools/a00_acceptance.py` 只输出简化 matrix/certificate/result。
- 影响：不能稳定回答“系统数据是否完善”。
- 建议任务：A00 生成 `artifact_manifest.json`、`phase_status_matrix.json`、`evidence_bundle.json`、`gap_propagation_report.json`，并纳入 final report。
- 优先级：P1。

### GAP-006: H00/U00/G00 后续闭环只排队，不自动回写系统补全

- 现象：H00 只 QUEUED，U00 只 upgrade QUEUED，G00 只 candidate。
- 影响：系统能发现问题，但补全闭环依赖人工。
- 建议任务：新增 safe-mode `upgrade_executor_plan`，先只写计划和 patch proposal，不自动改 production policy。
- 优先级：P1。

### GAP-007: Runtime index 未成为强制入口

- 现象：存在 `runtime_index/her_dfafs_runtime_index.json`，但运行工具并未统一写入/读取该 index。
- 影响：运行数据多但分散，系统健康状态不可一眼判断。
- 建议任务：O00 每次 run 结束强制更新 `runtime_index/run_index.json` 与 `runtime_index/system_health_snapshot.json`。
- 优先级：P1。

### GAP-008: 状态码体系需统一

- 现象：出现 `DESIGN_ONLY`、`READY_WITH_GAPS`、`RUNNABLE_WITH_GAPS`、`PIPELINE_READY_WITH_GAPS`、`*_ACCEPTED` 等多套表达。
- 影响：自动验收和下游路由容易误判。
- 建议任务：建立 `status_code_mapping.json`，将工具状态码映射到 controller policy 状态码，并明确禁止转换：`READY_WITH_GAPS != ACCEPTED`。
- 优先级：P1。

## 7. 补全文档/任务包

### TASK-P0-001: 补 K00 控制器文件包

- target: `system/her_document_function_system/controllers/K00_document_intake_controller/`
- outputs:
  - `01_k00_manifest.yaml`
  - `02_k00_context_pack.md`
  - `03_k00_objective_tree.yaml`
  - `04_k00_input_contract.json`
  - `05_k00_output_contract.json`
  - `06_k00_execution_protocol.md`
  - `07_k00_acceptance_gate.yaml`
  - `08_k00_state.json`
  - `09_k00_handoff_packet.schema.json`
  - `10_document_passport.schema.json`
  - `11_corpus_index.schema.json`
  - `12_system_mapping.schema.json`
  - `13_gap_detection.schema.json`
- acceptance:
  - registry 中 K00 path 指向该目录。
  - validate-config 不再出现 K00 controller file pack gap。

### TASK-P0-002: 统一 O00 run shape

- target:
  - `system/her_document_function_system/orchestrator/o00_run_shape_contract.schema.json`
  - `tools/o00_cli.py`
  - `tools/o00_run_document_main.py`
- required_decision:
  - `o00_runs/`：保留 sample/design replay。
  - `o00_run_document_runs/`：真实 document safe-mode pipeline run。
  - `runs/`：废弃或仅作为 legacy alias。
- acceptance:
  - `run-document` 产物包含 input/k00/f00/v00/a00/h00/u00/g00/o00/recovery/trace/audit/report。
  - CLI report 和 real runner report 使用同一 final_status 字段。

### TASK-P0-003: F00 文档资产六分类抽取

- target: `tools/f00_function_mapping.py`
- add outputs:
  - `f00/asset_classification.json`
  - `f00/method_passport_plan.json`
  - `f00/logic_library_plan.json`
  - `f00/field_contract_plan.json`
  - `f00/module_map_plan.json`
  - `f00/rule_template_plan.json`
  - `f00/output_contract_plan.json`
  - `f00/next_implementation_tasks.json`
- acceptance:
  - 对任意输入文档，至少能按六类资产输出空数组/命中数组，并给出 evidence_refs。
  - 不允许只输出固定 8 项模板后宣称文档已吸收。

### TASK-P1-004: V00 增加强验证

- target: `tools/v00_validation_evidence.py`
- add validators:
  - required file existence
  - required JSON field check
  - JSON schema check if schema available
  - handoff refs resolvability
  - status code allowed set
  - forbidden claims scan
- acceptance:
  - 输出 `v00/schema_validation_result.json`、`v00/field_validation_result.json`、`v00/status_validation_result.json`、`v00/handoff_ref_validation_result.json`。

### TASK-P1-005: A00 全局证据包

- target: `tools/a00_acceptance.py`
- add outputs:
  - `a00/artifact_manifest.json`
  - `a00/phase_status_matrix.json`
  - `a00/evidence_bundle.json`
  - `a00/gap_propagation_report.json`
- acceptance:
  - artifact_manifest 覆盖 K00/F00/V00/A00/H00/U00/G00/O00。
  - 有 open gaps 时 final_status 只能是 READY/RUNNABLE_WITH_GAPS 或 BLOCKED，不得是 ACCEPTED/PRODUCTION_READY。

### TASK-P1-006: Runtime index / health snapshot

- target:
  - `tools/her_runtime_index.py`
  - `data/her_document_function_system/runtime_index/run_index.json`
  - `data/her_document_function_system/runtime_index/system_health_snapshot.json`
- acceptance:
  - 每个 O00 run 结束自动登记 run_id、run_dir、final_status、open_gap_count、artifact_count、report_path。
  - system health snapshot 能显示各阶段最近一次状态和缺口数。

## 8. 当前可用性结论

- 可以用于：安全模式文档处理、阶段产物生成、设计级/文件级 replay、gap 保留、下游补全任务生成。
- 暂不应用于：生产自动化、实盘/纸面交易 runtime、自动部署、钱包签名、无人工确认的 policy activation。
- 下一轮最值得做：先补 K00 控制器文件包 + 统一 O00 run shape + F00 六类资产抽取。完成这三项后，系统才更接近用户要求的“文档内容自动吸收成方法论资产和实现任务”。
