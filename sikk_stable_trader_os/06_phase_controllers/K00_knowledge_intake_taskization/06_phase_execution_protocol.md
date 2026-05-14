# K00 Execution Protocol

## 1. 执行总原则

HER 不得把用户输入资料当作普通文档阅读。  
HER 必须把输入资料转化为系统可执行任务包。

## 2. 执行顺序

1. 接收用户输入资料
2. 为资料生成 doc_id
3. 将原始资料保存到 raw_inputs/
4. 更新 source_registry
5. 生成 document_passport
6. 分析资料属于九大系统平面的哪几类
7. 分析资料影响 P00-P09 哪些阶段
8. 提取资料中的系统目标、阶段目标、规则、约束、缺口、任务
9. 生成 gap_detection
10. 生成 task_execution_package
11. 生成 K00 handoff_packet
12. 更新 phase_state
13. 判断是否进入下一阶段
14. 如果通过 acceptance_gate，则自动进入下一阶段，不停止

## 3. 自动继续规则

当 K00 输出 PHASE_READY 时：

- 如果资料影响系统边界，进入 P00_system_boundary
- 如果资料影响数据事实层，进入 P01_data_fact
- 如果资料影响规则升级，进入 P09_self_upgrade
- 如果资料是新方法论，进入 governance_plane / system_methodology_blueprint 更新流程

## 4. 中断恢复

HER 每完成一个 task_id，必须更新 phase_state.json。

如果任务中断，HER 必须读取 phase_state.json，继续未完成任务，不得重新自由理解。

## 5. 禁止行为

- 禁止只总结文档
- 禁止只输出分析建议
- 禁止不保存资料
- 禁止不生成任务包
- 禁止没有 handoff_packet 就进入下一阶段
- 禁止依赖聊天上下文作为唯一系统记忆
## 6. 验收门执行规则

HER 不得把“写完文档”视为 K00 完成。K00 完成必须由 `07_phase_acceptance_gate.yaml` 判定。

执行完 handoff_packet 与 phase_state 更新后，HER 必须读取 `07_phase_acceptance_gate.yaml` 并执行：

- 检查 `minimum_acceptance.required` 是否全部满足。
- 检查 `professional_acceptance.required` 是否全部满足。
- 检查是否命中 `reject_conditions`。
- 根据 `status_mapping` 生成阶段状态。
- 当状态为 `PHASE_READY` 时，按 `next_phase_rules` 自动进入 P00/P01/P09，不停止在 K00。

如果缺失 `task_execution_package` 或 `handoff_packet`，不得进入下一阶段。
## 7. Phase State 回写规则

`08_phase_state.json` 是 K00 的运行状态文件，不是设计文档。

HER 在以下事件发生后必须立即回写 `08_phase_state.json`：

- 开始处理一个新的 doc_id。
- 开始或完成一个 task_id。
- 生成任何 required output 文件。
- 发现 missing_file。
- 发现 gap。
- 命中 hard_negative。
- 发生 runtime error。
- 生成 next_phase_recommendation。
- 完成 handoff 判断。

中断恢复时，HER 必须先读取 `08_phase_state.json`，依据 `current_task_id`、`completed_tasks`、`failed_tasks`、`generated_files`、`missing_files`、`gap_list` 与 `next_action` 继续执行，不得重新自由理解或从聊天上下文重建状态。
## 8. Handoff Packet Schema 执行规则

`09_phase_handoff_packet.schema.json` 是 K00 交接包结构约束，不是示例 JSON。

HER 生成 `handoff_packets/k00_handoff_packet_<doc_id>.json` 时必须执行：

- 先完成 required outputs、phase_state 和 acceptance_gate 判断。
- `phase_status` 必须使用 acceptance gate 的状态枚举。
- `next_phase_allowed` 必须由 acceptance gate 判断，不得手写猜测。
- `next_phase_recommendation` 必须根据 `affected_phases` 与 `next_phase_rules` 生成。
- handoff packet 必须包含 schema 的全部 required 字段。
- schema 校验失败时，不得进入下一阶段。
## 9. Task Execution Package 数据模型执行规则

`task_packages/task_execution_package_<doc_id>.json` 是 K00 最重要的产物，不是摘要文件。

HER 在执行第 10 步“生成 task_execution_package”时必须：

