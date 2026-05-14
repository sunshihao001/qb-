# 12. 给 HER 的正式任务书：建立 K00 知识资料摄取与阶段任务执行包控制器

## 任务名称

建立 K00 知识资料摄取与阶段任务执行包控制器

## 任务目标

当用户输入文档、知识资料、方法论文本、系统设计内容、旧系统资料、GPT 链接内容或截图转述内容时，HER 不得将其当成普通文档阅读后总结。

HER 必须先将资料保存为系统资产，并转化为可调度、可续跑、可验收、可交接的阶段任务执行包。

## 核心原则

1. HER 不能依赖聊天上下文作为系统记忆。
2. HER 必须保存输入资料。
3. HER 必须生成文档护照。
4. HER 必须生成系统平面映射。
5. HER 必须生成 P00-P09 阶段映射。
6. HER 必须识别系统缺口。
7. HER 必须生成阶段任务执行包。
8. HER 必须生成 phase_state。
9. HER 必须生成 handoff_packet。
10. HER 必须通过 acceptance_gate 判断阶段是否完成。
11. 当前阶段完成后，如果允许进入下一阶段，不得停止，必须继续推进。

## 必须建立目录

```text
/root/sikk-gmgn/sikk_stable_trader_os/00_knowledge_intake/
  raw_inputs/
  source_registry/
  document_passports/
  corpus_index/
  system_mapping/
  gap_detection/
  task_packages/
  intake_reports/
  handoff_packets/
```

## 必须建立 K00 Phase Package

```text
/root/sikk-gmgn/sikk_stable_trader_os/06_phase_controllers/K00_knowledge_intake_taskization/
  01_phase_manifest.yaml
  02_phase_context_pack.md
  03_phase_objective_tree.yaml
  04_phase_input_contract.json
  05_phase_output_contract.json
  06_phase_execution_protocol.md
  07_phase_acceptance_gate.yaml
  08_phase_state.json
  09_phase_handoff_packet.schema.json
```

## 每个文件职责

1. `01_phase_manifest.yaml`：定义阶段是谁、负责什么、权限边界是什么。这是阶段身份证。
2. `02_phase_context_pack.md`：给 HER 的阶段上下文压缩包。HER 运行时必须先读它，避免把资料当普通文档总结。
3. `03_phase_objective_tree.yaml`：定义目标层级和任务树，让 HER 按任务树推进，而不是自由发挥。
4. `04_phase_input_contract.json`：定义阶段输入，禁止使用未声明输入。
5. `05_phase_output_contract.json`：定义阶段必须输出什么。
6. `06_phase_execution_protocol.md`：告诉 HER 怎么运行，不是描述阶段。这是 HER 长任务运行核心。
7. `07_phase_acceptance_gate.yaml`：定义完成、暂停、拒绝、错误的判定。没有验收门，不允许说完成。
8. `08_phase_state.json`：运行状态文件。HER 每完成一步都必须回写。
9. `09_phase_handoff_packet.schema.json`：定义交接包结构，禁止随便写 JSON。

## 执行要求

1. 接收输入资料后，生成 doc_id。
2. 保存原始资料到 raw_inputs。
3. 更新 source_registry。
4. 生成 document_passport。
5. 生成 plane_mapping。
6. 生成 phase_mapping。
7. 生成 gap_detection。
8. 生成 task_execution_package。
9. 生成 k00_handoff_packet。
10. 更新 phase_state。
11. 检查 acceptance_gate。
12. 如果 K00 = PHASE_READY，自动进入下一阶段。
13. 如果下一个阶段是 P00_system_boundary，则创建或更新 P00 阶段包。
14. 如果下一个阶段是 P01_data_fact，则创建或更新 P01 阶段包。
15. 如果下一个阶段是 P09_self_upgrade，则生成升级提案。
16. 中间阶段完成后不得停止，必须根据 next_phase_rules 继续推进，直到遇到 BLOCKER、ERROR、REJECTED 或需要人工输入。

## 禁止事项

1. 禁止只总结文档。
2. 禁止只输出建议。
3. 禁止不保存资料。
4. 禁止不生成任务包。
5. 禁止没有 phase_state。
6. 禁止没有 acceptance_gate。
7. 禁止没有 handoff_packet。
8. 禁止依赖聊天上下文作为唯一记忆。
9. 禁止当前阶段未验收就进入下一阶段。
10. 禁止把知识资料直接变成交易判断。

## 验收标准

1. K00 目录存在。
2. K00 Phase Package 9 个文件全部存在。
3. 原始资料保存机制存在。
4. document_passport 机制存在。
5. plane_mapping 机制存在。
6. phase_mapping 机制存在。
7. gap_detection 机制存在。
8. task_execution_package 机制存在。
9. phase_state 可更新。
10. acceptance_gate 可判断状态。
11. handoff_packet schema 存在。
12. K00 完成后可自动进入 P00 / P01 / P09。
13. HER 不再把输入资料当普通文档阅读。

## 运行边界

本任务书不授权真实交易自动化。K00 的职责是知识资料资产化与任务化；不得生成真实买卖指令、签名交易、广播交易或私钥材料。
