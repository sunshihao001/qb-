#!/usr/bin/env python3
import json, sys, datetime
failure = sys.argv[1] if len(sys.argv)>1 else 'unknown'
actions={'文件未生成':'回到该阶段重新生成','文件为空':'重新生成并检查输入','JSON 非法':'修复 JSON，重新验证','命令失败':'记录 stderr，生成 retry plan','权限越界':'BLOCKED，等待用户授权'}
print(json.dumps({'failure_type':failure,'recovery_action':actions.get(failure,'查 recovery_decision_table 并生成恢复报告'),'created_at':datetime.datetime.utcnow().isoformat()+'Z'}, ensure_ascii=False, indent=2))
