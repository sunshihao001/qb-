
import argparse, json
from pathlib import Path
BASE = Path(__file__).resolve().parents[1]
def parser(desc):
    p=argparse.ArgumentParser(description=desc)
    p.add_argument('--dry-run', action='store_true', help='Do not write files')
    p.add_argument('--base', default=str(BASE), help='Hermes harness root; defaults to this hermes_harness')
    return p

def main():
    p=parser('Hermes task router'); p.add_argument('task_type', nargs='?', default='系统设计'); a=p.parse_args()
    routes={'文档研究':'method_wheel','目录治理':'directory_scouting','代码修改':'engineering_execution','系统设计':'architecture_design','调试恢复':'error_diagnosis','长时间任务':'segmented_loop','记忆整理':'memory_audit'}
    print(json.dumps({'task_type':a.task_type,'route_flow':routes.get(a.task_type,'scouting'),'dry_run':a.dry_run},ensure_ascii=False,indent=2))
if __name__=='__main__': main()
