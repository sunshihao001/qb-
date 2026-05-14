
from pathlib import Path
from .utils import listify,get_any,MISSING,write_csv
def normalize_kline(raw,run_dir):
    rows=[]; miss=[]
    for i,r in enumerate(listify(raw.get('raw_kline.json'))):
        row={'source_file':'raw_kline.json','row_id':i,'timestamp':get_any(r,['timestamp','time']),'open':get_any(r,['open','o']),'high':get_any(r,['high','h']),'low':get_any(r,['low','l']),'close':get_any(r,['close','c']),'volume':get_any(r,['volume','v'])}
        if row['timestamp']==MISSING: miss.append(f'kline[{i}].timestamp')
        rows.append(row)
    if not rows: rows=[{'source_file':'raw_kline.json','row_id':MISSING,'timestamp':MISSING,'open':MISSING,'high':MISSING,'low':MISSING,'close':MISSING,'volume':MISSING}]; miss.append('kline.rows')
    write_csv(Path(run_dir)/'normalized'/'kline_normalized.csv',rows,['source_file','row_id','timestamp','open','high','low','close','volume']); return rows,miss
