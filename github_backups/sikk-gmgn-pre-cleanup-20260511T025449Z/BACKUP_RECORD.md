# SIKK-GMGN GitHub 备份记录

## 基本信息

- 备份名称：`sikk-gmgn-pre-cleanup-20260511T025449Z`
- 备份目录：`/root/sikk-gmgn/github_backups/sikk-gmgn-pre-cleanup-20260511T025449Z/`
- GitHub 仓库内路径：`github_backups/sikk-gmgn-pre-cleanup-20260511T025449Z/`
- 原项目根目录：`/root/sikk-gmgn`
- 远程仓库：`https://github.com/sunshihao001/qb-.git`
- 分支：`main`
- 备份类型：清洗前 GitHub 备份，上传前整理版

## 这个目录是做什么的

这个目录用于在清理 `/root/sikk-gmgn` 大量历史运行数据之前，保存一份 GitHub 可追踪的备份记录。

它不是新的运行系统入口，也不是新的钱包分析主目录。

它的作用是：

1. 记录本次清洗前的保留/归档判断；
2. 保存清洗计划、审计报告、路径清单；
3. 保存选定有用资产的压缩包分片；
4. 方便以后从 GitHub 下载、校验、恢复；
5. 避免清洗过程中误删 HER 底层逻辑、SIKK 理论公式、contracts、schemas、modules、tests 等关键资产。

## 目录结构说明

```text
github_backups/sikk-gmgn-pre-cleanup-20260511T025449Z/
  README.md
  BACKUP_RECORD.md
  BACKUP_INCLUDE_RELATIVE_PATHS.txt
  BACKUP_DIR_SIZE.txt
  records/
  archives/
```

### `README.md`

GitHub 目录首页说明。

用于快速知道：

- 这是什么备份；
- 如何恢复；
- 各子目录是什么含义。

### `BACKUP_RECORD.md`

也就是本文档。

用于给人看，说明：

- 为什么备份；
- 备份目录是什么用；
- 备份了哪些类别；
- 怎么下载和恢复；
- 上传记录和校验方式。

### `BACKUP_INCLUDE_RELATIVE_PATHS.txt`

备份输入清单。

这里面的路径都是相对 `/root/sikk-gmgn` 的相对路径，用来生成压缩包。

它的作用是让未来能追溯：

- 当时到底把哪些目录放进了备份；
- 哪些目录是强保留；
- 哪些目录是备份后再考虑清洗。

### `records/`

清洗任务的记录目录。

包含：

- `slim_cleanup_direction.md`：用户纠正后的瘦身方向；
- `document_purpose_and_migration_decision.md`：说明计划文件为什么放在 `research_loop/plans`，是否迁移；
- `pre_cleanup_data_analysis_report.md`：清洗前数据分析报告；
- `data_cleanup_backup_manifest.json`：机器可读备份分类清单；
- `backup_include_paths.txt`：原始绝对路径备份清单；
- `backup_before_cleanup.sh`：本地备份脚本；
- `move_safe_cache_to_quarantine.sh`：安全缓存隔离脚本；
- `safe_delete_after_backup_paths.txt`：备份后可考虑安全删除的路径。

这个目录主要保留“为什么备份、怎么判断、怎么清洗”的依据。

### `archives/`

压缩包分片目录。

包含：

- `sikk-gmgn-useful-assets-20260511T025449Z.tar.gz.part-000`
- `SHA256SUMS_FULL_ARCHIVE.txt`
- `SHA256SUMS_PARTS.txt`
- `ARCHIVE_FILES.txt`

因为 GitHub 单文件限制较严格，所以压缩包按 49MB 分片保存。

当前只有一个分片，说明压缩后的备份包小于 49MB。

## 备份内容类别

### 强保留系统资产

这些是项目的核心，不应该在清洗中删除：

- `hermes_harness/`：HER 本体、底层 runtime/control 逻辑；
- `sikk_stable_trader_os/`：SIKK 稳定交易系统控制层；
- `modules/`：可执行模块与 runtime 能力；
- `contracts/`：输入/输出契约；
- `schemas/`：机器可校验 schema；
- `tests/`：回归测试和 fixture；
- `docs/`：constitution、routing、系统规则、文档处理方法；
- `skills/`：可复用技能/方法沉淀；
- `tools/`、`scripts/`：工具和脚本；
- `shared_handoff/`、`task_books/`、`audits/`：handoff、任务书、审计记录。

### 备份后可缩减的数据资产

这些不是长期主资产，备份后可以抽样保留或归档：

- `data/source_wallet_bot/`
- `data/stable_trader_os/`
- `data/runtime/`
- `data/gmgn_candidates_live_run/*`
- 历史 `sikk_sol_*` run 数据；
- `reports/system_audit/`
- `reports/source_wallet_bot/`
- `reports/intel_bot/`
- `reports/runtime/`
- `legacy_compat/`
- `research_loop/state/wallet_data_*`
- `runtime_logs/`
- `outputs/`

### 备份后的目标方向

项目应逐步瘦身为：

```text
HER 底层逻辑
+ 文档处理/契约化方法
+ SIKK 理论公式库
+ API adapter
+ 少量 replay/regression fixtures
```

而不是继续堆积大量历史运行数据。

## 恢复方法

在仓库根目录执行：

```bash
cd /root/sikk-gmgn/github_backups/sikk-gmgn-pre-cleanup-20260511T025449Z
cat archives/sikk-gmgn-useful-assets-20260511T025449Z.tar.gz.part-* > /tmp/sikk-gmgn-useful-assets-20260511T025449Z.tar.gz
sha256sum /tmp/sikk-gmgn-useful-assets-20260511T025449Z.tar.gz
cat archives/SHA256SUMS_FULL_ARCHIVE.txt
```

确认 sha256 一致后，解压到目标目录：

```bash
mkdir -p /root/restore-sikk-gmgn
cd /root/restore-sikk-gmgn
tar -xzf /tmp/sikk-gmgn-useful-assets-20260511T025449Z.tar.gz
```

## 注意事项

- 本备份未执行删除动作；
- 本备份排除了常见 cache、`__pycache__`、`.pytest_cache`、`.env`、私钥类文件；
- 本备份是清洗前快照，不代表生产可运行版本；
- 后续清洗应先验证 GitHub 上传成功，再做归档/隔离/删除；
- 如果未来要长期保留清洗原则，应从 `records/slim_cleanup_direction.md` copy-only 提炼到 `docs/system_cleanup_constitution.md`，不要直接移动原始任务记录。

## 当前状态

- 本地备份目录：已生成；
- 压缩包分片：已生成；
- sha256 校验文件：已生成；
- GitHub 上传：待 commit/push；
- 删除/清洗动作：尚未执行。
