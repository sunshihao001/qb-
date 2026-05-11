---
artifact_type: data_contracts_rule
status: verified
version: v2.0-stage4
generated_at: 2026-05-07T08:39:07Z
task_type: wallet_intel_semantic_integration
---
# Wallet-Intel 数据契约集合 V2.0 — 阶段 4

## 目标
让 Hermes 明确每类 Wallet-Intel 文件的用途、输入、输出和风险边界。

## 统一契约字段
每个契约必须包含：

```text
数据名称
数据层级
主要用途
输入来源
输出用途
核心字段
是否事实数据
是否推断数据
可被谁读取
不可被谁直接使用
失效条件
验证方式
```

## 1. 钱包原始数据契约
- 数据名称：钱包原始数据
- 数据层级：raw
- 主要用途：保留最初采集事实
- 输入来源：链上事件、GMGN/CSV/API/日志
- 输出用途：标准化层、事实层、审计回溯
- 核心字段：wallet_address、tx_hash、block_time、side、amount、token、price、source_path
- 是否事实数据：是
- 是否推断数据：否
- 可被谁读取：事实层、标准化模块、验证模块
- 不可被谁直接使用：策略门禁、交易动作模块
- 失效条件：来源缺失、时间戳错位、重复采集未去重
- 验证方式：raw_ref 可回读、hash/行数/时间范围核对

## 2. 钱包标准化数据契约
- 数据名称：钱包标准化数据
- 数据层级：normalized
- 主要用途：统一字段、单位和格式
- 输入来源：钱包原始数据
- 输出用途：画像、交易、证据、索引
- 核心字段：wallet_address、token_address、tx_time、side_norm、amount_norm、holding_norm、source_ref
- 是否事实数据：是
- 是否推断数据：否
- 可被谁读取：画像模块、证据模块、报告模块
- 不可被谁直接使用：买入/卖出指令模块
- 失效条件：字段映射缺失、单位转换错误、关键字段空值
- 验证方式：与原始数据双向抽查

## 3. 钱包画像数据契约
- 数据名称：钱包画像数据
- 数据层级：profile
- 主要用途：描述钱包持仓、行为特征、阶段属性
- 输入来源：标准化数据、事实层聚合
- 输出用途：画像报告、结构判断、阅读入口
- 核心字段：wallet_address、holding_ratio、avg_entry、profit_state、activity_window、top_holder_flag
- 是否事实数据：部分
- 是否推断数据：部分
- 可被谁读取：画像模块、结构分析模块、报告模块
- 不可被谁直接使用：交易执行模块
- 失效条件：窗口过短、样本不足、字段未对齐
- 验证方式：画像字段可追溯到事实/统计来源

## 4. 钱包交易数据契约
- 数据名称：钱包交易数据
- 数据层级：transaction
- 主要用途：记录买卖与转账事件
- 输入来源：标准化数据、原始交易记录
- 输出用途：行为分析、事实引用
- 核心字段：tx_hash、wallet_address、token_address、side、amount、price、tx_time、balance_delta
- 是否事实数据：是
- 是否推断数据：否
- 可被谁读取：事实层、行为层、报告模块
- 不可被谁直接使用：策略动作模块
- 失效条件：hash 重复、方向缺失、数量异常
- 验证方式：链上回查、时间顺序核对

## 5. 同源证据数据契约
- 数据名称：同源证据数据
- 数据层级：evidence
- 主要用途：支持同源/同步/路径一致性判断
- 输入来源：交易数据、资金路径、筹码分布
- 输出用途：结构证据层、候选组判断
- 核心字段：evidence_id、fact_refs、evidence_level、same_source_group_id、support_reason
- 是否事实数据：否
- 是否推断数据：部分
- 可被谁读取：证据层、推断层、审计模块
- 不可被谁直接使用：直接买入依据模块
- 失效条件：缺 fact_refs、证据等级为空、证据链断裂
- 验证方式：fact_id 追溯与 evidence_level 校验

