
from pathlib import Path
from .utils import get_any,MISSING,write_json
def build_token_market_context(raw,run_dir):
    tb=raw.get('raw_token_basic.json') or {}; qs=raw.get('raw_quote_security.json') or {}; out={'source_files':['raw_token_basic.json','raw_quote_security.json'],'price_usd':get_any(qs,['price_usd','quote_price_usd','price']),'liquidity_usd':get_any(qs,['liquidity_usd','liquidity']),'market_cap_usd':get_any(tb,['market_cap_usd','mcap']),'volume_24h_usd':get_any(tb,['volume_24h_usd','volume_1h_usd','volume_24h'])}
    miss=[k for k,v in out.items() if k!='source_files' and v==MISSING]; write_json(Path(run_dir)/'normalized'/'token_market_context.json',out); return out,miss
