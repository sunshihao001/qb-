from __future__ import annotations

from statistics import mean
from typing import Any, Iterable, List, Mapping, Optional, Sequence, Set

from .quantitative_structure_models import DominantCostZoneResult, WalletCostResult


def _first_present(row: Mapping[str, Any], keys: Sequence[str], default: Any = None) -> Any:
    for key in keys:
        if '.' in key:
            value: Any = row
            ok = True
            for part in key.split('.'):
                if isinstance(value, Mapping) and part in value:
                    value = value[part]
                else:
                    ok = False
                    break
            if ok and value not in (None, '', [], {}):
                return value
            continue
        value = row.get(key)
        if value not in (None, '', [], {}):
            return value
    return default


def _as_float(value: Any, default: Optional[float] = None) -> Optional[float]:
    try:
        if value in (None, ''):
            return default
        return float(str(value).replace('%', '').replace(',', '').strip())
    except (TypeError, ValueError):
        return default


def _as_int(value: Any, default: Optional[int] = None) -> Optional[int]:
    number = _as_float(value, None)
    if number is None:
        return default
    return int(number)


def _safe_div(numerator: Optional[float], denominator: Optional[float]) -> Optional[float]:
    if numerator is None or denominator in (None, 0):
        return None
    return numerator / denominator


def _role_text(row: Mapping[str, Any]) -> str:
    return str(row.get('role_name') or row.get('role') or row.get('role_code') or '')


def _is_distribution_receiver(row: Mapping[str, Any]) -> bool:
    role = _role_text(row)
    role_code = str(row.get('role_code') or '')
    has_token_source = bool(_first_present(row, ['token_source_address', 'token_transfer_in.address', 'token_in_address'], ''))
    return (
        '分发接收' in role
        or 'Token 接收' in role
        or role_code in {'DIST_RECV', 'TOKEN_RECEIVER'}
        or (bool(row.get('transfer_in')) and has_token_source)
    )


def _is_token_transfer_only(row: Mapping[str, Any], buy_amount_usd: Optional[float], buy_token_amount: Optional[float]) -> bool:
    has_token_source = bool(_first_present(row, ['token_source_address', 'token_transfer_in.address', 'token_in_address'], ''))
    transfer_in = bool(row.get('transfer_in'))
    return (transfer_in or has_token_source) and not (buy_amount_usd and buy_token_amount)


def _confidence_for_active_buy(*, buy_count: Optional[int], current_balance: Optional[float], sell_token_amount: Optional[float], first_cost: Optional[float], last_cost: Optional[float]) -> float:
    score = 0.65
    if buy_count is not None:
        if buy_count >= 3:
            score += 0.10
        elif buy_count >= 1:
            score += 0.05
    if current_balance not in (None, 0):
        score += 0.08
    if sell_token_amount not in (None, 0):
        score += 0.05
    if first_cost is not None and last_cost is not None:
        score += 0.07
    return round(min(score, 0.95), 4)


