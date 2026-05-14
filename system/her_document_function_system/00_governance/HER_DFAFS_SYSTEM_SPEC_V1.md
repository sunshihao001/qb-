     1|     1|# HER-DFAFS System Specification v1.0
     2|     2|
     3|     3|**System name:** HER-DFAFS  
     4|     4|**Full name:** HER Document-to-Function Automated Fulfillment System  
     5|     5|**中文名:** HER 文档到功能自动化落实系统  
     6|     6|**定位:** HER 专业化自动化文档处理与功能落实系统
     7|     7|
     8|     8|---
     9|     9|
    10|    10|## 1. 系统总定义
    11|    11|
    12|    12|HER 文档到功能自动化落实系统，是一个用于处理 GPT 解释性研究资料的受控自动化管线。
    13|    13|
    14|    14|它以 K00 为资料入口，以 KV 为长期结构化记忆索引，以 F00 为功能落实核心，以 schema / contract / code / test / replay / runner binding 为系统资产转化链路，以 acceptance evidence 和 handoff packet 作为完成证明，最终把研究资料转化为 HER 本地系统可执行、可验证、可复盘、可升级的功能能力。
    15|    15|
    16|    16|HER-DFAFS 专门处理 GPT 产生的大量解释性、方法论性、策略性、系统建设性资料。
    17|    17|
    18|    18|它的目标不是总结文档，而是把文档变成 HER 本地系统中的：
    19|    19|
    20|    20|- 可登记资料
    21|    21|- 可检索知识
    22|    22|- 可映射系统位置
    23|    23|- 可识别功能需求
    24|    24|- 可设计字段模型
    25|    25|- 可生成 schema / contract
    26|    26|- 可实现代码模块
    27|    27|- 可执行测试
    28|    28|- 可 replay 验证
    29|    29|- 可接入 runner / CLI / Telegram / report
    30|    30|- 可验收
    31|    31|- 可交接
    32|    32|- 可复盘
    33|    33|- 可升级
    34|    34|
    35|    35|**最终目标：** 让 GPT 解释性研究资料不再停留为“文档”，而是被自动编译成 HER 系统可执行、可验证、可审计、可持续升级的功能资产。
    36|    36|
    37|    37|---
    38|    38|
    39|    39|## 2. 总体系统哲学
    40|    40|
    41|    41|### 2.1 文档不是阅读材料
    42|    42|
    43|    43|上传文档不是给 AI 阅读的普通资料，而是潜在系统建设输入。
    44|    44|
    45|    45|文档可能是：
    46|    46|
    47|    47|- 潜在系统建设输入
    48|    48|- 潜在功能需求源
    49|    49|- 潜在规则来源
    50|    50|- 潜在字段定义来源
    51|    51|- 潜在状态机来源
    52|    52|- 潜在验收标准来源
    53|    53|- 潜在 runner / tool binding 来源
    54|    54|- 潜在治理边界来源
    55|    55|
    56|    56|处理文档时，不能只问“这个文档讲了什么？”，必须问：
    57|    57|
    58|    58|- 这个文档要求系统新增什么能力？
    59|    59|- 修改什么能力？
    60|    60|- 阻断什么错误能力？
    61|    61|- 强化什么判断能力？
    62|    62|- 产生什么数据？
    63|    63|- 接入什么阶段？
    64|    64|- 需要什么测试？
    65|    65|- 如何证明已经落实？
    66|    66|
    67|    67|### 2.2 K00 不是终点
    68|    68|
    69|    69|K00 只说明：资料已进入系统、已登记、已索引、已映射、已生成任务化入口。  
    70|    70|K00 不代表功能完成。
    71|    71|
    72|    72|真正的专业自动化文档处理必须继续进入：
    73|    73|
    74|    74|**F00 Function Realization Controller / 功能落实控制器**
    75|    75|
    76|    76|### 2.3 功能落实必须有证据
    77|    77|
    78|    78|如果系统只是生成任务包、建议、设计说明、阶段规划，只能叫 `DESIGN_ONLY`，不能叫 `IMPLEMENTED`、`TESTED` 或 `READY`。
    79|    79|
    80|    80|真正完成必须具备：
    81|    81|
    82|    82|- 文件写入证据
    83|    83|- schema / contract 变更证据
    84|    84|- 代码 patch 证据
    85|    85|- 测试执行证据
    86|    86|- replay 证据
    87|    87|- runner binding 证据
    88|    88|- trace / audit 证据
    89|    89|- acceptance 证据
    90|    90|- handoff 证据
    91|    91|
    92|    92|---
    93|    93|
    94|    94|## 3. 六层总体架构
    95|    95|
    96|    96|- **L0 入口治理层:** 判断资料性质、权限边界、风险边界。
    97|    97|- **L1 资料系统化层:** 把文档变成 HER 可管理资料。
    98|    98|- **L2 功能编译层:** 把解释性内容转成功能需求。
    99|    99|- **L3 资产落实层:** 把功能需求转成系统文件、代码、schema、contract。
   100|   100|- **L4 运行验证层:** 验证功能是否真的能跑。
   101|   101|- **L5 验收交接与复盘升级层:** 证明完成、生成 handoff、进入下游。
   102|   102|
   103|   103|---
   104|   104|
   105|   105|## 4. 全流程主链路
   106|   106|
   107|   107|```text
   108|   108|Document Received
   109|   109|↓
   110|   110|L0 Entry Governance
   111|   111|↓
   112|   112|K00 Knowledge Intake
   113|   113|↓
   114|   114|KV Memory Index
   115|   115|↓
   116|   116|System Mapping
   117|   117|↓
   118|   118|Gap Detection
   119|   119|↓
   120|   120|F00 Function Realization Controller
   121|   121|↓
   122|   122|F01 Concept-to-Function Compiler
   123|   123|↓
   124|   124|F02 Implementation Decision Gate
   125|   125|↓
   126|   126|R01 Repository State Scanner
   127|   127|↓
   128|   128|F03 Asset Planning
   129|   129|↓
   130|   130|F04 Field Model Builder
   131|   131|↓
   132|   132|F05 Rule Logic Builder
   133|   133|↓
   134|   134|F06 Schema / Contract Generator
   135|   135|↓
   136|   136|F07 Patch Writer / Code Realizer
   137|   137|↓
   138|   138|V01 Schema / Contract Validation
   139|   139|↓
   140|   140|V02 Unit Test / Contract Test
   141|   141|↓
   142|   142|V03 End-to-End Replay
   143|   143|↓
   144|   144|R02 Runner / CLI / Tool Binding
   145|   145|↓
   146|   146|A01 Acceptance Evidence Collector
   147|   147|↓
   148|   148|H01 Handoff Packet Writer
   149|   149|↓
   150|   150|U01 Review / Upgrade Loop
   151|   151|```
   152|   152|
   153|   153|硬规则：任何文档只要没有经过 `F00 → V03 → A01 → H01`，不能称为“已落实”。
   154|   154|
   155|   155|---
   156|   156|
   157|   157|## 5. 阶段规范
   158|   158|
   159|   159|### L0 Entry Governance
   160|   160|
   161|   161|目标：判断上传资料是什么，以及允许系统做到哪一步。L0 不能直接进入实现。
   162|   162|
   163|   163|资料类型白名单：
   164|   164|
   165|   165|- `SYSTEM_CONSTRUCTION_DOC`
   166|   166|- `METHODOLOGY_DOC`
   167|   167|- `PHASE_CONTROLLER_DOC`
   168|   168|- `DATA_MODEL_DOC`
   169|   169|- `TRADING_STRATEGY_DOC`
   170|   170|- `RISK_RULE_DOC`
   171|   171|- `SCHEMA_CONTRACT_DOC`
   172|   172|- `RUNNER_BINDING_DOC`
   173|   173|- `TRACE_AUDIT_DOC`
   174|   174|- `REPORT_REVIEW_DOC`
   175|   175|- `GOVERNANCE_DOC`
   176|   176|- `UNKNOWN_DOC`
   177|   177|
   178|   178|标准输出 `task_intent`：
   179|   179|
   180|   180|```json
   181|   181|{
   182|   182|  "task_id": "task_20260513_xxx",
   183|   183|  "doc_id": "doc_20260513_xxx",
   184|   184|  "task_type": "SYSTEM_CONSTRUCTION_DOC",
   185|   185|  "core_goal": "把解释性系统建设资料转化为 HER 可执行功能资产",
   186|   186|  "target_phase_candidate": ["K00", "F00", "P02", "P03"],
   187|   187|  "production_risk_flag": false,
   188|   188|  "forbidden_execution_scope": [
   189|   189|    "live_runtime",
   190|   190|    "wallet_signing",
   191|   191|    "auto_deploy",
   192|   192|    "production_rule_direct_change"
   193|   193|  ],
   194|   194|  "initial_status": "ENTRY_CLASSIFIED"
   195|   195|}
   196|   196|```
   197|   197|
   198|   198|入口验收：必须识别资料类型、目标阶段候选、风险边界、禁止 live/signing/auto deploy，并生成 task intent。
   199|   199|
   200|   200|### K00 Knowledge Intake & Taskization
   201|   201|
   202|   202|目标：把资料纳入 HER 系统，而不是实现功能。
   203|   203|
   204|   204|K00 必须生成：raw input、source registry、document passport、corpus index、system mapping、gap detection、KV memory index、K00 phase state、K00 acceptance、K00 handoff。
   205|   205|
   206|   206|状态：
   207|   207|
   208|   208|- `K00_ACCEPTED`: 资料完整纳入，可进入 F00。
   209|   209|- `K00_READY_WITH_GAPS`: 可进入 F00，但带非阻断缺口。
   210|   210|- `K00_BLOCKED`: 资料有效，但缺关键输入。
   211|   211|- `K00_REJECTED`: 资料不适合进入系统。
   212|   212|
   213|   213|### KV Memory Index
   214|   214|
   215|   215|KV 不是缓存，是 HER 结构化系统记忆索引层。它保存索引、引用、规则摘要、状态摘要、版本关系，不保存原文全文，不替代正式资产。
   216|   216|
   217|   217|KV 类型：
   218|   218|
   219|   219|- `system_rule_kv`
   220|   220|- `phase_definition_kv`
   221|   221|- `contract_kv`
   222|   222|- `schema_kv`
   223|   223|- `field_definition_kv`
   224|   224|- `gap_kv`
   225|   225|- `handoff_kv`
   226|   226|- `state_kv`
   227|   227|- `trace_index_kv`
   228|   228|- `version_kv`
   229|   229|- `forbidden_action_kv`
   230|   230|- `recovery_policy_kv`
   231|   231|
   232|   232|KV 禁止：不得替代 raw、source registry、contract、schema、handoff、phase_state；不得保存私钥/API key、wallet signing 信息；不得把聊天上下文当系统状态；不得把未验收规则写成 `KV_ACCEPTED`。
   233|   233|
   234|   234|### System Mapping
   235|   235|
   236|   236|目标：把文档映射到 HER 系统中的位置。系统位置映射只回答“这个资料影响系统哪里？”，不回答“要具体实现什么功能”。
   237|   237|
   238|   238|映射平面：methodology、governance、control、phase controller、data、schema/contract、KV memory、trace/audit、acceptance/handoff、runner/tool binding、report/review。
   239|   239|
   240|   240|输出字段：`plane`、`affected_phase`、`impact_type`、`risk_level`、`can_modify`、`cannot_modify`。
   241|   241|
   242|   242|### Gap Detection
   243|   243|
   244|   244|目标：识别系统无法从文档直接走到实现的所有缺口。
   245|   245|
   246|   246|Gap 等级：
   247|   247|
   248|   248|- `BLOCKING_GAP`
   249|   249|- `CRITICAL_GAP`
   250|   250|- `HIGH_GAP`
   251|   251|- `MEDIUM_GAP`
   252|   252|- `LOW_GAP`
   253|   253|
   254|   254|Gap 类型：
   255|   255|
   256|   256|- `upstream_source_gap`
   257|   257|- `field_source_gap`
   258|   258|- `input_contract_gap`
   259|   259|- `output_contract_gap`
   260|   260|- `schema_gap`
   261|   261|- `function_mapping_gap`
   262|   262|- `implementation_gap`
   263|   263|- `codebase_scan_gap`
   264|   264|- `test_gap`
   265|   265|- `replay_gap`
   266|   266|- `runner_binding_gap`
   267|   267|- `trace_gap`
   268|   268|- `acceptance_gap`
   269|   269|- `handoff_gap`
   270|   270|- `governance_gap`
   271|   271|- `recovery_policy_gap`
   272|   272|- `KV_conflict_gap`
   273|   273|
   274|   274|### F00 Function Realization Controller
   275|   275|
   276|   276|F00 不是文档处理器。F00 是解释性研究资料到系统功能资产的落实控制器。
   277|   277|
   278|   278|它负责把 K00 handoff 转成：`required_function`、`field_model`、`rule_logic`、`schema`、`contract`、`controller responsibility`、`code module`、`test case`、`replay case`、`runner binding`、`report field`、`trace requirement`、`acceptance evidence`、`downstream handoff`。
   279|   279|


