# I01 Full Phase Consistency Audit Context Pack

I01 是 Integration Program 的第一步，不是 P11。它不新增业务判断层，而是审计 P01-P10 是否能形成一条可运行、可验收、可回放、可升级的工程链。

## 必须回答
- P01-P10 输入输出是否一致？
- handoff 是否连续？
- 字段/状态码/gap/禁止事项是否跨阶段继承？
- 是否存在阶段越权或下游无法读取的输出？

## 禁止
- 不允许直接写 Runner。
- 不允许触发 Paper Runtime。
- 不允许改生产规则。
- 不允许新增 P11/P12/P13。

## 完成标准
必须生成 I01 的 8 个核心审计输出与 `i01_to_i02_handoff_packet.yaml`，并给出 `I01_READY / I01_READY_WITH_GAPS / I01_BLOCKED` 判断。
