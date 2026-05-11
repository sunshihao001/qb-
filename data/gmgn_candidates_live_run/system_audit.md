# SIKK 系统审计报告

- 审计时间：2026-05-03T08:34:51Z
- live run 根目录：`data/gmgn_candidates_live_run`
- 安全边界：只读审计；不采集、不交易、不签名、不广播。
- 当前候选数：50

## 模块统计
- candidates：success=0 failed=0 skipped=0
- kline：success=0 failed=0 skipped=0
- signals：success=0 failed=0 skipped=0
- quote_security：success=5 failed=0 skipped=0
- state_machine：success=50 failed=0 skipped=0
- wallet_structure：success=5 failed=0 skipped=0
- paper_runner：success=0 failed=0 skipped=0

## 缺失文件
- `data/gmgn_candidates_live_run/candidate_pool/token_candidates.json`
- `data/gmgn_candidates_live_run/kline/candidate_kline_pipeline_summary.json`
- `data/gmgn_candidates_live_run/signals/candidate_signal_summary.json`

## 缺失字段
- wallet_structure ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1：token_address, wallet_gate_result, paper_gate_effect, reason_codes, data_quality_status
- wallet_structure 7soYuSPe1LaJ9V37W7ZGDB5Xwxi41LUWjRT3AEQGpump：token_address, wallet_gate_result, paper_gate_effect, reason_codes, data_quality_status
- wallet_structure LzxN1DNn3qNdLw7VKYvxBqvWMY45rhTeq4KoytyLUSA：token_address, wallet_gate_result, paper_gate_effect, reason_codes, data_quality_status
- wallet_structure 6Xipib7UavxaXvWDhepFpU4NzypozVBPvNNjxTdXpump：token_address, wallet_gate_result, paper_gate_effect, reason_codes, data_quality_status
- wallet_structure 3pCyU31quPpsVYaC5TxtXpe6sR1KXSLzk5TkZgXGpump：token_address, wallet_gate_result, paper_gate_effect, reason_codes, data_quality_status

