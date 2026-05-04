# HER 任务启动器阶段验收报告

## 阶段名称
`sikk_her_task_router.py` HER 任务启动器 v1。

## 完成目标
把上一阶段沉淀的 HER 核心自动化体系进一步落成可调用脚本：输入 GPT 链接、外部链接或普通目标，自动生成任务棱镜、推荐 skill、工具路由、Section Task、验收清单。

## 修改文件
- `sikk_her_task_router.py`
- `tests/test_sikk_her_task_router.py`

## 新增文件
- `tasks/chatgpt_share_69f83af2/TASK_ROUTER.json`
- `tasks/chatgpt_share_69f83af2/TASK_ROUTER.md`
- `tasks/chatgpt_share_69f83af2/SECTION_TASK.md`
- `reports/chatgpt_share_69f83af2/her_task_router_acceptance.md`

## 新增能力
- 自动识别任务类型：`chatgpt_share` / `external_link` / `manual_goal`。
- 自动推荐 skills：ChatGPT share 默认推荐 `conversation-transcript-ingestion`、`sikk-sol-core-methodology`、`test-driven-development`。
- 自动生成任务棱镜 5 阶段：读取保存、问题识别、系统映射、分阶段执行、审计沉淀。
- 自动生成工具路由：链接读取、知识吸收、SIKK runtime、pytest、Super Hermes prism 思维、repomix、DeerFlow/delegate_task。
- 自动生成移动端可读的 `TASK_ROUTER.md` 与 `SECTION_TASK.md`。

## 测试命令
```bash
PYTHONPATH=/root/sikk-gmgn python3 -m pytest tests/test_sikk_her_task_router.py -q
PYTHONPATH=/root/sikk-gmgn python3 -m pytest tests/test_sikk_her_task_router.py tests/test_sikk_automation_workflow.py tests/test_sikk_knowledge_absorption.py -q
PYTHONPATH=/root/sikk-gmgn python3 -m pytest -q
PYTHONPATH=/root/sikk-gmgn python3 sikk_live_run.py --mode once --output-root data/gmgn_candidates_live_run --limit 5 --quote-sources none
```

## 测试结果
- TDD RED：首次运行 `tests/test_sikk_her_task_router.py` 失败，原因是 `ModuleNotFoundError: No module named 'sikk_her_task_router'`。
- GREEN：实现脚本后专项测试 `2 passed in 0.01s`。
- 相关专项组合：`8 passed in 0.04s`。
- 全量测试：`210 passed in 12.44s`。
- Runtime 最小验证：成功生成 `live_run_manifest.json`、`live_state.json`、`site/dashboard_data.json`、`telegram_callback_index.json` 等。

## 安全验收
- `real_swap_enabled=false`
- `confirmation_enabled=false`
- 任务启动器只写任务计划，不执行真实交易、不读取私钥、不签名、不广播。

## 实际调用示例
```bash
PYTHONPATH=/root/sikk-gmgn python3 sikk_her_task_router.py 'https://chatgpt.com/share/69f83af2-a380-83a7-a429-200c72d43279' --root /root/sikk-gmgn
```

输出：
- `/root/sikk-gmgn/tasks/chatgpt_share_69f83af2/TASK_ROUTER.json`
- `/root/sikk-gmgn/tasks/chatgpt_share_69f83af2/TASK_ROUTER.md`
- `/root/sikk-gmgn/tasks/chatgpt_share_69f83af2/SECTION_TASK.md`

## 未完成项
- 尚未把任务启动器接入 Telegram handler。
- 尚未自动执行浏览器读取和 `sikk_knowledge_absorption.py`，当前是生成任务计划与 Section Task，不直接跑完整吸收链。
- 尚未封装 Repomix/Super Hermes/DeerFlow 的真实 CLI 调用，只生成路由建议与约束。

## 是否允许进入下一阶段
允许。下一阶段建议：新增 `--execute-absorption` 安全选项，让 ChatGPT share 在生成任务路由后自动执行“读取/保存原文 → 知识吸收 → 验收报告”的本地链路；默认仍不触发真实交易。
