# Legacy Runtime Policy

## 对象

`/root/sikk-gmgn/data/gmgn_candidates_live_run`

## 裁决

- 历史运行主区
- 混合旧 runtime 产物
- 保留不动
- 不删除
- 不移动
- 不作为新主写路径
- 后续通过 compatibility index 读取
- 需要 copy-only 映射时必须生成 migration_map

## 说明

该目录承载旧的 GMGN 候选运行产物、dashboard、paper_live、state_machine、time_context、quote_security 等混合结果。它是历史系统事实，不是 Source Wallet Bot 的新主写路径。

## 后续原则

- 新 Source Wallet Bot 输出只写入 `data/source_wallet_bot/<mode>/<token_address>/`
- 旧 live runtime 目录只做兼容读取、审计回溯和 copy-only 治理
- 若未来需要归档迁移，必须先生成 migration map / manifest
