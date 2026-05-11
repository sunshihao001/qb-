# data_cleanup_20260511 文档用途与迁移判断

## 这份文件是什么

文件：`/root/sikk-gmgn/research_loop/plans/data_cleanup_20260511/slim_cleanup_direction.md`

它不是运行数据，不是系统执行入口，也不是交易分析结果。

它的功能是：

- 记录本次用户纠正后的“清洗方向”；
- 定义哪些资产真正有用；
- 给后续备份、归档、删除提供判断标准；
- 防止清洗时误删 HER 底层逻辑、文档处理方法论、公式理论、API adapter 设计；
- 作为下一步生成 `archive_then_remove_paths.txt` 的依据。

## 为什么它放在 research_loop/plans

因为它当前属于“清洗计划 / 操作计划”，不是长期系统规则。

当前路径：

```text
/root/sikk-gmgn/research_loop/plans/data_cleanup_20260511/slim_cleanup_direction.md
```

含义：

```text
research_loop/     研究/治理/计划工作区
plans/             计划类文档
数据清洗任务ID/     本次清洗任务包
```

所以它现在放这里是合理的：这是清洗前的计划和方向记录。

## 它未来应该迁移到哪里

如果只是临时清洗参考：

- 保持在 `research_loop/plans/data_cleanup_20260511/`
- 备份时一起打包即可
- 不需要迁移

如果要变成长期系统规则：

应该 copy-only 提炼到：

```text
/root/sikk-gmgn/docs/system_cleanup_constitution.md
```

或者追加到已有：

```text
/root/sikk-gmgn/docs/system_directory_constitution.md
```

推荐做法：

1. 当前文件保留为任务原始记录；
2. 复制一份长期版到 `docs/system_cleanup_constitution.md`；
3. 长期版只写原则，不写临时路径细节；
4. 原始计划文件继续留在 `research_loop/plans/...`，作为审计链。

## 是否需要迁移

结论：

- **现在备份前不需要迁移。**
- **备份后可以 copy-only 提炼一份到 docs。**
- **不要 move 原文件。**

原因：

- 当前路径符合“计划文件”的目录职责；
- 如果直接移动，会破坏本次清洗任务包的完整性；
- 长期规则应该进入 `docs/`，但应该是提炼版，不是原计划原封不动搬过去；
- 备份脚本已经包含这个计划目录，会一起备份。

## 备份时怎么处理

备份脚本已经会备份：

```text
/root/sikk-gmgn/research_loop/plans/data_cleanup_20260511/
```

因此包括：

- `slim_cleanup_direction.md`
- `pre_cleanup_data_analysis_report.md`
- `data_cleanup_backup_manifest.json`
- `backup_before_cleanup.sh`
- `move_safe_cache_to_quarantine.sh`
- 本说明文件

## 推荐下一步

备份前：

```bash
bash /root/sikk-gmgn/research_loop/plans/data_cleanup_20260511/backup_before_cleanup.sh
```

备份后，如果要长期固化规则，再创建：

```text
/root/sikk-gmgn/docs/system_cleanup_constitution.md
```

长期版应该只保留这几条：

- HER 底层逻辑是强保留资产；
- 文档处理方法论是强保留资产；
- SIKK 理论和计算公式是强保留资产；
- 大量历史运行数据不是强保留资产；
- 交易平台 API 可重拉的数据不长期堆积；
- 每类数据只保留少量 replay/regression fixture；
- 清洗采用 backup -> archive/quarantine -> verify -> delete 的顺序。
