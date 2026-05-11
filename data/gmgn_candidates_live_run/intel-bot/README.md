# Intel Bot 数据目录

## Telegram Bot 职责

Intel Bot 负责：结构分析、钱包画像、筹码结构、同源 / 分发 / 接盘 / 结果钱包判断。

## 固定目录

- `code/`：只放 Intel Bot 相关代码索引、schema 合同、生成脚本索引、只读分析模块说明。
- `logs/`：只放 Intel Bot 运行数据、迁移过来的旧结构数据、每个 token 的结构分析 / 钱包画像 / 筹码结构 / 同源 / 分发 / 接盘 / 结果钱包判断输出。

## 强制规则

迁移过来的历史数据也必须放在本目录下，不能散放到旧目录：

- 禁止：`data/gmgn_candidates_live_run/wallet_structure/`
- 禁止：`data/gmgn_candidates_live_run/intel_bot/`
- 禁止：`data/wallet_intelligence/`

统一归档位置：

- `intel-bot/logs/wallet_structure/`
- `intel-bot/logs/legacy_intel_bot/`
- `intel-bot/logs/legacy_wallet_intelligence/`
