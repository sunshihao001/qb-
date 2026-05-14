
from pathlib import Path
from .utils import get_any,MISSING,write_json
def normalize_token_basic(raw,token,chain,run_dir):
    data=raw.get('raw_token_basic.json') or {}; out={'source_file':'raw_token_basic.json','token_address':get_any(data,['token_address','address','ca','mint'],token),'token_symbol':get_any(data,['token_symbol','symbol','ticker']),'chain':get_any(data,['chain'],chain),'decimals':get_any(data,['decimals'],0),'created_at':get_any(data,['created_at','created_time','launch_time'])}
    miss=[k for k,v in out.items() if k!='source_file' and v==MISSING]; write_json(Path(run_dir)/'normalized'/'token_basic_normalized.json',out); return out,miss
