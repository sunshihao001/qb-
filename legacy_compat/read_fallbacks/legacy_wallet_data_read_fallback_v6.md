# Legacy Wallet Data Read Fallback V6

## 核心策略

- 旧目录先保留。
- 旧数据可以 copy-only，但本步骤不复制。
- 旧路径保留映射。
- 新任务优先读 token 索引和新语义体系。
- 旧目录只作为只读参考。
- 代码读取路径后续再逐步改。

## 读取顺序

1. `research_loop/state/wallet_data_token_index_v3/token_data_lookup_v3.json`
2. `research_loop/state/wallet_data_token_index_v3/tokens/<token>.json`
3. `legacy_compat/path_maps/legacy_to_new_semantic_mapping_v6.json`
4. 如果新体系缺失，再 fallback 旧路径；fallback 必须记录 reason。

## 禁止

- 不直接删除旧目录。
- 不直接移动旧目录。
- 不批量改所有代码路径。
- 不继续把 legacy runtime 目录作为新任务主写路径。

## 兼容决策字段

- `old_path`：旧文件路径。
- `new_semantic_owner`：新语义归属。
- `new_standard_read_position`：未来标准读取位置。
- `compat_read_still_needed`：是否仍需兼容读取。
- `legacy_write_forbidden`：是否禁止继续写入旧路径。
