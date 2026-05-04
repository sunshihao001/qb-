# S09：钱包结构门禁 v1.0 / 同源组 / delta / failure attribution

文档来源: `docs/imported/chatgpt_share_69f809c6_section_index.md`
原始链接: https://chatgpt.com/share/69f809c6-e7ac-83ab-823a-02d6cd8e5426
安全边界: paper-only；不真实 swap；不读取私钥；不签名；不广播；不打印 token/webhook。

## 本节目标
P1/P2：审计 same_source_group、sync scores、counterparty pressure、snapshot delta、failure attribution 是否进入主入口。

## 主题标识
`wallet_structure_gate`

## 需要读取的文件
- `sikk_wallet_structure_gate.py`
- `sikk_wallet_structure_daily_report.py`
- `sikk_wallet_trade_adapter.py`

## 允许新增/更新的输出文件
- `reports/chatgpt_share_69f809c6/S09_wallet_structure_gate_gap_report.md`

## 禁止修改/禁止行为
- 禁止新增真实 BUY / SELL / SWAP / EXECUTE / APPROVE / BROADCAST。
- 禁止新增并行主入口替代 `sikk_live_run.py`。
- 禁止把 AI 自然语言判断直接写成事实字段。
- 禁止删除已有 runtime、paper runner、dashboard、Telegram、wallet/cluster 模块。
- 缺字段必须写 `待补` / `MISSING` / `DATA_QUALITY_FAIL`，不得编造。

## 新增字段/检查字段
- `source_trace`
- `missing_reason`
- `evidence_level`
- `data_quality_status`
- `paper_only_safety_boundary`
- `runtime_manifest_safety`

## 验收命令
```bash
cd /root/sikk-gmgn
PYTHONPATH=/root/sikk-gmgn python3 -m pytest -q
PYTHONPATH=/root/sikk-gmgn python3 sikk_live_run.py --mode once --output-root data/gmgn_candidates_live_run --limit 5 --quote-sources none
```

## 完成标准
- 有真实输出文件，不只写方案。
- 有测试或命令验收输出。
- `live_run_manifest.json` 保持 `real_swap_enabled=false` / `broadcast_allowed=false`。
- Telegram/Web/CLI 文案中文化，技术文件名和 CLI flag 可保留英文。
- 如发现失败项，写入 `reports/chatgpt_share_69f809c6/FAILED_ITEMS.md`。

## 当前处理状态
- 状态: 待逐节执行。
- 备注: 本文件是 Section Task 合同；后续按优先级逐节 TDD/审计/验收。