def calculate_wallet_cost(row: Mapping[str, Any]) -> WalletCostResult:
    """Calculate one wallet's directly confirmable cost from active buy fields.

    Active buy wallets use: total buy amount USD / total bought token amount.
    Token-transfer and distribution receiver rows must not treat transfer price as cost.
    """
    wallet_address = str(_first_present(row, ['wallet_address', 'address', '钱包地址'], '') or '')
    token_address = str(_first_present(row, ['token_address', '代币地址', 'mint'], '') or '')
    buy_amount_usd = _as_float(_first_present(row, ['buy_amount_usd', 'buy_usd', 'buy_volume_usd', 'total_buy_usd', 'history_bought_cost'], None), None)
    buy_token_amount = _as_float(_first_present(row, ['buy_token_amount', 'buy_amount_cur', 'current_buy_amount', 'total_buy_token_amount'], None), None)
    first_buy_time = _first_present(row, ['first_buy_time', 'first_buy_timestamp', 'start_holding_at', '首次买入时间'], None)
    buy_count = _as_int(_first_present(row, ['buy_count', 'buy_tx_count_cur', 'buy_tx_count'], None), None)
    sell_amount_usd = _as_float(_first_present(row, ['sell_amount_usd', 'sell_usd', 'sell_volume_usd', 'total_sell_usd', 'history_sold_income'], None), None)
    sell_token_amount = _as_float(_first_present(row, ['sell_token_amount', 'sell_amount_cur', 'current_sell_amount', 'total_sell_token_amount'], None), None)
    current_balance = _as_float(_first_present(row, ['current_balance', 'holding_amount', 'balance', 'amount_cur', 'amount'], None), None)

    first_buy_cost = _as_float(_first_present(row, ['wallet_first_buy_cost', 'first_buy_cost'], None), None)
    if first_buy_cost is None:
        first_buy_cost = _safe_div(
            _as_float(_first_present(row, ['first_buy_amount_usd'], None), None),
            _as_float(_first_present(row, ['first_buy_token_amount'], None), None),
        )
    last_buy_cost = _as_float(_first_present(row, ['wallet_last_buy_cost', 'last_buy_cost'], None), None)
    if last_buy_cost is None:
        last_buy_cost = _safe_div(
            _as_float(_first_present(row, ['last_buy_amount_usd'], None), None),
            _as_float(_first_present(row, ['last_buy_token_amount'], None), None),
        )

    wallet_avg_cost = _safe_div(buy_amount_usd, buy_token_amount)
    if wallet_avg_cost is not None:
        if first_buy_cost is None:
            first_buy_cost = wallet_avg_cost
        if last_buy_cost is None:
            last_buy_cost = wallet_avg_cost
        return WalletCostResult(
            wallet_address=wallet_address,
            token_address=token_address,
            wallet_avg_cost=wallet_avg_cost,
            wallet_first_buy_cost=first_buy_cost,
            wallet_last_buy_cost=last_buy_cost,
            wallet_cost_confidence=_confidence_for_active_buy(
                buy_count=buy_count,
                current_balance=current_balance,
                sell_token_amount=sell_token_amount,
                first_cost=first_buy_cost,
                last_cost=last_buy_cost,
            ),
            buy_amount_usd=buy_amount_usd,
            buy_token_amount=buy_token_amount,
            first_buy_time=str(first_buy_time) if first_buy_time is not None else None,
            buy_count=buy_count,
            sell_amount_usd=sell_amount_usd,
            sell_token_amount=sell_token_amount,
            current_balance=current_balance,
            cost_source_type_zh='主动买入成本',
            wallet_cost_status_zh='成本可由主动买入估算',
            wallet_cost_notes_zh='钱包平均买入成本按总买入金额除以总买入 token 数量计算。',
        )

    if _is_distribution_receiver(row):
        status = '成本不可直接确认'
        note = '分发接收钱包的成本不能由转入价格确认，必须保留成本未知。'
        source = '分发接收成本未知'
    elif _is_token_transfer_only(row, buy_amount_usd, buy_token_amount):
        status = '成本不可直接确认'
        note = 'Token 转入钱包不能直接使用转入价格作为成本。'
        source = 'Token 转入成本未知'
    else:
        status = '成本证据不足'
        note = '缺少主动买入金额或买入 token 数量，无法计算单钱包平均买入成本。'
        source = '来源未知'

    return WalletCostResult(
        wallet_address=wallet_address,
        token_address=token_address,
        wallet_avg_cost=None,
        wallet_first_buy_cost=None,
        wallet_last_buy_cost=None,
        wallet_cost_confidence=0.0,
        buy_amount_usd=buy_amount_usd,
        buy_token_amount=buy_token_amount,
        first_buy_time=str(first_buy_time) if first_buy_time is not None else None,
        buy_count=buy_count,
        sell_amount_usd=sell_amount_usd,
        sell_token_amount=sell_token_amount,
        current_balance=current_balance,
        cost_source_type_zh=source,
        wallet_cost_status_zh=status,
        wallet_cost_notes_zh=note,
    )


def calculate_wallet_costs(rows: Iterable[Mapping[str, Any]]) -> List[WalletCostResult]:
    return [calculate_wallet_cost(row) for row in rows]


