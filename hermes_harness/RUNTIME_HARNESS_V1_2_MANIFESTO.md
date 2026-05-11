---
artifact_type: manifesto
status: verified
version: v1.2
valid_until: null
---
# Hermes V1.2 运行时式 Harness 总纲

## 核心判断
Hermes V1.2 的重点不是继续堆目录，而是把 Hermes 从“文档式 Harness”升级成“运行时式 Harness”。

## V1.0 / V1.1 解决的事
- 有目录
- 有规则
- 有任务护照
- 有验证与恢复
- 有控制闭环

## V1.2 要解决的事
Hermes 每一轮执行前如何治理输入；
执行中如何约束上下文、工具、权限与中断；
执行后如何验证、恢复、压缩、写回；
失败时如何保持执行叙事一致；
如何把验证者与执行者隔离。

## 必须补齐的 8 个运行时能力
1. 运行时状态机
2. 输入治理队列
3. 上下文预算制度
4. 工具调度账本
5. 中断语义
6. 恢复熔断
7. 执行叙事一致性
8. 内部验证者隔离

## 目标形态
补齐以上 8 项后，Hermes 应从：
- 可控执行环境
- 可续跑任务系统
- 可验证输出系统
- 可审计 AI 工作台

进一步升级为：
- 有状态的运行时系统

## 运行时原则
- 每轮执行前先治理输入
- 每轮执行中必须受上下文预算约束
- 每轮工具调用必须记录账本
- 每轮都要先判权限，再执行
- 每轮中断都要保留可恢复语义
- 每轮失败都要有熔断与恢复路径
- 每轮输出都要能保持叙事一致
- 执行者与验证者必须隔离

## 核心防线
真正防止 AI 做表面工程的，不是提醒，而是：
- artifact contract
- verification
- surface completion audit
- runtime state machine
- input governance queue
- context budget
- tool dispatch ledger
- verifier isolation

## 结论
V1.2 的本质不是更多模板，而是把 Hermes 变成一个可治理、可恢复、可解释、可审计的运行时系统。
