
from pathlib import Path
from .utils import listify,get_any,MISSING,write_csv
def normalize_holders(raw,run_dir):
    rows=[]; miss=[]
    for i,r in enumerate(listify(raw.get('raw_holder.json'))):
        row={'source_file':'raw_holder.json','row_id':i,'holder_address':get_any(r,['holder_address','wallet_address','address']),'balance':get_any(r,['balance','amount']),'percent':get_any(r,['percent','pct','share'])}
        if row['holder_address']==MISSING: miss.append(f'holder[{i}].holder_address')
        rows.append(row)
    if not rows: rows=[{'source_file':'raw_holder.json','row_id':MISSING,'holder_address':MISSING,'balance':MISSING,'percent':MISSING}]; miss.append('holder.rows')
    write_csv(Path(run_dir)/'normalized'/'holder_normalized.csv',rows,['source_file','row_id','holder_address','balance','percent']); return rows,miss
