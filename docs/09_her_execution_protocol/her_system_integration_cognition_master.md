# HER 系统接入与认知更新总控主文档

- document_id: `her_system_integration_cognition_master`
- version: `v1.0`
- scope: `SIKK Stable Trader OS / full_system_runtime_bundle / P01-P09`
- status: `ACTIVE_CONTROL_SURFACE`
- safety_boundary: `paper-only / no signing / no broadcast / no real trade`
- canonical_bundle: `/root/sikk-gmgn/task_books/full_system_runtime_bundle/`
- owner_layer: `HER total control plane`

---

## 1. 文件定位

本文件是 SIKK/HER 系统中“文档如何真正进入系统”的总控主文档。

它不是普通说明文，也不是阶段任务书，而是一个系统接入协议：

```text
文档 -> 控制面 -> runtime state -> gap register -> audit -> regression -> durable cognition
```

凡是 P01-P09、Wave runtime、full_system_runtime_bundle、阶段任务包、方案书、长期任务协议，只有完成本文件定义的接入条件，才算真正进入系统。

---

## 2. 核心原则

### 2.1 文档不是终点

```text
DOC_WRITTEN != SYSTEM_INTEGRATED
```

文档写完只代表存在文本，不代表：

- runtime 能读取
- 状态机能推进
- audit 能回写
- gap 能传播
- recovery 能恢复
- cognition 能沉淀

因此，任何“只写文档”的任务最多只能是：

```text
DOCUMENT_READY
```

不得直接声明：

```text
FULL_SYSTEM_BUNDLE_READY
```

### 2.2 系统接入优先级

```text
文档完整度
< 控制面引用
< runtime 可消费
< 状态机可推进
< gap 可同步
< audit 可追溯
< regression 可复跑
< verified cognition 可沉淀
```

### 2.3 认知更新不是记笔记

认知更新不是把当前任务过程写进 memory。

认知更新只允许沉淀稳定、可复用、已验证的规则：

- verified stable rule
- reusable control-plane rule
- repeatable runtime workflow
- accepted failure/recovery pattern
- durable directory/contract convention

以下内容不得写入长期认知：

- temporary task progress
- unresolved gap
- unverified assumption
- degraded status 被包装成 ready
- missing 被写成事实
- 一次性执行日志

---

## 3. 系统接入判定标准

一个文档、方案、任务包或 bundle 必须同时满足以下条件，才算 `SYSTEM_INTEGRATED`：

```text
1. control plane 已引用
2. runtime state 可消费
3. next_allowed_task 可解析
4. gap register 可读取
5. stop condition 可触发
6. audit report 可回写
7. handoff packet 可生成或读取
8. regression route 可回到失败点
9. verified rules 可进入 durable cognition candidate
```

若 1-6 未满足，状态必须是：

```text
SYSTEM_REJECTED
```

若 1-6 满足，但 7-9 未完全满足，状态必须是：

```text
SYSTEM_READY_WITH_GAPS
```

只有 1-9 全部满足，且 `gap_register == []`，才允许声明：

```text
SYSTEM_READY
```

---

## 4. full_system_runtime_bundle 接入规则

`full_system_runtime_bundle` 是 P01-P09 的全阶段任务包总装层。

它必须被以下系统层读取或引用：

### 4.1 总控入口

- `docs/09_her_execution_protocol/her_total_control_execution_protocol.md`
- `task_books/full_system_runtime_bundle/00_full_bundle_manifest.md`
- `task_books/full_system_runtime_bundle/full_system_runtime_bundle_index.json`

### 4.2 状态与路由

- `task_books/full_system_runtime_bundle/01_full_execution_order.md`
- `task_books/full_system_runtime_bundle/08_runtime_state_protocol.md`
- `runtime_logs/full_system_runtime/workflow_v4_state.json`

### 4.3 gap 与阻断

- `task_books/full_system_runtime_bundle/04_stop_condition_protocol.md`
- `task_books/full_system_runtime_bundle/16_gap_aware_progression_protocol.md`
- `reports/system_audit/full_system_workflow_v4_gap_register.json`

### 4.4 审计与验收

- `task_books/full_system_runtime_bundle/05_audit_protocol.md`
- `task_books/full_system_runtime_bundle/15_full_system_acceptance_protocol.md`
- `reports/system_audit/full_system_runtime_bundle_validation.json`
- `reports/system_audit/full_system_workflow_v4_audit.md`

### 4.5 认知更新桥接

- `task_books/full_system_runtime_bundle/17_system_integration_and_cognition_protocol.md`
- `docs/09_her_execution_protocol/trading_system_planbook_repository_protocol.md`
- `research_loop/plan_books/index/planbook_index.json`
- 本文件：`docs/09_her_execution_protocol/her_system_integration_cognition_master.md`

---

## 5. P01-P09 任务包接入标准

每个阶段任务包必须具备以下字段或等价章节：

```text
目标
边界
输入
输出
handoff
状态码
missing
阻断
降级
验收
审计
next_allowed_task
```

缺任一项，阶段不得宣称 READY，只能进入：

```text
PHASE_READY_WITH_GAPS
```

如果缺失输入、输出、阻断、验收、审计中的任意关键项，则进入：

```text
PHASE_REJECTED
```

---

