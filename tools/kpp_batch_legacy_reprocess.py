#!/usr/bin/env python3
"""Execute the queued legacy document reprocess package in lightweight KPP mode.

Produces document passports, chunk manifests, phase mappings, candidate task records,
and handoff packets for markdown docs. This is candidate-only and does not mutate
runtime/business logic.
"""
from __future__ import annotations
import hashlib, json, re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
try:
    import yaml  # type: ignore
except Exception:
    yaml=None
ROOT=Path('/root/sikk-gmgn')
OUT=ROOT/'data/knowledge_processing_program/batch_legacy_reprocess'
DOC_ROOTS=[ROOT/'sikk_stable_trader_os', ROOT/'docs']
PHASE_PATTERNS=[('P01','candidate|data fact|source data|数据事实|候选'),('P02','source data|数据事实|采集'),('P03','wallet|钱包|entity'),('P04','chip|筹码'),('P05','evidence|证据|structure position'),('P06','scenario|场景|盘型'),('P07','strategy|gate|策略|门禁'),('P08','risk|execution|执行|风控'),('P09','review|replay|复盘'),('P10','upgrade|升级|governance|治理')]

def write_json(p:Path,o:Any): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def write_yaml(p:Path,o:Any):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text((yaml.safe_dump(o,allow_unicode=True,sort_keys=False) if yaml else json.dumps(o,ensure_ascii=False,indent=2))+'\n',encoding='utf-8')
def rel(p:Path):
    try: return str(p.relative_to(ROOT))
    except Exception: return str(p)
def classify(txt:str,path:str):
    scores={}
    blob=(path+'\n'+txt[:5000]).lower()
    for phase,pat in PHASE_PATTERNS: scores[phase]=len(re.findall(pat,blob,re.I))
    phase=max(scores,key=scores.get) if max(scores.values())>0 else 'K00'
    return phase,scores
def chunks(txt:str,size:int=6000): return [txt[i:i+size] for i in range(0,len(txt),size)] or ['']
def main():
    ts=datetime.now(timezone.utc).isoformat(); docs=[]
    for root in DOC_ROOTS:
        if root.exists():
            docs += [p for p in root.rglob('*.md') if p.is_file() and 'node_modules' not in p.parts]
    seen={}; passports=[]; mappings=[]; tasks=[]; handoffs=[]
    for idx,p in enumerate(sorted(docs),1):
        txt=p.read_text(encoding='utf-8',errors='ignore')
        h=hashlib.sha256(txt.encode('utf-8','ignore')).hexdigest()
        if h in seen: continue
        seen[h]=rel(p)
        doc_id=f'LEGACY-DOC-{idx:04d}'
        phase,scores=classify(txt,rel(p))
        ch=chunks(txt)
        passport={'document_id':doc_id,'source_path':rel(p),'sha256':h,'bytes':len(txt.encode()),'line_count':txt.count('\n')+1,'classified_phase':phase,'status':'KPP_LIGHT_REPROCESSED_CANDIDATE_ONLY','created_at':ts}
        mapping={'document_id':doc_id,'source_path':rel(p),'phase_scores':scores,'primary_phase':phase,'assetization_required':['contract_check','controller_asset_check','runner_binding_check','acceptance_gate_check']}
        task={'task_id':f'KPP_TASK_{doc_id}','source_document_id':doc_id,'target_phase':phase,'status':'CANDIDATE_TASK_READY','required_review':'P00/P10 governance consumption before implementation','safety_boundary':'OBSERVE_PAPER_ONLY_NO_RUNTIME_TRADING'}
        handoff={'handoff_id':f'KPP_HANDOFF_{doc_id}','from':'KPP_BATCH_LEGACY_DOCUMENT_REPROCESS','to':phase,'status':'CANDIDATE_ONLY','document_id':doc_id,'source_path':rel(p),'chunks':len(ch)}
        passports.append(passport); mappings.append(mapping); tasks.append(task); handoffs.append(handoff)
        write_json(OUT/'document_passports'/f'{doc_id}.json',passport)
        write_json(OUT/'chunk_manifests'/f'{doc_id}.json',{'document_id':doc_id,'chunk_count':len(ch),'chunks':[{'chunk_id':f'{doc_id}-CHUNK-{i+1:03d}','char_count':len(c)} for i,c in enumerate(ch)]})
        write_yaml(OUT/'phase_mappings'/f'{doc_id}.yaml',mapping)
        write_yaml(OUT/'candidate_tasks'/f'{doc_id}.yaml',task)
        write_json(OUT/'handoff_packets'/f'{doc_id}.json',handoff)
    summary={'run_id':'KPP_BATCH_LEGACY_REPROCESS_20260513','status':'PASS','created_at':ts,'unique_documents_processed':len(passports),'duplicate_documents_skipped':len(docs)-len(passports),'output_root':rel(OUT),'safety_boundary':{'real_trade_enabled':False,'signing_enabled':False,'broadcast_enabled':False,'swap_enabled':False}}
    write_json(OUT/'reports/summary.json',summary)
    write_json(OUT/'indices/document_index.json',{'summary':summary,'documents':passports})
    write_yaml(OUT/'indices/phase_mapping_index.yaml',{'summary':summary,'mappings':mappings})
    write_yaml(OUT/'task_packages/generated_candidate_task_index.yaml',{'summary':summary,'tasks':tasks})
    write_yaml(OUT/'handoff/kpp_batch_legacy_reprocess_handoff.yaml',{'summary':summary,'handoffs':handoffs[:500]})
    print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
