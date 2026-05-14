# HER-DFAFS System Audit Package

固定口令入口：`HER_DOC_SYSTEM_AUDIT`

本目录是 HER 文档自动化处理系统的系统自审入口，不是普通说明文档。它用于检查系统自身是否具备：

- 阶段控制器完整性
- 输入 / 输出合约完整性
- K00→F00→V00→R00→A00→H00→U00→G00→O00 路由闭环
- 状态码、缺口、证据、恢复、审计规则
- 固定口令触发与安全边界

固定口令：

- `HER_DOC_PIPELINE`：启动文档到功能自动化主流程。
- `HER_DOC_SYSTEM_AUDIT`：审计系统自身是否完整。
- `HER_DOC_SYSTEM_REVIEW`：先系统设计审查，再决定是否执行。

重要规则：

1. F00 不得直接读取聊天上下文，必须从 K00 handoff 开始。
2. 缺 K00 handoff = `F00_BLOCKED`。
3. 缺 repo_root / write_policy 时只能进入 `DESIGN_ONLY`。
4. 任何 `READY_WITH_GAPS` 不得被改写为 `READY`。
5. 系统审计只判断结构/合约/证据，不等价于生产可用。