## 6. F00 输入合约

### 6.1 必须输入

F00 不能直接读取聊天上下文作为输入。F00 必须从 K00 handoff 开始。

F00 的唯一合法入口是：

```json
{
  "phase_id": "F00",
  "required_inputs": {
    "k00_handoff_packet": {
      "required": true,
      "description": "K00 交接包，F00 的唯一合法入口"
    },
    "document_passport_refs": {
      "required": true,
      "description": "资料护照引用"
    },
    "corpus_index_refs": {
      "required": true,
      "description": "文档内容索引引用"
    },
    "system_mapping_refs": {
      "required": true,
      "description": "系统位置映射引用"
    },
    "gap_detection_refs": {
      "required": true,
      "description": "K00 发现的缺口"
    },
    "kv_retrieval_refs": {
      "required": false,
      "description": "KV 检索索引，可作为辅助记忆"
    },
    "target_phase_candidates": {
      "required": true,
      "description": "可能被影响的 PXX / IXX / Runner / Review 阶段"
    },
    "execution_boundary": {
      "required": true,
      "description": "执行边界，明确是否允许写文件、写代码、跑测试"
    },
    "write_policy": {
      "required": true,
      "description": "是否允许实际写入系统文件"
    },
    "repo_root": {
      "required": true,
      "description": "当前代码库根目录"
    }
  }
}
```

