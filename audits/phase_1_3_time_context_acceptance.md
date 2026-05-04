# SIKK-GMGN 阶段 1.3 验收文档：全系统时间上下文协同门禁

- 文档版本：v1.3-acceptance
- 生成时间：2026-05-04
- 项目路径：`/root/sikk-gmgn`
- 主入口：`sikk_live_run.py`
- 核心模块：`sikk_time_context_gate.py`
- 验收范围：时间上下文门禁、输入字段来源收敛、TEMPORAL_UNKNOWN 根因定位、runtime 安全边界确认

## 1. 阶段目标

阶段 1.3 的目标不是扩大交易执行能力，而是补齐 SIKK-GMGN 在纸面验证链路中的“时间坐标治理层”。

本阶段重点回答四个问题：

- 每个 token 的关键阶段时间是否完整？
- 不同模块输出之间是否存在时间脱节？
- 缺失时间证据时，系统是否会保守降级，而不是误放行？
- runtime 是否仍保持 paper-only，不触发真实交易、签名或广播？

## 2. 核心安全边界

阶段 1.3 保持原有安全边界：

- `confirmation_enabled=false`
- `real_swap_enabled=false`
- `telegram_broadcast_enabled=false`
- `broadcast_allowed=false`
- 不读取私钥
- 不签名
- 不广播
- 不真实 swap
- 不新增真实交易按钮

runtime manifest 已确认：

- 通知开关：false
- Telegram 广播：false
- Telegram 目标：空
- 人工确认执行：false
- 真实 swap：false
- 广播许可：false
- dashboard：true
- trace：true

## 3. 新增/确认的核心产物

### 3.1 核心代码

- `sikk_time_context_gate.py`
  - 统一读取候选、信号、钱包结构、quote/security、paper、dashboard 等来源的时间字段。
  - 计算阶段 age、TTL、stale、temporal sync、temporal gate、time_context_score。
  - 输出全系统时间门禁结果。

### 3.2 专项测试

- `tests/test_sikk_time_context_gate.py`
  - 覆盖 D0/D4/quote stale/S3-S4 等关键时间规则。

### 3.3 Schema 文档

- `docs/sikk_time_context_schema.md`
  - 定义时间上下文字段、阶段 TTL、stale 语义、输入字段来源、审计输出。

### 3.4 Runtime 输出

输出目录：`data/gmgn_candidates_live_run/time_context/`

关键文件：

- `time_context_summary.json`
- `time_context_summary.csv`
- `time_context_report.md`
- `time_context_input_audit.json`
- `time_context_input_audit.md`
- `time_context_runtime_log.json`

## 4. 本轮运行结果

### 4.1 处理规模

- token 去重前数量：1566
- token 去重后数量：196
- 重复 token 数量：1370
- 当前 fallback token 来源：`gmgn_new_token_filter/token_candidates.json`

### 4.2 candidate_stage 分布

- `STAGE_UNKNOWN`：195
- `D4_OLD_TOKEN`：1

解释：当前大多数 token 来自 dashboard/paper/report 等下游产物或混合来源，缺少标准候选发现阶段的完整时间锚点，因此阶段判断保守落在 `STAGE_UNKNOWN`。

### 4.3 discovery_quality 分布

- `DISCOVERY_UNKNOWN`：195
- `NORMAL_DISCOVERY`：1

解释：只有少量 token 拥有可用于标准发现质量判断的发现时间字段；多数 token 只具备后续运行痕迹，不具备完整 discovery anchor。

### 4.4 temporal_gate 分布

- `TEMPORAL_UNKNOWN`：184
- `TEMPORAL_PAUSE`：6
- `TEMPORAL_ALLOW`：6

解释：系统已按时间证据完整性进行保守门禁。缺少跨阶段时间链的 token 不会被强行当成同步状态处理。

### 4.5 temporal_sync_status 分布

- `TEMPORAL_UNKNOWN`：184
- `TEMPORAL_DESYNC`：6
- `TEMPORAL_SYNCED`：6

