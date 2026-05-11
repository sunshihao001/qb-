---
artifact_type: routing_test_cases
status: verified
version: v2.0-stage1
generated_at: 2026-05-07T05:48:09Z
target_task_type: wallet_intel_semantic_integration
---
# Wallet-Intel 路由测试样例 V2.0 — 阶段 1

## 1. 测试目标
验证 Hermes 遇到 Wallet-Intel 钱包数据语义整合相关输入时，能正确路由到：

```text
wallet_intel_semantic_integration
```

而不是普通目录整理任务。

## 2. 正例：必须命中

### Case P1：钱包数据
输入：
```text
整理这个 token 的钱包数据，区分钱包事实和推断。
```
期望：
```text
route_decision = wallet_intel_semantic_integration
matched_keywords = [钱包数据, 钱包事实]
```

### Case P2：钱包采集
输入：
```text
把钱包采集结果做成数据护照。
```
期望：
```text
route_decision = wallet_intel_semantic_integration
matched_keywords = [钱包采集, 数据护照]
```

### Case P3：钱包画像 / 钱包交易
输入：
```text
检查钱包画像和钱包交易字段是否能解释。
```
期望：
```text
route_decision = wallet_intel_semantic_integration
matched_keywords = [钱包画像, 钱包交易]
```

### Case P4：结构分析 / 同源证据 / 筹码分析
输入：
```text
把结构分析、同源证据、筹码分析分到事实层、证据层、推断层。
```
期望：
```text
route_decision = wallet_intel_semantic_integration
matched_keywords = [结构分析, 同源证据, 筹码分析]
```

### Case P5：主导侧行为
输入：
```text
主导侧行为应该放在哪一层，如何进入 handoff？
```
期望：
```text
route_decision = wallet_intel_semantic_integration
matched_keywords = [主导侧行为, handoff]
```

### Case P6：旧目录导入 / 旧路径映射
输入：
```text
旧目录导入前先建立旧路径映射和字段字典。
```
期望：
```text
route_decision = wallet_intel_semantic_integration
matched_keywords = [旧目录导入, 旧路径映射, 字段字典]
```

### Case P7：英文 wallet intel
输入：
```text
Build wallet intel import validation for source wallet bot outputs.
```
期望：
```text
route_decision = wallet_intel_semantic_integration
matched_keywords = [wallet intel, source wallet bot]
```

### Case P8：intel bot
输入：
```text
intel bot 后续该读取哪些 handoff 包？
```
期望：
```text
route_decision = wallet_intel_semantic_integration
matched_keywords = [intel bot, handoff]
```

## 3. 混合例：必须先 Wallet-Intel，目录治理为子步骤

### Case M1：目录整理 + 钱包语义
输入：
```text
整理旧目录里的钱包事实和同源证据，放到新目录。
```
期望：
```text
primary_route = wallet_intel_semantic_integration
secondary_workflow = directory_governance
reason = 命中钱包事实、同源证据；不能按普通目录整理处理
```

### Case M2：数据整合 + 字段字典
输入：
```text
做一次数据整合，顺便把字段字典和数据护照补上。
```
期望：
```text
primary_route = wallet_intel_semantic_integration
matched_keywords = [数据整合, 字段字典, 数据护照]
```

## 4. 反例：不得误命中

### Case N1：普通 README 整理
输入：
```text
整理 README 的章节结构。
```
期望：
```text
route_decision != wallet_intel_semantic_integration
```

### Case N2：普通代码重构
输入：
```text
重构 Python 日志模块。
```
期望：
```text
route_decision != wallet_intel_semantic_integration
```

### Case N3：普通文件归档
输入：
```text
把下载目录里的图片按日期归档。
```
期望：
```text
route_decision != wallet_intel_semantic_integration
```

## 5. 测试通过标准

```text
所有 P 类正例命中 wallet_intel_semantic_integration；
所有 M 类混合例以 wallet_intel_semantic_integration 为主路由；
所有 N 类反例不误命中；
路由失败时进入 wallet_intel_route_failure_recovery_rule_v2。
```