def _weighted_mid(costs: List[WalletCostResult]) -> Optional[float]:
    weighted_sum = 0.0
    weight_sum = 0.0
    for item in costs:
        if item.wallet_avg_cost is None:
            continue
        weight = item.buy_token_amount or item.current_balance or 1.0
        weighted_sum += item.wallet_avg_cost * weight
        weight_sum += weight
    if weight_sum <= 0:
        return None
    return weighted_sum / weight_sum


def _percentile(values: List[float], percentile: float) -> Optional[float]:
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    rank = (len(ordered) - 1) * percentile
    lower = int(rank)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = rank - lower
    return ordered[lower] + (ordered[upper] - ordered[lower]) * fraction


def _wallet_group_id(row: Mapping[str, Any]) -> str:
    return str(_first_present(row, ['same_source_group_id', 'group_id', 'same_source_group', '组ID'], '') or '')


def _group_wallet_addresses(group: Mapping[str, Any]) -> Set[str]:
    addresses: Set[str] = set()
    raw_addresses = _first_present(group, ['wallet_addresses', 'wallets', 'members', 'member_wallets'], [])
    if isinstance(raw_addresses, str):
        addresses.add(raw_addresses)
    elif isinstance(raw_addresses, Iterable):
        for item in raw_addresses:
            if isinstance(item, Mapping):
                address = _first_present(item, ['wallet_address', 'address', '钱包地址'], '')
            else:
                address = item
            if address not in (None, ''):
                addresses.add(str(address))
    return addresses


def _same_source_group_ids(groups: List[Mapping[str, Any]]) -> Set[str]:
    group_ids: Set[str] = set()
    for group in groups:
        group_id = str(_first_present(group, ['same_source_group_id', 'group_id', 'same_source_group', '组ID'], '') or '')
        if group_id:
            group_ids.add(group_id)
    return group_ids


def _is_structure_cost_candidate(row: Mapping[str, Any]) -> bool:
    role_name = _role_text(row)
    role_code = str(row.get('role_code') or '')
    address_base_type = str(row.get('address_base_type') or '').lower()
    funding_source_type = str(row.get('funding_source_type') or '').lower()
    note = str(row.get('gmgn_note') or '').lower()
    if role_name in {'疑似接盘鲸鱼', '噪音钱包', '基础设施地址', '普通参与者'}:
        return False
    if role_code in {'BAG_WHALE', 'NOISE', 'INFRA'}:
        return False
    if any(marker in address_base_type for marker in ['exchange', 'router', 'infra', 'lp']):
        return False
    if any(marker in note for marker in ['交易所', '路由', '基础设施', '接盘']):
        return False
    if role_name in {
        '疑似早期买入钱包',
        '疑似临时执行钱包',
        '疑似同源执行组成员',
        '疑似核心资金源候选',
        '疑似结果钱包',
        '疑似新钱包狙击',
    }:
        return True
    if not role_name and _first_present(row, ['buy_amount_usd', 'buy_usd', 'buy_volume_usd', 'total_buy_usd', 'history_bought_cost'], None) is not None and _first_present(row, ['buy_token_amount', 'buy_amount_cur', 'current_buy_amount', 'total_buy_token_amount'], None) is not None:
        return True
    if row.get('transfer_in') and not _first_present(row, ['token_source_address', 'token_transfer_in.address', 'token_in_address'], ''):
        return True
    return False


def _row_lookup_by_wallet(normalized_rows: List[Mapping[str, Any]]) -> Dict[str, Mapping[str, Any]]:
    return {
        str(_first_present(row, ['wallet_address', 'address', '钱包地址'], '') or ''): row
        for row in normalized_rows
    }


def _wallet_cost_rows(wallet_costs: List[WalletCostResult], normalized_rows: List[Mapping[str, Any]]) -> List[tuple[WalletCostResult, Mapping[str, Any]]]:
    row_by_wallet = _row_lookup_by_wallet(normalized_rows)
    pairs: List[tuple[WalletCostResult, Mapping[str, Any]]] = []
    for item in wallet_costs:
        row = row_by_wallet.get(item.wallet_address)
        if row is None:
            continue
        if _is_structure_cost_candidate(row):
            pairs.append((item, row))
    return pairs


