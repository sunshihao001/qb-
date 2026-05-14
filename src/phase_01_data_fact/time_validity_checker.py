
from pathlib import Path
from .utils import parse_time,write_json
def check_time_validity(snapshot_time, quote_security, run_dir):
    snap=parse_time(snapshot_time); quote=parse_time(str(quote_security.get('quote_time'))); status='TIME_VALIDITY_OK'; reason='quote fresh'; age='missing'
    if snap and quote:
        age=abs((snap-quote).total_seconds())
        if age>86400: status='TIME_EXPIRED'; reason='quote older than 24h'
        elif age>=7200: status='TIME_STALE_WARNING'; reason='quote older than 2h'
    elif not quote: status='TIME_EXPIRED'; reason='quote_time missing'
    out={'phase':'phase_01_data_fact','snapshot_time':snapshot_time,'quote_time':quote_security.get('quote_time','missing'),'age_seconds':age,'time_validity_status':status,'reason':reason}
    write_json(Path(run_dir)/'summary'/'time_validity_report.json',out); return out