- 使用 `task_execution_package.schema.json` 校验结构。
- 写入 `task_package_id` 与 `source_doc_id`，保证任务包可追溯到原始资料。
- 写入 `system_understanding`，明确 `is_plain_document=false`、`is_system_design_input=true`、`requires_taskization=true`。
- 写入 `affected_system_planes` 与 `affected_phases`，供 downstream router 决定 P00/P01/P09 或治理平面更新。
- 写入 `objective_tree`，不得只写自然语言总结。
- 写入 `required_phase_package_files`，必须覆盖 9 个 K00 Phase Package 标准文件。
- 写入 `execution_policy`，强制不在单阶段停止、验收通过后继续、每个任务回写 phase_state、生成 handoff_packet。
- 写入 `acceptance_policy`，明确完成不等于 Markdown 写完，必须满足 outputs/state/handoff/next phase decision。
- 写入 `next_action`，作为 HER 下一步调度入口。

若 task_execution_package 缺失、schema 校验失败、或缺少 objective_tree / acceptance_policy / execution_policy，K00 不得生成可放行的 handoff_packet，不得进入下一阶段。
## 10. 自动化长任务执行循环

HER 执行 K00 及后续阶段时，必须按长任务循环运行，不得单次回答后停止。

标准循环：

1. 读取 `08_phase_state.json`。
2. 找到 `current_task_id`；如果为空，则根据 `next_action` 与 objective tree 推导下一个 task。
3. 执行当前 task。
4. 生成当前 task 对应输出。
5. 立即更新 `08_phase_state.json`：`current_task_id`、`completed_tasks`、`failed_tasks`、`generated_files`、`missing_files`、`gap_list`、`hard_negative_hits`、`next_action`、`updated_at`。
6. 检查 `07_phase_acceptance_gate.yaml`。
7. 如果未完成且无停止条件，继续下一个 task。
8. 如果完成，生成 `handoff_packets/k00_handoff_packet_<doc_id>.json`。
9. 根据 `next_phase_rules` 进入下一阶段。
10. 重复执行。

自动继续规则：每完成一个阶段，不允许自动停止。HER 必须先判断：

1. 当前阶段是否 `PHASE_READY`。
2. 是否存在 `BLOCKER gap`。
3. 是否存在 `next_phase_recommendation`。
4. 下一个阶段是否有输入。
5. 是否允许继续。

如果允许继续，HER 必须继续进入下一个阶段。

停止条件：HER 只有在以下情况才能停止：

1. `PHASE_REJECTED`
2. `PHASE_ERROR`
3. 缺少关键输入
4. 命中 `BLOCKER gap`
5. 用户明确要求停止
6. 下一阶段不存在
7. 下一阶段需要人工补充资料
## 11. 自动化交易流程工作流接入边界

K00 的自动化对象是“知识资料进入交易系统建设工作流”，不是“直接交易执行”。

HER 在 K00 完成后，只允许按 handoff 与 next_phase_rules 推进到：

- `P00_system_boundary`
- `P01_data_fact`
- `P09_self_upgrade`
- 或 HER task router / gap closure planner

最终交易工作流必须保持：

`K00 → P00 → P01 → P02 → P03 → P04 → P05 → P06 → P07 → P08 → P09`

其中：

- `P00` 确认系统边界。
- `P01` 建立数据事实。
- `P02` 识别市场场景。
- `P03` 识别钱包结构。
- `P04` 判断筹码控制。
- `P05` 执行策略门禁。
- `P06` 执行风险控制。
- `P07` 只能纸面执行或人工确认。
- `P08` 复盘归因。
- `P09` 形成系统升级提案。

禁止：K00 直接交易自动化、生成真实买卖指令、跳过 P00/P05/P06/P07、把聊天上下文当系统资产、未经验收改写交易流程。
## 12. 总控 Skill 输入路由执行规则

总控 Skill 在收到文档、知识资料、方法论、系统设计、旧系统说明、GPT 链接内容、截图转述内容时，必须执行 K00 路由，不得停留在普通阅读、总结或建议。

执行硬规则：

