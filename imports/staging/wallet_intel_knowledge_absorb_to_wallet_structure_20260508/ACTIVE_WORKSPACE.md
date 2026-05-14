# Wallet-Intel Active Workspace

当前有效工作目录：`/root/sikk-wallet-intel/`

群组名称：SIKK Wallet-Intel 协同工作群

## 系统定位

SIKK Wallet-Intel 是结构地址识别、证据归因、行为分类、历史沉淀和 GMGN 备注输出系统。

它不是自动交易系统。

## 三角色分工

### 1. SIKK Orchestrator

当前 Bot：`@haosjjd002bot`

负责：接收用户目标、生成任务编号、判断模块调用、分配任务、检查输出文件、检查字段缺失、汇总结论、生成下一步任务票、防止越权。

不做：不直接判断钱包角色、不直接推断主导侧行为、不直接改代码、不直接交易、不直接生成买/卖建议。

### 2. SIKK Wallet-Fact

当前 Bot：`@sunqbfemxbot`

模块目录：`/root/sikk-wallet-intel/wallet_fact/`

负责：GMGN 数据采集、字段标准化、钱包画像、当前 token 行为分析、资金来源分析、Token 来源分析、同源组识别、筹码分布分析、历史地址库更新、GMGN 备注基础字段生成。

只回答：发生了什么、谁买了、谁卖了、谁还持有、筹码从谁到谁、是否同源、是否回流、历史是否复现。

输出：`wallet_structure_normalized.json`、`chip_distribution_summary.json`、`same_source_groups.json`、`fund_flow_edges.csv`、`address_history.json`、`wallet_fact_report.md`。

不做：不推断主导侧意图、不说准备拉盘、不说准备砸盘、不输出交易建议、不接状态机。

### 3. SIKK Behavior-Inference

当前 Bot：结构行为分析 Bot

模块目录：`/root/sikk-wallet-intel/behavior_inference/`

负责：读取钱包事实模块标准输出，判断疑似吸筹、疑似控盘、疑似洗盘、疑似突破测试、疑似推进拉升、疑似二段扩张、疑似部分派发、疑似主动派发、疑似撤退、疑似再吸筹、疑似再激活，并输出行为解释报告。

只读取：`wallet_structure_normalized.json`、`chip_distribution_summary.json`、`same_source_groups.json`、`fund_flow_edges.csv`、`address_history.json`。

不能直接读取：`state_machine`、`paper runner`、`dashboard`、`report`、`case file`、`execution logs`、`swap/signing/broadcast` 文件。

输出：`dominant_behavior_inference.json`、`chip_control_status.json`、`behavior_reasoning_report.md`。

## 全局硬边界

- 不做交易。
- 不做 paper。
- 不做复盘。
- 不接状态机。
- 不读取私钥。
- 不签名。
- 不广播。
- 不 swap。
- 不做交易建议。
- 不开仓。
- 缺字段必须降级，不能编造。

## 标准流程 / Correct Workflow

群里的标准流程必须严格按这个顺序执行：

```text
用户提出目标
    ↓
总控 Bot 生成任务票
    ↓
钱包事实模块先采集与标准化
    ↓
钱包事实模块输出标准事实文件
    ↓
结构行为模块读取标准事实文件
    ↓
结构行为模块输出主导侧行为推断
    ↓
总控 Bot 汇总结果、检查缺字段、生成下一步建议
```

### 禁止反向流程

禁止出现以下反向或跳层行为：

1. 结构行为模块不能先猜行为。
2. 钱包事实模块不能为了行为结论补字段。
3. 总控 Bot 不能跳过事实层直接问行为层。

### 执行约束

- 没有标准事实文件，结构行为模块必须输出 `INSUFFICIENT_DATA` 或降级，不得高置信推断。
- 标准事实文件字段缺失时，总控 Bot 必须把缺字段列入任务票，回到钱包事实模块补采或标记不可得。
- 钱包事实模块只能补事实来源可验证的字段，不能为了匹配某个行为结论而造字段。
- 总控 Bot 汇总时只能引用两个模块的标准产物，不得自行替代模块判断。

