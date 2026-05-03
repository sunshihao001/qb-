# v0.3 WP2 审计报告：市值上下文全链路贯穿

## 1. 工作包目标

建立统一 `market_cap_context` 合约，让发现、信号、钱包判断、paper 入场、当前、退出市值可以进入同一条复盘链路。

## 2. 修改文件

- 新增：`sikk_market_cap_context.py`
- 新增：`tests/test_sikk_market_cap_context.py`
- 修改：`sikk_live_run.py`
- 修改：`tests/test_sikk_live_run.py`

## 3. 标准字段

```text
discovery_market_cap_usd
signal_market_cap_usd
wallet_decision_market_cap_usd
paper_entry_market_cap_usd
current_market_cap_usd
exit_market_cap_usd
market_cap_change_from_discovery_pct
market_cap_change_from_signal_pct
market_cap_change_from_wallet_decision_pct
market_cap_context_quality
market_cap_missing_fields
```

## 4. 数据质量规则

- `OK`：6 个市值字段全部存在。
- `DEGRADED`：至少 3 个存在，但仍有缺字段。
- `PARTIAL`：仅 1-2 个存在。
- `MISSING`：全部缺失。

缺字段只进入 `market_cap_missing_fields`，不编造、不默认填 0。

## 5. 接入方式

`build_enriched_runtime_statuses()` 在合并状态机、quote/security、paper、failure attribution 后，调用：

```python
market_context = build_market_cap_context(...)
merge_market_cap_context(status, market_context)
```

因此 `live_state.json` / token_status / dashboard 可以直接读取：

```text
status["market_cap_context"]
status["market_cap_change_from_discovery_pct"]
```

## 6. 测试结果

指定测试：

```bash
PYTHONPATH=/root/sikk-gmgn pytest -q tests/test_sikk_market_cap_context.py tests/test_sikk_live_run.py
```

结果：

```text
8 passed in 0.05s
```

全量测试：

```bash
PYTHONPATH=/root/sikk-gmgn pytest -q
```

结果：

```text
133 passed in 10.41s
```

## 7. 审计结论

WP2 已完成。v0.3 当前具备独立市值上下文合约，并已接入 live runtime。下一步进入 WP3：主导侧/对手盘生命周期闭环增强。
