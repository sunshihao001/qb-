# 钱包结构交易接入适配层 Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** 把已有钱包结构采集/分析系统作为旁路情报源安全接入交易状态机和 paper runner，避免钱包采集/字段缺失/过期结论卡死主流程。

**Architecture:** 新增 `sikk_wallet_trade_adapter.py` 作为交易接入适配层，只读取标准 `wallet_structure_decision.json` / 已有 summary 结论，不现场调用钱包采集。状态机增加 `wallet_structure_mode=off|observe|soft|hard`，默认 `observe`；paper runner 复用适配器写入钱包结构字段并处理持仓恶化动作。

**Tech Stack:** Python stdlib, pytest, existing `/root/sikk-gmgn` JSON/CSV pipeline. 默认 paper/readiness，只读，不执行真实 swap。

---

## Task 1: 新增 wallet trade adapter 合约与缺失降级

**Objective:** 创建 `sikk_wallet_trade_adapter.py`，提供缺失 decision 不崩溃的标准返回，并支持读取单 token `wallet_structure_decision.json`。

**Files:**
- Create: `sikk_wallet_trade_adapter.py`
- Test: `tests/test_sikk_wallet_trade_adapter.py`

**Step 1: Write failing test**

```python
def test_load_wallet_decision_missing_returns_unknown_and_stale(tmp_path):
    from sikk_wallet_trade_adapter import load_wallet_decision

    decision = load_wallet_decision("TokenMissing111", tmp_path / "wallet_structure")

    assert decision["wallet_structure_status"] == "WALLET_UNKNOWN"
    assert decision["decision_action"] == "NO_DECISION"
    assert decision["wallet_structure_factor"] == 1.0
    assert decision["is_stale"] is True
    assert decision["reason"] == "wallet_structure_decision_missing"
```

**Step 2: Run test to verify failure**

Run:

```bash
cd /root/sikk-gmgn
python3 -m pytest tests/test_sikk_wallet_trade_adapter.py::test_load_wallet_decision_missing_returns_unknown_and_stale -q
```

Expected: FAIL because module does not exist.

**Step 3: Write minimal implementation**

Implement:
- `_read_json(path)`
- `load_wallet_decision(token_address, wallet_structure_dir)`
- fallback fields: `WALLET_UNKNOWN`, scores `0`, factor `1.0`, reason `wallet_structure_decision_missing`, `is_stale=True`.

**Step 4: Run test to verify pass**

```bash
python3 -m pytest tests/test_sikk_wallet_trade_adapter.py::test_load_wallet_decision_missing_returns_unknown_and_stale -q
```

---

## Task 2: 实现 apply_wallet_gate 的 off/observe/soft/hard 语义

**Objective:** 让状态机可通过统一适配器应用钱包结构模式，默认 observe 不改变状态。

**Files:**
- Modify: `sikk_wallet_trade_adapter.py`
- Test: `tests/test_sikk_wallet_trade_adapter.py`

**Step 1: Write failing tests**

Add tests:

```python
def test_apply_wallet_gate_observe_records_but_does_not_block():
    from sikk_wallet_trade_adapter import apply_wallet_gate

    status = {"state": "PAPER_READY", "当前状态": "PAPER_READY"}
    decision = {"wallet_structure_status": "WALLET_BLOCK", "wallet_risk_score": 99, "counterparty_pressure_score": 99, "reason": "对手盘压力高"}

    out = apply_wallet_gate(status, decision, mode="observe")

    assert out["state"] == "PAPER_READY"
    assert out["wallet_gate"] == "WALLET_BLOCK"
    assert out["wallet_gate_effect"] == "OBSERVE_ONLY"
    assert out["would_block"] is True


def test_apply_wallet_gate_soft_blocks_only_high_confidence_risk():
    from sikk_wallet_trade_adapter import apply_wallet_gate

    out = apply_wallet_gate(
        {"state": "PAPER_READY"},
        {"wallet_structure_status": "WALLET_BLOCK", "wallet_risk_score": 80, "counterparty_pressure_score": 20, "reason": "高风险"},
        mode="soft",
    )

    assert out["state"] == "BLOCKED"
    assert out["wallet_gate_effect"] == "SOFT_BLOCK"


def test_apply_wallet_gate_hard_pauses_missing_or_unknown():
    from sikk_wallet_trade_adapter import apply_wallet_gate

    out = apply_wallet_gate({"state": "PAPER_READY"}, {"wallet_structure_status": "WALLET_UNKNOWN", "reason": "missing"}, mode="hard")

    assert out["state"] == "PAUSE"
    assert out["wallet_gate_effect"] == "HARD_PAUSE_UNKNOWN"
```

