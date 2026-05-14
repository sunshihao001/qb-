# HER_DOC_SYSTEM_AUDIT 固定口令协议

## 1. 触发口令

当用户输入以下任一表达时，进入系统自审流程：

- `HER_DOC_SYSTEM_AUDIT`
- `HER_DOC_SYSTEM_REVIEW`
- “调用文档自动化处理系统项目，先审查自身体系”
- “补全系统阶段文档/系统数据”

## 2. 审计目标

不是总结文档，而是检查 HER-DFAFS 自身是否具备可运行系统的必要资产。

## 3. 审计范围

- canonical root 是否正确
- standalone root 是否被禁写
- controller registry 是否存在
- O00 是否列出所有阶段
- G00 是否定义治理边界
- K00 handoff 是否可被 F00 合法消费
- F00 输入合约是否禁止直接读聊天上下文
- V00/R00/A00/H00/U00/G00 是否具备合约/状态/验收/交接资产
- 状态码、gap、evidence、trace、audit、recovery 是否存在
- CLI/sample replay/config 是否存在

## 4. 输出要求

每次审计必须生成或刷新：

- `audit_result_YYYYMMDD.json`
- `SYSTEM_STAGE_READINESS_MATRIX.md`
- `SYSTEM_GAP_REGISTER.md`
- `SYSTEM_COMPLETION_BACKLOG.md`

## 5. 状态规则

- 缺 K00 handoff：`F00_BLOCKED`
- 缺 document passport：`F00_BLOCKED`
- 缺 corpus index：`F00_BLOCKED`
- 缺 system mapping：`F00_READY_WITH_GAPS` 或 `F00_BLOCKED`
- 缺 gap detection：`F00_BLOCKED`
- 缺 KV：可继续，但标记 `KV_GAP`
- 缺 repo_root：`DESIGN_ONLY`
- 缺 write_policy：禁止写文件，只能 `DESIGN_ONLY`
- 缺 execution_boundary：`F00_BLOCKED`

## 6. 禁止动作

- 不得把聊天上下文当作 F00 输入。
- 不得跳过 K00。
- 不得把 design 文档说成已执行。
- 不得把 sample replay 说成生产运行。
- 不得把 `READY_WITH_GAPS` 改写成 `READY`。
