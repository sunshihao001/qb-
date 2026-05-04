# SIKK 专业交互系统认知更新

更新时间：2026-05-03T13:00:42Z

## 本轮吸收结论

按 share 方法轮，SIKK 的下一阶段不是新增零散页面或 Telegram 广播，而是建立统一索引驱动的专业交互系统。

## 现状认知

- `sikk_live_run.py` 是 canonical 单入口。
- paper JSON / CSV 同步已存在。
- wallet daily report 使用报告目录中的新 CSV / JSON / MD。
- live_state / live_board / live_dashboard / site 已能由主入口生成。
- `sikk_query.py` 和 `sikkctl.py` 已形成早期只读查询层。
- `sikk_telegram_open.py` 已形成 Telegram view 雏形。
- 缺少真正落盘的 `data/gmgn_candidates_live_run/index/*.json` 统一索引。
- 缺少短码 callback 的 Telegram 专业控制台。
- 缺少 Alert 统一索引。

## 设计认知

统一数据链路应为：

```text
sikk_live_run.py
  -> paper JSON/CSV
  -> live_state/live_board/live_dashboard
  -> site/dashboard_data.json/index.html/app.js/style.css
  -> wallet daily report
  -> sikk_unified_view_builder.py
  -> data/gmgn_candidates_live_run/index/*.json
  -> CLI/Web/Telegram/Report/Alert
```

## 下一阶段执行顺序

1. 新增 `sikk_unified_view_builder.py`。
2. 生成 `index/system_index.json` 等统一索引文件。
3. 让 `sikk_query.py` / `sikkctl.py` 优先读统一索引。
4. 新增 `sikk_telegram_callback_index.py` 和 `sikk_telegram_views.py`。
5. Telegram 用户可见中文，底层 callback 使用短码。
6. Web 增加点击详情层。
7. Alert 只读提醒层从统一索引派生。
8. `sikk_live_run.py` 每轮结束刷新统一索引。

## 安全边界

- 不执行真实 swap。
- 不读取私钥。
- 不签名。
- 不广播。
- 不新增 BUY / SELL / SWAP / EXECUTE / APPROVE / BROADCAST 按钮。
- Alert 只提醒，不交易。
