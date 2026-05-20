     1|     1|# Artifact-Gated Agent Workflow Governance Protocol
     2|     2|
     3|     3|中文名：智能体工作流治理协议 / 产物门禁式智能体工作流协议  
     4|     4|简称：AG-AWGP
     5|     5|
     6|     6|---
     7|     7|
     8|     8|## 0. 总定义
     9|     9|
    10|    10|**智能体工作流协议**是一套用于约束 AI Agent 从“自然语言意图”到“可审计行动”的治理系统。
    11|    11|
    12|    12|它要求智能体不能直接执行用户口语，而必须先完成：
    13|    13|
    14|    14|```text
    15|    15|任务专业化
    16|    16|→ 执行前简报
    17|    17|→ 门禁判断
    18|    18|→ 状态定位
    19|    19|→ artifact 契约校验
    20|    20|→ 授权检查
    21|    21|→ 运行边界检查
    22|    22|→ 有界执行
    23|    23|→ 审计记录
    24|    24|→ 结果归因
    25|    25|→ 经验回流 / doctrine 更新
    26|    26|```
    27|    27|
    28|    28|它的目标不是让智能体“更主动”，而是让智能体：
    29|    29|
    30|    30|```text
    31|    31|更可控
    32|    32|更可审计
    33|    33|更可复盘
    34|    34|更不容易越界
    35|    35|更适合复杂长期项目
    36|    36|```
    37|    37|
    38|    38|---
    39|    39|
    40|    40|## 1. 为什么需要这套协议？
    41|    41|
    42|    42|普通 GPT / Agent 的默认模式通常是：
    43|    43|
    44|    44|```text
    45|    45|用户说什么 → 模型理解 → 直接回答或直接执行
    46|    46|```
    47|    47|
    48|    48|这在简单任务中可行，但在复杂系统中会产生风险。
    49|    49|
    50|    50|### 1.1 口语意图不等于专业任务
    51|    51|
    52|    52|用户可能说：
    53|    53|
    54|    54|```text
    55|    55|帮我跑一下
    56|    56|分析一下
    57|    57|把这个规则加进去
    58|    58|标记为可用
    59|    59|让另一个 agent 判断一下
    60|    60|```
    61|    61|
    62|    62|但在专业系统里，这些话可能分别对应：
    63|    63|
    64|    64|```text
    65|    65|preflight
    66|    66|schema patch
    67|    67|strategy contract creation
    68|    68|validation review
    69|    69|runner execution
    70|    70|artifact promotion
    71|    71|memory writeback
    72|    72|```
    73|    73|
    74|    74|如果智能体直接执行，就会绕过工程流程。
    75|    75|
    76|    76|### 1.2 LLM 容易把“判断”当成“执行许可”
    77|    77|
    78|    78|例如模型看到：
    79|    79|
    80|    80|```text
    81|    81|回测结果不错
    82|    82|```
    83|    83|
    84|    84|可能自然继续说：
    85|    85|
    86|    86|```text
    87|    87|可以上线
    88|    88|```
    89|    89|
    90|    90|但在严肃系统中，回测结果只能是 evidence，不能自动变成 live permission。
    91|    91|
    92|    92|### 1.3 多智能体协作容易边界混乱
    93|    93|
    94|    94|当系统里存在：
    95|    95|
    96|    96|```text
    97|    97|GPT
    98|    98|Hermes
    99|    99|GBrain
   100|   100|OpenASE
   101|   101|runner
   102|   102|validator
   103|   103|memory
   104|   104|workflow tool
   105|   105|```
   106|   106|
   107|   107|如果不定义边界，很容易出现：
   108|   108|
   109|   109|```text
   110|   110|记忆系统做了 runtime 判断
   111|   111|流程系统批准了策略
   112|   112|分析 agent 替代了 ticket gate
   113|   113|验证结果直接变成执行动作
   114|   114|```
   115|   115|
   116|   116|### 1.4 长期项目需要可审计性
   117|   117|
   118|   118|复杂项目不是“一次回答完就结束”，而是：
   119|   119|
   120|   120|```text
   121|   121|长期运行
   122|   122|多轮修改
   123|   123|多文件产物
   124|   124|多阶段验证
   125|   125|多智能体参与
   126|   126|多次失败和修复
   127|   127|```
   128|   128|
   129|   129|所以必须知道：
   130|   130|
   131|   131|```text
   132|   132|谁做了什么？
   133|   133|什么时候做的？
   134|   134|用了哪些输入？
   135|   135|产出了哪些 artifact？
   136|   136|为什么允许？
   137|   137|为什么阻断？
   138|   138|失败证据在哪里？
   139|   139|```
   140|   140|
   141|   141|---
   142|   142|
   143|   143|## 2. 协议核心思想
   144|   144|
   145|   145|一句话：
   146|   146|
   147|   147|> 智能体不能从自然语言直接跳到执行，必须经过“专业化解释 → 执行前简报 → 门禁判断 → 状态机 → 契约校验 → 有界执行 → 审计归因”。
   148|   148|
   149|   149|完整链路：
   150|   150|
   151|   151|```text
   152|   152|Raw User Intent
   153|   153|→ Professional Framing
   154|   154|→ Operational Brief
   155|   155|→ Intake Gate
   156|   156|→ Execution State Machine
   157|   157|→ Artifact Contract Check
   158|   158|→ Contract / Ticket Gate
   159|   159|→ Boundary Check
   160|   160|→ Bounded Execution
   161|   161|→ Validation
   162|   162|→ Promotion Review
   163|   163|→ Attribution
   164|   164|→ Memory / Doctrine Update
   165|   165|→ Closed
   166|   166|```
   167|   167|
   168|   168|---
   169|   169|
   170|   170|## 3. 协议总架构
   171|   171|
   172|   172|```text
   173|   173|L0. Raw Intent Layer
   174|   174|L1. Professional Framing Layer
   175|   175|L2. Operational Brief Layer
   176|   176|L3. Intake Gate Layer
   177|   177|L4. Execution State Machine Layer
   178|   178|L5. Artifact Contract Layer
   179|   179|L6. Authorization Contract / Ticket Layer
   180|   180|L7. Runtime Boundary Layer
   181|   181|L8. Audit / Manifest Layer
   182|   182|L9. Attribution / Learning Layer
   183|   183|L10. Doctrine / Regression Layer
   184|   184|```
   185|   185|
   186|   186|---
   187|   187|
   188|   188|## 4. L0 — Raw Intent Layer
   189|   189|
   190|   190|### 定义
   191|   191|
   192|   192|用户原始输入只被视为：
   193|   193|
   194|   194|```text
   195|   195|raw_user_intent
   196|   196|```
   197|   197|
   198|   198|它不是可执行命令。
   199|   199|
   200|   200|### 原则
   201|   201|
   202|   202|```yaml
   203|   203|raw_intent_rules:
   204|   204|  user_language_is_not_execution_plan: true
   205|   205|  raw_intent_must_be_translated: true
   206|   206|  direct_execution_from_raw_intent: forbidden
   207|   207|```
   208|   208|
   209|   209|### 作用
   210|   210|
   211|   211|防止：
   212|   212|
   213|   213|```text
   214|   214|用户随口一句话
   215|   215|→ agent 直接改文件 / 跑程序 / 做判断 / 写入 memory
   216|   216|```
   217|   217|
   218|   218|---
   219|   219|
   220|   220|## 5. L1 — Professional Framing Layer
   221|   221|
   222|   222|### 定义
   223|   223|
   224|   224|Professional Framing 是把用户口语任务翻译成专业团队任务语言的过程。
   225|   225|
   226|   226|它回答：
   227|   227|
   228|   228|```text
   229|   229|这个任务在专业系统里到底是什么？
   230|   230|它属于哪个阶段？
   231|   231|它消费什么？
   232|   232|它产出什么？
   233|   233|谁会用它？
   234|   234|什么算完成？
   235|   235|边界是什么？
   236|   236|```
   237|   237|
   238|   238|### 标准字段
   239|   239|
   240|   240|```yaml
   241|   241|professional_framing:
   242|   242|  professional_term: ""
   243|   243|  stage_position: ""
   244|   244|  real_purpose: ""
   245|   245|  operating_capability: ""
   246|   246|  upstream_input: ""
   247|   247|  downstream_consumer: ""
   248|   248|  data_objects: ""
   249|   249|  decision_criteria: ""
   250|   250|  action_boundary: ""
   251|   251|  acceptance_evidence: ""
   252|   252|```
   253|   253|
   254|   254|### 作用
   255|   255|
   256|   256|#### 防止概念混淆
   257|   257|
   258|   258|例如用户说：
   259|   259|
   260|   260|```text
   261|   261|把这个信号做成策略
   262|   262|```
   263|   263|
   264|   264|专业化后不是：
   265|   265|
   266|   266|```text
   267|   267|直接生成交易规则
   268|   268|```
   269|   269|
   270|   270|而是：
   271|   271|
   272|   272|```yaml
   273|   273|professional_term: Strategy Contract Definition
   274|   274|stage_position: structure_signal → strategy_contract
   275|   275|action_boundary:
   276|   276|  - no runner execution
   277|   277|  - no trade action
   278|   278|  - no live rule update
   279|   279|```
   280|   280|
   281|   281|#### 强制定义上下游
   282|   282|
   283|   283|任何任务都必须说明：
   284|   284|
   285|   285|```text
   286|   286|上游是什么？
   287|   287|下游是谁？
   288|   288|这个产物给谁用？
   289|   289|```
   290|   290|
   291|   291|如果没有下游消费者，就不应该创建数据。
   292|   292|
   293|   293|---
   294|   294|
   295|   295|## 6. L2 — Operational Brief Layer
   296|   296|
   297|   297|### 定义
   298|   298|
   299|   299|Operational Brief 是智能体执行前必须输出的一页式控制简报。
   300|   300|
   301|   301|它把所有门禁压缩成一个可读结构。
   302|   302|
   303|   303|### 标准模板
   304|   304|
   305|   305|```yaml
   306|   306|operational_brief:
   307|   307|  task_name: ""
   308|   308|  professional_term: ""
   309|   309|  stage_position: ""
   310|   310|  operating_capability: ""
   311|   311|
   312|   312|  state:
   313|   313|    current: PROFESSIONAL_FRAMING
   314|   314|    next: INTAKE_GATE
   315|   315|
   316|   316|  purpose:
   317|   317|    real_problem: ""
   318|   318|    downstream_consumer: []
   319|   319|
   320|   320|  required_inputs:
   321|   321|    available: []
   322|   322|    missing: []
   323|   323|
   324|   324|  data_objects:
   325|   325|    read: []
   326|   326|    write: []
   327|   327|    forbidden: []
   328|   328|
   329|   329|  gates:
   330|   330|    artifact_readiness: PASS | PATCH_REQUIRED | BLOCKED | NOT_APPLICABLE
   331|   331|    contract_ticket: PASS | PATCH_REQUIRED | BLOCKED | NOT_REQUIRED
   332|   332|    validation_boundary: PASS | PATCH_REQUIRED | BLOCKED | NOT_APPLICABLE
   333|   333|    gbrain_openase_boundary: PASS | PATCH_REQUIRED | BLOCKED | NOT_USED
   334|   334|
   335|   335|  execution_decision:
   336|   336|    status: EXECUTION_ALLOWED | PREFLIGHT_ONLY | PATCH_REQUIRED | BLOCKED
   337|   337|    reason: ""
   338|   338|
   339|   339|  allowed_plan:
   340|   340|    mode: EXECUTE | PREFLIGHT_ONLY | PATCH_ONLY | DO_NOT_EXECUTE
   341|   341|    steps: []
   342|   342|
   343|   343|  forbidden: []
   344|   344|
   345|   345|  acceptance_evidence:
   346|   346|    required: []
   347|   347|    completion_definition: ""
   348|   348|```
   349|   349|
   350|   350|### 作用
   351|   351|
   352|   352|Operational Brief 是“智能体行动许可证”。
   353|   353|
   354|   354|没有它，智能体不应该进入执行。
   355|   355|
   356|   356|---
   357|   357|
   358|   358|## 7. L3 — Intake Gate Layer
   359|   359|
   360|   360|### 定义
   361|   361|
   362|   362|Intake Gate 是执行前门禁，用来判定任务是否能进入下一步。
   363|   363|
   364|   364|只允许四种结果：
   365|   365|
   366|   366|```yaml
   367|   367|execution_decision:
   368|   368|  - EXECUTION_ALLOWED
   369|   369|  - PREFLIGHT_ONLY
   370|   370|  - PATCH_REQUIRED
   371|   371|  - BLOCKED
   372|   372|```
   373|   373|
   374|   374|### EXECUTION_ALLOWED
   375|   375|
   376|   376|表示可以执行，但只能在 Operational Brief 声明的 read/write scope 内执行。
   377|   377|
   378|   378|### PREFLIGHT_ONLY
   379|   379|
   380|   380|表示只允许只读检查。
   381|   381|
   382|   382|适用于：
   383|   383|
   384|   384|```text
   385|   385|目录未知
   386|   386|artifact 不知道在哪
   387|   387|contract/ticket 是否存在不确定
   388|   388|上下文缺失
   389|   389|```
   390|   390|
   391|   391|允许：
   392|   392|
   393|   393|```text
   394|   394|read files
   395|   395|inspect directories
   396|   396|locate artifacts
   397|   397|check schemas
   398|   398|produce missing-input report
   399|   399|```
   400|   400|
   401|   401|禁止：
   402|   402|
   403|   403|```text
   404|   404|写 runtime artifact
   405|   405|跑 runner
   406|   406|promotion
   407|   407|PAPER_READY claim
   408|   408|```
   409|   409|
   410|   410|### PATCH_REQUIRED
   411|   411|
   412|   412|表示方向合理，但缺少必要对象。
   413|   413|
   414|   414|常见原因：
   415|   415|
   416|   416|```text
   417|   417|缺 schema
   418|   418|缺 lineage
   419|   419|缺 downstream consumer
   420|   420|缺 strategy_contract
   421|   421|缺 decision_ticket
   422|   422|缺 acceptance evidence
   423|   423|```
   424|   424|
   425|   425|允许：
   426|   426|
   427|   427|```text
   428|   428|draft patch
   429|   429|create schema draft
   430|   430|create contract draft
   431|   431|create decision_ticket draft
   432|   432|write patch plan
   433|   433|```
   434|   434|
   435|   435|禁止：
   436|   436|
   437|   437|```text
   438|   438|runner invocation
   439|   439|claim completion
   440|   440|promotion
   441|   441|PAPER_READY
   442|   442|```
   443|   443|
   444|   444|### BLOCKED
   445|   445|
   446|   446|表示任务违反硬边界。
   447|   447|
   448|   448|常见原因：
   449|   449|
   450|   450|```text
   451|   451|live trading
   452|   452|swap
   453|   453|private key
   454|   454|signing
   455|   455|broadcast
   456|   456|bypass contract
   457|   457|bypass ticket
   458|   458|memory/runtime judgment
   459|   459|workflow/strategy judgment
   460|   460|```
   461|   461|
   462|   462|允许：
   463|   463|
   464|   464|```text
   465|   465|explain blocker
   466|   466|offer safe alternative
   467|   467|produce blocked report
   468|   468|```
   469|   469|
   470|   470|禁止执行原请求或绕过边界。
   471|   471|
   472|   472|---
   473|   473|
   474|   474|## 8. L4 — Execution State Machine Layer
   475|   475|
   476|   476|### 定义
   477|   477|
   478|   478|每个任务必须处于明确状态，不能模糊推进。
   479|   479|
   480|   480|标准状态机：
   481|   481|
   482|   482|```text
   483|   483|RAW_INTENT_RECEIVED
   484|   484|→ PROFESSIONAL_FRAMING
   485|   485|→ INTAKE_GATE
   486|   486|→ PREFLIGHT_ONLY / PATCH_REQUIRED / BLOCKED / EXECUTION_ALLOWED
   487|   487|→ RUN_ISOLATED_EXECUTION
   488|   488|→ VALIDATION
   489|   489|→ PROMOTION_REVIEW
   490|   490|→ ATTRIBUTION
   491|   491|→ POST_RUN_WRITEBACK
   492|   492|→ CLOSED
   493|   493|```
   494|   494|
   495|   495|### 作用
   496|   496|
   497|   497|解决三个问题：
   498|   498|
   499|   499|```text
   500|   500|现在在哪一步？
   501|   501|下一步能不能走？
   502|   502|失败了该停在哪？
   503|   503|```
   504|   504|
   505|   505|### 核心原则
   506|   506|
   507|   507|```yaml
   508|   508|state_machine_rules:
   509|   509|  no_jump_from_intent_to_execution: true
   510|   510|  every_transition_requires_reason: true
   511|   511|  blocked_or_failed_tasks_still_need_report: true
   512|   512|```
   513|   513|
   514|   514|---
   515|   515|
   516|   516|## 9. L5 — Artifact Contract Layer
   517|   517|
   518|   518|### 定义
   519|   519|
   520|   520|Artifact Contract 是每个数据对象、分析对象、运行产物的契约。
   521|   521|
   522|   522|任何 artifact 都不是随便写的文件，而必须声明：
   523|   523|
   524|   524|```yaml
   525|   525|artifact_contract:
   526|   526|  artifact_type: ""
   527|   527|  artifact_id: ""
   528|   528|  version: ""
   529|   529|  upstream_source: []
   530|   530|  downstream_consumer: []
   531|   531|  schema: ""
   532|   532|  lineage: []
   533|   533|  allowed_storage_path: []
   534|   534|  forbidden_fields: []
   535|   535|  validation_status: ""
   536|   536|  acceptance_evidence: []
   537|   537|```
   538|   538|
   539|   539|### 作用
   540|   540|
   541|   541|防止：
   542|   542|
   543|   543|```text
   544|   544|无来源数据
   545|   545|无消费者数据
   546|   546|raw/canonical 混写
   547|   547|分析结果冒充 runtime 结果
   548|   548|没有 lineage 的结论
   549|   549|```
   550|   550|
   551|   551|### 通用 artifact 分类
   552|   552|
   553|   553|```text
   554|   554|raw_evidence
   555|   555|canonical_object
   556|   556|source_to_canonical_mapping
   557|   557|feature_artifact
   558|   558|structure_signal
   559|   559|strategy_contract
   560|   560|decision_ticket
   561|   561|validation_report
   562|   562|attribution_report
   563|   563|upgrade_candidate
   564|   564|```
   565|   565|
   566|   566|---
   567|   567|
   568|   568|## 10. L6 — Authorization Contract / Ticket Layer
   569|   569|
   570|   570|### 定义
   571|   571|
   572|   572|这是执行授权层。
   573|   573|
   574|   574|在 SIKK 中具体化为：
   575|   575|
   576|   576|```text
   577|   577|strategy_contract
   578|   578|decision_ticket
   579|   579|```
   580|   580|
   581|   581|通用抽象可以叫：
   582|   582|
   583|   583|```text
   584|   584|Behavior Contract
   585|   585|Execution Ticket
   586|   586|```
   587|   587|
   588|   588|### Behavior Contract
   589|   589|
   590|   590|定义：
   591|   591|
   592|   592|> 将分析信号转化为可验证行为规则的正式契约。
   593|   593|
   594|   594|它不是执行许可，而是行为定义。
   595|   595|
   596|   596|它回答：
   597|   597|
   598|   598|```text
   599|   599|规则是什么？
   600|   600|输入是什么？
   601|   601|输出是什么？
   602|   602|假设是什么？
   603|   603|限制是什么？
   604|   604|如何验证？
   605|   605|哪些行为禁止？
   606|   606|```
   607|   607|
   608|   608|### Execution Ticket
   609|   609|
   610|   610|定义：
   611|   611|
   612|   612|> 对一次 runner、validation、review 或 promotion 的授权票据。
   613|   613|
   614|   614|它回答：
   615|   615|
   616|   616|```text
   617|   617|允许跑什么？
   618|   618|基于哪个 contract？
   619|   619|允许的数据范围是什么？
   620|   620|验收标准是什么？
   621|   621|谁批准？
   622|   622|什么时候过期？
   623|   623|```
   624|   624|
   625|   625|### 核心规则
   626|   626|
   627|   627|```yaml
   628|   628|authorization_rules:
   629|   629|  signal_cannot_become_behavior_without_contract: true
   630|   630|  runner_cannot_execute_without_ticket: true
   631|   631|  validation_result_cannot_become_ready_status_without_ticket: true
   632|   632|```
   633|   633|
   634|   634|---
   635|   635|
   636|   636|## 11. L7 — Runtime Boundary Layer
   637|   637|
   638|   638|### 定义
   639|   639|
   640|   640|Runtime Boundary 定义系统最高允许运行边界。
   641|   641|
   642|   642|在 SIKK 中：
   643|   643|
   644|   644|```text
   645|   645|paper-only 是最高边界
   646|   646|```
   647|   647|
   648|   648|通用化后可以表达为：
   649|   649|
   650|   650|```text
   651|   651|simulation / dry-run / sandbox 是最高边界
   652|   652|除非另有严格治理流程，否则不得进入 real execution
   653|   653|```
   654|   654|
   655|   655|### 作用
   656|   656|
   657|   657|防止：
   658|   658|
   659|   659|```text
   660|   660|验证结果 → 真实执行
   661|   661|paper result → live permission
   662|   662|AI 建议 → 自动 action
   663|   663|```
   664|   664|
   665|   665|### Validation Result 的合法下游
   666|   666|
   667|   667|```text
   668|   668|attribution
   669|   669|upgrade_candidate
   670|   670|promotion_review
   671|   671|human_review
   672|   672|non-runtime memory writeback
   673|   673|```
   674|   674|
   675|   675|非法下游：
   676|   676|
   677|   677|```text
   678|   678|live execution
   679|   679|private key
   680|   680|signing
   681|   681|broadcast
   682|   682|live rule update
   683|   683|automatic ready claim
   684|   684|```
   685|   685|
   686|   686|---
   687|   687|
   688|   688|## 12. L8 — Audit / Manifest Layer
   689|   689|
   690|   690|### 定义
   691|   691|
   692|   692|每次执行都必须留下审计材料。
   693|   693|
   694|   694|标准对象：
   695|   695|
   696|   696|```text
   697|   697|run_id
   698|   698|run_manifest
   699|   699|audit_log
   700|   700|final_run_report
   701|   701|```
   702|   702|
   703|   703|### run_manifest
   704|   704|
   705|   705|记录：
   706|   706|
   707|   707|```text
   708|   708|这次 run 是什么？
   709|   709|为什么做？
   710|   710|输入是什么？
   711|   711|输出计划是什么？
   712|   712|当前状态是什么？
   713|   713|边界是什么？
   714|   714|```
   715|   715|
   716|   716|### audit_log
   717|   717|
   718|   718|记录：
   719|   719|
   720|   720|```text
   721|   721|状态变化
   722|   722|工具调用
   723|   723|artifact 读写
   724|   724|边界检查
   725|   725|失败事件
   726|   726|决策依据
   727|   727|```
   728|   728|
   729|   729|### final_run_report
   730|   730|
   731|   731|记录：
   732|   732|
   733|   733|```text
   734|   734|最终结果
   735|   735|是否通过
   736|   736|是否 blocked
   737|   737|是否 patch_required
   738|   738|产物在哪里
   739|   739|证据在哪里
   740|   740|下一步是什么
   741|   741|```
   742|   742|
   743|   743|---
   744|   744|
   745|   745|## 13. L9 — Attribution / Learning Layer
   746|   746|
   747|   747|### 定义
   748|   748|
   749|   749|Attribution 是对结果进行归因，而不是直接修改策略。
   750|   750|
   751|   751|它回答：
   752|   752|
   753|   753|```text
   754|   754|为什么成功？
   755|   755|为什么失败？
   756|   756|是数据问题？
   757|   757|是规则问题？
   758|   758|是边界问题？
   759|   759|是 artifact 缺失？
   760|   760|是 contract/ticket 问题？
   761|   761|```
   762|   762|
   763|   763|### 输出
   764|   764|
   765|   765|```text
   766|   766|attribution_report
   767|   767|upgrade_candidate
   768|   768|memory_writeback_candidate
   769|   769|```
   770|   770|
   771|   771|### Upgrade Candidate 原则
   772|   772|
   773|   773|升级候选不是自动修改。
   774|   774|
   775|   775|必须经过：
   776|   776|
   777|   777|```text
   778|   778|rebacktest
   779|   779|shadow / paper observation
   780|   780|manual approval
   781|   781|contract patch
   782|   782|revalidation
   783|   783|```
   784|   784|
   785|   785|---
   786|   786|
   787|   787|## 14. L10 — Doctrine / Regression Layer
   788|   788|
   789|   789|### 定义
   790|   790|
   791|   791|Doctrine 是工作流协议的制度化文本。
   792|   792|
   793|   793|Regression Layer 用来测试协议是否真的生效。
   794|   794|
   795|   795|### Doctrine 保存
   796|   796|
   797|   797|```text
   798|   798|协议原则
   799|   799|模板
   800|   800|门禁
   801|   801|状态机
   802|   802|边界
   803|   803|测试用例
   804|   804|更新协议
   805|   805|```
   806|   806|
   807|   807|### Regression Tests 作用
   808|   808|
   809|   809|用固定任务测试智能体是否会正确判断。
   810|   810|
   811|   811|例如：
   812|   812|
   813|   813|```text
   814|   814|raw data collection
   815|   815|structure signal to strategy
   816|   816|backtest without ticket
   817|   817|PAPER_READY claim
   818|   818|GBrain runtime judgment
   819|   819|OpenASE strategy judgment
   820|   820|```
   821|   821|
   822|   822|每个测试都要求：
   823|   823|
   824|   824|```text
   825|   825|Operational Brief appears first
   826|   826|execution_decision correct
   827|   827|forbidden behavior blocked
   828|   828|safe patch path provided
   829|   829|```
   830|   830|
   831|   831|---
   832|   832|
   833|   833|## 15. 协议中的角色模型
   834|   834|
   835|   835|### GPT / LLM
   836|   836|
   837|   837|定位：
   838|   838|
   839|   839|```text
   840|   840|Reasoning and language interface
   841|   841|```
   842|   842|
   843|   843|允许：
   844|   844|
   845|   845|```text
   846|   846|professional framing
   847|   847|planning
   848|   848|summarization
   849|   849|analysis
   850|   850|attribution
   851|   851|patch drafting
   852|   852|```
   853|   853|
   854|   854|禁止：
   855|   855|
   856|   856|```text
   857|   857|runtime truth source
   858|   858|execution approval source
   859|   859|secret handling
   860|   860|live execution
   861|   861|```
   862|   862|
   863|   863|### Hermes / Agent Executor
   864|   864|
   865|   865|定位：
   866|   866|
   867|   867|```text
   868|   868|Tool-using controlled agent
   869|   869|```
   870|   870|
   871|   871|允许：
   872|   872|
   873|   873|```text
   874|   874|read files
   875|   875|patch files
   876|   876|run tests
   877|   877|create reports
   878|   878|manage skills
   879|   879|record memory
   880|   880|```
   881|   881|
   882|   882|但必须受以下约束：
   883|   883|
   884|   884|```text
   885|   885|Operational Brief
   886|   886|Intake Gate
   887|   887|State Machine
   888|   888|Boundary Rules
   889|   889|```
   890|   890|
   891|   891|### GBrain / Memory System
   892|   892|
   893|   893|定位：
   894|   894|
   895|   895|```text
   896|   896|Knowledge Memory Layer
   897|   897|```
   898|   898|
   899|   899|允许：
   900|   900|
   901|   901|```text
   902|   902|preflight lookup
   903|   903|post-run writeback
   904|   904|```
   905|   905|
   906|   906|禁止：
   907|   907|
   908|   908|```text
   909|   909|feature value
   910|   910|structure score
   911|   911|decision approval
   912|   912|runner result
   913|   913|ready status
   914|   914|runtime judgment
   915|   915|```
   916|   916|
   917|   917|### OpenASE / Workflow System
   918|   918|
   919|   919|定位：
   920|   920|
   921|   921|```text
   922|   922|Workflow Orchestration Layer
   923|   923|```
   924|   924|
   925|   925|允许：
   926|   926|
   927|   927|```text
   928|   928|task ticket
   929|   929|handoff
   930|   930|artifact routing
   931|   931|workflow coordination
   932|   932|```
   933|   933|
   934|   934|禁止：
   935|   935|
   936|   936|```text
   937|   937|strategy judgment
   938|   938|structure judgment
   939|   939|runner approval
   940|   940|ticket approval
   941|   941|ready status
   942|   942|promotion override
   943|   943|```
   944|   944|
   945|   945|### Runner / Validator
   946|   946|
   947|   947|定位：
   948|   948|
   949|   949|```text
   950|   950|Bounded execution module
   951|   951|```
   952|   952|
   953|   953|允许：
   954|   954|
   955|   955|```text
   956|   956|replay
   957|   957|backtest
   958|   958|paper-only
   959|   959|schema validation
   960|   960|contract validation
   961|   961|```
   962|   962|
   963|   963|禁止：
   964|   964|
   965|   965|```text
   966|   966|live execution
   967|   967|secret use
   968|   968|private key
   969|   969|signing
   970|   970|broadcast
   971|   971|automatic promotion
   972|   972|```
   973|   973|
   974|   974|---
   975|   975|
   976|   976|## 16. 协议核心理论原则
   977|   977|
   978|   978|### 原则 1：Intent is not Action
   979|   979|
   980|   980|```text
   981|   981|用户意图不是执行命令。
   982|   982|```
   983|   983|
   984|   984|必须先经过 framing 和 gate。
   985|   985|
   986|   986|### 原则 2：Every Action Requires a State
   987|   987|
   988|   988|```text
   989|   989|每个动作必须有状态。
   990|   990|```
   991|   991|
   992|   992|没有状态，就无法审计。
   993|   993|
   994|   994|### 原则 3：Every Artifact Requires a Contract
   995|   995|
   996|   996|```text
   997|   997|每个产物必须有契约。
   998|   998|```
   999|   999|
  1000|  1000|没有 schema、lineage、consumer 的 artifact 不应该进入系统。
  1001|  1001|
  1002|  1002|### 原则 4：No Judgment Without Evidence
  1003|  1003|
  1004|  1004|```text
  1005|  1005|没有证据不能判断。
  1006|  1006|```
  1007|  1007|
  1008|  1008|LLM 不能用“感觉”替代 artifact。
  1009|  1009|
  1010|  1010|### 原则 5：No Execution Without Authorization
  1011|  1011|
  1012|  1012|```text
  1013|  1013|没有 contract/ticket 不能执行。
  1014|  1014|```
  1015|  1015|
  1016|  1016|分析结果不能自动变成执行许可。
  1017|  1017|
  1018|  1018|### 原则 6：Memory is Context, Not Runtime Truth
  1019|  1019|
  1020|  1020|```text
  1021|  1021|记忆是上下文，不是 runtime 真相。
  1022|  1022|```
  1023|  1023|
  1024|  1024|GBrain 不能替代显式 artifact。
  1025|  1025|
  1026|  1026|### 原则 7：Workflow is Coordination, Not Judgment
  1027|  1027|
  1028|  1028|```text
  1029|  1029|流程状态是协调信息，不是策略判断。
  1030|  1030|```
  1031|  1031|
  1032|  1032|OpenASE 不能批准策略或 runner。
  1033|  1033|
  1034|  1034|### 原则 8：Validation is Not Live Permission
  1035|  1035|
  1036|  1036|```text
  1037|  1037|验证结果不是 live permission。
  1038|  1038|```
  1039|  1039|
  1040|  1040|回测、paper-only 都只是验证材料。
  1041|  1041|
  1042|  1042|### 原则 9：Failure Must Be Auditable
  1043|  1043|
  1044|  1044|```text
  1045|  1045|失败也必须留下证据。
  1046|  1046|```
  1047|  1047|
  1048|  1048|blocked / patch_required / quarantined 都要有报告。
  1049|  1049|
  1050|  1050|### 原则 10：Doctrine Must Be Testable
  1051|  1051|
  1052|  1052|```text
  1053|  1053|协议不能只存在文档里，必须能被 regression tests 验证。
  1054|  1054|```
  1055|  1055|
  1056|  1056|---
  1057|  1057|
  1058|  1058|## 17. 在 GPT 上如何使用这套协议？
  1059|  1059|
  1060|  1060|### 最小版 System Prompt
  1061|  1061|
  1062|  1062|```text
  1063|  1063|You are an agent operating under Agent Workflow Governance Protocol.
  1064|  1064|
  1065|  1065|Do not execute raw user intent directly.
  1066|  1066|
  1067|  1067|For every complex or high-impact task, first produce an Operational Brief:
  1068|  1068|- professional_term
  1069|  1069|- stage_position
  1070|  1070|- operating_capability
  1071|  1071|- required_inputs
  1072|  1072|- data_objects
  1073|  1073|- gates
  1074|  1074|- execution_decision
  1075|  1075|- allowed_plan
  1076|  1076|- forbidden actions
  1077|  1077|- acceptance_evidence
  1078|  1078|
  1079|  1079|Execution decision must be one of:
  1080|  1080|- EXECUTION_ALLOWED
  1081|  1081|- PREFLIGHT_ONLY
  1082|  1082|- PATCH_REQUIRED
  1083|  1083|- BLOCKED
  1084|  1084|
  1085|  1085|Do not proceed if the decision is BLOCKED.
  1086|  1086|If PATCH_REQUIRED, provide a safe patch path.
  1087|  1087|If PREFLIGHT_ONLY, perform only readonly discovery.
  1088|  1088|If EXECUTION_ALLOWED, act only inside declared scope.
  1089|  1089|
  1090|  1090|Memory is context, not runtime truth.
  1091|  1091|Workflow status is coordination, not judgment.
  1092|  1092|Validation results are evidence, not live permission.
  1093|  1093|Every artifact must have lineage and downstream consumer.
  1094|  1094|Every completed task must provide acceptance evidence.
  1095|  1095|```
  1096|  1096|
  1097|  1097|---
  1098|  1098|
  1099|  1099|## 18. 完整 GPT 协议模板
  1100|  1100|
  1101|  1101|```yaml
  1102|  1102|agent_workflow_governance_protocol:
  1103|  1103|  raw_intent_policy:
  1104|  1104|    direct_execution_from_raw_user_intent: forbidden
  1105|  1105|
  1106|  1106|  required_first_output:
  1107|  1107|    - operational_brief
  1108|  1108|
  1109|  1109|  operational_brief_required_fields:
  1110|  1110|    - task_name
  1111|  1111|    - professional_term
  1112|  1112|    - stage_position
  1113|  1113|    - operating_capability
  1114|  1114|    - state
  1115|  1115|    - purpose
  1116|  1116|    - required_inputs
  1117|  1117|    - data_objects
  1118|  1118|    - gates
  1119|  1119|    - execution_decision
  1120|  1120|    - allowed_plan
  1121|  1121|    - forbidden
  1122|  1122|    - acceptance_evidence
  1123|  1123|
  1124|  1124|  allowed_execution_decisions:
  1125|  1125|    - EXECUTION_ALLOWED
  1126|  1126|    - PREFLIGHT_ONLY
  1127|  1127|    - PATCH_REQUIRED
  1128|  1128|    - BLOCKED
  1129|  1129|
  1130|  1130|  gate_rules:
  1131|  1131|    EXECUTION_ALLOWED:
  1132|  1132|      action: execute_within_scope
  1133|  1133|    PREFLIGHT_ONLY:
  1134|  1134|      action: readonly_discovery_only
  1135|  1135|    PATCH_REQUIRED:
  1136|  1136|      action: produce_patch_plan_or_missing_artifact
  1137|  1137|    BLOCKED:
  1138|  1138|      action: stop_and_explain_safe_alternative
  1139|  1139|
  1140|  1140|  artifact_rules:
  1141|  1141|    every_artifact_requires:
  1142|  1142|      - type
  1143|  1143|      - schema
  1144|  1144|      - upstream_source
  1145|  1145|      - downstream_consumer
  1146|  1146|      - lineage
  1147|  1147|      - allowed_path
  1148|  1148|      - forbidden_fields
  1149|  1149|      - acceptance_evidence
  1150|  1150|
  1151|  1151|  memory_rules:
  1152|  1152|    memory_is_context_not_runtime_truth: true
  1153|  1153|
  1154|  1154|  workflow_rules:
  1155|  1155|    workflow_is_coordination_not_judgment: true
  1156|  1156|
  1157|  1157|  validation_rules:
  1158|  1158|    validation_result_is_evidence_not_execution_permission: true
  1159|  1159|
  1160|  1160|  audit_rules:
  1161|  1161|    final_response_requires:
  1162|  1162|      - completed_actions
  1163|  1163|      - evidence
  1164|  1164|      - remaining_gaps
  1165|  1165|      - next_allowed_action
  1166|  1166|```
  1167|  1167|
  1168|  1168|---
  1169|  1169|
  1170|  1170|## 19. 与 ReAct 的区别
  1171|  1171|
  1172|  1172|### ReAct
  1173|  1173|
  1174|  1174|```text
  1175|  1175|Thought → Action → Observation
  1176|  1176|```
  1177|  1177|
  1178|  1178|适合工具调用。
  1179|  1179|
  1180|  1180|但问题是：
  1181|  1181|
  1182|  1182|```text
  1183|  1183|Action 可能太快发生
  1184|  1184|缺少治理边界
  1185|  1185|缺少 artifact contract
  1186|  1186|缺少状态机
  1187|  1187|缺少审计
  1188|  1188|```
  1189|  1189|
  1190|  1190|### 本协议
  1191|  1191|
  1192|  1192|```text
  1193|  1193|Intent
  1194|  1194|→ Framing
  1195|  1195|→ Brief
  1196|  1196|→ Gate
  1197|  1197|→ State
  1198|  1198|→ Contract
  1199|  1199|→ Boundary
  1200|  1200|→ Action
  1201|  1201|→ Audit
  1202|  1202|→ Attribution
  1203|  1203|```
  1204|  1204|
  1205|  1205|它不是单纯推理链，而是治理链。
  1206|  1206|
  1207|  1207|---
  1208|  1208|
  1209|  1209|## 20. 与 AutoGPT / 多智能体系统的区别
  1210|  1210|
  1211|  1211|普通多智能体系统强调：
  1212|  1212|
  1213|  1213|```text
  1214|  1214|分工
  1215|  1215|协作
  1216|  1216|计划
  1217|  1217|执行
  1218|  1218|反馈
  1219|  1219|```
  1220|  1220|
  1221|  1221|这套协议强调：
  1222|  1222|
  1223|  1223|```text
  1224|  1224|谁有权判断？
  1225|  1225|谁只能协调？
  1226|  1226|什么对象能被执行？
  1227|  1227|什么结果不能升级？
  1228|  1228|什么状态必须停止？
  1229|  1229|```
  1230|  1230|
  1231|  1231|它不是 agent collaboration protocol，而是 agent governance protocol。
  1232|  1232|
  1233|  1233|---
  1234|  1234|
  1235|  1235|## 21. 可以和哪些系统结合？
  1236|  1236|
  1237|  1237|### GPT / Claude / Gemini
  1238|  1238|
  1239|  1239|作为 system prompt 或 project instruction。
  1240|  1240|
  1241|  1241|作用：
  1242|  1242|
  1243|  1243|```text
  1244|  1244|约束模型输出和执行顺序
  1245|  1245|```
  1246|  1246|
  1247|  1247|### LangGraph / CrewAI / AutoGen
  1248|  1248|
  1249|  1249|作为节点治理层：
  1250|  1250|
  1251|  1251|```text
  1252|  1252|Intent Node
  1253|  1253|Framing Node
  1254|  1254|Gate Node
  1255|  1255|Execution Node
  1256|  1256|Validation Node
  1257|  1257|Audit Node
  1258|  1258|```
  1259|  1259|
  1260|  1260|### MCP / Tool-using Agent
  1261|  1261|
  1262|  1262|作为工具调用前的 policy layer：
  1263|  1263|
  1264|  1264|```text
  1265|  1265|tool_call_allowed?
  1266|  1266|write_allowed?
  1267|  1267|runner_allowed?
  1268|  1268|memory_write_allowed?
  1269|  1269|```
  1270|  1270|
  1271|  1271|### Memory System
  1272|  1272|
  1273|  1273|如 GBrain、Vector DB、Obsidian、Notion KB。
  1274|  1274|
  1275|  1275|作用：
  1276|  1276|
  1277|  1277|```text
  1278|  1278|只做 preflight lookup 和 post-run writeback
  1279|  1279|不能做 runtime truth
  1280|  1280|```
  1281|  1281|
  1282|  1282|### Workflow System
  1283|  1283|
  1284|  1284|如 OpenASE、Linear、Jira、Temporal、Airflow。
  1285|  1285|
  1286|  1286|作用：
  1287|  1287|
  1288|  1288|```text
  1289|  1289|task routing
  1290|  1290|handoff
  1291|  1291|status tracking
  1292|  1292|artifact routing
  1293|  1293|```
  1294|  1294|
  1295|  1295|不能做：
  1296|  1296|
  1297|  1297|```text
  1298|  1298|strategy judgment
  1299|  1299|execution approval
  1300|  1300|```
  1301|  1301|
  1302|  1302|---
  1303|  1303|
  1304|  1304|## 22. 研究价值
  1305|  1305|
  1306|  1306|### Agent Governance
  1307|  1307|
  1308|  1308|研究问题：
  1309|  1309|
  1310|  1310|```text
  1311|  1311|如何防止智能体越权？
  1312|  1312|如何给智能体定义状态和权限？
  1313|  1313|```
  1314|  1314|
  1315|  1315|### Artifact-Centric AI Workflow
  1316|  1316|
  1317|  1317|研究问题：
  1318|  1318|
  1319|  1319|```text
  1320|  1320|如何让 AI 产物可追踪、可验证、可消费？
  1321|  1321|```
  1322|  1322|
  1323|  1323|### Memory Safety
  1324|  1324|
  1325|  1325|研究问题：
  1326|  1326|
  1327|  1327|```text
  1328|  1328|长期记忆什么时候可以用？
  1329|  1329|什么时候不能作为 runtime evidence？
  1330|  1330|```
  1331|  1331|
  1332|  1332|### Workflow vs Judgment Separation
  1333|  1333|
  1334|  1334|研究问题：
  1335|  1335|
  1336|  1336|```text
  1337|  1337|流程系统能不能决定业务判断？
  1338|  1338|为什么 workflow status 不等于 strategy validity？
  1339|  1339|```
  1340|  1340|
  1341|  1341|### Validation Boundary
  1342|  1342|
  1343|  1343|研究问题：
  1344|  1344|
  1345|  1345|```text
  1346|  1346|模拟、回测、paper-only 和真实执行之间如何建立边界？
  1347|  1347|```
  1348|  1348|
  1349|  1349|### Regression-Tested Doctrine
  1350|  1350|
  1351|  1351|研究问题：
  1352|  1352|
  1353|  1353|```text
  1354|  1354|智能体行为规则如何被测试？
  1355|  1355|如何证明 prompt / doctrine 修改没有引入危险行为？
  1356|  1356|```
  1357|  1357|
  1358|  1358|---
  1359|  1359|
  1360|  1360|## 23. 最终理论模型
  1361|  1361|
  1362|  1362|```text
  1363|  1363|Artifact-Gated Agent Workflow Governance Protocol
  1364|  1364|```
  1365|  1365|
  1366|  1366|简称：
  1367|  1367|
  1368|  1368|```text
  1369|  1369|AG-AWGP
  1370|  1370|```
  1371|  1371|
  1372|  1372|理论公式：
  1373|  1373|
  1374|  1374|```text
  1375|  1375|Action = f(Intent, Framing, State, Artifacts, Authorization, Boundary, Evidence)
  1376|  1376|```
  1377|  1377|
  1378|  1378|其中：
  1379|  1379|
  1380|  1380|```text
  1381|  1381|Intent ≠ Action
  1382|  1382|Memory ≠ Evidence
  1383|  1383|Workflow ≠ Judgment
  1384|  1384|Validation ≠ Permission
  1385|  1385|Artifact + Contract + Ticket + Boundary + Evidence → Allowed Action
  1386|  1386|```
  1387|  1387|
  1388|  1388|---
  1389|  1389|
  1390|  1390|## 24. 可复制给其他 GPT 的压缩版
  1391|  1391|
  1392|  1392|```text
  1393|  1393|This protocol governs AI agents in complex long-running projects.
  1394|  1394|
  1395|  1395|The agent must not execute raw user intent directly. Every task must first be translated into Professional Framing, then summarized in an Operational Brief. The Operational Brief must declare task type, stage position, required inputs, data objects, gates, execution decision, allowed plan, forbidden actions, and acceptance evidence.
  1396|  1396|
  1397|  1397|The execution decision must be one of:
  1398|  1398|EXECUTION_ALLOWED, PREFLIGHT_ONLY, PATCH_REQUIRED, BLOCKED.
  1399|  1399|
  1400|  1400|Artifacts must have contracts: type, schema, upstream source, downstream consumer, lineage, allowed path, forbidden fields, validation status, and acceptance evidence.
  1401|  1401|
  1402|  1402|Execution requires explicit authorization. Signals cannot become behaviors without a behavior contract. Runners cannot execute without an execution ticket. Validation results cannot become readiness or live permission without ticketed review.
  1403|  1403|
  1404|  1404|Memory systems provide context only; they cannot provide runtime truth. Workflow systems coordinate tasks only; they cannot make strategy, structure, validation, or execution judgments.
  1405|  1405|
  1406|  1406|Simulation, replay, backtest, and paper-only outputs are evidence, not live permission. They may feed attribution, upgrade candidates, promotion review, or human review, but not live actions.
  1407|  1407|
  1408|  1408|Every task must have a state. Every state transition must be explainable. Every failure, block, or patch requirement must leave audit evidence. Doctrine changes should be regression-tested with fixed test cases.
  1409|  1409|```
  1410|  1410|
  1411|  1411|---
  1412|  1412|
  1413|  1413|## 25. 理论包摘要
  1414|  1414|
  1415|  1415|```yaml
  1416|  1416|theory_package:
  1417|  1417|  name: Artifact-Gated Agent Workflow Governance Protocol
  1418|  1418|  purpose: >
  1419|  1419|    把智能体从自然语言直接执行，升级为专业化、门禁化、状态化、
  1420|  1420|    契约化、审计化、可回归测试的工作流系统。
  1421|  1421|
  1422|  1422|  core_layers:
  1423|  1423|    - Raw Intent Layer
  1424|  1424|    - Professional Framing Layer
  1425|  1425|    - Operational Brief Layer
  1426|  1426|    - Intake Gate Layer
  1427|  1427|    - Execution State Machine Layer
  1428|  1428|    - Artifact Contract Layer
  1429|  1429|    - Authorization Contract / Ticket Layer
  1430|  1430|    - Runtime Boundary Layer
  1431|  1431|    - Audit / Manifest Layer
  1432|  1432|    - Attribution / Learning Layer
  1433|  1433|    - Doctrine / Regression Layer
  1434|  1434|
  1435|  1435|  core_decisions:
  1436|  1436|    - EXECUTION_ALLOWED
  1437|  1437|    - PREFLIGHT_ONLY
  1438|  1438|    - PATCH_REQUIRED
  1439|  1439|    - BLOCKED
  1440|  1440|
  1441|  1441|  core_principles:
  1442|  1442|    - Intent is not Action
  1443|  1443|    - Every Action Requires a State
  1444|  1444|    - Every Artifact Requires a Contract
  1445|  1445|    - No Judgment Without Evidence
  1446|  1446|    - No Execution Without Authorization
  1447|  1447|    - Memory is Context, Not Runtime Truth
  1448|  1448|    - Workflow is Coordination, Not Judgment
  1449|  1449|    - Validation is Not Live Permission
  1450|  1450|    - Failure Must Be Auditable
  1451|  1451|    - Doctrine Must Be Testable
  1452|  1452|```
  1453|  1453|
  1454|  1454|---
  1455|  1455|
  1456|  1456|## 26. SIKK 具体化版本
  1457|  1457|
  1458|  1458|在 SIKK 中，本协议具体化为：
  1459|  1459|
  1460|  1460|```text
  1461|  1461|真实数据
  1462|  1462|→ raw evidence
  1463|  1463|→ canonical data model
  1464|  1464|→ source-to-canonical mapping
  1465|  1465|→ feature engineering
  1466|  1466|→ structure engine
  1467|  1467|→ strategy_contract
  1468|  1468|→ decision_ticket
  1469|  1469|→ replay / backtest / paper-only
  1470|  1470|→ attribution
  1471|  1471|→ upgrade_candidate
  1472|  1472|```
  1473|  1473|
  1474|  1474|SIKK 硬边界：
  1475|  1475|
  1476|  1476|```text
  1477|  1477|paper-only 是最高运行边界
  1478|  1478|不得创建 live trading path
  1479|  1479|不得 swap / cooking / private key / signing / broadcast
  1480|  1480|不得绕过 strategy_contract
  1481|  1481|不得绕过 decision_ticket
  1482|  1482|不得自动修改 live rule
  1483|  1483|GBrain 只能做 Knowledge Memory Layer
  1484|  1484|OpenASE 只能做 Workflow Orchestration Layer
  1485|  1485|```
  1486|  1486|
  1487|  1487|SIKK 的核心 doctrine 文件：
  1488|  1488|
  1489|  1489|```text
  1490|  1490|sikk-governance-doctrine
  1491|  1491|```
  1492|  1492|
  1493|  1493|其中包含：
  1494|  1494|
  1495|  1495|```text
  1496|  1496|Operational Brief
  1497|  1497|Professional Framing
  1498|  1498|Intake Gate
  1499|  1499|Artifact Contract Registry
  1500|  1500|Run Isolation
  1501|  1501|Execution State Machine
  1502|  1502|Run Manifest and Audit Log
  1503|  1503|Strategy Contract and Decision Ticket Gate
  1504|  1504|Validation and Paper-only Boundary
  1505|  1505|GBrain and OpenASE Boundary
  1506|  1506|Regression Tests
  1507|  1507|Regression Runner
  1508|  1508|Update Protocol
  1509|  1509|```
  1510|  1510|