## 6. 候选钱包组数据契约
- 数据名称：候选钱包组数据
- 数据层级：group
- 主要用途：记录可能同组的钱包集合
- 输入来源：同源证据、交易聚类、路径相似度
- 输出用途：结构分析、后续核验
- 核心字段：group_id、wallet_list、group_score、group_reason、evidence_refs
- 是否事实数据：否
- 是否推断数据：是
- 可被谁读取：结构分析、证据复核、报告模块
- 不可被谁直接使用：交易执行模块
- 失效条件：样本过少、证据不一致、组内冲突
- 验证方式：抽样复核 wallet_list 与 evidence_refs

## 7. 资金路径数据契约
- 数据名称：资金路径数据
- 数据层级：path
- 主要用途：描述资金来源、流转和回流路径
- 输入来源：转账记录、交易记录、源钱包证据
- 输出用途：结构证据、风险判断、回溯
- 核心字段：path_id、from_wallet、to_wallet、hop_count、funding_source、return_path
- 是否事实数据：部分
- 是否推断数据：部分
- 可被谁读取：证据层、风险分析、报告模块
- 不可被谁直接使用：交易动作模块
- 失效条件：路径中断、节点缺失、方向无法确认
- 验证方式：逐跳回查、链路一致性检查

## 8. 筹码分布数据契约
- 数据名称：筹码分布数据
- 数据层级：distribution
- 主要用途：反映持仓集中度和分布变化
- 输入来源：持仓数据、地址聚合、时间窗口统计
- 输出用途：结构判断、风险提示
- 核心字段：top_holder_pct、top10_pct、holding_concentration、distribution_window
- 是否事实数据：部分
- 是否推断数据：部分
- 可被谁读取：结构分析、风险分析、报告模块
- 不可被谁直接使用：直接买入依据模块
- 失效条件：时间窗口不一致、统计口径混乱
- 验证方式：窗口重算、Top Holder 对照

## 9. 主导侧行为推断契约
- 数据名称：主导侧行为推断
- 数据层级：inference
- 主要用途：解释主导侧生命周期、控筹/派发/扩张迹象
- 输入来源：事实层、证据层、筹码分布、资金路径
- 输出用途：行为层、交接层、风险门禁
- 核心字段：dominant_side_status、uncertainty、supporting_evidence_ids、inference_reason
- 是否事实数据：否
- 是否推断数据：是
- 可被谁读取：推断层、策略交接层、报告模块
- 不可被谁直接使用：交易执行模块
- 失效条件：证据不足、窗口过短、假设冲突
- 验证方式：证据回链与不确定性检查

## 10. 钱包结构裁决契约
- 数据名称：钱包结构裁决
- 数据层级：decision
- 主要用途：给策略门禁提供结构判断输入
- 输入来源：推断层、证据层、画像层
- 输出用途：WALLET_SUPPORT / WALLET_PAUSE / WALLET_BLOCK
- 核心字段：wallet_structure_decision、decision_reason、evidence_refs、uncertainty
- 是否事实数据：否
- 是否推断数据：是
- 可被谁读取：策略门禁、paper runner、dashboard
- 不可被谁直接使用：直接买入信号模块
- 失效条件：证据链断裂、推断未标注不确定性
- 验证方式：decision 可追溯到 evidence/inference

## 11. handoff 交接包契约
- 数据名称：handoff 交接包
- 数据层级：handoff
- 主要用途：给后续模块传递可读输入
- 输入来源：结构裁决、推断层、字段字典
- 输出用途：状态机、paper runner、后续分析模块
- 核心字段：handoff_id、target_module、summary、decision_ref、read_scope
- 是否事实数据：否
- 是否推断数据：部分
- 可被谁读取：指定下游模块
- 不可被谁直接使用：交易执行信号
- 失效条件：target_module 缺失、decision_ref 缺失
- 验证方式：handoff 可读性与引用完整性检查

## 12. 人类可读报告契约
- 数据名称：人类可读报告
- 数据层级：report
- 主要用途：给人类审阅、复核、归档
- 输入来源：事实层、证据层、推断层、handoff
- 输出用途：审计、复核、交付
- 核心字段：report_id、token_address、summary、facts、evidence、inference、handoff_notes
- 是否事实数据：混合
- 是否推断数据：混合
- 可被谁读取：人类审阅者、审计、归档模块
- 不可被谁直接使用：自动交易动作模块
- 失效条件：未标注层级、缺少引用、与事实不一致
- 验证方式：抽样复核与引用追溯