### 6.2 输入缺失处理

- 无 `k00_handoff_packet`：`F00_BLOCKED`
- 无 `document_passport_refs`：`F00_BLOCKED`
- 无 `corpus_index_refs`：`F00_BLOCKED`
- 无 `system_mapping_refs`：`F00_READY_WITH_GAPS` 或 `F00_BLOCKED`，由缺口等级决定
- 无 `gap_detection_refs`：`F00_BLOCKED`
- 无 `kv_retrieval_refs`：可继续，但必须标记 `KV_GAP`
- 无 `repo_root`：只能 `DESIGN_ONLY`
- 无 `write_policy`：禁止写文件，只能 `DESIGN_ONLY`
- 无 `execution_boundary`：`F00_BLOCKED`

### 6.3 约束落点

该合约已落入：

- `04_function_realization/F00_function_realization_controller/04_f00_input_contract.json`

控制器执行协议必须先加载该 input contract，再读取 K00-approved refs；不得把聊天上下文、KV、历史记忆或普通文档摘要当成 F00 输入源。
   280|   280|### F01 Concept-to-Function Compiler
   281|   281|
   282|   282|目标：把文档里的核心观点逐条编译成功能需求。
   283|   283|
   284|   284|输出 `concept_to_function_map` 字段：`source_concept`、`required_function`、`function_type`、`target_phase`、`input_fields`、`output_fields`、`required_logic`、`required_assets`、`status`。
   285|   285|
   286|   286|`function_type` 白名单：
   287|   287|
   288|   288|- `NEW_FUNCTION`
   289|   289|- `MODIFY_FUNCTION`
   290|   290|- `ENHANCE_FUNCTION`
   291|   291|- `HARD_BLOCK_RULE`
   292|   292|- `SOFT_SCORE_RULE`
   293|   293|- `STATE_MACHINE_RULE`
   294|   294|- `SCHEMA_UPDATE`
   295|   295|- `CONTRACT_UPDATE`
   296|   296|- `TRACE_REQUIREMENT`
   297|   297|- `REPORT_REQUIREMENT`
   298|   298|- `TEST_REQUIREMENT`
   299|   299|- `RUNNER_BINDING`
   300|   300|- `GOVERNANCE_RULE`
   301|   301|- `REVIEW_RULE`
   302|   302|- `KV_INDEX_UPDATE`
   303|   303|- `HANDOFF_UPDATE`
   304|   304|- `RECOVERY_POLICY_UPDATE`
   305|   305|
   306|   306|### F02 Implementation Decision Gate
   307|   307|
   308|   308|目标：判断每个 `required_function` 应该如何落实。不是所有功能都应该马上写代码。
   309|   309|
   310|   310|决策状态：
   311|   311|
   312|   312|- `IMPLEMENT_NOW`
   313|   313|- `DESIGN_ONLY`
   314|   314|- `EXTEND_EXISTING`
   315|   315|- `UPDATE_SCHEMA_ONLY`
   316|   316|- `UPDATE_CONTRACT_ONLY`
   317|   317|- `ADD_TEST_ONLY`
   318|   318|- `ADD_REPORT_ONLY`
   319|   319|- `ADD_KV_ONLY`
   320|   320|- `ADD_TRACE_ONLY`
   321|   321|- `BLOCKED_BY_MISSING_DATA`
   322|   322|- `BLOCKED_BY_PRODUCTION_RISK`
   323|   323|- `BLOCKED_BY_UNKNOWN_CODEBASE`
   324|   324|- `DEFER_TO_DOWNSTREAM_PHASE`
   325|   325|
   326|   326|输出：`function_id`、`decision`、`reason`、`required_inputs`、`blocked_by`、`next_action`。
   327|   327|
   328|   328|### R01 Repository State Scanner
   329|   329|
   330|   330|目标：设计实现前扫描当前代码库状态，避免重复造文件、改错路径、破坏旧系统。
   331|   331|
   332|   332|扫描对象：existing controllers、schemas、contracts、Python modules、tests、runners、reports、legacy paths、config files、docs。
   333|   333|
   334|   334|输出：
   335|   335|
   336|   336|```json
   337|   337|{
   338|   338|  "repo_scan_status": "SCANNED",
   339|   339|  "existing_assets": [],
   340|   340|  "reuse_candidates": [],
   341|   341|  "conflict_assets": [],
   342|   342|  "missing_assets": [],
   343|   343|  "legacy_assets": [],
   344|   344|  "recommended_actions": []
   345|   345|}
   346|   346|```
   347|   347|
   348|   348|### F03 Implementation Asset Planner
   349|   349|
   350|   350|目标：把功能需求拆成系统资产。
   351|   351|
   352|   352|资产类型：schema_file、input_contract、output_contract、controller_file、python_module、function、config_file、cli_command、runner_binding、telegram_command、test_file、replay_sample、trace_spec、audit_log_spec、report_template、dashboard_field、handoff_packet_field、kv_index_entry、recovery_policy。
   353|   353|
   354|   354|输出字段：`function_id`、`asset_type`、`asset_name`、`path`、`action`、`reason`、`acceptance_check`。
   355|   355|
   356|   356|Action 白名单：`CREATE`、`UPDATE`、`EXTEND`、`DEPRECATE`、`BLOCK`、`DESIGN_ONLY`、`PLANNED_NOT_WRITTEN`。
   357|   357|
   358|   358|### F04 Field Model Builder
   359|   359|
   360|   360|目标：所有解释性判断必须转成字段模型。没有字段来源，就不能设计判断逻辑。
   361|   361|
   362|   362|字段属性：`field_name`、`field_type`、`source_module`、`source_path`、`required`、`default_value`、`missing_policy`、`validation_rule`、`evidence_level`、`confidence`、`counter_evidence`、`owner_phase`、`used_by_function`、`output_contract_target`、`handoff_target`、`report_visibility`、`KV_indexed`、`trace_required`。
   363|   363|
   364|   364|### F05 Rule Logic Builder
   365|   365|
   366|   366|目标：把判断逻辑转成可执行规则。禁止只写“由 AI 判断 / 综合判断 / 系统判断”。
   367|   367|
   368|   368|规则结构：
   369|   369|
   370|   370|```json
   371|   371|{
   372|   372|  "rule_id": "rule_xxx",
   373|   373|  "rule_type": "HARD_BLOCK_RULE",
   374|   374|  "input_fields": [],
   375|   375|  "calculation_method": "",
   376|   376|  "threshold_or_condition": "",
   377|   377|  "positive_evidence": [],
   378|   378|  "counter_evidence": [],
   379|   379|  "confidence_logic": "",
   380|   380|  "failure_condition": "",
   381|   381|  "output_status": "",
   382|   382|  "trace_required": true
   383|   383|}
   384|   384|```
   385|   385|
   386|   386|不可数学量化时，至少必须转成 enum、checklist、decision tree、scoring rubric、evidence matrix、hard gate、soft gate、contradiction detector、confidence band。
   387|   387|
   388|   388|### F06 Schema / Contract Generator
   389|   389|
   390|   390|目标：把字段模型和规则输出转成 schema / contract。
   391|   391|
   392|   392|必须生成或更新：`input_contract.json`、`output_contract.json`、`schema.json`、`handoff_packet.schema.json`、`validation_rules.yaml`。
   393|   393|
   394|   394|每个功能必须明确：输入从哪里来、字段是否必填、缺失如何处理、输出给谁、输出结构、失败表示、是否进入 trace/report/handoff。
   395|   395|
   396|   396|### F07 Patch Writer / Code Realizer
   397|   397|
   398|   398|目标：把资产计划转成真实文件变更。
   399|   399|
   400|   400|Patch 输出：`patch_plan.json`、`modified_files.json`、`diff_summary.md`、`change_trace.jsonl`、`rollback_plan.md`。
   401|   401|
   402|   402|状态：`PATCH_PLANNED`、`PATCH_WRITTEN`、`PATCH_APPLIED`、`PATCH_FAILED`、`ROLLBACK_REQUIRED`。
   403|   403|
   404|   404|代码实现必须包含：module_name、file_path、functions、function_inputs、function_outputs、error_handling、trace_write、test_file、replay_command、acceptance_command。
   405|   405|
   406|   406|### V01 Schema / Contract Validation
   407|   407|
   408|   408|目标：验证 schema、contract、handoff packet 是否结构正确。
   409|   409|
   410|   410|验证内容：JSON schema 合法、required fields 完整、input/output 一致、handoff 包含必要引用、missing policy 存在、status enum 合法。
   411|   411|
   412|   412|### V02 Unit / Contract Test Runner
   413|   413|
   414|   414|目标：验证功能模块是否正确工作。
   415|   415|
   416|   416|测试类型：unit_test、schema_validation_test、contract_test、rule_logic_test、gap_detection_test、KV_index_test、handoff_test、failure_case_test。
   417|   417|
   418|   418|测试证据输出：
   419|   419|
   420|   420|```json
   421|   421|{
   422|   422|  "test_command": "",
   423|   423|  "test_status": "PASSED",
   424|   424|  "passed": 10,
   425|   425|  "failed": 0,
   426|   426|  "covered_functions": [],
   427|   427|  "covered_rules": [],
   428|   428|  "failure_reason": null
   429|   429|}
   430|   430|```
   431|   431|
   432|   432|没有测试执行证据，不允许进入 READY。
   433|   433|
   434|   434|### V03 End-to-End Replay Gate
   435|   435|
   436|   436|目标：验证从输入文档到功能输出的端到端链路。
   437|   437|
   438|   438|Replay 链路：sample_document → K00 intake → function mapping → field model → rule logic → schema/contract → module output → trace → report → handoff。
   439|   439|
   440|   440|Replay 输出：`replay_input.json`、`replay_output.json`、`replay_trace.jsonl`、`replay_report.md`、`replay_acceptance.json`。
   441|   441|
   442|   442|### R02 Runner / Tool Binding Validator
   443|   443|
   444|   444|目标：验证功能是否真正接入系统入口。
   445|   445|
   446|   446|接入对象：CLI command、orchestrator step、Telegram command、scheduled job、paper-only runtime、report generator、dashboard field。
   447|   447|
   448|   448|状态：`BINDING_DESIGNED`、`BINDING_WRITTEN`、`BINDING_TESTED`、`BINDING_FAILED`、`NOT_BOUND`。
   449|   449|
   450|   450|没有 `BINDING_TESTED`，不能说已经进入运行系统。
   451|   451|
   452|   452|### A01 Acceptance Evidence Collector
   453|   453|
   454|   454|目标：收集所有验收证据。
   455|   455|
   456|   456|必须证据：K00 acceptance、function mapping result、field model、rule logic、schema/contract validation、trace/audit、handoff packet。涉及代码必须有 patch evidence；涉及功能必须有 test evidence；专业级必须有 replay evidence；需运行则必须有 runner binding evidence。
   457|   457|
   458|   458|状态：`ACCEPTANCE_PASSED`、`ACCEPTANCE_READY_WITH_GAPS`、`ACCEPTANCE_BLOCKED`、`ACCEPTANCE_REJECTED`。
   459|   459|
   460|   460|### H01 Downstream Handoff Writer
   461|   461|
   462|   462|目标：把已处理结果交给下游阶段。
   463|   463|
   464|   464|Handoff 必须包含：from_phase、to_phase、source_doc_refs、registry_refs、passport_refs、corpus_index_refs、system_mapping_refs、function_mapping_refs、field_model_refs、rule_logic_refs、schema_refs、contract_refs、patch_refs、test_refs、replay_refs、runner_binding_refs、KV_refs、gap_refs、acceptance_refs、allowed_next_actions、forbidden_next_actions、unresolved_gaps。
   465|   465|
   466|   466|### U01 Review / Upgrade Loop
   467|   467|
   468|   468|目标：把执行结果反馈到系统认知与模块升级。
   469|   469|
   470|   470|复盘内容：哪些文档成功变成功能、哪些只停留在设计、哪些功能缺字段、哪些规则无法测试、哪些 runner 未接入、哪些 gap 重复出现、哪些 KV 冲突。
   471|   471|
   472|   472|---
   473|   473|
   474|   474|## 6. 总状态机
   475|   475|
   476|   476|完整状态链：
   477|   477|
   478|   478|```text
   479|   479|DOC_RECEIVED
   480|   480|→ ENTRY_CLASSIFIED
   481|   481|→ K00_ACCEPTED
   482|   482|→ KV_INDEXED
   483|   483|→ SYSTEM_MAPPED
   484|   484|→ GAP_ANALYZED
   485|   485|→ FUNCTION_MAPPED
   486|   486|→ IMPLEMENTATION_DECIDED
   487|   487|→ ASSET_PLANNED
   488|   488|→ FIELD_MODEL_READY
   489|   489|→ RULE_LOGIC_READY
   490|   490|→ SCHEMA_CONTRACT_READY
   491|   491|→ PATCH_WRITTEN
   492|   492|→ PATCH_APPLIED
   493|   493|→ SCHEMA_VALIDATED
   494|   494|→ UNIT_TESTED
   495|   495|→ REPLAY_TESTED
   496|   496|→ RUNNER_BOUND
   497|   497|→ ACCEPTANCE_PASSED
   498|   498|→ HANDOFF_READY
   499|   499|→ REVIEW_LOGGED
   500|   500|```
   501|   501|
   502|   502|异常状态：
   503|   503|
   504|   504|- `K00_BLOCKED`
   505|   505|- `FUNCTION_BLOCKED`
   506|   506|- `IMPLEMENTATION_BLOCKED`
   507|   507|- `PATCH_FAILED`
   508|   508|- `TEST_FAILED`
   509|   509|- `REPLAY_FAILED`
   510|   510|- `BINDING_FAILED`
   511|   511|- `ACCEPTANCE_BLOCKED`
   512|   512|- `DESIGN_ONLY`
   513|   513|- `PLANNED_NOT_WRITTEN`
   514|   514|- `NOT_EXECUTED`
   515|   515|- `READY_WITH_GAPS`
   516|   516|
   517|   517|---
   518|   518|
   519|   519|## 7. 目录体系
   520|   520|
   521|   521|```text
   522|   522|/root/her_document_function_system/
   523|   523|  00_governance/
   524|   524|  01_intake/
   525|   525|  02_mapping/
   526|   526|  03_kv_memory/
   527|   527|  04_function_realization/
   528|   528|  05_contracts_schemas/
   529|   529|  06_code_realization/
   530|   530|  07_validation/
   531|   531|  08_runner_binding/
   532|   532|  09_acceptance_handoff/
   533|   533|  10_review_upgrade/
   534|   534|```
   535|   535|
   536|   536|目录原则：入口与实现分离；资料、记忆、契约、代码、验证、交接分层；raw/registry/passport 永远不能被 KV 替代；完成必须有 evidence 与 handoff；复盘必须反哺治理与升级。
   537|   537|
   538|   538|---
   539|   539|
   540|   540|## 8. 关键数据模型
   541|   541|
   542|   542|### document_passport
   543|   543|
   544|   544|```json
   545|   545|{
   546|   546|  "doc_id": "",
   547|   547|  "source_name": "",
   548|   548|  "source_type": "",
   549|   549|  "raw_path": "",
   550|   550|  "content_hash": "",
   551|   551|  "document_role": "",
   552|   552|  "core_intent": "",
   553|   553|  "affected_planes": [],
   554|   554|  "target_phase_candidates": [],
   555|   555|  "forbidden_actions": [],
   556|   556|  "status": ""
   557|   557|}
   558|   558|```
   559|   559|
   560|   560|### function_mapping
   561|   561|
   562|   562|```json
   563|   563|{
   564|   564|  "function_id": "",
   565|   565|  "source_concept": "",
   566|   566|  "required_function": "",
   567|   567|  "function_type": "",
   568|   568|  "target_phase": "",
   569|   569|  "input_fields": [],
   570|   570|  "output_fields": [],
   571|   571|  "required_logic": "",
   572|   572|  "required_assets": [],
   573|   573|  "implementation_status": ""
   574|   574|}
   575|   575|```
   576|   576|
   577|   577|### field_model
   578|   578|
   579|   579|```json
   580|   580|{
   581|   581|  "field_name": "",
   582|   582|  "field_type": "",
   583|   583|  "source": "",
   584|   584|  "required": true,
   585|   585|  "missing_policy": "",
   586|   586|  "evidence_level": "",
   587|   587|  "confidence_required": true,
   588|   588|  "counter_evidence_required": true,
   589|   589|  "used_by": [],
   590|   590|  "output_to": []
   591|   591|}
   592|   592|```
   593|   593|
   594|   594|### rule_logic
   595|   595|
   596|   596|```json
   597|   597|{
   598|   598|  "rule_id": "",
   599|   599|  "rule_type": "",
   600|   600|  "input_fields": [],
   601|   601|  "calculation_method": "",
   602|   602|  "threshold_or_condition": "",
   603|   603|  "positive_evidence": [],
   604|   604|  "counter_evidence": [],
   605|   605|  "confidence_logic": "",
   606|   606|  "failure_condition": "",
   607|   607|  "output_status": "",
   608|   608|  "trace_required": true
   609|   609|}
   610|   610|```
   611|   611|
   612|   612|### implementation_asset
   613|   613|
   614|   614|```json
   615|   615|{
   616|   616|  "asset_id": "",
   617|   617|  "function_id": "",
   618|   618|  "asset_type": "",
   619|   619|  "path": "",
   620|   620|  "action": "",
   621|   621|  "reason": "",
   622|   622|  "upstream_input": "",
   623|   623|  "downstream_output": "",
   624|   624|  "acceptance_check": ""
   625|   625|}
   626|   626|```
   627|   627|
   628|   628|---
   629|   629|
   630|   630|## 9. 专业级功能完整性审计
   631|   631|
   632|   632|每次处理文档后，必须审计：文档摄取、原始资料保存、source registry、passport、corpus index、system mapping、gap detection、KV index、function mapping、field model、rule logic、schema、contract、controller responsibility、code module（视功能必须）、test、replay（专业级必须）、runner binding（如需运行则必须）、trace/audit、acceptance、handoff、review/upgrade。
   633|   633|
   634|   634|审计结论状态：`AUDIT_PASSED`、`AUDIT_PASSED_WITH_GAPS`、`AUDIT_BLOCKED`、`AUDIT_FAILED`、`AUDIT_NOT_RUN`。
   635|   635|
   636|   636|---
   637|   637|
   638|   638|## 10. 七角色视角审计
   639|   639|
   640|   640|- **系统架构师:** 这个功能落在哪个系统层？是否破坏结构？
   641|   641|- **数据建模师:** 字段是否完整？来源是否明确？
   642|   642|- **策略分析师:** 判断逻辑是否可解释？是否有反证？
   643|   643|- **工程实现者:** 是否能写成代码？文件在哪里？
   644|   644|- **测试工程师:** 如何证明它能跑？失败样本是什么？
   645|   645|- **风控审计员:** 是否会越权进入 runner / live / signing？
   646|   646|- **复盘官:** 结果是否能进入报告和升级循环？
   647|   647|
   648|   648|---
   649|   649|
   650|   650|## 11. 系统验收标准
   651|   651|
   652|   652|### 不能算完成
   653|   653|
   654|   654|只总结文档、只生成任务包、只有系统映射、只有 gap list、只有设计说明、没有字段模型、没有 schema/contract、没有代码落点、没有测试、没有 replay、没有 runner binding、没有 acceptance evidence、没有 handoff。
   655|   655|
   656|   656|这些只能是：`DESIGN_ONLY`、`READY_WITH_GAPS`、`PLANNED_NOT_WRITTEN`、`NOT_EXECUTED`。
   657|   657|
   658|   658|### 专业完成条件
   659|   659|
   660|   660|必须满足：
   661|   661|
   662|   662|- `K00_ACCEPTED`
   663|   663|- `KV_INDEXED`
   664|   664|- `FUNCTION_MAPPED`
   665|   665|- `FIELD_MODEL_READY`
   666|   666|- `RULE_LOGIC_READY`
   667|   667|- `SCHEMA_CONTRACT_READY`
   668|   668|- `PATCH_APPLIED` 或 `DESIGN_ONLY` 明确标记
   669|   669|- `TESTED`
   670|   670|- `REPLAY_TESTED`
   671|   671|- `ACCEPTANCE_PASSED`
   672|   672|- `HANDOFF_READY`
   673|   673|
   674|   674|如果涉及运行入口，还必须：`RUNNER_BOUND`、`BINDING_TESTED`。
   675|   675|
   676|   676|---
   677|   677|
   678|   678|## 12. 新旧版本区别
   679|   679|
   680|   680|| 对比项 | 之前版本 | 新版本 |
   681|   681||---|---|---|
   682|   682|| 文档处理 | 摄取 / 索引 / 映射 | 摄取后继续功能落实 |
   683|   683|| K00 | 核心终点 | 只是入口 |
   684|   684|| KV | 补充索引 | 正式记忆索引层 |
   685|   685|| 功能映射 | 不完整 | 核心阶段 |
   686|   686|| 字段模型 | 有但不硬 | 强制 |
   687|   687|| 判断逻辑 | 有要求 | 必须可执行结构 |
   688|   688|| 代码落实 | 弱 | 独立 Patch Writer |
   689|   689|| 测试证据 | 计划为主 | 必须收集 |
   690|   690|| Replay | 可选 | 专业级必须 |
   691|   691|| Runner 绑定 | 计划为主 | 必须验证 |
   692|   692|| Acceptance | 阶段验收 | 证据验收 |
   693|   693|| Handoff | 阶段交接 | 包含功能、代码、测试、replay、runner 证据 |
   694|   694|| Review | 不完整 | 闭环升级 |
   695|   695|
   696|   696|**收束句:** HER-DFAFS 的本质，是把 GPT 解释性研究资料从“可读内容”编译成“可执行功能资产”，并用字段模型、规则逻辑、schema / contract、代码、测试、replay、runner、acceptance、handoff、review 构成完整闭环。
   697|   697|
   698|
   699|---
   700|
   701|## 13. 最终系统定义
   702|
   703|这套系统可以正式定义为：
   704|
   705|> HER 文档到功能自动化落实系统，是一个用于处理 GPT 解释性研究资料的受控自动化管线。
   706|>
   707|> 它以 K00 为资料入口，以 KV 为长期结构化记忆索引，以 F00 为功能落实核心，以 schema / contract / code / test / replay / runner binding 为系统资产转化链路，以 acceptance evidence 和 handoff packet 作为完成证明，最终把研究资料转化为 HER 本地系统可执行、可验证、可复盘、可升级的功能能力。
   708|
   709|---
   710|
   711|## 14. 当前是否达到专业化轻量机构水准
   712|
   713|### 14.1 判断
   714|
   715|- **认知框架:** 已达到轻量机构级系统设计水准。
   716|- **功能模块:** 基本齐全。
   717|- **执行闭环:** 需要后续落地为 HER Skill / Controller / 文件结构 / CLI。
   718|- **自动化程度:** 设计层已完整，工程层需要实现。
   719|
   720|### 14.2 还不能宣称
   721|
   722|- 系统已运行完成。
   723|
   724|### 14.3 可以宣称
   725|
   726|- 专业级自动化文档处理与功能落实系统体系已经建立完成。
   727|- 下一步应进入 HER Skill 化、Controller 化、文件模板化、CLI 化和 replay 验证。
   728|
   729|---
   730|
   731|## 15. 下一步建议
   732|
   733|下一步不应该继续扩展理论。
   734|
   735|应该进入具体落地：
   736|
   737|> 建立 `F00_function_realization_controller`。
   738|
   739|并生成以下文件：
   740|
   741|1. `01_f00_manifest.yaml`
   742|2. `02_f00_context_pack.md`
   743|3. `03_f00_objective_tree.yaml`
   744|4. `04_f00_input_contract.json`
   745|5. `05_f00_output_contract.json`
   746|6. `06_f00_execution_protocol.md`
   747|7. `07_f00_acceptance_gate.yaml`
   748|8. `08_f00_state.json`
   749|9. `09_f00_handoff_packet.schema.json`
   750|10. `10_concept_to_function_map.schema.json`
   751|11. `11_function_asset_plan.schema.json`
   752|12. `12_test_replay_evidence.schema.json`
   753|
   754|这样 HER 才能从“理解资料”真正进入“自动功能落实”。
   755|

