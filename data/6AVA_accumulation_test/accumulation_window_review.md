# SIKK Accumulation Window Detector 测试复盘

## 测试对象
- 代币：SCAM / Scam Altman
- 地址：6AVAUKa9uxQpruHZUinFECpXEh1usRVtzQWK8N2wpump
- 链：Solana
- GMGN 创建时间：2026-04-27 16:22:11 UTC
- GMGN open_timestamp / 迁移开放交易时间：2026-04-27 16:30:38 UTC
- 本轮 K线锚点：open_timestamp 后 1m K线
- 流通供应量：999,978,483

## 模块识别结果
- T_start：2026-04-27 16:38:00 UTC
- T_start 估算市值：277,617.69 USD
- T_end：2026-04-27 16:52:00 UTC
- T_end 估算市值：674,289.40 USD
- 窗口长度：15 根 1m K线 / 14 分钟
- 窗口高点：0.00078695081
- 窗口低点：0.00020284997
- POC：0.00044014093625
- VAH：0.00078086642625
- VAL：0.00036712833125
- AVWAP 锚点：2026-04-27 16:31:00 UTC
- 窗口状态：valid
- 突破类型：放量突破最近 LH

## K线阶段解释
- 16:31-16:37：开盘后价格从约 151.7k 市值逐步抬升到 233.9k 市值，评分多为 30-50，尚未满足连续吸筹阈值。
- 16:38-16:40：连续三根 accumulation_score=60，触发 T_start。主要证据为：未继续大幅创新低、OBV 未跟随走弱、明显下影线、重新贴近/站上开盘 AVWAP。
- 16:41-16:51：价格沿 AVWAP 上方震荡抬升，16:49 形成 HL，16:50-16:51 CMF 转正且 OBV 增强。
- 16:52：RVOL=2.16，score=90，close 放量突破最近 LH，标记 T_end。
- 16:53-16:56：突破后延续扩张，市值约 780k → 1.14M，说明 16:52 是较早的结构突破确认点。

## 钱包辅助判断摘要
- P0 / bonding curve 早期：16:22:11 附近出现多笔 dev_team + bundler + sniper + paper_hands 小额地址，包含 creator/dev_team 标签，属于迁移开放前的早期执行/测试/曲线阶段证据，不直接写“庄家”。
- 开放交易初段：16:31-16:33 出现多笔 bundler/KOL/fresh_wallet 地址，部分买入额 1k-8k USD，随后在后续价格扩张中有较高利润，支持早期结构参与迹象。
- 吸筹窗口内：16:38:42-16:48:01 在样本中命中 16 个地址，其中多为 bundler/fresh/transfer_in/top_holder 相关；多地址在窗口内买入后卖出或仍持仓，说明 T_start-T_end 不是纯 K线孤立信号，而是有钱包行为配合。
- 典型窗口内地址：
  - EWUP...JjBR：16:38:42，买入约 4,204 USD，标签 padre,bundler,paper_hands，候选：捆绑/短持。
  - 7cNf...ph1j：16:40:09，买入约 57,960 USD，fresh_wallet,bundler，候选：新钱+捆绑执行。
  - BXE1...hDBc：16:42:33，买入约 7,252 USD，仍持仓约 0.473%，候选：捆绑持仓观察。
  - 3y5V...3iip：16:45:34，买入约 58,762 USD，top_holder,bundler,transfer_in，仍持仓约 1.965%，候选：Token转入+Top持仓观察。
  - Dpjp...YVun：16:45:55，bundler,transfer_in，仍持仓约 0.692%，候选：Token转入持仓观察。

## 复盘结论
本轮模块把吸筹开始识别在 16:38 UTC，估算市值约 277.6k；把早期吸筹结束/突破确认识别在 16:52 UTC，估算市值约 674.3k。结合钱包侧，16:38-16:52 内出现了 bundler、新钱包、Token转入、Top持仓等多类地址参与，和 K线的 OBV/CMF/AVWAP/放量突破证据一致。该窗口适合作为后续固定范围成交量分布、POC、AVWAP、Fib 区间的锚定范围。

## 输出文件
- 模块代码：/root/sikk-gmgn/sikk_accumulation_window_detector.py
- K线CSV：/root/sikk-gmgn/data/6AVA_accumulation_test/kline_1m.csv
- 识别JSON：/root/sikk-gmgn/data/6AVA_accumulation_test/outputs/accumulation_window.json
- 识别CSV：/root/sikk-gmgn/data/6AVA_accumulation_test/outputs/accumulation_window.csv
- 逐K线明细：/root/sikk-gmgn/data/6AVA_accumulation_test/outputs/accumulation_window_bars.csv
- 窗口内钱包辅助表：/root/sikk-gmgn/data/6AVA_accumulation_test/wallet_auxiliary_in_accumulation_window.csv