解释：只有具备足够时间锚点的 token 才能进入 `TEMPORAL_SYNCED` 或 `TEMPORAL_DESYNC`；无法形成完整时间链的 token 保守标记为 `TEMPORAL_UNKNOWN`。

### 4.6 stale 统计

- `wallet_decision_stale`：12

阶段 stale 统计：

- `S1_CANDIDATE_DISCOVERY`：104
- `S4_WALLET_STRUCTURE`：12
- `S10_PAPER_RUNNER`：2

解释：stale 集中在候选发现、钱包结构、paper runner 三个阶段，说明当前 runtime 更像是多来源历史/运行产物混合，而不是统一候选发现批次。

## 5. 硬规则验收

阶段 1.3 的关键硬规则结果如下：

- D0 是否出现 `TEMPORAL_ALLOW`：否
- D4 是否被错误 `TEMPORAL_BLOCK`：否
- `quote_stale=true` 是否出现 `TEMPORAL_ALLOW`：否
- S3/S4 stale 规则：本轮无错误放行样本

对应计数：

- `d0_temporal_allow_count`：0
- `d4_wrong_block_count`：0
- `quote_stale_allow_count`：0
- `s3_s4_expired_count`：0

结论：时间门禁硬规则未发现错误放行或错误阻断。

## 6. TEMPORAL_UNKNOWN 根因

`TEMPORAL_UNKNOWN` 的根因已经收敛，不是规则测试失败，而是输入证据链不完整。

主要原因：

- 候选输入来源混合：`gmgn_new_token_filter`、`state_machine`、`candidate_signal_outputs`、`dashboard_data`、`live_state`、`paper_live`、`quote_security` 等来源同时参与合并。
- 多数记录来自下游 paper/report/dashboard 运行产物，而不是标准候选发现入口。
- `first_seen_at` 在当前合并 token 中全部缺失。
- `token_open_time` 仅在极少数来源行出现。
- `quote_time`、`security_scan_time` 等 quote/security 时间锚点缺失率高。
- `wallet_decision_created_at` 只在少量 paper/case 文件中出现。
- 跨阶段时间链无法完整形成，因此 `compute_temporal_sync_status` 保守返回 `TEMPORAL_UNKNOWN`。

字段可用率样本：

- `token_open_time`：1 / 196，约 0.51%
- `discovered_at`：1 / 196，约 0.51%
- `first_seen_at`：0 / 196，0%
- `last_seen_at`：192 / 196，约 97.96%
- `signal_time`：37 / 196，约 18.88%
- `signal_level`：196 / 196，100%
- `wallet_decision_created_at`：12 / 196，约 6.12%
- `quote_time`：0 / 196，0%
- `security_scan_time`：0 / 196，0%

结论：当前 `TEMPORAL_UNKNOWN` 是数据质量/时间锚点问题，不是门禁规则失效。

## 7. 输入字段来源收敛

阶段 1.3 已把输入字段来源收敛到可审计形态。

### 7.1 token 来源聚合

主要来源包括：

- `paper_live/failure_attribution.jsonl`
- `paper_live/risk_events.jsonl`
- `site/dashboard_data.json`
- `paper_live/position_journal/*.jsonl`
- `gmgn_new_token_filter/token_candidates.json`
- `state_machine/candidate_states.json`
- `candidate_signal_outputs/candidate_signal_summary.json`
- `live_state.json`
- `wallet_structure/*/wallet_structure_decision.json`
- `quote_security/*/*.json`
- `paper_live/paper_positions_open.json`
- `paper_live/paper_positions_closed.json`
- `paper_live/case_files/*.json`

### 7.2 收敛结果

已输出：

- token 来源文件计数
- 去重前/后 token 数量
- fallback token 来源
- 字段可用率
- 字段 top_paths
- `STAGE_UNKNOWN` 原因
- `TEMPORAL_UNKNOWN` 原因
- missing_fields Top 10
- missing_sources 列表

这意味着后续不再需要靠人工猜测“为什么 unknown”，可以直接从 `time_context_input_audit.json/md` 定位缺失字段和来源路径。

## 8. missing_fields Top 10

