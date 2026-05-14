
from pathlib import Path
from .utils import REQUIRED_RAW, OPTIONAL_RAW, read_json
def load_raw_inputs(raw_input_dir):
    raw_dir=Path(raw_input_dir); raw={}; mr=[]; mo=[]; inv=[]
    for name in REQUIRED_RAW+OPTIONAL_RAW:
        p=raw_dir/name; req=name in REQUIRED_RAW
        if p.exists(): raw[name]=read_json(p); status='present'
        else:
            raw[name]=None; status='missing_required' if req else 'missing_optional'; (mr if req else mo).append(name)
        inv.append({'raw_file':name,'path':str(p),'required':req,'status':status})
    return {'raw_input_dir':str(raw_dir),'raw':raw,'missing_required_raw':mr,'missing_optional_raw':mo,'inventory':inv}
