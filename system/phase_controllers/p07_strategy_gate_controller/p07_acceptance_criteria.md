# P07 Acceptance Criteria

生成时间：2026-05-12T04:08:53Z

P07_READY 要求：41 个系统文件存在；29 个运行数据目录存在；策略注册、硬否定、各 Gate schema、Gap Policy、Hard Negative Rules、State Machine、Trace、P08 Request、P07→P08 Handoff、报告与执行协议均存在；禁止 buy_signal / direct paper runtime / bypass P08 / live execution。

状态定义：
- P07_READY：设计包完整且无阻断缺口。
- P07_READY_WITH_GAPS：设计包完整，但 runner/tool binding、真实 P06 handoff 执行、P08 联调尚未完成。
- P07_REJECTED：核心合约或策略政策缺失。
- P07_BLOCKED：缺 P06 handoff、trace、acceptance，或出现 live execution / buy signal / direct paper runtime 路径。

本次包落地验收目标为：P07_PACKAGE_READY_WITH_RUNTIME_GAPS，不开放 runtime、paper runtime、live execution。
