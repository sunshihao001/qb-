# HER_DOC Validator

Status: `VALIDATOR_ACTIVE`

## Purpose

The validator is the acceptance gate that prevents HER_DOC from being considered complete based on prose, intent, or queue creation alone.

It validates two layers:

1. **Project layer** — the HER_DOC control assets themselves.
2. **Bundle layer** — the output bundle produced by a full evidence-level scan.

## Supported Modes

### 1) Project mode

Validates that the HER_DOC project assets exist and contain the required control vocabulary.

Command:

```bash
python /root/sikk-gmgn/system/her_doc/HER_DOC_VALIDATOR.py project
```

### 2) Bundle mode

Validates a scan output directory contains the required matrix/report artifacts.

Command:

```bash
python /root/sikk-gmgn/system/her_doc/HER_DOC_VALIDATOR.py bundle /path/to/output_dir
```

## Validator Rules

- Missing file -> fail/block.
- Empty file -> fail.
- YAML parse error -> fail.
- Missing `schema_id` in schema YAML -> fail.
- Missing required project keywords -> fail.
- Missing required output artifacts -> fail.

## Output Contract

The script prints JSON with:

- `status`
- `project_dir` or `bundle_dir`
- `files_checked`
- `issue_count`
- `issues`

## Relation to HER_DOC Flow

Sequence:

```text
HER_DOC constitution
-> HER_DOC protocol
-> HER_DOC schemas
-> HER_DOC skill
-> HER_DOC validator
-> full trading system deep scan
```

Do not move to the deep scan until the validator exists and passes project validation.
