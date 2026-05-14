# U00 Recovery Policy

- Missing H00 handoff => block.
- Missing A00 evidence bundle => block.
- Missing root cause for failures => block.
- Missing queue item for upgrade candidate => downgrade to READY_WITH_GAPS.
- Missing governance candidate for policy-level risk => block or downgrade.
- Missing trace/audit => block.
- Never promote review text into applied upgrade status.
