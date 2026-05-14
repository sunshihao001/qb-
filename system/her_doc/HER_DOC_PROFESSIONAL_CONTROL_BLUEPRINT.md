# HER_DOC Professional Control Project Upgrade Blueprint

Status: `UPGRADE_BLUEPRINT_ACTIVE`
Version: `HER_DOC_PROFESSIONAL_CONTROL_V1`
Scope: `/root/sikk-gmgn/system/her_doc/`

## 1. Re-definition

HER_DOC is not a report writer and not a simple document reader.

HER_DOC is a **document-to-system-function control project**.

Its mission is to convert the following inputs:

- documents;
- GPT research;
- methodology notes;
- old scripts;
- old data;
- old reports;
- current system files;
- operator goals;

into file-backed, auditable, schedulable, verifiable, replayable, and upgradeable system assets:

- system goals;
- phase controllers;
- fields;
- schemas;
- contracts;
- runners;
- trace requirements;
- acceptance gates;
- handoff contracts;
- runtime binding reviews;
- R00 validation tasks;
- P09 replay fields;
- P10 upgrade candidates;
- GPT research queues;
- HER build queues;
- legacy absorption records.

## 2. Core Doctrine

```text
Document is not the final knowledge store.
Document is the source material for system function assets.

Research is not a summary.
Research must become fields, rules, schemas, contracts, runners, acceptance, replay fields, and upgrade candidates.

Scan is not a report.
Scan must produce evidence matrices, gap matrices, research queues, build queues, runtime blockers, and handoff packets.
```

## 3. Professional Control Chain

The professional HER_DOC chain is:

```text
UNSTRUCTURED_SOURCE
  -> DOCUMENT_PASSPORT
  -> FUNCTIONAL_OBJECT
  -> SYSTEM_MAPPING
  -> EVIDENCE_REQUIREMENT
  -> GAP_CLASSIFICATION
  -> QUEUE_ROUTING
  -> BUILD_OR_RESEARCH_PACKET
  -> SAFE_RUNTIME_BINDING_REVIEW
  -> ACCEPTANCE_OR_BLOCKER
  -> P09_REPLAY_OR_P10_UPGRADE_INPUT
```

Every step must produce a file-backed artifact.
Chat understanding is not state.

## 4. HER_DOC Control Objects

HER_DOC must recognize and create these object classes:

1. `GOAL_OBJECT`
   - Converts natural-language goals into system-targeted goal statements.
   - Required fields: goal_id, scope, target_phase_or_plane, final_decision_relevance, evidence_level.

2. `FUNCTIONAL_OBJECT`
   - Extracted implementable/reviewable function from source material.
   - Examples: field, rule, calculation, schema candidate, gate rule, replay field.

3. `SYSTEM_ASSET_CANDIDATE`
   - Candidate that may become code/schema/contract/runner/test.
   - Never accepted without build or governance evidence.

4. `EVIDENCE_REQUIREMENT`
   - Defines what proof is needed for each claim.
   - Must include required_evidence_level and verification method.

5. `GAP_OBJECT`
   - Explicit missing piece.
   - Must answer: what is missing, why it matters, where it belongs, who should handle it.

6. `GPT_RESEARCH_TASK`
   - Used when method, model, field semantics, evidence/counter-evidence, hard negative, gate logic, replay logic, or upgrade logic is not mature enough.

7. `HER_BUILD_TASK`
   - Used when the target is clear enough to create/update schema, contract, runner binding, trace, acceptance, handoff, or validator.

8. `RUNTIME_BINDING_REVIEW_TASK`
   - Used when callability, R00 integration, paper-only invocation, runner safety, idempotency, or output routing is uncertain.

9. `LEGACY_ABSORPTION_TASK`
   - Used for old scripts/data/reports/GPT outputs.
   - Must be read-only first.

10. `HANDOFF_PACKET`
    - Required before downstream modules consume HER_DOC results as accepted input.

## 5. Evidence Ladder

HER_DOC must never claim above available proof:

- `E0_NONE`: no evidence.
- `E1_DECLARED`: text declares it.
- `E2_FILE_EXISTS`: path exists and is readable.
- `E3_FILE_READ_OR_SCHEMA_VALID`: content/schema parsed or static validation passed.
- `E4_SAFE_RUNTIME_PROOF`: import/dry-run/paper-only/replay proof passed.
- `E5_ACCEPTED_HANDOFF`: downstream acceptance packet cites the proof.

