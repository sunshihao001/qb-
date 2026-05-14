# A00 Context Pack

## 定位
A00 是 HER Document-to-Function Automated Fulfillment System 的总验收证据控制器。它不重新实现 K00/F00/V00/R00 的业务功能，只读取正式 handoff、phase state、gap、trace、audit、artifact manifest 与 evidence，做证据裁决。

## 上游读取
- K00：资料摄取、registry、passport、corpus index、system mapping、KV、gap、handoff。
- F00：concept_to_function、field_model、rule_logic、asset_plan、schema/contract plan、patch/runner/test/replay plan、handoff。
- V00：schema/contract/function/field/rule/test/replay validation evidence、failure evidence、handoff。
- R00：binding target inventory、command contract、binding specs、dry-run evidence、generated output manifest、handoff；仅在涉及 runner/tool binding 时为强制。

## 核心原则
- 证据优先：不能用总结代替 evidence。
- 状态降级：状态与证据不一致时，A00 必须降级而不是美化。
- gap 传播：未解决 gap 必须进入 final report、readiness certificate、downstream handoff。
- 边界安全：禁止 live runtime、wallet signing、auto deploy、production trading。

## 输出去向
A00 输出 readiness certificate 与 A00 downstream handoff，交给 H00/U00/G00。若阻断，则输出 recovery_report，禁止进入最终 H00 ready handoff。
