# HER I02 Execution Protocol

1. Read K00 I02 handoff and task package.
2. Load I02 controller context and policies.
3. Declare canonical roots.
4. Scan P01-P10/I01/system/legacy paths without modifying them.
5. Build all indexes and reports.
6. Generate I03 prerequisite packet.
7. Generate I02→I03 handoff.
8. Run parse/path/safety verification.
9. Mark I02_READY or I02_READY_WITH_GAPS.

Forbidden: P11/P12, business logic mutation, runner implementation, paper runtime start, live execution, wallet signing, auto deploy, legacy deletion.
