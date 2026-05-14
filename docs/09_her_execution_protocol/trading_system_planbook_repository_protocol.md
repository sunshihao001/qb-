# 交易系统方案书仓库协议｜Planbook Repository Protocol

- document_id: `trading_system_planbook_repository_protocol`
- version: `v1.0`
- status: `ACTIVE_CONTROL_SURFACE`
- scope: `SIKK Stable Trader OS / HER / full_system_runtime_bundle / P01-P09`
- safety_boundary: `paper-only / no signing / no broadcast / no real trade`
- canonical_planbook_root: `/root/sikk-gmgn/research_loop/plan_books/`
- runtime_reader: `/root/sikk-gmgn/modules/runtime/planbook_repository.py`
- audit_output: `/root/sikk-gmgn/reports/system_audit/planbook_repository_validation.json`

---

## 1. 模块定位

本协议定义“交易系统方案书保存、索引、读取、审计、回流”的标准模块。

它解决的问题不是“文档放在哪里”，而是：

```text
方案书 -> 方案书仓库 -> 机器索引 -> runtime reader -> control plane -> gap/audit -> durable cognition candidate
```

任何交易系统方案、长任务方案、方法论设计、系统认知规则，如果希望被 HER 后续稳定读取，不得只存在于聊天上下文；必须进入本模块或被本模块索引。

---

## 2. 标准保存位置

### 2.1 方案书主仓库

```text
/root/sikk-gmgn/research_loop/plan_books/
```

用途：保存交易系统方案书、长期设计方案、工作流方案、方法论方案。

推荐分层：

```text
research_loop/plan_books/
  index/planbook_index.json
  active/
  draft/
  archived/
  templates/
```

### 2.2 HER 总控协议

```text
/root/sikk-gmgn/docs/09_her_execution_protocol/
```

用途：保存 HER 总控层、系统接入协议、长期控制规则。

### 2.3 可执行任务包

```text
/root/sikk-gmgn/task_books/full_system_runtime_bundle/
```

用途：保存 P01-P09 可执行任务包、Wave 协议、runtime bundle、状态与审计协议。

---

## 3. 方案书 metadata 合约

每份可被系统读取的方案书必须包含以下 metadata 或等价字段：

```text
planbook_id
version
status
scope
owner_layer
source_type
created_at_or_updated_at
runtime_consumption
control_plane_refs
gap_policy
audit_policy
durable_cognition_policy
safety_boundary
```

允许状态：

```text
DRAFT
ACTIVE_CONTROL_SURFACE
RUNTIME_CONSUMABLE
ARCHIVED
REJECTED
```

---

## 4. runtime 读取规则

runtime reader 必须执行：

```text
1. 扫描 canonical_planbook_root 与允许的 HER/taskbook 引用目录
2. 读取 markdown/json 方案书
3. 解析 metadata
4. 校验 required metadata
5. 生成 planbook_index.json
6. 写 validation audit
7. 将 missing/gaps 写入 gap_register
8. 禁止将未验证 assumption 写入 durable cognition
```

如果方案书只有文本但没有 metadata，则状态为：

```text
PLANBOOK_READY_WITH_GAPS
```

如果方案书含真实签名、广播、密钥、真实交易执行授权，则状态为：

```text
PLANBOOK_REJECTED
```

---

## 5. HER 接入规则

HER 在处理交易系统长期任务时，读取顺序应增加：

```text
1. HER 总控协议
2. 目录宪法
3. system directory routes
4. planbook repository protocol
5. planbook_index.json
6. full_system_runtime_bundle
7. 当前 Wave/Pxx taskbook
```

方案书认知只有在满足以下条件后，才可进入 durable cognition candidate：

```text
1. status 是 ACTIVE_CONTROL_SURFACE 或 RUNTIME_CONSUMABLE
2. 有 control_plane_refs
3. 有 runtime_consumption
4. audit_status 不是 REJECTED
5. gap_policy 明确 unresolved gap 不得写成事实
6. 已通过 regression/smoke 或被总控标记为 verified stable rule
```

---

## 6. Stop condition

以下情况必须阻断或降级：

- canonical_planbook_root 不存在：降级并自举目录
- planbook_index.json 不可解析：REJECTED
- 方案书 metadata 缺失：READY_WITH_GAPS
- 方案书引用不存在：READY_WITH_GAPS 或 REJECTED，取决于引用是否为 required
- 出现真实交易授权/签名/广播/密钥读取：REJECTED
- 将 missing/gap/assumption 写为 verified cognition：REJECTED

---

## 7. 验收标准

本模块 READY 条件：

```text
1. research_loop/plan_books/ 目录存在
2. index/planbook_index.json 存在且 JSON parse 通过
3. modules/runtime/planbook_repository.py 可读取并校验方案书
4. reports/system_audit/planbook_repository_validation.json 已生成
5. HER 总控协议引用本协议
6. system_directory_routes.json 登记 planbook routes
7. full_system_workflow_v4 可输出 planbook_repository 状态
8. pytest 覆盖 reader/index/audit/safety boundary
```

若 1-6 满足但 7-8 未完全满足：

```text
PLANBOOK_REPOSITORY_READY_WITH_GAPS
```

若全部满足：

```text
PLANBOOK_REPOSITORY_READY
```
