# Section Task｜chatgpt_share_69f868b8

## 目标
把输入任务转成 HER/Hermes 可执行的分阶段工作包，而不是只做总结。

## 范围
- 来源：`https://chatgpt.com/share/69f868b8-19c0-83ab-9c04-6339a93258bc`
- 类型：`chatgpt_share`
- 安全边界：paper-only；不执行真实 swap；不读取私钥；不签名；不广播。

## 执行步骤
1. 读取相关文件或链接；不可读必须说明。
2. 建立任务棱镜与约束报告。
3. 做系统映射审计。
4. 按 TDD 修改知识资产/代码/文档。
5. 运行测试命令。
6. 输出验收标准与报告。

## 测试命令
- `PYTHONPATH=/root/sikk-gmgn python3 -m pytest tests/test_sikk_her_task_router.py -q`
- `PYTHONPATH=/root/sikk-gmgn python3 -m pytest -q`
- `PYTHONPATH=/root/sikk-gmgn python3 sikk_live_run.py --mode once --output-root data/gmgn_candidates_live_run --limit 5 --quote-sources none`
- `检查 live_run_manifest.json 中 real_swap_enabled=false 且 confirmation_enabled=false`

## 验收标准
- 输入已保存或不可读已说明。
- 每个结论绑定文件、字段、命令、测试或验收标准。
- 所有新增能力可被真实命令或测试调用。
- 安全边界保持 false：real_swap/signing/broadcast/confirmation。
