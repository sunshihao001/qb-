# Hermes Harness V2.0 Verification

验证对象：Hermes Harness V2.0 混合式判断运行时系统。

## 验证清单

1. `17_control_registry` 存在：待自动测试确认。
2. `18_thread_rollout_state` 存在：待自动测试确认。
3. `19_exec_policy` 存在：待自动测试确认。
4. `20_context_budget` 存在：待自动测试确认。
5. `21_judgment_benchmark` 存在：待自动测试确认。
6. `22_anti_self_deception` 存在：待自动测试确认。
7. JSON / JSONL 文件格式合法：由 `test_hybrid_harness_v2.py` 读取解析确认。
8. 没有删除旧数据：本次为 copy/create/update-only，不执行删除旧目录。
9. 没有修改业务代码：范围限制在 `/root/sikk-gmgn/hermes_harness/`。
10. 没有触发真实交易：未调用交易/广播/GMGN swap/OKX execution 工具。
11. 没有读取密钥：exec policy 明确 R5 deny，未读取 `.env`/token/private key。
12. 没有伪造执行记录：V2 runner 将 dry-run 明确标记为 dry-run，边界写入 state bridge。

## 自动验证命令

```bash
cd /root/sikk-gmgn/hermes_harness
python3 -m pytest 06_verification/tests/test_hybrid_harness_v2.py -q
```

## 自动验证结果

```text
python3 -m pytest 06_verification/tests/test_hybrid_harness_v2.py -q
6 passed in 0.14s

python3 -m pytest 06_verification/tests/test_hybrid_harness_v2.py 06_verification/tests/test_reliability_calibration.py 06_verification/tests/test_runtime_hook_launcher.py 06_verification/tests/test_judgment_governance.py -q
16 passed in 0.44s
```

## V2.0 dry-run 结果

```json
{"status":"COMPLETED","route":"hermes_hybrid_judgment_runtime_v2","thread_id":"hermes.thread.20260509.020359","overall_passed":true,"boundary":"dry-run proves chain is runnable; not real cross-run reliability improvement"}
```

## 边界说明

本验证确认 V2.0 结构、策略、runner、thread/rollout/state bridge、benchmark 和 anti-self-deception 审计链路可运行；不声明真实跨轮可靠性已经提升。真实提升必须通过后续真实任务 benchmark/regression 数据证明。