---

## 16. SIKK 集成目录标准

为避免再次产生目录混乱，HER-DFAFS 的新控制器资产应进入 `/root/sikk-gmgn` 体系：

```text
/root/sikk-gmgn/system/her_document_function_system/
  controllers/
    F00_function_realization_controller/
      01_f00_manifest.yaml
      02_f00_context_pack.md
      03_f00_objective_tree.yaml
      04_f00_input_contract.json
      05_f00_output_contract.json
      06_f00_execution_protocol.md
      07_f00_acceptance_gate.yaml
      08_f00_state.json
      09_f00_handoff_packet.schema.json
      10_concept_to_function_map.schema.json
      11_function_asset_plan.schema.json
      12_field_model.schema.json
      13_rule_logic.schema.json
      14_implementation_decision.schema.json
      15_test_replay_evidence.schema.json
      16_runner_binding.schema.json
      17_recovery_policy.md
      18_trace_audit_spec.yaml
      19_f00_final_report_template.md

/root/sikk-gmgn/data/her_document_function_system/
  f00_runs/
    <run_id>/
      input/
      repo_scan/
      concept_to_function/
      implementation_decision/
      asset_plan/
      field_model/
      rule_logic/
      schema_contract/
      code_patch/
      tests/
      replay/
      runner_binding/
      trace/
      acceptance/
      handoff/
      reports/
```