def _select_same_source_group_costs(
    *,
    normalized_rows: List[Mapping[str, Any]],
    wallet_costs: List[WalletCostResult],
    same_source_groups: List[Mapping[str, Any]],
) -> List[WalletCostResult]:
    if not same_source_groups:
        return []

    group_ids = _same_source_group_ids(same_source_groups)
    group_addresses: Set[str] = set()
    for group in same_source_groups:
        group_addresses.update(_group_wallet_addresses(group))

    row_by_wallet = _row_lookup_by_wallet(normalized_rows)

    selected: List[WalletCostResult] = []
    for item in wallet_costs:
        if item.wallet_avg_cost is None:
            continue
        row = row_by_wallet.get(item.wallet_address, {})
        row_group_id = _wallet_group_id(row)
        if not ((group_ids and row_group_id in group_ids) or (group_addresses and item.wallet_address in group_addresses)):
            continue
        if _is_structure_cost_candidate(row):
            selected.append(item)
    return selected


def _calculate_same_source_group_cost_zone(
    *,
    normalized_rows: List[Mapping[str, Any]],
    wallet_costs: List[WalletCostResult],
    same_source_groups: List[Mapping[str, Any]],
) -> tuple[Optional[float], Optional[float], Optional[float], Optional[float]]:
    group_costs = _select_same_source_group_costs(
        normalized_rows=normalized_rows,
        wallet_costs=wallet_costs,
        same_source_groups=same_source_groups,
    )
    if not group_costs:
        return None, None, None, None

    cost_values = [item.wallet_avg_cost for item in group_costs if item.wallet_avg_cost is not None]
    buy_amount_total = sum(item.buy_amount_usd or 0.0 for item in group_costs)
    buy_token_total = sum(item.buy_token_amount or 0.0 for item in group_costs)
    group_mid = _safe_div(buy_amount_total, buy_token_total) or _weighted_mid(group_costs) or mean(cost_values)
    group_low = _percentile(cost_values, 0.25)
    group_high = _percentile(cost_values, 0.75)
    confidence = mean([item.wallet_cost_confidence for item in group_costs])
    if len(group_costs) >= 3:
        confidence += 0.06
    elif len(group_costs) >= 2:
        confidence += 0.03
    return group_low, group_mid, group_high, round(min(confidence, 0.98), 4)


def _cost_position_status(current_price: Optional[float], dominant_cost_mid: Optional[float]) -> tuple[Optional[float], str]:
    if current_price is None or dominant_cost_mid in (None, 0):
        return None, '成本区证据不足'
    pct = round((current_price - dominant_cost_mid) / dominant_cost_mid * 100, 4)
    if pct < -3:
        status = '当前价格跌破主导侧成本区'
    elif abs(pct) <= 5:
        status = '当前价格接近主导侧成本区'
    elif pct <= 30:
        status = '当前价格略高于主导侧成本区'
    else:
        status = '当前价格大幅高于主导侧成本区'
    return pct, status


def _dominant_cost_deviation_status(current_price: Optional[float], dominant_cost_mid: Optional[float]) -> tuple[Optional[float], str]:
    if current_price is None or dominant_cost_mid in (None, 0):
        return None, '成本区证据不足'
    deviation = round(current_price / dominant_cost_mid - 1, 4)
    if deviation < -0.10:
        status = '跌破成本区'
    elif deviation <= 0.20:
        status = '成本附近'
    elif deviation <= 0.80:
        status = '轻度盈利区'
    elif deviation <= 2.00:
        status = '明显盈利区'
    else:
        status = '高派发风险区'
    return deviation, status


def _format_cost_value(value: Optional[float]) -> str:
    if value is None:
        return ''
    return f'{value:g}'


def _volume_weighted_cost_from_kline(kline_rows: Sequence[Mapping[str, Any]]) -> Optional[float]:
    weighted_sum = 0.0
    volume_sum = 0.0
    for row in kline_rows:
        price = _as_float(_first_present(row, ['hlc3', 'typical_price', 'close', 'price'], None), None)
        volume = _as_float(_first_present(row, ['volume', 'volume_usd', 'quote_volume', 'amount'], None), None)
        if price is None or volume is None or volume <= 0:
            continue
        weighted_sum += price * volume
        volume_sum += volume
    return _safe_div(weighted_sum, volume_sum)


