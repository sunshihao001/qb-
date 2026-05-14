# SIKK / HER 单 Token Runtime Absorption Acceptance Report

- created_at: 2026-05-14T20:34:54Z
- token: TROLLIEN `ECgweD7xkMj4bm8CcM9rusxKjyQGgdosCvVmhGUupump`
- replay_mode: readonly_existing_runtime_output_absorption
- final_acceptance: **PHASE_REPLAY_PASS_WITH_GAPS**

## 判定依据
- P01-P08：已形成从候选事实、钱包/筹码事实、结构推理、筹码结构、证据/反证、场景识别、策略门禁到 paper-only gate 的连续 handoff。
- P08/P09：已消费既有 paper runner closed position，未执行真实 swap/签名/广播。
- P07 strategy gate 明确消费了 P01-P06 handoff 与 runtime `candidate_states.json`。
- 每个阶段均写入 `phase_trace.jsonl`，字段包含 phase_id/input_files/output_files/runner_used/decision/evidence_level/counter_evidence/missing_fields/status/failure_reason/downstream_handoff。

## 为什么不是 PASS
- 钱包结构为 `WALLET_BLOCK` 且 `would_block=true`，但 runtime 当前 wallet gate mode 为 observe-only，仍允许 `PAPER_READY`。
- wallet row-level 字段缺失：wallet_address, role, game_side, evidence_level。
- P06 场景识别是基于现有 runtime 输出重建，未发现独立 native P06 runner 输出。
- quote/security `max_price_impact_pct` 为 null。
- `failure_attribution.jsonl` 未包含该 token 的专属复盘 row，虽然 `paper_positions_closed.json` 存在该 token 的 closed paper result。

## 验收结论
**PHASE_REPLAY_PASS_WITH_GAPS**：闭环可跑通，但必须按 issue registry 修复门禁/字段/复盘 trace 缺口后，才能升级为无缺口 PASS。
