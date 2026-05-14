# SIKK-SOL v0.4 初始审计：OKX 前300集群关联与持仓行为层

- 审计时间：2026-05-03T01:41:10Z
- 当前分支：`sikk-paper-audit-20260502`
- 当前基线提交：`e562a45 feat: add SIKK v0.3 chip control context loop`
- 安全边界：paper-only；不真实买入/卖出；不调用 gmgn_swap/gmgn_cooking；不广播；不 yolo。
- 基线测试：`PYTHONPATH=/root/sikk-gmgn pytest -q` → `133 passed in 9.77s`

## 1. 审计结论

- 现有代码尚无正式 `sikk_okx_cluster_holding_analyzer.py` 或 `okx_cluster_*` 标准输出层。
- v0.3 已有 `sikk_chip_control_state_machine.py`，适合作为 OKX 集群证据接入口。
- v0.3 已有 `sikk_market_cap_context.py`、`sikk_dominant_lifecycle_classifier.py`，可与集群入场市值、集群 delta、生命周期证据关联。
- `sikk_system_audit.py` 与 `sikk_explainability_engine.py` 已有 v0.3 字段检查，可扩展 v0.4 的 `okx_cluster` 字段。
- paper failure attribution 已存在，可增加 `CLUSTER_DISTRIBUTION_RISK`、`COUNTERPARTY_ABSORBING_CLUSTER`、`BAGHOLDER_CLUSTER` 等归因。

## 2. 关键搜索结果

