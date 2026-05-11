# Reliability Calibration Policy V1.7

## Route

`hermes_reliability_calibration_layer`

## Purpose

V1.7 converts judgment governance into measured reliability feedback. It prevents Hermes from claiming that a new control layer improved reliability unless expected outcome and observed outcome are compared and the calibration delta is recorded.

## Mandatory gates

1. **expected outcome gate** — every calibration run must state what Hermes expected to happen.
2. **observed outcome gate** — every calibration run must state what actually happened or what was actually evidenced.
3. **calibration delta gate** — expected vs observed must produce a typed calibration delta.
4. **judgment error rate gate** — each delta must update a judgment error rate signal: improved, worsened, stable, or unknown.
5. **benchmark update gate** — non-zero deltas must produce or update a benchmark case for replay.
6. **rule adjustment gate** — system rules may be proposed as rule adjustment candidates, not silently promoted.
7. **memory candidate gate** — memory candidate review must block direct stable memory when evidence is dry-run only or single-run only.
8. **revalidation window gate** — every reliability claim needs a future revalidation window or trigger.
9. **next-run bias correction gate** — the next runtime loop must know which bias to correct: overconfidence, false completion, over-engineering, under-evidence, or memory contamination.

## Policy

- Do not treat V1.6 governance passing as proof of V1.7 reliability improvement.
- Do not treat a benchmark file as a solved benchmark.
- Do not promote rule adjustment candidates into stable memory without independent revalidation.
- Prefer small bias corrections over broad new control layers.
- Every calibration artifact must preserve the difference between dry-run evidence and real-world outcome evidence.
