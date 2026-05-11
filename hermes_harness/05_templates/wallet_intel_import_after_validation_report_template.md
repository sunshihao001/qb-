---
artifact_type: template
status: candidate_verified_by_system_write
version: v2.0
generated_at: 2026-05-07T05:40:28Z
---
# Wallet-Intel 导入后理解验证报告模板 V2.0

## 1. 验证概览
- 验证批次：
- 验证时间：
- 验证任务：
- 抽样 token 数量：3-5
- 验证范围：数据护照 / 事实 / 证据 / 推断 / 结论 / handoff / 字段字典 / 旧路径映射 / 缺失项
- 总体结论：PASS / PARTIAL / FAIL

## 2. 抽样 Token 列表
- Token 1：
- Token 2：
- Token 3：
- Token 4：
- Token 5：

## 3. 单 Token 验证

### Token: <token_address>
- 数据护照：PASS / PARTIAL / FAIL
- 事实层：PASS / PARTIAL / FAIL
- 证据层：PASS / PARTIAL / FAIL
- 推断层：PASS / PARTIAL / FAIL
- 结论层：PASS / PARTIAL / FAIL
- handoff 包：PASS / PARTIAL / FAIL
- 字段字典：PASS / PARTIAL / FAIL
- 旧路径映射：PASS / PARTIAL / FAIL
- 缺失项标记：PASS / PARTIAL / FAIL

#### Hermes 是否能说清
- 这个 token 有哪些数据：
- 哪些是事实：
- 哪些是证据：
- 哪些是推断：
- 哪些是结论：
- 数据来自旧目录哪里：
- 后续模块该读什么：
- 当前缺什么：

#### 结论
- 单 token 判定：PASS / PARTIAL / FAIL
- 主要问题：
- 修复建议：

## 4. 全局问题汇总
- 事实层问题：
- 证据层问题：
- 推断层问题：
- 结论层问题：
- 来源映射问题：
- 下游接续问题：
- 缺失标记问题：

## 5. 通过标准
只有 Hermes 能按 token 清楚说明以下内容，才算理解数据：

```text
有哪些数据；
哪些是事实；
哪些是证据；
哪些是推断；
哪些是结论；
来自旧目录哪里；
后续模块读什么；
当前缺什么。
```

## 6. 复验建议
- 需要修复的项：
- 复验 token 范围：
- 是否允许进入下一阶段：是 / 否
