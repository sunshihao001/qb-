# P05 Evidence Controller Context

P05 是证据对象系统，不是证据摘要脚本、打分模块、场景识别器或策略解释器。

## HER 执行前必须读取
- `p05_evidence_controller.yaml`
- `p05_input_contract.yaml`
- `evidence_object_schema.yaml`
- `evidence_hard_negative_rules.yaml`
- `p05_to_p06_handoff_contract.yaml`

## 核心边界
- P04 输出的是筹码结构状态；P05 将其转成证据对象。
- 每条证据必须绑定 hypothesis frame、source trace、field trace。
- 支持证据必须检查反证；冲突/UNKNOWN 必须显式登记。
- P05 只能交接给 P06，不得进入 P07、paper runtime、live execution。

创建时间：2026-05-12T02:44:17Z
