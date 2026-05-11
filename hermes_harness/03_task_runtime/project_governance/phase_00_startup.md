# Hermes 项目治理长任务 Phase 0

## 状态
- phase: 00_startup_and_boundary_lock
- status: started

## 目标
锁定边界，初始化运行状态，准备进入只读侦察。

## 已知输入
- task package: `08_reports/project_governance/project_governance_task_package.json`
- project root: `/root/sikk-gmgn`
- harness root: `/root/sikk-gmgn/hermes_harness`

## 约束
- 不删除
- 不移动旧目录
- 不改业务代码
- 不触发交易
- 不读取密钥

## 下一步
进入只读全局侦察，生成初版 inventory。
