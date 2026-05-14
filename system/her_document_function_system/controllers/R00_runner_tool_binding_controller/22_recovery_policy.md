# R00 Recovery Policy

## missing V00 handoff
Status: R00_BLOCKED. Do not infer validation from chat context. Require V00 handoff packet path and validation evidence refs.

## validation not passed
Status: R00_BLOCKED. Return to V00 until acceptance is V00_ACCEPTED or allowed READY_WITH_GAPS with no blocking gaps.

## missing command contract
Status: DESIGN_ONLY or R00_BLOCKED. Create command contract before any runner binding.

## missing safe_mode or execution boundary
Status: R00_BLOCKED. Do not run dry-run until live runtime, wallet signing, auto deploy, and production trading are explicitly false.

## dry-run failed
Status: BINDING_FAILED. Preserve stdout, stderr, exit_code, generated/missing outputs, failure evidence, and required fix. Never convert failed binding to passed.

## missing generated output manifest
Status: NOT_EXECUTED or BINDING_FAILED. Binding cannot be BINDING_TESTED or R00_ACCEPTED.

## production risk detected
Status: R00_BLOCKED. Disable binding and escalate to governance boundary.

## Telegram / scheduler design confusion
Telegram binding is design-only until a separate bot integration is approved. Scheduler binding is disabled by default until explicit approval.