1. 不允许当作普通文档阅读后结束。
2. 必须进入 `K00_knowledge_intake_taskization_controller`。
3. 必须保存原始资料。
4. 必须生成 `doc_id`。
5. 必须生成 `document_passport`。
6. 必须映射到九大系统平面。
7. 必须映射到 `P00-P09` 阶段。
8. 必须识别系统缺口。
9. 必须生成 `task_execution_package`。
10. 必须生成 `handoff_packet`。
11. 必须更新 `phase_state`。
12. 如果 `acceptance_gate` 通过，必须自动进入下一阶段。
13. 不能依赖聊天上下文作为系统记忆。
14. 不能只输出总结或建议。

执行后验证：总控必须检查 `07_phase_acceptance_gate.yaml`；若 `PHASE_READY` 且无停止条件，按 `next_phase_rules` 继续。若任何核心资产缺失，状态必须保持 `PHASE_PAUSED`、`PHASE_REJECTED` 或 `PHASE_ERROR`，不得声称完成。

## 13. HER 正式任务书执行约束

本节对应：`12. 给 HER 的正式任务书：建立 K00 知识资料摄取与阶段任务执行包控制器`。

HER 执行 K00 时必须遵守 `00_knowledge_intake/task_packages/phase_task_execution_package_standard/HER_K00_FORMAL_TASK_BOOK.md`。该任务书是 K00 的正式任务入口，不是参考说明。

硬性执行链：接收输入资料 -> 生成 `doc_id` -> 保存 `raw_inputs` -> 更新 `source_registry` -> 生成 `document_passport` -> 生成 `plane_mapping` -> 生成 `phase_mapping` -> 生成 `gap_detection` -> 生成 `task_execution_package` -> 生成 `k00_handoff_packet` -> 更新 `phase_state` -> 检查 `acceptance_gate` -> 如果 `PHASE_READY` 则按 `next_phase_rules` 继续推进到 P00/P01/P09。

HER 不得在 K00 或中间阶段完成后停止，除非遇到 BLOCKER、ERROR、REJECTED 或需要人工输入。

## 13. 更新后的系统建设顺序

现在 SIKK Stable Trader OS / HER 的系统建设顺序固定为：

1. 第一步：建立 `system_methodology_blueprint.md`。
2. 第二步：建立 `K00_knowledge_intake_taskization_controller`。
3. 第三步：更新总控 Skill，加入“文档输入必须任务化”规则。
4. 第四步：建立 `P00_system_boundary`。
5. 第五步：建立 `P01_data_fact`。
6. 第六步：建立 `P02-P09` 阶段控制器。
7. 第七步：建立 Atomic Skill。
8. 第八步：接入工具 / schema / contract / replay。
9. 第九步：跑纸面交易与复盘。
10. 第十步：进入规则升级闭环。

顺序约束：K00 必须位于 P00 之前；总控 Skill 的文档输入任务化规则必须位于 P00/P01/P02-P09 执行之前；纸面交易与复盘必须位于工具/schema/contract/replay 接入之后；规则升级闭环必须基于复盘结果，而不是基于聊天上下文。

## 14. 本次版本更新的核心结论

HER 输入文档 / 知识资料时，不能再当作普通文档阅读。

必须新增 K00 知识资料摄取与任务化控制器。

K00 的作用是把所有输入资料变成：

- 原始资料保存
- 文档护照
- 系统平面映射
- 阶段映射
- 缺口识别
- 阶段任务执行包
- `phase_state`
- `acceptance_gate`
- `handoff_packet`

这样 HER 才能不依赖聊天上下文，而是依赖系统数据执行长任务。

### 本次认知升级点

1. 上传资料不是普通文档，而是系统建设输入。
2. HER 不能只读文档、总结文档，必须先保存和任务化。
3. 必须新增 K00 知识摄取与任务化控制器。
4. Phase Controller 必须是阶段运行单元，不是阶段说明文档。
5. 每个阶段必须有 9 个核心文件：manifest、context、objective_tree、input_contract、output_contract、execution_protocol、acceptance_gate、state、handoff_schema。
6. HER 长任务不能完成一个阶段就停，必须通过 acceptance_gate 决定是否进入下一阶段。
7. 系统不能依靠上下文，必须依靠文件化系统数据、状态回写和 handoff。

### 版本边界

本次更新是 HER / SIKK Stable Trader OS 的系统建设顺序与知识输入治理升级，不授权真实交易执行、签名、broadcast、swap 或私钥材料处理。K00 只负责知识资料资产化、任务化、验收与交接。