`/root/her_document_function_system/` 保留为 bootstrap/reference 根目录；新的专业化控制器与运行数据以 SIKK 集成路径为准。

## 7. F00 输出合约

F00 必须输出以下文件化资产。F00 的输出不得只存在于聊天上下文中；只有写入 canonical F00 控制器输出目录并通过验收门的资产，才可作为 F00 输出。

```json
{
  "phase_id": "F00",
  "required_outputs": {
    "function_mapping": "concept_to_function_map.json",
    "implementation_decision": "implementation_decision.json",
    "repo_scan_result": "repo_scan_result.json",
    "function_asset_plan": "function_asset_plan.json",
    "field_model": "field_model.json",
    "rule_logic": "rule_logic.json",
    "schema_contract_plan": "schema_contract_plan.json",
    "patch_plan": "patch_plan.json",
    "test_replay_plan": "test_replay_plan.json",
    "runner_binding_plan": "runner_binding_plan.json",
    "trace_log": "f00_trace.jsonl",
    "audit_log": "f00_audit.jsonl",
    "acceptance_result": "f00_acceptance_result.json",
    "handoff_packet": "f00_to_downstream_handoff_packet.json",
    "final_report": "f00_final_report.md"
  }
}
```

### 7.1 输出缺失处理

- 缺少任一 required output：`F00_OUTPUT_BLOCKED`。
- 输出文件存在但状态为 `NOT_GENERATED` / `NOT_ACCEPTED` / `NOT_READY`：不得通过验收。
- `f00_to_downstream_handoff_packet.json` 必须依赖 `f00_acceptance_result.json`，不得提前 READY。
- `f00_trace.jsonl` 与 `f00_audit.jsonl` 必须保留运行轨迹与审计轨迹。
- `f00_final_report.md` 是人类可读总结，不替代结构化输出。