## 卡住 token
- NORMIE `4y874got9bZ2sR42qHYdnfoL6UcdfMaa1SjcP7Ucpump` state=WATCHING reason=SIKK 信号仍为观察/预备层
- AALIEN `ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1` state=PAPER_READY reason=吸筹窗口 valid + SIKK S3/S4 + 允许纸面交易 + 仓位大于0
- WOLVERINE `7soYuSPe1LaJ9V37W7ZGDB5Xwxi41LUWjRT3AEQGpump` state=PAPER_READY reason=吸筹窗口 valid + SIKK S3/S4 + 允许纸面交易 + 仓位大于0
- UNITED `LzxN1DNn3qNdLw7VKYvxBqvWMY45rhTeq4KoytyLUSA` state=PAPER_READY reason=吸筹窗口 valid + SIKK S3/S4 + 允许纸面交易 + 仓位大于0
- MILF `6Xipib7UavxaXvWDhepFpU4NzypozVBPvNNjxTdXpump` state=PAPER_READY reason=吸筹窗口 valid + SIKK S3/S4 + 允许纸面交易 + 仓位大于0
- GOP `3pCyU31quPpsVYaC5TxtXpe6sR1KXSLzk5TkZgXGpump` state=PAPER_READY reason=吸筹窗口 valid + SIKK S3/S4 + 允许纸面交易 + 仓位大于0
- TEMPO `3wL2KuTsaDUX33VvpwCn7st7yxGhY6KKqPkZtMQzpump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- GAY `2Fiut5a3s7vBkGFKXd7kH2v8W1idJ9g7CWAvMEdVpump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- memeoids `5zA1r2LyA9UcShFoZ4DNVJXq1V5pSD4gmibDh5Zxpump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- GA `BhCuLLN38Ru7qBkXBmGzNeG6ipiAcqvywpvNjQW7pump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- rice `2wQq3MrFFHPQnapMt1wnZ2vGkVZDv5ENDCrdLCqFpump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- ELIENUS `yrKmZe5x2YBp1P6ufKLUCNifPbqxwHiwsbfDRWBpump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- Butt `DcSLSZkhxBECsJF4Jny57c1xTaMwKo9HQMKiyXYbpump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- DickButt `4R1Vcbp15UiXJxdmwtgSjp7wFVgqb5keXejW8qA3pump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- WCINU `4mLUpStfvutSZP27m397WmArEbS8xt5HKTzFL8Depump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- Spirit `HXzqEEUjQ6JevbrJiMBAwoiCVikZb93XHmYtde4iCA3G` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- CLAUDE `4D7UFHc6dDc5eKFdbMqdaBC8Sri8V56sE9zSkW53pump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- 小丫头 `J1UpPrMTEv2sNPFtB8ecyc4YScvrYoZJ7iriWJnwpump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- PEPX `9qy89gnSE6HkPPFigfJPWppuLsL3hTpE7HR3YE4Qpump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- OMOGGLE `8MjmLaX4q7xJqHSqLrt2v6sXBgJe97muaXmi7qdepump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- RETArd `G7Tg9KsfQce1HZvBjXfv5ZcdKpuKzPTajhMf51nRpump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- RC `79ogrGd2bhRS455phmsJo8iHYzBusqgLeyxF9Tf5pump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- PEPTA `7WddhpM5mLMTyS16Dqeru1mUcoHetVVkh92zU8Tppump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- AMC `B85ta9Qp7EgoVXaMka9BQYrFogSmC3PRjsxNM6HaHF41` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- HIIE `AKKAPZBnJnzfE83DspsBSoqGSMwa2haFvoEJj1qzdrmk` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- FIT `CFRX4w9w2mvhwZAxCPnyTY3PhHTJ9vQgninuXZfH5Wwn` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- 1000x `C1FjBybKVyatJcJ8JDd7VunSjVkmsb3m1p6q3qvHpump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- CHUDBOB `Bvh8xqP2nkzZBBEywAFqNAc7Mek7QiUofeTmTbKRpump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- lolcat `F8R8VWgiKHvpEh13DFtKsk5PSN7vMzzvP5mmLLUspump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- SIGHT  `ByqipPbSHxzLi6ga5LNrnE229vsLuSrCfHMaDbe1TRND` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- UNIPUMP `9KrdYnHHrsWYpWMxyzbmmrjcXRr7ERWpB3byNeb1pump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- MOGMAN `9gBzMZ1oJ9wDTvzVrhaA7tKMmtWqg9SEmc1UuBPbpump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- Octopus `HDG8Ng6YLpiYXzBASD1Zd5Wh7T8DHRYFcbf4YGuvpump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- monk  `GH6MV3UVLjSbY2WaMUZqEECkDFnt7W4Z7Jrij43gpump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- CRACKROCK `HdRFFy6Sm42rDAPLGRAZ1YymtpLukziwBrE9QGs4pump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- Shrek `6ixv7h9LQ8Vz4S9F4Ta8BWM7USaDapihZroDWSRBpump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- ELUENT `DQa4mxFws6WsXMwn8gpEBXqMsGfDn4Uopi8W2Zvopump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- three `FeMbDoX7R1Psc4GEcvJdsbNbZA3bfztcyDCatJVJpump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- Walter `2CKp88BFyPzr7gEuQKXMJ9cqa24AFXUNC41FR7udpump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- RJGN `hpvoUYjKkvy2hyqC7444mU6eXFD3ETZW4tLd6Dapump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- STJUDE `E8syR4zsgQG2zo9YyiyfX4ujubByR4z6qj9stjASpump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- WINNING `JAxMg5ErnK6ji37TnUh89yA2mouDkFVpiKGaEi1mpump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- PETS `3QQQxazHaMb72d7N9iftT26vuk6A4Re31fYmkwA2pump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- Scribbli `8c3JdTcEqy9XdUJ36NAns7XVDfh356nWxvwcMYKNpump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- Wish `2ssMotVbTUfRJev2UnibHzHsoeszPzgwbfsTZPSHpump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- TrumpCoin `GBvoABT1MH7CogLm46JEy15h3qiKqnmgKZq69BTdpump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- VIGIL `F3iV4HCdr4rBCHmLZPEEFiLxBwznSVwPYx2AoQy5pump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- ROAF `4ne9SgdsLE2P2FJEjxDxUnpwS3fLGCPpHFzYeuDCpump` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- CLUTCH `74CQjPmRd5A7MGc7Dnp1kgUNdPsYtB8FNbtak2Padpce` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据
- ROAF `5ByEYVGSKtTzcQRhY8QkWRqKdhweXMHvHnacRznYnhUY` state=WATCHING reason=候选筛选等级为观察层，等待更多 K线/结构证据

