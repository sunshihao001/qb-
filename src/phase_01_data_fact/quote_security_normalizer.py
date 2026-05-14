
from pathlib import Path
from .utils import get_any,MISSING,write_json
def normalize_quote_security(raw,run_dir):
    data=raw.get('raw_quote_security.json') or {}; out={'source_file':'raw_quote_security.json','quote_time':get_any(data,['quote_time','quote_fetched_at','timestamp','time']),'price_usd':get_any(data,['price_usd','quote_price_usd','price']),'liquidity_usd':get_any(data,['liquidity_usd','liquidity']),'security_status':get_any(data,['security_status','security_risk_level','risk_status'],'unknown'),'is_honeypot':get_any(data,['is_honeypot']),'buy_tax':get_any(data,['buy_tax']),'sell_tax':get_any(data,['sell_tax'])}
    miss=[k for k,v in out.items() if k not in ['source_file','security_status','is_honeypot','buy_tax','sell_tax'] and v==MISSING]; write_json(Path(run_dir)/'normalized'/'quote_security_normalized.json',out); return out,miss
