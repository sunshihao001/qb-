---
artifact_type: template
status: candidate_verified_by_system_write
version: v2.0
generated_at: 2026-05-07T05:42:24Z
---
# Wallet-Intel 旧路径映射模板 V2.0

## 1. 映射文件定位
本模板用于记录 Wallet-Intel 旧目录与新标准语义层之间的可追溯关系。

本模板不授权复制、移动、删除或覆盖任何旧文件。

## 2. 映射总信息
- map_id：
- generated_at：
- task_id：
- import_id：
- token_address：
- token_symbol：
- mapping_mode：index-only / copy-only / read-fallback
- old_root_status：read-only
- new_standard_entry：
- generated_by：Hermes Wallet-Intel Harness V2.0

## 3. 映射记录格式
每条映射必须包含：

```json
{
  "token_address": "",
  "semantic_layer": "ingest|facts|evidence|inference|conclusion|handoff|reports|index",
  "old_path": "",
  "old_file_type": "",
  "new_path": "",
  "new_artifact_type": "",
  "mapping_mode": "index-only|copy-only|read-fallback",
  "source_status": "read-only|copied|missing|needs_review",
  "checksum_sha256": "",
  "size_bytes": null,
  "raw_unit_refs": [],
  "field_dictionary_ref": "",
  "data_passport_ref": "",
  "missing_status": "none|missing_file|missing_field|missing_evidence|needs_review",
  "notes": ""
}
```

## 4. 语义层判定规则
旧目录名不能直接决定新层级，必须按内容语义判断：

- 原始采集、API 响应、CSV 导入 → `ingest`
- 钱包买卖、持仓、资金、Top Holder → `facts`
- 同源候选、资金路径、Token transfer、GMGN 标签、K线阶段 → `evidence`
- 角色分类、结构组、控筹、派发、二拉动机 → `inference`
- SUPPORT / PAUSE / BLOCK、paper gate、当前处理判断 → `conclusion`
- bot2/case/telegram/review 下游包 → `handoff`
- 人类报告、case 报告、dashboard 摘要 → `reports`
- token_index、wallet_index、route_index、path_map → `index`

## 5. 禁止事项

```text
不得把旧路径名等同于语义层。
不得用旧目录存在替代理解验证。
不得移动旧文件。
不得删除旧文件。
不得覆盖旧文件。
不得缺少 old_path -> new_path。
不得缺少 source_status。
```
