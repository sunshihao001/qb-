# K00 Context Pack｜知识摄取与 F00 合法入口桥接

K00 是 HER-DFAFS 的入口控制器，不是普通总结阶段。

## 本阶段为什么存在

F00 不能直接读取聊天上下文作为输入。任何文档、系统资料、方法论文本、粘贴资料，都必须先经过 K00：

1. raw source preservation
2. source registry
3. document passport
4. corpus index
5. system mapping
6. gap detection
7. task/package/handoff

## 本阶段不做什么

- 不直接实现功能代码。
- 不直接跑 V00/R00/A00。
- 不把聊天上下文当长期事实。
- 不跳过 passport/index/mapping/gap。

## 本阶段必须输出什么

K00 handoff packet 必须包含 F00 输入合约要求的字段：

- `k00_handoff_packet`
- `document_passport_refs`
- `corpus_index_refs`
- `system_mapping_refs`
- `gap_detection_refs`
- `kv_retrieval_refs` 可选
- `target_phase_candidates`
- `execution_boundary`
- `write_policy`
- `repo_root`

## 完成状态

- 全字段存在且可追溯：`K00_HANDOFF_READY`
- 有缺口但允许继续：`K00_READY_WITH_GAPS`
- 缺 handoff/passport/index/gap：`K00_BLOCKED`
