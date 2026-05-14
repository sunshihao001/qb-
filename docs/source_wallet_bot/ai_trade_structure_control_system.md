# AI-Driven Trade Structure Control System

## 0. System Essence

This project is not a single wallet-analysis module.

It is an AI-driven trade-structure control engineering system built around the HER / Harness Engineering loop:

```text
Skill capability map
  → target system mapping
  → automatic gap discovery
  → automatic implementation completion
  → verification loop
```

The system must not rely on the model being "smart" in an unconstrained way. It must have:

- control plane
- execution loop
- permissions and boundaries
- recovery and rollback posture
- verification gates
- multi-agent role separation
- auditable skill/workflow modules

A skill is not a prompt. A skill is a verifiable workflow module with explicit inputs, outputs, permissions, failure modes, and tests.

---

## 1. Primary Root and Layer Boundary

The professionalized wallet-structure / new-token structure-analysis main root is:

```text
/root/sikk-gmgn/
```

Primary wallet-structure data root:

```text
/root/sikk-gmgn/data/source_wallet_bot/<mode>/<token_address>/
```

Primary implementation roots:

```text
/root/sikk-gmgn/modules/source_wallet_bot/
/root/sikk-gmgn/modules/wallet_structure/
```

Primary methodology / rule / model root:

```text
/root/sikk-gmgn/research_loop/methodology/
```

Wallet-Intel remains the collaboration/orchestration/inference workspace:

```text
/root/sikk-wallet-intel/
```

It may read or copy standard fact packages from `/root/sikk-gmgn`, but it is not the primary root for new wallet-structure data, code, or methodology.

---

## 2. Core System Goal

When a new token appears, the system should execute a controlled pipeline:

```text
new token appears
  → call available skills to fetch available data
  → exclude security hard risks
  → exclude market hard risks
  → build early wallet facts
  → identify suspected structural wallets / same-source execution groups
  → identify first control-box / accumulation range
  → judge whether early structural funds have completed distribution
  → judge whether there is still second-push / second-expansion motivation
  → combine K-line, momentum, cost zone, strategy methods, wallet holdings, lifecycle
  → output: excluded / recorded / risk-monitor / watch / paper-entry / live-candidate
```

The core purpose is **not** "find the dealer and buy".

The system answers:

1. Has this token passed security and market hard gates?
2. Does early structural capital actually exist?
3. Has structural capital not fully distributed yet?
4. Is the current trend still controlled or influenced by the structural side?
5. Does current participation have acceptable risk/reward?
6. Would the user become exit liquidity for the structural side?

---

## 3. System Layers

### Layer 1 — Skill Capability Map

Purpose: know what the system can currently do.

Assets:

- available skills
- modules
- scripts
- data collectors
- quantitative calculators
- validators
- report writers
- orchestration runners

Outputs:

```text
skill_capability_map.json
skill_to_target_system_map.json
missing_capability_report.md
```

Required fields per skill/module:

- capability name
- input contract
- output contract
- required data
- permissions
- forbidden side effects
- current implementation path
- tests
- verification command
- known gaps

### Layer 2 — Target System Mapping

Purpose: map the desired new-token decision chain to actual capabilities.

Target chain:

1. token discovery
2. quote/security collection
3. market hard-risk gate
4. wallet raw data collection
5. wallet normalization
6. wallet fact package
7. same-source group detection
8. cost-zone calculation
9. chip inventory and distribution progress
10. control-box / K-line structure detection
11. lifecycle / second-expansion motivation
12. risk-reward / exit-liquidity risk judgment
13. output state classification

Each target must map to:

- input files
- source module
- output files
- acceptance criteria
- fallback behavior
- verification command

### Layer 3 — Automatic Gap Discovery

Purpose: detect what is missing before the model invents conclusions.

Gap types:

- missing input file
- missing field
- missing collector
- missing normalizer
- missing calculator
- missing test
- missing output contract
- missing manifest
- missing permission boundary
- missing fallback
- stale or conflicting directory route

Gap output:

```text
research_loop/state/<task_id>/gap_scan.json
research_loop/state/<task_id>/gap_priority.md
```

Rules:

