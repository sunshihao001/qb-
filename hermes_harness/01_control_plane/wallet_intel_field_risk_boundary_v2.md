---
artifact_type: field_dictionary_risk_boundary
status: verified
version: v2.0-stage5
generated_at: 2026-05-07T06:03:18Z
task_type: wallet_intel_semantic_integration
---
# Wallet-Intel 字段风险边界说明 V2.0 — 阶段 5

## 1. 核心边界

```text
字段字典是语义说明，不是交易信号表。
字段用途是帮助理解、追溯、分类、交接，不是直接给出买卖动作。
```

## 2. 关键字段边界

### same_source_group_id
只能解释为：

```text
疑似同源组编号
```

不得解释为：

```text
确定同源
确认同伙
确认同一人
```

### dominant_side_status
只能解释为：

```text
行为推断字段
```

它描述的是主导侧生命周期 / 控筹 / 派发 / 扩张动机的推断状态，不是事实状态。

### wallet_structure_decision
只能解释为：

```text
策略门禁输入
```

它是给状态机、paper runner、dashboard、review 流程读取的输入，不是结果事实。

### WALLET_SUPPORT / WALLET_PAUSE / WALLET_BLOCK
只能解释为：

```text
门禁动作或状态
```

不能解释为：

```text
直接买入信号
直接卖出信号
确定赚钱机会
```

## 3. 风险规则

```text
1. 统计字段不等于事实结论。
2. 结构证据字段不等于同源确认。
3. 行为推断字段必须保留不确定性。
4. 策略交接字段必须带动作边界和失效条件。
5. 未知字段必须进入 unknown_fields_review，不得硬解释。
6. 缺来源字段时不得生成“确定语义”。
```

## 4. 后续模块使用原则

```text
字段字典只告诉后续模块如何读字段。
字段字典不替代事实层、证据层、推断层或策略交接层。
字段字典不能绕过验证。
```
