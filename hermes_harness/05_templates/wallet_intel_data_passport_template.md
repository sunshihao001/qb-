---
artifact_type: template
status: candidate_verified_by_system_write
version: v2.0
generated_at: 2026-05-07T05:40:28Z
---
# Wallet-Intel 数据护照模板 V2.0

## 1. Token 基本信息
- token_address：
- token_symbol：
- chain：solana
- analysis_id：
- batch_id：
- generated_at：

## 2. 标准入口
- standard_entry：
- token_index_ref：
- field_dictionary_ref：
- legacy_path_map_ref：
- source_manifest_ref：

## 3. 数据层可用性
- ingest：存在 / 缺失 / 待补
- facts：存在 / 缺失 / 待补
- evidence：存在 / 缺失 / 待补
- inference：存在 / 缺失 / 待补
- conclusion：存在 / 缺失 / 待补
- handoff：存在 / 缺失 / 待补
- reports：存在 / 缺失 / 待补
- index：存在 / 缺失 / 待补

## 4. 事实层摘要
只记录可验证事件，不写角色判断。

- 钱包基础事实：文件 / 字段 / raw_unit_refs
- 交易事实：文件 / 字段 / raw_unit_refs
- 持仓事实：文件 / 字段 / raw_unit_refs
- 资金事实：文件 / 字段 / raw_unit_refs / 资金待查状态
- Top Holder 事实：文件 / 字段 / raw_unit_refs
- Token 转入 / 转出事实：文件 / 字段 / raw_unit_refs

## 5. 证据层摘要
证据不等于结论。

- 同源候选证据：
- 资金路径证据：
- Token transfer 证据：
- GMGN 标签证据：
- K线阶段证据：
- 旧路径来源证据：

## 6. 推断层摘要
每条推断必须有证据等级。

- 同源推断：证据等级 / 引用事实 / 反向证据
- 执行组推断：证据等级 / 引用事实 / 反向证据
- 控筹推断：证据等级 / 引用事实 / 反向证据
- 派发推断：证据等级 / 引用事实 / 反向证据
- 二次拉升动机推断：证据等级 / 引用事实 / 反向证据

## 7. 结论层摘要
每条结论必须有反证条件与失效条件。

- 当前结论：
- 证据等级：
- 引用事实：
- 引用证据：
- 引用推断：
- 反证条件：
- 失效条件：
- 复查窗口：
- 动作边界：仅 paper / observe / review；不触发真实交易

## 8. Handoff 摘要
- handoff_packet_ref：
- 下游模块：
- 下游读取文件：
- 字段层级说明：
- 缺失项：
- 禁止解释为交易指令：是

## 9. 旧路径追溯
- old_path：
- new_path：
- mapping_ref：
- checksum_ref：
- copy_mode：copy-only / index-only / read-fallback
- source_status：只读参考 / 已导入副本 / 待补

## 10. 缺失项
- 缺失字段：
- 缺失文件：
- 缺失证据：
- 缺失资金路径：
- 缺失 transfer source：
- 缺失 Top Holder：
- 缺失旧路径映射：
- 影响：
- 下一步补查：
