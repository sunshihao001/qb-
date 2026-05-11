---
artifact_type: control_policy
status: verified
version: v1.2
valid_until: null
---
# Interrupt Policy

## Purpose
Interrupts are formal runtime states, not user-experience issues.

After an interrupt, Hermes must preserve transcript/result consistency and close any open tool calls with synthetic results when needed.

## Interrupt States
- `USER_ABORTED`
- `SYSTEM_ABORTED`
- `TOOL_ABORTED`
- `RECOVERY_ABORTED`

## Required Interrupt Reports
All interrupt cases must write into:

`07_recovery/interrupt_reports/`

## Required Report Fields
- interrupt phase
- last action before interrupt
- whether unfinished tool calls exist
- whether synthetic results were added
- whether current state is recoverable
- next round entry

## Hard Rules
- Interrupts must be represented in runtime state.
- Do not continue pretending the task is still executing normally after an interrupt.
- If tool calls were left open, they must be synthetic-closed.
- Transcript and tool results must remain consistent.
- If the interrupt is unrecoverable, the task must move to recovery or blocked status.

## Recovery Consistency Rules
- A user abort does not erase runtime evidence.
- A system abort must annotate the reason and recovery entry.
- A tool abort must be paired with ledger closure.
- A recovery abort means the recovery path itself failed and must be reported distinctly.

## Status Mapping
- `USER_ABORTED` → user-driven stop
- `SYSTEM_ABORTED` → internal policy or state stop
- `TOOL_ABORTED` → tool failure or cancellation
- `RECOVERY_ABORTED` → recovery path failed or was stopped
