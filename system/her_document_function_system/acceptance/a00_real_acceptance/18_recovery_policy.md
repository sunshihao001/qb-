# A00 Real Acceptance Recovery Policy

- Missing O00 pipeline_run: BLOCKED, return to O00.
- Missing V00 validation evidence bundle: BLOCKED, return to V00.
- Missing R00 binding evidence bundle: BLOCKED, return to R00.
- Missing trace/audit: READY_WITH_GAPS only if evidence exists; otherwise BLOCKED when required evidence cannot be audited.
- Hidden gap detected: BLOCKED and route to U00/G00.
- Any live/signing/deploy/trading request: HARD_BLOCK.