**Step 2:** Run tests and verify RED.

**Step 3:** Implement mode logic:
- `off`: no state change, effect `OFF`.
- `observe`: no state change, set `would_block/would_pause/support` flags.
- `soft`: only `WALLET_BLOCK` plus `wallet_risk_score >=75` or `counterparty_pressure_score >=70` blocks.
- `hard`: `WALLET_BLOCK -> BLOCKED`, `WALLET_PAUSE/WALLET_UNKNOWN/stale -> PAUSE`, support/neutral only set effect.

**Step 4:** Run adapter tests.

---

## Task 3: 状态机接入 wallet_structure_mode，默认 observe

**Objective:** 修改 `run_candidate_state_machine(...)`，不再默认硬阻断；默认 observe 只记录钱包结构，避免主流程被钱包结构卡死。

**Files:**
- Modify: `sikk_candidate_state_machine.py`
- Modify: `tests/test_sikk_state_wallet_structure_integration.py`
- Test: existing `tests/test_sikk_candidate_state_machine.py`

**Step 1: Write failing tests**

Update/add tests:

```python
def test_state_machine_default_observe_records_wallet_block_without_blocking(tmp_path):
    from tests.test_sikk_candidate_state_machine import _build_inputs, TOKEN_READY
    from sikk_candidate_state_machine import run_candidate_state_machine

    inputs = _build_inputs(tmp_path)
    wallet_summary = _write_json(tmp_path / "wallet_structure" / "candidate_wallet_structure_summary.json", {
        "处理结果": [{"代币地址": TOKEN_READY, "钱包结构结论": "WALLET_BLOCK", "钱包风险评分": 99, "对手盘压力评分": 99, "状态调整原因": "对手盘压力高"}]
    })

    result = run_candidate_state_machine(
        candidates_path=inputs["candidates"],
        kline_summary_path=inputs["kline"],
        signal_summary_path=inputs["signals"],
        wallet_structure_summary_path=wallet_summary,
        output_dir=tmp_path / "state_machine",
    )
    row = next(item for item in _read_json(Path(result["states_json"]))["候选状态"] if item["代币地址"] == TOKEN_READY)
    assert row["当前状态"] == "PAPER_READY"
    assert row["钱包结构结论"] == "WALLET_BLOCK"
    assert row["钱包门禁效果"] == "OBSERVE_ONLY"
```

Also update old hard-block tests to pass `wallet_structure_mode="hard"`.

**Step 2:** Run target test and verify failure.

**Step 3:** Implement:
- Import adapter helpers.
- Add `wallet_structure_mode: str = "observe"` parameter to `run_candidate_state_machine` and CLI `--wallet-structure-mode`.
- Convert existing `wallet_item` to decision dict.
- Use `apply_wallet_gate` only after deriving base state.
- Preserve Chinese fields plus new fields: `钱包门禁模式`, `钱包门禁效果`, `would_block`, `would_pause`, `wallet_decision_stale`.
- Hard mode retains old behavior.

**Step 4:** Run:

```bash
python3 -m pytest tests/test_sikk_state_wallet_structure_integration.py tests/test_sikk_candidate_state_machine.py -q
```

---

## Task 4: Orchestrator exposes wallet_structure_mode and defaults observe

**Objective:** `run_sikk_gmgn_pipeline.py` passes mode to both first and second state-machine runs; CLI adds `--wallet-structure-mode`.

**Files:**
- Modify: `run_sikk_gmgn_pipeline.py`
- Test: `tests/test_run_sikk_gmgn_pipeline.py` or integration test file

**Step 1:** Add test with fake wallet runner returning `WALLET_BLOCK`; default run should keep token `PAPER_READY` but show observe effect. Hard mode should block.

**Step 2:** Run failing test.

**Step 3:** Implement:
- `run_full_pipeline(..., wallet_structure_mode="observe")`
- `parser.add_argument("--wallet-structure-mode", choices=["off", "observe", "soft", "hard"], default="observe")`
- Manifest parameters include wallet_structure_mode.
- Pass mode into `run_candidate_state_machine(...)` both before and after wallet summary.

**Step 4:** Run related orchestrator tests.

---

## Task 5: Paper runner uses adapter for entry fields and open-position degradation

