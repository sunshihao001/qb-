# HER P09 Execution Protocol

1. Read K00 handoff and P09 context.
2. Read P08/Paper Runtime review case handoff.
3. Build review case record.
4. Lock historical replay input snapshot.
5. Reconstruct P01-P08 decision chain.
6. Reconstruct paper runtime path.
7. Evaluate outcome.
8. Run failure attribution.
9. Run success attribution.
10. Detect missed opportunity / false positive / false negative.
11. Build calibration candidates.
12. Build P10 upgrade candidate data request.
13. Write P09 trace/report/acceptance.
14. Handoff only to P10.

Forbidden: current data overlay, direct rule mutation, threshold mutation, runtime patch, paper runtime start, live execution, wallet signing, order broadcast.