## 6. Wave 接入标准

### 6.1 Wave 0：总控协议层

必须完成：

- manifest
- execution order
- runtime state protocol
- stop condition protocol
- audit protocol
- acceptance protocol
- gap-aware progression protocol
- system integration cognition protocol

Wave 0 通过后，允许进入：

```text
WAVE_01_P01_P03_FOUNDATION_RUNTIME
```

### 6.2 Wave 1：P01-P03

必须检查：

- P01 数据事实门是否可验收
- P02 结构映射门是否可交接
- P03 控制与约束门是否可产生下游 hard negative / control flags

Wave 1 不允许直接推导交易结论。

### 6.3 Wave 2：P04-P05

必须检查：

- 场景识别是否只基于上游证据
- 位置状态是否保留 missing / degraded
- 不得用情绪判断覆盖结构证据

### 6.4 Wave 3：P06-P07

必须检查：

- 策略只输出 paper decision
- 执行风控只输出 risk gate
- 禁止 signing / broadcast / real trade

### 6.5 Wave 4：P08-P09

必须检查：

- P08 只做复盘学习
- P09 只生成升级候选
- 复盘建议不得自动上线

### 6.6 Verification

必须运行：

```bash
python3 -m pytest -q tests/test_full_system_workflow_v4.py tests/test_full_system_runtime_runner.py
```

如涉及阶段 runner 或新增协议扫描，应追加对应测试。

---

## 7. 认知更新规则

### 7.1 可沉淀为认知的内容

满足以下条件才可进入 durable cognition：

```text
1. 多文件一致引用
2. runtime 或测试验证通过
3. 不依赖一次性上下文
4. 不包含未解决 gap
5. 不包含 secret / token / private key
6. 不改变 paper-only 安全边界
```

### 7.2 不可沉淀为认知的内容

以下内容必须留在报告或 gap register，不得进入长期认知：

```text
- 当前任务进度
- 临时 TODO
- 单次测试日志
- unresolved gap
- guessed rule
- degraded assumption
- missing field
- API key / token / secret
```

### 7.3 cognition candidate 格式

任何候选认知必须写成声明式事实，而不是命令式指令：

```text
正确：full_system_runtime_bundle 的 READY 判定要求 gap_register 为空且 runtime/audit 已接入。
错误：以后每次都要把 full_system_runtime_bundle 判成 READY。
```

---

## 8. 状态机

### 8.1 文档状态

```text
DOCUMENT_MISSING
DOCUMENT_DRAFTED
DOCUMENT_LINKED
DOCUMENT_CONSUMABLE
```

### 8.2 系统状态

```text
SYSTEM_REJECTED
SYSTEM_READY_WITH_GAPS
SYSTEM_READY
```

### 8.3 Bundle 状态

```text
FULL_SYSTEM_BUNDLE_REJECTED
FULL_SYSTEM_BUNDLE_READY_WITH_GAPS
FULL_SYSTEM_BUNDLE_READY
```

### 8.4 状态升级规则

```text
DOCUMENT_DRAFTED -> DOCUMENT_LINKED
需要：manifest/index/control plane 引用

DOCUMENT_LINKED -> DOCUMENT_CONSUMABLE
需要：runtime state / wave runner 可读取

SYSTEM_READY_WITH_GAPS -> SYSTEM_READY
需要：gap_register == [] 且 regression 通过

READY_WITH_GAPS 不得被人工口头升级为 READY
```

---

## 9. 审计回写规则

每次系统接入或认知更新后，必须至少更新一个审计面：

- audit markdown
- validation json
- gap register
- runtime state
- handoff packet

审计必须记录：

```text
- changed_files
- linked_control_files
- status_before
- status_after
- gaps_remaining
- next_allowed_task
- safety_boundary
- verification_command
- verification_result
```

---

## 10. 失败与恢复规则

以下情况必须进入 patch/regression loop：

```text
- 控制面未引用
- index 未登记
- runtime state 无法消费
- audit 未回写
- gap register 不一致
- READY_WITH_GAPS 被误报 READY
- P06/P07 出现真实交易动作
- P08/P09 自动上线升级建议
```

恢复路径：

```text
failed_component
-> gap_register
-> task_6_patch_regression_loop
-> targeted patch
-> regression
-> reroute_to_failed_wave_or_e2e
```

---

## 11. 本文件对当前 Task0 的结论

当前 Task0 的正确目标不是“写出 P01-P09 文档”，而是：

```text
建立一个可被 HER 控制面读取、可由 runtime 推进、可被 audit 验证、可由 gap register 修复、可把 verified rule 沉淀为长期认知的 full_system_runtime_bundle。
```

在 Wave1-Wave4 与 verification 未完成前，最终候选状态保持：

```text
FULL_SYSTEM_BUNDLE_READY_WITH_GAPS
```

不得声明：

```text
FULL_SYSTEM_BUNDLE_READY
```

---

## 12. 下一步路由

当前允许的下一步是：

```text
WAVE_01_P01_P03_FOUNDATION_RUNTIME
```

执行重点：

```text
1. 核对 P01-P03 任务包是否满足接入标准
2. 缺项写入 gap register
3. 补齐阶段 contract / handoff / audit / status
4. 运行 workflow v4 回归
5. 更新 runtime bundle validation
```
