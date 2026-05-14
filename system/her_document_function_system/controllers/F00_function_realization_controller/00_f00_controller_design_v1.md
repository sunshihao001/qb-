     1|     1|# F00_function_realization_controller
     2|     2|
     3|     3|# HER 专业化文档到功能落实控制器设计 v1.0
     4|     4|
     5|     5|## 1. 定位
     6|     6|
     7|     7|下面建立的是 F00 功能落实控制器，不是普通说明文档。
     8|     8|
     9|     9|它的定位是：
    10|    10|
    11|    11|```text
    12|    12|F00 = K00 之后的功能落实控制器
    13|    13|```
    14|    14|
    15|    15|K00 负责把 GPT 研究资料变成系统可接收、可索引、可交接的资料。
    16|    16|
    17|    17|F00 负责把这些资料继续转化成：
    18|    18|
    19|    19|```text
    20|    20|功能需求
    21|    21|→ 字段模型
    22|    22|→ 判断逻辑
    23|    23|→ schema / contract
    24|    24|→ 代码模块
    25|    25|→ 测试
    26|    26|→ replay
    27|    27|→ runner binding
    28|    28|→ trace / audit
    29|    29|→ acceptance
    30|    30|→ handoff
    31|    31|```
    32|    32|
    33|    33|也就是从：
    34|    34|
    35|    35|```text
    36|    36|解释性文档
    37|    37|```
    38|    38|
    39|    39|推进到：
    40|    40|
    41|    41|```text
    42|    42|HER 可执行、可验证、可审计、可交接的系统功能资产
    43|    43|```
    44|    44|
    45|    45|## 2. 控制器边界
    46|    46|
    47|    47|F00 不是：
    48|    48|
    49|    49|- 文档总结器
    50|    50|- 普通知识整理器
    51|    51|- K00 的重复入口
    52|    52|- 代码自动修改器本身
    53|    53|- runner / live / signing 执行器
    54|    54|
    55|    55|F00 是：
    56|    56|
    57|    57|- K00 handoff 的下游接收器
    58|    58|- 文档概念到功能需求的编译器
    59|    59|- 字段模型与判断逻辑的生成控制器
    60|    60|- schema / contract / code / test / replay / runner binding 的资产规划控制器
    61|    61|- acceptance 与 handoff 的证据组织器
    62|    62|
    63|    63|## 3. 最小闭环
    64|    64|
    65|    65|F00 的最小闭环是：
    66|    66|
    67|    67|```text
    68|    68|K00_handoff_packet
    69|    69|→ concept_to_function_map
    70|    70|→ field_model_candidates
    71|    71|→ rule_logic_candidates
    72|    72|→ implementation_decisions
    73|    73|→ function_asset_plan
    74|    74|→ test_replay_evidence_requirements
    75|    75|→ F00_state
    76|    76|→ F00_handoff_packet
    77|    77|```
    78|    78|
    79|    79|## 4. 完成标准
    80|    80|
    81|    81|F00 不能只输出设计说明。
    82|    82|
    83|    83|F00 必须至少生成：
    84|    84|
    85|    85|- `concept_to_function_map`
    86|    86|- `implementation_decisions`
    87|    87|- `function_asset_plan`
    88|    88|- `test_replay_evidence_requirements`
    89|    89|- `F00_state`
    90|    90|- `F00_handoff_packet`
    91|    91|
    92|    92|F00 通过验收后，只能宣称：
    93|    93|
    94|    94|```text
    95|    95|FUNCTION_MAPPED
    96|    96|```
    97|    97|
    98|    98|不能宣称：
    99|    99|
   100|   100|```text
   101|   101|PATCH_APPLIED
   102|   102|TESTED
   103|   103|REPLAY_TESTED
   104|   104|RUNNER_BOUND
   105|   105|ACCEPTANCE_PASSED
   106|   106|```
   107|   107|
   108|   108|这些必须由后续阶段真实执行并留下证据。
   109|   109|
   110|
   111|---
   112|
   113|# 1. F00 总定义
   114|
   115|## 1.1 控制器名称
   116|
   117|```yaml
   118|controller_name: F00_function_realization_controller
   119|controller_type: HER_PHASE_CONTROLLER
   120|phase_id: F00
   121|phase_name: Function Realization Controller
   122|中文名称: 功能落实控制器
   123|```
   124|
   125|## 1.2 核心使命
   126|
   127|F00 负责把 K00 handoff 交接过来的解释性研究资料、系统建设资料、方法论资料、策略资料、阶段资料，转化为 HER 本地系统中的可执行功能资产。
   128|
   129|F00 不只回答：
   130|
   131|```text
   132|这个文档讲了什么？
   133|```
   134|
   135|而是必须回答：
   136|
   137|```text
   138|这个文档要求系统新增什么功能？
   139|修改什么功能？
   140|增强什么功能？
   141|阻断什么错误？
   142|需要哪些字段？
   143|需要哪些判断规则？
   144|需要哪些 schema / contract？
   145|需要哪些代码模块？
   146|需要哪些测试？
   147|需要哪些 replay？
   148|需要接入哪个 runner？
   149|如何验收？
   150|如何交接？
   151|```
   152|
   153|## 1.3 F00 的系统位置
   154|
   155|完整链路：
   156|
   157|```text
   158|GPT 研究资料
   159|↓
   160|K00 Knowledge Intake & Taskization
   161|↓
   162|KV Memory Index
   163|↓
   164|K00 Handoff
   165|↓
   166|F00 Function Realization Controller
   167|↓
   168|PXX / IXX / Runner / Report / Review
   169|```
   170|
   171|F00 是 K00 和实际系统实现之间的桥梁。
   172|
   173|---
   174|
   175|# 2. F00 不是做什么
   176|
   177|F00 禁止被误用成以下角色：
   178|
   179|- **文档摘要器**  
   180|  错误原因：F00 不做普通总结。
   181|
   182|- **任务包生成器**  
   183|  错误原因：任务包不是功能完成。
   184|
   185|- **代码生成器**  
   186|  错误原因：F00 可以规划或触发代码落实，但不是无脑写代码。
   187|
   188|- **runner 启动器**  
   189|  错误原因：F00 不直接启动 live / paper runtime。
   190|
   191|- **生产部署器**  
   192|  错误原因：F00 不做 auto deploy。
   193|
   194|- **钱包执行器**  
   195|  错误原因：F00 不触碰 wallet signing。
   196|
   197|- **聊天上下文记忆**  
   198|  错误原因：F00 必须依赖正式输入、状态和 handoff。
   199|
   200|- **KV 替代器**  
   201|  错误原因：F00 可读取 KV，但不能把 KV 当正式系统状态。
   202|

