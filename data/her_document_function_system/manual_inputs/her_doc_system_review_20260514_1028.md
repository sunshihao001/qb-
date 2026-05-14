HER_DOC_SYSTEM_REVIEW
项目名称：HER_DOC 轻量机构级文档到功能自动化系统
当前阶段：三口令固定化 + 问题清单任务包 + 自动化应用场景落实
目标：用 HER_DOC 系统体系把文档/规则/阶段材料转成可审计、可执行、可追踪、可交接的实际应用场景任务包；只允许 safe-mode/read-only/design-level replay，不进入实盘、签名、广播、生产策略激活。
约束：不得触发 live runtime / wallet signing / auto deploy / production trading / policy active；不得声明 FULL_RUNTIME_READY 或 PIPELINE_ACCEPTED；所有缺口必须显式进入 gap_register 或 task_package。
期望输出：system_review、system_audit、implementation_task_package、evidence_binder、pipeline_run、final_report。
是否允许执行文件/代码操作：允许在 /root/sikk-gmgn/system/her_document_function_system 与 /root/sikk-gmgn/data/her_document_function_system 下生成 safe-mode 产物；允许补充 tools 下安全审计/证据绑定脚本。
