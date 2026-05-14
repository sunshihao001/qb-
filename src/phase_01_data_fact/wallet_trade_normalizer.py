
from pathlib import Path
from .utils import listify,get_any,MISSING,write_csv
def normalize_wallet_trades(raw,run_dir):
    rows=[]; miss=[]
    for i,r in enumerate(listify(raw.get('raw_wallet_trade.json'))):
        row={'source_file':'raw_wallet_trade.json','row_id':i,'wallet_address':get_any(r,['wallet_address','address','maker']),'tx_hash':get_any(r,['tx_hash','hash','signature']),'side':get_any(r,['side','type']),'amount_token':get_any(r,['amount_token','amount']),'amount_usd':get_any(r,['amount_usd','usd']),'timestamp':get_any(r,['timestamp','time','block_time'])}
        if row['wallet_address']==MISSING: miss.append(f'wallet_trade[{i}].wallet_address')
        rows.append(row)
    if not rows: rows=[{'source_file':'raw_wallet_trade.json','row_id':MISSING,'wallet_address':MISSING,'tx_hash':MISSING,'side':MISSING,'amount_token':MISSING,'amount_usd':MISSING,'timestamp':MISSING}]; miss.append('wallet_trade.rows')
    write_csv(Path(run_dir)/'normalized'/'wallet_trade_normalized.csv',rows,['source_file','row_id','wallet_address','tx_hash','side','amount_token','amount_usd','timestamp']); return rows,miss