## 钱包结构旁路/降级
- `4y874got9bZ2sR42qHYdnfoL6UcdfMaa1SjcP7Ucpump` status=未接入 effect=NO_WALLET_INPUT reason=
- `3wL2KuTsaDUX33VvpwCn7st7yxGhY6KKqPkZtMQzpump` status=未接入 effect=NO_WALLET_INPUT reason=
- `2Fiut5a3s7vBkGFKXd7kH2v8W1idJ9g7CWAvMEdVpump` status=未接入 effect=NO_WALLET_INPUT reason=
- `5zA1r2LyA9UcShFoZ4DNVJXq1V5pSD4gmibDh5Zxpump` status=未接入 effect=NO_WALLET_INPUT reason=
- `BhCuLLN38Ru7qBkXBmGzNeG6ipiAcqvywpvNjQW7pump` status=未接入 effect=NO_WALLET_INPUT reason=
- `2wQq3MrFFHPQnapMt1wnZ2vGkVZDv5ENDCrdLCqFpump` status=未接入 effect=NO_WALLET_INPUT reason=
- `yrKmZe5x2YBp1P6ufKLUCNifPbqxwHiwsbfDRWBpump` status=未接入 effect=NO_WALLET_INPUT reason=
- `DcSLSZkhxBECsJF4Jny57c1xTaMwKo9HQMKiyXYbpump` status=未接入 effect=NO_WALLET_INPUT reason=
- `4R1Vcbp15UiXJxdmwtgSjp7wFVgqb5keXejW8qA3pump` status=未接入 effect=NO_WALLET_INPUT reason=
- `4mLUpStfvutSZP27m397WmArEbS8xt5HKTzFL8Depump` status=未接入 effect=NO_WALLET_INPUT reason=
- `HXzqEEUjQ6JevbrJiMBAwoiCVikZb93XHmYtde4iCA3G` status=未接入 effect=NO_WALLET_INPUT reason=
- `4D7UFHc6dDc5eKFdbMqdaBC8Sri8V56sE9zSkW53pump` status=未接入 effect=NO_WALLET_INPUT reason=
- `J1UpPrMTEv2sNPFtB8ecyc4YScvrYoZJ7iriWJnwpump` status=未接入 effect=NO_WALLET_INPUT reason=
- `9qy89gnSE6HkPPFigfJPWppuLsL3hTpE7HR3YE4Qpump` status=未接入 effect=NO_WALLET_INPUT reason=
- `8MjmLaX4q7xJqHSqLrt2v6sXBgJe97muaXmi7qdepump` status=未接入 effect=NO_WALLET_INPUT reason=
- `G7Tg9KsfQce1HZvBjXfv5ZcdKpuKzPTajhMf51nRpump` status=未接入 effect=NO_WALLET_INPUT reason=
- `79ogrGd2bhRS455phmsJo8iHYzBusqgLeyxF9Tf5pump` status=未接入 effect=NO_WALLET_INPUT reason=
- `7WddhpM5mLMTyS16Dqeru1mUcoHetVVkh92zU8Tppump` status=未接入 effect=NO_WALLET_INPUT reason=
- `B85ta9Qp7EgoVXaMka9BQYrFogSmC3PRjsxNM6HaHF41` status=未接入 effect=NO_WALLET_INPUT reason=
- `AKKAPZBnJnzfE83DspsBSoqGSMwa2haFvoEJj1qzdrmk` status=未接入 effect=NO_WALLET_INPUT reason=
- `CFRX4w9w2mvhwZAxCPnyTY3PhHTJ9vQgninuXZfH5Wwn` status=未接入 effect=NO_WALLET_INPUT reason=
- `C1FjBybKVyatJcJ8JDd7VunSjVkmsb3m1p6q3qvHpump` status=未接入 effect=NO_WALLET_INPUT reason=
- `Bvh8xqP2nkzZBBEywAFqNAc7Mek7QiUofeTmTbKRpump` status=未接入 effect=NO_WALLET_INPUT reason=
- `F8R8VWgiKHvpEh13DFtKsk5PSN7vMzzvP5mmLLUspump` status=未接入 effect=NO_WALLET_INPUT reason=
- `ByqipPbSHxzLi6ga5LNrnE229vsLuSrCfHMaDbe1TRND` status=未接入 effect=NO_WALLET_INPUT reason=
- `9KrdYnHHrsWYpWMxyzbmmrjcXRr7ERWpB3byNeb1pump` status=未接入 effect=NO_WALLET_INPUT reason=
- `9gBzMZ1oJ9wDTvzVrhaA7tKMmtWqg9SEmc1UuBPbpump` status=未接入 effect=NO_WALLET_INPUT reason=
- `HDG8Ng6YLpiYXzBASD1Zd5Wh7T8DHRYFcbf4YGuvpump` status=未接入 effect=NO_WALLET_INPUT reason=
- `GH6MV3UVLjSbY2WaMUZqEECkDFnt7W4Z7Jrij43gpump` status=未接入 effect=NO_WALLET_INPUT reason=
- `HdRFFy6Sm42rDAPLGRAZ1YymtpLukziwBrE9QGs4pump` status=未接入 effect=NO_WALLET_INPUT reason=
- `6ixv7h9LQ8Vz4S9F4Ta8BWM7USaDapihZroDWSRBpump` status=未接入 effect=NO_WALLET_INPUT reason=
- `DQa4mxFws6WsXMwn8gpEBXqMsGfDn4Uopi8W2Zvopump` status=未接入 effect=NO_WALLET_INPUT reason=
- `FeMbDoX7R1Psc4GEcvJdsbNbZA3bfztcyDCatJVJpump` status=未接入 effect=NO_WALLET_INPUT reason=
- `2CKp88BFyPzr7gEuQKXMJ9cqa24AFXUNC41FR7udpump` status=未接入 effect=NO_WALLET_INPUT reason=
- `hpvoUYjKkvy2hyqC7444mU6eXFD3ETZW4tLd6Dapump` status=未接入 effect=NO_WALLET_INPUT reason=
- `E8syR4zsgQG2zo9YyiyfX4ujubByR4z6qj9stjASpump` status=未接入 effect=NO_WALLET_INPUT reason=
- `JAxMg5ErnK6ji37TnUh89yA2mouDkFVpiKGaEi1mpump` status=未接入 effect=NO_WALLET_INPUT reason=
- `3QQQxazHaMb72d7N9iftT26vuk6A4Re31fYmkwA2pump` status=未接入 effect=NO_WALLET_INPUT reason=
- `8c3JdTcEqy9XdUJ36NAns7XVDfh356nWxvwcMYKNpump` status=未接入 effect=NO_WALLET_INPUT reason=
- `2ssMotVbTUfRJev2UnibHzHsoeszPzgwbfsTZPSHpump` status=未接入 effect=NO_WALLET_INPUT reason=
- `GBvoABT1MH7CogLm46JEy15h3qiKqnmgKZq69BTdpump` status=未接入 effect=NO_WALLET_INPUT reason=
- `F3iV4HCdr4rBCHmLZPEEFiLxBwznSVwPYx2AoQy5pump` status=未接入 effect=NO_WALLET_INPUT reason=
- `4ne9SgdsLE2P2FJEjxDxUnpwS3fLGCPpHFzYeuDCpump` status=未接入 effect=NO_WALLET_INPUT reason=
- `74CQjPmRd5A7MGc7Dnp1kgUNdPsYtB8FNbtak2Padpce` status=未接入 effect=NO_WALLET_INPUT reason=
- `5ByEYVGSKtTzcQRhY8QkWRqKdhweXMHvHnacRznYnhUY` status=未接入 effect=NO_WALLET_INPUT reason=

