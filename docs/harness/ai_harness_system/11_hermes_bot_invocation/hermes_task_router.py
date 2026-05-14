# Hermes Task Router

from pathlib import Path

ROUTES = {
    "文档研究": "方法轮",
    "目录治理": "目录侦察流",
    "代码修改": "工程执行流",
    "系统设计": "架构设计流",
    "调试恢复": "错误诊断流",
    "长时间任务": "分段循环流",
    "记忆整理": "记忆审计流",
}

def route(task_type: str) -> dict:
    flow = ROUTES.get(task_type, "通用受控流程")
    return {
        "task_type": task_type,
        "route_flow": flow,
    }

if __name__ == "__main__":
    import json, sys
    task_type = sys.argv[1] if len(sys.argv) > 1 else ""
    print(json.dumps(route(task_type), ensure_ascii=False, indent=2))
