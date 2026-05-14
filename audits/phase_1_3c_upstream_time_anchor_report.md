# 阶段 1.3C 上游时间锚点修复报告

## 1. 本次目标与安全边界
- 目标：只修复上游 GMGN/OKX/钱包结构时间字段写入，降低时间上下文缺锚点问题。
- 不修改交易逻辑、不修改 paper 开平仓、不修改钱包评分、不修改盘型判断。
- 不读取私钥、不签名、不广播、不开启 real swap。

## 2. 修改文件
- `sikk_gmgn_new_token_filter.py`
- `run_sikk_gmgn_pipeline.py`
- `sikk_quote_security_review.py`
- `sikk_candidate_wallet_structure_pipeline.py`
- `sikk_time_context_gate.py`
- `tests/test_sikk_gmgn_new_token_filter.py`
- `tests/test_sikk_quote_security_outputs.py`
- `tests/test_sikk_candidate_wallet_structure_pipeline.py`

## 3. 新增字段
### GMGN 候选发现
- `token_address` / `token_symbol`
- `token_open_time` / `pool_created_at`
- `discovered_at` / `first_seen_at` / `last_seen_at`
- `candidate_snapshot_at` / `candidate_batch_id` / `candidate_source`

### quote/security
- `quote_source` / `quote_requested_at` / `quote_received_at`
- `quote_time` / `quote_time_source`
- `security_scan_started_at` / `security_scan_finished_at`
- `security_scan_time` / `security_scan_created_at` / `security_scan_time_source`

### wallet_structure_decision
- `wallet_snapshot_time` / `wallet_decision_created_at`
- `wallet_delta_time` / `wallet_source_time`
- `wallet_refresh_started_at` / `wallet_refresh_finished_at`

## 4. 新增 registry 文件
- `data/gmgn_candidates_live_run/time_context/token_first_seen_registry.json`
- 当前 registry 条目数：5
- 语义：首次发现写入 `first_seen_at`，后续运行不覆盖；`last_seen_at` 每轮更新。

## 5. 字段样例
### GMGN 候选时间字段样例
```json
{
  "token_address": "Y4vtfnvGSTe2exSm94SXUq3684MGWwWEhXzASkupump",
  "token_symbol": "trollina",
  "token_open_time": "2026-05-04T10:40:59Z",
  "pool_created_at": "2026-05-03T17:45:23Z",
  "discovered_at": "2026-05-04T12:40:24Z",
  "first_seen_at": "2026-05-04T12:38:27Z",
  "last_seen_at": "2026-05-04T12:40:24Z",
  "candidate_snapshot_at": "2026-05-04T12:40:24Z",
  "candidate_batch_id": "RUN_20260504_124024",
  "candidate_source": "gmgn_trenches:completed"
}
```
### OKX/GMGN quote 时间字段样例
```json
{
  "token_address": "ECgweD7xkMj4bm8CcM9rusxKjyQGgdosCvVmhGUupump",
  "quote_source": "GMGN,OKX",
  "quote_requested_at": "2026-05-04T12:40:32Z",
  "quote_received_at": "2026-05-04T12:40:32Z",
  "quote_time": "2026-05-04T12:40:32Z",
  "quote_time_source": "received_at_fallback"
}
```
### wallet decision 时间字段样例
```json
{
  "token_address": "ECgweD7xkMj4bm8CcM9rusxKjyQGgdosCvVmhGUupump",
  "wallet_snapshot_time": "2026-05-04T12:40:27Z",
  "wallet_decision_created_at": "2026-05-04T12:40:27Z",
  "wallet_delta_time": "2026-05-04T12:40:27Z",
  "wallet_source_time": "2026-05-04T12:40:27Z",
  "wallet_refresh_started_at": "2026-05-04T12:40:27Z",
  "wallet_refresh_finished_at": "2026-05-04T12:40:27Z"
}
```

## 6. 字段可用率前后对比
- 开盘时间 `token_open_time`：上一轮 1/196（0.51%）→ 本轮 5/203（2.46%）
- SIKK发现时间 `discovered_at`：上一轮 1/196（0.51%）→ 本轮 5/203（2.46%）
- 首次发现时间 `first_seen_at`：上一轮 0/196（0.00%）→ 本轮 5/203（2.46%）
- 报价时间 `quote_time`：上一轮 0/196（0.00%）→ 本轮 1/203（0.49%）
- 安全扫描时间 `security_scan_time`：上一轮 0/196（0.00%）→ 本轮 1/203（0.49%）
- 钱包决策生成时间 `wallet_decision_created_at`：上一轮 12/196（6.12%）→ 本轮 13/203（6.40%）

## 7. TEMPORAL_UNKNOWN / STAGE_UNKNOWN 对比
- `TEMPORAL_UNKNOWN`：上一轮 184 → 本轮 190
- `STAGE_UNKNOWN`：上一轮 195 → 本轮 198
- 说明：本轮 `--limit 5` 新增 token 后总数为 203；字段可用率已提升，但历史旧 token / paper / dashboard 遗留产物仍占多数，因此 UNKNOWN 绝对数未低于上一轮。本次未通过伪造历史时间来压低 UNKNOWN。

## 8. 安全边界验证
- `notification_enabled`：`False`
- `telegram_broadcast_enabled`：`False`
- `confirmation_enabled`：`False`
- `real_swap_enabled`：`False`
- `broadcast_allowed`：`False`

## 9. 运行验证结果
- `PYTHONPATH=/root/sikk-gmgn python3 sikk_live_run.py --mode once --output-root data/gmgn_candidates_live_run --limit 5 --quote-sources okx,gmgn`：exit 0，产物生成成功。
- `PYTHONPATH=/root/sikk-gmgn python3 sikk_time_context_gate.py --base-dir data/gmgn_candidates_live_run`：exit 0，`token_count=203`。
- `PYTHONPATH=/root/sikk-gmgn python3 -m pytest tests/test_sikk_time_context_gate.py -q`：`4 passed in 0.05s`。
- `PYTHONPATH=/root/sikk-gmgn python3 -m pytest -q`：`248 passed in 13.05s`。

## 10. 验收结论
- 已完成上游字段写入与 registry。
- 已保持 paper-only/no-swap/no-signing/no-broadcast 安全边界。
- 字段可用率验收项全部高于上一轮基线。
- UNKNOWN 绝对数验收项未达成：原因是历史旧 token 与下游遗留产物仍大量混入 time_context 合并宇宙；本轮未用 dashboard/paper/report 时间反向伪造 `token_open_time` 或 `discovered_at`。
- 建议下一步阶段 1.3D：收敛 time_context 的 candidate universe，只以当前候选发现源作为候选基线，历史 paper/report 只作为关联证据，不反向扩展 token universe。
