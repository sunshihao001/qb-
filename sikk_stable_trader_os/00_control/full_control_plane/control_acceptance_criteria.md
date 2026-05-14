# Control Acceptance Criteria

## CONTROL_READY 必须满足
1. 27 个控制面文件全部存在。
2. YAML/JSON 可解析。
3. 全局 Plane 注册、Controller 注册、依赖图、执行顺序、任务树、合约路由、输入输出合约、验收门、状态码、硬否定、状态机、权限矩阵、工具注册、路径路由、handoff、审计、缺口、失败恢复、legacy、人类 override、HER 协议均存在。
4. 不存在阶段越权逻辑。
5. 不存在跳过验收进入下游的逻辑。
6. 不存在自动实盘执行越权。

## CONTROL_READY_WITH_GAPS
文件/合约/控制面可作为系统总控基座，但存在非阻断缺口：Controller 未全部代码化、验收门未全部自动化、legacy mapping 未实际扫描、工具未实测、handoff 未集成联调、状态机未接真实 orchestrator、Telegram 状态面板未接入。

## CONTROL_REJECTED
缺少核心注册表、合约、验收门、状态机、失败处理、缺口登记、审计、legacy 策略或存在实盘越权时驳回。
