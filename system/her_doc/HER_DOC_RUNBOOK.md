# HER_DOC Professional Runbook

Status: `RUNBOOK_ACTIVE`
Version: `HER_DOC_PROFESSIONAL_CONTROL_V1`

## 1. Purpose

This runbook defines how to operate HER_DOC as a professional control project.
HER_DOC transforms documents/research/legacy assets/system files into system
function assets, evidence requirements, gap queues, build queues, runtime binding
reviews, and downstream handoff packets.

## 2. Universal Pre-Flight

Default cognition: **manual-scan-only**.

- A generic HER_DOC run, document intake, skill/system cognition change, targeted fix, assetization, queue generation, or runtime-binding review does **not** require automatic full-system scanning.
- Do not run repository-wide scans, system rescans, deep scans, or broad inventory unless the user explicitly requests scanning.
- Prefer targeted reading of the relevant protocol/schema/skill/file.
- If broader scanning may help, list it as an optional next step.

Before any explicitly requested HER_DOC scan/rescan/deep scan run:

```bash
python /root/sikk-gmgn/system/her_doc/HER_DOC_VALIDATOR.py project
```

Required:

```json
{"status":"PASS","issue_count":0}
```

If it fails, return `BLOCKED_VALIDATOR_PROJECT_GATE` and stop.

## 3. Operating Modes

### 3.1 Scan-only Mode

Use when the goal is to understand current assets and gaps.

Outputs:

- document passports;
- functional object registry;
- system mapping;
- evidence requirements;
- gap classification;
- queues;
- blocker matrices;
- report.

Forbidden:

- building system logic;
- modifying trading runtime;
- claiming runtime readiness.

### 3.2 Assetization Mode

Use when source material should be prepared for K00/K-system intake.

Outputs:

- document passport;
- functional object registry;
- system mapping matrix;
- K00 assetization queue;
- blocked/accepted status.

Rule:

Research is candidate-only until governance/K00 acceptance exists.

### 3.3 Runtime Binding Review Mode

Use when the question is whether R00, CPO, phase runners, or paper runtime can call a path safely.

Allowed:

- static entrypoint discovery;
- import checks;
- safe `--dry-run`;
- inert `--paper-only` fixture;
- replay-only historical fixture;
- trace validation.

Forbidden:

- real buy/sell/swap/transfer;
- private key access;
- signing;
- broadcast;
- auto order;
- auto deploy.

Outputs:

- runtime binding verification matrix;
- blocker matrix;
- safe proof refs or explicit blockers.

### 3.4 Legacy Absorption Mode

Use for old scripts/data/reports/GPT research.

Outputs:

- legacy script absorption matrix;
- legacy data replay matrix;
- legacy research assetization matrix;
- pollution guards;
- target route.

Rule:

Legacy asset existence is not current capability.

### 3.5 Queue-generation Mode

Use when the system has known gaps but should not be modified yet.

Outputs:

- GPT research queue;
- HER build queue;
- runtime binding review queue;
- stage completion queue;
- K00 assetization queue.

Rule:

Queue created does not mean work completed.

### 3.6 Bundle Validation Mode

After writing a scan output bundle:

```bash
python /root/sikk-gmgn/system/her_doc/HER_DOC_VALIDATOR.py bundle <output_dir>
```

If pass:

- artifact completeness is verified.

If fail:

- keep bundle;
- mark `BLOCKED_VALIDATOR_BUNDLE_GATE`;
- do not claim output complete.

Bundle pass does not prove runtime readiness.

## 4. Standard Output Directory Rules

- HER_DOC project control files: `/root/sikk-gmgn/system/her_doc/`
- HER_DOC scan outputs: `/root/sikk-gmgn/reports/<scan_id>/`
- Long task state: `/root/sikk-gmgn/research_loop/state/<task_id>/`
- External imports: `/root/sikk-gmgn/imports/staging/<import_id>/`

Do not write random scan outputs in project root.

## 5. Minimum Final Response Sections

Every HER_DOC task final response must include:

1. files created/updated;
2. validator project gate result;
3. validator bundle gate result if applicable;
4. evidence verified;
5. gaps preserved;
6. queues created;
7. claims not made;
8. next exact invocation.

## 6. Professional Overclaim Guard

Never claim:

- full completion;
- runtime accepted;
- production ready;
- live enabled;
- trading ready;
- stable CPO;
- R00 ready;
- P09 ready;
- P10 ready;
- paper-only ready;

unless required E4/E5 evidence exists.