## 状态机冲突
- `3pCyU31quPpsVYaC5TxtXpe6sR1KXSLzk5TkZgXGpump` token_in_open_and_closed_positions  
- `ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1` token_in_open_and_closed_positions  

## Dashboard 缺字段
- token_count：50
- chip_control_action：50
- chip_control_state：50
- cluster_holding_pct_delta：50
- counterparty_state：50
- current_market_cap_usd：50
- current_price：50
- discovered_at：50
- discovery_market_cap_usd：50
- dominant_side_intent：50
- dominant_side_lifecycle：50
- exit_monitor_at：50
- exit_reason：50
- failure_attribution_type：50
- first_signal_at：50
- largest_cluster_holding_pct：50
- largest_cluster_holding_pct_delta：50
- okx_cluster_control_retention_score：50
- okx_cluster_distribution_score：50
- okx_cluster_risk_score：50
- okx_cluster_score：50
- okx_cluster_status：50
- paper_entry_at：50
- paper_entry_market_cap_usd：50
- paper_exit_at：50
- top300_total_holding_pct：50
- wallet_decision_at：50

## 复盘不可用字段
- current_market_cap_usd：160
- exit_price：3
- exit_reason：3
- exit_time：3
- failure_reason：23
- failure_type：23
- paper_entry_market_cap_usd：160

## 下一步建议
- 补齐 live run 标准输出目录：候选池、K线、信号、状态机、钱包结构、quote/security、paper_live、live_state/dashboard。
- 按审计列出的 missing_fields 修补上游输出合约，字段缺失时显式写 DEGRADED/MISSING 而不是空值。
- 优先排查卡住 token：确认其 K线/信号/quote/security/wallet 决策是否缺失或被跳过。
- 修复钱包结构旁路/降级：标准化 wallet_structure_decision.json 并保留 reason_codes/data_quality_status。
- 处理状态机冲突：开放纸面仓位不得同时处于 BLOCKED/FAILED/EXITED，关闭与开放仓位索引需去重。
- 升级 dashboard live_state 事件级字段，覆盖发现→判断→入场→持仓→退出，并接入 chip_control / market_cap_context / lifecycle v0.3 与 OKX cluster v0.4 字段。
- 补齐复盘字段：市值、入场/退出时间价格、failure_type/failure_reason。
- 保持 paper-only：审计层不得调用采集、gmgn_swap/gmgn_cooking、交易广播或 yolo。