def _kline_price_range(kline_rows: Sequence[Mapping[str, Any]]) -> tuple[Optional[float], Optional[float]]:
    prices: List[float] = []
    for row in kline_rows:
        volume = _as_float(_first_present(row, ['volume', 'volume_usd', 'quote_volume', 'amount'], None), None)
        if volume is not None and volume <= 0:
            continue
        low = _as_float(_first_present(row, ['low', 'close', 'price'], None), None)
        high = _as_float(_first_present(row, ['high', 'close', 'price'], None), None)
        if low is not None:
            prices.append(low)
        if high is not None:
            prices.append(high)
    if not prices:
        return None, None
    return min(prices), max(prices)


def _market_cost_proxy(
    *,
    market_cost_mid: Optional[float],
    box_cost_mid: Optional[float],
    market_structure: Optional[Mapping[str, Any]],
    kline_rows: Optional[Sequence[Mapping[str, Any]]],
) -> tuple[Optional[float], Optional[float], str]:
    market_structure = market_structure or {}
    kline_rows = kline_rows or []

    poc = _as_float(_first_present(market_structure, ['POC_price', 'poc_price', 'poc', 'POC'], None), None)
    vah = _as_float(_first_present(market_structure, ['VAH_price', 'vah_price', 'VAH'], None), None)
    val = _as_float(_first_present(market_structure, ['VAL_price', 'val_price', 'VAL'], None), None)
    avwap = _as_float(_first_present(market_structure, ['latest_AVWAP', 'avwap', 'AVWAP', 'anchored_vwap'], None), None)

    resolved_box_mid = box_cost_mid
    if resolved_box_mid is None and val is not None and vah is not None:
        resolved_box_mid = (val + vah) / 2
    if resolved_box_mid is None:
        resolved_box_mid = poc

    vwap_mid = _volume_weighted_cost_from_kline(kline_rows)
    resolved_market_mid = market_cost_mid
    if resolved_market_mid is None:
        candidates = [value for value in [poc, avwap, vwap_mid, resolved_box_mid] if value is not None]
        resolved_market_mid = round(mean(candidates), 10) if candidates else None

    zone_low = val
    zone_high = vah
    if zone_low is None or zone_high is None:
        zone_low, zone_high = _kline_price_range(kline_rows)

    volume_cost_zone = ''
    if zone_low is not None and zone_high is not None:
        details: List[str] = []
        if poc is not None:
            details.append(f'POC: {_format_cost_value(poc)}')
        if avwap is not None:
            details.append(f'AVWAP: {_format_cost_value(avwap)}')
        if not details and resolved_market_mid is not None:
            details.append(f'成交量加权中枢: {_format_cost_value(resolved_market_mid)}')
        suffix = f'（{"，".join(details)}）' if details else ''
        volume_cost_zone = f'{_format_cost_value(zone_low)} ~ {_format_cost_value(zone_high)}{suffix}'

    return resolved_market_mid, resolved_box_mid, volume_cost_zone


