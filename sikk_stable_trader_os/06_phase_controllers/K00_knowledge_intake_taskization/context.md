# K00 知识摄取与 Phase Controller 候选任务化阶段

文件编号：K00-CONTEXT-002  
阶段编号：K00_knowledge_intake_taskization  
阶段名称：知识摄取与 Phase Controller 候选任务化  
版本：v2.0-light-institutional  
状态：REQUIRED_BEFORE_P00  
适用系统：SIKK Stable Trader OS  
安全边界：paper-only，禁止真实交易  
下游阶段：P00_system_bootstrap_controller  

## 1. 阶段定位

K00 不是普通文档读取阶段。K00 是 SIKK Stable Trader OS 的知识入口、资产化入口、方法论抽取入口和 Phase Controller 候选任务化入口。

K00 的核心职责：接收用户输入/文档/旧系统资料/方法论文本/交易逻辑/系统设计；保存为知识资产；生成 passport、索引、摘要、主题标签和缺口报告；抽取系统目标、阶段目标、任务结构、输入输出要求、验收要求、状态回写要求和下游交接关系；整理成 `Phase Controller Candidate Spec`；交给 P00 系统建造控制器；由 P00 决定是否正式注册为 Phase Controller、是否写入 phase registry、是否接入 control plane。

K00 不直接运行交易系统，不直接裁决阶段状态，不直接注册正式 Phase Controller，不直接进入 P01-P10 业务阶段。

## 2. Phase Controller 核心定义

Phase Controller 不是阶段说明文档。Phase Controller 是一个可调度的阶段运行单元，负责把系统目标拆成阶段目标，把阶段目标拆成任务树，把任务树绑定到输入合约、输出合约、Atomic Skill、代码工具、验收门、状态回写和下游交接包。

它不追求一次性给出智能判断，而是保证每一个判断都有字段来源、证据等级、反证记录、失败处理和可复盘路径。

任何阶段如果只是说明“这个阶段做什么”，但没有绑定输入、输出、任务树、验收门、状态回写和 handoff packet，都不能被视为真正的 Phase Controller。

## 3. K00 对 Phase Controller 的职责边界

K00 的职责不是正式创建 Phase Controller。K00 的职责是把输入资料转化为 Phase Controller 的候选构建材料。

- K00 负责：保存输入资料、生成 document passport、抽取方法论要求、抽取系统目标/阶段目标、生成任务树候选、输入/输出合约候选、Atomic Skill/工具需求、验收门候选、状态回写候选、handoff 候选、phase_controller_candidate_spec、k00_to_p00_handoff_packet。
- P00 负责：审核、编译、规范化、正式落盘 controller.yaml、写入 phase_registry.yaml、接入 current_system_state.json、绑定 runner / acceptance / handoff registry、裁决下一合法阶段。

## 4. K00 阶段目标

将任何输入资料从“可读文本”转化为“可被系统建造层消费的结构化候选资产”。K00 必须把资料转成：知识资产、文档 passport、方法论要求索引、领域对象候选、阶段目标候选、任务树候选、输入/输出合约候选、Atomic Skill 候选、代码工具/runner 候选、验收门候选、状态回写候选、下游 handoff 候选、blocking gaps、non-blocking gaps、K00 → P00 handoff packet。

## 5. K00 不负责什么

K00 不负责：正式建立 Phase Controller、正式生成 phase registry、正式生成 current system state、裁决 P01 可以启动、执行交易系统、判断 token 是否可以买、生成真实交易指令、绕过 P00、把文档存在当成系统消费完成。

## 6. K00 核心问题树

K00 处理任何资料时，必须回答：资料是什么类型；属于哪个系统平面；是否旧系统资料；是否包含可复用规则；是否包含字段/文件/命令/阶段/判断逻辑/验收标准；是否包含系统总目标、阶段目标、安全边界、禁止事项、系统缺口；是否应生成 Phase Controller 候选；归属已有阶段还是新增阶段；需要哪些输入、输出、Atomic Skill、runner、验收门、失败处理、状态回写、下游 handoff；是否存在数据、字段、合约、runner、消费者、状态分裂或“文档已存在但系统未消费”的缺口。

## 7. K00 输入标准

允许输入：user_text_goal、uploaded_document、old_system_file、method_wheel_text、trading_logic_note、wallet_structure_note、market_structure_note、governance_rule_note、data_schema_note、phase_design_note、runner_design_note、acceptance_rule_note。

禁止输入：real_trade_execution_instruction、private_key、seed_phrase、unverified_live_trade_signal、direct_buy_sell_order。

## 8. K00 输出标准

