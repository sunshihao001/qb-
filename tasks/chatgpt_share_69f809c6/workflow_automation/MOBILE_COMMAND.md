# 手机可用入口｜SIKK GPT 工作流自动化

## Telegram 自然语言入口

直接发送：

```text
工作流自动化 https://chatgpt.com/share/69f809c6-e7ac-83ab-823a-02d6cd8e5426
```

说明：这是自然语言触发词，*无需 slash command*，可避开 Hermes Gateway 对未知 `/命令` 的拦截。

## VPS 本地一键命令

```bash
PYTHONPATH=/root/sikk-gmgn python3 sikk_her_task_router.py 'https://chatgpt.com/share/69f809c6-e7ac-83ab-823a-02d6cd8e5426' --root /root/sikk-gmgn --execute-absorption --workflow-package
```

## 安全边界

- paper-only
- 禁止真实交易
- 禁止真实 swap
- 禁止读取私钥
- 禁止签名
- 禁止 broadcast

## 自动执行链路

1. 识别 GPT share / 外链 / 普通目标。
2. 生成 TASK_ROUTER 与 SECTION_TASK。
3. 自动执行知识吸收：inbox → passport → rules → audit → update → skill → Hindsight。
4. 生成工作流包与验收报告。
5. 后续仍通过 `sikk_live_run.py` 单入口做 paper-only runtime 验证。

## 当前 Slug

`chatgpt_share_69f809c6`
