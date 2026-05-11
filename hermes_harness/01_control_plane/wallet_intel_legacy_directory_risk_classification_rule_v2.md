---
artifact_type: legacy_directory_risk_classification_rule
status: verified
version: v2.0-stage7
generated_at: 2026-05-07T08:15:59Z
task_type: wallet_intel_semantic_integration
---
# Wallet-Intel 旧目录风险分级规则 V2.0 — 阶段 7

## 1. 风险等级

```text
R0：低风险历史参考目录
R1：可只读补查目录
R2：高价值旧数据目录，只允许 copy-only 导入
R3：兼容依赖目录，仍被代码调用，必须 compatibility_required
R4：敏感/危险目录，禁止读取或输出内容
```

## 2. 分级标准

### R0：低风险历史参考目录

```text
只含公开报告、说明文档、历史摘要；
不含敏感凭证；
不被代码直接调用；
默认只读。
```

### R1：可只读补查目录

```text
含历史数据源或旧报告；
可通过 legacy_path_map 定位；
允许只读补查；
不允许写入。
```

### R2：高价值旧数据目录

```text
含事实、证据、字段、token 原始材料；
需要进入新标准体系；
只允许 copy-only；
复制后必须记录 checksum 和 old_path/new_path。
```

### R3：兼容依赖目录

```text
仍被代码、reader、dashboard、脚本或报告调用；
必须标记 compatibility_required；
在替换前保留只读；
不得删除、移动或覆盖。
```

### R4：敏感/危险目录

```text
可能包含私钥、API key、token、auth、.env、钱包密钥、未脱敏日志；
禁止读取或输出内容；
如需处理，只记录路径风险，不读取内容。
```

## 3. 风险动作矩阵

| 等级 | 默认动作 | 是否可读 | 是否可复制 | 是否可写 | 是否可删/移 | 备注 |
|---|---|---:|---:|---:|---:|---|
| R0 | 保留参考 | 是 | 否 | 否 | 否 | 只读历史参考 |
| R1 | 映射补查 | 是，需 mapping | 否 | 否 | 否 | fallback only |
| R2 | copy-only 导入 | 是，需授权 | 是，需授权 | 否 | 否 | 必须 checksum |
| R3 | 兼容保留 | 是，需说明 | 否 | 否 | 否 | compatibility_required |
| R4 | 阻断 | 否 | 否 | 否 | 否 | 只记录风险，不读取内容 |

## 4. 失败处理

```text
路径风险不明 → 标记 unknown_risk，停止读取。
发现敏感迹象 → 标记 R4，停止读取，不输出内容。
发现仍被代码调用 → 标记 R3 compatibility_required。
缺映射 → 不允许 fallback，写 trace_missing。
```