**Objective:** 统一 paper runner 的钱包字段写入和持仓恶化规则，补充 dominant/chip 状态触发。

**Files:**
- Modify: `sikk_paper_live_runner.py`
- Test: `tests/test_sikk_paper_live_runner.py`

**Step 1: Write failing tests**

Add tests:
- New paper entry contains `dominant_side_status`, `chip_transfer_status`, `wallet_decision_age_sec`, `wallet_decision_stale` when state/decision provides them.
- `decide_wallet_position_action` returns `FORCE_PAPER_EXIT` when `dominant_side_status == DISTRIBUTION_ACTIVE`.
- `decide_wallet_position_action` returns `FORCE_PAPER_EXIT` when `chip_transfer_status == DISTRIBUTION_TO_COUNTERPARTY`.
- `EXIT_MONITOR` when current risk/pressure/structure score worsens versus entry by thresholds.

**Step 2:** Run target tests RED.

**Step 3:** Implement:
- Import `attach_wallet_factor_to_position` and `evaluate_wallet_change_for_open_position` if extracted to adapter.
- Or adapt existing functions to expose the same behavior.
- Preserve current no-real-swap scope notes.

**Step 4:** Run paper tests.

---

## Task 6: Verification and safety grep

**Objective:** Verify all modified paths compile, tests pass, and forbidden real-trade snippets are only guards/tests/scope text.

Run:

```bash
cd /root/sikk-gmgn
python3 -m pytest \
  tests/test_sikk_wallet_trade_adapter.py \
  tests/test_sikk_state_wallet_structure_integration.py \
  tests/test_sikk_candidate_state_machine.py \
  tests/test_run_sikk_gmgn_pipeline.py \
  tests/test_sikk_paper_live_runner.py -q

python3 -m pytest \
  tests/test_sikk_live_run.py \
  tests/test_sikk_wallet_structure_daily_report.py \
  tests/test_sikk_runtime_v02.py \
  tests/test_sikk_wallet_structure_snapshot.py \
  tests/test_sikk_same_source_grouping.py \
  tests/test_sikk_wallet_structure_gate.py \
  tests/test_sikk_candidate_wallet_structure_pipeline.py \
  tests/test_sikk_state_wallet_structure_integration.py \
  tests/test_sikk_orchestrator_wallet_structure_integration.py \
  tests/test_sikk_paper_wallet_structure_integration.py \
  tests/test_sikk_candidate_state_machine.py \
  tests/test_run_sikk_gmgn_pipeline.py \
  tests/test_sikk_paper_live_runner.py \
  tests/test_sikk_candidate_quote_security_pipeline.py -q

python3 -m py_compile \
  sikk_wallet_trade_adapter.py \
  sikk_candidate_state_machine.py \
  run_sikk_gmgn_pipeline.py \
  sikk_paper_live_runner.py \
  sikk_live_run.py

grep -R "庄家\|gmgn-cli swap\|gmgn-cli multi-swap\|gmgn-cli order strategy create\|order strategy create\|onchainos swap execute\|swap execute\|private key\|api key\|bot_token\|webhook_url" \
  sikk_wallet_trade_adapter.py \
  sikk_candidate_state_machine.py \
  run_sikk_gmgn_pipeline.py \
  sikk_paper_live_runner.py \
  tests/test_sikk_wallet_trade_adapter.py \
  tests/test_sikk_state_wallet_structure_integration.py \
  tests/test_run_sikk_gmgn_pipeline.py \
  tests/test_sikk_paper_live_runner.py | cat
```

Expected:
- tests pass
- compile pass
- grep matches only in safety guards, blacklists, tests, or scope statements
- no real execution path added

---

## Acceptance Criteria

- `wallet_structure_mode=off` 时状态机可恢复原本不使用钱包结构的运行。
- 默认 `observe` 时，`WALLET_BLOCK` 只记录 `would_block=true`，不把 `PAPER_READY` 改成 `BLOCKED`。
- `soft` 只阻断高置信钱包风险。
- `hard` 保留完整门禁行为。
- 缺失/过期 `wallet_structure_decision.json` 不崩溃；observe/soft 不阻断，hard 暂停。
- `token_status/candidate_states` 能看到 wallet gate 字段。
- paper positions 能看到钱包结构字段。
- 持仓中钱包结构恶化可触发 `EXIT_MONITOR` / `FORCE_PAPER_EXIT`，仍仅为纸面动作。
- 所有输出中文优先，明确“不执行真实 swap”。