---

# 3. F00 核心责任

## 3.1 主要责任

F00 必须完成以下责任：

- **读取 K00 handoff**  
  必须从 K00 合法交接进入。

- **读取 document passport**  
  理解资料角色和目标阶段。

- **读取 corpus index**  
  提取核心观点、规则、要求。

- **读取 system mapping**  
  确定影响系统层。

- **读取 gap list**  
  判断缺口是否阻断。

- **读取 KV index**  
  辅助检索旧规则、旧字段、旧合约。

- **进行功能需求映射**  
  把解释性内容变成 `required_function`。

- **建立字段模型**  
  明确字段、来源、类型、缺失策略。

- **建立判断逻辑**  
  形成 `rule_id`、条件、反证、输出状态。

- **生成 schema / contract 需求**  
  明确输入输出和交接结构。

- **规划或生成系统资产**  
  schema、contract、code、test、replay、runner。

- **扫描代码库状态**  
  防止重复造文件或改错路径。

- **做实现决策**  
  判断立即实现、仅设计、扩展旧模块、阻断。

- **建立测试与 replay 计划**  
  所有功能必须可验证。

- **生成 runner binding 计划**  
  明确如何被系统调用。

- **执行验收**  
  区分设计、写入、测试、绑定、阻断。

- **生成 handoff**  
  交接给目标 PXX / IXX / Runner / Review。

## 3.2 F00 权限

```yaml
permissions:
  - read_k00_handoff
  - read_document_passport
  - read_corpus_index
  - read_system_mapping
  - read_gap_detection
  - read_kv_index
  - scan_repository
  - design_function_mapping
  - design_field_model
  - design_rule_logic
  - design_schema_contract
  - plan_code_assets
  - write_design_files
  - write_schema_contract_files_if_allowed
  - write_code_patch_if_allowed
  - write_test_plan
  - write_replay_plan
  - write_trace_spec
  - write_acceptance_result
  - write_handoff_packet
```

## 3.3 F00 禁止行为

```yaml
forbidden_actions:
  - bypass_k00
  - execute_without_handoff
  - treat_document_as_summary_task
  - declare_function_done_without_assets
  - declare_implemented_without_patch
  - declare_tested_without_test_evidence
  - declare_runner_bound_without_binding_test
  - start_live_runtime
  - start_paper_runtime_without_explicit_safe_mode
  - wallet_signing
  - auto_deploy
  - modify_production_rules_directly
  - overwrite_raw_documents
  - delete_legacy_assets
  - treat_kv_as_contract
  - treat_chat_context_as_state
```