---

## 8. F00 文档到实际功能需求映射强制规范

### 8.1 核心原则

处理 GPT 研究资料时，HER-DFAFS 不得只总结，也不得只生成 K00 任务包后声明完成。K00 只代表资料进入系统，后续必须执行“文档 → 实际功能需求映射”。

完整方法轮必须是：

```text
入口识别
→ K00 摄取
→ 系统位置映射
→ 功能需求映射
→ 功能资产拆解
→ 字段模型
→ 判断逻辑
→ schema / contract
→ code module
→ test / replay
→ runner binding
→ 功能完整性审计
→ acceptance
→ handoff
```

### 8.2 解释性观点到 required_function 的转换

每条解释性观点、方法论判断、系统建设建议、风险边界或流程要求，都必须转换成一条或多条 `required_function`。不得停留在“观点总结”“核心摘要”“建议清单”。

每个 `required_function` 必须声明 `function_type`，且只能属于以下类型之一：

- `NEW_FUNCTION`
- `MODIFY_FUNCTION`
- `ENHANCE_FUNCTION`
- `HARD_BLOCK_RULE`
- `SOFT_SCORE_RULE`
- `STATE_MACHINE_RULE`
- `SCHEMA_UPDATE`
- `CONTRACT_UPDATE`
- `TRACE_REQUIREMENT`
- `REPORT_REQUIREMENT`
- `TEST_REQUIREMENT`
- `RUNNER_BINDING`
- `GOVERNANCE_RULE`
- `REVIEW_RULE`

