# Stable Trader OS Phase Handoff Flow

```text
P00 constitution
→ P01 data fact
→ P02 wallet structure
→ P03 chip control
→ P04 scenario recognition
→ P05 structure position
→ P06 strategy gate
→ P07 execution risk
→ P08 review learning
→ P09 system upgrade
```

## Handoff Packet Required Fields

```json
{
  "phase": "Pxx",
  "token_address": "",
  "snapshot_id": "",
  "status": "READY_WITH_GAPS",
  "handoff_files": {},
  "allowed_next_stage": "Pxx",
  "hard_negatives": [],
  "missing": [],
  "degraded_gaps": [],
  "audit_refs": []
}
```

## Rule

Report files are presentation only. Downstream readers consume handoff packets and normalized JSON decisions.
