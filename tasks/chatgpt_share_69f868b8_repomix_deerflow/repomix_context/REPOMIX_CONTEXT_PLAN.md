# Repomix Context Plan｜SIKK

- 目标: 为 Hermes/DeerFlow-style 多角色执行提供分阶段代码上下文。
- 边界: paper-only；不读取私钥；不签名；不广播；不执行真实交易。

## Contexts
- `full`: 全仓库压缩上下文，用于系统架构审计。 → `ai_context/full/sikk_full_architecture.xml`
- `index`: 统一索引、查询、dashboard 与 paper review 上下文。 → `ai_context/index/sikk_index_context.xml`
- `wallet`: GMGN 钱包结构、同源候选、结构融合上下文。 → `ai_context/wallet/sikk_wallet_context.xml`
- `cluster`: OKX Top300 cluster 与筹码控制上下文。 → `ai_context/cluster/sikk_cluster_context.xml`
- `case`: Case File、证据链、完整性审计上下文。 → `ai_context/case/sikk_case_context.xml`
- `telegram`: Telegram 中文控制台、按钮与回调上下文。 → `ai_context/telegram/sikk_telegram_context.xml`
- `web`: 静态 dashboard 与移动端详情页上下文。 → `ai_context/web/sikk_web_context.xml`
- `runtime`: canonical runtime 与 paper runner 上下文。 → `ai_context/runtime/sikk_runtime_context.xml`
- `audit`: 系统审计、解释、研究循环上下文。 → `ai_context/audit/sikk_audit_context.xml`

## 使用
```bash
bash /root/sikk-gmgn/tasks/chatgpt_share_69f868b8_repomix_deerflow/repomix_context/make_sikk_context.sh full
bash /root/sikk-gmgn/tasks/chatgpt_share_69f868b8_repomix_deerflow/repomix_context/make_sikk_context.sh runtime
```