扩展类型如 `KV_INDEX_UPDATE`、`HANDOFF_UPDATE`、`RECOVERY_POLICY_UPDATE` 可以作为系统内部补充类型，但不能替代上述核心分类。

### 8.3 单个功能的最小说明字段

每个功能必须说明：

- `input_fields`: 输入字段。
- `field_sources`: 字段来源，必须引用 K00 handoff、passport、corpus index、system mapping、gap detection、KV 或 repo scan。
- `output_fields`: 输出字段。
- `judgement_logic`: 判断逻辑，禁止只写“AI 综合判断”。
- `schema`: 需要新增或更新的 schema。
- `contract`: 需要新增或更新的 input/output/handoff contract。
- `code_module`: 代码模块、函数或 controller 落点；若未写入必须标记 `PLANNED_NOT_WRITTEN` 或 `DESIGN_ONLY`。
- `tests`: 单元测试、契约测试、规则测试或失败用例。
- `replay`: 端到端 replay 输入、期望输出与验证命令。
- `trace`: trace 事件与字段。
- `report`: 报告字段或模板落点。
- `kv`: KV 索引更新或明确 `KV_NOT_REQUIRED`。
- `handoff`: 交接字段、目标阶段与禁止动作。
- `runner_binding`: CLI / runner / orchestrator / Telegram / report generator 绑定；未绑定不得称为可运行。
- `acceptance_criteria`: 验收标准和证据路径。

