---
artifact_type: control_policy
status: verified
version: v1.2
valid_until: null
---
# Input Governance Queue Policy

## Purpose
Hermes must govern input before invoking the model or building task context.

## Required Queue
All inbound material must pass through `03_task_runtime/input_governance_queue.jsonl` before being copied into task context, memory, or passport fields.

## Input Questions
Every task start must answer:
- What type of input is this?
- Is it too long?
- Is it duplicated?
- Is it relevant to the current task?
- Is it a long-term rule?
- Is it temporary noise?
- Should it go into the task passport?
- Should it go into memory?
- Should it be discarded or summarized?

## Processing Order
1. Classify input type.
2. Detect duplication.
3. Check relevance.
4. Decide long-term vs temporary.
5. Decide passport, memory, summary, or discard.
6. Append the decision to the governance queue.
7. Only then assemble task context.

## Hard Rules
- Do not place all user input directly into task context.
- Clean first, then assemble.
- Long-term rules may be copied only after validation.
- Temporary noise must not be promoted to memory.
- Irrelevant or duplicate content should be summarized or dropped.
- Governance decisions must be audit-able.

## Required Record Fields
Each queue entry should record:
- task_id
- input_id
- input_type
- source
- length_class
- relevance_class
- duplicate_flag
- disposition
- target_surface
- timestamp
- reviewer

## Disposition Values
- passport
- memory
- context
- summary
- discard
- pending_review
