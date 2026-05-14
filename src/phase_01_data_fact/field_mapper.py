
from pathlib import Path
from .utils import write_csv
FIELDS=[('raw_token_basic.json','token_address','token_address','代币地址',True,False,'BLOCK'),('raw_wallet_trade.json','wallet_address','wallet_address','钱包地址',True,False,'BLOCK'),('raw_holder.json','holder_address','holder_address','持有人地址',True,False,'BLOCK'),('raw_kline.json','timestamp','timestamp','K线时间',True,False,'BLOCK'),('raw_quote_security.json','quote_time','quote_time','报价时间',True,False,'BLOCK'),('raw_top_trader.json','wallet_address','wallet_address','Top Trader 钱包',False,True,'DEGRADE'),('raw_transfer.json','from_address','from_address','转出地址',False,True,'DEGRADE')]
def write_field_mapping(run_dir):
    rows=[{'source_file':a,'source_field':b,'standard_field':c,'chinese_name':d,'required':e,'allow_missing':f,'missing_action':g,'notes':'P01 fact mapping only'} for a,b,c,d,e,f,g in FIELDS]
    p=Path(run_dir)/'field_mapping'/'field_mapping_table.csv'; write_csv(p,rows,['source_file','source_field','standard_field','chinese_name','required','allow_missing','missing_action','notes']); return p
