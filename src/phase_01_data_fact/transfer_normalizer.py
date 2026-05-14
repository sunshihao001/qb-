
from pathlib import Path
from .utils import listify,get_any,MISSING,write_csv
def normalize_transfers(raw,run_dir):
    data=raw.get('raw_transfer.json'); miss=[]; warnings=[]; rows=[]
    if data is None:
        miss.append('raw_transfer.json'); warnings=['transfer_missing_no_distribution_inference','transfer_missing_no_backflow_inference']; rows=[{'source_file':'raw_transfer.json','row_id':MISSING,'from_address':MISSING,'to_address':MISSING,'amount_token':MISSING,'tx_hash':MISSING,'timestamp':MISSING,'inference_guard':'missing_transfer_no_distribution_or_backflow_judgement'}]
    else:
        for i,r in enumerate(listify(data)): rows.append({'source_file':'raw_transfer.json','row_id':i,'from_address':get_any(r,['from_address','from']),'to_address':get_any(r,['to_address','to']),'amount_token':get_any(r,['amount_token','amount']),'tx_hash':get_any(r,['tx_hash','hash','signature']),'timestamp':get_any(r,['timestamp','time']),'inference_guard':'p01_fact_only_no_distribution_or_backflow_judgement'})
    write_csv(Path(run_dir)/'normalized'/'transfer_normalized.csv',rows,['source_file','row_id','from_address','to_address','amount_token','tx_hash','timestamp','inference_guard']); return rows,miss,warnings
