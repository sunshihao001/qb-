# U00 Context Pack

## Role
U00 is the HER Review / Upgrade controller.

## Legal upstream inputs
- H00 handoff packet
- A00 evidence bundle
- phase status matrix
- gap reports
- failure evidence
- queue state
- trace logs
- audit logs

## Forbidden reads
- raw chat context as authoritative input
- direct production state mutation
- live runtime, wallet signing, auto deploy, production trading

## Output rule
U00 must transform evidence into upgrade candidates and handoff packets, not into self-proclaimed fixes.
