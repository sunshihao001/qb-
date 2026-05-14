# I02 Context

I02 Directory & Contract Index Unification 是 P10 后的 Integration Program 任务，不是 P11/P12。目标是把 P01-P10、I01 以及 legacy 路径统一登记为 HER/Runner 可读取的索引系统。

## 边界
- 只做目录、合约、schema、handoff、runtime data path、legacy mapping 的索引化。
- 不改业务判断逻辑、不写 Runner、不启动 Paper Runtime、不允许 live execution、不签名、不部署。

## 完成条件
必须生成 18 类核心输出、I03 prerequisite、I02→I03 handoff、acceptance/report，并通过解析、路径、安全边界验证。
