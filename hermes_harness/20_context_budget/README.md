# 20_context_budget — Context Budget / Compact Semantic Rebuild

## 定位

上下文预算不是历史摘要系统，而是运行时工作内存治理层。

## 主要文件

- `context_budget_policy.md`：上下文装配优先级。
- `compact_rebuild_policy.md`：compact 后语义重建规则。
- `context_budget_state.json`：当前状态。
- `compact_snapshots/`：compact 前后快照。
- `post_compact_context/`：压缩后语义重建材料。
- `context_overflow_reports/`：溢出报告。

## 核心边界

compact 是 semantic reconstruction，不是聊天记录摘要。重建时必须保留目标、状态、证据、错误、验收标准和下一步，而不是保留所有历史噪声。
