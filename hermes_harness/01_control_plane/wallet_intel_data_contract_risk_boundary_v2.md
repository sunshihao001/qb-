---
artifact_type: data_contract_risk_boundary
status: verified
version: v2.0-stage4
generated_at: 2026-05-07T08:39:07Z
task_type: wallet_intel_semantic_integration
---
# Wallet-Intel 数据契约风险边界说明 V2.0 — 阶段 4

## 1. 总原则

```text
数据契约是用途约束，不是交易指令。
契约用于控制读取、验证、追溯和交接，不用于自动买卖判断。
```

## 2. 风险边界

### 原始 / 标准化 / 交易 / 事实契约

```text
可以进入事实层引用，但必须保留来源与时间戳。
不得把统计结果伪装成事实。
```

### 证据 / 候选组 / 资金路径 / 筹码分布

```text
只能作为结构证据或统计证据。
必须带 evidence_level、fact_refs 或统计窗口。
不能直接变成买入依据。
```

### 主导侧行为推断

```text
必须标注 uncertainty。
不能写成确定事实。
不能跳过证据链。
```

### 钱包结构裁决 / handoff

```text
只能作为策略门禁输入或交接输入。
WALLET_SUPPORT / WALLET_PAUSE / WALLET_BLOCK 不是交易信号。
```

### 人类可读报告

```text
可读、可审、可追溯。
不能代替事实层和证据层。
```

## 3. 失效处理

```text
缺输入来源 → contract_invalid
缺核心字段 → contract_partial
缺验证方式 → contract_unverified
缺风险边界 → contract_blocked
```

## 4. 禁止项

```text
禁止将 handoff 当买入信号。
禁止将推断字段当事实字段。
禁止将结构裁决直接写成交易动作。
禁止跳过契约直接读旧目录。
```
