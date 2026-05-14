# 密钥与配置恢复规则

## 总原则

备份分支只保存系统文件、规则、代码、测试、恢复流程，不保存真实 secret。

恢复时如果缺少密钥，只能记录为：

```text
manual secret injection required
```

不能从旧目录复制真实值进备份或恢复报告。

## 禁止备份/恢复的真实内容

- 私钥
- 助记词
- seed phrase
- exchange signing secret
- Telegram bot token 实值
- webhook secret 实值
- GitHub token 实值
- OpenAI / Anthropic / 其他 LLM API key 实值
- GMGN / OKX 等任何真实 API secret 实值

## 允许进入备份的内容

- `.env.example`
- `config.example.yaml`
- placeholder：`REPLACE_ME`
- required marker：`required_manual_injection`
- 权限说明文档
- secret 名称清单，但不能包含真实值

## 推荐占位模板

```text
TELEGRAM_BOT_TOKEN=required_manual_injection
GMGN_API_KEY=required_manual_injection_if_live_data_enabled
OKX_API_KEY=required_manual_injection_if_adapter_enabled
PRIVATE_KEY=forbidden
MNEMONIC=forbidden
REAL_SWAP_ENABLED=false
BROADCAST_ENABLED=false
PAPER_ONLY=true
```

## 恢复时判断

如果系统启动需要 Telegram token：

```text
恢复结论：代码恢复成功；Telegram gateway 需要人工注入 TELEGRAM_BOT_TOKEN 后才能启动。
```

如果系统要求 private key：

```text
恢复结论：阻塞。该路径违反 paper-only / no-private-key 边界。
```

## 对 AI/Agent 的约束

任何 agent 在恢复过程中不得：

- 搜索真实密钥。
- 打印真实密钥。
- 把 `.env` 加入 Git。
- 为了“完整恢复”生成或导入私钥。
- 启用真实交易开关。