- Missing evidence must produce downgraded status.
- Missing data must not be filled with behavior assumptions.
- Gap reports should generate implementation tasks, not final trading claims.

### Layer 4 — Automatic Implementation Completion

Purpose: convert gaps into small, testable implementation tasks.

Task package fields:

- task id
- capability gap
- target module
- target test
- output contract affected
- forbidden side effects
- acceptance criteria
- rollback note

Allowed implementation roots:

```text
/root/sikk-gmgn/modules/source_wallet_bot/
/root/sikk-gmgn/modules/wallet_structure/
/root/sikk-gmgn/tests/
/root/sikk-gmgn/research_loop/methodology/
```

Forbidden for wallet-structure implementation:

```text
/root/sikk-wallet-intel/ as primary wallet-structure code root
/root/sikk-gmgn/data/gmgn_candidates_live_run/ as new main write path
trading / swap / signing / broadcast modules
```

### Layer 5 — Verification Loop

Purpose: every capability must be verified before being treated as active.

Verification includes:

- unit tests
- focused integration tests
- fixture replay
- output schema validation
- path/layout audit
- manifest completeness
- forbidden-output scan
- no trading side effects

Verification outputs:

```text
research_loop/acceptance/<task_id>_acceptance.md
research_loop/state/<task_id>/verification.json
```

---

## 4. Domain Decision Pipeline

### Phase 0 — Discovery / Intake

Input:

- new token address
- GMGN link
- candidate feed item
- manual `ca <token>` request

Output:

```text
manifest/token_intake.json
```

Decision:

- valid token
- invalid token
- duplicate token
- insufficient token metadata

### Phase 1 — Security Hard-Risk Gate

Purpose: exclude tokens that fail hard security criteria.

Examples:

- honeypot / cannot sell evidence
- owner/mint/freeze risks when available
- LP or liquidity abnormality
- suspicious contract flags
- malicious token metadata
- severe quote/security failure

Output classes:

```text
SECURITY_EXCLUDED
SECURITY_MONITOR
SECURITY_PASS_WITH_WARNINGS
SECURITY_PASS
```

### Phase 2 — Market Hard-Risk Gate

Purpose: exclude tokens where market conditions invalidate structure analysis or participation.

Examples:

- liquidity too thin
- spread too high
- slippage too high
- volume fake or too low
- market cap / liquidity mismatch
- extreme one-candle move with no support
- quote instability

Output classes:

```text
MARKET_EXCLUDED
MARKET_MONITOR
MARKET_PASS_WITH_WARNINGS
MARKET_PASS
```

### Phase 3 — Early Wallet Fact Construction

Purpose: build reliable wallet facts before behavior inference.

Canonical output root:

```text
/root/sikk-gmgn/data/source_wallet_bot/<mode>/<token>/
```

Required outputs:

```text
wallet_data/raw/
wallet_data/normalized/
structure_analysis/wallet_fact/wallet_structure_normalized.json
structure_analysis/wallet_fact/chip_distribution_summary.json
structure_analysis/wallet_fact/same_source_groups.json
structure_analysis/wallet_fact/fund_flow_edges.csv
structure_analysis/wallet_fact/address_history.json
```

### Phase 4 — Structural Wallet / Same-Source Execution Groups

Purpose: identify whether early structural capital exists.

Questions:

- Are early buyers related?
- Are execution wallets funded similarly?
- Are token receivers part of a distribution pattern?
- Are there historical repeat wallets?
- Are there coordinated buy/sell windows?

Output:

```text
structure_analysis/intelligence/same_source_evidence_normalized.json
structure_analysis/intelligence/structure_evidence_pack.json
```

### Phase 5 — First Control Box / Accumulation Range

Purpose: detect the first structural box where early control occurred.

Inputs:

- K-line
- early wallet buys/sells
- volume bands
- dominant cost zone
- same-source group entry range

Outputs:

```text
structure_analysis/intelligence/control_box.json
structure_analysis/intelligence/cost_zone_alignment.json
```

### Phase 6 — Distribution Completion / Inventory State

Purpose: determine whether early structural capital has already distributed.

Key metrics:

