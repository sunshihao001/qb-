# Directory Official Decisions 20260506

本文件是恢复包所需的目录治理快照，目标是让备份分支 clone 后可以自检，不新增业务流程。

## 固定决策

- 新运行输出不得写入旧 `data/gmgn_candidates_live_run/` 主路径。
- 钱包结构 / Source Wallet Bot 主目录固定在 `/root/sikk-gmgn/`。
- 旧目录只读兼容，迁移只能 copy-only，不 delete，不 move。
- 恢复必须先到 sandbox / isolated target，不覆盖 `/root/sikk-gmgn`。
- 备份恢复目录 `备份恢复/` 只保存恢复手册、清单、脚本和验收模板，不作为交易模块。
