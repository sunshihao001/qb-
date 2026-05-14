# P07 Strategy Gate Context

生成时间：2026-05-12T04:08:53Z

P07 不是买入信号模块、策略打分模块、交易触发器、纸面交易启动器或实盘确认器。

P07 的唯一职责是：读取 P06 场景识别、P05 证据束、P04 筹码结构、P02 数据质量和 Governance 硬规则，输出 OBSERVE / PAUSE / BLOCK / PAPER_CANDIDATE / HUMAN_CONFIRMATION_REQUIRED / STRATEGY_GATE_REJECTED。

执行原则：
- 先 hard negative，后准入。
- UNKNOWN / CONFLICT / WEAK_USE_ONLY 不能默认通过。
- PAPER_CANDIDATE 只允许交给 P08 做执行前风控，不等于 PAPER_READY。
- 禁止 buy_signal、paper_runtime_started、live_execution_allowed。
- 每个裁决必须可复盘：证据、反证、风险、失效条件、P08 要求必须被记录。
