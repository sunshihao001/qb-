from __future__ import annotations
import json, datetime as dt
from pathlib import Path
FINAL_STATUS="G00_REAL_GOVERNANCE_POLICY_REGISTRY_READY_WITH_GAPS"
BLOCKED_STATUS="G00_REAL_GOVERNANCE_POLICY_REGISTRY_BLOCKED"
FORBIDDEN_ACTIONS=["live_runtime","wallet_signing","auto_deploy","production_trading","execute_real_order","silent_policy_overwrite","weaken_forbidden_actions"]
FORBIDDEN_CLAIMS=["SYSTEM_GOVERNANCE_ENFORCED","PIPELINE_ACCEPTED","PRODUCTION_READY","LIVE_READY","SYSTEM_FULLY_IMPLEMENTED"]
TARGETS=["o00","k00","f00","v00","r00","a00","h00","u00"]
def now_iso(): return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
def stamp(): return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
def read_json(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def write_json(p,obj): p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding="utf-8")
def write_text(p,s): p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(s,encoding="utf-8")
def append_jsonl(p,obj): p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); p.open("a",encoding="utf-8").write(json.dumps({"timestamp":now_iso(),**obj},ensure_ascii=False)+"\n")
def rel_or_abs(repo, s):
    if not s: return None
    p=Path(s); return p if p.is_absolute() else Path(repo)/p
def ensure_dirs(root):
    for d in ["input","preflight","candidates","domain_mapping","conflict_check","policy_rules","policy_bundles","registry","versioning","handoff","failure_evidence","trace","audit","acceptance","recovery","reports"]: (Path(root)/d).mkdir(parents=True,exist_ok=True)
