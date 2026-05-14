# Source Registry

## 1. 目的

Source Registry 用于登记 Source & Wallet Intelligence Bot 认可的事实源、标准化源、历史导入源与展示/复盘源，并定义每个数据源的可信度等级与禁反推规则。

## 2. 数据源等级

### L0：链上原始事件
- 说明：最底层事实事件，如 swap、transfer、mint、burn、pool create、LP add/remove。
- 用途：事实源首选。
- 约束：只记录客观链上时间和事件，不做结论。

### L1：GMGN / OKX / 钱包接口返回
- 说明：GMGN、OKX、钱包/地址/API 返回的结构化数据。
- 用途：可作为事实源，但必须保留 provider_timestamp 与 raw_response_path。
- 约束：不得用 dashboard/paper/report 反推其时间锚点。

### L2：SIKK normalized 标准产物
- 说明：由 Source Bot 标准化后的输出。
- 用途：可作为标准事实层，用于后续结构模型。
- 约束：必须保留 source_time、retrieved_at、normalized_at。

### L3：旧系统压缩包 / 历史 summary
- 说明：旧任务包、历史摘要、复盘归档。
- 用途：只能作为历史样本、导入样本、证据补充。
- 约束：不能覆盖实时事实源。

### L4：dashboard / paper / report / case file
- 说明：展示层、纸面层、报告层、案例层输出。
- 用途：只可用于展示、复盘、审计。
- 约束：不能反向生成事实字段。

## 3. 禁止规则

- dashboard 不能反推 discovered_at
- paper entry_time 不能反推 token_open_time
- report 不能反推 quote_time
- case file 不能反推 wallet_snapshot_time
- 旧 state_machine 不能进入新状态机
- 旧 paper/report 结果不能覆盖实时数据

## 4. Source Registry 与 Source Manifest 的关系

- Source Registry：定义数据源类别、等级、可信度与边界。
- Source Manifest：记录每次请求/响应的具体运行痕迹。

两者配合使用：
- Registry 决定某类数据能不能进入事实层。
- Manifest 记录该次调用是否成功、何时发生、原始响应存放在哪里。

## 5. 可信度原则

- L0 通常最高。
- L1 在保留 provider_timestamp 与 raw_response_path 时可作为强事实。
- L2 是经过标准化后的事实产物。
- L3 只能做历史参考。
- L4 只能做展示/复盘/审计。

## 6. 适用范围

本 Registry 适用于：
- candidates_normalized
- kline_normalized
- quote_security_normalized
- wallet_structure_normalized
- source_manifest
- first_seen_registry
- same-source evidence
- backflow / funding / transfer evidence
