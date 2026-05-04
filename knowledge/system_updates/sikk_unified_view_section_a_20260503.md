# SIKK 统一索引层 Section A 认知更新

更新时间：2026-05-03T13:00Z

## 已完成

Section A 已实现：新增 `sikk_unified_view_builder.py`，把主入口已生成的 paper/live/site/report 输出收敛到 `data/gmgn_candidates_live_run/index/*.json`。

## 已生成索引

```text
system_index.json
token_detail_index.json
position_index.json
latest_open_positions.json
latest_closed_positions.json
case_file_index.json
auto_review_index.json
alert_index.json
telegram_callback_index.json
```

## 当前真实样本

```text
token_count=156
open_position_count=5
closed_position_count=178
opportunity_count=26
open_json_count=5
closed_json_count=178
open_csv_count=5
closed_csv_count=178
alert_count=6
telegram_callback_count=250
```

## 安全边界

```text
real_swap_enabled=False
broadcast_allowed=False
private_key_required=False
confirmation_enabled=False
telegram_broadcast_enabled=False
```

统一索引只读；不采集、不报价、不交易、不签名、不广播。

## 下一节

Section B：让 `sikk_query.py` / `sikkctl.py` 优先读取 `data/gmgn_candidates_live_run/index/*.json`，保留当前 dashboard fallback。
