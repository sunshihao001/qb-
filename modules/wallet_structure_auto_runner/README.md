# Wallet Structure Auto Runner L3 子模块

## 定位

本模块是钱包结构分析系统的 L3 自动运行器包装层。

它把旧入口：

```text
sikk_wallet_structure_auto_runner.py
```

升级为稳定公共 API：

```python
from modules.wallet_structure_auto_runner import run_wallet_structure_auto_task
```

## 边界

- 只读采集。
- 只做钱包结构自动任务编排。
- 写 checkpoint、manifest、guard trend index、system audit 引用。
- 不执行真实交易。
- 不签名。
- 不广播。
- 不读取私钥。
- 不把 WALLET_SUPPORT 当作交易许可。

## HER 位置

```text
Goal
→ Auto Runner
→ Source Wallet Bot
→ Wallet Data Guard
→ Wallet Structure Gate
→ System Audit
→ Acceptance
```

## 标准输出

- `checkpoint/wallet_structure_auto_task_checkpoint.json`
- `manifest/wallet_structure_auto_task_manifest.json`
- `guard_index/wallet_data_guard_trend_index.json`
- `system_audit/wallet_structure_system_audit.json`
- `system_audit/wallet_structure_system_audit.md`

## 兼容策略

当前不移动旧根脚本，L3 模块只做 additive wrapper，保证旧测试、旧 CLI、旧调度入口继续可用。
