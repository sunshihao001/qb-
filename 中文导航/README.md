# 中文导航层

这里是 *人类阅读用* 的中文目录导航，不是工程真实主路径。

## 使用原则

- 真实工程路径继续使用英文目录名。
- 这里仅提供中文别名、用途说明和快速定位。
- 不把运行数据直接放进这里。
- 不把代码、报告、方法论迁移到这里。

## 中文目录对照

- `运行数据` → `data/`
- `钱包事实数据` → `data/source_wallet_bot/`
- `结构推断数据` → `data/intel_bot/`
- `旧运行混合区` → `data/gmgn_candidates_live_run/`
- `功能代码` → `modules/`
- `自动化测试` → `tests/`
- `方法轮` → `research_loop/`
- `方法论资产` → `research_loop/methodology/`
- `系统文档` → `docs/`
- `人类报告` → `reports/`
- `旧路径兼容` → `legacy_compat/`
- `交接合同` → `contracts/`
- `系统Schema` → `schemas/`
- `导入暂存` → `imports/`
- `项目工具` → `tools/`

## 直接查找建议

- 要找钱包事实：去 `data/source_wallet_bot/<mode>/<token_address>/`
- 要找行为推断：去 `data/intel_bot/<mode>/<token_address>/`
- 要找方法轮规则：去 `research_loop/methodology/`
- 要找代码：去 `modules/`
- 要找验收/审计：去 `reports/`

## 备注

中文导航层只负责“看得懂、找得到”，真实写入仍遵守 `docs/system_directory_constitution.md` 和 `docs/system_directory_routes.json`。
