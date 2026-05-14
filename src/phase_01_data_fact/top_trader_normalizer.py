
from pathlib import Path
from .utils import listify,get_any,MISSING,write_csv
def normalize_top_traders(raw,run_dir):
    data=raw.get('raw_top_trader.json'); miss=[]; rows=[]
    if data is None: miss.append('raw_top_trader.json'); rows=[{'source_file':'raw_top_trader.json','row_id':MISSING,'wallet_address':MISSING,'pnl_usd':MISSING,'volume_usd':MISSING}]
    else:
        for i,r in enumerate(listify(data)): rows.append({'source_file':'raw_top_trader.json','row_id':i,'wallet_address':get_any(r,['wallet_address','address']),'pnl_usd':get_any(r,['pnl_usd','pnl']),'volume_usd':get_any(r,['volume_usd','volume'])})
    write_csv(Path(run_dir)/'normalized'/'top_trader_normalized.csv',rows,['source_file','row_id','wallet_address','pnl_usd','volume_usd']); return rows,miss
