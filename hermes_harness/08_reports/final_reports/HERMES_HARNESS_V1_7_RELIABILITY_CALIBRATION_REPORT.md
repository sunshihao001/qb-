# HERMES HARNESS V1.7 RELIABILITY CALIBRATION FINAL REPORT

## 升级结论

已将 Hermes Harness 从 V1.6 `judgment governance` 推进到 V1.7 `reliability calibration`。

V1.7 的核心不是“再加一个检查表”，而是让 Hermes 形成跨轮可靠性校准：

```text
expected outcome
→ observed outcome
→ calibration delta
→ judgment error rate
→ benchmark update
→ rule adjustment candidate
→ memory candidate review
→ revalidation window
→ next-run bias correction
```

## 新能力

- 新增 route: `hermes_reliability_calibration_layer`
- 新增 hook: `reliability_calibration_hook`
- 新增目录: `16_reliability_calibration/`
- 新增 runner: `09_scripts/hermes_reliability_calibration_run.py`
- runtime hook 已从 V1.4/V1.6 继续升级，状态版本写入 `v1.7`

## 已落地文件

- `HERMES_HARNESS_V1_7_RELIABILITY_CALIBRATION_LAYER.md`
- `01_control_plane/reliability_calibration_policy_v1_7.md`
- `11_workflows/reliability_calibration.workflow.md`
- `16_reliability_calibration/README.md`
- `16_reliability_calibration/templates/reliability_calibration_state_template.json`
- `09_scripts/hermes_reliability_calibration_run.py`
- `06_verification/tests/test_reliability_calibration.py`
- `06_verification/HERMES_HARNESS_V1_7_RELIABILITY_CALIBRATION_VERIFICATION_REPORT.md`
- `README.md` V1.7 section updated

## 验证结果

```text
10 passed in 0.30s
```

## 当前边界

V1.7 已完成“校准链路可运行”的系统升级；但真实可靠性提升需要后续真实任务的跨轮 expected-vs-observed 数据来证明。

因此本次 calibration decision 保持为：`needs_revalidation`。