## 6. Queue Routing Rules

Route every unresolved object to exactly one primary route and optional secondary routes:

- `GPT_RESEARCH_FIRST`: methodology, market model, field semantics, evidence/counter-evidence, hard negative, gate meaning, replay/upgrade logic.
- `HER_BUILD_DIRECT`: clear schema/contract/runner/trace/acceptance/handoff/validator work.
- `RUNTIME_BINDING_REVIEW`: R00 callability, paper-only runner, safe runtime proof, CPO stability, idempotency, failure recovery.
- `LEGACY_ABSORPTION`: old scripts, old data, old reports, old GPT outputs.
- `K00_ASSETIZATION`: research that may become formal knowledge asset.
- `STAGE_COMPLETION`: phase wrapper/completeness gap.
- `BLOCKED_BY_SAFETY`: anything touching signing, broadcast, real trade, auto order, or auto deploy.

## 7. Professional HER_DOC Deliverables

A professional HER_DOC run should create or update:

- `document_passport_matrix.yaml`
- `functional_object_registry.yaml`
- `system_mapping_matrix.yaml`
- `evidence_requirement_matrix.yaml`
- `phase_file_evidence_matrix.yaml`
- `gap_classification_matrix.yaml`
- `gpt_research_queue.yaml`
- `her_build_queue.yaml`
- `runtime_binding_verification_matrix.yaml`
- `r00_runtime_blocker_matrix.yaml`
- `legacy_script_absorption_matrix.yaml`
- `legacy_data_replay_matrix.yaml`
- `legacy_research_assetization_matrix.yaml`
- `handoff_packet.yaml` when downstream acceptance exists
- `validator_project_gate_result.json`
- `validator_bundle_gate_result.json`
- human report only after matrices exist

## 8. Upgrade Gaps in Current HER_DOC Project

Current HER_DOC already has constitution, execution protocol, schemas, safe runtime rules, overclaim guard, validator, and bundle gate.

Still missing or weak as a professional control project:

1. `HER_DOC_CONTROL_OBJECT_REGISTRY.yaml`
   - A canonical registry of all object classes and required fields.

2. `HER_DOC_PROFESSIONAL_CONTROL_BLUEPRINT.md`
   - This document; defines HER_DOC as a control project, not a report process.

3. `HER_DOC_GAP_CLASSIFICATION_SCHEMA.yaml`
   - A schema for missing pieces with owner route, severity, target path, evidence level, and acceptance.

4. `HER_DOC_HANDOFF_PACKET_SCHEMA.yaml`
   - A schema for downstream accepted handoff.

5. `HER_DOC_RUNBOOK.md`
   - Exact operator execution modes: scan-only, assetization, runtime-binding-review, legacy-absorption, queue-generation, bundle-validation.

6. `HER_DOC_PROJECT_MATURITY_MATRIX.yaml`
   - Project self-assessment: concept/document/process/control/runtime/handoff maturity.

7. Stronger validator checks for optional professional artifacts.
   - Current validator checks required core artifacts only.
   - Upgrade should add a professional mode later, not break existing project gate now.

## 9. Safety Boundary

HER_DOC may:

- read files;
- create control documents/schemas under `/root/sikk-gmgn/system/her_doc/`;
- create scan reports under `/root/sikk-gmgn/reports/`;
- parse YAML/JSON/Markdown;
- run project/bundle validators;
- run safe dry-run/replay validators if explicitly scoped.

HER_DOC must not:

- perform real trading;
- read/write private keys;
- sign transactions;
- broadcast transactions;
- auto order;
- auto deploy;
- treat research or reports as accepted runtime rules.

## 10. Success Definition

HER_DOC becomes a professional control project when it can consistently answer:

1. What source did this claim come from?
2. What function object was extracted?
3. Which system phase/plane consumes it?
4. What evidence level supports it?
5. What is missing?
6. Should the gap go to GPT, HER, runtime review, legacy absorption, K00, or stage completion?
7. What file must be built next?
8. What validator or safe runtime proof is required?
9. What downstream handoff is allowed or blocked?
10. What claims are explicitly not made?
