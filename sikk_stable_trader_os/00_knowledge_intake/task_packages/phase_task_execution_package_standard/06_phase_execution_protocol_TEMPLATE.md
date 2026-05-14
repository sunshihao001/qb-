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
