# HER_DOC Evidence-Level Execution Protocol

Status: `PROTOCOL_ACTIVE_WITH_VALIDATOR_GATE`

## Trigger Recognition

Use this protocol whenever the task says or implies:

- `HER_DOC`;
- 文档转系统;
- document-to-system;
- GPT 研究资料进入系统;
- legacy 资料吸收;
- runtime binding review;
- 不要只生成报告;
- 不要把解释性文档当落地。

Scan-specific triggers are **manual-only** and must not be inferred from generic HER_DOC use:

- evidence-level scan;
- full trading system deep scan;
- system_rescan / rescan;
- 用户明确说“扫描 / 全量扫描 / 深度扫描 / 我手动发扫描”。

If scan-specific wording is absent, stay in targeted document-to-system / assetization / queue / binding-review mode and do not run broad scans.

## Mandatory Execution Order

Do not jump directly to a final report. Execute in this order:

### HER_DOC-PRE Validator Project Gate

Before any explicitly requested HER_DOC full scan or business scan, run:

```bash
python /root/sikk-gmgn/system/her_doc/HER_DOC_VALIDATOR.py project
```

Required result:

```json
{"status": "PASS", "issue_count": 0}
```

If this gate fails, stop the scan and return `BLOCKED_VALIDATOR_PROJECT_GATE`.
Do not continue into business/system scanning when the HER_DOC control project itself is not valid.

Manual-scan-only rule:

- This validator gate is mandatory **only when a scan/rescan/deep-scan is explicitly requested**.
- Generic HER_DOC, document intake, skill update, targeted protocol edit, queue generation, or runtime-binding review does not authorize broad scanning.
- In non-scan tasks, inspect only the named/relevant protocol, schema, skill, or artifact needed for the requested change.

### HER_DOC-00 Scope and Safety Gate

Inputs:
- user goal;
- target root;
- allowed write paths;
- forbidden actions;
- validator project gate result.

Outputs:
- scope statement;
- safety boundary;
- run status seed;
- `validator_project_gate: PASS` evidence record.

Failure -> `BLOCKED_SCOPE_UNCLEAR`, `BLOCKED_FOR_LIVE_RISK`, or `BLOCKED_VALIDATOR_PROJECT_GATE`.

### HER_DOC-01 Input Asset Inventory

Classify sources using `HER_DOC_INPUT_TYPE_REGISTRY.yaml`.

Outputs:
- asset inventory or explicit missing-source record.

Inventory is not completion.

### HER_DOC-02 Document Passport

Each source or source group must have a document passport following `HER_DOC_DOCUMENT_PASSPORT_SCHEMA.yaml`.

Outputs:
- source identity;
- status;
- safety class;
- target phase/plane.

### HER_DOC-03 Functional Object Extraction

Extract implementable or reviewable objects following `HER_DOC_FUNCTIONAL_OBJECT_SCHEMA.yaml`.

Objects include goals, fields, schemas, contracts, runners, evidence rules, counter-evidence rules, risk rules, gate rules, replay fields, and upgrade rules.

### HER_DOC-04 System Mapping

Map each object to K00-K08, P00, control planes, P01-P10, I01-I05, R00, CPO, P09, or P10 using `HER_DOC_SYSTEM_MAPPING_SCHEMA.yaml`.

If mapping is uncertain, record `mapping_confidence: LOW` and route to research/review.

### HER_DOC-05 Evidence Requirement and Verification

For every claim, create evidence requirements using `HER_DOC_EVIDENCE_REQUIREMENT_SCHEMA.yaml`.

No claim can be stronger than its evidence level:

- `E0_NONE`
- `E1_DECLARED`
- `E2_FILE_EXISTS`
- `E3_FILE_READ_OR_SCHEMA_VALID`
- `E4_SAFE_RUNTIME_PROOF`
- `E5_ACCEPTED_HANDOFF`

### HER_DOC-06 Gap and Queue Routing

Route unresolved work:

- methodology/market/model uncertainty -> GPT research queue;
- clear schema/contract/runner/trace work -> HER build queue;
- runner/callability uncertainty -> runtime binding review;
- old scripts/data/reports/research -> legacy absorption;
- formal knowledge intake -> K00 assetization;
- stage wrappers/handoff/acceptance -> stage completion.

Queue creation is not completion.

### HER_DOC-07 Status, Guard, and Handoff

Compute status using `HER_DOC_COMPLETION_STATUS_RULES.md` and `HER_DOC_OVERCLAIM_GUARD.md`.

Write final packet/report only after evidence and queues exist.

### HER_DOC-POST Validator Bundle Gate

After an explicitly requested full scan writes its output directory, run:

```bash
python /root/sikk-gmgn/system/her_doc/HER_DOC_VALIDATOR.py bundle <output_dir>
```

Required result for artifact completeness:

```json
{"status": "PASS", "issue_count": 0}
```

If bundle validation fails:

- keep all generated artifacts;
- mark final status `BLOCKED_VALIDATOR_BUNDLE_GATE` or `HER_DOC_SCAN_OUTPUT_INCOMPLETE`;
- list missing/empty outputs from validator JSON;
- do not claim full scan completed.

If bundle validation passes but evidence coverage is below the status threshold, use the lower evidence status from `HER_DOC_COMPLETION_STATUS_RULES.md`.

## Required Final Response Sections

Every final response must separate:

- files created/updated;
- validator project gate result;
- validator bundle gate result, if applicable;
- evidence verified;
- gaps preserved;
- queues created;
- claims not made;
- next exact invocation.

## Safe Runtime Rule

Safe verification is allowed only as defined in `HER_DOC_SAFE_RUNTIME_VERIFICATION.md`. No live trading/signing/broadcast/deploy is allowed.
