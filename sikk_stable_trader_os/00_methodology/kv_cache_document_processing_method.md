# KV Cache Enhanced Document Processing Method

- doc_id: `DOC-20260513-001`
- status: `METHODOLOGY_ADDENDUM_READY_FOR_K00_AND_P00_CONSUMPTION`
- scope: `SIKK Stable Trader OS / K00 knowledge intake / document processing vNext`
- created_at: `2026-05-13T02:48:33Z`
- safety_boundary: `OBSERVE_PAPER_ONLY`

## 1. 定位

KV Cache 在新版文档处理方法中不是“聊天缓存”，也不是临时摘要。

它是 K00 文档处理链路中的 **结构化语义缓存层**，用于把每份资料拆成可复用、可追踪、可验收的 Key-Value 知识单元，并让后续 Stable Trader OS 体系设计、Phase Controller、Contract、Schema、Rule、Task Package 能够复用这些稳定资产。

核心目标：

```text
文档原文
→ 分块 / 段落 / 章节
→ KV 语义单元
→ 资产分类
→ 系统平面映射
→ 阶段映射
→ 合约/规则/任务包生成
→ 下游消费与回写
```

## 2. 为什么需要 KV Cache

现有 K00 已经能保存 raw、生成 passport、mapping、gap、task package、handoff。

但缺口是：

- 文档内容被处理后，稳定知识单元没有统一缓存键。
- 多份文档中重复出现的规则、字段、阶段目标、反证逻辑无法自动去重与复用。
- 交易系统体系设计依赖长文档、跨阶段资料和多轮增量输入，单次上下文容易丢失细节。
- 文档资产化和系统消费之间缺少可查询的“中间知识层”。
- 后续 P00/P01-P09 需要的是可引用的字段、规则和任务，而不是整篇文档摘要。

因此 KV Cache 必须成为新版文档处理的前置方法。

## 3. KV Cache 的核心对象

每个 KV 单元必须至少包含：

```yaml
kv_item:
  key: "KV::<doc_id>::<asset_class>::<stable_slug>::<version>"
  doc_id: "DOC-20260513-001"
  source_span:
    raw_path: "00_knowledge_intake/raw_inputs/DOC-20260513-001_kv_cache_document_processing_model.md"
    section: "string"
    line_start: null
    line_end: null
  asset_class: "judgement_logic | field_requirement | counter_evidence_rule | quantitative_model | behavior_inference | output_template | phase_contract | task_node | glossary"
  value:
    summary: "可复用语义内容"
    normalized_form: "系统可消费表达"
    code_facing_interpretation: "如果需要落代码，入口函数/字段/测试/输出路径是什么"
  mappings:
    planes: []
    phases: []
    contracts: []
    schemas: []
  reuse_policy:
    cache_status: "ACTIVE | SUPERSEDED | CONFLICT | DRAFT"
    dedupe_key: "semantic_hash_or_rule_id"
    version: "v1"
  evidence:
    evidence_level: "EVIDENCE_A_STRONG | EVIDENCE_B_MEDIUM | EVIDENCE_C_WEAK | EVIDENCE_D_UNVERIFIED"
    source_doc_hash: "a595f3239dd0db6bd066f0969ab95b03b5f07ee1d0b551608a7eec51ca1acbb5"
  governance:
    allowed_consumers: ["K00", "P00", "P01", "P02", "P03", "P04", "P05", "P06", "P07", "P08", "P09"]
    forbidden_uses: ["direct_real_trade", "private_key", "auto_broadcast"]
```

## 4. 新版文档处理链路

新版 K00 文档处理应从“文档级处理”升级成“文档级 + KV 单元级双层处理”。

```text
Step 0: 接收资料
Step 1: 保存 raw input，生成 doc_id 和 sha256
Step 2: 生成 document_passport
Step 3: 分块：按章节/语义/规则/字段/任务节点切分
Step 4: 为每个稳定语义单元生成 KV item
Step 5: KV item 归入六类资产或扩展资产类
Step 6: 去重、冲突检测、版本继承
Step 7: 生成 system plane mapping / phase mapping
Step 8: 生成 gap detection
Step 9: 从 KV items 生成 task_execution_package
Step 10: 生成 handoff_packet，携带 kv_cache_manifest
Step 11: 下游阶段消费后回写 consumed_by / implemented_by / superseded_by
```

## 5. 与用户偏好的六类资产吸收法对齐

KV Cache 必须兼容用户已确认的六类资产吸收方式：

- `judgement_logic`：判断逻辑资产
- `field_requirement`：字段需求资产
- `counter_evidence_rule`：反证规则资产
- `quantitative_model`：量化模型资产
- `behavior_inference`：行为推断资产
- `output_template`：输出模板资产

同时允许 Stable Trader OS 扩展：

- `phase_contract`：阶段输入/输出/验收合约
- `task_node`：可执行任务节点
- `glossary`：术语与枚举
- `directory_rule`：目录与路由规则
- `runner_binding`：runner/tool 绑定规则

## 6. 对交易系统体系设计的作用

KV Cache 对 Stable Trader OS 的核心价值：

- 体系设计不再只靠大文档上下文，而是能追踪到具体规则单元。
- Phase Controller 可以从 KV items 自动组装目标树、输入合约、输出合约、验收门。
- P01-P07 交易判断逻辑可以引用规则 key，而不是引用一整篇方法论。
- P08/P09 复盘升级时可以精确标记哪个 KV 规则被证伪、升级或废弃。
- 文档新增内容不会直接污染系统，需要先进入 KV cache，再经映射、验收、handoff 消费。

## 7. 必须新增/更新的产物

建议新增：

```text
00_knowledge_intake/kv_cache/
  kv_cache.schema.json
  kv_cache_manifest_<doc_id>.json
  kv_items_<doc_id>.jsonl
  kv_conflict_report_<doc_id>.json
```

建议更新：

```text
00_knowledge_intake/document_passports/document_passport_<doc_id>.yaml
00_knowledge_intake/system_mapping/plane_mapping_<doc_id>.json
00_knowledge_intake/system_mapping/phase_mapping_<doc_id>.json
00_knowledge_intake/gap_detection/gap_detection_<doc_id>.json
00_knowledge_intake/task_packages/task_execution_package_<doc_id>.json
00_knowledge_intake/handoff_packets/k00_handoff_packet_<doc_id>.json
```

## 8. 验收标准

K00 只有在以下条件满足时，才能说 KV Cache 已融入新版文档处理方法：

- raw input 已保存。
- document_passport 已生成。
- KV cache 方法论 addendum 已生成。
- kv_cache schema 已有草案。
- 至少一个 kv_cache_manifest 已生成。
- task_execution_package 明确列出需要更新的 K00/P00 文件。
- handoff_packet 明确把该升级交给 P00 / K00 implementation。
- 不把 KV Cache 当作聊天记忆或摘要缓存。
- 不允许 KV Cache 绕过合约、验收门、hard negative 和 paper-only 边界。

## 9. 当前状态

本文件是方法论接入层，不代表 runner 已完成。

当前状态应标记为：

```text
KV_CACHE_METHOD_ACCEPTED_IMPLEMENTATION_REQUIRED
```

下一步应由 K00/P00 生成实现任务：

1. 新增 `kv_cache.schema.json`。
2. 新增 KV item extractor / manifest writer。
3. 修改 K00 handoff_packet，加入 `kv_cache_manifest`。
4. 修改 task package generator，让任务节点能引用 `kv_item.key`。
5. 增加验收：没有 KV manifest 的新版文档处理只能是 `K00_READY_WITH_KV_GAP`。
