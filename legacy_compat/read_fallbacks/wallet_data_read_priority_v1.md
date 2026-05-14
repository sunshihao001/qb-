# Hermes 钱包数据读取优先级 V2

用途：防止后续任务读错目录、重复分析、漏掉旧数据，也避免在所有旧目录里乱搜。

## 总原则

Hermes 处理一个 token 的钱包/结构分析时，必须先按新标准体系读取；只有当新体系缺数据时，才逐层回退到旧目录映射与只读补查。

不要直接从 dashboard、paper、reports 或大范围旧目录反推事实。

## 读取顺序

### 1. 新标准入口
优先读取标准目录下的主输出：

- `data/source_wallet_bot/legacy/<token_address>/wallet_data/raw/`
- `data/source_wallet_bot/legacy/<token_address>/wallet_data/normalized/`
- `data/source_wallet_bot/legacy/<token_address>/structure_analysis/wallet_fact/`
- `data/source_wallet_bot/legacy/<token_address>/structure_analysis/intelligence/`
- `data/source_wallet_bot/legacy/<token_address>/structure_analysis/handoff/`
- `data/source_wallet_bot/legacy/<token_address>/structure_analysis/reports/`

### 2. token 索引
读取该 token 的索引与清单，确认标准包是否存在、哪些文件已复制：

- `legacy_compat/path_maps/wallet_data_token_index_v1.json`
- token manifest / copy manifest / path map

用途：判断 token 是否已有可用标准包。

### 3. 数据护照
读取 token 的护照类文件，用于确认资产边界、来源、版本、可读路径：

- token manifest
- package passport
- directory layout / governance manifest

用途：确认“该读什么、该不该读、是否已标准化”。

### 4. 字段字典
先看字段字典和合同，再决定缺字段是否真的缺失：

- `modules/source_wallet_bot/field_dictionary.csv`
- `modules/source_wallet_bot/gmgn_to_sikk_field_mapping.csv`
- `modules/source_wallet_bot/*.schema.json`
- 相关 contract / acceptance 文件

用途：避免把“字段改名”误判成“数据缺失”。

### 5. 旧路径映射
如果标准体系缺文件或缺字段，再查旧路径映射：

- `legacy_compat/path_maps/*.json`
- `legacy_compat/read_fallbacks/*.md`
- 旧路径 -> 新路径映射表

用途：定位旧目录对应的标准落点，而不是盲搜全仓。

### 6. 旧目录只读补查
最后才允许只读补查旧目录：

- `data/gmgn_candidates_live_run/**`
- `data/source_wallet_bot/live/**`
- `data/source_wallet_bot/ad_hoc/**`
- 其他 legacy runtime 只读区

规则：
- 只读，不写回
- 只查映射能指到的范围
- 不做全仓盲搜
- 补查必须记录 old_path、reason、token_address、semantic_layer guess、是否已有标准副本

## 缺失判定

如果按以上顺序仍找不到：

- 标记为缺失
- 记录缺失字段或缺失文件名
- 不要擅自从旧报告、dashboard、paper_live 反推出事实

## 必须避免的行为

- 不从 `paper_live`、dashboard、site、reports 反推 facts
- 不把 `priority_level` 当买入信号
- 不把 inference 当确定事实
- 不在所有旧目录里乱搜
- 不删除、不移动旧目录
- 不修改业务代码作为这一步的前置动作

## 建议落地策略

1. 新标准优先
2. 标准缺失才回退映射
3. 映射缺失才补查旧目录
4. 两边都没有才标记缺失

这样 Hermes 才不会每次又回到混乱状态。