本轮 Top 10 缺失字段：

- `age_sec`：196
- `created_at`：196
- `elapsed_sec`：196
- `failure_detected_at`：196
- `final_gate_created_at`：196
- `input_window_end`：196
- `input_window_start`：196
- `intent_created_at`：196
- `latest_kline_time`：196
- `lifecycle_created_at`：196

解释：这些字段属于统一时间 schema 的横向字段，目前很多来源是历史 dashboard、paper、case/report 产物，并不天然包含完整时间上下文字段。本阶段先完成审计和门禁，不强行伪造缺失时间。

## 9. missing_sources 列表

本轮缺失/不完整来源类型：

- `candidate_discovery`
- `daily_review`
- `dominant_intent`
- `dominant_lifecycle`
- `failure_attribution`
- `final_gate`
- `kline_collection`
- `paper_runner`
- `pattern_recognition`
- `quote_security`
- `wallet_pattern_alignment`
- `wallet_structure`

解释：这些来源并非都完全不存在，而是对部分 token 缺少标准时间字段或完整阶段证据。因此系统按 token 维度保守降级。

## 10. 验收命令与结果

### 10.1 专项测试

命令：

```bash
cd /root/sikk-gmgn
PYTHONPATH=/root/sikk-gmgn python3 -m pytest tests/test_sikk_time_context_gate.py -q
```

结果：

```text
4 passed in 0.05s
```

### 10.2 time_context gate 单独运行

命令：

```bash
cd /root/sikk-gmgn
PYTHONPATH=/root/sikk-gmgn python3 sikk_time_context_gate.py --base-dir data/gmgn_candidates_live_run
```

结果：

```json
{"status": "ok", "token_count": 196, "output_dir": "data/gmgn_candidates_live_run/time_context"}
```

### 10.3 全量测试

命令：

```bash
cd /root/sikk-gmgn
PYTHONPATH=/root/sikk-gmgn python3 -m pytest -q
```

结果：

```text
245 passed in 13.51s
```

### 10.4 runtime 单入口验证

命令：

```bash
cd /root/sikk-gmgn
PYTHONPATH=/root/sikk-gmgn python3 sikk_live_run.py --mode once --output-root data/gmgn_candidates_live_run --limit 5 --quote-sources none
```

结果：runtime 成功生成：

- `live_run_manifest.json`
- `live_state.json`
- `live_board.md`
- `live_dashboard.html`
- `site/dashboard_data.json`
- `site/index.html`
- `site/app.js`
- `site/style.css`
- `events/live_events.jsonl`
- `events/latest_events.md`
- paper daily report
- wallet structure daily report
- token status
- telegram callback index
- system index

## 11. 阶段 1.3 结论

阶段 1.3 已完成验收。

确认结果：

- 规则测试通过。
- 全量测试通过。
- runtime 单入口验证通过。
- `TEMPORAL_UNKNOWN` 根因已定位为输入时间证据链不完整。
- 输入字段来源已收敛到可审计文件。
- D0 未错误放行。
- D4 未错误阻断。
- quote stale 未错误放行。
- 系统仍保持 paper-only 安全边界。

## 12. 后续建议

下一阶段建议不是直接开启实盘，而是继续补齐时间证据链：

1. 候选发现入口统一写入：
   - `token_open_time`
   - `discovered_at`
   - `first_seen_at`
   - `candidate_batch_id`

2. quote/security 输出统一写入：
   - `quote_time`
   - `quote_received_at`
   - `security_scan_time`
   - `security_scan_created_at`

3. 钱包结构输出统一写入：
   - `wallet_decision_created_at`
   - `wallet_snapshot_time`
   - `wallet_delta_time`

4. 生命周期/意图/盘型模块统一写入：
   - `lifecycle_created_at`
   - `intent_created_at`
   - `pattern_created_at`
   - `latest_kline_time`

5. dashboard/paper/case file 只读消费时间上下文，不反向伪造发现时间。

6. 继续保持：
   - paper-only
   - no swap
   - no signing
   - no broadcast
   - no private key