### okx_cluster_existing
```text
NO_MATCH
```
### chip_state
```text
sikk_candidate_wallet_structure_pipeline.py:276:                "筹码控制权状态": decision.chip_control_state,
sikk_chip_control_state_machine.py:16:CHIP_CONTROL_STATES = {
sikk_chip_control_state_machine.py:17:    "CONTROL_RETAINED_BY_STRUCTURE_SIDE",
sikk_chip_control_state_machine.py:18:    "CONTROL_MIGRATING_TO_COUNTERPARTY",
sikk_chip_control_state_machine.py:19:    "CONTROL_LOST_TO_DISTRIBUTION",
sikk_chip_control_state_machine.py:20:    "CONTROL_UNCLEAR",
sikk_chip_control_state_machine.py:25:    "CONTROL_RETAINED_BY_STRUCTURE_SIDE": "ALLOW_PAPER_READY_IF_OTHER_GATES_PASS",
sikk_chip_control_state_machine.py:26:    "CONTROL_MIGRATING_TO_COUNTERPARTY": "PAUSE_OR_EXIT_MONITOR",
sikk_chip_control_state_machine.py:27:    "CONTROL_LOST_TO_DISTRIBUTION": "BLOCK_OR_FORCE_PAPER_EXIT",
sikk_chip_control_state_machine.py:28:    "CONTROL_UNCLEAR": "OBSERVE_ONLY",
sikk_chip_control_state_machine.py:34:SUPPORTIVE_LIFECYCLES = {"EARLY_ACCUMULATION", "CONTROL_BOX_ACCUMULATION", "SECOND_STAGE_PREPARATION", "SECOND_STAGE_EXPANSION", "REACTIVATION", "FAST_ACCUMULATION_LAUNCH"}
sikk_chip_control_state_machine.py:41:    chip_control_state: str = "CONTROL_UNCLEAR"
sikk_chip_control_state_machine.py:47:    invalidators: list[str] = field(default_factory=list)
sikk_chip_control_state_machine.py:56:            "chip_control_state": self.chip_control_state,
sikk_chip_control_state_machine.py:57:            "筹码控制权状态": self.chip_control_state,
sikk_chip_control_state_machine.py:67:            "invalidators": self.invalidators,
sikk_chip_control_state_machine.py:68:            "chip_control_invalidators": self.invalidators,
sikk_chip_control_state_machine.py:114:def evaluate_chip_control_state(
sikk_chip_control_state_machine.py:163:    invalidators: list[str] = []
sikk_chip_control_state_machine.py:165:    state = "CONTROL_UNCLEAR"
sikk_chip_control_state_machine.py:172:        invalidators.append("缺少 wallet_structure_decision，不能判断筹码控制权")
sikk_chip_control_state_machine.py:178:        invalidators.append("钱包结构数据质量不足，必须补采或降级观察")
sikk_chip_control_state_machine.py:180:        state = "CONTROL_LOST_TO_DISTRIBUTION"
sikk_chip_control_state_machine.py:183:        reasons.append("CONTROL_BREAK_OR_DISTRIBUTION")
sikk_chip_control_state_machine.py:190:        invalidators.extend(["主动分发/生命周期阻断已出现", "quote/security 转为 BLOCK 或 MISSING", "paper 持仓进入 FORCE_PAPER_EXIT 复盘"])
sikk_chip_control_state_machine.py:192:        state = "CONTROL_MIGRATING_TO_COUNTERPARTY"
sikk_chip_control_state_machine.py:195:        reasons.append("CONTROL_MIGRATING_TO_COUNTERPARTY")
sikk_chip_control_state_machine.py:202:        invalidators.extend(["对手盘压力继续升高", "同源/同步组继续卖出", "高结果钱包持仓继续下降"])
sikk_chip_control_state_machine.py:204:        state = "CONTROL_LOST_TO_DISTRIBUTION" if (has_clearout or has_distribution or lifecycle_state in {"ACTIVE_DISTRIBUTION", "FINAL_DISTRIBUTION"}) else "CONTROL_MIGRATING_TO_COUNTERPARTY"
sikk_chip_control_state_machine.py:207:        reasons.append("CONTROL_BREAK_OR_DISTRIBUTION")
sikk_chip_control_state_machine.py:216:        invalidators.extend(["早期/结构侧钱包继续清仓", "quote/security 转为 BLOCK 或 MISSING", "paper 持仓进入 FORCE_PAPER_EXIT 复盘"])
sikk_chip_control_state_machine.py:218:        state = "CONTROL_RETAINED_BY_STRUCTURE_SIDE"
sikk_chip_control_state_machine.py:228:        invalidators.extend(["同源/同步组卖出分升至 60+", "对手盘压力升至 50+", "wallet_structure_status 变为 WALLET_PAUSE/WALLET_BLOCK", "quote/security 未通过时不得进入 PAPER_READY"])
sikk_chip_control_state_machine.py:230:        state = "CONTROL_RETAINED_BY_STRUCTURE_SIDE"
sikk_chip_control_state_machine.py:234:        invalidators.extend(["单点结构证据偏弱，只能作为记录/观察", "quote/security 未通过时不得进入 PAPER_READY"])
sikk_chip_control_state_machine.py:236:        state = "CONTROL_UNCLEAR"
sikk_chip_control_state_machine.py:239:        reasons.append("CONTROL_UNCLEAR")
sikk_chip_control_state_machine.py:240:        invalidators.append("缺少足够结构侧保留或迁移证据")
sikk_chip_control_state_machine.py:245:        if mc_change >= 500 and state == "CONTROL
```
### dashboard
```text
scripts/hindsight_recall_sikk.py:43:    parser.add_argument("--max-tokens", type=int, default=4096)
scripts/hindsight_recall_sikk.py:57:            max_tokens=args.max_tokens,
sikk_candidate_state_machine.py:100:    for key in ["候选结果", "候选列表", "tokens", "candidates", "results"]:
sikk_candidate_wallet_structure_pipeline.py:276:                "筹码控制权状态": decision.chip_control_state,
sikk_chip_control_state_machine.py:41:    chip_control_state: str = "CONTROL_UNCLEAR"
sikk_chip_control_state_machine.py:42:    chip_control_confidence: int = 0
sikk_chip_control_state_machine.py:43:    chip_control_action: str = "OBSERVE_ONLY"
sikk_chip_control_state_machine.py:56:            "chip_control_state": self.chip_control_state,
sikk_chip_control_state_machine.py:57:            "筹码控制权状态": self.chip_control_state,
sikk_chip_control_state_machine.py:58:            "chip_control_confidence": self.chip_control_confidence,
sikk_chip_control_state_machine.py:59:            "筹码控制置信度": self.chip_control_confidence,
sikk_chip_control_state_machine.py:60:            "chip_control_action": self.chip_control_action,
sikk_chip_control_state_machine.py:61:            "筹码控制动作": self.chip_control_action,
sikk_chip_control_state_machine.py:64:            "chip_control_reason_codes": self.reason_codes,
sikk_chip_control_state_machine.py:66:            "chip_control_evidence_refs": self.evidence_refs,
sikk_chip_control_state_machine.py:68:            "chip_control_invalidators": self.invalidators,
sikk_chip_control_state_machine.py:114:def evaluate_chip_control_state(
sikk_chip_control_state_machine.py:117:    lifecycle_row: Mapping[str, Any] | None = None,
sikk_chip_control_state_machine.py:128:    lifecycle = lifecycle_row or {}
sikk_chip_control_state_machine.py:132:    token = str(_first(wallet, "token_address", "代币地址", "token", default=_first(lifecycle, "token_address", "代币地址", default=_first(market, "token_address", "代币地址", default=""))))
sikk_chip_control_state_machine.py:133:    symbol = str(_first(wallet, "symbol", "token_symbol", "代币符号", default=_first(lifecycle, "symbol", "token_symbol", "代币符号", default="")))
sikk_chip_control_state_machine.py:147:    lifecycle_state = str(_first(lifecycle, "dominant_side_lifecycle", "lifecycle", "主导侧生命周期", default="UNKNOWN"))
sikk_chip_control_state_machine.py:148:    lifecycle_intent = str(_first(lifecycle, "dominant_side_intent", "intent", "主导侧意图", default="UNKNOWN"))
sikk_chip_control_state_machine.py:149:    lifecycle_action = str(_first(lifecycle, "allowed_action", "允许动作", default="UNKNOWN"))
sikk_chip_control_state_machine.py:179:    elif lifecycle_state in BLOCKING_LIFECYCLES or has_distribution:
sikk_chip_control_state_machine.py:181:        confidence = 85 if lifecycle_state in BLOCKING_LIFECYCLES else 78
sikk_chip_control_state_machine.py:184:        if lifecycle_state in BLOCKING_LIFECYCLES:
sikk_chip_control_state_machine.py:185:            reasons.append(f"LIFECYCLE_{lifecycle_state}")
sikk_chip_control_state_machine.py:191:    elif has_sync_sell or sync_sell >= 60 or counterparty >= 50 or lifecycle_state in MIGRATING_LIFECYCLES:
sikk_chip_control_state_machine.py:200:        if lifecycle_state in MIGRATING_LIFECYCLES:
sikk_chip_control_state_machine.py:201:            reasons.append(f"LIFECYCLE_{lifecycle_state}")
sikk_chip_control_state_machine.py:204:        state = "CONTROL_LOST_TO_DISTRIBUTION" if (has_clearout or has_distribution or lifecycle_state in {"ACTIVE_DISTRIBUTION", "FINAL_DISTRIBUTION"}) else "CONTROL_MIGRATING_TO_COUNTERPARTY"
sikk_chip_control_state_machine.py:205:        confidence = 85 if lifecycle_state in BLOCKING_LIFECYCLES else 75
sikk_chip_control_state_machine.py:208:        if lifecycle_state in BLOCKING_LIFECYCLES:
sikk_chip_control_state_machine.py:209:            reasons.append(f"LIFECYCLE_{lifecycle_state}")
sikk_chip_control_state_machine.py:225:        if lifecycle_state in SUPPORTIVE_LIFECYCLES:
sikk_chip_control_state_machine.py:227:            reasons.append(f"LIFE
```
### audit
```text
sikk_chip_control_state_machine.py:48:    missing_fields: list[str] = field(default_factory=list)
sikk_chip_control_state_machine.py:69:            "missing_fields": self.missing_fields,
sikk_chip_control_state_machine.py:277:        missing_fields=missing,
sikk_dashboard_builder.py:76:    failure_rows = _read_jsonl(paper_dir / "failure_attribution.jsonl")
sikk_dashboard_builder.py:143:        "failure_attribution_type": _pick(token, paper, paper_closed, failure, keys=("failure_attribution_type", "failure_type")),
sikk_dashboard_builder.py:231:            f"<td>{_display(event['failure_attribution_type'])}</td>"
sikk_dashboard_builder.py:247:<h2>Token 状态 / 事件链路</h2><p>缺失字段统一显示“待补”，用于审计发现→判断→入场→持仓→退出链路。</p><div class="table-wrap"><table><thead><tr><th>符号</th><th>地址</th><th>Priority</th><th>State</th><th>Signal Level</th><th>Signal Gate</th><th>Wallet</th><th>结构分</th><th>风险分</th><th>对手盘</th><th>数据质量</th><th>Quote</th><th>Security</th><th>Paper</th><th>PnL</th><th>discovered_at</th><th>discovery_market_cap_usd</th><th>discovery_liquidity_usd</th><th>first_signal_at</th><th>first_signal_type</th><th>signal_market_cap_usd</th><th>wallet_decision_at</th><th>wallet_decision_market_cap_usd</th><th>paper_entry_at</th><th>paper_entry_market_cap_usd</th><th>paper_entry_price</th><th>paper_entry_amount_sol</th><th>paper_entry_amount_usd</th><th>paper_token_amount</th><th>current_market_cap_usd</th><th>current_price</th><th>unrealized_pnl_sol</th><th>unrealized_pnl_pct</th><th>exit_monitor_at</th><th>paper_exit_at</th><th>exit_reason</th><th>failure_attribution_type</th><th>Reason</th><th>Next</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
sikk_explainability_engine.py:223:        _append_if_present(q["为什么失败"], _field(failure, "failure_type", "失败类型"), sources.get("failure", "failure_attribution.jsonl"), "failure_type", "失败类型")
sikk_explainability_engine.py:224:        _append_if_present(q["为什么失败"], _field(failure, "failure_reason", "失败原因"), sources.get("failure", "failure_attribution.jsonl"), "failure_reason", "失败原因")
sikk_explainability_engine.py:227:        q["为什么失败"].append(_missing("为什么失败", sources.get("failure", "failure_attribution.jsonl")))
sikk_explainability_engine.py:236:        _evidence("待复查", "如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致", f"{sources.get('paper_open', 'paper_positions_open.json')}；{sources.get('paper_closed', 'paper_positions_closed.json')}；{sources.get('failure', 'failure_attribution.jsonl')}"),
sikk_explainability_engine.py:241:        _evidence("条件", "paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败", f"{sources.get('paper_closed', 'paper_positions_closed.json')}；{sources.get('failure', 'failure_attribution.jsonl')}"),
sikk_explainability_engine.py:314:    failure_path = base / "paper_live" / "failure_attribution.jsonl"
sikk_explainability_engine.py:333:        "failure_attribution": failure_path,
sikk_live_run.py:149:def _failure_attribution_rows(root: Path) -> Dict[str, Dict[str, Any]]:
sikk_live_run.py:150:    path = root / "paper_live" / "failure_attribution.jsonl"
sikk_live_run.py:187:        "failure_attribution_type": row.get("failure_type") or paper.get("failure_attribution_type"),
sikk_live_run.py:194:            "failure_attribution_type": row.get("failure_type") or paper.get("failure_attribution_type"),
sikk_live_run.py:225:    failure_by_token = _failure_attribution_rows(base)
sikk_live_run.py:256:            paper["failure_attribution_type"] = failure_row.get("failure_type") or paper.get("failure_attribution_type")
sikk_live_run.py:470:        failure_attribution_path=root / "paper_live" / "failure_attribution.jsonl",
sikk_market_cap_context.py:38:    market_cap_missing_fields: list[str] = field(default_factory=list)
sikk_market_cap_context.py:56:                "market_cap_missing_fields": self.market_cap_missing_fields,
sikk_market_cap_context.py:69:            "market_cap_missing_fields": self.market_cap_missing_fields,
sikk_market_cap_context.py:175:    
```
### explain
```text
sikk_candidate_wallet_structure_pipeline.py:276:                "筹码控制权状态": decision.chip_control_state,
sikk_chip_control_state_machine.py:41:    chip_control_state: str = "CONTROL_UNCLEAR"
sikk_chip_control_state_machine.py:42:    chip_control_confidence: int = 0
sikk_chip_control_state_machine.py:43:    chip_control_action: str = "OBSERVE_ONLY"
sikk_chip_control_state_machine.py:56:            "chip_control_state": self.chip_control_state,
sikk_chip_control_state_machine.py:57:            "筹码控制权状态": self.chip_control_state,
sikk_chip_control_state_machine.py:58:            "chip_control_confidence": self.chip_control_confidence,
sikk_chip_control_state_machine.py:59:            "筹码控制置信度": self.chip_control_confidence,
sikk_chip_control_state_machine.py:60:            "chip_control_action": self.chip_control_action,
sikk_chip_control_state_machine.py:61:            "筹码控制动作": self.chip_control_action,
sikk_chip_control_state_machine.py:64:            "chip_control_reason_codes": self.reason_codes,
sikk_chip_control_state_machine.py:66:            "chip_control_evidence_refs": self.evidence_refs,
sikk_chip_control_state_machine.py:68:            "chip_control_invalidators": self.invalidators,
sikk_chip_control_state_machine.py:114:def evaluate_chip_control_state(
sikk_chip_control_state_machine.py:147:    lifecycle_state = str(_first(lifecycle, "dominant_side_lifecycle", "lifecycle", "主导侧生命周期", default="UNKNOWN"))
sikk_chip_control_state_machine.py:250:        missing.append("market_cap_context")
sikk_chip_control_state_machine.py:259:        "market_cap_context" if market else "market_cap_context_missing",
sikk_chip_control_state_machine.py:270:        chip_control_state=state,
sikk_chip_control_state_machine.py:271:        chip_control_confidence=confidence,
sikk_chip_control_state_machine.py:272:        chip_control_action=STATE_TO_ACTION[state],
sikk_chip_control_state_machine.py:282:__all__ = ["CHIP_CONTROL_STATES", "STATE_TO_ACTION", "ChipControlDecision", "evaluate_chip_control_state"]
sikk_dominant_lifecycle_classifier.py:18:from sikk_chip_control_state_machine import evaluate_chip_control_state
sikk_dominant_lifecycle_classifier.py:358:    chip_control = evaluate_chip_control_state(
sikk_dominant_lifecycle_classifier.py:363:            "dominant_side_lifecycle": lifecycle,
sikk_dominant_lifecycle_classifier.py:374:        "dominant_side_lifecycle": lifecycle,
sikk_dominant_lifecycle_classifier.py:399:        "chip_control_state": chip_control["chip_control_state"],
sikk_dominant_lifecycle_classifier.py:400:        "chip_control_confidence": chip_control["chip_control_confidence"],
sikk_dominant_lifecycle_classifier.py:401:        "chip_control_action": chip_control["chip_control_action"],
sikk_dominant_lifecycle_classifier.py:402:        "chip_control_reason_codes": chip_control["chip_control_reason_codes"],
sikk_dominant_lifecycle_classifier.py:403:        "chip_control_invalidators": chip_control["chip_control_invalidators"],
sikk_dominant_lifecycle_classifier.py:404:        "chip_control_evidence_refs": chip_control["chip_control_evidence_refs"],
sikk_dominant_lifecycle_classifier.py:417:        "主导侧生命周期": row["dominant_side_lifecycle"],
sikk_dominant_lifecycle_classifier.py:442:        "筹码控制权状态": row.get("chip_control_state"),
sikk_dominant_lifecycle_classifier.py:443:        "筹码控制置信度": row.get("chip_control_confidence"),
sikk_dominant_lifecycle_classifier.py:444:        "筹码控制动作": row.get("chip_control_action"),
sikk_dominant_lifecycle_classifier.py:445:        "筹码控制原因码": "；".join(row.get("chip_control_reason_codes") or []),
sikk_dominant_lifecycle_classifier.py:446:        "筹码控制失效条件": "；".join(row.get("chip_control_invalidators") or []),
sikk_dominant_lifecycle_classifier.py:525:        lifecycle_counts[row["dominant_side_lifecycle"]] = lifecycle_counts.get(row["dominant_side_lifecycle"], 0) + 1
sikk_explainability_engine.py:23:    "为什么支持",
sikk_explainability_engine.py:29:    "下一步看什么",
sikk_explainability_engine.
```
### paper_failure
```text
sikk_chip_control_state_machine.py:26:    "CONTROL_MIGRATING_TO_COUNTERPARTY": "PAUSE_OR_EXIT_MONITOR",
sikk_chip_control_state_machine.py:27:    "CONTROL_LOST_TO_DISTRIBUTION": "BLOCK_OR_FORCE_PAPER_EXIT",
sikk_chip_control_state_machine.py:190:        invalidators.extend(["主动分发/生命周期阻断已出现", "quote/security 转为 BLOCK 或 MISSING", "paper 持仓进入 FORCE_PAPER_EXIT 复盘"])
sikk_chip_control_state_machine.py:216:        invalidators.extend(["早期/结构侧钱包继续清仓", "quote/security 转为 BLOCK 或 MISSING", "paper 持仓进入 FORCE_PAPER_EXIT 复盘"])
sikk_chip_control_state_machine.py:253:        reasons.append("PAPER_OPEN_REQUIRES_EXIT_MONITOR")
sikk_chip_control_state_machine.py:254:        invalidators.append("paper 仓位应进入 EXIT_MONITOR / FORCE_PAPER_EXIT 复盘路径")
sikk_dashboard_builder.py:71:    closed_payload = _read_json(paper_dir / "paper_positions_closed.json")
sikk_dashboard_builder.py:75:        closed_rows = _read_csv_rows(paper_dir / "paper_positions_closed.csv")
sikk_dashboard_builder.py:76:    failure_rows = _read_jsonl(paper_dir / "failure_attribution.jsonl")
sikk_dashboard_builder.py:140:        "exit_monitor_at": _pick(token, paper, source, failure, keys=("exit_monitor_at", "事件时间", "last_update_time")) if monitor_action in {"EXIT_MONITOR", "PAPER_FORCE_EXIT"} else _pick(token, paper, keys=("exit_monitor_at",)),
sikk_dashboard_builder.py:143:        "failure_attribution_type": _pick(token, paper, paper_closed, failure, keys=("failure_attribution_type", "failure_type")),
sikk_dashboard_builder.py:231:            f"<td>{_display(event['failure_attribution_type'])}</td>"
sikk_dashboard_builder.py:247:<h2>Token 状态 / 事件链路</h2><p>缺失字段统一显示“待补”，用于审计发现→判断→入场→持仓→退出链路。</p><div class="table-wrap"><table><thead><tr><th>符号</th><th>地址</th><th>Priority</th><th>State</th><th>Signal Level</th><th>Signal Gate</th><th>Wallet</th><th>结构分</th><th>风险分</th><th>对手盘</th><th>数据质量</th><th>Quote</th><th>Security</th><th>Paper</th><th>PnL</th><th>discovered_at</th><th>discovery_market_cap_usd</th><th>discovery_liquidity_usd</th><th>first_signal_at</th><th>first_signal_type</th><th>signal_market_cap_usd</th><th>wallet_decision_at</th><th>wallet_decision_market_cap_usd</th><th>paper_entry_at</th><th>paper_entry_market_cap_usd</th><th>paper_entry_price</th><th>paper_entry_amount_sol</th><th>paper_entry_amount_usd</th><th>paper_token_amount</th><th>current_market_cap_usd</th><th>current_price</th><th>unrealized_pnl_sol</th><th>unrealized_pnl_pct</th><th>exit_monitor_at</th><th>paper_exit_at</th><th>exit_reason</th><th>failure_attribution_type</th><th>Reason</th><th>Next</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
sikk_explainability_engine.py:216:        _append_if_present(q["为什么退出"], _field(paper_closed, "exit_reason", "退出原因"), sources.get("paper_closed", "paper_positions_closed.json"), "exit_reason", "纸面退出原因")
sikk_explainability_engine.py:217:        _append_if_present(q["为什么退出"], _field(paper_closed, "exit_time", "退出时间"), sources.get("paper_closed", "paper_positions_closed.json"), "exit_time", "纸面退出时间")
sikk_explainability_engine.py:220:        q["为什么退出"].append(_missing("为什么退出", sources.get("paper_closed", "paper_positions_closed.json")))
sikk_explainability_engine.py:223:        _append_if_present(q["为什么失败"], _field(failure, "failure_type", "失败类型"), sources.get("failure", "failure_attribution.jsonl"), "failure_type", "失败类型")
sikk_explainability_engine.py:224:        _append_if_present(q["为什么失败"], _field(failure, "failure_reason", "失败原因"), sources.get("failure", "failure_attribution.jsonl"), "failure_reason", "失败原因")
sikk_explainability_engine.py:227:        q["为什么失败"].append(_missing("为什么失败", sources.get("failure", "failure_attribution.jsonl")))
sikk_explainability_engine.py:236:        _evidence("待复查", "如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致", f"{sources.get('paper_open', 'paper_positions_open.json')}；{sources.get('paper_closed', 'paper_positions_closed.json')}；{sources.get('failure', 'failure_attribution.jsonl')}"),
sikk_explainabil
```
