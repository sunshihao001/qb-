# Wallet Data Guard 子模块

## 定位

`modules/wallet_data_guard/` 是 SIKK 钱包分析项目的数据防污染保护子模块。

它不是新的钱包分析主系统，不替代：

```text
modules/source_wallet_bot
→ sikk_candidate_wallet_structure_pipeline.py
→ sikk_wallet_structure_gate.py
→ sikk_candidate_state_machine.py / sikk_live_run.py
```

## 目标

防止以下污染：

```text
raw/facts/evidence/inference/handoff/state/report 混层
推断回写事实
状态机回写钱包数据
handoff 当交易信号
compat 路线写 canonical decision
旧目录 fallback 缺 mapping_id
没有 source_refs 的 facts
```

## 子文件

```text
contracts.py             # 分层、producer、canonical/compat 路由合同
write_gate.py            # 受控写入门禁
source_manifest.py       # 数据来源护照生成与校验
contamination_scan.py    # 污染扫描器
```

## 基本原则

```text
raw ≠ fact
fact ≠ evidence
evidence ≠ inference
inference ≠ conclusion
handoff ≠ trade signal
compat ≠ canonical
memory ≠ truth
```

## 使用示例

```python
from modules.wallet_data_guard import SemanticLayer, ProducerType, write_controlled_artifact

write_controlled_artifact(
    path="data/source_wallet_bot/paper/<token>/wallet_data/raw/gmgn.json",
    layer=SemanticLayer.RAW,
    producer=ProducerType.COLLECTOR,
    payload={"rows": []},
    source_refs=["gmgn:holders"],
    task_passport="hermes_harness/02_task_intake/task_passport_wallet_data_guard_20260507_231233.md",
)
```

## 扫描示例

```python
from modules.wallet_data_guard import scan_wallet_data_contamination
report = scan_wallet_data_contamination("data")
```
