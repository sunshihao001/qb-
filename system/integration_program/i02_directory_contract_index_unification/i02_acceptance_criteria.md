# I02 Acceptance Criteria

## I02_READY
All 18 required output records exist, parse, and no blocking safety violation is detected. I03 prerequisite and I02→I03 handoff exist.

## I02_READY_WITH_GAPS
Core indexes and handoff exist, but non-blocking gaps remain such as missing optional artifacts, partial legacy mapping, or naming inconsistencies.

## I02_BLOCKED
Any safety hard negative appears: live execution, wallet signing, paper runtime start, auto deploy, business logic mutation, legacy deletion/migration by I02.

## I02_REJECTED
No usable source/index inputs exist or required output contracts cannot be built.