必需输出：raw_input_copy、document_passport、knowledge_asset_index_entry、methodology_requirement_extract、phase_goal_candidate、task_tree_candidate、input_contract_candidate、output_contract_candidate、atomic_skill_candidate、tool_binding_candidate、acceptance_gate_candidate、state_writeback_candidate、handoff_packet_candidate、phase_controller_candidate_spec、gap_report、k00_to_p00_handoff_packet。

## 9. K00 标准处理流程

保存输入资料 → 生成资料 passport → 判断资料类型 → 抽取系统目标 → 抽取阶段目标 → 抽取任务树 → 抽取输入要求 → 抽取输出要求 → 抽取 Atomic Skill 需求 → 抽取代码工具/runner 需求 → 抽取验收门 → 抽取状态回写要求 → 抽取下游 handoff 对象 → 识别 blocking gaps → 识别 non-blocking gaps → 生成 Phase Controller Candidate Spec → 生成 K00 → P00 handoff packet → 更新知识资产索引 → 写入 K00 runtime state → 等待 P00 消费。

## 10. Phase Controller Candidate Spec 标准

候选规格标准路径：`00_knowledge_intake/phase_controller_candidates/<asset_id>_phase_controller_candidate_spec.yaml`。候选规格不是正式 Phase Controller，只能作为 P00 编译输入。

## 11. K00 验收标准

K00 阶段完成必须满足：输入资料已保存；document passport 已生成；资料类型已识别；系统目标已抽取；阶段目标候选已抽取；任务树候选已生成；输入/输出合约候选已生成；Atomic Skill 与工具/runner 需求已识别；验收门、状态回写、下游 handoff 候选已生成；gap report、phase_controller_candidate_spec、k00_to_p00_handoff_packet 已生成；K00 没有越权注册正式 Phase Controller；P00 被标记为下游消费者；paper_only=true；real_trade_enabled=false。

## 12. K00 阻断条件

出现输入资料未保存、passport 缺失、资料类型未知、无法抽取系统目标、无法判断下游阶段、candidate spec 缺失、handoff packet 缺失、验收门候选缺失、输出文件不可解析、K00 尝试直接注册 Phase Controller、K00 尝试直接启动 P01、K00 尝试进入真实交易时，K00 不得标记为完成。

## 13. K00 输出状态

合法输出状态：INPUT_RECEIVED、ASSET_SAVED、PASSPORT_CREATED、REQUIREMENTS_EXTRACTED、PHASE_CONTROLLER_CANDIDATE_CREATED、HANDOFF_TO_P00_READY、WAITING_P00_CONSUMPTION、BLOCKED_BY_MISSING_INPUT、BLOCKED_BY_INVALID_OUTPUT、BLOCKED_BY_NO_DOWNSTREAM_TARGET。

非法输出状态：P01_READY、SYSTEM_READY、TRADE_READY、REAL_TRADE_ENABLED、PHASE_CONTROLLER_REGISTERED。

## 14. K00 与系统完整链路

用户输入 / 文档 / 旧系统资料 → K00：知识摄取与 Phase Controller 候选任务化 → phase_controller_candidate_spec.yaml → k00_to_p00_handoff_packet.json → P00：系统建造与方法论编译 → 正式 Phase Controller → phase_registry.yaml → current_system_state.json → Data Plane / Control Plane → P01-P10 业务阶段。

## 15. K00 最终判断原则

K00 的最终判断不是“这份资料我读完了”，而是“这份资料是否已经被转化为可被 P00 编译的系统建造材料”。K00 的成功标准不是摘要质量，而是资料是否具备进入系统体系的结构化入口。

## K00 专业化后的权威系统链路（DOC-20260511-019）

```text
输入资料 / 用户目标 / 方法论 / 旧系统文件
  ↓
K00：知识摄取与 Phase Controller 候选任务化
  ↓
phase_controller_candidate_spec.yaml
  ↓
k00_to_p00_handoff_packet.json
  ↓
P00：方法论编译与系统建造控制器
  ↓
正式 controller.yaml
  ↓
phase_registry.yaml
  ↓
current_system_state.json
  ↓
input_contract / output_contract / acceptance_gate / handoff_packet
  ↓
P01-P10 可调度运行
```

链路解释：K00 只负责把输入资料、用户目标、方法论与旧系统文件转化为 `phase_controller_candidate_spec.yaml` 与 `k00_to_p00_handoff_packet.json`。P00 才是方法论编译与系统建造控制器，负责正式生成 `controller.yaml`、注册 `phase_registry.yaml`、接入 `current_system_state.json`，并把 input_contract / output_contract / acceptance_gate / handoff_packet 纳入可调度运行链路。P01-P10 只能在 P00 消费完成并通过控制面验收后调度运行。

