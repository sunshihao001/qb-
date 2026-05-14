# Governance Plane 治理平面 v2.0

文件编号：GOVERNANCE-PLANE-002  
状态：GOVERNANCE_PLANE_V2_INSTITUTIONAL_LANDED  
来源：DOC-20260511-021  
更新时间：2026-05-11T16:08:03Z

## 定位
Governance Plane 不是规则说明，而是 SIKK Stable Trader OS 的权限、安全边界、硬否定、阶段裁决、证据语言、假设控制、复盘升级约束平面。

## 不负责
- 不分析 token。
- 不判断钱包角色。
- 不生成交易信号。
- 不运行 paper trade。
- 不启动 P01-P10。

## 负责
- 约束 K00-P10 的 can / cannot。
- 阻断真实交易、越权阶段跃迁、P01 绕过 Data Plane、paper runner 绕过 P06/P07。
- 限制确定性语言与未证实主导侧意图。
- 禁止缺失字段靠推断补齐。
- 向 Domain / Data / Control 输出治理约束。

## 当前裁决
- paper_only: true
- real_trade_enabled: false
- auto_order_allowed: false
- p01_runtime_connection_allowed: false
- P01 当前不得运行。
- 下一合法阶段仍属于 SYSTEM_PLANES_PROFESSIONAL_GENERATION_AND_ACCEPTANCE。
