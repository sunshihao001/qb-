# HER_DOC Overclaim Guard

## Purpose

Prevent HER_DOC from upgrading a document, report, plan, queue, old asset, or dry-run into a stronger state than evidence supports.

## Mandatory Guard Checks

Before final response or handoff, answer each with evidence refs:

1. Did we call a report an execution artifact?
2. Did we call a plan implemented without code/test/runtime evidence?
3. Did we call a queue item completed without result evidence?
4. Did we call path existence runtime binding?
5. Did we call dry-run live readiness?
6. Did we imply P09 review readiness without replay proof?
7. Did we imply P10 upgrade readiness without governance/acceptance proof?
8. Did we hide missing fields, gaps, failed checks, or legacy uncertainty?
9. Did we use chat memory as evidence without a file-backed artifact?
10. Did we treat old GPT research as accepted system rule?

Any yes without explicit accepted exception -> downgrade or block.

## Required Final Language

Use:

- `created/updated` only for files actually written;
- `verified` only for checks actually run;
- `queued` only for unresolved work in a queue artifact;
- `blocked` when required evidence or safety gate is missing;
- `not claimed` for readiness not proven.

Do not use these unless downstream evidence proves them:

- fully complete;
- runtime accepted;
- production ready;
- live enabled;
- trading ready;
- stable CPO;
- R00 ready;
- P09 ready;
- P10 ready.