def calculate_dominant_cost_zone(
    *,
    normalized_rows: List[Mapping[str, Any]],
    same_source_groups: List[Mapping[str, Any]],
    current_price: Optional[float] = None,
    market_cost_mid: Optional[float] = None,
    box_cost_mid: Optional[float] = None,
    market_structure: Optional[Mapping[str, Any]] = None,
    kline_rows: Optional[Sequence[Mapping[str, Any]]] = None,
) -> DominantCostZoneResult:
    """Calculate the first-pass suspicious dominant-side cost zone.

    This first implementation uses only directly confirmable active-buy wallet costs.
    Same-source group aggregation can consume these wallet-level costs in the next layer.
    """
    wallet_costs = calculate_wallet_costs(normalized_rows)
    resolved_market_cost_mid, resolved_box_cost_mid, volume_cost_zone_zh = _market_cost_proxy(
        market_cost_mid=market_cost_mid,
        box_cost_mid=box_cost_mid,
        market_structure=market_structure,
        kline_rows=kline_rows,
    )
    cost_rows = _wallet_cost_rows(wallet_costs, normalized_rows)
    active_costs = [item for item, _ in cost_rows]
    if not active_costs:
        return DominantCostZoneResult(
            market_cost_mid=resolved_market_cost_mid,
            market_cost_mid_zh=resolved_market_cost_mid,
            box_cost_mid=resolved_box_cost_mid,
            box_cost_mid_zh=resolved_box_cost_mid,
            volume_cost_zone_zh=volume_cost_zone_zh,
            current_price=current_price,
            cost_position_status_zh='成本区证据不足',
            cost_evidence_grade_zh='证据不足',
            cost_notes_zh='没有足够的结构侧候选钱包成本，Token 转入、接盘鲸鱼或噪音/基础设施钱包不能直接确认成本。',
            wallet_costs=wallet_costs,
        )

    avg_values = [item.wallet_avg_cost for item in active_costs if item.wallet_avg_cost is not None]
    first_values = [item.wallet_first_buy_cost for item in active_costs if item.wallet_first_buy_cost is not None]
    last_values = [item.wallet_last_buy_cost for item in active_costs if item.wallet_last_buy_cost is not None]
    dominant_low = min(avg_values)
    dominant_high = max(avg_values)
    dominant_mid = _weighted_mid(active_costs) or mean(avg_values)
    same_source_group_cost_low, same_source_group_cost_mid, same_source_group_cost_high, same_source_group_cost_confidence = _calculate_same_source_group_cost_zone(
        normalized_rows=normalized_rows,
        wallet_costs=wallet_costs,
        same_source_groups=same_source_groups,
    )
    confidence = mean([item.wallet_cost_confidence for item in active_costs])
    if len(active_costs) >= 3:
        confidence = min(confidence + 0.05, 0.98)
    price_pct, status = _cost_position_status(current_price, dominant_mid)
    dominant_cost_deviation_rate, dominant_cost_deviation_status_zh = _dominant_cost_deviation_status(current_price, dominant_mid)
    evidence_grade = '结构侧候选钱包主动买入成本证据' if len(active_costs) >= 2 else '单个结构侧候选钱包主动买入成本证据'

    return DominantCostZoneResult(
        wallet_avg_cost=dominant_mid,
        wallet_first_buy_cost=mean(first_values) if first_values else None,
        wallet_last_buy_cost=mean(last_values) if last_values else None,
        wallet_cost_confidence=round(confidence, 4),
        same_source_group_cost_low=same_source_group_cost_low,
        same_source_group_cost_mid=same_source_group_cost_mid,
        same_source_group_cost_high=same_source_group_cost_high,
        same_source_group_cost_confidence=same_source_group_cost_confidence,
        dominant_cost_low=dominant_low,
        dominant_cost_mid=dominant_mid,
        dominant_cost_high=dominant_high,
        dominant_cost_confidence=round(confidence, 4),
        dominant_cost_low_zh=dominant_low,
        dominant_cost_mid_zh=dominant_mid,
        dominant_cost_high_zh=dominant_high,
        dominant_cost_confidence_zh=round(confidence, 4),
        market_cost_mid=resolved_market_cost_mid,
        market_cost_mid_zh=resolved_market_cost_mid,
        box_cost_mid=resolved_box_cost_mid,
        box_cost_mid_zh=resolved_box_cost_mid,
        volume_cost_zone_zh=volume_cost_zone_zh,
        current_price=current_price,
        price_to_dominant_cost_pct=price_pct,
        dominant_cost_deviation_rate=dominant_cost_deviation_rate,
        dominant_cost_deviation_status_zh=dominant_cost_deviation_status_zh,
        cost_position_status_zh=status,
        cost_evidence_grade_zh=evidence_grade,
        cost_notes_zh='当前成本区仅使用结构侧候选钱包的可确认主动买入成本；Token 转入、接盘鲸鱼、噪音钱包和基础设施地址保留为排除项。',
        wallet_costs=wallet_costs,
    )
