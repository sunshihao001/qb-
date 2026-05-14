# SIKK Stable Trader OS｜Data Plane v2.0

来源链：DOC-20260511-003 方法论总纲 → DOC-20260511-004 治理平面 → DOC-20260511-005 领域平面 → P0 修复任务。

## 1. Data Plane 定位
Data Plane 是 K00 之后、P00/P01 之前的系统事实层。它不负责预测、不负责交易、不负责下单；它负责定义系统可消费事实、字段来源、事实状态、降级规则、handoff 路径和验证边界。

## 2. 上位约束
- Governance Plane：所有数据读取必须遵守 paper-only / read-only / no-secret / no-signing / no-broadcast / no-swap。
- Domain Plane：所有字段、实体、状态必须可回溯到领域对象、字段字典、状态字典。
- Methodology Blueprint：数据事实先于结构判断、场景识别、策略门控和执行风险。

## 3. 数据事实分层
- raw_input：原始输入，只保存，不推断。
- normalized_fact：字段标准化后的事实，可进入 P01。
- evidence_bundle：支持判断的证据集合，可进入 P02-P06。
- inference_result：推断结果，不得伪装成事实。
- handoff_packet：阶段交接包，必须含 status、source、gap、acceptance。
- audit_report：验收与回放记录。

## 4. 事实状态
- PRESENT：字段存在且来源清晰。
- MISSING_OPTIONAL：可降级缺失。
- MISSING_REQUIRED：阻塞缺失。
- STALE：过期事实，需降级或重取。
- CONFLICTED：来源冲突，禁止直接进入正向判断。
- DERIVED：派生字段，必须保留源字段。

## 5. P01 消费规则
P01 只能消费 normalized_fact_model.schema.json 合法的事实包。缺失值必须显式标注，不能由 AI 补猜。P01 输出只能是事实质量、兼容性、缺口和下游 handoff，不得输出买卖建议。

## 6. 安全边界
- paper_only: true
- read_only_research: true
- real_trade_enabled: false
- signing_enabled: false
- broadcast_enabled: false
- auto_swap_enabled: false
- secret_access: not_requested_not_used

## 7. 下游 handoff
Data Plane 完成后交给 P00 system_context_control，再由 P00 决定是否允许 P01 data_fact_runtime_connection。当前裁决：自动化 workflow 的 P01 必须等待 Data Plane + Control Registry + P00/P01 controller stub 验证完成。
