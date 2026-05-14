# i04 paper-only runtime integration context

Authority: DOC-20260512-I04_PAPER_RUNTIME_INTEGRATION_V1

I04 boundary: only integrate P08-allowed candidates into paper-only runtime, never mutate upstream strategy logic, never start live execution, never wallet sign, never auto deploy.

Acceptance anchors:
- I03 handoff read
- P08 handoff read
- paper runtime input manifest created
- permission gate created
- paper position, trade, equity, risk, exit, trace artifacts created
- P09 review replay input created
- I04 to I05 handoff created

Read order:
1. system_methodology_blueprint.md
2. professional_build_order.md
3. I03 to I04 handoff packet
4. I04 prerequisite packet
5. P08 to paper runtime handoff packet
6. paper runtime data request packet
7. path guard, trace writer, acceptance runner, handoff writer bindings
8. permission records, entry plans, quote/slippage/cost/invalidation/risk records