### 8.4 功能完整性审计范围

F00 / A01 必须审计是否漏掉以下项目：

- 数据摄取
- 字段标准化
- schema
- contract
- controller
- 判断逻辑
- scoring
- hard gate
- state machine
- trace
- audit
- report
- KV
- handoff
- test
- replay
- runner binding
- recovery
- governance

缺少任一必需项时，必须写入 `missing_function_audit` 与 `gap_list`，不得输出 `ACCEPTANCE_PASSED`。

### 8.5 禁止状态冒充

以下冒充行为被硬禁止：

- 直接总结资料后宣称处理完成。
- 只生成 K00 任务包就说完成。
- 把 `K00_ACCEPTED` 当成功能完成。
- 把 `DESIGN_ONLY` 当成 `IMPLEMENTED`。
- 把 `PLANNED_NOT_WRITTEN` 当成 `WRITTEN`。
- 没有测试就输出 `READY`。
- 没有 runner binding 就说可运行。
- 没有 handoff 就进入下游。
- 启动 live runtime / wallet signing / auto deploy。

### 8.6 F00 最终输出字段

F00 最终结果必须至少输出以下顶层字段：

```json
{
  "doc_id": "",
  "target_phase": [],
  "system_mapping": [],
  "function_mapping": [],
  "required_functions": [],
  "implementation_assets": [],
  "field_model": [],
  "rule_logic": [],
  "schema_contract_changes": [],
  "code_modules": [],
  "test_replay_plan": [],
  "runner_binding_plan": [],
  "missing_function_audit": [],
  "gap_list": [],
  "acceptance_result": {},
  "handoff_result": {},
  "final_status": ""
}
```

若任一字段无法生成，必须显式写入缺失原因、来源缺口、阻断状态和恢复路径。

<!-- updated_at: 2026-05-13T14:04:37 -->

