# 旧目录 → 标准钱包数据体系 可执行迁移清单 V1

## 目标

在不破坏旧目录、不中断现有 runtime 的前提下，把旧钱包数据逐步收敛到标准体系：

```text
standard_wallet_data/
├─ ingest/
├─ facts/
├─ evidence/
├─ inference/
├─ handoff/
├─ reports/
└─ index/
```

## 总迁移原则

1. 只做 copy-only，不做 mv。
2. 先建标准目录与索引，再复制旧数据。
3. 复制前写 manifest，复制后写 checksum。
4. 每一类数据先做映射确认，再做小批量试迁移。
5. 旧目录保留，直到新体系稳定运行。
6. 不允许原始层被推断层覆盖。

## 迁移阶段

### Phase 0：准备
- [ ] 建立 `standard_wallet_data/` 根目录
- [ ] 建立七层子目录
- [ ] 建立 `index/` 路由文件模板
- [ ] 建立迁移 manifest 模板
- [ ] 建立 checksum 记录模板

### Phase 1：采集层迁移
- [ ] 从 `data/gmgn_candidates_live_run/intel-bot/logs/wallet_structure/<token>/snapshots/` 复制原始快照到 `ingest/raw/`
- [ ] 从 `modules/source_wallet_bot/` 产物中提取原始输入包到 `ingest/source_packets/`
- [ ] 将采集清单写入 `ingest/manifests/`
- [ ] 对 `snapshot_*.json`、`delta_*.json`、`latest_delta.json` 进行归档

### Phase 2：事实层迁移
- [ ] 将 `wallet_entity_profile_normalized.json` 复制到 `facts/wallet_entity/`
- [ ] 将 `wallet_trade_normalized.json` 复制到 `facts/wallet_trade/`
- [ ] 将 `wallet_status.json` / `token_status.json` 复制到 `facts/wallet_state/`
- [ ] 将 token 级事实统一补成 `token_facts/`

### Phase 3：证据层迁移
- [ ] 将 `same_source_evidence_normalized.json` 复制到 `evidence/same_source/`
- [ ] 将资金路径相关产物复制到 `evidence/funding_path/`
- [ ] 将 token transfer 相关产物复制到 `evidence/token_transfer/`
- [ ] 将对手盘相关产物复制到 `evidence/counterparty_evidence/`

### Phase 4：推断层迁移
- [ ] 将 `wallet_structure_decision.json` 复制到 `inference/wallet_structure/`
- [ ] 将角色分类产物复制到 `inference/role_classification/`
- [ ] 将行为推断产物复制到 `inference/behavior_inference/`
- [ ] 将 `candidate_states.json` 复制到 `inference/lifecycle/`
- [ ] 将筹码控制权状态复制到 `inference/chip_control/`

### Phase 5：handoff 迁移
- [ ] 将 `bot2_handoff_packet.json` 复制到 `handoff/bot2/`
- [ ] 将 case 交接包复制到 `handoff/case_packet/`
- [ ] 将 Telegram 交接包复制到 `handoff/telegram_packet/`
- [ ] 将复核交接包复制到 `handoff/review_packet/`

### Phase 6：报告迁移
- [ ] 将 summary 报告复制到 `reports/summary/`
- [ ] 将 case 报告复制到 `reports/case/`
- [ ] 将日报复制到 `reports/daily/`
- [ ] 将审计报告复制到 `reports/audit/`
- [ ] 将 dashboard 输出复制到 `reports/dashboard/`

### Phase 7：索引迁移
- [ ] 生成 `system_index.json`
- [ ] 生成 `token_index.json`
- [ ] 生成 `wallet_index.json`
- [ ] 生成 `handoff_index.json`
- [ ] 生成 `report_index.json`
- [ ] 生成 `search_index.json`
- [ ] 生成 `route_index.json`

## 迁移优先级

### 优先级 A：必须先做
1. `ingest/manifests/`
2. `ingest/raw/`
3. `facts/wallet_entity/`
4. `facts/wallet_trade/`
5. `inference/wallet_structure/`
6. `handoff/bot2/`
7. `reports/case/`
8. `index/system_index.json`

### 优先级 B：第二批
1. `facts/wallet_state/`
2. `evidence/same_source/`
3. `evidence/token_transfer/`
4. `inference/lifecycle/`
5. `reports/daily/`
6. `reports/audit/`

### 优先级 C：后续补齐
1. `evidence/funding_path/`
2. `evidence/counterparty_evidence/`
3. `inference/behavior_inference/`
4. `inference/chip_control/`
5. `handoff/telegram_packet/`
6. `handoff/review_packet/`
7. `reports/dashboard/`

## 迁移分组建议

### A. token 级目录组
适合按 token 批量迁移：
- `data/gmgn_candidates_live_run/intel-bot/logs/wallet_structure/<token>/...`
- `data/gmgn_candidates_live_run/wallet_structure/<token>/structure_analysis/...`

### B. 模块级目录组
适合按模块整体复制：
- `modules/source_wallet_bot/`
- `modules/wallet_structure/`

### C. runtime 输出组
适合按运行输出批量收拢：
- `data/gmgn_candidates_live_run/paper_live/`
- `data/gmgn_candidates_live_run/reports/`
- `data/gmgn_candidates_live_run/site/`
- `data/gmgn_candidates_live_run/index/`

## 推荐执行顺序

```text
1. 建标准目录
2. 建 manifest / checksum 模板
3. 迁移一个 token 样本
4. 验证文件命名与路由
5. 再批量迁移其余 token
6. 最后迁移 reports / index / handoff
```

## 迁移前必须做的检查

- [ ] 旧目录是否仍被当前 runtime 读取
- [ ] 目标目录是否会与旧路径冲突
- [ ] 复制后是否能被索引层发现
- [ ] 复制后是否能被报告层引用
- [ ] 复制后是否能被人工复核
- [ ] 复制后是否保留原始 hash

## 迁移后验收标准

- [ ] 旧目录仍可正常读取
- [ ] 新目录能被统一索引层读到
- [ ] facts / evidence / inference / handoff / reports 层职责分离
- [ ] 同一个 token 的数据可通过 `analysis_id` 串联
- [ ] 不存在原始层被推断层覆盖
- [ ] 不存在单文件同时承担采集 + 事实 + 推断 + 报告职责

## 一句话执行原则

```text
先建新体系，再 copy-only；先小样本验证，再批量收敛；先保留旧路径，再决定是否长期切换。
```