- structure_inventory_remaining_pct
- distribution_progress_score
- dominant_cost_deviation_rate
- realized/unrealized PnL by structural wallets
- high-result wallet holding status

Output classes:

```text
INVENTORY_UNKNOWN
INVENTORY_RETAINED
INVENTORY_PARTIAL_DISTRIBUTION
INVENTORY_MOSTLY_DISTRIBUTED
INVENTORY_EXITED
```

### Phase 7 — Second-Push / Second-Expansion Motivation

Purpose: judge whether there is still structural motivation to continue.

Inputs:

- inventory remaining
- dominant cost zone
- current price relative to cost
- counterparty pressure
- K-line momentum
- wallet reactivation
- new same-source buys
- control-box defense

Output classes:

```text
NO_EVIDENCE_OF_SECOND_PUSH
SECOND_PUSH_WATCH
SECOND_PUSH_POSSIBLE
SECOND_EXPANSION_STRUCTURE_PRESENT
```

### Phase 8 — Combined Structure-Risk Decision

Purpose: produce the final non-execution classification.

Allowed outputs:

```text
EXCLUDED
RECORDED
RISK_MONITOR
WATCH
PAPER_ENTRY_CANDIDATE
LIVE_CANDIDATE
```

Forbidden outputs:

```text
BUY_NOW
SELL_NOW
OPEN_POSITION
CLOSE_POSITION
GUARANTEED_PROFIT
CONFIRMED_DEALER
```

---

## 5. Control Plane

The control plane owns:

- task identity
- phase state
- permissions
- input/output route validation
- recovery checkpoints
- agent assignments
- verification status
- forbidden side-effect scans

Control files:

```text
research_loop/state/<task_id>/loop_state.json
research_loop/state/<task_id>/phase_lock.json
research_loop/state/<task_id>/permissions.json
research_loop/state/<task_id>/recovery_checkpoint.json
research_loop/state/<task_id>/verification.json
```

Principles:

- one task id per target token/run
- one active phase at a time
- phase cannot advance without required artifacts
- failed phases produce recovery tasks
- verification failure blocks activation

---

## 6. Multi-Agent Role Separation

### Orchestrator

Owns:

- task ticket
- phase routing
- assignment
- file existence checks
- field completeness checks
- summary

Does not own:

- wallet fact fabrication
- behavior inference fabrication
- trading decisions

### Skill-Capability Auditor

Owns:

- skill inventory
- capability map
- target mapping
- gap detection

### Wallet-Fact Worker

Owns:

- raw collection
- normalization
- wallet fact package
- missing fact report

### Structure-Quant Worker

Owns:

- cost zone
- inventory
- distribution progress
- same-source quantitative scoring
- counterparty pressure

### Market/K-Line Worker

Owns:

- K-line context
- momentum
- control box
- market hard-risk gate

### Behavior-Inference Worker

Owns:

- lifecycle inference
- second-push motivation inference
- explanation report
- evidence level / downgrade

### Verification Worker

Owns:

- tests
- schema validation
- output contract checks
- no-side-effect scan

---

## 7. Skill as Verifiable Workflow Module

Every skill should be represented as a workflow module:

```json
{
  "skill_name": "...",
  "capabilities": ["..."],
  "inputs": ["..."],
  "outputs": ["..."],
  "allowed_paths": ["..."],
  "forbidden_paths": ["..."],
  "permissions": ["read", "write", "test"],
  "forbidden_side_effects": ["swap", "sign", "broadcast", "private_key", "state_machine_trade_gate"],
  "verification": {
    "tests": ["..."],
    "schema_checks": ["..."],
    "sample_fixture": "..."
  },
  "known_gaps": ["..."],
  "recovery": ["..."]
}
```

Skills must be callable, auditable, and verifiable. They should not only be prose prompts.

---

## 8. Final Interpretation

This system is a trade-structure intelligence and control system.

It can classify tokens into:

- excluded
- recorded
- risk monitor
- watch
- paper-entry candidate
- live candidate

But those are **control states**, not automatic execution orders.

The highest-level risk question is:

```text
Are we identifying a still-active structural opportunity, or are we becoming exit liquidity for already-distributed structural capital?
```
