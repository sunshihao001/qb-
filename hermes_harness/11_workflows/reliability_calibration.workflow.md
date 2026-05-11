# Reliability Calibration Workflow

Route: `hermes_reliability_calibration_layer`

## Workflow

1. Intake problem and optional prior run directory.
2. Record expected outcome.
3. Record observed outcome.
4. Link evidence artifacts.
5. Compute calibration delta.
6. Classify error type and judgment error rate trend.
7. Write benchmark update.
8. Write rule adjustment candidate.
9. Review memory candidate lifecycle.
10. Set revalidation window.
11. Write next-run bias correction.
12. Generate reliability calibration report.

## Exit states

- `improve` — observed evidence supports reduced error risk.
- `hold` — no meaningful delta, continue existing rules.
- `degrade` — observed outcome contradicts expected reliability improvement.
- `needs_revalidation` — current evidence is insufficient or dry-run-only.
