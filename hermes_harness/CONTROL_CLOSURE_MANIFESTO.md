---
artifact_type: manifesto
status: verified
version: v1.1
valid_until: null
---
# Hermes V1.1 控制闭环总纲

## 核心判断
Hermes V1.1 的重点不是继续堆功能，而是补齐控制闭环。

## 必须优先补齐的 10 项
1. 任务路由
2. 输入契约
3. 输出契约
4. 状态机
5. 权限分级
6. 三段验证
7. 恢复决策
8. 断点续跑
9. 记忆过期
10. 表面完成审计

## 目标形态
补齐以上 10 项后，Hermes 应从“能听命令的 agent”升级为：
- 可控执行环境
- 可续跑任务系统
- 可验证输出系统
- 可审计 AI 工作台

## 专业化原则
- 每个动作都有依据
- 每个产物都有归属
- 每个失败都有恢复
- 每个完成都必须经过验证
- 每个长期记忆都必须经过过期审查

## 关键防线
真正防止 AI 做表面工程的，不是提醒，而是：
- artifact contract
- verification
- surface completion audit

## 长任务原则
Hermes 长任务能否专业化，关键看 checkpoint 和 resume，不是看一次能跑多长。

## 结论
V1.0 是骨架，V1.1 是控制闭环。
